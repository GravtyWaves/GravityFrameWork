"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_integration.py
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

    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_manifest_content():
    """Sample service manifest content."""
    return """
apiVersion: gravity/v1
kind: Service
metadata:
  name: test-service
  version: 1.0.0
  description: Test service for integration testing

spec:
  type: api
  runtime: python:3.11
  command: python main.py
  
  dependencies:
    - name: other-service
      version: ">=1.0.0"
  
  databases:
    - name: test_db
      type: postgresql
      version: "15"
  
  ports:
    - container: 8000
      host: 8000
  
  health_check:
    endpoint: /health
    interval: 30
    timeout: 5
    retries: 3
"""


@pytest.mark.integration
class TestIntegrationWorkflows:
    """Integration tests for complete workflows."""
    
    @pytest.mark.asyncio
    async def test_full_service_lifecycle(self, temp_workspace, sample_manifest_content):
        """Test complete service lifecycle: discover -> install -> start -> stop."""
        # Create service directory with manifest
        service_dir = temp_workspace / "test-service"
        service_dir.mkdir()
        (service_dir / "gravity-service.yaml").write_text(sample_manifest_content)
        (service_dir / "Dockerfile").write_text("FROM python:3.11\nCMD python main.py")
        
        # Initialize framework
        framework = GravityFramework(project_path=temp_workspace)
        
        # Mock Docker and database operations
        with patch('docker.from_env') as mock_docker, \
             patch.object(framework.db_orchestrator, 'setup_databases', new_callable=AsyncMock) as mock_db:
            
            mock_docker_client = Mock()
            mock_docker_client.images = Mock()
            mock_docker_client.containers = Mock()
            mock_docker.return_value = mock_docker_client
            
            # 1. Discover services
            services = await framework.discover_services(str(service_dir))
            assert len(services) == 1
            assert services[0].name == "test-service"
            
            # 2. Install service
            mock_docker_client.images.build.return_value = (Mock(id="image-id"), [])
            result = await framework.install("test-service")
            assert result is True
            
            service = framework.get_service("test-service")
            assert service.status == ServiceStatus.INSTALLED
            
            # 3. Setup databases
            mock_db.return_value = {"TEST_DB_URL": "postgresql://..."}
            
            # 4. Start service
            mock_container = Mock()
            mock_container.status = "running"
            mock_docker_client.containers.run.return_value = mock_container
            
            with patch.object(framework.service_manager, '_wait_for_health', return_value=True):
                result = await framework.start("test-service")
                assert result is True
            
            assert service.status == ServiceStatus.RUNNING
            
            # 5. Check health
            with patch('httpx.AsyncClient') as mock_http:
                mock_response = AsyncMock()
                mock_response.status_code = 200
                mock_http.return_value.__aenter__.return_value.get = AsyncMock(
                    return_value=mock_response
                )
                
                health = await framework.health_check("test-service")
                assert health is True
            
            # 6. Stop service
            result = await framework.stop("test-service")
            assert result is True
            assert service.status == ServiceStatus.STOPPED
    
    @pytest.mark.asyncio
    async def test_dependency_resolution_workflow(self, temp_workspace):
        """Test service dependency resolution in correct order."""
        # Create three services with dependencies
        # service-a depends on nothing
        # service-b depends on service-a
        # service-c depends on service-b
        
        manifests = {
            "service-a": """
apiVersion: gravity/v1
kind: Service
metadata:
  name: service-a
  version: 1.0.0
spec:
  type: api
  runtime: python:3.11
  command: python main.py
""",
            "service-b": """
apiVersion: gravity/v1
kind: Service
metadata:
  name: service-b
  version: 1.0.0
spec:
  type: api
  runtime: python:3.11
  command: python main.py
  dependencies:
    - name: service-a
      version: "^1.0.0"
""",
            "service-c": """
apiVersion: gravity/v1
kind: Service
metadata:
  name: service-c
  version: 1.0.0
spec:
  type: api
  runtime: python:3.11
  command: python main.py
  dependencies:
    - name: service-b
      version: "^1.0.0"
"""
        }
        
        # Create service directories
        for name, content in manifests.items():
            service_dir = temp_workspace / name
            service_dir.mkdir()
            (service_dir / "gravity-service.yaml").write_text(content)
        
        framework = GravityFramework(project_path=temp_workspace)
        
        # Discover all services
        for service_dir in temp_workspace.iterdir():
            await framework.discover_services(str(service_dir))
        
        # Resolve dependencies
        services = list(framework.registry.services.values())
        resolver = framework.dependency_resolver
        install_order = resolver.resolve(services)
        
        # Verify order: service-a -> service-b -> service-c
        names = [s.name for s in install_order]
        assert names.index("service-a") < names.index("service-b")
        assert names.index("service-b") < names.index("service-c")
    
    @pytest.mark.asyncio
    async def test_database_auto_creation_workflow(self, temp_workspace):
        """Test automatic database creation for services."""
        manifest = """
apiVersion: gravity/v1
kind: Service
metadata:
  name: db-service
  version: 1.0.0
spec:
  type: api
  runtime: python:3.11
  command: python main.py
  
  databases:
    - name: main_db
      type: postgresql
      version: "15"
      extensions:
        - uuid-ossp
    
    - name: cache_db
      type: redis
      version: "7"
"""
        
        service_dir = temp_workspace / "db-service"
        service_dir.mkdir()
        (service_dir / "gravity-service.yaml").write_text(manifest)
        
        framework = GravityFramework(project_path=temp_workspace)
        
        # Discover service
        services = await framework.discover_services(str(service_dir))
        service = services[0]
        
        # Mock database creation
        with patch.object(framework.db_orchestrator, '_create_postgres_db', new_callable=AsyncMock) as mock_pg, \
             patch.object(framework.db_orchestrator, '_setup_redis', new_callable=AsyncMock) as mock_redis:
            
            mock_pg.return_value = "postgresql://localhost:5432/main_db"
            mock_redis.return_value = "redis://localhost:6379"
            
            # Setup databases
            env_vars = await framework.db_orchestrator.setup_databases(service)
            
            # Verify database creation was called
            mock_pg.assert_called_once()
            mock_redis.assert_called_once()
            
            # Verify environment variables were generated
            assert "MAIN_DB_URL" in env_vars
            assert "CACHE_DB_URL" in env_vars
    
    @pytest.mark.asyncio
    async def test_parallel_service_start(self, temp_workspace):
        """Test starting multiple independent services in parallel."""
        # Create two independent services
        for i in range(2):
            service_dir = temp_workspace / f"service-{i}"
            service_dir.mkdir()
            (service_dir / "gravity-service.yaml").write_text(f"""
apiVersion: gravity/v1
kind: Service
metadata:
  name: service-{i}
  version: 1.0.0
spec:
  type: api
  runtime: python:3.11
  command: python main.py
""")
        
        framework = GravityFramework(project_path=temp_workspace)
        
        # Discover services
        for service_dir in temp_workspace.iterdir():
            await framework.discover_services(str(service_dir))
        
        # Mock Docker operations
        with patch('docker.from_env') as mock_docker:
            mock_docker_client = Mock()
            mock_docker_client.images = Mock()
            mock_docker_client.containers = Mock()
            mock_docker.return_value = mock_docker_client
            
            # Install all services
            mock_docker_client.images.build.return_value = (Mock(id="image-id"), [])
            
            install_tasks = [
                framework.install(f"service-{i}")
                for i in range(2)
            ]
            results = await asyncio.gather(*install_tasks)
            
            assert all(results)
    
    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self, temp_workspace):
        """Test framework recovery from errors."""
        manifest = """
apiVersion: gravity/v1
kind: Service
metadata:
  name: error-service
  version: 1.0.0
spec:
  type: api
  runtime: python:3.11
  command: python main.py
"""
        
        service_dir = temp_workspace / "error-service"
        service_dir.mkdir()
        (service_dir / "gravity-service.yaml").write_text(manifest)
        
        framework = GravityFramework(project_path=temp_workspace)
        
        # Discover service
        await framework.discover_services(str(service_dir))
        
        # Mock Docker to fail installation
        with patch('docker.from_env') as mock_docker:
            mock_docker_client = Mock()
            mock_docker_client.images = Mock()
            mock_docker_client.images.build.side_effect = Exception("Build failed")
            mock_docker.return_value = mock_docker_client
            
            # Try to install (should fail gracefully)
            result = await framework.install("error-service")
            assert result is False
            
            service = framework.get_service("error-service")
            assert service.status == ServiceStatus.ERROR
            
            # Framework should still be operational
            status = await framework.status()
            assert len(status) == 1
    
    @pytest.mark.asyncio
    async def test_service_update_workflow(self, temp_workspace, sample_manifest_content):
        """Test updating a service to a new version."""
        service_dir = temp_workspace / "update-service"
        service_dir.mkdir()
        manifest_file = service_dir / "gravity-service.yaml"
        manifest_file.write_text(sample_manifest_content)
        
        framework = GravityFramework(project_path=temp_workspace)
        
        # Discover initial version
        services = await framework.discover_services(str(service_dir))
        assert services[0].version == "1.0.0"
        
        # Update manifest to new version
        updated_manifest = sample_manifest_content.replace("version: 1.0.0", "version: 2.0.0")
        manifest_file.write_text(updated_manifest)
        
        # Re-discover
        services = await framework.discover_services(str(service_dir))
        assert services[0].version == "2.0.0"
    
    @pytest.mark.asyncio
    async def test_multi_database_service(self, temp_workspace):
        """Test service requiring multiple database types."""
        manifest = """
apiVersion: gravity/v1
kind: Service
metadata:
  name: multi-db-service
  version: 1.0.0
spec:
  type: api
  runtime: python:3.11
  command: python main.py
  
  databases:
    - name: postgres_db
      type: postgresql
      version: "15"
    
    - name: mongo_db
      type: mongodb
      version: "6"
    
    - name: redis_cache
      type: redis
      version: "7"
"""
        
        service_dir = temp_workspace / "multi-db-service"
        service_dir.mkdir()
        (service_dir / "gravity-service.yaml").write_text(manifest)
        
        framework = GravityFramework(project_path=temp_workspace)
        
        # Discover service
        services = await framework.discover_services(str(service_dir))
        service = services[0]
        
        # Verify all database requirements were parsed
        databases = service.manifest.spec.get("databases", [])
        assert len(databases) == 3
        assert {db["type"] for db in databases} == {"postgresql", "mongodb", "redis"}
    
    @pytest.mark.asyncio
    async def test_health_check_monitoring(self, temp_workspace):
        """Test continuous health check monitoring."""
        manifest = """
apiVersion: gravity/v1
kind: Service
metadata:
  name: health-service
  version: 1.0.0
spec:
  type: api
  runtime: python:3.11
  command: python main.py
  
  health_check:
    endpoint: /health
    interval: 1
    timeout: 5
    retries: 3
"""
        
        service_dir = temp_workspace / "health-service"
        service_dir.mkdir()
        (service_dir / "gravity-service.yaml").write_text(manifest)
        
        framework = GravityFramework(project_path=temp_workspace)
        await framework.discover_services(str(service_dir))
        
        service = framework.get_service("health-service")
        service.status = ServiceStatus.RUNNING
        
        # Mock health checks
        with patch('httpx.AsyncClient') as mock_http:
            # First check: healthy
            mock_response_ok = AsyncMock()
            mock_response_ok.status_code = 200
            
            # Second check: unhealthy
            mock_response_fail = AsyncMock()
            mock_response_fail.status_code = 500
            
            mock_http.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=[mock_response_ok, mock_response_fail]
            )
            
            # Check healthy
            result1 = await framework.health_check("health-service")
            assert result1 is True
            
            # Check unhealthy
            result2 = await framework.health_check("health-service")
            assert result2 is False

