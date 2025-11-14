"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_framework_extended.py
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
from unittest.mock import Mock, patch, AsyncMock
from gravity_framework.core.framework import GravityFramework
from gravity_framework.models.service import (
    Service,
    ServiceManifest,
    DatabaseRequirement,
    ServiceDependency
)


class TestFrameworkExtended:
    """Extended tests for GravityFramework."""
    
    def test_install_specific_service(self, tmp_path):
        """Test installing a specific service."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock async install
        async def mock_install():
            return True
        
        with patch.object(framework, 'install', side_effect=mock_install):
            # Installation method exists
            assert framework.registry.get_service("test-service") is not None
    
    @pytest.mark.asyncio
    async def test_start_services(self, tmp_path):
        """Test starting services."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock service manager
        with patch.object(framework.service_manager, 'start_service', new_callable=AsyncMock) as mock_start:
            mock_start.return_value = True
            
            result = await framework.start()
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_stop_services(self, tmp_path):
        """Test stopping services."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock service manager
        with patch.object(framework.service_manager, 'stop_service', new_callable=AsyncMock) as mock_stop:
            mock_stop.return_value = True
            
            result = await framework.stop()
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_restart_service(self, tmp_path):
        """Test restarting a service."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock service manager
        with patch.object(framework.service_manager, 'restart_service', new_callable=AsyncMock) as mock_restart:
            mock_restart.return_value = True
            
            result = await framework.restart("test-service")
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_get_logs(self, tmp_path):
        """Test getting service logs."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock service manager
        with patch.object(framework.service_manager, 'get_service_logs', new_callable=AsyncMock) as mock_logs:
            mock_logs.return_value = "Test log output"
            
            logs = await framework.logs("test-service")
            
            assert logs == "Test log output"
    
    @pytest.mark.asyncio
    async def test_health_check(self, tmp_path):
        """Test health check."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test service
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock service manager
        with patch.object(framework.service_manager, 'check_health', new_callable=AsyncMock) as mock_health:
            mock_health.return_value = True
            
            result = await framework.health_check("test-service")
            
            assert result == {"test-service": True}
    
    def test_status_with_services(self, tmp_path):
        """Test status with registered services."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test services
        for i in range(3):
            manifest = ServiceManifest(
                name=f"service-{i}",
                version="1.0.0",
                repository=f"https://github.com/test/service-{i}"
            )
            service = Service(manifest=manifest)
            framework.registry.add_service(service)
        
        status = framework.status()
        
        assert isinstance(status, dict)
        assert len(status.get('services', [])) == 3
    
    def test_discover_from_local_path(self, tmp_path):
        """Test discovering services from local path."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Create service directory with manifest
        service_dir = tmp_path / "services" / "test-service"
        service_dir.mkdir(parents=True)
        
        manifest_content = """
name: test-service
version: 1.0.0
type: api
repository: https://github.com/test/test
        """
        
        (service_dir / "gravity-service.yaml").write_text(manifest_content)
        
        # Mock scanner
        with patch.object(framework.scanner, 'discover_from_path') as mock_discover:
            manifest = ServiceManifest(
                name="test-service",
                version="1.0.0",
                repository="https://github.com/test/test"
            )
            mock_service = Service(manifest=manifest)
            mock_discover.return_value = mock_service
            
            services = framework.discover_services(str(service_dir))
            
            assert len(services) == 1
            assert services[0].manifest.name == "test-service"
    
    @pytest.mark.asyncio
    async def test_install_with_dependencies(self, tmp_path):
        """Test installing services with dependencies."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Create service with dependency
        from gravity_framework.models.service import ServiceDependency
        
        manifest = ServiceManifest(
            name="dependent-service",
            version="1.0.0",
            repository="https://github.com/test/dependent",
            dependencies=[
                ServiceDependency(name="base-service", version=">=1.0.0")
            ]
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock service manager
        with patch.object(framework.service_manager, 'install_service', new_callable=AsyncMock) as mock_install:
            mock_install.return_value = True
            
            result = await framework.install("dependent-service")
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_install_with_databases(self, tmp_path):
        """Test installing service that requires databases."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Create service with database requirements
        manifest = ServiceManifest(
            name="db-service",
            version="1.0.0",
            repository="https://github.com/test/db-service",
            databases=[
                DatabaseRequirement(name="main_db", type="postgresql", version="15"),
                DatabaseRequirement(name="cache", type="redis", version="7")
            ]
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Mock installation
        with patch.object(framework.service_manager, 'install_service', new_callable=AsyncMock) as mock_install:
            mock_install.return_value = True
            
            # Just check that install works - database setup is tested separately
            result = await framework.install("db-service")
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_get_all_services(self, tmp_path):
        """Test get_all_services method."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test services
        for i in range(5):
            manifest = ServiceManifest(
                name=f"service-{i}",
                version="1.0.0",
                repository=f"https://github.com/test/service-{i}"
            )
            service = Service(manifest=manifest)
            framework.registry.add_service(service)
        
        services = await framework.get_all_services()
        
        assert len(services) == 5
        assert all(isinstance(s, Service) for s in services)
    
    def test_get_service_by_name(self, tmp_path):
        """Test getting service by name."""
        framework = GravityFramework(project_path=tmp_path)
        
        # Add test service
        manifest = ServiceManifest(
            name="target-service",
            version="1.0.0",
            repository="https://github.com/test/target"
        )
        service = Service(manifest=manifest)
        framework.registry.add_service(service)
        
        # Get service
        retrieved = framework.get_service("target-service")
        
        assert retrieved is not None
        assert retrieved.manifest.name == "target-service"
        
        # Try non-existent service
        not_found = framework.get_service("non-existent")
        assert not_found is None
