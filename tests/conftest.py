"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/conftest.py
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


@pytest.fixture
def test_project_dir(tmp_path):
    """Create a temporary test project directory."""
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
