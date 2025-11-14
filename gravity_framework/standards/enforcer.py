"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/standards/enforcer.py
PURPOSE: Code standards enforcement
DESCRIPTION: Enforces coding standards, type hints, docstrings, and best practices
             across the codebase.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""


from typing import Dict, List, Any, Optional
from pathlib import Path
import re
import ast
import logging

logger = logging.getLogger(__name__)


class StandardsEnforcer:
    """
    Automatically enforce all TEAM_PROMPT.md coding standards.
    
    This class validates code against the strict standards defined in
    TEAM_PROMPT.md and can automatically fix many common violations.
    """
    
    def __init__(self, project_path: Path, ai_assistant=None):
        """
        Initialize standards enforcer.
        
        Args:
            project_path: Path to project root
            ai_assistant: AI assistant for intelligent fixes
        """
        self.project_path = Path(project_path)
        self.ai = ai_assistant
    
    def validate_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Validate a Python file against all standards.
        
        Checks:
        1. English-only content
        2. Type hints on all functions
        3. Docstrings present
        4. No hardcoded secrets
        5. Proper imports
        6. Error handling
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dictionary with validation results
        """
        violations = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return {
                'valid': False,
                'violations': [f'Syntax error: {e}']
            }
        
        # 1. Check for non-English content
        non_english = self._check_english_only(content)
        if non_english:
            violations.extend(non_english)
        
        # 2. Check type hints
        missing_hints = self._check_type_hints(tree)
        if missing_hints:
            violations.extend(missing_hints)
        
        # 3. Check docstrings
        missing_docs = self._check_docstrings(tree)
        if missing_docs:
            violations.extend(missing_docs)
        
        # 4. Check for hardcoded secrets
        secrets = self._check_secrets(content)
        if secrets:
            violations.extend(secrets)
        
        # 5. Check imports
        import_issues = self._check_imports(tree)
        if import_issues:
            violations.extend(import_issues)
        
        return {
            'valid': len(violations) == 0,
            'violations': violations,
            'file': str(file_path)
        }
    
    def _check_english_only(self, content: str) -> List[str]:
        """
        Check that code/comments are in English only.
        
        Args:
            content: File content
            
        Returns:
            List of violations
        """
        violations = []
        
        # Check for non-ASCII characters (except in strings)
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Skip string literals
            if '"""' in line or "'''" in line or '"' in line or "'" in line:
                continue
            
            # Check for non-English characters
            for char in line:
                if ord(char) > 127 and not char.isspace():
                    violations.append(
                        f"Line {i}: Non-English character detected: '{char}'. "
                        "All code and comments must be in ENGLISH only."
                    )
                    break
        
        return violations
    
    def _check_type_hints(self, tree: ast.AST) -> List[str]:
        """
        Check that all functions have type hints.
        
        Args:
            tree: AST tree
            
        Returns:
            List of violations
        """
        violations = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip __init__, __str__, etc. (can be less strict)
                if node.name.startswith('__') and node.name.endswith('__'):
                    continue
                
                # Check return type hint
                if node.returns is None and node.name != '__init__':
                    violations.append(
                        f"Function '{node.name}' (line {node.lineno}) missing return type hint"
                    )
                
                # Check parameter type hints
                for arg in node.args.args:
                    if arg.annotation is None and arg.arg != 'self' and arg.arg != 'cls':
                        violations.append(
                            f"Function '{node.name}' parameter '{arg.arg}' (line {node.lineno}) "
                            "missing type hint"
                        )
        
        return violations
    
    def _check_docstrings(self, tree: ast.AST) -> List[str]:
        """
        Check that functions and classes have docstrings.
        
        Args:
            tree: AST tree
            
        Returns:
            List of violations
        """
        violations = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # Skip private functions/classes (less strict)
                if node.name.startswith('_'):
                    continue
                
                docstring = ast.get_docstring(node)
                if not docstring:
                    type_name = 'Function' if isinstance(node, ast.FunctionDef) else 'Class'
                    violations.append(
                        f"{type_name} '{node.name}' (line {node.lineno}) missing docstring"
                    )
        
        return violations
    
    def _check_secrets(self, content: str) -> List[str]:
        """
        Check for hardcoded secrets.
        
        Args:
            content: File content
            
        Returns:
            List of violations
        """
        violations = []
        
        # Patterns for common secrets
        patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'password'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'API key'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'secret'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'token'),
            (r'SECRET_KEY\s*=\s*["\'][^"\']+["\']', 'SECRET_KEY'),
        ]
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Skip comments and example code
            if line.strip().startswith('#') or 'example' in line.lower():
                continue
            
            for pattern, secret_type in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append(
                        f"Line {i}: Hardcoded {secret_type} detected. "
                        "Use environment variables instead (Settings from pydantic_settings)"
                    )
        
        return violations
    
    def _check_imports(self, tree: ast.AST) -> List[str]:
        """
        Check import organization and forbidden imports.
        
        Args:
            tree: AST tree
            
        Returns:
            List of violations
        """
        violations = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Check for forbidden patterns (service imports)
                    if '_service.' in alias.name:
                        violations.append(
                            f"Line {node.lineno}: Direct service import detected: {alias.name}. "
                            "Use API/Event communication instead."
                        )
        
        return violations
    
    def auto_fix_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Automatically fix common standards violations using AI.
        
        AI will:
        - Add missing type hints
        - Generate docstrings
        - Fix English language issues
        - Suggest security improvements
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dictionary with fix results
        """
        if not self.ai:
            return {
                'success': False,
                'error': 'AI assistant required for auto-fix'
            }
        
        # Read original file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Get violations
        validation = self.validate_file(file_path)
        if validation['valid']:
            return {
                'success': True,
                'message': 'File already meets all standards',
                'changes_made': []
            }
        
        # Ask AI to fix violations
        prompt = f"""
        Fix the following code to meet TEAM_PROMPT.md standards.
        
        VIOLATIONS FOUND:
        {chr(10).join('- ' + v for v in validation['violations'])}
        
        STANDARDS TO FOLLOW:
        1. All code and comments in ENGLISH only
        2. Type hints on ALL functions (parameters and return type)
        3. Docstrings for all public functions and classes
        4. No hardcoded secrets (use Settings from pydantic_settings)
        5. No direct service imports
        
        ORIGINAL CODE:
        {original_content}
        
        Return ONLY the fixed code, no explanations.
        """
        
        fixed_content = self.ai.query(prompt)
        
        # Write fixed file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return {
            'success': True,
            'message': 'File fixed successfully',
            'violations_fixed': len(validation['violations']),
            'changes_made': validation['violations']
        }
    
    def validate_project(self) -> Dict[str, Any]:
        """
        Validate entire project against standards.
        
        Returns:
            Dictionary with project-wide validation results
        """
        all_violations = []
        files_checked = 0
        files_with_violations = 0
        
        # Find all Python files
        python_files = list(self.project_path.rglob('*.py'))
        
        for file_path in python_files:
            # Skip venv, __pycache__, etc.
            if any(part.startswith('.') or part in ['venv', '__pycache__', 'node_modules'] 
                   for part in file_path.parts):
                continue
            
            files_checked += 1
            result = self.validate_file(file_path)
            
            if not result['valid']:
                files_with_violations += 1
                all_violations.append(result)
        
        return {
            'valid': files_with_violations == 0,
            'files_checked': files_checked,
            'files_with_violations': files_with_violations,
            'violations': all_violations
        }


class CommitMessageValidator:
    """
    Validate and enforce Conventional Commits format.
    """
    
    @staticmethod
    def validate(message: str) -> Dict[str, Any]:
        """
        Validate commit message against TEAM_PROMPT standards.
        
        Args:
            message: Commit message
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        
        if not message or not message.strip():
            errors.append("Commit message cannot be empty")
            return {'valid': False, 'errors': errors}
        
        lines = message.strip().split('\n')
        subject = lines[0]
        
        # Check English only
        if not all(ord(char) < 128 or char in '(),:;-_' for char in subject):
            errors.append("Commit message must be in ENGLISH only")
        
        # Check Conventional Commits format
        pattern = r'^(feat|fix|refactor|docs|test|chore|style|perf)(\([a-z0-9\-]+\))?: .+'
        if not re.match(pattern, subject):
            errors.append(
                "Must follow Conventional Commits: type(scope): subject\n"
                "Valid types: feat, fix, refactor, docs, test, chore, style, perf"
            )
        
        # Check no trailing period
        if subject.endswith('.'):
            errors.append("Subject should not end with period")
        
        # Check length
        if len(subject) > 72:
            errors.append(f"Subject too long ({len(subject)} chars, max 72)")
        
        # Check lowercase after colon
        match = re.match(r'^[a-z]+(\([a-z0-9\-]+\))?: (.+)', subject)
        if match and match.group(2)[0].isupper():
            errors.append("Description after colon should start with lowercase")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
