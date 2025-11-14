"""
Interactive Setup Demo - Shows step-by-step guidance system.

This demonstrates how the framework analyzes microservices
and guides users through setup automatically.
"""

from gravity_framework import GravityFramework
from pathlib import Path


def main():
    """Demo interactive setup."""
    
    print("=" * 70)
    print("🎯 Gravity Framework - Interactive Setup Demo")
    print("=" * 70)
    print()
    print("This will:")
    print("  1. Discover your microservices")
    print("  2. Analyze them deeply")
    print("  3. Guide you step-by-step")
    print("  4. Auto-execute most commands")
    print()
    
    # Create framework
    framework = GravityFramework(ai_assist=True)
    
    # Example: Add some services
    print("📍 Discovering microservices...")
    print()
    
    # You can add services from GitHub URLs:
    services = [
        "https://github.com/org/auth-service",
        "https://github.com/org/user-service",
        "https://github.com/org/api-gateway"
    ]
    
    # Or from local paths for testing:
    # framework.discover_services("./services/auth-service")
    # framework.discover_services("./services/user-service")
    
    for repo in services:
        print(f"  → Discovering: {repo}")
        try:
            framework.discover_services(repo)
        except Exception as e:
            print(f"     (Skipped - {e})")
    
    print()
    
    # Now start interactive setup
    print("🚀 Starting interactive setup...")
    print()
    
    summary = framework.interactive_setup()
    
    # Show final results
    print()
    print("=" * 70)
    print("✅ Setup Complete!")
    print("=" * 70)
    print()
    
    if summary.get('error'):
        print(f"⚠️  {summary['error']}")
    else:
        print(f"Total Steps: {summary['total_steps']}")
        print(f"Completed: {summary['completed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print()
        
        if summary['success_rate'] == 100:
            print("🎉 All services are ready!")
            print()
            print("Next steps:")
            print("  • Run: framework.start()")
            print("  • Or use: gravity start")
        else:
            print("⚠️  Some steps failed. Check logs above.")
    
    print()


def demo_with_local_services():
    """Demo using local service directories."""
    
    print("📂 Using local services from ./services/ directory")
    print()
    
    framework = GravityFramework(
        project_path=Path.cwd(),
        ai_assist=True
    )
    
    # Discover all local services
    services = framework.discover_services()
    
    print(f"Found {len(services)} services:")
    for service in services:
        print(f"  • {service.manifest.name} ({service.manifest.type.value})")
    
    print()
    
    # Interactive setup
    summary = framework.interactive_setup()
    
    print(f"\n✅ Setup completed with {summary['success_rate']:.0f}% success rate")


if __name__ == "__main__":
    # Choose which demo to run
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "local":
        demo_with_local_services()
    else:
        main()
