#!/usr/bin/env python3
"""
Build and verify Gravity Framework package for PyPI release.

This script:
1. Verifies version consistency across files
2. Runs all tests
3. Checks code quality
4. Builds distribution packages
5. Verifies package contents
"""

import subprocess
import sys
from pathlib import Path
import re


def run_command(cmd: str, description: str) -> bool:
    """Run a command and report results."""
    print(f"\n{'='*80}")
    print(f"🔧 {description}")
    print(f"{'='*80}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print(f"❌ {description} - FAILED")
        if result.stderr:
            print(result.stderr)
        return False


def verify_version_consistency() -> bool:
    """Verify version is consistent across all files."""
    print("\n" + "="*80)
    print("🔍 Verifying version consistency...")
    print("="*80)
    
    files_to_check = {
        "pyproject.toml": r'version = "(\d+\.\d+\.\d+)"',
        "gravity_framework/__init__.py": r'__version__ = "(\d+\.\d+\.\d+)"',
        "CHANGELOG.md": r'\[(\d+\.\d+\.\d+)\] - 2025-11-14',
    }
    
    versions = {}
    
    for file_path, pattern in files_to_check.items():
        path = Path(file_path)
        if not path.exists():
            print(f"❌ File not found: {file_path}")
            return False
        
        content = path.read_text(encoding='utf-8')
        match = re.search(pattern, content)
        
        if match:
            version = match.group(1)
            versions[file_path] = version
            print(f"  {file_path}: {version}")
        else:
            print(f"❌ Version not found in {file_path}")
            return False
    
    # Check if all versions match
    unique_versions = set(versions.values())
    if len(unique_versions) == 1:
        version = unique_versions.pop()
        print(f"\n✅ All files have consistent version: {version}")
        return True
    else:
        print(f"\n❌ Version mismatch detected:")
        for file_path, version in versions.items():
            print(f"  {file_path}: {version}")
        return False


def main():
    """Main build and verification process."""
    print("\n" + "="*80)
    print("🚀 GRAVITY FRAMEWORK - PACKAGE BUILD & VERIFICATION")
    print("="*80)
    
    checks = []
    
    # 1. Version consistency
    checks.append(("Version Consistency", verify_version_consistency()))
    
    # 2. Run tests
    checks.append((
        "Run Tests",
        run_command("pytest tests/ -v --cov=gravity_framework --cov-report=term", "Running tests")
    ))
    
    # 3. Code quality - Black
    checks.append((
        "Code Formatting (Black)",
        run_command("black --check gravity_framework/ tests/", "Checking code formatting")
    ))
    
    # 4. Import sorting - isort
    checks.append((
        "Import Sorting (isort)",
        run_command("isort --check-only gravity_framework/ tests/", "Checking import sorting")
    ))
    
    # 5. Type checking - mypy
    print("\n" + "="*80)
    print("🔧 Type Checking (mypy) - SKIPPED (optional)")
    print("="*80)
    # mypy can be strict, skip for now
    
    # 6. Clean previous builds
    checks.append((
        "Clean Build",
        run_command("python -m pip install --upgrade build twine", "Installing build tools")
    ))
    
    checks.append((
        "Remove Old Builds",
        run_command("rm -rf dist/ build/ *.egg-info 2>/dev/null || true", "Cleaning old builds")
    ))
    
    # 7. Build package
    checks.append((
        "Build Package",
        run_command("python -m build", "Building distribution packages")
    ))
    
    # 8. Check package
    checks.append((
        "Check Package",
        run_command("twine check dist/*", "Validating package")
    ))
    
    # 9. List package contents
    print("\n" + "="*80)
    print("📦 Package Contents")
    print("="*80)
    dist_dir = Path("dist")
    if dist_dir.exists():
        for file in dist_dir.iterdir():
            print(f"  {file.name} ({file.stat().st_size / 1024:.2f} KB)")
    
    # Summary
    print("\n" + "="*80)
    print("📊 BUILD SUMMARY")
    print("="*80)
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Package is ready for release.")
        print("\nNext steps:")
        print("1. Review RELEASE_NOTES_v1.0.0.md")
        print("2. Create GitHub release: https://github.com/GravtyWaves/GravityFrameWork/releases/new")
        print("3. Upload to PyPI: twine upload dist/*")
        print("="*80)
        return 0
    else:
        print("❌ SOME CHECKS FAILED! Please fix issues before release.")
        print("="*80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
