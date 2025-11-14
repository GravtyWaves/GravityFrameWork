"""Additional tests for ServiceScanner to improve coverage."""

import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
import git

from gravity_framework.discovery.scanner import ServiceScanner
from gravity_framework.models.service import Service, ServiceStatus


@pytest.fixture
def temp_services_dir(tmp_path):
    """Create a temporary services directory."""
    services_dir = tmp_path / "services"
    return services_dir


@pytest.fixture
def scanner(temp_services_dir):
    """Create a ServiceScanner instance."""
    return ServiceScanner(temp_services_dir)


def test_scanner_creates_services_dir(temp_services_dir):
    """Test that scanner creates services directory if it doesn't exist."""
    assert not temp_services_dir.exists()
    scanner = ServiceScanner(temp_services_dir)
    assert temp_services_dir.exists()
    assert scanner.services_dir == temp_services_dir


def test_discover_from_git_invalid_manifest(scanner, tmp_path):
    """Test discovering service with invalid manifest file."""
    repo_url = "https://github.com/test/invalid-service"
    
    mock_repo = MagicMock()
    service_path = scanner.services_dir / "invalid-service"
    service_path.mkdir(parents=True, exist_ok=True)
    
    # Create invalid YAML
    manifest_path = service_path / "gravity-service.yaml"
    manifest_path.write_text("invalid: yaml: content: ::::")
    
    with patch("gravity_framework.discovery.scanner.git.Repo.clone_from", return_value=mock_repo):
        service = scanner.discover_from_git(repo_url)
        assert service is None


def test_discover_from_git_empty_manifest(scanner, tmp_path):
    """Test discovering service with empty manifest file."""
    repo_url = "https://github.com/test/empty-service"
    
    mock_repo = MagicMock()
    service_path = scanner.services_dir / "empty-service"
    service_path.mkdir(parents=True, exist_ok=True)
    
    # Create empty manifest
    manifest_path = service_path / "gravity-service.yaml"
    manifest_path.write_text("")
    
    with patch("gravity_framework.discovery.scanner.git.Repo.clone_from", return_value=mock_repo):
        service = scanner.discover_from_git(repo_url)
        assert service is None


def test_discover_from_git_validation_error(scanner, tmp_path):
    """Test discovering service with manifest validation error."""
    repo_url = "https://github.com/test/validation-error-service"
    
    mock_repo = MagicMock()
    service_path = scanner.services_dir / "validation-error-service"
    service_path.mkdir(parents=True, exist_ok=True)
    
    # Create manifest missing required fields
    manifest_path = service_path / "gravity-service.yaml"
    manifest_path.write_text("""
name: test
# missing version and repository
""")
    
    with patch("gravity_framework.discovery.scanner.git.Repo.clone_from", return_value=mock_repo):
        service = scanner.discover_from_git(repo_url)
        assert service is None


def test_discover_from_git_alternative_manifest_names(scanner, tmp_path):
    """Test discovering service with alternative manifest file names."""
    repo_url = "https://github.com/test/alt-service"
    
    mock_repo = MagicMock()
    service_path = scanner.services_dir / "alt-service"
    service_path.mkdir(parents=True, exist_ok=True)
    
    # Create manifest with alternative name
    manifest_path = service_path / "gravity-service.yml"
    manifest_data = {
        "name": "alt-service",
        "version": "1.0.0",
        "repository": repo_url,
        "type": "api"
    }
    manifest_path.write_text(yaml.dump(manifest_data))
    
    with patch("gravity_framework.discovery.scanner.git.Repo.clone_from", return_value=mock_repo):
        service = scanner.discover_from_git(repo_url)
        assert service is not None
        assert service.manifest.name == "alt-service"


def test_discover_from_git_git_error(scanner):
    """Test discovering service when Git command fails."""
    repo_url = "https://github.com/test/git-error"
    
    with patch("gravity_framework.discovery.scanner.git.Repo.clone_from", side_effect=git.GitCommandError("clone", "")):
        service = scanner.discover_from_git(repo_url)
        assert service is None


def test_discover_from_git_general_error(scanner):
    """Test discovering service when general error occurs."""
    repo_url = "https://github.com/test/general-error"
    
    with patch("gravity_framework.discovery.scanner.git.Repo.clone_from", side_effect=Exception("Unexpected error")):
        service = scanner.discover_from_git(repo_url)
        assert service is None


def test_discover_from_path_no_manifest(scanner, tmp_path):
    """Test discovering service from path without manifest."""
    service_path = tmp_path / "no-manifest-service"
    service_path.mkdir()
    
    service = scanner.discover_from_path(service_path)
    assert service is None


def test_discover_from_path_invalid_manifest(scanner, tmp_path):
    """Test discovering service from path with invalid manifest."""
    service_path = tmp_path / "invalid-service"
    service_path.mkdir()
    
    manifest_path = service_path / "gravity-service.yaml"
    manifest_path.write_text("name: only-name")  # Missing required fields
    
    service = scanner.discover_from_path(service_path)
    assert service is None


def test_discover_all_with_hidden_dirs(scanner, tmp_path):
    """Test discover_all skips hidden directories."""
    # Create hidden directory
    hidden_dir = scanner.services_dir / ".hidden"
    hidden_dir.mkdir(parents=True)
    manifest_path = hidden_dir / "gravity-service.yaml"
    manifest_data = {
        "name": "hidden-service",
        "version": "1.0.0",
        "repository": "https://github.com/test/hidden"
    }
    manifest_path.write_text(yaml.dump(manifest_data))
    
    # Create normal directory
    normal_dir = scanner.services_dir / "normal"
    normal_dir.mkdir()
    manifest_path = normal_dir / "gravity-service.yaml"
    manifest_data = {
        "name": "normal-service",
        "version": "1.0.0",
        "repository": "https://github.com/test/normal"
    }
    manifest_path.write_text(yaml.dump(manifest_data))
    
    services = scanner.discover_all()
    assert len(services) == 1
    assert services[0].manifest.name == "normal-service"


def test_discover_all_with_files(scanner, tmp_path):
    """Test discover_all skips files in services directory."""
    # Create a file instead of directory
    file_path = scanner.services_dir / "not-a-dir.txt"
    scanner.services_dir.mkdir(parents=True, exist_ok=True)
    file_path.write_text("just a file")
    
    services = scanner.discover_all()
    assert len(services) == 0


def test_discover_from_git_update_existing_repo(scanner, tmp_path):
    """Test discovering service updates existing repository."""
    repo_url = "https://github.com/test/existing-service"
    
    # Create existing service directory
    service_path = scanner.services_dir / "existing-service"
    service_path.mkdir(parents=True)
    
    # Mock git.Repo for existing repository
    mock_repo = MagicMock()
    mock_origin = MagicMock()
    mock_origin.pull = MagicMock()
    mock_repo.remotes.origin = mock_origin
    
    # Create valid manifest
    manifest_path = service_path / "gravity-service.yaml"
    manifest_data = {
        "name": "existing-service",
        "version": "2.0.0",
        "repository": repo_url
    }
    manifest_path.write_text(yaml.dump(manifest_data))
    
    with patch("gravity_framework.discovery.scanner.git.Repo", return_value=mock_repo):
        service = scanner.discover_from_git(repo_url, "develop")
        
        assert service is not None
        assert service.manifest.name == "existing-service"
        assert service.manifest.version == "2.0.0"
        mock_origin.pull.assert_called_once_with("develop")
