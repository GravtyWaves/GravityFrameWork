"""Targeted tests for framework.py uncovered lines to reach 95% coverage."""

import pytest
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, MagicMock

from gravity_framework.core.framework import GravityFramework
from gravity_framework.models.service import (
    Service,
    ServiceManifest,
    ServiceDependency,
    DatabaseRequirement,
    DatabaseType,
    ServiceStatus
)


class TestFrameworkCoverageMissingLines:
    """Tests targeting specific uncovered lines in framework.py"""
    
    def test_discover_services_from_local_path(self, tmp_path):
        """Test discovering services from local path (lines 91, 94-96)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Create a local service directory
        local_service_path = tmp_path / "local-service"
        local_service_path.mkdir()
        
        # Mock scanner to return a service
        mock_service = Mock(spec=Service)
        mock_service.manifest = Mock(spec=ServiceManifest)
        mock_service.manifest.name = "local-service"
        
        with patch.object(framework.scanner, 'discover_from_path', return_value=mock_service) as mock_discover:
            services = framework.discover_services(str(local_service_path))
            
            mock_discover.assert_called_once()
            assert len(services) == 1
            assert services[0].manifest.name == "local-service"
    
    def test_discover_services_from_invalid_source(self, tmp_path):
        """Test discovering services from source that returns None (line 86)."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.scanner, 'discover_from_git', return_value=None):
            services = framework.discover_services("https://github.com/invalid/repo")
            
            # Should return empty list when service discovery returns None
            assert services == []
    
    def test_discover_services_from_local_path_returns_none(self, tmp_path):
        """Test local path discovery returning None."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.scanner, 'discover_from_path', return_value=None):
            services = framework.discover_services("/some/local/path")
            
            assert services == []
    
    @pytest.mark.asyncio
    async def test_install_no_services(self, tmp_path):
        """Test install with no services (lines 124-126)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Registry is empty by default
        result = await framework.install()
        
        # Should return True even with no services
        assert result is True
    
    @pytest.mark.asyncio
    async def test_install_dependency_resolution_fails(self, tmp_path):
        """Test install when dependency resolution fails (lines 127-129)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add a service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock resolver to return empty list (resolution failed)
        with patch('gravity_framework.core.framework.DependencyResolver') as MockResolver:
            mock_resolver_instance = MockResolver.return_value
            mock_resolver_instance.resolve.return_value = []
            
            result = await framework.install()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_install_database_setup_fails(self, tmp_path):
        """Test install when database setup fails (lines 139-142)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add service with database requirement
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            databases=[DatabaseRequirement(name="testdb", type=DatabaseType.POSTGRESQL)]
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock database orchestrator to fail
        with patch.object(framework.db_orchestrator, 'setup_databases', new_callable=AsyncMock) as mock_setup:
            mock_setup.return_value = False
            
            result = await framework.install()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_install_service_installation_fails(self, tmp_path):
        """Test install when service installation fails (lines 144-146)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock database setup to succeed but service install to fail
        with patch.object(framework.db_orchestrator, 'setup_databases', new_callable=AsyncMock, return_value=True):
            with patch.object(framework.service_manager, 'install_service', new_callable=AsyncMock, return_value=False):
                result = await framework.install()
                
                assert result is False
    
    @pytest.mark.asyncio
    async def test_start_no_services(self, tmp_path):
        """Test start with no services (lines 184-185)."""
        framework = GravityFramework(project_path=tmp_path)
        
        result = await framework.start()
        
        # Should return True even with no services
        assert result is True
    
    @pytest.mark.asyncio
    async def test_start_dependency_resolution_fails(self, tmp_path):
        """Test start when dependency resolution fails (lines 193-195)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.status = ServiceStatus.INSTALLED
        framework.registry.add_service(service)
        
        # Mock resolver to fail
        with patch('gravity_framework.core.framework.DependencyResolver') as MockResolver:
            mock_resolver_instance = MockResolver.return_value
            mock_resolver_instance.resolve.return_value = []
            
            result = await framework.start()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_start_service_fails(self, tmp_path):
        """Test start when a service fails to start (lines 210-212)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add service with database
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            databases=[DatabaseRequirement(name="testdb", type=DatabaseType.POSTGRESQL)]
        )
        service = Service(manifest=manifest)
        service.status = ServiceStatus.INSTALLED
        service.created_databases = {"testdb": {"url": "postgresql://localhost/testdb"}}
        framework.registry.add_service(service)
        
        # Mock connection string
        with patch.object(framework.db_orchestrator, 'get_connection_string', new_callable=AsyncMock, return_value="postgresql://localhost/testdb"):
            # Mock service manager to fail
            with patch.object(framework.service_manager, 'start_service', new_callable=AsyncMock, return_value=False):
                result = await framework.start()
                
                assert result is False
    
    @pytest.mark.asyncio
    async def test_stop_no_running_services(self, tmp_path):
        """Test stop with no running services (lines 240-241)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add a stopped service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.status = ServiceStatus.STOPPED
        framework.registry.add_service(service)
        
        result = await framework.stop()
        
        # Should return True even with no running services
        assert result is True
    
    @pytest.mark.asyncio
    async def test_stop_dependency_resolution_returns_none(self, tmp_path):
        """Test stop when dependency resolution returns None (lines 247-249)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add running service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.status = ServiceStatus.RUNNING
        framework.registry.add_service(service)
        
        # Mock resolver to return None
        with patch('gravity_framework.core.framework.DependencyResolver') as MockResolver:
            mock_resolver_instance = MockResolver.return_value
            mock_resolver_instance.resolve.return_value = None
            
            with patch.object(framework.service_manager, 'stop_service', new_callable=AsyncMock):
                result = await framework.stop()
                
                # Should still succeed and use original services list
                assert result is True
    
    @pytest.mark.asyncio
    async def test_restart_stop_fails(self, tmp_path):
        """Test restart when stop fails (line 273)."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework, 'stop', new_callable=AsyncMock, return_value=False):
            result = await framework.restart()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_logs_service_not_found(self, tmp_path):
        """Test logs for non-existent service (line 322)."""
        framework = GravityFramework(project_path=tmp_path)
        
        result = await framework.logs("non-existent-service")
        
        assert "Service not found" in result
    
    @pytest.mark.asyncio
    async def test_health_check_specific_service_not_found(self, tmp_path):
        """Test health check for non-existent service (line 340)."""
        framework = GravityFramework(project_path=tmp_path)
        
        result = await framework.health_check("non-existent-service")
        
        assert result == {"non-existent-service": False}
    
    @pytest.mark.asyncio
    async def test_health_check_specific_service_exists(self, tmp_path):
        """Test health check for specific existing service (lines 342-343)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        with patch.object(framework.service_manager, 'check_health', new_callable=AsyncMock, return_value=True):
            result = await framework.health_check("test-service")
            
            assert result == {"test-service": True}
    
    @pytest.mark.asyncio
    async def test_health_check_all_services(self, tmp_path):
        """Test health check for all services (lines 345-349)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add multiple services
        for i in range(3):
            manifest = ServiceManifest(
                name=f"service-{i}",
                version="1.0.0",
                repository="https://github.com/test/test"
            )
            service = Service(manifest=manifest)
            framework.registry.add_service(service)
        
        with patch.object(framework.service_manager, 'check_health', new_callable=AsyncMock, return_value=True):
            result = await framework.health_check()
            
            assert len(result) == 3
            assert all(result.values())  # All should be healthy
    
    @pytest.mark.asyncio
    async def test_start_with_database_environment_variables(self, tmp_path):
        """Test start adds database URLs as environment variables (lines 196-205)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add service with database
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            databases=[DatabaseRequirement(name="auth_db", type=DatabaseType.POSTGRESQL)]
        )
        service = Service(manifest=manifest)
        service.status = ServiceStatus.INSTALLED
        service.created_databases = {"auth_db": {"url": "postgresql://localhost/auth_db"}}
        framework.registry.add_service(service)
        
        captured_env_vars = {}
        
        async def capture_env(svc, env_vars):
            captured_env_vars.update(env_vars)
            return True
        
        with patch.object(framework.db_orchestrator, 'get_connection_string', 
                         new_callable=AsyncMock, return_value="postgresql://localhost/auth_db"):
            with patch.object(framework.service_manager, 'start_service', side_effect=capture_env):
                result = await framework.start()
                
                assert result is True
                assert "AUTH_DB_URL" in captured_env_vars
                assert captured_env_vars["AUTH_DB_URL"] == "postgresql://localhost/auth_db"
    
    def test_discover_services_exception_handling(self, tmp_path):
        """Test discover_services handles exceptions (lines 94-96)."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.scanner, 'discover_from_git', side_effect=Exception("Git error")):
            services = framework.discover_services("https://github.com/test/repo")
            
            # Should return empty list on exception
            assert services == []
    
    @pytest.mark.asyncio
    async def test_install_exception_handling(self, tmp_path):
        """Test install handles exceptions (lines 147-150)."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock to raise exception
        with patch('gravity_framework.core.framework.DependencyResolver', side_effect=Exception("Resolution error")):
            result = await framework.install()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_start_exception_handling(self, tmp_path):
        """Test start handles exceptions."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.status = ServiceStatus.INSTALLED
        framework.registry.add_service(service)
        
        # Mock to raise exception
        with patch('gravity_framework.core.framework.DependencyResolver', side_effect=Exception("Start error")):
            result = await framework.start()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_stop_exception_handling(self, tmp_path):
        """Test stop handles exceptions."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add running service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        service.status = ServiceStatus.RUNNING
        framework.registry.add_service(service)
        
        # Mock to raise exception
        with patch.object(framework.service_manager, 'stop_service', new_callable=AsyncMock, side_effect=Exception("Stop error")):
            result = await framework.stop()
            
            assert result is False
