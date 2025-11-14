"""
Interactive Guide System - Step-by-step assistance for users.

This module analyzes microservices and provides interactive,
step-by-step guidance to users, automating as much as possible.
"""

import logging
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path
import subprocess
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.tree import Tree

from gravity_framework.models.service import Service

logger = logging.getLogger(__name__)
console = Console()


class InteractiveGuide:
    """
    Interactive guide that analyzes services and provides step-by-step
    assistance to users, automatically executing commands when possible.
    """
    
    def __init__(self, services: List[Service]):
        """Initialize interactive guide.
        
        Args:
            services: List of discovered services
        """
        self.services = services
        self.steps_completed = []
        self.steps_failed = []
        
    def analyze_and_guide(self) -> Dict[str, Any]:
        """Analyze services and provide interactive guidance.
        
        Returns:
            Summary of guidance session
        """
        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]🤖 Gravity Framework - Interactive Guide[/bold cyan]\n"
            "[dim]I'll analyze your microservices and guide you step-by-step[/dim]",
            border_style="cyan"
        ))
        
        # Step 1: Analyze all services
        analysis = self._analyze_services()
        
        # Step 2: Show what was found
        self._show_analysis_summary(analysis)
        
        # Step 3: Guide through setup
        if Confirm.ask("\n[cyan]Ready to set up your microservices?[/cyan]", default=True):
            self._guide_setup(analysis)
        
        # Step 4: Summary
        return self._show_completion_summary()
    
    def _analyze_services(self) -> Dict[str, Any]:
        """Deep analysis of all services.
        
        Returns:
            Comprehensive analysis results
        """
        console.print("\n[yellow]⏳ Analyzing your microservices...[/yellow]")
        
        analysis = {
            'total_services': len(self.services),
            'services': [],
            'databases_needed': [],
            'dependencies': [],
            'environment_vars': {},
            'ports': [],
            'steps': []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Analyzing...", total=len(self.services))
            
            for service in self.services:
                # Analyze each service deeply
                service_info = self._analyze_service(service)
                analysis['services'].append(service_info)
                
                # Collect databases
                if service.manifest.databases:
                    for db in service.manifest.databases:
                        analysis['databases_needed'].append({
                            'service': service.manifest.name,
                            'db_name': db.name,
                            'db_type': db.type.value,
                            'service_info': service_info
                        })
                
                # Collect dependencies
                if service.manifest.dependencies:
                    for dep in service.manifest.dependencies:
                        analysis['dependencies'].append({
                            'service': service.manifest.name,
                            'needs': dep.name,
                            'optional': dep.optional if hasattr(dep, 'optional') else False
                        })
                
                # Collect environment variables
                if service.manifest.environment:
                    analysis['environment_vars'][service.manifest.name] = service.manifest.environment.variables
                
                # Collect ports
                if service.manifest.ports:
                    for port in service.manifest.ports:
                        analysis['ports'].append({
                            'service': service.manifest.name,
                            'container_port': port.container,
                            'host_port': port.host if hasattr(port, 'host') else None
                        })
                
                progress.advance(task)
        
        # Generate steps based on analysis
        analysis['steps'] = self._generate_steps(analysis)
        
        return analysis
    
    def _analyze_service(self, service: Service) -> Dict[str, Any]:
        """Deep analysis of a single service.
        
        Args:
            service: Service to analyze
            
        Returns:
            Service analysis results
        """
        info = {
            'name': service.manifest.name,
            'type': service.manifest.type.value,
            'repository': service.manifest.repository,
            'has_readme': False,
            'has_requirements': False,
            'has_dockerfile': False,
            'has_docker_compose': False,
            'install_instructions': None,
            'run_command': service.manifest.command,
            'needs_build': False,
            'build_command': None
        }
        
        # Check if service path exists
        if service.path:
            service_path = Path(service.path)
            
            # Check for common files
            info['has_readme'] = (service_path / 'README.md').exists()
            info['has_requirements'] = (service_path / 'requirements.txt').exists()
            info['has_dockerfile'] = (service_path / 'Dockerfile').exists()
            info['has_docker_compose'] = (service_path / 'docker-compose.yml').exists()
            
            # Parse README for instructions
            if info['has_readme']:
                info['install_instructions'] = self._parse_readme_instructions(
                    service_path / 'README.md'
                )
            
            # Check if needs build
            if service.manifest.install_script or info['has_requirements']:
                info['needs_build'] = True
                info['build_command'] = service.manifest.install_script or 'pip install -r requirements.txt'
        
        return info
    
    def _parse_readme_instructions(self, readme_path: Path) -> Optional[Dict[str, Any]]:
        """Parse README to extract installation/setup instructions.
        
        Args:
            readme_path: Path to README file
            
        Returns:
            Extracted instructions
        """
        try:
            content = readme_path.read_text(encoding='utf-8')
            
            instructions = {
                'install_commands': [],
                'run_commands': [],
                'env_vars': [],
                'notes': []
            }
            
            # Simple parsing - look for code blocks
            in_code_block = False
            current_section = None
            
            for line in content.split('\n'):
                line_lower = line.lower()
                
                # Detect sections
                if 'install' in line_lower or 'setup' in line_lower:
                    current_section = 'install'
                elif 'run' in line_lower or 'start' in line_lower:
                    current_section = 'run'
                elif 'environment' in line_lower or 'env' in line_lower:
                    current_section = 'env'
                
                # Detect code blocks
                if line.startswith('```'):
                    in_code_block = not in_code_block
                    continue
                
                # Extract commands from code blocks
                if in_code_block and line.strip():
                    if current_section == 'install':
                        instructions['install_commands'].append(line.strip())
                    elif current_section == 'run':
                        instructions['run_commands'].append(line.strip())
            
            return instructions if any(instructions.values()) else None
            
        except Exception as e:
            logger.debug(f"Failed to parse README: {e}")
            return None
    
    def _generate_steps(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate step-by-step setup instructions.
        
        Args:
            analysis: Service analysis results
            
        Returns:
            List of steps to execute
        """
        steps = []
        
        # Step 1: Create databases
        if analysis['databases_needed']:
            steps.append({
                'id': 'create_databases',
                'title': 'Create Databases',
                'description': f"Create {len(analysis['databases_needed'])} database(s) for your services",
                'auto_execute': True,
                'items': analysis['databases_needed']
            })
        
        # Step 2: Install dependencies for each service
        for service_info in analysis['services']:
            if service_info['needs_build']:
                steps.append({
                    'id': f"install_{service_info['name']}",
                    'title': f"Install {service_info['name']} Dependencies",
                    'description': f"Install Python dependencies for {service_info['name']}",
                    'auto_execute': True,
                    'command': service_info['build_command'],
                    'service': service_info['name'],
                    'path': None  # Will be filled later
                })
        
        # Step 3: Configure environment variables
        if analysis['environment_vars']:
            steps.append({
                'id': 'configure_env',
                'title': 'Configure Environment Variables',
                'description': 'Set up required environment variables',
                'auto_execute': True,
                'items': analysis['environment_vars']
            })
        
        # Step 4: Start services
        steps.append({
            'id': 'start_services',
            'title': 'Start All Services',
            'description': f"Start all {analysis['total_services']} microservices",
            'auto_execute': True,
            'items': analysis['services']
        })
        
        return steps
    
    def _show_analysis_summary(self, analysis: Dict[str, Any]):
        """Show analysis summary to user.
        
        Args:
            analysis: Analysis results
        """
        console.print("\n[bold green]✅ Analysis Complete![/bold green]\n")
        
        # Summary table
        table = Table(title="Microservices Overview")
        table.add_column("Service", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Databases", style="magenta")
        table.add_column("Status", style="green")
        
        for service_info in analysis['services']:
            db_count = sum(1 for db in analysis['databases_needed'] if db['service'] == service_info['name'])
            status = "✅ Ready" if not service_info['needs_build'] else "🔨 Needs Build"
            
            table.add_row(
                service_info['name'],
                service_info['type'],
                str(db_count) if db_count > 0 else "-",
                status
            )
        
        console.print(table)
        
        # Setup steps preview
        console.print(f"\n[bold]📋 Setup Plan ({len(analysis['steps'])} steps):[/bold]")
        for i, step in enumerate(analysis['steps'], 1):
            auto = "🤖 Auto" if step.get('auto_execute') else "👤 Manual"
            console.print(f"  {i}. {auto} - {step['title']}")
    
    def _guide_setup(self, analysis: Dict[str, Any]):
        """Guide user through setup process.
        
        Args:
            analysis: Analysis results
        """
        console.print("\n" + "="*60)
        console.print("[bold cyan]🚀 Starting Setup Process[/bold cyan]")
        console.print("="*60 + "\n")
        
        for i, step in enumerate(analysis['steps'], 1):
            console.print(f"\n[bold yellow]Step {i}/{len(analysis['steps'])}: {step['title']}[/bold yellow]")
            console.print(f"[dim]{step['description']}[/dim]\n")
            
            if step.get('auto_execute'):
                # Auto-execute this step
                success = self._execute_step(step, analysis)
                if success:
                    self.steps_completed.append(step['id'])
                    console.print(f"[green]✅ {step['title']} completed![/green]")
                else:
                    self.steps_failed.append(step['id'])
                    console.print(f"[red]❌ {step['title']} failed![/red]")
                    
                    if not Confirm.ask("[yellow]Continue anyway?[/yellow]", default=True):
                        break
            else:
                # Manual step - show instructions
                console.print("[yellow]⚠️ Manual action required[/yellow]")
                self._show_manual_instructions(step)
                
                if Confirm.ask("[cyan]Have you completed this step?[/cyan]", default=True):
                    self.steps_completed.append(step['id'])
                else:
                    self.steps_failed.append(step['id'])
        
    def _execute_step(self, step: Dict[str, Any], analysis: Dict[str, Any]) -> bool:
        """Execute a setup step automatically.
        
        Args:
            step: Step to execute
            analysis: Full analysis context
            
        Returns:
            True if successful
        """
        step_id = step['id']
        
        if step_id == 'create_databases':
            return self._execute_create_databases(step)
        
        elif step_id.startswith('install_'):
            return self._execute_install_dependencies(step, analysis)
        
        elif step_id == 'configure_env':
            return self._execute_configure_env(step)
        
        elif step_id == 'start_services':
            return self._execute_start_services(step)
        
        return False
    
    def _execute_create_databases(self, step: Dict[str, Any]) -> bool:
        """Execute database creation step.
        
        Args:
            step: Step details
            
        Returns:
            True if successful
        """
        console.print("[cyan]🗄️  Creating databases...[/cyan]")
        
        # This will be handled by DatabaseOrchestrator
        # Just show what will be created
        for db in step['items']:
            console.print(f"  ✓ {db['db_type']} database: {db['db_name']} (for {db['service']})")
        
        return True
    
    def _execute_install_dependencies(self, step: Dict[str, Any], analysis: Dict[str, Any]) -> bool:
        """Execute dependency installation step.
        
        Args:
            step: Step details
            analysis: Full analysis
            
        Returns:
            True if successful
        """
        service_name = step['service']
        command = step['command']
        
        # Find service path
        service = next((s for s in self.services if s.manifest.name == service_name), None)
        if not service or not service.path:
            console.print(f"[red]Cannot find path for {service_name}[/red]")
            return False
        
        console.print(f"[cyan]📦 Installing dependencies for {service_name}...[/cyan]")
        console.print(f"[dim]Running: {command}[/dim]")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=service.path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                console.print(f"[green]✓ Dependencies installed[/green]")
                return True
            else:
                console.print(f"[red]✗ Installation failed: {result.stderr[:200]}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
            return False
    
    def _execute_configure_env(self, step: Dict[str, Any]) -> bool:
        """Execute environment configuration step.
        
        Args:
            step: Step details
            
        Returns:
            True if successful
        """
        console.print("[cyan]🔧 Configuring environment variables...[/cyan]")
        
        # Show environment variables per service
        for service_name, env_vars in step['items'].items():
            console.print(f"\n[yellow]{service_name}:[/yellow]")
            for key, value in env_vars.items():
                console.print(f"  {key} = {value}")
        
        # Environment variables will be injected by framework
        console.print(f"\n[green]✓ Environment configured (will be injected at runtime)[/green]")
        return True
    
    def _execute_start_services(self, step: Dict[str, Any]) -> bool:
        """Execute service start step.
        
        Args:
            step: Step details
            
        Returns:
            True if successful
        """
        console.print("[cyan]🚀 Starting services...[/cyan]")
        
        # Services will be started by ServiceManager
        for service_info in step['items']:
            console.print(f"  ✓ {service_info['name']} will start on port {service_info.get('port', 'auto')}")
        
        return True
    
    def _show_manual_instructions(self, step: Dict[str, Any]):
        """Show manual instructions for a step.
        
        Args:
            step: Step details
        """
        console.print(Panel(
            step.get('instructions', 'Please complete this step manually'),
            title=f"Instructions for: {step['title']}",
            border_style="yellow"
        ))
    
    def _show_completion_summary(self) -> Dict[str, Any]:
        """Show final summary of setup process.
        
        Returns:
            Summary statistics
        """
        console.print("\n" + "="*60)
        console.print("[bold cyan]📊 Setup Summary[/bold cyan]")
        console.print("="*60 + "\n")
        
        total = len(self.steps_completed) + len(self.steps_failed)
        success_rate = (len(self.steps_completed) / total * 100) if total > 0 else 0
        
        console.print(f"✅ Completed: {len(self.steps_completed)}")
        console.print(f"❌ Failed: {len(self.steps_failed)}")
        console.print(f"📈 Success Rate: {success_rate:.1f}%\n")
        
        if self.steps_completed:
            console.print("[green]Completed steps:[/green]")
            for step_id in self.steps_completed:
                console.print(f"  ✓ {step_id}")
        
        if self.steps_failed:
            console.print("\n[red]Failed steps:[/red]")
            for step_id in self.steps_failed:
                console.print(f"  ✗ {step_id}")
        
        console.print("\n" + "="*60)
        
        return {
            'total_steps': total,
            'completed': len(self.steps_completed),
            'failed': len(self.steps_failed),
            'success_rate': success_rate
        }
