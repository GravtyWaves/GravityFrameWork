"""
Core framework module containing the main GravityFramework class.
"""

from typing import Optional, Dict, List, Any
import logging
import asyncio
from pathlib import Path

from gravity_framework.models.service import Service, ServiceRegistry, ServiceStatus
from gravity_framework.discovery.scanner import ServiceScanner
from gravity_framework.resolver.dependency import DependencyResolver
from gravity_framework.database.orchestrator import DatabaseOrchestrator
from gravity_framework.core.manager import ServiceManager

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
    
    def __init__(self, project_path: Optional[Path] = None, config: Optional[Dict] = None):
        """
        Initialize the Gravity Framework.
        
        Args:
            project_path: Path to the Gravity project directory.
                         If None, uses current directory.
            config: Optional configuration dictionary
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.config = config or {}
        
        # Initialize components
        self.registry = ServiceRegistry()
        self.scanner = ServiceScanner(self.project_path / "services")
        self.db_orchestrator = DatabaseOrchestrator(self.config.get("databases", {}))
        self.service_manager = ServiceManager()
        
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
                return services
                
        except Exception as e:
            logger.error(f"Error discovering services: {e}")
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
                return False
            
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
