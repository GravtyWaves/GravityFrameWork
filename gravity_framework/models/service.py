"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/models/service.py
PURPOSE: Data models for services and service registry
DESCRIPTION: Defines Service, ServiceManifest, ServiceRegistry and related models
             for representing and managing microservices.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""

    API = "api"
    WEB = "web"
    WORKER = "worker"
    CRON = "cron"
    DATABASE = "database"
    CACHE = "cache"


class DatabaseType(str, Enum):
    """Database types."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"


class ServiceStatus(str, Enum):
    """Service status."""
    UNKNOWN = "unknown"
    DISCOVERED = "discovered"
    INSTALLING = "installing"
    INSTALLED = "installed"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class DatabaseRequirement(BaseModel):
    """Database requirement model."""
    name: str = Field(..., description="Database name")
    type: DatabaseType = Field(..., description="Database type")
    version: Optional[str] = Field(None, description="Required version")
    charset: Optional[str] = Field("utf8mb4", description="Character set")
    collation: Optional[str] = Field(None, description="Collation")
    extensions: Optional[List[str]] = Field(default_factory=list, description="PostgreSQL extensions")


class ServiceDependency(BaseModel):
    """Service dependency model."""
    name: str = Field(..., description="Dependency service name")
    version: Optional[str] = Field(None, description="Required version range")
    optional: bool = Field(False, description="Whether dependency is optional")


class HealthCheck(BaseModel):
    """Health check configuration."""
    endpoint: str = Field("/health", description="Health check endpoint")
    interval: int = Field(30, description="Check interval in seconds")
    timeout: int = Field(5, description="Timeout in seconds")
    retries: int = Field(3, description="Number of retries")


class ServicePort(BaseModel):
    """Service port configuration."""
    container: int = Field(..., description="Container port")
    host: Optional[int] = Field(None, description="Host port (auto-assigned if not specified)")
    protocol: str = Field("tcp", description="Protocol (tcp/udp)")


class ServiceEnvironment(BaseModel):
    """Service environment configuration."""
    variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    secrets: List[str] = Field(default_factory=list, description="Secret names")


class ServiceManifest(BaseModel):
    """Service manifest model (gravity-service.yaml)."""
    
    # Basic info
    name: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    description: Optional[str] = Field(None, description="Service description")
    type: ServiceType = Field(ServiceType.API, description="Service type")
    
    # Repository info
    repository: str = Field(..., description="Git repository URL")
    branch: str = Field("main", description="Git branch")
    
    # Dependencies
    dependencies: List[ServiceDependency] = Field(default_factory=list, description="Service dependencies")
    
    # Database requirements
    databases: List[DatabaseRequirement] = Field(default_factory=list, description="Database requirements")
    
    # Runtime config
    runtime: str = Field("python:3.11", description="Runtime environment")
    command: Optional[str] = Field(None, description="Start command")
    working_dir: str = Field("/app", description="Working directory")
    
    # Networking
    ports: List[ServicePort] = Field(default_factory=list, description="Port mappings")
    health_check: Optional[HealthCheck] = Field(None, description="Health check config")
    
    # Environment
    environment: ServiceEnvironment = Field(default_factory=ServiceEnvironment, description="Environment config")
    
    # API Gateway
    api_prefix: Optional[str] = Field(None, description="API path prefix")
    public: bool = Field(False, description="Whether service has public endpoints")
    
    # Resources
    cpu_limit: Optional[str] = Field(None, description="CPU limit (e.g., '1.0')")
    memory_limit: Optional[str] = Field(None, description="Memory limit (e.g., '512M')")
    
    # Installation
    install_script: Optional[str] = Field(None, description="Installation script")
    build_args: Dict[str, str] = Field(default_factory=dict, description="Build arguments")
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """Validate service name."""
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Service name must contain only alphanumeric characters, hyphens, and underscores")
        return v.lower()
    
    @field_validator("version")
    @classmethod
    def validate_version(cls, v):
        """Validate semantic version."""
        parts = v.split(".")
        if len(parts) < 2:
            raise ValueError("Version must be in format X.Y or X.Y.Z")
        return v


class Service(BaseModel):
    """Service instance model."""
    
    # Manifest data
    manifest: ServiceManifest
    
    # Runtime state
    status: ServiceStatus = Field(ServiceStatus.DISCOVERED, description="Current status")
    path: Optional[str] = Field(None, description="Local path")
    container_id: Optional[str] = Field(None, description="Container ID")
    
    # Assigned ports
    assigned_ports: Dict[int, int] = Field(default_factory=dict, description="Container port -> Host port mapping")
    
    # Database info
    created_databases: List[str] = Field(default_factory=list, description="Created database names")
    
    # Errors
    error_message: Optional[str] = Field(None, description="Last error message")
    
    model_config = ConfigDict(use_enum_values=True)


class ServiceRegistry(BaseModel):
    """Service registry model."""
    
    services: Dict[str, Service] = Field(default_factory=dict, description="Registered services")
    
    def add_service(self, service: Service) -> None:
        """Add a service to registry."""
        self.services[service.manifest.name] = service
    
    def get_service(self, name: str) -> Optional[Service]:
        """Get a service by name."""
        return self.services.get(name)
    
    def remove_service(self, name: str) -> bool:
        """Remove a service from registry."""
        if name in self.services:
            del self.services[name]
            return True
        return False
    
    def get_by_status(self, status: ServiceStatus) -> List[Service]:
        """Get all services with specific status."""
        return [s for s in self.services.values() if s.status == status]
    
    def get_all(self) -> List[Service]:
        """Get all services."""
        return list(self.services.values())
