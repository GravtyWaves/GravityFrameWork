"""
================================================================================
PROJECT: Gravity Framework
FILE: examples/commit_management.py
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


from gravity_framework import GravityFramework
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_analyze_changes():
    """Example: Analyze changed files."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Analyze Changes")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Analyze all changed files
    analysis = framework.analyze_commits()
    
    if analysis.get('error'):
        print(f"Error: {analysis['error']}")
        return
    
    # Print summary
    print(f"\n{analysis['summary']}\n")
    
    # Print recommendations
    print("Recommended commits:")
    for rec in analysis['recommendations']:
        print(f"\n• {rec['suggested_message']}")
        print(f"  Category: {rec['category']}")
        print(f"  Files: {len(rec['files'])}")


def example_organize_commits():
    """Example: Create organized commits."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Create Organized Commits")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Create organized commits (without pushing)
    result = framework.organize_and_commit(
        auto_generate_messages=True,
        push=False
    )
    
    if result.get('error'):
        print(f"Error: {result['error']}")
        return
    
    # Print results
    print(f"\n✅ Created {result['total_commits']} commits")
    
    for commit in result['commits']:
        print(f"\n• {commit['hash'][:8]} - {commit['message']}")
        print(f"  Files: {len(commit['files'])}")


def example_smart_commit_push():
    """Example: Complete smart commit and push."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Smart Commit & Push (Complete Workflow)")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # ONE COMMAND - Complete workflow!
    result = framework.smart_commit_push()
    
    if result.get('error'):
        print(f"Error: {result['error']}")
        return
    
    # Print summary
    print(f"\n{result['summary']}")


def example_auto_commit():
    """Example: Auto-commit when threshold reached."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Auto-Commit (100 Files Threshold)")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Check if auto-commit needed
    result = framework.check_auto_commit()
    
    if result is None:
        print("Threshold not reached yet")
    else:
        print(f"Auto-commit triggered!")
        print(f"\n{result['summary']}")


def example_complete_workflow():
    """Example: Complete development workflow."""
    print("\n" + "=" * 80)
    print("COMPLETE DEVELOPMENT WORKFLOW")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Step 1: Make changes to your code
    print("\n1. Make changes to your code...")
    print("   (You've been coding...)")
    
    # Step 2: Validate standards before committing
    print("\n2. Validate code standards...")
    validation = framework.validate_standards()
    
    if not validation['valid']:
        print(f"   ⚠️  Found {validation['total_violations']} violations")
        
        # Auto-fix issues
        print("\n3. Auto-fixing violations...")
        fix_result = framework.auto_fix_standards()
        print(f"   ✅ Fixed {fix_result['files_fixed']} files")
    else:
        print("   ✅ All standards met!")
    
    # Step 3: Analyze changes
    print("\n4. Analyzing changes...")
    analysis = framework.analyze_commits()
    print(f"{analysis['summary']}")
    
    # Step 4: Smart commit and push
    print("\n5. Creating organized commits and pushing...")
    result = framework.smart_commit_push()
    
    if result['success']:
        print("\n✅ WORKFLOW COMPLETE!")
        print(f"\n{result['summary']}")
    else:
        print("\n❌ Workflow failed")


def example_manual_commit_organization():
    """Example: Manual commit organization with custom messages."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Manual Commit Organization")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Get analysis
    analysis = framework.analyze_commits()
    
    if analysis.get('error'):
        print(f"Error: {analysis['error']}")
        return
    
    print("Recommendations:")
    
    # Show each recommendation
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"\n{i}. {rec['category']}")
        print(f"   Type: {rec['commit_type']}")
        print(f"   Scope: {rec['scope']}")
        print(f"   Files: {len(rec['files'])}")
        print(f"   Message: {rec['suggested_message']}")
        
        for file in rec['files'][:3]:  # Show first 3 files
            print(f"     - {file}")
        
        if len(rec['files']) > 3:
            print(f"     ... and {len(rec['files']) - 3} more")


def example_cli_usage():
    """Example: CLI usage for commit management."""
    print("\n" + "=" * 80)
    print("CLI USAGE EXAMPLES")
    print("=" * 80)
    
    examples = [
        ("Analyze changes", "gravity commit analyze"),
        ("Create organized commits", "gravity commit organize"),
        ("Smart commit and push", "gravity commit push"),
        ("Check auto-commit", "gravity commit check"),
        ("Force commit", "gravity commit force"),
    ]
    
    for description, command in examples:
        print(f"\n• {description}:")
        print(f"  $ {command}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("GRAVITY FRAMEWORK - INTELLIGENT COMMIT MANAGEMENT")
    print("=" * 80)
    print("\nManaged by: Dr. Chen Wei")
    print("Role: CLI & Developer Experience Designer")
    print("Specialization: Git workflow automation")
    print("\n" + "=" * 80)
    
    # Run examples
    try:
        # 1. Analyze changes
        example_analyze_changes()
        
        input("\nPress Enter to continue to next example...")
        
        # 2. Organize commits
        example_organize_commits()
        
        input("\nPress Enter to continue to next example...")
        
        # 3. Smart commit & push
        # example_smart_commit_push()  # Commented - would actually push!
        print("\nExample 3 skipped (would push to remote)")
        
        input("\nPress Enter to continue to next example...")
        
        # 4. Auto-commit
        example_auto_commit()
        
        input("\nPress Enter to continue to next example...")
        
        # 5. Manual organization
        example_manual_commit_organization()
        
        input("\nPress Enter to continue to next example...")
        
        # 6. CLI usage
        example_cli_usage()
        
        input("\nPress Enter to see complete workflow...")
        
        # 7. Complete workflow
        # example_complete_workflow()  # Commented - would commit!
        print("\nComplete workflow skipped (would commit and push)")
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
