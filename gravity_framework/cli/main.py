"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/cli/main.py
PURPOSE: Command-line interface
DESCRIPTION: Provides CLI commands for interacting with the Gravity Framework
             using Typer and Rich for beautiful terminal output.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""


import typer
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional, List
import yaml

from gravity_framework.core.framework import GravityFramework
from gravity_framework.deployment.composer import DockerComposeGenerator

app = typer.Typer(
    name="gravity",
    help="Gravity Framework - Microservices Orchestration Platform",
    add_completion=True,
    rich_markup_mode="rich",
)

console = Console()


def get_framework(project_path: Optional[Path] = None) -> GravityFramework:
    """Get or create a GravityFramework instance."""
    path = project_path or Path.cwd()
    
    # Load config if exists
    config_file = path / ".gravity" / "config.yaml"
    config = {}
    if config_file.exists():
        with open(config_file) as f:
            config = yaml.safe_load(f) or {}
    
    return GravityFramework(path, config)


@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the project to create"),
    path: Optional[Path] = typer.Option(None, help="Path where to create the project"),
):
    """
    Initialize a new Gravity project.
    
    Example:
        gravity init my-app
    """
    console.print(Panel.fit(
        f"🚀 Initializing Gravity project: [bold cyan]{project_name}[/bold cyan]",
        border_style="green"
    ))
    
    project_path = path or Path.cwd() / project_name
    
    try:
        # Create project directory
        project_path.mkdir(parents=True, exist_ok=False)
        
        # Create subdirectories
        (project_path / "services").mkdir()
        (project_path / ".gravity").mkdir()
        (project_path / "config").mkdir()
        
        # Create initial config file
        (project_path / ".gravity" / "config.yaml").write_text(
            f"project_name: {project_name}\n"
            f"version: 1.0.0\n"
            f"services: []\n"
        )
        
        console.print(f"✅ Project created at: [bold]{project_path}[/bold]")
        console.print("\nNext steps:")
        console.print("  1. cd " + str(project_path))
        console.print("  2. gravity service add <repository-url>")
        console.print("  3. gravity install")
        console.print("  4. gravity start")
        
    except FileExistsError:
        console.print(f"[red]❌ Error:[/red] Directory '{project_name}' already exists")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command("add")
def add_service(
    repository: str = typer.Argument(..., help="Git repository URL or local path"),
    branch: str = typer.Option("main", help="Git branch to use"),
):
    """
    Add a service to the project.
    
    Example:
        gravity add https://github.com/user/auth-service
        gravity add ./local-service
    """
    console.print(Panel.fit(
        f"🔍 Adding service from: [bold cyan]{repository}[/bold cyan]",
        border_style="green"
    ))
    
    try:
        framework = get_framework()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Discovering service...", total=None)
            services = framework.discover_services(repository)
        
        if services:
            for service in services:
                console.print(f"✅ Added service: [bold]{service.manifest.name}[/bold] v{service.manifest.version}")
        else:
            console.print("[red]❌ No valid service found[/red]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command("list")
def list_services():
    """
    List all discovered services.
    
    Example:
        gravity list
    """
    try:
        framework = get_framework()
        services = framework.registry.get_all()
        
        if not services:
            console.print("[yellow]No services found. Use 'gravity add' to add services.[/yellow]")
            return
        
        table = Table(title="Discovered Services", show_header=True, header_style="bold magenta")
        table.add_column("Name", style="cyan")
        table.add_column("Version", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Status", style="blue")
        table.add_column("Path")
        
        for service in services:
            table.add_row(
                service.manifest.name,
                service.manifest.version,
                service.manifest.type.value,
                service.status.value,
                service.path or "N/A"
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def install(
    services: Optional[List[str]] = typer.Argument(None, help="Specific services to install"),
):
    """
    Install services and dependencies.
    
    Example:
        gravity install                    # Install all
        gravity install auth-service       # Install specific service
        gravity install auth-service user  # Install multiple services
    """
    console.print(Panel.fit(
        "📦 Installing services and dependencies...",
        border_style="blue"
    ))
    
    try:
        framework = get_framework()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Installing...", total=None)
            success = asyncio.run(framework.install(services))
            progress.update(task, completed=True)
        
        if success:
            console.print("[green]✅ Installation completed successfully![/green]")
        else:
            console.print("[red]❌ Installation failed[/red]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def start(
    services: Optional[List[str]] = typer.Argument(None, help="Specific services to start"),
    detach: bool = typer.Option(True, "--detach/--no-detach", "-d", help="Run in detached mode"),
    build: bool = typer.Option(False, "--build", "-b", help="Build images before starting"),
):
    """
    Generate docker-compose.yml and start services.
    
    This command:
    1. Generates docker-compose.yml from service manifests
    2. Generates .env.example file
    3. Starts all services with docker-compose up
    
    Example:
        gravity start                    # Start all services
        gravity start --build            # Rebuild and start
        gravity start --no-detach        # Start in foreground
    """
    console.print(Panel.fit(
        "🚀 Starting services with Docker Compose...",
        border_style="green"
    ))
    
    try:
        import subprocess
        
        framework = get_framework()
        project_path = Path.cwd()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Step 1: Get all services
            task1 = progress.add_task("Loading services...", total=None)
            all_services = asyncio.run(framework.get_all_services())
            
            if not all_services:
                console.print("[yellow]⚠ No services found. Add services first with 'gravity add'[/yellow]")
                raise typer.Exit(1)
            
            progress.update(task1, completed=True)
            
            # Step 2: Generate docker-compose.yml
            task2 = progress.add_task("Generating docker-compose.yml...", total=None)
            generator = DockerComposeGenerator()
            compose_config = asyncio.run(generator.generate(all_services))
            
            compose_file = project_path / "docker-compose.yml"
            asyncio.run(generator.write_file(compose_config, compose_file))
            
            console.print(f"✅ Generated: [bold]{compose_file}[/bold]")
            progress.update(task2, completed=True)
            
            # Step 3: Generate .env.example
            task3 = progress.add_task("Generating .env.example...", total=None)
            env_content = asyncio.run(generator.generate_env_template(all_services))
            env_file = project_path / ".env.example"
            env_file.write_text(env_content)
            
            console.print(f"✅ Generated: [bold]{env_file}[/bold]")
            progress.update(task3, completed=True)
            
            # Step 4: Start with docker-compose
            task4 = progress.add_task("Starting containers...", total=None)
            
            # Build docker-compose command
            cmd = ["docker-compose", "up"]
            if detach:
                cmd.append("-d")
            if build:
                cmd.append("--build")
            
            # Run docker-compose up
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            progress.update(task4, completed=True)
        
        if result.returncode == 0:
            console.print("[green]✅ Services started successfully![/green]")
            
            if detach:
                console.print("\n[bold]Running services:[/bold]")
                for service in all_services:
                    console.print(f"  • {service.manifest.name}")
                
                console.print("\n[bold]Useful commands:[/bold]")
                console.print("  • [cyan]docker-compose ps[/cyan]        - View running containers")
                console.print("  • [cyan]docker-compose logs -f[/cyan]   - View logs")
                console.print("  • [cyan]gravity stop[/cyan]             - Stop all services")
        else:
            console.print("[red]❌ Failed to start services[/red]")
            if result.stderr:
                console.print(f"\n[red]Error output:[/red]\n{result.stderr}")
            raise typer.Exit(1)
            
    except FileNotFoundError:
        console.print("[red]❌ Error:[/red] docker-compose not found. Please install Docker and docker-compose")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        import traceback
        traceback.print_exc()
        raise typer.Exit(1)


@app.command()
def stop(
    services: Optional[List[str]] = typer.Argument(None, help="Specific services to stop"),
):
    """
    Stop services in reverse dependency order.
    
    Example:
        gravity stop                    # Stop all
        gravity stop auth-service       # Stop specific service
        gravity stop auth-service user  # Stop multiple services
    """
    console.print(Panel.fit(
        "🛑 Stopping services...",
        border_style="red"
    ))
    
    try:
        framework = get_framework()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Stopping services...", total=None)
            success = asyncio.run(framework.stop(services))
            progress.update(task, completed=True)
        
        if success:
            console.print("[green]✅ Services stopped successfully![/green]")
        else:
            console.print("[red]❌ Failed to stop services[/red]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def restart(
    services: Optional[List[str]] = typer.Argument(None, help="Specific services to restart"),
):
    """
    Restart services.
    
    Example:
        gravity restart                    # Restart all
        gravity restart auth-service       # Restart specific service
    """
    console.print(Panel.fit(
        "🔄 Restarting services...",
        border_style="yellow"
    ))
    
    try:
        framework = get_framework()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Restarting services...", total=None)
            success = asyncio.run(framework.restart(services))
            progress.update(task, completed=True)
        
        if success:
            console.print("[green]✅ Services restarted successfully![/green]")
        else:
            console.print("[red]❌ Failed to restart services[/red]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def status():
    """
    Show status of all services.
    
    Example:
        gravity status
    """
    console.print(Panel.fit(
        "📊 Service Status",
        border_style="cyan"
    ))
    
    try:
        framework = get_framework()
        status_info = framework.status()
        
        # Summary
        console.print(f"\n[bold]Total Services:[/bold] {status_info['total_services']}")
        console.print(f"[green]Running:[/green] {status_info['running']} | [yellow]Stopped:[/yellow] {status_info['stopped']} | [red]Error:[/red] {status_info['error']}\n")
        
        if not status_info['services']:
            console.print("[yellow]No services found[/yellow]")
            return
        
        # Detailed table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Service", style="cyan")
        table.add_column("Version", style="green")
        table.add_column("Type")
        table.add_column("Status")
        table.add_column("Ports")
        table.add_column("Databases")
        
        for name, info in status_info['services'].items():
            status_style = {
                "running": "green",
                "stopped": "yellow",
                "error": "red",
                "installed": "blue",
            }.get(info['status'], "white")
            
            ports_str = ", ".join([f"{c}→{h}" for c, h in info['ports'].items()]) if info['ports'] else "N/A"
            dbs_str = ", ".join(info['databases']) if info['databases'] else "N/A"
            
            table.add_row(
                name,
                info['version'],
                info['type'],
                f"[{status_style}]{info['status']}[/{status_style}]",
                ports_str,
                dbs_str
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def logs(
    service: str = typer.Argument(..., help="Service name"),
    tail: int = typer.Option(100, help="Number of lines to show"),
    follow: bool = typer.Option(False, "-f", "--follow", help="Follow log output"),
):
    """
    Show logs for a service.
    
    Example:
        gravity logs auth-service
        gravity logs auth-service --tail 50
    """
    try:
        framework = get_framework()
        log_output = asyncio.run(framework.logs(service, tail))
        
        console.print(Panel.fit(
            f"📋 Logs for [bold cyan]{service}[/bold cyan]",
            border_style="blue"
        ))
        console.print(log_output)
        
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def health():
    """
    Check health status of services.
    
    Example:
        gravity health
    """
    try:
        framework = get_framework()
        health_status = asyncio.run(framework.health_check())
        
        console.print(Panel.fit(
            "💚 Health Check",
            border_style="green"
        ))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Service", style="cyan")
        table.add_column("Health")
        
        for service_name, is_healthy in health_status.items():
            status = "[green]✓ Healthy[/green]" if is_healthy else "[red]✗ Unhealthy[/red]"
            table.add_row(service_name, status)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def dashboard(
    port: int = typer.Option(9000, help="Port for the dashboard"),
):
    """
    Open the web dashboard.
    
    Example:
        gravity dashboard
        gravity dashboard --port 8080
    """
    console.print(Panel.fit(
        f"🌐 Starting dashboard on port [bold]{port}[/bold]",
        border_style="magenta"
    ))
    
    console.print("[yellow]Dashboard coming soon...[/yellow]")


@app.command()
def version():
    """Show Gravity Framework version."""
    from gravity_framework import __version__
    console.print(f"Gravity Framework version [bold cyan]{__version__}[/bold cyan]")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
