"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_orchestrator.py
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

    config = {
        "postgres_host": "localhost",
        "postgres_port": 5432,
        "postgres_user": "test_user",
        "postgres_password": "test_pass",
        "mysql_host": "localhost",
        "mysql_port": 3306,
        "mysql_user": "test_user",
        "mysql_password": "test_pass",
    }
    return DatabaseOrchestrator(config)


@pytest.fixture
def service_with_postgres():
    """Create service with PostgreSQL requirement."""
    manifest = ServiceManifest(
        name="test-service",
        version="1.0.0",
        repository="https://github.com/test/service",
        databases=[
            DatabaseRequirement(
                name="test_db",
                type=DatabaseType.POSTGRESQL,
                extensions=["uuid-ossp", "pgcrypto"]
            )
        ]
    )
    return Service(manifest=manifest)


@pytest.fixture
def service_with_mysql():
    """Create service with MySQL requirement."""
    manifest = ServiceManifest(
        name="test-service",
        version="1.0.0",
        repository="https://github.com/test/service",
        databases=[
            DatabaseRequirement(
                name="test_db",
                type=DatabaseType.MYSQL,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci"
            )
        ]
    )
    return Service(manifest=manifest)


@pytest.fixture
def service_with_mongodb():
    """Create service with MongoDB requirement."""
    manifest = ServiceManifest(
        name="test-service",
        version="1.0.0",
        repository="https://github.com/test/service",
        databases=[
            DatabaseRequirement(
                name="test_db",
                type=DatabaseType.MONGODB
            )
        ]
    )
    return Service(manifest=manifest)


class TestDatabaseOrchestrator:
    """Test DatabaseOrchestrator class."""
    
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initializes with config."""
        assert orchestrator.postgres_host == "localhost"
        assert orchestrator.postgres_port == 5432
        assert orchestrator.mysql_host == "localhost"
    
    @pytest.mark.asyncio
    async def test_setup_databases_no_requirements(self, orchestrator):
        """Test setup with no database requirements."""
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="repo",
            databases=[]
        )
        service = Service(manifest=manifest)
        
        result = await orchestrator.setup_databases(service)
        assert result is True
    
    @pytest.mark.asyncio
    @patch('gravity_framework.database.orchestrator.asyncpg.connect')
    async def test_create_postgres_db(self, mock_connect, orchestrator, service_with_postgres):
        """Test creating PostgreSQL database."""
        mock_conn = AsyncMock()
        mock_conn.fetchval = AsyncMock(return_value=None)
        mock_conn.execute = AsyncMock()
        mock_conn.close = AsyncMock()
        mock_connect.return_value = mock_conn
        
        result = await orchestrator.setup_databases(service_with_postgres)
        
        assert result is True
        assert "test_db" in service_with_postgres.created_databases
    
    @pytest.mark.asyncio
    @patch('gravity_framework.database.orchestrator.aiomysql.connect')
    async def test_create_mysql_db(self, mock_connect, orchestrator, service_with_mysql):
        """Test creating MySQL database."""
        # Create async mock cursor
        mock_cursor = AsyncMock()
        mock_cursor.fetchone = AsyncMock(return_value=None)
        mock_cursor.execute = AsyncMock()
        mock_cursor.__aenter__ = AsyncMock(return_value=mock_cursor)
        mock_cursor.__aexit__ = AsyncMock(return_value=None)
        
        # Create async mock connection
        mock_conn = AsyncMock()
        mock_conn.cursor = MagicMock(return_value=mock_cursor)
        mock_conn.commit = AsyncMock()
        mock_conn.close = MagicMock()  # aiomysql uses sync close
        
        # Make connect return the connection
        async def async_connect(*args, **kwargs):
            return mock_conn
        
        mock_connect.side_effect = async_connect
        
        result = await orchestrator.setup_databases(service_with_mysql)
        
        assert result is True
        assert "test_db" in service_with_mysql.created_databases
    
    @pytest.mark.asyncio
    async def test_get_connection_string_postgres(self, orchestrator):
        """Test generating PostgreSQL connection string."""
        db_req = DatabaseRequirement(
            name="test_db",
            type=DatabaseType.POSTGRESQL
        )
        
        conn_str = await orchestrator.get_connection_string(db_req)
        
        assert "postgresql+asyncpg://" in conn_str
        assert "test_user" in conn_str
        assert "test_db" in conn_str
    
    @pytest.mark.asyncio
    async def test_get_connection_string_mysql(self, orchestrator):
        """Test generating MySQL connection string."""
        db_req = DatabaseRequirement(
            name="test_db",
            type=DatabaseType.MYSQL,
            charset="utf8mb4"
        )
        
        conn_str = await orchestrator.get_connection_string(db_req)
        
        assert "mysql+aiomysql://" in conn_str
        assert "test_user" in conn_str
        assert "charset=utf8mb4" in conn_str
    
    @pytest.mark.asyncio
    async def test_get_connection_string_mongodb(self, orchestrator):
        """Test generating MongoDB connection string."""
        db_req = DatabaseRequirement(
            name="test_db",
            type=DatabaseType.MONGODB
        )
        
        conn_str = await orchestrator.get_connection_string(db_req)
        
        assert "mongodb://" in conn_str
        assert "test_db" in conn_str
    
    @pytest.mark.asyncio
    async def test_get_connection_string_redis(self, orchestrator):
        """Test generating Redis connection string."""
        db_req = DatabaseRequirement(
            name="cache",
            type=DatabaseType.REDIS
        )
        
        conn_str = await orchestrator.get_connection_string(db_req)
        
        assert "redis://" in conn_str
