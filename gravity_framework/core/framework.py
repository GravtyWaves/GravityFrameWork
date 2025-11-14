"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/core/framework.py
PURPOSE: Main GravityFramework class - core orchestration engine
DESCRIPTION: Provides the main GravityFramework class that orchestrates microservice
             discovery, installation, database setup, and autonomous development.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""


from typing import Optional, Dict, List, Any
import logging
import asyncio
from pathlib import Path

from gravity_framework.models.service import Service, ServiceRegistry, ServiceStatus
from gravity_framework.discovery.scanner import ServiceScanner
from gravity_framework.resolver.dependency import DependencyResolver
from gravity_framework.database.orchestrator import DatabaseOrchestrator
from gravity_framework.database.multi_access import MultiDatabaseAccessManager, DataFederationLayer
from gravity_framework.core.manager import ServiceManager
from gravity_framework.ai.assistant import AIAssistant
from gravity_framework.ai.team_generator import DynamicTeamGenerator, ProjectConfigGenerator
from gravity_framework.ai.autonomous_dev import AutonomousDevelopmentSystem
from gravity_framework.devops.automation import DevOpsAutomation
from gravity_framework.git.integration import GitIntegration, GitHubIntegration
from gravity_framework.git.commit_manager import CommitManager, AutoCommitScheduler
from gravity_framework.standards.enforcer import StandardsEnforcer
from gravity_framework.project.manager import ProjectManager
from gravity_framework.learning.system import ContinuousLearningSystem, AIProvider

logger = logging.getLogger(__name__)


class GravityFramework:
    """
    Main Gravity Framework class for orchestrating microservices.
    
    This class provides the core functionality for discovering, installing,
    connecting, and managing microservices.
    
    Example:
        >>> framework = GravityFramework()
        >>> framework.discover_services("https://github.com/user/auth-service")
        >>> framework.install()
        >>> framework.start()
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        config: Optional[Dict] = None,
        ai_assist: bool = True,
        ollama_model: str = "llama3.2:3b",
        auto_install_ai: bool = True,
        ai_provider: AIProvider = AIProvider.OLLAMA,
        ai_api_keys: Optional[Dict[str, str]] = None,
        enable_learning: bool = True
    ):
        """
        Initialize the Gravity Framework.
        
        Args:
            project_path: Path to the Gravity project directory.
                         If None, uses current directory.
            config: Optional configuration dictionary
            ai_assist: Enable AI-powered assistance (auto-detects Ollama)
            ollama_model: Ollama model to use (default: llama3.2:3b - fast & free)
            auto_install_ai: Automatically install Ollama if not found (default: True)
            ai_provider: AI provider to use (OLLAMA=free, OPENAI, ANTHROPIC, etc.)
            ai_api_keys: API keys for paid AI providers (e.g., {'openai': 'sk-...'})
            enable_learning: Enable continuous learning system (default: True)
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.config = config or {}
        
        # Initialize components
        self.registry = ServiceRegistry()
        self.scanner = ServiceScanner(self.project_path / "services")
        self.db_orchestrator = DatabaseOrchestrator(self.config.get("databases", {}))
        self.service_manager = ServiceManager()
        self.ai = AIAssistant(
            enabled=ai_assist,
            ollama_model=ollama_model,
            auto_install=auto_install_ai
        )  # FREE AI with auto-install!
        self.devops = DevOpsAutomation(self.project_path)  # Complete infrastructure automation!
        
        # NEW: Intelligent Git integration
        try:
            self.git = GitIntegration(self.project_path, self.ai)
            self.github = GitHubIntegration(self.project_path)
            self.commit_manager = CommitManager(self.git, self.ai)
            self.auto_commit = AutoCommitScheduler(self.commit_manager, threshold=100)
            logger.info("Git integration enabled")
        except ValueError:
            # Not a Git repository, that's OK
            self.git = None
            self.github = None
            self.commit_manager = None
            self.auto_commit = None
            logger.info("Git integration disabled (not a Git repository)")
        
        # NEW: Standards enforcement
        self.standards = StandardsEnforcer(self.project_path, self.ai)
        
        # NEW: Dynamic team generator
        self.team_generator = DynamicTeamGenerator(self.ai)
        
        # NEW: Project manager
        self.project_manager = ProjectManager(self.project_path, self.ai)
        
        # NEW: Continuous learning system
        if enable_learning:
            self.learning = ContinuousLearningSystem(
                storage_path=self.project_path / '.gravity' / 'learning',
                ai_provider=ai_provider,
                api_keys=ai_api_keys
            )
            logger.info("Continuous learning enabled")
        else:
            self.learning = None
        
        # NEW: Multi-database access manager
        self.multi_db = MultiDatabaseAccessManager()
        self.data_federation = DataFederationLayer(self.multi_db)
        
        self._plugins: Dict[str, Any] = {}
        
        logger.info(f"Initialized Gravity Framework at {self.project_path}")
    
    def discover_services(self, source: Optional[str] = None) -> List[Service]:
        """
        Discover microservices from Git repositories or local paths.
        
        Args:
            source: Optional specific source (Git URL or local path).
                   If None, scans all services in services directory.
            
        Returns:
            List of discovered services
            
        Raises:
            ValueError: If repository URL is invalid
        """
        logger.info(f"Discovering services from {source or 'all sources'}")
        
        try:
            if source:
                # Discover from specific source
                if source.startswith(("http://", "https://", "git@")):
                    # Git repository
                    service = self.scanner.discover_from_git(source)
                    if service:
                        self.registry.add_service(service)
                        return [service]
                else:
                    # Local path
                    service = self.scanner.discover_from_path(Path(source))
                    if service:
                        self.registry.add_service(service)
                        return [service]
                return []
            else:
                # Discover all services in services directory
                services = self.scanner.discover_all()
                for service in services:
                    self.registry.add_service(service)
                
                # Record learning event
                if self.learning:
                    self.learning.record_service_discovery(
                        services=[s.manifest.name for s in services],
                        success=True
                    )
                
                return services
                
        except Exception as e:
            logger.error(f"Error discovering services: {e}")
            
            # Record failure
            if self.learning:
                self.learning.record_service_discovery(
                    services=[],
                    success=False,
                    errors=[str(e)]
                )
            
            return []
    
    async def install(self, service_names: Optional[List[str]] = None) -> bool:
        """
        Install services and their dependencies.
        
        Args:
            service_names: Optional list of specific services to install.
                          If None, installs all discovered services.
            
        Returns:
            True if installation succeeded
        """
        logger.info(f"Installing services: {service_names or 'all'}")
        
        try:
            # Get services to install
            if service_names:
                services = [self.registry.get_service(name) for name in service_names]
                services = [s for s in services if s is not None]
            else:
                services = self.registry.get_all()
            
            if not services:
                logger.warning("No services to install")
                return True
            
            # Resolve dependencies
            resolver = DependencyResolver(services)
            ordered_services = resolver.resolve()
            
            if not ordered_services:
                logger.error("Failed to resolve dependencies")
                
                # Record failure
                if self.learning:
                    conflicts = resolver.get_conflicts() if hasattr(resolver, 'get_conflicts') else []
                    self.learning.record_dependency_resolution(
                        dependencies=[s.manifest.name for s in services],
                        conflicts=conflicts,
                        success=False
                    )
                
                return False
            
            # Record successful dependency resolution
            if self.learning:
                self.learning.record_dependency_resolution(
                    dependencies=[s.manifest.name for s in ordered_services],
                    conflicts=[],
                    success=True
                )
            
            # Install services in dependency order
            for service in ordered_services:
                logger.info(f"📦 Installing {service.manifest.name}...")
                
                # Setup databases
                if not await self.db_orchestrator.setup_databases(service):
                    logger.error(f"Failed to setup databases for {service.manifest.name}")
                    return False
                
                # Install service
                if not await self.service_manager.install_service(service):
                    logger.error(f"Failed to install {service.manifest.name}")
                    return False
            
            logger.info(f"✓ Successfully installed {len(ordered_services)} service(s)")
            return True
            
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            return False
    
    async def start(self, service_names: Optional[List[str]] = None) -> bool:
        """
        Start services in dependency order.
        
        Args:
            service_names: Optional list of specific services to start.
                          If None, starts all installed services.
            
        Returns:
            True if services started successfully
        """
        logger.info(f"Starting services: {service_names or 'all'}")
        
        try:
            # Get services to start
            if service_names:
                services = [self.registry.get_service(name) for name in service_names]
                services = [s for s in services if s is not None]
            else:
                services = self.registry.get_by_status(ServiceStatus.INSTALLED)
                if not services:
                    services = self.registry.get_all()
            
            if not services:
                logger.warning("No services to start")
                return True
            
            # Resolve dependencies to get start order
            resolver = DependencyResolver(services)
            ordered_services = resolver.resolve()
            
            if not ordered_services:
                logger.error("Failed to resolve dependencies")
                return False
            
            # Prepare environment variables with database URLs
            for service in ordered_services:
                env_vars = {}
                
                # Add database connection strings
                for db_req in service.manifest.databases:
                    if db_req.name in service.created_databases:
                        conn_str = await self.db_orchestrator.get_connection_string(db_req)
                        env_key = f"{db_req.name.upper()}_URL"
                        env_vars[env_key] = conn_str
                
                # Start service
                logger.info(f"🚀 Starting {service.manifest.name}...")
                if not await self.service_manager.start_service(service, env_vars):
                    logger.error(f"Failed to start {service.manifest.name}")
                    return False
                
                # Small delay between starts
                await asyncio.sleep(2)
            
            logger.info(f"✓ Successfully started {len(ordered_services)} service(s)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start services: {e}")
            return False
    
    async def stop(self, service_names: Optional[List[str]] = None) -> bool:
        """
        Stop services in reverse dependency order.
        
        Args:
            service_names: Optional list of specific services to stop.
                          If None, stops all running services.
            
        Returns:
            True if services stopped successfully
        """
        logger.info(f"Stopping services: {service_names or 'all'}")
        
        try:
            # Get services to stop
            if service_names:
                services = [self.registry.get_service(name) for name in service_names]
                services = [s for s in services if s is not None]
            else:
                services = self.registry.get_by_status(ServiceStatus.RUNNING)
            
            if not services:
                logger.warning("No running services to stop")
                return True
            
            # Stop services in reverse dependency order
            resolver = DependencyResolver(services)
            ordered_services = resolver.resolve()
            
            if ordered_services:
                ordered_services.reverse()  # Stop dependents first
            else:
                ordered_services = services
            
            # Stop each service
            for service in ordered_services:
                logger.info(f"🛑 Stopping {service.manifest.name}...")
                await self.service_manager.stop_service(service)
            
            logger.info(f"✓ Successfully stopped {len(ordered_services)} service(s)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop services: {e}")
            return False
    
    async def restart(self, service_names: Optional[List[str]] = None) -> bool:
        """
        Restart services.
        
        Args:
            service_names: Optional list of specific services to restart.
            
        Returns:
            True if services restarted successfully
        """
        logger.info(f"Restarting services: {service_names or 'all'}")
        
        if not await self.stop(service_names):
            return False
        
        await asyncio.sleep(2)
        
        return await self.start(service_names)
    
    def status(self) -> Dict[str, Any]:
        """
        Get status of all services.
        
        Returns:
            Dictionary containing comprehensive service status information
        """
        logger.info("Getting service status")
        
        services_status = {}
        for service in self.registry.get_all():
            services_status[service.manifest.name] = {
                "version": service.manifest.version,
                "type": service.manifest.type.value,
                "status": service.status.value,
                "path": service.path,
                "container_id": service.container_id[:12] if service.container_id else None,
                "ports": service.assigned_ports,
                "databases": service.created_databases,
                "error": service.error_message
            }
        
        return {
            "total_services": len(services_status),
            "running": len(self.registry.get_by_status(ServiceStatus.RUNNING)),
            "stopped": len(self.registry.get_by_status(ServiceStatus.STOPPED)),
            "error": len(self.registry.get_by_status(ServiceStatus.ERROR)),
            "services": services_status
        }
    
    async def logs(self, service_name: str, tail: int = 100) -> str:
        """
        Get logs for a specific service.
        
        Args:
            service_name: Name of the service
            tail: Number of log lines to return
            
        Returns:
            Log output string
        """
        service = self.registry.get_service(service_name)
        if not service:
            return f"Service not found: {service_name}"
        
        return await self.service_manager.get_service_logs(service, tail)
    
    async def health_check(self, service_name: Optional[str] = None) -> Dict[str, bool]:
        """
        Check health status of services.
        
        Args:
            service_name: Optional specific service name.
                         If None, checks all services.
            
        Returns:
            Dictionary mapping service names to health status (True/False)
        """
        if service_name:
            service = self.registry.get_service(service_name)
            if not service:
                return {service_name: False}
            
            is_healthy = await self.service_manager.check_health(service)
            return {service_name: is_healthy}
        else:
            health_status = {}
            for service in self.registry.get_all():
                is_healthy = await self.service_manager.check_health(service)
                health_status[service.manifest.name] = is_healthy
            return health_status
    
    def register_plugin(self, name: str, plugin: Any) -> None:
        """
        Register a custom plugin for extensibility.
        
        Args:
            name: Plugin name
            plugin: Plugin instance
        """
        logger.info(f"Registering plugin: {name}")
        self._plugins[name] = plugin
    
    def get_service(self, name: str) -> Optional[Service]:
        """
        Get a service by name.
        
        Args:
            name: Service name
            
        Returns:
            Service instance or None if not found
        """
        return self.registry.get_service(name)
    
    async def get_all_services(self) -> List[Service]:
        """
        Get all registered services.
        
        Returns:
            List of all services
        """
        # First try to discover all services if registry is empty
        if not self.registry.services:
            self.discover_services()
        
        return self.registry.get_all()
    
    def ai_analyze(self) -> Dict[str, Any]:
        """
        AI-powered analysis of microservices architecture.
        
        Uses GitHub Copilot (free) to analyze services and provide:
        - Connection recommendations
        - Database schema insights
        - Optimization suggestions
        - Architecture best practices
        
        Returns:
            Dictionary with AI analysis results
            
        Example:
            >>> framework = GravityFramework(ai_assist=True)
            >>> framework.discover_services()
            >>> analysis = framework.ai_analyze()
            >>> print(analysis['recommendations'])
        """
        services = self.registry.get_all()
        
        if not services:
            return {
                "error": "No services discovered yet",
                "suggestion": "Run framework.discover_services() first"
            }
        
        return self.ai.analyze_services(services)
    
    def ai_suggest_connections(self) -> List[Dict[str, str]]:
        """
        Get AI suggestions for how services should connect (puzzle-solving).
        
        AI analyzes services and suggests optimal connections:
        - API endpoints to call
        - Authentication patterns
        - Database access patterns
        - Service dependencies
        
        Returns:
            List of connection suggestions
            
        Example:
            >>> suggestions = framework.ai_suggest_connections()
            >>> for conn in suggestions:
            ...     print(f"{conn['from']} -> {conn['to']}: {conn['method']}")
        """
        services = self.registry.get_all()
        return self.ai.suggest_connections(services)
    
    def ai_diagnose(self, error: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        AI-powered error diagnosis and troubleshooting.
        
        Provides intelligent solutions for common issues.
        
        Args:
            error: Error message to diagnose
            context: Optional additional context
            
        Returns:
            Diagnosis with suggested solutions
            
        Example:
            >>> diagnosis = framework.ai_diagnose(
            ...     "Connection refused on port 8000",
            ...     {"service": "auth-service"}
            ... )
            >>> print(diagnosis['solutions'])
        """
        return self.ai.diagnose_issue(error, context or {})
    
    def ai_optimize_deployment(self) -> Dict[str, Any]:
        """
        Get AI recommendations for deployment optimization.
        
        Returns:
            Optimization suggestions for resources, scaling, and performance
            
        Example:
            >>> opts = framework.ai_optimize_deployment()
            >>> for opt in opts['performance']:
            ...     print(opt['recommendation'])
        """
        services = self.registry.get_all()
        return self.ai.optimize_deployment(services)
    
    def interactive_setup(self) -> Dict[str, Any]:
        """
        Interactive step-by-step setup guide.
        
        Analyzes all discovered services and provides interactive guidance:
        - Shows what will be installed
        - Creates databases automatically
        - Installs dependencies
        - Configures environment variables
        - Starts services
        
        Most steps are automated - minimal user interaction needed!
        
        Returns:
            Setup summary with statistics
            
        Example:
            >>> framework = GravityFramework()
            >>> framework.discover_services()
            >>> summary = framework.interactive_setup()
            
            🤖 Gravity Framework - Interactive Guide
            I'll analyze your microservices and guide you step-by-step
            
            ⏳ Analyzing your microservices...
            ✅ Analysis Complete!
            
            📋 Setup Plan (4 steps):
              1. 🤖 Auto - Create Databases
              2. 🤖 Auto - Install auth-service Dependencies
              3. 🤖 Auto - Configure Environment Variables  
              4. 🤖 Auto - Start All Services
            
            Ready to set up your microservices? [Y/n]: y
            
            🚀 Starting Setup Process
            ============================
            
            Step 1/4: Create Databases
            🗄️  Creating databases...
              ✓ postgresql database: auth_db (for auth-service)
            ✅ Create Databases completed!
            
            Step 2/4: Install auth-service Dependencies
            📦 Installing dependencies for auth-service...
            Running: pip install -r requirements.txt
            ✓ Dependencies installed
            ✅ Install auth-service Dependencies completed!
            
            ...
            
            📊 Setup Summary
            ✅ Completed: 4
            ❌ Failed: 0
            📈 Success Rate: 100.0%
        """
        from gravity_framework.core.interactive_guide import InteractiveGuide
        
        services = self.registry.get_all()
        
        if not services:
            logger.warning("No services discovered yet. Run discover_services() first.")
            return {'error': 'No services found'}
        
        guide = InteractiveGuide(services)
        return guide.analyze_and_guide()
    
    def setup_infrastructure(self, services: Optional[List[Service]] = None) -> Dict[str, Any]:
        """
        Automatically generate complete web application infrastructure.
        
        This method generates production-ready infrastructure including:
        - Nginx reverse proxy with load balancing
        - Docker infrastructure (multi-stage builds, docker-compose)
        - Monitoring stack (Prometheus + Grafana)
        - CI/CD pipeline (GitHub Actions)
        - Automated backups (PostgreSQL, Redis)
        - SSL/TLS setup (Let's Encrypt)
        - Master deployment script
        
        Args:
            services: List of services to generate infrastructure for.
                     If None, uses all discovered services.
        
        Returns:
            Dictionary with results:
            {
                'success': True/False,
                'infrastructure': {
                    'nginx': '/path/to/nginx/config',
                    'docker': '/path/to/docker-compose.yml',
                    'monitoring': '/path/to/monitoring',
                    'cicd': '/path/to/.github/workflows',
                    'backups': '/path/to/backup/scripts',
                    'ssl': '/path/to/ssl/config',
                    'deployment': '/path/to/deploy.sh'
                },
                'message': 'Infrastructure generated successfully'
            }
        """
        if services is None:
            services = self.registry.get_all()
        
        if not services:
            logger.warning("No services to generate infrastructure for. Run discover_services() first.")
            return {
                'success': False,
                'error': 'No services found',
                'message': 'Please run discover_services() first to discover microservices.'
            }
        
        logger.info(f"Generating complete infrastructure for {len(services)} services...")
        
        try:
            result = self.devops.setup_complete_infrastructure(services)
            logger.info("Infrastructure generation completed successfully!")
            return result
        except Exception as e:
            logger.error(f"Infrastructure generation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Infrastructure generation failed: {e}'
            }
    
    def deploy(self, environment: str = 'production') -> Dict[str, Any]:
        """
        Deploy the complete application with one command.
        
        This method executes the generated deployment script to deploy
        all services with proper infrastructure in place.
        
        Args:
            environment: Deployment environment (production, staging, development)
        
        Returns:
            Dictionary with deployment status and results
        """
        deployment_script = self.project_path / 'deploy.sh'
        
        if not deployment_script.exists():
            logger.error("Deployment script not found. Run setup_infrastructure() first.")
            return {
                'success': False,
                'error': 'Deployment script not found',
                'message': 'Please run setup_infrastructure() first to generate deployment scripts.'
            }
        
        logger.info(f"Deploying application to {environment}...")
        
        try:
            import subprocess
            
            # Make script executable (Unix-like systems)
            import os
            if os.name != 'nt':  # Not Windows
                deployment_script.chmod(0o755)
            
            # Run deployment script
            result = subprocess.run(
                [str(deployment_script), environment],
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            
            if result.returncode == 0:
                logger.info("Deployment completed successfully!")
                return {
                    'success': True,
                    'environment': environment,
                    'output': result.stdout,
                    'message': f'Application deployed successfully to {environment}'
                }
            else:
                logger.error(f"Deployment failed: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr,
                    'message': f'Deployment to {environment} failed'
                }
        
        except subprocess.TimeoutExpired:
            logger.error("Deployment timed out after 10 minutes")
            return {
                'success': False,
                'error': 'Deployment timeout',
                'message': 'Deployment timed out after 10 minutes'
            }
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Deployment failed: {e}'
            }
    
    def generate_project_team(
        self,
        project_description: str,
        team_size: int = 9
    ) -> Dict[str, Any]:
        """
        Generate custom expert AI team for your project.
        
        When you describe your project, AI creates a tailored team of world-class
        experts with relevant expertise for your specific domain.
        
        Example:
            >>> framework = GravityFramework()
            >>> team = framework.generate_project_team(
            ...     "Building an e-commerce platform with AI recommendations"
            ... )
            >>> print(f"Team generated: {len(team['team_members'])} experts")
        
        Args:
            project_description: Description of your project
            team_size: Number of team members (default: 9)
            
        Returns:
            Dictionary with:
            - team_members: List of expert profiles
            - team_prompt: Complete TEAM_PROMPT.md for your project
            - project_analysis: AI analysis of your project
            - expertise_coverage: How well team covers requirements
        """
        logger.info("Generating custom expert team for your project...")
        
        team_data = self.team_generator.generate_team(
            project_description,
            team_size
        )
        
        # Save team prompt to project
        prompt_file = self.team_generator.save_team_prompt(
            team_data,
            self.project_path
        )
        
        logger.info(f"✅ Team generated! Prompt saved to: {prompt_file}")
        logger.info(f"Team: {len(team_data['team_members'])} experts")
        logger.info(f"Coverage: {team_data['expertise_coverage']['coverage_percentage']:.1f}%")
        
        return team_data
    
    def smart_commit(
        self,
        message: Optional[str] = None,
        files: Optional[List[str]] = None,
        auto_fix: bool = True
    ) -> Dict[str, Any]:
        """
        Intelligent Git commit with automatic standards enforcement.
        
        This method:
        1. Validates all code against TEAM_PROMPT.md standards
        2. Runs comprehensive pre-commit checks
        3. Auto-fixes code quality issues
        4. Generates/validates commit message (Conventional Commits)
        5. Creates commit only if all checks pass
        
        Example:
            >>> framework = GravityFramework()
            >>> result = framework.smart_commit(
            ...     message="feat(auth): add OAuth2 support"
            ... )
            >>> print(result['success'])  # True if committed
        
        Args:
            message: Commit message (will be generated if not provided)
            files: Files to commit (default: all staged files)
            auto_fix: Automatically fix code issues (default: True)
            
        Returns:
            Dictionary with commit results
        """
        if not self.git:
            return {
                'success': False,
                'error': 'Not a Git repository'
            }
        
        logger.info("Running smart commit...")
        
        result = self.git.smart_commit(
            message=message,
            files=files,
            auto_fix=auto_fix,
            skip_checks=False  # NEVER skip checks!
        )
        
        return result
    
    def validate_standards(self) -> Dict[str, Any]:
        """
        Validate entire project against TEAM_PROMPT.md standards.
        
        Checks:
        - English-only code/comments
        - Type hints on all functions
        - Docstrings present
        - No hardcoded secrets
        - Proper imports
        - Test coverage >= 95%
        
        Example:
            >>> framework = GravityFramework()
            >>> validation = framework.validate_standards()
            >>> if validation['valid']:
            ...     print("All standards met! ✅")
            ... else:
            ...     print(f"Found {validation['files_with_violations']} files with issues")
        
        Returns:
            Dictionary with validation results
        """
        logger.info("Validating project standards...")
        
        result = self.standards.validate_project()
        
        if result['valid']:
            logger.info("✅ All standards met!")
        else:
            logger.warning(
                f"❌ {result['files_with_violations']} files have violations"
            )
        
        return result
    
    def auto_fix_standards(self, file_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Automatically fix standards violations using AI.
        
        AI will:
        - Add missing type hints
        - Generate docstrings
        - Fix English language issues
        - Remove hardcoded secrets
        - Improve code quality
        
        Example:
            >>> framework = GravityFramework()
            >>> # Fix all files
            >>> framework.auto_fix_standards()
            >>> 
            >>> # Fix specific file
            >>> framework.auto_fix_standards("app/services/payment.py")
        
        Args:
            file_path: Specific file to fix (default: all files with violations)
            
        Returns:
            Dictionary with fix results
        """
        if file_path:
            logger.info(f"Auto-fixing: {file_path}")
            return self.standards.auto_fix_file(Path(file_path))
        else:
            # Fix all files with violations
            validation = self.validate_standards()
            
            if validation['valid']:
                return {
                    'success': True,
                    'message': 'No fixes needed, all standards met'
                }
            
            results = []
            for file_result in validation['violations']:
                fix_result = self.standards.auto_fix_file(
                    Path(file_result['file'])
                )
                results.append(fix_result)
            
            return {
                'success': True,
                'files_fixed': len(results),
                'results': results
            }
    
    def analyze_commits(self) -> Dict[str, Any]:
        """
        Analyze changed files and show commit recommendations.
        
        This method groups changed files by category and suggests
        how to organize commits.
        
        Example:
            >>> framework = GravityFramework()
            >>> analysis = framework.analyze_commits()
            >>> print(analysis['summary'])
        
        Returns:
            Dictionary with:
            - groups: Categorized files
            - summary: Change summary
            - recommendations: Suggested commits
        """
        if not self.commit_manager:
            return {
                'success': False,
                'error': 'Git integration not available'
            }
        
        return self.commit_manager.analyze_changes()
    
    def organize_and_commit(
        self,
        auto_generate_messages: bool = True,
        push: bool = False
    ) -> Dict[str, Any]:
        """
        Create organized commits based on file categories.
        
        This method:
        1. Groups changed files by type (features, docs, tests, etc.)
        2. Creates separate commit for each group
        3. Generates appropriate commit messages
        4. Optionally pushes to remote
        
        Example:
            >>> framework = GravityFramework()
            >>> # Commit and push
            >>> result = framework.organize_and_commit(push=True)
            >>> print(f"Created {result['commits']['total_commits']} commits")
        
        Args:
            auto_generate_messages: Use AI for commit messages (default: True)
            push: Push commits after creating them (default: False)
            
        Returns:
            Dictionary with commit results
        """
        if not self.commit_manager:
            return {
                'success': False,
                'error': 'Git integration not available'
            }
        
        return self.commit_manager.create_organized_commits(
            auto_generate_messages=auto_generate_messages,
            push_after_commit=push
        )
    
    def smart_commit_push(self) -> Dict[str, Any]:
        """
        Complete smart commit and push workflow.
        
        This is the ONE-COMMAND solution for commits:
        1. Analyzes all changes
        2. Groups files logically
        3. Creates organized commits
        4. Pushes to remote
        
        All following TEAM_PROMPT.md standards!
        
        Example:
            >>> framework = GravityFramework()
            >>> # Make changes to files...
            >>> # Then one command to commit and push everything:
            >>> framework.smart_commit_push()
            >>> # Done! All changes committed and pushed properly!
        
        Returns:
            Complete workflow results
        """
        if not self.commit_manager:
            return {
                'success': False,
                'error': 'Git integration not available'
            }
        
        return self.commit_manager.smart_commit_and_push()
    
    def check_auto_commit(self) -> Optional[Dict[str, Any]]:
        """
        Check if auto-commit threshold reached (100 files).
        
        As per TEAM_PROMPT.md: "Commit and push every 100 file changes"
        
        This method checks if 100+ files have changed and automatically
        commits and pushes if threshold is reached.
        
        Example:
            >>> framework = GravityFramework()
            >>> # After making many changes...
            >>> result = framework.check_auto_commit()
            >>> if result:
            >>>     print("Auto-committed!")
        
        Returns:
            Commit results if threshold reached, None otherwise
        """
        if not self.auto_commit:
            return None
        
        return self.auto_commit.check_and_commit()
    
    # ==========================================
    # Project Management Methods
    # ==========================================
    
    def analyze_project_plan(self, description: str) -> Dict[str, Any]:
        """
        Analyze project and generate comprehensive task breakdown.
        
        AI Project Manager (Dr. Marcus Hartmann) analyzes your project
        and creates detailed task list with:
        - Milestones
        - Tasks with dependencies
        - Time estimates
        - Team assignments
        - Risk assessment
        
        Example:
            >>> framework = GravityFramework()
            >>> analysis = framework.analyze_project_plan('''
            ...     Building e-commerce platform with:
            ...     - User authentication
            ...     - Product catalog
            ...     - Shopping cart
            ...     - Payment processing
            ...     - Order management
            ... ''')
            >>> print(f"Milestones: {len(analysis['milestones'])}")
        
        Args:
            description: Project description
            
        Returns:
            Dictionary with project analysis
        """
        return self.project_manager.analyze_project(description)
    
    def create_project_tasks(self, description: str) -> List:
        """
        Create project tasks from description.
        
        This is a shortcut that:
        1. Analyzes project
        2. Creates all tasks
        3. Saves to file
        
        Example:
            >>> framework = GravityFramework()
            >>> tasks = framework.create_project_tasks("Build REST API")
            >>> print(f"Created {len(tasks)} tasks")
        
        Args:
            description: Project description
            
        Returns:
            List of created tasks
        """
        analysis = self.project_manager.analyze_project(description)
        return self.project_manager.create_tasks_from_analysis(analysis)
    
    def get_project_tasks(
        self,
        status: Optional[str] = None,
        assignee: Optional[str] = None
    ) -> List:
        """
        Get project tasks with optional filters.
        
        Example:
            >>> # Get all tasks
            >>> all_tasks = framework.get_project_tasks()
            >>> 
            >>> # Get completed tasks
            >>> completed = framework.get_project_tasks(status='completed')
            >>> 
            >>> # Get tasks for specific person
            >>> my_tasks = framework.get_project_tasks(assignee='Dr. Chen Wei')
        
        Args:
            status: Filter by status (not-started, in-progress, completed, blocked)
            assignee: Filter by assignee name
            
        Returns:
            List of tasks
        """
        from gravity_framework.project.manager import TaskStatus
        
        status_enum = TaskStatus(status) if status else None
        
        return self.project_manager.get_task_list(
            status=status_enum,
            assignee=assignee
        )
    
    def get_next_tasks(self, assignee: Optional[str] = None) -> List:
        """
        Get next tasks to work on.
        
        Returns tasks that:
        - Are not started
        - Have all dependencies completed
        - Are sorted by priority
        
        Example:
            >>> framework = GravityFramework()
            >>> next_tasks = framework.get_next_tasks()
            >>> for task in next_tasks[:3]:  # Top 3 tasks
            >>>     print(f"- {task.title} (Priority: {task.priority.value})")
        
        Args:
            assignee: Filter by assignee
            
        Returns:
            List of tasks ready to start
        """
        return self.project_manager.get_next_tasks(assignee)
    
    def get_project_progress(self) -> Dict[str, Any]:
        """
        Get project progress report.
        
        Example:
            >>> framework = GravityFramework()
            >>> progress = framework.get_project_progress()
            >>> print(f"Completion: {progress['completion_rate']}%")
            >>> print(f"In Progress: {progress['in_progress']}")
            >>> print(f"Blockers: {len(progress['blockers'])}")
        
        Returns:
            Dictionary with progress metrics
        """
        return self.project_manager.get_progress_report()
    
    def generate_todo_list(self, format: str = 'markdown') -> str:
        """
        Generate formatted TODO list.
        
        Example:
            >>> framework = GravityFramework()
            >>> 
            >>> # Markdown format
            >>> markdown = framework.generate_todo_list('markdown')
            >>> with open('TODO.md', 'w') as f:
            >>>     f.write(markdown)
            >>> 
            >>> # JSON format
            >>> json_data = framework.generate_todo_list('json')
        
        Args:
            format: Output format ('markdown', 'json', 'text')
            
        Returns:
            Formatted TODO list
        """
        return self.project_manager.generate_todo_list(format)
    
    # ==================== Learning System Methods ====================
    
    def get_smart_recommendations(
        self,
        operation: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Get AI-powered smart recommendations based on learning.
        
        The system learns from every operation and provides increasingly
        better recommendations over time.
        
        Example:
            >>> framework = GravityFramework()
            >>> 
            >>> # Get recommendations for deployment
            >>> recs = framework.get_smart_recommendations(
            >>>     'deployment',
            >>>     {'environment': 'production', 'services': ['auth', 'api']}
            >>> )
            >>> for rec in recs:
            >>>     print(f"💡 {rec}")
        
        Args:
            operation: Operation type (deployment, service_discovery, etc.)
            context: Operation context
            
        Returns:
            List of smart recommendations
        """
        if not self.learning:
            return []
        
        return self.learning.get_smart_recommendations(
            operation,
            context or {}
        )
    
    def get_learning_report(self) -> Dict[str, Any]:
        """
        Get comprehensive learning report.
        
        Shows how much the system has learned and where it's improving.
        
        Example:
            >>> framework = GravityFramework()
            >>> report = framework.get_learning_report()
            >>> 
            >>> print(f"Total events learned: {report['statistics']['total_events']}")
            >>> print(f"Success rate: {report['statistics']['success_rate']:.1f}%")
            >>> print(f"Solutions discovered: {report['statistics']['solutions_learned']}")
            >>> 
            >>> print("\nTop operations:")
            >>> for op in report['top_operations']:
            >>>     print(f"  {op['operation']}: {op['total']} times ({op['success_rate']}%)")
        
        Returns:
            Comprehensive learning report with statistics
        """
        if not self.learning:
            return {
                'error': 'Learning system not enabled',
                'statistics': {},
                'top_operations': [],
                'improvement_areas': [],
                'knowledge_growth': {}
            }
        
        return self.learning.get_learning_report()
    
    def switch_ai_provider(
        self,
        provider: AIProvider,
        api_key: Optional[str] = None
    ) -> bool:
        """
        Switch AI provider at runtime.
        
        Example:
            >>> framework = GravityFramework()
            >>> 
            >>> # Start with free Ollama
            >>> framework.discover_services()
            >>> 
            >>> # Switch to GPT-4 for complex analysis
            >>> framework.switch_ai_provider(
            >>>     AIProvider.OPENAI,
            >>>     api_key='sk-...'
            >>> )
            >>> analysis = framework.analyze_project_plan("Complex system")
            >>> 
            >>> # Switch back to free Ollama
            >>> framework.switch_ai_provider(AIProvider.OLLAMA)
        
        Args:
            provider: New AI provider
            api_key: API key (if required)
            
        Returns:
            True if successful
        """
        if not self.learning:
            logger.warning("Learning system not enabled")
            return False
        
        try:
            # Update learning system
            if api_key:
                self.learning.ai.api_keys[provider.value] = api_key
            
            self.learning.ai.primary_provider = provider
            
            # Re-initialize clients
            self.learning.ai._initialize_clients()
            
            logger.info(f"Switched to AI provider: {provider.value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to switch AI provider: {e}")
            return False
    
    # ==================== Multi-Database Access Methods ====================
    
    async def register_service_databases(self) -> int:
        """
        Auto-register all service databases for multi-access.
        
        Scans all discovered services and registers their databases
        for unified access and learning.
        
        Example:
            >>> framework = GravityFramework()
            >>> services = framework.discover_services()
            >>> await framework.install()
            >>> 
            >>> # Register all databases
            >>> count = await framework.register_service_databases()
            >>> print(f"Registered {count} databases")
            >>> 
            >>> # Now can access all data
            >>> stats = await framework.get_all_database_stats()
        
        Returns:
            Number of databases registered
        """
        count = 0
        
        for service in self.registry.get_all():
            # Get database URL from service config
            service_config = service.manifest.config or {}
            database_url = service_config.get('database_url')
            
            if not database_url:
                # Try to construct from service metadata
                db_config = service.manifest.databases
                if db_config:
                    for db in db_config:
                        db_name = db.get('name', f"{service.manifest.name}_db")
                        db_type = db.get('type', 'postgresql')
                        
                        # Construct URL (assumes local development)
                        if db_type == 'postgresql':
                            database_url = f"postgresql+asyncpg://postgres:postgres@localhost/{db_name}"
                        elif db_type == 'mysql':
                            database_url = f"mysql+aiomysql://root:root@localhost/{db_name}"
                        
                        if database_url:
                            break
            
            if database_url:
                success = await self.multi_db.register_service_database(
                    service_name=service.manifest.name,
                    database_url=database_url,
                    database_type=service_config.get('database_type', 'postgresql')
                )
                
                if success:
                    count += 1
                    logger.info(f"Registered database for {service.manifest.name}")
        
        return count
    
    async def query_service_database(
        self,
        service_name: str,
        sql: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query a specific service's database.
        
        Example:
            >>> framework = GravityFramework()
            >>> await framework.register_service_databases()
            >>> 
            >>> # Query auth service
            >>> users = await framework.query_service_database(
            >>>     'auth-service',
            >>>     'SELECT * FROM users WHERE active = :active',
            >>>     {'active': True}
            >>> )
            >>> print(f"Active users: {len(users)}")
        
        Args:
            service_name: Service to query
            sql: SQL query
            params: Query parameters
            
        Returns:
            Query results
        """
        return await self.multi_db.query_service(service_name, sql, params)
    
    async def search_all_databases(
        self,
        search_term: str
    ) -> Dict[str, Any]:
        """
        Search for data across all service databases.
        
        Example:
            >>> framework = GravityFramework()
            >>> await framework.register_service_databases()
            >>> 
            >>> # Search for user email
            >>> results = await framework.search_all_databases('user@example.com')
            >>> 
            >>> for service, matches in results.items():
            >>>     print(f"{service}: {len(matches)} matches")
        
        Args:
            search_term: Term to search for
            
        Returns:
            Search results from all services
        """
        return await self.multi_db.search_across_services(search_term)
    
    async def get_all_database_stats(self) -> Dict[str, Any]:
        """
        Get statistics from all databases.
        
        Example:
            >>> framework = GravityFramework()
            >>> await framework.register_service_databases()
            >>> 
            >>> stats = await framework.get_all_database_stats()
            >>> 
            >>> for service, data in stats.items():
            >>>     print(f"{service}:")
            >>>     print(f"  Tables: {data['table_count']}")
            >>>     print(f"  Total rows: {data['total_rows']}")
        
        Returns:
            Statistics for all services
        """
        return await self.multi_db.get_statistics()
    
    async def learn_from_all_data(self) -> Dict[str, Any]:
        """
        Learn patterns and insights from all service data.
        
        Analyzes data across all microservices to discover:
        - Schema patterns
        - Data relationships
        - Usage patterns
        - Common structures
        
        Example:
            >>> framework = GravityFramework()
            >>> await framework.register_service_databases()
            >>> 
            >>> insights = await framework.learn_from_all_data()
            >>> 
            >>> print("Schemas discovered:")
            >>> for service, schema in insights['schemas'].items():
            >>>     print(f"  {service}: {len(schema['tables'])} tables")
            >>> 
            >>> print("\nPatterns found:")
            >>> for service, patterns in insights['patterns'].items():
            >>>     print(f"  {service}: {patterns}")
            >>> 
            >>> print("\nRelationships detected:")
            >>> for service, rels in insights['relationships'].items():
            >>>     print(f"  {service}: {len(rels)} relationships")
        
        Returns:
            Comprehensive learning insights
        """
        insights = await self.multi_db.learn_from_data()
        
        # Also record in learning system
        if self.learning:
            # Record schemas as learning event
            self.learning.knowledge_base.record_event(
                from gravity_framework.learning.system import LearningEvent
                
                event = LearningEvent(
                    event_type='data_analysis',
                    context={
                        'services': list(insights['schemas'].keys()),
                        'total_tables': sum(
                            len(s.get('tables', {})) 
                            for s in insights['schemas'].values()
                        )
                    },
                    outcome='patterns_discovered',
                    success=True
                )
            )
        
        return insights
    
    async def answer_with_data(
        self,
        question: str
    ) -> Dict[str, Any]:
        """
        Answer user questions using data from all microservices.
        
        Uses AI and database access to answer questions by:
        1. Understanding the question
        2. Searching relevant databases
        3. Aggregating data from multiple services
        4. Providing comprehensive answer
        
        Example:
            >>> framework = GravityFramework()
            >>> await framework.register_service_databases()
            >>> 
            >>> # Ask about users
            >>> answer = await framework.answer_with_data(
            >>>     "How many active users do we have?"
            >>> )
            >>> print(answer)
            >>> 
            >>> # Ask about orders
            >>> answer = await framework.answer_with_data(
            >>>     "What is the total revenue this month?"
            >>> )
            >>> print(answer)
        
        Args:
            question: User's question
            
        Returns:
            Answer with supporting data
        """
        ai_client = self.learning.ai if self.learning else None
        return await self.multi_db.answer_user_query(question, ai_client)
    
    async def federated_query(
        self,
        table_name: str,
        where: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query a table across all services that have it.
        
        If multiple services have the same table (e.g., "users"),
        this will query all of them and combine results.
        
        Example:
            >>> framework = GravityFramework()
            >>> await framework.register_service_databases()
            >>> 
            >>> # Get all users from all services
            >>> all_users = await framework.federated_query(
            >>>     'users',
            >>>     where='active = true',
            >>>     limit=50
            >>> )
            >>> 
            >>> # Results include source service
            >>> for user in all_users:
            >>>     print(f"{user['email']} from {user['_source_service']}")
        
        Args:
            table_name: Table to query
            where: Optional WHERE clause
            limit: Maximum rows per service
            
        Returns:
            Combined results with source service tag
        """
        return await self.data_federation.federated_query(table_name, where, limit)
    
    async def aggregate_data(
        self,
        table_name: str,
        aggregate_func: str = "COUNT(*)"
    ) -> Dict[str, Any]:
        """
        Aggregate data across all services.
        
        Example:
            >>> framework = GravityFramework()
            >>> await framework.register_service_databases()
            >>> 
            >>> # Count users across all services
            >>> result = await framework.aggregate_data('users', 'COUNT(*)')
            >>> print(f"Total users: {result['total']}")
            >>> 
            >>> for service, count in result['by_service'].items():
            >>>     print(f"  {service}: {count}")
            >>> 
            >>> # Sum revenue
            >>> result = await framework.aggregate_data('orders', 'SUM(total)')
            >>> print(f"Total revenue: ${result['total']}")
        
        Args:
            table_name: Table to aggregate
            aggregate_func: SQL aggregate function
            
        Returns:
            Aggregated results by service and total
        """
        return await self.data_federation.aggregate_across_services(
            table_name,
            aggregate_func
        )
    
    async def learn_from_database_data(self) -> Dict[str, Any]:
        """
        Enhanced learning from all database data.
        
        Combines:
        - Schema analysis
        - Data pattern detection
        - Relationship discovery
        - AI-powered insights
        
        Example:
            >>> framework = GravityFramework()
            >>> await framework.register_service_databases()
            >>> 
            >>> # Learn from all data
            >>> insights = await framework.learn_from_database_data()
            >>> 
            >>> print("Data Patterns:")
            >>> for service, patterns in insights['data_patterns'].items():
            >>>     print(f"  {service}:")
            >>>     print(f"    Tables: {patterns['table_count']}")
            >>>     print(f"    Relationships: {len(patterns['relationships'])}")
            >>> 
            >>> print("\nRecommendations:")
            >>> for rec in insights['recommendations']:
            >>>     print(f"  - {rec}")
        
            
        Returns:
            Comprehensive learning insights with recommendations
        """
        # Get database insights
        db_insights = await self.multi_db.learn_from_data()
        
        # If learning enabled, use AI for deeper analysis
        if self.learning:
            ai_insights = await self.learning.learn_from_database_data(self.multi_db)
            
            # Merge insights
            return {
                **db_insights,
                **ai_insights,
                'ai_enhanced': True
            }
        
        return db_insights
    
    # ===================================================================
    # AUTONOMOUS DEVELOPMENT METHODS
    # ===================================================================
    
    async def develop_application_autonomously(
        self,
        description: str,
        industry: str = "general"
    ) -> Dict[str, Any]:
        """
        Autonomously develop complete full-stack application with AI team.
        
        The AI team will:
        1. Analyze requirements
        2. Design architecture
        3. Design database
        4. Develop frontend
        5. Develop backend
        6. Implement security
        7. Design testing
        8. Design deployment
        
        ALL decisions are made by team voting (12+ members).
        NO user interaction needed!
        
        Args:
            description: High-level description of application to build
            industry: Industry type (ecommerce, healthcare, finance, education, general)
            
        Example:
            >>> framework = GravityFramework()
            >>> 
            >>> # Autonomous development - team decides everything!
            >>> result = await framework.develop_application_autonomously(
            ...     description="E-commerce platform with product catalog, cart, and payments",
            ...     industry="ecommerce"
            ... )
            >>> 
            >>> print(f"Team Size: {result['team_size']}")
            >>> print(f"Approval Rate: {result['approval_rate']:.1f}%")
            >>> 
            >>> # See all phases
            >>> for phase, data in result['phases'].items():
            ...     print(f"\n{phase.upper()}:")
            ...     if data.get('approved'):
            ...         print(f"  ✓ Approved by team")
            ...         print(f"  Support: {data['vote']['support_percentage']:.1f}%")
            
        Returns:
            Complete development results with all code and decisions
        """
        logger.info(f"Starting autonomous development: {description}")
        
        # Create autonomous development system
        auto_dev = AutonomousDevelopmentSystem(
            project_name=self.project_path.name,
            industry=industry,
            ai_client=self.ai if self.learning else self.ai
        )
        
        # Develop application (AI team handles everything!)
        result = await auto_dev.develop_application(description)
        
        # Get detailed report
        report = auto_dev.get_development_report()
        
        # Record learning event
        if self.learning:
            await self.learning.record_autonomous_development(
                description=description,
                industry=industry,
                result=result,
                report=report
            )
        
        logger.info("Autonomous development completed!")
        
        return {
            **result,
            **report
        }
    
    def get_development_team_info(self, industry: str = "general") -> Dict[str, Any]:
        """
        Get information about the AI development team.
        
        Args:
            industry: Industry type for specialized consultant
            
        Example:
            >>> framework = GravityFramework()
            >>> team_info = framework.get_development_team_info("healthcare")
            >>> 
            >>> print(f"Team Size: {team_info['team_size']}")
            >>> print("\nTeam Members:")
            >>> for member in team_info['members']:
            ...     print(f"  {member['name']} ({member['role']})")
            ...     print(f"    IQ: {member['iq']}, Experience: {member['experience']} years")
            ...     print(f"    Vote Weight: {member['vote_weight']:.2f}")
            
        Returns:
            Team information including all members
        """
        from gravity_framework.ai.autonomous_dev import DevelopmentTeam
        
        team = DevelopmentTeam(industry)
        
        return {
            'team_size': len(team.members),
            'industry': industry,
            'members': [
                {
                    'name': m.name,
                    'role': m.role.value,
                    'specialization': m.specialization,
                    'iq': m.iq,
                    'experience': m.experience_years,
                    'vote_weight': m.vote_weight
                }
                for m in team.members
            ],
            'voting_system': 'Democratic with weighted votes',
            'decision_method': 'Team consensus (no user input)',
            'minimum_approval': '50% weighted support'
        }
                    'message': f'Deployment to {environment} failed'
                }
        
        except subprocess.TimeoutExpired:
            logger.error("Deployment timed out after 10 minutes")
            return {
                'success': False,
                'error': 'Deployment timeout',
                'message': 'Deployment timed out after 10 minutes'
            }
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Deployment failed: {e}'
            }
        
        return self.registry.get_all()