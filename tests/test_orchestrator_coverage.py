"""Comprehensive tests for DatabaseOrchestrator to improve coverage."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from pathlib import Path

from gravity_framework.database.orchestrator import DatabaseOrchestrator
from gravity_framework.models.service import (
    Service, ServiceManifest, ServiceType, DatabaseType, DatabaseRequirement
)


@pytest.fixture
def orchestrator():
    """Create a DatabaseOrchestrator instance."""
    config = {
        "postgres_host": "localhost",
        "postgres_port": 5432,
        "postgres_user": "test_user",
        "postgres_password": "test_pass",
        "mysql_host": "localhost",
        "mysql_port": 3306,
        "mysql_user": "test_user",
        "mysql_password": "test_pass",
        "mongodb_host": "localhost",
        "mongodb_port": 27017,
        "mongodb_user": "test_user",
        "mongodb_password": "test_pass",
        "redis_host": "localhost",
        "redis_port": 6379,
        "redis_password": "test_pass"
    }
    return DatabaseOrchestrator(config)


@pytest.fixture
def service_with_postgres():
    """Service with PostgreSQL database."""
    manifest = ServiceManifest(
        name="auth-service",
        type=ServiceType.API,
        version="1.0.0",
        repository="https://github.com/test/auth",
        databases=[
            DatabaseRequirement(
                name="auth_db",
                type=DatabaseType.POSTGRESQL,
                extensions=["uuid-ossp", "pgcrypto"]
            )
        ]
    )
    service = Service(manifest=manifest)
    service.path = "/services/auth"
    return service


@pytest.fixture
def service_with_mysql():
    """Service with MySQL database."""
    manifest = ServiceManifest(
        name="user-service",
        type=ServiceType.API,
        version="1.0.0",
        repository="https://github.com/test/user",
        databases=[
            DatabaseRequirement(
                name="user_db",
                type=DatabaseType.MYSQL,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci"
            )
        ]
    )
    service = Service(manifest=manifest)
    service.path = "/services/user"
    return service


@pytest.fixture
def service_with_mongodb():
    """Service with MongoDB database."""
    manifest = ServiceManifest(
        name="logging-service",
        type=ServiceType.API,
        version="1.0.0",
        repository="https://github.com/test/logging",
        databases=[
            DatabaseRequirement(
                name="logs_db",
                type=DatabaseType.MONGODB
            )
        ]
    )
    service = Service(manifest=manifest)
    service.path = "/services/logging"
    return service


@pytest.fixture
def service_with_redis():
    """Service with Redis."""
    manifest = ServiceManifest(
        name="cache-service",
        type=ServiceType.API,
        version="1.0.0",
        repository="https://github.com/test/cache",
        databases=[
            DatabaseRequirement(
                name="cache",
                type=DatabaseType.REDIS
            )
        ]
    )
    service = Service(manifest=manifest)
    service.path = "/services/cache"
    return service


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test orchestrator initializes with default config."""
    orchestrator = DatabaseOrchestrator()
    assert orchestrator.postgres_host == "localhost"
    assert orchestrator.postgres_port == 5432
    assert orchestrator.mysql_host == "localhost"
    assert orchestrator.redis_host == "localhost"


@pytest.mark.asyncio
async def test_orchestrator_with_custom_config():
    """Test orchestrator with custom configuration."""
    config = {
        "postgres_host": "custom-host",
        "postgres_port": 5433,
        "mysql_user": "custom_user"
    }
    orchestrator = DatabaseOrchestrator(config)
    assert orchestrator.postgres_host == "custom-host"
    assert orchestrator.postgres_port == 5433
    assert orchestrator.mysql_user == "custom_user"


@pytest.mark.asyncio
async def test_setup_databases_no_databases():
    """Test setup_databases with service that has no databases."""
    orchestrator = DatabaseOrchestrator()
    manifest = ServiceManifest(
        name="static-service",
        type=ServiceType.WEB,
        version="1.0.0",
        repository="https://github.com/test/static"
    )
    service = Service(manifest=manifest)
    service.path = "/services/static"
    
    result = await orchestrator.setup_databases(service)
    assert result is True
    assert len(service.created_databases) == 0


@pytest.mark.asyncio
async def test_create_postgres_db_success(orchestrator, service_with_postgres):
    """Test successful PostgreSQL database creation."""
    mock_conn = AsyncMock()
    mock_conn.fetchval = AsyncMock(return_value=None)  # DB doesn't exist
    mock_conn.execute = AsyncMock()
    mock_conn.close = AsyncMock()
    
    mock_db_conn = AsyncMock()
    mock_db_conn.execute = AsyncMock()
    mock_db_conn.close = AsyncMock()
    
    with patch("gravity_framework.database.orchestrator.asyncpg.connect") as mock_connect:
        mock_connect.side_effect = [mock_conn, mock_db_conn]
        
        result = await orchestrator.setup_databases(service_with_postgres)
        
        assert result is True
        assert "auth_db" in service_with_postgres.created_databases
        mock_conn.execute.assert_called_once()
        # Verify extensions were installed
        assert mock_db_conn.execute.call_count == 2


@pytest.mark.asyncio
async def test_create_postgres_db_already_exists(orchestrator, service_with_postgres):
    """Test PostgreSQL database creation when DB already exists."""
    mock_conn = AsyncMock()
    mock_conn.fetchval = AsyncMock(return_value=1)  # DB exists
    mock_conn.close = AsyncMock()
    
    with patch("gravity_framework.database.orchestrator.asyncpg.connect", return_value=mock_conn):
        result = await orchestrator.setup_databases(service_with_postgres)
        
        assert result is True
        mock_conn.execute.assert_not_called()


@pytest.mark.asyncio
async def test_create_mysql_db_success(orchestrator, service_with_mysql):
    """Test successful MySQL database creation."""
    mock_cursor = AsyncMock()
    mock_cursor.fetchone = AsyncMock(return_value=None)  # DB doesn't exist
    mock_cursor.execute = AsyncMock()
    mock_cursor.__aenter__ = AsyncMock(return_value=mock_cursor)
    mock_cursor.__aexit__ = AsyncMock()
    
    mock_conn = AsyncMock()
    mock_conn.cursor = MagicMock(return_value=mock_cursor)
    mock_conn.commit = AsyncMock()
    mock_conn.close = MagicMock()
    
    with patch("gravity_framework.database.orchestrator.aiomysql.connect", return_value=mock_conn):
        result = await orchestrator.setup_databases(service_with_mysql)
        
        assert result is True
        assert "user_db" in service_with_mysql.created_databases


@pytest.mark.asyncio
async def test_create_mysql_db_already_exists(orchestrator, service_with_mysql):
    """Test MySQL database creation when DB already exists."""
    mock_cursor = AsyncMock()
    mock_cursor.fetchone = AsyncMock(return_value=("user_db",))  # DB exists
    mock_cursor.execute = AsyncMock()
    mock_cursor.__aenter__ = AsyncMock(return_value=mock_cursor)
    mock_cursor.__aexit__ = AsyncMock()
    
    mock_conn = AsyncMock()
    mock_conn.cursor = MagicMock(return_value=mock_cursor)
    mock_conn.close = MagicMock()
    
    with patch("gravity_framework.database.orchestrator.aiomysql.connect", return_value=mock_conn):
        result = await orchestrator.setup_databases(service_with_mysql)
        
        assert result is True


@pytest.mark.asyncio
async def test_create_mongodb_success(orchestrator, service_with_mongodb):
    """Test successful MongoDB database creation."""
    mock_db = AsyncMock()
    mock_db.create_collection = AsyncMock()
    mock_db.command = AsyncMock()
    
    mock_client = MagicMock()
    mock_client.__getitem__ = MagicMock(return_value=mock_db)
    mock_client.close = MagicMock()
    
    with patch("gravity_framework.database.orchestrator.AsyncIOMotorClient", return_value=mock_client):
        result = await orchestrator.setup_databases(service_with_mongodb)
        
        assert result is True
        assert "logs_db" in service_with_mongodb.created_databases
        mock_db.create_collection.assert_called_once_with("_gravity_init")
        mock_db.command.assert_called_once_with("ping")


@pytest.mark.asyncio
async def test_setup_redis_success(orchestrator, service_with_redis):
    """Test successful Redis setup."""
    mock_redis = AsyncMock()
    mock_redis.ping = AsyncMock()
    mock_redis.close = AsyncMock()
    
    with patch("gravity_framework.database.orchestrator.aioredis.from_url", return_value=mock_redis):
        result = await orchestrator.setup_databases(service_with_redis)
        
        assert result is True
        assert "cache" in service_with_redis.created_databases
        mock_redis.ping.assert_called_once()


@pytest.mark.asyncio
async def test_setup_databases_failure(orchestrator, service_with_postgres):
    """Test database setup failure handling."""
    with patch("gravity_framework.database.orchestrator.asyncpg.connect", side_effect=Exception("Connection failed")):
        result = await orchestrator.setup_databases(service_with_postgres)
        
        assert result is False
        assert len(service_with_postgres.created_databases) == 0


@pytest.mark.asyncio
async def test_get_connection_string_postgres(orchestrator):
    """Test PostgreSQL connection string generation."""
    db_req = DatabaseRequirement(
        name="test_db",
        type=DatabaseType.POSTGRESQL
    )
    
    conn_str = await orchestrator.get_connection_string(db_req)
    
    assert conn_str == "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db"


@pytest.mark.asyncio
async def test_get_connection_string_mysql(orchestrator):
    """Test MySQL connection string generation."""
    db_req = DatabaseRequirement(
        name="test_db",
        type=DatabaseType.MYSQL,
        charset="utf8mb4"
    )
    
    conn_str = await orchestrator.get_connection_string(db_req)
    
    assert conn_str == "mysql+aiomysql://test_user:test_pass@localhost:3306/test_db?charset=utf8mb4"


@pytest.mark.asyncio
async def test_get_connection_string_mongodb_with_auth(orchestrator):
    """Test MongoDB connection string with authentication."""
    db_req = DatabaseRequirement(
        name="test_db",
        type=DatabaseType.MONGODB
    )
    
    conn_str = await orchestrator.get_connection_string(db_req)
    
    assert conn_str == "mongodb://test_user:test_pass@localhost:27017/test_db"


@pytest.mark.asyncio
async def test_get_connection_string_mongodb_without_auth():
    """Test MongoDB connection string without authentication."""
    orchestrator = DatabaseOrchestrator({
        "mongodb_host": "localhost",
        "mongodb_port": 27017
    })
    
    db_req = DatabaseRequirement(
        name="test_db",
        type=DatabaseType.MONGODB
    )
    
    conn_str = await orchestrator.get_connection_string(db_req)
    
    assert conn_str == "mongodb://localhost:27017/test_db"


@pytest.mark.asyncio
async def test_get_connection_string_redis(orchestrator):
    """Test Redis connection string generation."""
    db_req = DatabaseRequirement(
        name="cache",
        type=DatabaseType.REDIS
    )
    
    conn_str = await orchestrator.get_connection_string(db_req)
    
    assert conn_str == "redis://localhost:6379"


@pytest.mark.asyncio
async def test_get_connection_string_unknown_type(orchestrator):
    """Test connection string generation for unknown database type."""
    # We can't create an invalid DatabaseType, so skip this test
    # Pydantic validates the enum at creation time
    pytest.skip("Pydantic validates DatabaseType enum at creation")


@pytest.mark.asyncio
async def test_cleanup_databases_no_databases(orchestrator):
    """Test cleanup when service has no created databases."""
    manifest = ServiceManifest(
        name="test-service",
        type=ServiceType.API,
        version="1.0.0",
        repository="https://github.com/test/test"
    )
    service = Service(manifest=manifest)
    service.path = "/services/test"
    
    result = await orchestrator.cleanup_databases(service)
    assert result is True


@pytest.mark.asyncio
async def test_cleanup_postgres_db(orchestrator, service_with_postgres):
    """Test PostgreSQL database cleanup."""
    service_with_postgres.created_databases.append("auth_db")
    
    mock_conn = AsyncMock()
    mock_conn.execute = AsyncMock()
    mock_conn.close = AsyncMock()
    
    with patch("gravity_framework.database.orchestrator.asyncpg.connect", return_value=mock_conn):
        result = await orchestrator.cleanup_databases(service_with_postgres)
        
        assert result is True
        mock_conn.execute.assert_called_once()


@pytest.mark.asyncio
async def test_cleanup_mysql_db(orchestrator, service_with_mysql):
    """Test MySQL database cleanup."""
    service_with_mysql.created_databases.append("user_db")
    
    mock_cursor = AsyncMock()
    mock_cursor.execute = AsyncMock()
    mock_cursor.__aenter__ = AsyncMock(return_value=mock_cursor)
    mock_cursor.__aexit__ = AsyncMock()
    
    mock_conn = AsyncMock()
    mock_conn.cursor = MagicMock(return_value=mock_cursor)
    mock_conn.commit = AsyncMock()
    mock_conn.close = MagicMock()
    
    with patch("gravity_framework.database.orchestrator.aiomysql.connect", return_value=mock_conn):
        result = await orchestrator.cleanup_databases(service_with_mysql)
        
        assert result is True


@pytest.mark.asyncio
async def test_cleanup_mongodb(orchestrator, service_with_mongodb):
    """Test MongoDB database cleanup."""
    service_with_mongodb.created_databases.append("logs_db")
    
    mock_client = MagicMock()
    mock_client.drop_database = AsyncMock()
    mock_client.close = MagicMock()
    
    with patch("gravity_framework.database.orchestrator.AsyncIOMotorClient", return_value=mock_client):
        result = await orchestrator.cleanup_databases(service_with_mongodb)
        
        assert result is True
        mock_client.drop_database.assert_called_once_with("logs_db")


@pytest.mark.asyncio
async def test_cleanup_databases_failure(orchestrator, service_with_postgres):
    """Test cleanup failure handling."""
    service_with_postgres.created_databases.append("auth_db")
    
    with patch("gravity_framework.database.orchestrator.asyncpg.connect", side_effect=Exception("Cleanup failed")):
        result = await orchestrator.cleanup_databases(service_with_postgres)
        
        assert result is False
