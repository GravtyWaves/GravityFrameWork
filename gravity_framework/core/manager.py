"""Service lifecycle manager."""

import logging
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import httpx
import docker
from docker.models.containers import Container

from gravity_framework.models.service import Service, ServiceStatus

logger = logging.getLogger(__name__)


class ServiceManager:
    """Service lifecycle manager."""
    
    def __init__(self, docker_client=None):
        """Initialize service manager.
        
        Args:
            docker_client: Optional Docker client instance. If None, will be created on first use.
        """
        self._docker_client = docker_client
        self.containers: Dict[str, Container] = {}
    
    @property
    def docker_client(self):
        """Lazy-load Docker client."""
        if self._docker_client is None:
            self._docker_client = docker.from_env()
        return self._docker_client
    
    async def install_service(self, service: Service) -> bool:
        """Install a service (run install script if exists).
        
        Args:
            service: Service instance
            
        Returns:
            True if installation was successful
        """
        logger.info(f"Installing service: {service.manifest.name}")
        
        if not service.path:
            logger.error(f"Service path not set for {service.manifest.name}")
            return False
        
        service.status = ServiceStatus.INSTALLING
        
        try:
            service_path = Path(service.path)
            
            # Check for install script
            if service.manifest.install_script:
                script_path = service_path / service.manifest.install_script
                
                if script_path.exists():
                    logger.info(f"Running install script: {service.manifest.install_script}")
                    
                    result = subprocess.run(
                        ["/bin/bash", str(script_path)],
                        cwd=service_path,
                        capture_output=True,
                        text=True,
                        timeout=300  # 5 minutes timeout
                    )
                    
                    if result.returncode != 0:
                        logger.error(f"Install script failed: {result.stderr}")
                        service.status = ServiceStatus.ERROR
                        service.error_message = result.stderr
                        return False
                    
                    logger.debug(f"Install output: {result.stdout}")
            
            # Check for requirements.txt (Python services)
            requirements_file = service_path / "requirements.txt"
            if requirements_file.exists():
                logger.info("Installing Python dependencies...")
                
                result = subprocess.run(
                    ["pip", "install", "-r", "requirements.txt"],
                    cwd=service_path,
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 minutes timeout
                )
                
                if result.returncode != 0:
                    logger.warning(f"Failed to install dependencies: {result.stderr}")
            
            # Check for package.json (Node.js services)
            package_json = service_path / "package.json"
            if package_json.exists():
                logger.info("Installing Node.js dependencies...")
                
                result = subprocess.run(
                    ["npm", "install"],
                    cwd=service_path,
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                
                if result.returncode != 0:
                    logger.warning(f"Failed to install npm dependencies: {result.stderr}")
            
            service.status = ServiceStatus.INSTALLED
            logger.info(f"✓ Service installed: {service.manifest.name}")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error(f"Installation timeout for {service.manifest.name}")
            service.status = ServiceStatus.ERROR
            service.error_message = "Installation timeout"
            return False
        except Exception as e:
            logger.error(f"Installation failed for {service.manifest.name}: {e}")
            service.status = ServiceStatus.ERROR
            service.error_message = str(e)
            return False
    
    async def start_service(self, service: Service, env_vars: Optional[Dict[str, str]] = None) -> bool:
        """Start a service in Docker container.
        
        Args:
            service: Service instance
            env_vars: Additional environment variables
            
        Returns:
            True if service started successfully
        """
        logger.info(f"Starting service: {service.manifest.name}")
        
        if not service.path:
            logger.error(f"Service path not set for {service.manifest.name}")
            return False
        
        service.status = ServiceStatus.STARTING
        
        try:
            # Prepare environment variables
            environment = service.manifest.environment.variables.copy()
            if env_vars:
                environment.update(env_vars)
            
            # Add database connection strings
            for db in service.created_databases:
                db_req = next((d for d in service.manifest.databases if d.name == db), None)
                if db_req:
                    env_key = f"{db.upper()}_URL"
                    # This will be set by database orchestrator
                    environment.setdefault(env_key, "")
            
            # Prepare port mappings
            ports = {}
            for port_config in service.manifest.ports:
                host_port = port_config.host or self._find_free_port()
                container_port = port_config.container
                ports[f"{container_port}/{port_config.protocol}"] = host_port
                service.assigned_ports[container_port] = host_port
            
            # Prepare volumes
            volumes = {
                str(Path(service.path).absolute()): {
                    'bind': service.manifest.working_dir,
                    'mode': 'rw'
                }
            }
            
            # Build Docker image if Dockerfile exists
            dockerfile_path = Path(service.path) / "Dockerfile"
            image_name = f"gravity-{service.manifest.name}:{service.manifest.version}"
            
            if dockerfile_path.exists():
                logger.info(f"Building Docker image: {image_name}")
                
                # Build arguments
                buildargs = service.manifest.build_args.copy()
                
                image, build_logs = self.docker_client.images.build(
                    path=service.path,
                    tag=image_name,
                    buildargs=buildargs,
                    rm=True
                )
                
                for log in build_logs:
                    if 'stream' in log:
                        logger.debug(log['stream'].strip())
            else:
                # Use base runtime image
                image_name = service.manifest.runtime
            
            # Start container
            container = self.docker_client.containers.run(
                image_name,
                command=service.manifest.command,
                environment=environment,
                ports=ports,
                volumes=volumes,
                working_dir=service.manifest.working_dir,
                name=f"gravity-{service.manifest.name}",
                detach=True,
                restart_policy={"Name": "unless-stopped"},
                labels={
                    "gravity.service": service.manifest.name,
                    "gravity.version": service.manifest.version,
                    "gravity.type": service.manifest.type.value
                }
            )
            
            service.container_id = container.id
            self.containers[service.manifest.name] = container
            
            # Wait for service to be healthy
            if service.manifest.health_check:
                logger.info(f"Waiting for {service.manifest.name} to become healthy...")
                if not await self._wait_for_health(service):
                    logger.warning(f"Service {service.manifest.name} may not be healthy")
            
            service.status = ServiceStatus.RUNNING
            logger.info(f"✓ Service started: {service.manifest.name} (container: {container.short_id})")
            return True
            
        except docker.errors.ContainerError as e:
            logger.error(f"Container error for {service.manifest.name}: {e}")
            service.status = ServiceStatus.ERROR
            service.error_message = str(e)
            return False
        except docker.errors.ImageNotFound as e:
            logger.error(f"Image not found for {service.manifest.name}: {e}")
            service.status = ServiceStatus.ERROR
            service.error_message = f"Image not found: {service.manifest.runtime}"
            return False
        except Exception as e:
            logger.error(f"Failed to start {service.manifest.name}: {e}")
            service.status = ServiceStatus.ERROR
            service.error_message = str(e)
            return False
    
    async def stop_service(self, service: Service, timeout: int = 10) -> bool:
        """Stop a running service.
        
        Args:
            service: Service instance
            timeout: Graceful shutdown timeout in seconds
            
        Returns:
            True if service stopped successfully
        """
        logger.info(f"Stopping service: {service.manifest.name}")
        
        if not service.container_id:
            logger.warning(f"No container ID for {service.manifest.name}")
            return True
        
        service.status = ServiceStatus.STOPPING
        
        try:
            container = self.docker_client.containers.get(service.container_id)
            container.stop(timeout=timeout)
            
            service.status = ServiceStatus.STOPPED
            logger.info(f"✓ Service stopped: {service.manifest.name}")
            return True
            
        except docker.errors.NotFound:
            logger.warning(f"Container not found: {service.container_id}")
            service.status = ServiceStatus.STOPPED
            return True
        except Exception as e:
            logger.error(f"Failed to stop {service.manifest.name}: {e}")
            service.status = ServiceStatus.ERROR
            service.error_message = str(e)
            return False
    
    async def restart_service(self, service: Service) -> bool:
        """Restart a service.
        
        Args:
            service: Service instance
            
        Returns:
            True if service restarted successfully
        """
        logger.info(f"Restarting service: {service.manifest.name}")
        
        if not await self.stop_service(service):
            return False
        
        await asyncio.sleep(2)  # Wait a bit
        
        return await self.start_service(service)
    
    async def get_service_logs(self, service: Service, tail: int = 100) -> str:
        """Get service logs.
        
        Args:
            service: Service instance
            tail: Number of lines to return
            
        Returns:
            Log output
        """
        if not service.container_id:
            return "No container running"
        
        try:
            container = self.docker_client.containers.get(service.container_id)
            logs = container.logs(tail=tail, timestamps=True).decode('utf-8')
            return logs
        except Exception as e:
            logger.error(f"Failed to get logs for {service.manifest.name}: {e}")
            return f"Error getting logs: {e}"
    
    async def check_health(self, service: Service) -> bool:
        """Check if service is healthy.
        
        Args:
            service: Service instance
            
        Returns:
            True if service is healthy
        """
        if not service.manifest.health_check:
            # If no health check defined, check if container is running
            return service.status == ServiceStatus.RUNNING
        
        # Get host port for health check
        if not service.assigned_ports:
            return False
        
        # Find HTTP port
        http_port = None
        for container_port, host_port in service.assigned_ports.items():
            if container_port in [80, 8080, 3000, 5000]:
                http_port = host_port
                break
        
        if not http_port:
            http_port = list(service.assigned_ports.values())[0]
        
        # Make health check request
        url = f"http://localhost:{http_port}{service.manifest.health_check.endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    timeout=service.manifest.health_check.timeout
                )
                return response.status_code == 200
        except Exception:
            return False
    
    async def _wait_for_health(self, service: Service, max_attempts: Optional[int] = None) -> bool:
        """Wait for service to become healthy.
        
        Args:
            service: Service instance
            max_attempts: Maximum number of attempts (uses health_check.retries if None)
            
        Returns:
            True if service became healthy
        """
        if not service.manifest.health_check:
            return True
        
        attempts = max_attempts or service.manifest.health_check.retries
        interval = service.manifest.health_check.interval
        
        for i in range(attempts):
            if await self.check_health(service):
                return True
            
            if i < attempts - 1:
                await asyncio.sleep(interval)
        
        return False
    
    def _find_free_port(self) -> int:
        """Find a free port on the host.
        
        Returns:
            Free port number
        """
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
