"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_manager_coverage.py
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
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from gravity_framework.core.manager import ServiceManager
from gravity_framework.models.service import (
    Service,
    ServiceManifest,
    ServicePort,
    ServiceStatus
)


class TestManagerCoverage:
    """Tests to improve manager.py coverage."""
    
    @pytest.mark.asyncio
    async def test_install_service_no_path(self):
        """Test installing service without path set (lines 48-49)."""
        manager = ServiceManager()
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.path = None  # No path set
        
        result = await manager.install_service(service)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_install_service_with_install_script(self, tmp_path):
        """Test installing service with install script (lines 93, 109)."""
        manager = ServiceManager()
        
        # Create service directory and install script
        service_path = tmp_path / "test-service"
        service_path.mkdir()
        install_script = service_path / "install.sh"
        install_script.write_text("#!/bin/bash\necho 'Installing...'")
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            install_script="install.sh"
        )
        service = Service(manifest=manifest)
        service.path = str(service_path)
        
        # Mock subprocess
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            result = await manager.install_service(service)
            
            mock_run.assert_called_once()
            assert result is True
            assert service.status == ServiceStatus.INSTALLED
    
    @pytest.mark.asyncio
    async def test_install_service_script_fails(self, tmp_path):
        """Test install service when install script fails (lines 115-124)."""
        manager = ServiceManager()
        
        service_path = tmp_path / "test-service"
        service_path.mkdir()
        install_script = service_path / "install.sh"
        install_script.write_text("#!/bin/bash\nexit 1")
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            install_script="install.sh"
        )
        service = Service(manifest=manifest)
        service.path = str(service_path)
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=1)
            
            result = await manager.install_service(service)
            
            assert result is False
            assert service.status == ServiceStatus.ERROR
    
    @pytest.mark.asyncio
    async def test_start_service_with_env_vars(self, tmp_path):
        """Test starting service with environment variables (lines 139-140)."""
        manager = ServiceManager(docker_client=MagicMock())
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            runtime="python:3.11",
            command="python app.py",
            ports=[ServicePort(container=8000, host=8000)]
        )
        service = Service(manifest=manifest)
        service.path = str(tmp_path)
        
        env_vars = {
            "DATABASE_URL": "postgresql://localhost/testdb",
            "REDIS_URL": "redis://localhost:6379"
        }
        
        mock_container = MagicMock()
        mock_container.id = "abc123"
        manager.docker_client.containers.run = MagicMock(return_value=mock_container)
        
        result = await manager.start_service(service, env_vars)
        
        assert result is True
        # Check that env_vars were passed
        call_kwargs = manager.docker_client.containers.run.call_args[1]
        assert "environment" in call_kwargs
    
    @pytest.mark.asyncio
    async def test_start_service_no_runtime(self):
        """Test starting service without runtime specified (lines 152-156)."""
        manager = ServiceManager()
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
            # No runtime specified
        )
        service = Service(manifest=manifest)
        
        result = await manager.start_service(service)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_start_service_exception(self, tmp_path):
        """Test start_service handles exceptions (lines 179-193)."""
        manager = ServiceManager(docker_client=MagicMock())
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            runtime="python:3.11",
            command="python app.py"
        )
        service = Service(manifest=manifest)
        service.path = str(tmp_path)
        
        # Mock Docker client to raise exception
        manager.docker_client.containers.run = MagicMock(side_effect=Exception("Docker error"))
        
        result = await manager.start_service(service)
        
        assert result is False
        assert service.status == ServiceStatus.ERROR
        assert "Docker error" in service.error_message
    
    @pytest.mark.asyncio
    async def test_stop_service_not_running(self):
        """Test stopping service that isn't running (lines 229-231)."""
        manager = ServiceManager()
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.container_id = None  # Not running
        
        await manager.stop_service(service)
        
        # Should complete without error
        assert service.container_id is None
    
    @pytest.mark.asyncio
    async def test_stop_service_exception(self):
        """Test stop_service handles exceptions (lines 236-243)."""
        manager = ServiceManager(docker_client=MagicMock())
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.container_id = "abc123"
        
        # Mock container that raises exception
        mock_container = MagicMock()
        mock_container.stop = MagicMock(side_effect=Exception("Stop failed"))
        manager.docker_client.containers.get = MagicMock(return_value=mock_container)
        
        await manager.stop_service(service)
        
        # Should handle exception gracefully
        assert service.status == ServiceStatus.ERROR
    
    @pytest.mark.asyncio
    async def test_restart_service(self):
        """Test restarting a service (lines 271-279)."""
        manager = ServiceManager(docker_client=MagicMock())
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            runtime="python:3.11",
            command="python app.py"
        )
        service = Service(manifest=manifest)
        service.path = "/tmp/test-service"
        service.container_id = "abc123"
        
        # Mock stop and start
        with patch.object(manager, 'stop_service', new_callable=AsyncMock) as mock_stop:
            with patch.object(manager, 'start_service', new_callable=AsyncMock, return_value=True) as mock_start:
                result = await manager.restart_service(service)
                
                mock_stop.assert_called_once_with(service)
                mock_start.assert_called_once_with(service)
                assert result is True
    
    @pytest.mark.asyncio
    async def test_get_service_logs_no_container(self):
        """Test getting logs when service has no container (lines 316-318)."""
        manager = ServiceManager()
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.container_id = None
        
        logs = await manager.get_service_logs(service)
        
        assert "No container running" in logs
    
    @pytest.mark.asyncio
    async def test_get_service_logs_exception(self):
        """Test get_service_logs handles exceptions (lines 341-342)."""
        manager = ServiceManager(docker_client=MagicMock())
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.container_id = "abc123"
        
        # Mock container that raises exception
        mock_container = MagicMock()
        mock_container.logs = MagicMock(side_effect=Exception("Logs error"))
        manager.docker_client.containers.get = MagicMock(return_value=mock_container)
        
        logs = await manager.get_service_logs(service)
        
        assert "Error" in logs
    
    @pytest.mark.asyncio
    async def test_check_health_no_health_check_config(self):
        """Test health check when service has no health check configured (lines 357-358)."""
        manager = ServiceManager()
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
            # No health_check configured
        )
        service = Service(manifest=manifest)
        service.container_id = "abc123"
        service.assigned_ports = {"8000": 8000}
        
        result = await manager.check_health(service)
        
        # When no health_check configured, check_health returns False
        # because it tries to build URL from health_check.endpoint which is None
        assert result is False
    
    @pytest.mark.asyncio
    async def test_check_health_exception(self):
        """Test check_health handles exceptions (line 371)."""
        manager = ServiceManager()
        
        from gravity_framework.models.service import HealthCheck
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            health_check=HealthCheck(endpoint="/health")
        )
        service = Service(manifest=manifest)
        service.assigned_ports = {"8000": 8000}
        
        # Mock httpx to raise exception
        with patch('httpx.AsyncClient') as MockClient:
            mock_client = MockClient.return_value.__aenter__.return_value
            mock_client.get = AsyncMock(side_effect=Exception("Connection refused"))
            
            result = await manager.check_health(service)
            
            assert result is False
