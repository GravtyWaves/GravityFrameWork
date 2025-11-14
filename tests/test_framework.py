"""
Tests for the core GravityFramework class.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from gravity_framework.core.framework import GravityFramework
from gravity_framework.models.service import Service, ServiceManifest


class TestGravityFramework:
    """Test suite for GravityFramework class."""
    
    def test_framework_initialization(self, tmp_path):
        """Test that framework initializes correctly."""
        framework = GravityFramework(project_path=tmp_path)
        
        assert framework.project_path == tmp_path
        assert framework.registry is not None
        assert framework.scanner is not None
    
    def test_framework_initialization_default_path(self):
        """Test framework initialization with default path."""
        framework = GravityFramework()
        
        assert framework.project_path == Path.cwd()
    
    def test_discover_services(self, tmp_path):
        """Test service discovery."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.scanner, 'discover_from_git') as mock_discover:
            mock_service = Mock(spec=Service)
            mock_service.manifest = Mock(spec=ServiceManifest)
            mock_service.manifest.name = "test-service"
            mock_discover.return_value = mock_service
            
            services = framework.discover_services("https://github.com/test/repo")
            
            assert isinstance(services, list)
            assert len(services) <= 1
    
    async def test_install_all_services(self, tmp_path):
        """Test installing all services."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.service_manager, 'install_service', new_callable=AsyncMock) as mock_install:
            mock_install.return_value = True
            
            result = await framework.install()
            
            assert result is True
    
    async def test_install_specific_service(self, tmp_path):
        """Test installing a specific service."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.service_manager, 'install_service', new_callable=AsyncMock) as mock_install:
            mock_install.return_value = True
            
            result = await framework.install(service_names=["auth-service"])
            
            assert result is True
    
    async def test_start_services(self, tmp_path):
        """Test starting services."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.service_manager, 'start_service', new_callable=AsyncMock) as mock_start:
            mock_start.return_value = True
            
            result = await framework.start()
            
            assert result is True
    
    async def test_stop_services(self, tmp_path):
        """Test stopping services."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.service_manager, 'stop_service', new_callable=AsyncMock) as mock_stop:
            mock_stop.return_value = True
            
            result = await framework.stop()
            
            assert result is True
    
    async def test_status_check(self, tmp_path):
        """Test status check."""
        framework = GravityFramework(project_path=tmp_path)
        
        with patch.object(framework.service_manager, 'get_status', new_callable=AsyncMock) as mock_status:
            mock_status.return_value = []
            
            status = await framework.status()
            
            assert isinstance(status, list)
    
    def test_register_plugin(self, tmp_path):
        """Test plugin registration."""
        framework = GravityFramework(project_path=tmp_path)
        
        class MockPlugin:
            pass
        
        plugin = MockPlugin()
        framework.register_plugin("test_plugin", plugin)
        
        assert "test_plugin" in framework._plugins
        assert framework._plugins["test_plugin"] == plugin
