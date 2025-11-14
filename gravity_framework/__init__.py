"""
Gravity Framework - Microservices Orchestration Platform

A Python framework for discovering, installing, connecting, and orchestrating
independent microservices from separate repositories into cohesive web applications.
"""

__version__ = "0.1.0"
__author__ = "Gravity Framework Team"
__email__ = "team@gravityframework.dev"
__license__ = "MIT"

# Lazy imports to avoid circular dependency
def __getattr__(name):
    if name == "GravityFramework":
        from gravity_framework.core.framework import GravityFramework
        return GravityFramework
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["GravityFramework"]
