"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_scanner.py
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

    return ServiceScanner(tmp_path / "services")


@pytest.fixture
def sample_manifest():
    """Sample service manifest data."""
    return {
        "name": "test-service",
        "version": "1.0.0",
        "description": "Test service",
        "type": "api",
        "repository": "https://github.com/test/test-service",
        "branch": "main",
        "dependencies": [
            {"name": "user-service", "version": ">=1.0.0"}
        ],
        "databases": [
            {
                "name": "test_db",
                "type": "postgresql",
                "extensions": ["uuid-ossp"]
            }
        ],
        "runtime": "python:3.11",
        "command": "uvicorn main:app --host 0.0.0.0 --port 8000",
        "ports": [
            {"container": 8000, "host": 8001}
        ],
        "health_check": {
            "endpoint": "/health",
            "interval": 30
        }
    }


class TestServiceScanner:
    """Test ServiceScanner class."""
    
    def test_scanner_initialization(self, scanner, tmp_path):
        """Test scanner initializes correctly."""
        assert scanner.services_dir == tmp_path / "services"
        assert scanner.services_dir.exists()
    
    def test_parse_valid_manifest(self, scanner, sample_manifest, tmp_path):
        """Test parsing valid manifest."""
        manifest_path = tmp_path / "gravity-service.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(sample_manifest, f)
        
        manifest = scanner._parse_manifest(
            manifest_path,
            "https://github.com/test/test-service",
            "main"
        )
        
        assert manifest is not None
        assert manifest.name == "test-service"
        assert manifest.version == "1.0.0"
        assert len(manifest.databases) == 1
        assert len(manifest.dependencies) == 1
    
    def test_parse_invalid_yaml(self, scanner, tmp_path):
        """Test parsing invalid YAML."""
        manifest_path = tmp_path / "gravity-service.yaml"
        manifest_path.write_text("invalid: yaml: content: {")
        
        manifest = scanner._parse_manifest(manifest_path, "repo", "main")
        assert manifest is None
    
    def test_parse_empty_manifest(self, scanner, tmp_path):
        """Test parsing empty manifest."""
        manifest_path = tmp_path / "gravity-service.yaml"
        manifest_path.write_text("")
        
        manifest = scanner._parse_manifest(manifest_path, "repo", "main")
        assert manifest is None
    
    @patch('gravity_framework.discovery.scanner.git.Repo')
    def test_discover_from_git(self, mock_repo_class, scanner, sample_manifest, tmp_path):
        """Test discovering service from Git repository."""
        # Setup mock
        mock_repo = MagicMock()
        mock_repo_class.clone_from.return_value = mock_repo
        
        # Create manifest file
        service_path = scanner.services_dir / "test-service"
        service_path.mkdir(parents=True)
        manifest_path = service_path / "gravity-service.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(sample_manifest, f)
        
        # Test discovery
        service = scanner.discover_from_git("https://github.com/test/test-service")
        
        assert service is not None
        assert service.manifest.name == "test-service"
        assert service.status == ServiceStatus.DISCOVERED
    
    @patch('gravity_framework.discovery.scanner.git.Repo')
    def test_discover_from_git_no_manifest(self, mock_repo_class, scanner):
        """Test discovering service without manifest."""
        mock_repo = MagicMock()
        mock_repo_class.clone_from.return_value = mock_repo
        
        service = scanner.discover_from_git("https://github.com/test/no-manifest")
        assert service is None
    
    def test_discover_from_path(self, scanner, sample_manifest, tmp_path):
        """Test discovering service from local path."""
        service_path = tmp_path / "local-service"
        service_path.mkdir()
        manifest_path = service_path / "gravity-service.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(sample_manifest, f)
        
        service = scanner.discover_from_path(service_path)
        
        assert service is not None
        assert service.manifest.name == "test-service"
        assert service.status == ServiceStatus.DISCOVERED
    
    def test_discover_all(self, scanner, sample_manifest):
        """Test discovering all services in directory."""
        # Create multiple services
        for i in range(3):
            service_path = scanner.services_dir / f"service-{i}"
            service_path.mkdir()
            manifest_data = sample_manifest.copy()
            manifest_data["name"] = f"service-{i}"
            manifest_path = service_path / "gravity-service.yaml"
            with open(manifest_path, "w") as f:
                yaml.dump(manifest_data, f)
        
        services = scanner.discover_all()
        
        assert len(services) == 3
        assert all(s.status == ServiceStatus.DISCOVERED for s in services)
    
    def test_discover_all_empty_directory(self, scanner):
        """Test discovering services in empty directory."""
        services = scanner.discover_all()
        assert len(services) == 0
