"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/git/__init__.py
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


from gravity_framework.git.integration import GitIntegration, GitHubIntegration
from gravity_framework.git.commit_manager import CommitManager, AutoCommitScheduler

__all__ = [
    'GitIntegration', 
    'GitHubIntegration',
    'CommitManager',
    'AutoCommitScheduler'
]
