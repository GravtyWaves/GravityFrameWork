"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_composer.py
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

import pytest
from gravity_framework.models.service import (
    Service,
    ServiceManifest,
    ServicePort,
    DatabaseRequirement,
    ServiceDependency,
    HealthCheck
)
from gravity_framework.deployment.composer import DockerComposeGenerator


@pytest.fixture
def sample_services():
    """Create sample services for testing."""
    # Auth service with PostgreSQL and Redis
    auth_manifest = ServiceManifest(
        name="auth-service",
        version="1.0.0",
        repository="https://github.com/test/auth-service",
        type="api",
        ports=[ServicePort(container=8000)],
        databases=[
            DatabaseRequirement(name="auth_db", type="postgresql", version="15"),
            DatabaseRequirement(name="auth_cache", type="redis", version="7")
        ],
        dependencies=[],
        health_check=HealthCheck(
            endpoint="/health",
            interval=30,
            timeout=5,
            retries=3
        )
    )
    auth_manifest.environment.variables = {"LOG_LEVEL": "info", "DEBUG": "false"}
    
    auth_service = Service(manifest=auth_manifest)
    
    # User service with PostgreSQL, depends on auth
    user_manifest = ServiceManifest(
        name="user-service",
        version="1.5.0",
        repository="https://github.com/test/user-service",
        type="api",
        ports=[ServicePort(container=8000)],
        databases=[
            DatabaseRequirement(name="user_db", type="postgresql", version="15")
        ],
        dependencies=[
            ServiceDependency(name="auth-service", version=">=1.0.0")
        ],
        health_check=HealthCheck(
            endpoint="/health",
            interval=30,
            timeout=5,
            retries=3
        )
    )
    user_manifest.environment.variables = {"LOG_LEVEL": "debug"}
    
    user_service = Service(manifest=user_manifest)
    
    return [auth_service, user_service]


@pytest.mark.asyncio
async def test_generate_compose_config(sample_services):
    """Test generating docker-compose configuration."""
    generator = DockerComposeGenerator(base_port=8001)
    config = await generator.generate(sample_services)
    
    # Check version
    assert config["version"] == "3.9"
    
    # Check networks
    assert "gravity-net" in config["networks"]
    assert config["networks"]["gravity-net"]["driver"] == "bridge"
    
    # Check volumes
    assert "auth_db_data" in config["volumes"]
    assert "auth_cache_data" in config["volumes"]
    assert "user_db_data" in config["volumes"]


@pytest.mark.asyncio
async def test_database_services_generated(sample_services):
    """Test that database services are correctly generated."""
    generator = DockerComposeGenerator()
    config = await generator.generate(sample_services)
    
    services = config["services"]
    
    # Check PostgreSQL databases
    assert "auth_db-db" in services
    assert services["auth_db-db"]["image"].startswith("postgres:")
    assert services["auth_db-db"]["environment"]["POSTGRES_DB"] == "auth_db"
    
    assert "user_db-db" in services
    assert services["user_db-db"]["image"].startswith("postgres:")
    
    # Check Redis
    assert "auth_cache-db" in services
    assert services["auth_cache-db"]["image"].startswith("redis:")


@pytest.mark.asyncio
async def test_service_dependencies(sample_services):
    """Test that service dependencies are correctly set."""
    generator = DockerComposeGenerator()
    config = await generator.generate(sample_services)
    
    services = config["services"]
    
    # Auth service depends on its databases
    auth_depends = services["auth-service"]["depends_on"]
    assert "auth_db-db" in auth_depends
    assert "auth_cache-db" in auth_depends
    assert auth_depends["auth_db-db"]["condition"] == "service_healthy"
    
    # User service depends on its database AND auth-service
    user_depends = services["user-service"]["depends_on"]
    assert "user_db-db" in user_depends
    assert "auth-service" in user_depends


@pytest.mark.asyncio
async def test_environment_variables(sample_services):
    """Test that environment variables are correctly generated."""
    generator = DockerComposeGenerator()
    config = await generator.generate(sample_services)
    
    services = config["services"]
    
    # Check auth service environment
    auth_env = services["auth-service"]["environment"]
    assert "LOG_LEVEL" in auth_env
    assert auth_env["LOG_LEVEL"] == "info"
    assert "AUTH_DB_URL" in auth_env
    assert "postgresql://" in auth_env["AUTH_DB_URL"]
    assert "AUTH_CACHE_URL" in auth_env
    assert "redis://" in auth_env["AUTH_CACHE_URL"]
    
    # Check user service has auth service URL
    user_env = services["user-service"]["environment"]
    assert "AUTH_SERVICE_URL" in user_env
    assert "http://auth-service:" in user_env["AUTH_SERVICE_URL"]


@pytest.mark.asyncio
async def test_port_allocation(sample_services):
    """Test that ports are correctly allocated."""
    generator = DockerComposeGenerator(base_port=9000)
    config = await generator.generate(sample_services)
    
    services = config["services"]
    
    # First service should get base_port
    auth_ports = services["auth-service"]["ports"]
    assert "9000:8000" in auth_ports
    
    # Second service should get base_port + 1
    user_ports = services["user-service"]["ports"]
    assert "9001:8000" in user_ports


@pytest.mark.asyncio
async def test_health_checks(sample_services):
    """Test that health checks are correctly configured."""
    generator = DockerComposeGenerator()
    config = await generator.generate(sample_services)
    
    services = config["services"]
    
    # Check service health check
    auth_health = services["auth-service"]["healthcheck"]
    assert "curl" in " ".join(auth_health["test"])
    assert "/health" in " ".join(auth_health["test"])
    assert auth_health["interval"] == "30s"
    assert auth_health["retries"] == 3
    
    # Check database health check
    postgres_health = services["auth_db-db"]["healthcheck"]
    assert "pg_isready" in " ".join(postgres_health["test"])


@pytest.mark.asyncio
async def test_collect_databases(sample_services):
    """Test database collection with deduplication."""
    generator = DockerComposeGenerator()
    databases = generator._collect_databases(sample_services)
    
    # Should have 3 unique databases
    db_names = [db.name for db in databases]
    assert len(db_names) == 3
    assert "auth_db" in db_names
    assert "auth_cache" in db_names
    assert "user_db" in db_names


@pytest.mark.asyncio
async def test_mysql_database():
    """Test MySQL database configuration."""
    manifest = ServiceManifest(
        name="test-service",
        version="1.0.0",
        repository="https://github.com/test/test-service",
        type="api",
        databases=[
            DatabaseRequirement(name="test_db", type="mysql", version="8.0")
        ]
    )
    
    service = Service(manifest=manifest)
    
    generator = DockerComposeGenerator()
    config = await generator.generate([service])
    
    mysql_service = config["services"]["test_db-db"]
    assert mysql_service["image"] == "mysql:8.0"
    assert mysql_service["environment"]["MYSQL_DATABASE"] == "test_db"


@pytest.mark.asyncio
async def test_mongodb_database():
    """Test MongoDB database configuration."""
    manifest = ServiceManifest(
        name="test-service",
        version="1.0.0",
        repository="https://github.com/test/test-service",
        type="api",
        databases=[
            DatabaseRequirement(name="test_db", type="mongodb", version="6.0")
        ]
    )
    
    service = Service(manifest=manifest)
    
    generator = DockerComposeGenerator()
    config = await generator.generate([service])
    
    mongo_service = config["services"]["test_db-db"]
    assert mongo_service["image"] == "mongo:6.0"
    assert mongo_service["environment"]["MONGO_INITDB_DATABASE"] == "test_db"


@pytest.mark.asyncio
async def test_write_file(sample_services, tmp_path):
    """Test writing docker-compose.yml to file."""
    generator = DockerComposeGenerator()
    config = await generator.generate(sample_services)
    
    output_file = tmp_path / "docker-compose.yml"
    await generator.write_file(config, output_file)
    
    assert output_file.exists()
    
    # Verify content
    content = output_file.read_text()
    assert "version: '3.9'" in content or 'version: "3.9"' in content
    assert "auth-service:" in content
    assert "user-service:" in content


@pytest.mark.asyncio
async def test_generate_env_template(sample_services):
    """Test .env.example generation."""
    generator = DockerComposeGenerator()
    env_content = await generator.generate_env_template(sample_services)
    
    assert "POSTGRES_USER" in env_content
    assert "POSTGRES_PASSWORD" in env_content
    assert "MYSQL_USER" in env_content
    assert "MONGO_USER" in env_content
    assert "LOG_LEVEL" in env_content
