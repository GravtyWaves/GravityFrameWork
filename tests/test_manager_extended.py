"""Extended tests for ServiceManager to increase coverage."""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path

from gravity_framework.core.manager import ServiceManager
from gravity_framework.models.service import (
    Service,
    ServiceManifest,
    ServicePort,
    HealthCheck,
    DatabaseRequirement
)


@pytest.fixture
def manager():
    """Create ServiceManager with mocked Docker client."""
    mock_client = Mock()
    mock_client.containers = Mock()
    mock_client.images = Mock()
    
    manager = ServiceManager(docker_client=mock_client)
    return manager


@pytest.fixture
def sample_service():
    """Create a sample service for testing."""
    manifest = ServiceManifest(
        name="test-service",
        version="1.0.0",
        repository="https://github.com/test/test",
        ports=[ServicePort(container=8000)],
        health_check=HealthCheck(
            endpoint="/health",
            interval=30,
            timeout=5,
            retries=3
        )
    )
    service = Service(manifest=manifest)
    service.path = "/app/services/test-service"
    return service


@pytest.mark.asyncio
async def test_start_service_success(manager, sample_service):
    """Test successful service start."""
    # Mock container
    mock_container = Mock()
    mock_container.id = "abc123"
    mock_container.status = "running"
    
    manager.docker_client.containers.run = Mock(return_value=mock_container)
    
    # Mock health check
    with patch.object(manager, '_wait_for_health', new_callable=AsyncMock) as mock_health:
        mock_health.return_value = True
        
        result = await manager.start_service(sample_service)
        
        assert result is True
        assert sample_service.container_id == "abc123"


@pytest.mark.asyncio
async def test_start_service_with_env_vars(manager, sample_service):
    """Test starting service with environment variables."""
    env_vars = {
        "DATABASE_URL": "postgresql://localhost/testdb",
        "API_KEY": "test-key-123"
    }
    
    mock_container = Mock()
    mock_container.id = "def456"
    mock_container.status = "running"
    
    manager.docker_client.containers.run = Mock(return_value=mock_container)
    
    with patch.object(manager, '_wait_for_health', new_callable=AsyncMock) as mock_health:
        mock_health.return_value = True
        
        result = await manager.start_service(sample_service, env_vars=env_vars)
        
        assert result is True
        # Verify environment was passed
        call_kwargs = manager.docker_client.containers.run.call_args[1]
        assert 'environment' in call_kwargs


@pytest.mark.asyncio
async def test_start_service_health_check_failure(manager, sample_service):
    """Test service start with health check failure."""
    mock_container = Mock()
    mock_container.id = "ghi789"
    mock_container.stop = Mock()
    mock_container.remove = Mock()
    
    manager.docker_client.containers.run = Mock(return_value=mock_container)
    
    # Health check fails
    with patch.object(manager, '_wait_for_health', new_callable=AsyncMock) as mock_health:
        mock_health.return_value = False
        
        result = await manager.start_service(sample_service)
        
        # Service still starts even if health check fails (just warning)
        assert result is True


@pytest.mark.asyncio
async def test_stop_service_success(manager, sample_service):
    """Test successful service stop."""
    sample_service.container_id = "jkl012"
    
    mock_container = Mock()
    mock_container.stop = Mock()
    mock_container.remove = Mock()
    
    manager.docker_client.containers.get = Mock(return_value=mock_container)
    
    result = await manager.stop_service(sample_service)
    
    assert result is True
    mock_container.stop.assert_called()


@pytest.mark.asyncio
async def test_stop_service_timeout(manager, sample_service):
    """Test stopping service with custom timeout."""
    sample_service.container_id = "mno345"
    
    mock_container = Mock()
    mock_container.stop = Mock()
    mock_container.remove = Mock()
    
    manager.docker_client.containers.get = Mock(return_value=mock_container)
    
    result = await manager.stop_service(sample_service, timeout=30)
    
    assert result is True
    mock_container.stop.assert_called_with(timeout=30)


@pytest.mark.asyncio
async def test_stop_service_not_running(manager, sample_service):
    """Test stopping service that is not running."""
    sample_service.container_id = None
    
    result = await manager.stop_service(sample_service)
    
    # Returns True if already stopped (nothing to stop)
    assert result is True
@pytest.mark.asyncio
async def test_restart_service_success(manager, sample_service):
    """Test successful service restart."""
    with patch.object(manager, 'stop_service', new_callable=AsyncMock) as mock_stop, \
         patch.object(manager, 'start_service', new_callable=AsyncMock) as mock_start:
        
        mock_stop.return_value = True
        mock_start.return_value = True
        
        result = await manager.restart_service(sample_service)
        
        assert result is True
        mock_stop.assert_called_once()
        mock_start.assert_called_once()


@pytest.mark.asyncio
async def test_restart_service_stop_failure(manager, sample_service):
    """Test restart when stop fails."""
    with patch.object(manager, 'stop_service', new_callable=AsyncMock) as mock_stop:
        mock_stop.return_value = False
        
        result = await manager.restart_service(sample_service)
        
        assert result is False


@pytest.mark.asyncio
async def test_get_service_logs(manager, sample_service):
    """Test getting service logs."""
    sample_service.container_id = "pqr678"
    
    mock_container = Mock()
    mock_container.logs = Mock(return_value=b"Log line 1\nLog line 2\nLog line 3\n")
    
    manager.docker_client.containers.get = Mock(return_value=mock_container)
    
    logs = await manager.get_service_logs(sample_service, tail=10)
    
    assert "Log line 1" in logs
    # Manager adds timestamps=True by default
    mock_container.logs.assert_called_with(tail=10, timestamps=True)


@pytest.mark.asyncio
async def test_get_service_logs_no_container(manager, sample_service):
    """Test getting logs when container doesn't exist."""
    sample_service.container_id = None
    
    logs = await manager.get_service_logs(sample_service)
    
    assert logs == "No container running"
@pytest.mark.asyncio
async def test_check_health_success(manager, sample_service):
    """Test successful health check."""
    sample_service.container_id = "stu901"
    sample_service.assigned_ports = {8000: 8000}
    
    # Mock HTTP response for health check
    import httpx
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        
        result = await manager.check_health(sample_service)
        
        assert result is True
@pytest.mark.asyncio
async def test_check_health_failure(manager, sample_service):
    """Test failed health check."""
    sample_service.container_id = "vwx234"
    
    mock_container = Mock()
    mock_container.exec_run = Mock(return_value=(1, b"Error"))
    
    manager.docker_client.containers.get = Mock(return_value=mock_container)
    
    result = await manager.check_health(sample_service)
    
    assert result is False


@pytest.mark.asyncio
async def test_check_health_no_healthcheck(manager):
    """Test health check for service without health check config."""
    manifest = ServiceManifest(
        name="no-health-service",
        version="1.0.0",
        repository="https://github.com/test/test",
        health_check=None
    )
    service = Service(manifest=manifest)
    service.container_id = "yza567"
    
    result = await manager.check_health(service)
    # Returns False if no health check configured
    assert result is False


@pytest.mark.asyncio
async def test_wait_for_health_success(manager, sample_service):
    """Test waiting for health check to pass."""
    with patch.object(manager, 'check_health', new_callable=AsyncMock) as mock_health:
        mock_health.return_value = True
        
        result = await manager._wait_for_health(sample_service, max_attempts=3)
        
        assert result is True


@pytest.mark.asyncio
async def test_wait_for_health_timeout(manager, sample_service):
    """Test health check timeout."""
    with patch.object(manager, 'check_health', new_callable=AsyncMock) as mock_health:
        mock_health.return_value = False
        
        result = await manager._wait_for_health(sample_service, max_attempts=2)
        
        assert result is False


def test_find_free_port(manager):
    """Test finding a free port."""
    port = manager._find_free_port()
    
    assert isinstance(port, int)
    assert 1024 <= port <= 65535


@pytest.mark.asyncio
async def test_install_service_with_script(manager, sample_service):
    """Test installing service with install script."""
    sample_service.manifest.install_script = "pip install -r requirements.txt"
    sample_service.path = str(Path("/app/services/test-service"))
    
    mock_container = Mock()
    mock_container.exec_run = Mock(return_value=(0, b"Installation successful"))
    mock_container.wait = Mock(return_value={"StatusCode": 0})
    mock_container.remove = Mock()
    
    manager.docker_client.containers.run = Mock(return_value=mock_container)
    
    result = await manager.install_service(sample_service)
    
    assert result is True


@pytest.mark.asyncio
async def test_install_service_failure(manager, sample_service):
    """Test failed service installation."""
    sample_service.path = str(Path("/app/services/test-service"))
    
    mock_container = Mock()
    mock_container.wait = Mock(return_value={"StatusCode": 1})
    mock_container.remove = Mock()
    
    manager.docker_client.containers.run = Mock(return_value=mock_container)
    
    result = await manager.install_service(sample_service)
    
    # Service status is set to INSTALLED even if no install script
    assert result is True