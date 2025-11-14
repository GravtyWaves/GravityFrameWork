"""Test configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def tmp_project_path(tmp_path):
    """Create a temporary project directory."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


@pytest.fixture
def sample_service_manifest():
    """Sample service manifest for testing."""
    return {
        "apiVersion": "gravity/v1",
        "kind": "Service",
        "metadata": {
            "name": "test-service",
            "version": "1.0.0",
            "description": "Test service for unit tests"
        },
        "spec": {
            "provides": ["test-feature"],
            "requires": [],
            "database": {
                "type": "postgresql",
                "schema": "test"
            },
            "api": {
                "type": "rest",
                "port": 8001,
                "basePath": "/api/v1/test"
            },
            "healthCheck": {
                "path": "/health",
                "interval": "30s"
            }
        }
    }
