"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_start_command.py
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
from unittest.mock import Mock, patch
from click.testing import CliRunner
from gravity_framework.cli.main import app
from gravity_framework.models.service import Service, ServiceManifest, ServicePort


@pytest.fixture
def cli_runner():
    """Create CLI runner."""
    return CliRunner()


@pytest.fixture
def sample_service():
    """Create a sample service."""
    manifest = ServiceManifest(
        name="test-service",
        version="1.0.0",
        repository="https://github.com/test/test-service",
        type="api",
        ports=[ServicePort(container=8000)]
    )
    return Service(manifest=manifest)


@pytest.fixture
def mock_framework(sample_service):
    """Mock GravityFramework."""
    with patch('gravity_framework.cli.main.get_framework') as mock:
        framework = Mock()
        
        # Mock get_all_services to return sample service
        async def mock_get_all():
            return [sample_service]
        
        framework.get_all_services = mock_get_all
        mock.return_value = framework
        
        yield mock


@pytest.fixture
def mock_docker_compose():
    """Mock subprocess for docker-compose."""
    with patch('subprocess.run') as mock:
        result = Mock()
        result.returncode = 0
        result.stdout = "Services started"
        result.stderr = ""
        mock.return_value = result
        yield mock


def test_start_command_help(cli_runner):
    """Test start command help."""
    result = cli_runner.invoke(app, ["start", "--help"])
    assert result.exit_code == 0
    assert "Generate docker-compose.yml and start services" in result.stdout


@patch('gravity_framework.cli.main.Path.cwd')
def test_start_generates_compose_file(
    mock_cwd,
    cli_runner,
    mock_framework,
    mock_docker_compose,
    tmp_path
):
    """Test that start command generates docker-compose.yml."""
    # Setup temp directory
    mock_cwd.return_value = tmp_path
    
    # Run command
    result = cli_runner.invoke(app, ["start"])
    
    # Check docker-compose.yml was created
    compose_file = tmp_path / "docker-compose.yml"
    assert compose_file.exists()
    
    # Check content
    content = compose_file.read_text()
    assert "version:" in content
    assert "services:" in content
    assert "test-service:" in content


@patch('gravity_framework.cli.main.Path.cwd')
def test_start_generates_env_example(
    mock_cwd,
    cli_runner,
    mock_framework,
    mock_docker_compose,
    tmp_path
):
    """Test that start command generates .env.example."""
    mock_cwd.return_value = tmp_path
    
    result = cli_runner.invoke(app, ["start"])
    
    # Check .env.example was created
    env_file = tmp_path / ".env.example"
    assert env_file.exists()
    
    # Check content
    content = env_file.read_text()
    assert "POSTGRES" in content or "Gravity Framework" in content


@patch('gravity_framework.cli.main.Path.cwd')
def test_start_calls_docker_compose(
    mock_cwd,
    cli_runner,
    mock_framework,
    mock_docker_compose,
    tmp_path
):
    """Test that start command calls docker-compose up."""
    mock_cwd.return_value = tmp_path
    
    result = cli_runner.invoke(app, ["start"])
    
    # Check docker-compose was called
    mock_docker_compose.assert_called_once()
    
    # Check command arguments
    call_args = mock_docker_compose.call_args
    cmd = call_args[0][0]
    assert "docker-compose" in cmd
    assert "up" in cmd
    assert "-d" in cmd  # detached by default


@patch('gravity_framework.cli.main.Path.cwd')
def test_start_with_build_flag(
    mock_cwd,
    cli_runner,
    mock_framework,
    mock_docker_compose,
    tmp_path
):
    """Test start command with --build flag."""
    mock_cwd.return_value = tmp_path
    
    result = cli_runner.invoke(app, ["start", "--build"])
    
    # Check --build was passed to docker-compose
    call_args = mock_docker_compose.call_args
    cmd = call_args[0][0]
    assert "--build" in cmd


@patch('gravity_framework.cli.main.Path.cwd')
def test_start_no_detach(
    mock_cwd,
    cli_runner,
    mock_framework,
    mock_docker_compose,
    tmp_path
):
    """Test start command without detached mode."""
    mock_cwd.return_value = tmp_path
    
    result = cli_runner.invoke(app, ["start", "--no-detach"])
    
    # Check -d was NOT passed
    call_args = mock_docker_compose.call_args
    cmd = call_args[0][0]
    assert "-d" not in cmd


@patch('gravity_framework.cli.main.Path.cwd')
def test_start_with_no_services(
    mock_cwd,
    cli_runner,
    tmp_path
):
    """Test start command when no services found."""
    mock_cwd.return_value = tmp_path
    
    with patch('gravity_framework.cli.main.get_framework') as mock:
        framework = Mock()
        
        async def mock_get_all():
            return []
        
        framework.get_all_services = mock_get_all
        mock.return_value = framework
        
        result = cli_runner.invoke(app, ["start"])
        
        # Should exit with error
        assert result.exit_code == 1
        assert "No services found" in result.stdout


@patch('gravity_framework.cli.main.Path.cwd')
def test_start_docker_compose_failure(
    mock_cwd,
    cli_runner,
    mock_framework,
    tmp_path
):
    """Test start command when docker-compose fails."""
    mock_cwd.return_value = tmp_path
    
    with patch('subprocess.run') as mock_run:
        result = Mock()
        result.returncode = 1
        result.stderr = "Error: containers failed to start"
        mock_run.return_value = result
        
        result = cli_runner.invoke(app, ["start"])
        
        # Should exit with error
        assert result.exit_code == 1
        assert "Failed to start services" in result.stdout


@patch('gravity_framework.cli.main.Path.cwd')
def test_start_docker_not_installed(
    mock_cwd,
    cli_runner,
    mock_framework,
    tmp_path
):
    """Test start command when docker-compose not installed."""
    mock_cwd.return_value = tmp_path
    
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = FileNotFoundError()
        
        result = cli_runner.invoke(app, ["start"])
        
        # Should exit with error
        assert result.exit_code == 1
        assert "docker-compose not found" in result.stdout
