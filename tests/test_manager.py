"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_manager.py
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

    client = Mock()
    client.containers = Mock()
    client.images = Mock()
    client.networks = Mock()
    return client


@pytest.fixture
def sample_service():
    """Create sample service for testing."""
    manifest = ServiceManifest(
        name="test-service",
        version="1.0.0",
        repository="https://github.com/test/repo",
        type=ServiceType.API,
        runtime="python:3.11",
        command="python main.py",
        ports=[ServicePort(container=8000, host=8000)],
        health_check=HealthCheck(
            endpoint="/health",
            interval=30,
            timeout=5,
            retries=3
        )
    )
    
    return Service(
        manifest=manifest,
        status=ServiceStatus.DISCOVERED,
        path="/path/to/service"
    )


@pytest.fixture
def service_manager(mock_docker_client):
    """Create ServiceManager instance with mocked Docker client."""
    manager = ServiceManager()
    manager._docker_client = mock_docker_client
    return manager


class TestServiceManager:
    """Test suite for ServiceManager."""
    
    def test_init_creates_docker_client(self):
        """Test that initialization lazily creates Docker client."""
        with patch('docker.from_env') as mock_from_env:
            mock_from_env.return_value = Mock()
            manager = ServiceManager()
            # Access the property to trigger lazy loading
            _ = manager.docker_client
            mock_from_env.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_install_service_success(self, service_manager, sample_service):
        """Test successful service installation."""
        with patch('pathlib.Path.exists', return_value=False):
            result = await service_manager.install_service(sample_service)
        
        assert result is True
        assert sample_service.status == ServiceStatus.INSTALLED
    
    @pytest.mark.asyncio
    async def test_install_service_with_script(self, service_manager, sample_service):
        """Test installation with install script."""
        sample_service.manifest.install_script = "setup.sh"
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('subprocess.run') as mock_run:
            
            mock_run.return_value = Mock(returncode=0, stdout="Success", stderr="")
            result = await service_manager.install_service(sample_service)
            
            assert result is True
            assert sample_service.status == ServiceStatus.INSTALLED
    
    @pytest.mark.asyncio
    async def test_install_service_failure(self, service_manager, sample_service):
        """Test service installation failure."""
        sample_service.manifest.install_script = "setup.sh"
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('subprocess.run') as mock_run:
            
            mock_run.return_value = Mock(returncode=1, stdout="", stderr="Error")
            result = await service_manager.install_service(sample_service)
            
            assert result is False
            assert sample_service.status == ServiceStatus.ERROR
    
    @pytest.mark.asyncio
    async def test_start_service_success(self, service_manager, sample_service):
        """Test successful service start."""
        sample_service.status = ServiceStatus.INSTALLED
        
        mock_container = Mock()
        mock_container.id = "container-id"
        mock_container.status = "running"
        service_manager.docker_client.containers.run.return_value = mock_container
        
        with patch.object(service_manager, '_wait_for_health', return_value=True):
            result = await service_manager.start_service(sample_service)
        
        assert result is True
        assert sample_service.status == ServiceStatus.RUNNING
    
    @pytest.mark.asyncio
    async def test_find_free_port(self, service_manager):
        """Test finding free port."""
        port = service_manager._find_free_port()
        
        assert isinstance(port, int)
        assert 1024 <= port <= 65535
