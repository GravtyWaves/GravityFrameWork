"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/deployment/composer.py
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


from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

from gravity_framework.models.service import Service, DatabaseRequirement


class DockerComposeGenerator:
    """
    Generates docker-compose.yml configurations from discovered services.
    
    This class takes a list of services with their manifests and creates
    a complete docker-compose configuration including:
    - Service containers with proper environment variables
    - Database containers (PostgreSQL, MySQL, MongoDB, Redis)
    - Network configuration for service communication
    - Volume mounts for persistence
    - Dependency ordering
    
    Example:
        >>> generator = DockerComposeGenerator()
        >>> compose_config = await generator.generate(services)
        >>> await generator.write_file(compose_config, Path("docker-compose.yml"))
    """
    
    def __init__(self, base_port: int = 8000):
        """
        Initialize the Docker Compose generator.
        
        Args:
            base_port: Starting port number for port mapping (default: 8000)
        """
        self.base_port = base_port
        self.port_counter = base_port
    
    async def generate(self, services: List[Service]) -> Dict[str, Any]:
        """
        Generate complete docker-compose configuration.
        
        Args:
            services: List of services to include in the configuration
            
        Returns:
            Dictionary representing docker-compose.yml structure
            
        Example:
            >>> services = [auth_service, user_service]
            >>> config = await generator.generate(services)
            >>> config['version']
            '3.9'
        """
        compose = {
            "version": "3.9",
            "services": {},
            "networks": {
                "gravity-net": {
                    "driver": "bridge",
                    "name": "gravity-network"
                }
            },
            "volumes": {}
        }
        
        # Collect all database requirements
        databases = self._collect_databases(services)
        
        # Add database containers first
        for db in databases:
            db_service = self._generate_database_service(db)
            compose["services"][db_service["name"]] = db_service["config"]
            
            # Add volume for database persistence
            volume_name = f"{db.name}_data"
            compose["volumes"][volume_name] = {
                "driver": "local"
            }
        
        # Add microservice containers
        for service in services:
            service_config = await self._generate_service_config(service, databases)
            compose["services"][service.manifest.name] = service_config
        
        return compose
    
    def _collect_databases(self, services: List[Service]) -> List[DatabaseRequirement]:
        """
        Collect all unique database requirements from services.
        
        Args:
            services: List of services to scan
            
        Returns:
            List of unique database requirements
        """
        databases = []
        seen = set()
        
        for service in services:
            for db_req in service.manifest.databases:
                # Use database name as unique identifier
                if db_req.name not in seen:
                    databases.append(db_req)
                    seen.add(db_req.name)
        
        return databases
    
    def _generate_database_service(self, db: DatabaseRequirement) -> Dict[str, Any]:
        """
        Generate Docker Compose service definition for a database.
        
        Args:
            db: Database requirement specification
            
        Returns:
            Dictionary with database service name and configuration
        """
        service_name = f"{db.name}-db"
        
        if db.type == "postgresql":
            config = {
                "image": f"postgres:{db.version or '15'}",
                "container_name": service_name,
                "environment": {
                    "POSTGRES_DB": db.name,
                    "POSTGRES_USER": "${POSTGRES_USER:-gravity}",
                    "POSTGRES_PASSWORD": "${POSTGRES_PASSWORD:-gravity_secret}",
                },
                "volumes": [
                    f"{db.name}_data:/var/lib/postgresql/data"
                ],
                "networks": ["gravity-net"],
                "healthcheck": {
                    "test": ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-gravity}"],
                    "interval": "10s",
                    "timeout": "5s",
                    "retries": 5
                },
                "restart": "unless-stopped"
            }
            
        elif db.type == "mysql":
            config = {
                "image": f"mysql:{db.version or '8.0'}",
                "container_name": service_name,
                "environment": {
                    "MYSQL_DATABASE": db.name,
                    "MYSQL_USER": "${MYSQL_USER:-gravity}",
                    "MYSQL_PASSWORD": "${MYSQL_PASSWORD:-gravity_secret}",
                    "MYSQL_ROOT_PASSWORD": "${MYSQL_ROOT_PASSWORD:-root_secret}",
                },
                "volumes": [
                    f"{db.name}_data:/var/lib/mysql"
                ],
                "networks": ["gravity-net"],
                "healthcheck": {
                    "test": ["CMD", "mysqladmin", "ping", "-h", "localhost"],
                    "interval": "10s",
                    "timeout": "5s",
                    "retries": 5
                },
                "restart": "unless-stopped"
            }
            
        elif db.type == "mongodb":
            config = {
                "image": f"mongo:{db.version or '6.0'}",
                "container_name": service_name,
                "environment": {
                    "MONGO_INITDB_DATABASE": db.name,
                    "MONGO_INITDB_ROOT_USERNAME": "${MONGO_USER:-gravity}",
                    "MONGO_INITDB_ROOT_PASSWORD": "${MONGO_PASSWORD:-gravity_secret}",
                },
                "volumes": [
                    f"{db.name}_data:/data/db"
                ],
                "networks": ["gravity-net"],
                "healthcheck": {
                    "test": ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"],
                    "interval": "10s",
                    "timeout": "5s",
                    "retries": 5
                },
                "restart": "unless-stopped"
            }
            
        elif db.type == "redis":
            config = {
                "image": f"redis:{db.version or '7-alpine'}",
                "container_name": service_name,
                "command": "redis-server --appendonly yes",
                "volumes": [
                    f"{db.name}_data:/data"
                ],
                "networks": ["gravity-net"],
                "healthcheck": {
                    "test": ["CMD", "redis-cli", "ping"],
                    "interval": "10s",
                    "timeout": "5s",
                    "retries": 5
                },
                "restart": "unless-stopped"
            }
        else:
            raise ValueError(f"Unsupported database type: {db.type}")
        
        return {
            "name": service_name,
            "config": config
        }
    
    async def _generate_service_config(
        self,
        service: Service,
        databases: List[DatabaseRequirement]
    ) -> Dict[str, Any]:
        """
        Generate Docker Compose configuration for a microservice.
        
        Args:
            service: Service to generate configuration for
            databases: List of all database requirements (for connection strings)
            
        Returns:
            Service configuration dictionary
        """
        # Generate environment variables
        environment = await self._generate_environment(service, databases)
        
        # Allocate host port
        host_port = self._allocate_port()
        
        # Build depends_on list
        depends_on = {}
        
        # Add database dependencies
        for db_req in service.manifest.databases:
            db_service_name = f"{db_req.name}-db"
            depends_on[db_service_name] = {
                "condition": "service_healthy"
            }
        
        # Add service dependencies
        for dep in service.manifest.dependencies:
            depends_on[dep.name] = {
                "condition": "service_started"
            }
        
        # Get container port from first port in manifest, or default to 8000
        container_port = service.manifest.ports[0].container if service.manifest.ports else 8000
        
        # Build service configuration
        config = {
            "build": {
                "context": f"./services/{service.manifest.name}",
                "dockerfile": "Dockerfile"
            },
            "image": f"{service.manifest.name}:latest",
            "container_name": service.manifest.name,
            "environment": environment,
            "ports": [
                f"{host_port}:{container_port}"
            ],
            "networks": ["gravity-net"],
            "volumes": [
                f"./services/{service.manifest.name}:/app"
            ],
            "restart": "unless-stopped"
        }
        
        # Add depends_on if there are dependencies
        if depends_on:
            config["depends_on"] = depends_on
        
        # Add health check if defined
        if service.manifest.health_check:
            config["healthcheck"] = {
                "test": ["CMD", "curl", "-f", f"http://localhost:{container_port}{service.manifest.health_check.endpoint}"],
                "interval": f"{service.manifest.health_check.interval}s",
                "timeout": f"{service.manifest.health_check.timeout}s",
                "retries": service.manifest.health_check.retries,
                "start_period": "30s"
            }
        
        return config
    
    async def _generate_environment(
        self,
        service: Service,
        databases: List[DatabaseRequirement]
    ) -> Dict[str, str]:
        """
        Generate environment variables for a service.
        
        Args:
            service: Service to generate environment for
            databases: All database requirements
            
        Returns:
            Dictionary of environment variables
        """
        env = {}
        
        # Add service-specific environment variables
        for key, value in service.manifest.environment.variables.items():
            env[key] = value
        
        # Add database connection strings
        for db_req in service.manifest.databases:
            env_var_name = f"{db_req.name.upper()}_URL"
            connection_string = self._generate_connection_string(db_req)
            env[env_var_name] = connection_string
        
        # Get container port from first port in manifest, or default to 8000
        container_port = service.manifest.ports[0].container if service.manifest.ports else 8000
        
        # Add URLs for dependent services
        for dep in service.manifest.dependencies:
            service_url_var = f"{dep.name.upper().replace('-', '_')}_URL"
            env[service_url_var] = f"http://{dep.name}:{container_port}"
        
        return env
    
    def _generate_connection_string(self, db: DatabaseRequirement) -> str:
        """
        Generate database connection string.
        
        Args:
            db: Database requirement
            
        Returns:
            Connection string for the database
        """
        db_service_name = f"{db.name}-db"
        
        if db.type == "postgresql":
            return f"postgresql://${{POSTGRES_USER:-gravity}}:${{POSTGRES_PASSWORD:-gravity_secret}}@{db_service_name}:5432/{db.name}"
        
        elif db.type == "mysql":
            return f"mysql://${{MYSQL_USER:-gravity}}:${{MYSQL_PASSWORD:-gravity_secret}}@{db_service_name}:3306/{db.name}"
        
        elif db.type == "mongodb":
            return f"mongodb://${{MONGO_USER:-gravity}}:${{MONGO_PASSWORD:-gravity_secret}}@{db_service_name}:27017/{db.name}"
        
        elif db.type == "redis":
            return f"redis://{db_service_name}:6379/0"
        
        else:
            raise ValueError(f"Unsupported database type: {db.type}")
    
    def _allocate_port(self) -> int:
        """
        Allocate next available host port.
        
        Returns:
            Port number
        """
        port = self.port_counter
        self.port_counter += 1
        return port
    
    async def write_file(self, config: Dict[str, Any], output_path: Path) -> None:
        """
        Write docker-compose configuration to file.
        
        Args:
            config: Docker Compose configuration dictionary
            output_path: Path where to write the file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                config,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True
            )
    
    async def generate_env_template(self, services: List[Service]) -> str:
        """
        Generate .env.example file with all required environment variables.
        
        Args:
            services: List of services
            
        Returns:
            Content for .env.example file
        """
        lines = [
            "# Gravity Framework Environment Variables",
            "# Copy this file to .env and update with your values",
            "",
            "# Database Credentials",
            "POSTGRES_USER=gravity",
            "POSTGRES_PASSWORD=gravity_secret",
            "MYSQL_USER=gravity",
            "MYSQL_PASSWORD=gravity_secret",
            "MYSQL_ROOT_PASSWORD=root_secret",
            "MONGO_USER=gravity",
            "MONGO_PASSWORD=gravity_secret",
            ""
        ]
        
        # Add service-specific variables
        for service in services:
            if service.manifest.environment.variables:
                lines.append(f"# {service.manifest.name} environment")
                for key in service.manifest.environment.variables.keys():
                    lines.append(f"{key}=")
                lines.append("")
        
        return "\n".join(lines)
