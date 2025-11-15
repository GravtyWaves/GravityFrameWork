"""
Test version 1.0.0 release.

This module verifies that the version 1.0.0 release is correct.
"""

import pytest
from gravity_framework import __version__


def test_version_is_1_0_0():
    """Test that version is 1.0.0."""
    assert __version__ == "1.0.0", f"Expected version 1.0.0, got {__version__}"


def test_version_format():
    """Test that version follows semantic versioning."""
    parts = __version__.split('.')
    assert len(parts) == 3, "Version should have 3 parts (major.minor.patch)"
    assert all(part.isdigit() for part in parts), "All version parts should be numeric"


def test_production_ready():
    """Test that this is a production release."""
    major_version = int(__version__.split('.')[0])
    assert major_version >= 1, "Production release should be version 1.0.0 or higher"


def test_package_metadata():
    """Test that package metadata is correct."""
    from gravity_framework import __author__, __email__, __license__
    
    assert __author__ == "Gravity Framework Team"
    assert __email__ == "team@gravityframework.dev"
    assert __license__ == "MIT"


def test_all_modules_importable():
    """Test that all main modules can be imported."""
    modules = [
        'gravity_framework.core.framework',
        'gravity_framework.core.manager',
        'gravity_framework.discovery.scanner',
        'gravity_framework.resolver.dependency',
        'gravity_framework.database.orchestrator',
        'gravity_framework.database.multi_access',
        'gravity_framework.deployment.composer',
        'gravity_framework.ai.assistant',
        'gravity_framework.ai.autonomous_dev',
        'gravity_framework.ai.team_generator',
        'gravity_framework.git.integration',
        'gravity_framework.git.commit_manager',
        'gravity_framework.devops.automation',
        'gravity_framework.learning.system',
        'gravity_framework.documentation.generator',
        'gravity_framework.project.manager',
        'gravity_framework.standards.enforcer',
        'gravity_framework.testing.generator',
    ]
    
    for module_name in modules:
        try:
            __import__(module_name)
        except ImportError as e:
            pytest.fail(f"Failed to import {module_name}: {e}")


def test_cli_importable():
    """Test that CLI module is importable."""
    try:
        from gravity_framework.cli import main
        assert main is not None
    except ImportError as e:
        pytest.fail(f"Failed to import CLI: {e}")


def test_models_importable():
    """Test that models are importable."""
    try:
        from gravity_framework.models.service import Service, ServiceManifest
        assert Service is not None
        assert ServiceManifest is not None
    except ImportError as e:
        pytest.fail(f"Failed to import models: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
