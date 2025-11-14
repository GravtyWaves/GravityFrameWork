"""
================================================================================
PROJECT: Gravity Framework
FILE: add_file_headers.py
PURPOSE: Add standard file headers to all Python files
DESCRIPTION: Utility script to add comprehensive file headers to all Python
             source files in the project.

AUTHOR: Gravity Framework Team
LICENSE: MIT
CREATED: 2025-11-14
================================================================================
"""

import os
from pathlib import Path
from datetime import datetime


FILE_HEADER_TEMPLATE = '''"""
================================================================================
PROJECT: Gravity Framework
FILE: {relative_path}
PURPOSE: {purpose}
DESCRIPTION: {description}

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: {created_date}
MODIFIED: {modified_date}

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""
'''

# File purposes and descriptions
FILE_INFO = {
    "gravity_framework/core/framework.py": {
        "purpose": "Main GravityFramework class - core orchestration engine",
        "description": "Provides the main GravityFramework class that orchestrates microservice\n             discovery, installation, database setup, and autonomous development."
    },
    "gravity_framework/core/manager.py": {
        "purpose": "Service lifecycle management",
        "description": "Manages service lifecycle including starting, stopping, monitoring,\n             and health checking of microservices."
    },
    "gravity_framework/ai/autonomous_dev.py": {
        "purpose": "Autonomous development system with AI team voting",
        "description": "Implements autonomous full-stack development with a 14-member AI team\n             that uses democratic voting to make all architectural decisions."
    },
    "gravity_framework/ai/assistant.py": {
        "purpose": "AI assistant integration (Ollama, OpenAI, etc.)",
        "description": "Provides AI assistance for microservice orchestration using various\n             AI providers including Ollama (free local AI)."
    },
    "gravity_framework/ai/team_generator.py": {
        "purpose": "Dynamic AI team generation for projects",
        "description": "Generates project-specific AI expert teams based on project requirements\n             and technology stack."
    },
    "gravity_framework/models/service.py": {
        "purpose": "Data models for services and service registry",
        "description": "Defines Service, ServiceManifest, ServiceRegistry and related models\n             for representing and managing microservices."
    },
    "gravity_framework/discovery/scanner.py": {
        "purpose": "Service discovery from Git repositories and local paths",
        "description": "Scans Git repositories and local directories to discover microservices\n             and parse their manifests."
    },
    "gravity_framework/resolver/dependency.py": {
        "purpose": "Dependency resolution with PubGrub algorithm",
        "description": "Resolves service dependencies and version conflicts using the PubGrub\n             algorithm, ensuring compatible service versions."
    },
    "gravity_framework/database/orchestrator.py": {
        "purpose": "Database orchestration and auto-creation",
        "description": "Automatically creates and manages databases for microservices supporting\n             PostgreSQL, MySQL, MongoDB, Redis, and SQLite."
    },
    "gravity_framework/database/multi_access.py": {
        "purpose": "Multi-database access and query federation",
        "description": "Provides unified access to all microservice databases with query\n             federation and aggregation capabilities."
    },
    "gravity_framework/learning/system.py": {
        "purpose": "Continuous learning and knowledge management",
        "description": "Implements continuous learning system that learns from framework usage\n             and provides intelligent recommendations."
    },
    "gravity_framework/git/integration.py": {
        "purpose": "Git and GitHub integration",
        "description": "Handles Git operations and GitHub API integration for repository\n             management and service discovery."
    },
    "gravity_framework/git/commit_manager.py": {
        "purpose": "Smart commit management and auto-commit",
        "description": "Intelligently categorizes changes, generates commit messages, and\n             handles automatic commits when file count exceeds threshold."
    },
    "gravity_framework/devops/automation.py": {
        "purpose": "DevOps automation (Docker, Kubernetes, CI/CD)",
        "description": "Automates DevOps tasks including Docker containerization, Kubernetes\n             deployment, and CI/CD pipeline generation."
    },
    "gravity_framework/standards/enforcer.py": {
        "purpose": "Code standards enforcement",
        "description": "Enforces coding standards, type hints, docstrings, and best practices\n             across the codebase."
    },
    "gravity_framework/project/manager.py": {
        "purpose": "Project management and scaffolding",
        "description": "Manages project initialization, configuration, and provides project\n             management utilities."
    },
    "gravity_framework/cli/main.py": {
        "purpose": "Command-line interface",
        "description": "Provides CLI commands for interacting with the Gravity Framework\n             using Typer and Rich for beautiful terminal output."
    },
}


def get_file_header(file_path: Path, relative_path: str) -> str:
    """Generate file header for a Python file."""
    
    # Get file info or use default
    info = FILE_INFO.get(relative_path.replace("\\", "/"), {
        "purpose": "Framework component",
        "description": f"Component of the Gravity Framework for microservices orchestration"
    })
    
    # Determine creation and modification dates
    created_date = "2025-11-13"  # Project start date
    modified_date = datetime.now().strftime("%Y-%m-%d")
    
    header = FILE_HEADER_TEMPLATE.format(
        relative_path=relative_path.replace("\\", "/"),
        purpose=info["purpose"],
        description=info["description"],
        created_date=created_date,
        modified_date=modified_date
    )
    
    return header


def has_header(content: str) -> bool:
    """Check if file already has a proper header."""
    lines = content.split("\n")
    if len(lines) < 3:
        return False
    
    # Check if it starts with a docstring that looks like a header
    if lines[0].strip().startswith('"""') and "PROJECT:" in content[:500]:
        return True
    
    return False


def add_header_to_file(file_path: Path, root_dir: Path):
    """Add header to a Python file if it doesn't have one."""
    try:
        # Read existing content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has header
        if has_header(content):
            print(f"✓ Skipping {file_path.relative_to(root_dir)} (already has header)")
            return
        
        # Get relative path
        relative_path = str(file_path.relative_to(root_dir))
        
        # Generate header
        header = get_file_header(file_path, relative_path)
        
        # Remove existing module docstring if present
        content_lines = content.split("\n")
        new_content = []
        skip_until_end_quote = False
        i = 0
        
        # Skip initial docstring
        if content_lines and content_lines[0].strip().startswith('"""'):
            i = 1
            while i < len(content_lines):
                if '"""' in content_lines[i]:
                    i += 1
                    break
                i += 1
        
        # Keep the rest
        new_content = content_lines[i:]
        
        # Build final content
        final_content = header + "\n" + "\n".join(new_content)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"✓ Added header to {file_path.relative_to(root_dir)}")
        
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")


def main():
    """Add headers to all Python files in the project."""
    root_dir = Path(__file__).parent
    
    print("=" * 80)
    print("Adding File Headers to Gravity Framework Python Files")
    print("=" * 80)
    print()
    
    # Find all Python files
    python_files = []
    for pattern in ["gravity_framework/**/*.py", "tests/**/*.py", "examples/**/*.py"]:
        python_files.extend(root_dir.glob(pattern))
    
    # Also add root-level Python files
    python_files.extend([
        root_dir / "setup.py",
        root_dir / "cleanup.py"
    ])
    
    # Filter out __pycache__ and similar
    python_files = [f for f in python_files if "__pycache__" not in str(f)]
    
    print(f"Found {len(python_files)} Python files")
    print()
    
    # Process each file
    processed = 0
    for file_path in sorted(python_files):
        if file_path.exists():
            add_header_to_file(file_path, root_dir)
            processed += 1
    
    print()
    print("=" * 80)
    print(f"Processed {processed} files")
    print("=" * 80)


if __name__ == "__main__":
    main()
