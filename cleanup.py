"""
================================================================================
PROJECT: Gravity Framework
FILE: cleanup.py
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


import shutil
from pathlib import Path
import sys


def cleanup_project():
    """Clean up unnecessary files and directories."""
    
    project_root = Path(__file__).parent
    
    print("🧹 Gravity Framework Cleanup")
    print("=" * 60)
    
    # Directories to remove
    dirs_to_remove = [
        "existing-project",
        "test-project",
        "htmlcov",
    ]
    
    # Files to remove (optional - can be moved to archive)
    files_to_archive = [
        "ROADMAP_V1.md",  # Will be merged into ROADMAP.md
    ]
    
    # Remove directories
    for dir_name in dirs_to_remove:
        dir_path = project_root / dir_name
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✓ Removed directory: {dir_name}/")
            except Exception as e:
                print(f"✗ Failed to remove {dir_name}/: {e}")
        else:
            print(f"  Skip (not found): {dir_name}/")
    
    # Archive old files
    archive_dir = project_root / "archive"
    if files_to_archive:
        archive_dir.mkdir(exist_ok=True)
        print(f"\n📦 Archiving old files to archive/")
        
        for file_name in files_to_archive:
            file_path = project_root / file_name
            if file_path.exists():
                try:
                    shutil.move(str(file_path), str(archive_dir / file_name))
                    print(f"✓ Archived: {file_name}")
                except Exception as e:
                    print(f"✗ Failed to archive {file_name}: {e}")
            else:
                print(f"  Skip (not found): {file_name}")
    
    # Clean Python cache
    print(f"\n🗑️  Cleaning Python cache files...")
    cache_patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.egg-info",
    ]
    
    removed_count = 0
    for pattern in cache_patterns:
        for path in project_root.rglob(pattern.replace("**/", "")):
            if path.is_dir():
                try:
                    shutil.rmtree(path)
                    removed_count += 1
                except Exception:
                    pass
            elif path.is_file():
                try:
                    path.unlink()
                    removed_count += 1
                except Exception:
                    pass
    
    print(f"✓ Removed {removed_count} cache files/directories")
    
    # Check for self-installation
    print(f"\n🔍 Checking for circular dependencies...")
    
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        content = requirements_file.read_text()
        if "gravity-framework" in content.lower():
            print("⚠️  WARNING: Found 'gravity-framework' in requirements.txt")
            print("   This creates circular dependency!")
            print("   For development, use: pip install -e .")
        else:
            print("✓ No circular dependencies found")
    
    # Create necessary directories
    print(f"\n📁 Creating necessary directories...")
    
    dirs_to_create = [
        "docs/guides",
        "docs/api",
        "docs/examples", 
        "examples/sample-services",
        "tests/integration",
        "tests/e2e",
    ]
    
    for dir_name in dirs_to_create:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {dir_name}/")
        else:
            print(f"  Exists: {dir_name}/")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Cleanup completed!")
    print("\n📋 Next steps:")
    print("1. Review changes: git status")
    print("2. Install for development: pip install -e .")
    print("3. Run tests: pytest")
    print("4. Check issues: See ISSUES_AND_ROADMAP.md")
    print("=" * 60)


if __name__ == "__main__":
    try:
        cleanup_project()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cleanup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during cleanup: {e}")
        sys.exit(1)
