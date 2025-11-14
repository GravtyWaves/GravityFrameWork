"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/__init__.py
PURPOSE: Main package initialization and exports
DESCRIPTION: Microservices Orchestration & Autonomous Development Platform
             A Python framework for discovering, installing, connecting, and
             orchestrating microservices, plus autonomous full-stack development
             with AI team voting.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
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
    elif name == "AutonomousDevelopmentSystem":
        from gravity_framework.ai.autonomous_dev import AutonomousDevelopmentSystem
        return AutonomousDevelopmentSystem
    elif name == "DevelopmentTeam":
        from gravity_framework.ai.autonomous_dev import DevelopmentTeam
        return DevelopmentTeam
    elif name == "TeamRole":
        from gravity_framework.ai.autonomous_dev import TeamRole
        return TeamRole
    elif name == "AIProvider":
        from gravity_framework.learning.system import AIProvider
        return AIProvider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "GravityFramework",
    "AutonomousDevelopmentSystem",
    "DevelopmentTeam",
    "TeamRole",
    "AIProvider"
]
