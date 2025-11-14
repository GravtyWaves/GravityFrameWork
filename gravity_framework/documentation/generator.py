"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/documentation/generator.py
PURPOSE: Framework component
DESCRIPTION: Component of the Gravity Framework for microservices orchestration

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""


from typing import Dict, List, Any, Optional, Set
from pathlib import Path
import ast
import inspect
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Analyze Python code to extract structure for documentation."""
    
    def __init__(self, project_path: Path):
        """Initialize code analyzer."""
        self.project_path = Path(project_path)
        self.modules: Dict[str, Any] = {}
        self.classes: Dict[str, Any] = {}
        self.functions: Dict[str, Any] = {}
        self.relationships: List[Dict[str, str]] = []
    
    def analyze_project(self) -> Dict[str, Any]:
        """
        Analyze entire project structure.
        
        Returns:
            Dictionary with project analysis
        """
        logger.info(f"Analyzing project at {self.project_path}")
        
        # Find all Python files
        python_files = list(self.project_path.rglob("*.py"))
        
        # Filter out virtual env and cache
        python_files = [
            f for f in python_files
            if '.venv' not in str(f) and '__pycache__' not in str(f)
        ]
        
        logger.info(f"Found {len(python_files)} Python files")
        
        # Analyze each file
        for file_path in python_files:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                logger.error(f"Failed to analyze {file_path}: {e}")
        
        return {
            'modules': self.modules,
            'classes': self.classes,
            'functions': self.functions,
            'relationships': self.relationships
        }
    
    def _analyze_file(self, file_path: Path) -> None:
        """Analyze single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            module_name = self._get_module_name(file_path)
            
            # Extract module docstring
            module_doc = ast.get_docstring(tree) or ""
            
            self.modules[module_name] = {
                'path': str(file_path),
                'docstring': module_doc,
                'classes': [],
                'functions': []
            }
            
            # Visit all nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self._analyze_class(node, module_name, file_path)
                elif isinstance(node, ast.FunctionDef):
                    if not self._is_method(node):
                        self._analyze_function(node, module_name)
        
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
    
    def _get_module_name(self, file_path: Path) -> str:
        """Get module name from file path."""
        rel_path = file_path.relative_to(self.project_path)
        parts = list(rel_path.parts[:-1]) + [rel_path.stem]
        return '.'.join(parts)
    
    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method (has self/cls parameter)."""
        if not node.args.args:
            return False
        first_arg = node.args.args[0].arg
        return first_arg in ('self', 'cls')
    
    def _analyze_class(self, node: ast.ClassDef, module_name: str, file_path: Path) -> None:
        """Analyze class definition."""
        class_name = f"{module_name}.{node.name}"
        
        # Extract docstring
        docstring = ast.get_docstring(node) or ""
        
        # Extract base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{base.value.id}.{base.attr}")
        
        # Extract methods
        methods = []
        attributes = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = {
                    'name': item.name,
                    'docstring': ast.get_docstring(item) or "",
                    'args': [arg.arg for arg in item.args.args],
                    'returns': self._get_return_type(item)
                }
                methods.append(method_info)
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    attributes.append({
                        'name': item.target.id,
                        'type': self._get_annotation(item.annotation)
                    })
        
        self.classes[class_name] = {
            'name': node.name,
            'module': module_name,
            'docstring': docstring,
            'bases': bases,
            'methods': methods,
            'attributes': attributes,
            'file': str(file_path)
        }
        
        # Track relationships
        for base in bases:
            self.relationships.append({
                'type': 'inheritance',
                'from': class_name,
                'to': base
            })
        
        self.modules[module_name]['classes'].append(node.name)
    
    def _analyze_function(self, node: ast.FunctionDef, module_name: str) -> None:
        """Analyze function definition."""
        func_name = f"{module_name}.{node.name}"
        
        self.functions[func_name] = {
            'name': node.name,
            'module': module_name,
            'docstring': ast.get_docstring(node) or "",
            'args': [arg.arg for arg in node.args.args],
            'returns': self._get_return_type(node)
        }
        
        self.modules[module_name]['functions'].append(node.name)
    
    def _get_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """Get return type annotation."""
        if node.returns:
            return self._get_annotation(node.returns)
        return None
    
    def _get_annotation(self, node) -> str:
        """Get type annotation as string."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Subscript):
            value = self._get_annotation(node.value)
            slice_val = self._get_annotation(node.slice)
            return f"{value}[{slice_val}]"
        return "Any"


class MermaidDiagramGenerator:
    """Generate Mermaid diagrams from code analysis."""
    
    def __init__(self, analysis: Dict[str, Any]):
        """Initialize diagram generator."""
        self.analysis = analysis
    
    def generate_class_diagram(self) -> str:
        """
        Generate UML class diagram in Mermaid format.
        
        Returns:
            Mermaid diagram code
        """
        lines = [
            "```mermaid",
            "classDiagram",
            ""
        ]
        
        # Add classes
        for class_name, class_info in self.analysis['classes'].items():
            simple_name = class_info['name']
            
            # Class definition
            lines.append(f"    class {simple_name} {{")
            
            # Attributes
            for attr in class_info['attributes']:
                attr_type = attr.get('type', 'Any')
                lines.append(f"        +{attr_type} {attr['name']}")
            
            # Methods
            for method in class_info['methods']:
                args = ', '.join(method['args'][1:])  # Skip self
                returns = method.get('returns', 'None')
                lines.append(f"        +{method['name']}({args}) {returns}")
            
            lines.append("    }")
            lines.append("")
        
        # Add relationships
        for rel in self.analysis['relationships']:
            if rel['type'] == 'inheritance':
                from_class = rel['from'].split('.')[-1]
                to_class = rel['to'].split('.')[-1]
                lines.append(f"    {to_class} <|-- {from_class}")
        
        lines.append("```")
        
        return '\n'.join(lines)
    
    def generate_erd(self, models_module: str = 'models') -> str:
        """
        Generate Entity-Relationship Diagram.
        
        Args:
            models_module: Name of models module
            
        Returns:
            Mermaid ER diagram
        """
        lines = [
            "```mermaid",
            "erDiagram",
            ""
        ]
        
        # Find model classes (those with __tablename__)
        entities = []
        
        for class_name, class_info in self.analysis['classes'].items():
            if models_module in class_info['module']:
                simple_name = class_info['name']
                entities.append(simple_name)
                
                # Entity definition
                lines.append(f"    {simple_name} {{")
                
                for attr in class_info['attributes']:
                    attr_type = attr.get('type', 'string')
                    lines.append(f"        {attr_type} {attr['name']}")
                
                lines.append("    }")
                lines.append("")
        
        # Add relationships (this is simplified, real implementation would parse ForeignKey)
        # For now, we'll add placeholder relationships
        if len(entities) >= 2:
            lines.append(f"    {entities[0]} ||--o{{ {entities[1]} : has")
        
        lines.append("```")
        
        return '\n'.join(lines)
    
    def generate_sequence_diagram(self, flow_name: str, steps: List[Dict[str, str]]) -> str:
        """
        Generate sequence diagram for a workflow.
        
        Args:
            flow_name: Name of the flow
            steps: List of steps with 'from', 'to', 'message'
            
        Returns:
            Mermaid sequence diagram
        """
        lines = [
            "```mermaid",
            "sequenceDiagram",
            f"    title {flow_name}",
            ""
        ]
        
        for step in steps:
            from_actor = step['from']
            to_actor = step['to']
            message = step['message']
            lines.append(f"    {from_actor}->>+{to_actor}: {message}")
        
        lines.append("```")
        
        return '\n'.join(lines)
    
    def generate_flowchart(self, process_name: str, steps: List[Dict[str, Any]]) -> str:
        """
        Generate flowchart/activity diagram.
        
        Args:
            process_name: Name of the process
            steps: List of steps with 'id', 'type', 'text', 'next'
            
        Returns:
            Mermaid flowchart
        """
        lines = [
            "```mermaid",
            "flowchart TD",
            f"    title {process_name}",
            ""
        ]
        
        for step in steps:
            step_id = step['id']
            step_type = step.get('type', 'process')
            text = step['text']
            
            # Different shapes for different types
            if step_type == 'start':
                lines.append(f"    {step_id}([{text}])")
            elif step_type == 'end':
                lines.append(f"    {step_id}([{text}])")
            elif step_type == 'decision':
                lines.append(f"    {step_id}{{{text}}}")
            else:
                lines.append(f"    {step_id}[{text}]")
            
            # Add connections
            if 'next' in step:
                for next_step in step['next']:
                    label = next_step.get('label', '')
                    target = next_step['id']
                    if label:
                        lines.append(f"    {step_id} -->|{label}| {target}")
                    else:
                        lines.append(f"    {step_id} --> {target}")
        
        lines.append("```")
        
        return '\n'.join(lines)


class DocumentationGenerator:
    """Generate comprehensive project documentation."""
    
    def __init__(self, project_path: Path, ai_assistant=None):
        """Initialize documentation generator."""
        self.project_path = Path(project_path)
        self.ai = ai_assistant
        self.analyzer = CodeAnalyzer(project_path)
        self.analysis: Dict[str, Any] = {}
    
    def generate_all(self) -> Dict[str, str]:
        """
        Generate all documentation.
        
        Returns:
            Dictionary with all generated docs
        """
        logger.info("Starting documentation generation...")
        
        # Analyze code
        self.analysis = self.analyzer.analyze_project()
        
        # Generate diagrams
        diagram_gen = MermaidDiagramGenerator(self.analysis)
        
        docs = {
            'class_diagram': diagram_gen.generate_class_diagram(),
            'erd': diagram_gen.generate_erd(),
            'api_docs': self._generate_api_docs(),
            'architecture': self._generate_architecture_docs(),
            'module_docs': self._generate_module_docs()
        }
        
        logger.info("Documentation generation complete!")
        
        return docs
    
    def _generate_api_docs(self) -> str:
        """Generate API documentation."""
        lines = [
            "# API Documentation",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Modules",
            ""
        ]
        
        for module_name, module_info in self.analysis['modules'].items():
            if '__pycache__' in module_name or 'test' in module_name:
                continue
            
            lines.append(f"### `{module_name}`")
            lines.append("")
            
            if module_info['docstring']:
                lines.append(module_info['docstring'])
                lines.append("")
            
            # Classes
            if module_info['classes']:
                lines.append("**Classes:**")
                for class_name in module_info['classes']:
                    full_name = f"{module_name}.{class_name}"
                    if full_name in self.analysis['classes']:
                        class_info = self.analysis['classes'][full_name]
                        lines.append(f"- `{class_name}`: {class_info['docstring'].split('.')[0]}")
                lines.append("")
            
            # Functions
            if module_info['functions']:
                lines.append("**Functions:**")
                for func_name in module_info['functions']:
                    full_name = f"{module_name}.{func_name}"
                    if full_name in self.analysis['functions']:
                        func_info = self.analysis['functions'][full_name]
                        args = ', '.join(func_info['args'])
                        lines.append(f"- `{func_name}({args})`: {func_info['docstring'].split('.')[0]}")
                lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_architecture_docs(self) -> str:
        """Generate architecture documentation."""
        lines = [
            "# Architecture Documentation",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Project Structure",
            ""
        ]
        
        # Group by top-level packages
        packages: Dict[str, List[str]] = {}
        
        for module_name in self.analysis['modules'].keys():
            if '__pycache__' in module_name:
                continue
            
            parts = module_name.split('.')
            if len(parts) > 1:
                package = parts[0]
                if package not in packages:
                    packages[package] = []
                packages[package].append(module_name)
        
        for package, modules in sorted(packages.items()):
            lines.append(f"### `{package}/`")
            lines.append("")
            
            for module in sorted(modules):
                indent = "  " * (len(module.split('.')) - 1)
                module_name = module.split('.')[-1]
                lines.append(f"{indent}- `{module_name}.py`")
            
            lines.append("")
        
        # Statistics
        lines.extend([
            "## Statistics",
            "",
            f"- **Total Modules:** {len(self.analysis['modules'])}",
            f"- **Total Classes:** {len(self.analysis['classes'])}",
            f"- **Total Functions:** {len(self.analysis['functions'])}",
            ""
        ])
        
        return '\n'.join(lines)
    
    def _generate_module_docs(self) -> str:
        """Generate detailed module documentation."""
        lines = [
            "# Module Documentation",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            ""
        ]
        
        for class_name, class_info in sorted(self.analysis['classes'].items()):
            if '__pycache__' in class_name:
                continue
            
            lines.append(f"## Class: `{class_info['name']}`")
            lines.append("")
            lines.append(f"**Module:** `{class_info['module']}`")
            lines.append("")
            
            if class_info['docstring']:
                lines.append(class_info['docstring'])
                lines.append("")
            
            # Inheritance
            if class_info['bases']:
                lines.append("**Inherits from:**")
                for base in class_info['bases']:
                    lines.append(f"- `{base}`")
                lines.append("")
            
            # Attributes
            if class_info['attributes']:
                lines.append("**Attributes:**")
                lines.append("")
                lines.append("| Name | Type |")
                lines.append("|------|------|")
                for attr in class_info['attributes']:
                    lines.append(f"| `{attr['name']}` | `{attr.get('type', 'Any')}` |")
                lines.append("")
            
            # Methods
            if class_info['methods']:
                lines.append("**Methods:**")
                lines.append("")
                
                for method in class_info['methods']:
                    args = ', '.join(method['args'])
                    returns = method.get('returns', 'None')
                    lines.append(f"### `{method['name']}({args}) -> {returns}`")
                    lines.append("")
                    
                    if method['docstring']:
                        lines.append(method['docstring'])
                        lines.append("")
            
            lines.append("---")
            lines.append("")
        
        return '\n'.join(lines)
    
    def save_documentation(self, docs: Dict[str, str], output_dir: Path) -> None:
        """Save generated documentation to files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save each document
        files = {
            'class_diagram.md': docs['class_diagram'],
            'erd.md': docs['erd'],
            'API_REFERENCE.md': docs['api_docs'],
            'ARCHITECTURE.md': docs['architecture'],
            'MODULES.md': docs['module_docs']
        }
        
        for filename, content in files.items():
            file_path = output_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved: {file_path}")
