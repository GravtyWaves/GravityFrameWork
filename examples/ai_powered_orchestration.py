"""
================================================================================
PROJECT: Gravity Framework
FILE: examples/ai_powered_orchestration.py
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


import asyncio
from gravity_framework import GravityFramework


async def main():
    """Demonstrate AI-powered microservice orchestration."""
    
    print("🌟 Gravity Framework - AI-Powered Orchestration Demo\n")
    
    # Initialize framework with AI assistance (FREE via GitHub Copilot)
    framework = GravityFramework(ai_assist=True)
    
    print("📡 Discovering microservices from GitHub...")
    
    # Discover services from GitHub URLs
    # Note: These are example URLs - replace with your actual microservices
    services = []
    
    # Example: Discover auth service
    auth_service = framework.discover_services("https://github.com/your-org/auth-service")
    if auth_service:
        services.extend(auth_service)
    
    # Example: Discover user service  
    user_service = framework.discover_services("https://github.com/your-org/user-service")
    if user_service:
        services.extend(user_service)
    
    # Example: Discover payment service
    payment_service = framework.discover_services("https://github.com/your-org/payment-service")
    if payment_service:
        services.extend(payment_service)
    
    print(f"✓ Discovered {len(services)} microservices\n")
    
    # AI Analysis - Get intelligent recommendations
    print("🤖 Running AI analysis...")
    analysis = framework.ai_analyze()
    
    print(f"\n📊 AI Analysis Results:")
    print(f"  Total Services: {analysis.get('total_services', 0)}")
    
    if analysis.get('recommendations'):
        print(f"\n💡 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"  • {rec.get('message', 'N/A')}")
    
    if analysis.get('warnings'):
        print(f"\n⚠️  Warnings:")
        for warning in analysis['warnings']:
            print(f"  • {warning.get('message', 'N/A')}")
    
    if analysis.get('optimizations'):
        print(f"\n⚡ Optimizations:")
        for opt in analysis['optimizations']:
            print(f"  • {opt.get('message', 'N/A')}")
    
    # AI Connection Suggestions - Puzzle-solving
    print("\n\n🧩 AI Connection Suggestions (Puzzle-Solving):")
    connections = framework.ai_suggest_connections()
    
    for conn in connections:
        print(f"\n  {conn['from']} → {conn['to']}")
        print(f"    Type: {conn['type']}")
        print(f"    Method: {conn['method']}")
        print(f"    Endpoint: {conn.get('endpoint', 'N/A')}")
        print(f"    Priority: {conn.get('priority', 'medium')}")
    
    # Install services with AI-created databases
    print("\n\n📦 Installing services (AI will auto-create databases)...")
    
    # The framework automatically:
    # 1. Creates databases declared in each service's manifest
    # 2. Configures connections
    # 3. Injects environment variables
    # 4. Uses AI to analyze schema relationships
    
    success = await framework.install()
    
    if success:
        print("✓ All services installed successfully")
        print("✓ Databases auto-created and connected")
    else:
        print("✗ Installation failed")
        
        # AI-powered diagnosis
        diagnosis = framework.ai_diagnose(
            "Installation failed",
            {"phase": "install", "services": len(services)}
        )
        
        print("\n🔍 AI Diagnosis:")
        print(f"  Likely Cause: {diagnosis.get('likely_cause', 'Unknown')}")
        print("\n  Suggested Solutions:")
        for solution in diagnosis.get('solutions', []):
            print(f"    • {solution}")
        
        return
    
    # Start services
    print("\n🚀 Starting microservices...")
    started = await framework.start()
    
    if started:
        print("✓ All services started successfully\n")
        
        # Get deployment optimization suggestions
        print("⚙️  AI Deployment Optimization Suggestions:")
        optimizations = framework.ai_optimize_deployment()
        
        if optimizations.get('resource_allocation'):
            print("\n  Resource Allocation:")
            for alloc in optimizations['resource_allocation']:
                print(f"    • {alloc['service']}: {alloc['recommendation']}")
        
        if optimizations.get('scaling'):
            print("\n  Scaling Recommendations:")
            for scale in optimizations['scaling']:
                print(f"    • Type: {scale['type']}")
                print(f"      Services: {', '.join(scale.get('services', []))}")
                print(f"      Recommendation: {scale['recommendation']}")
        
        if optimizations.get('performance'):
            print("\n  Performance Improvements:")
            for perf in optimizations['performance']:
                print(f"    • {perf['recommendation']}")
                print(f"      Benefit: {perf.get('benefit', 'N/A')}")
                if 'impact' in perf:
                    print(f"      Expected Impact: {perf['impact']}")
    
    # Show service status
    print("\n\n📊 Service Status:")
    status = framework.status()
    
    print(f"  Total Services: {status['total_services']}")
    print(f"  Running: {status['running']}")
    print(f"  Stopped: {status['stopped']}")
    print(f"  Errors: {status['error']}")
    
    print("\n\n🎉 AI-Powered Orchestration Complete!")
    print("\nKey AI Features Used:")
    print("  ✓ Intelligent service connection suggestions")
    print("  ✓ Database schema analysis and auto-creation")
    print("  ✓ Architecture optimization recommendations")
    print("  ✓ Error diagnosis and troubleshooting")
    print("  ✓ Deployment optimization")
    print("\n💡 All AI features are FREE via GitHub Copilot integration!")


async def example_database_auto_creation():
    """
    Example: Microservices WITHOUT databases can get them auto-created.
    
    Gravity Framework automatically creates databases for microservices
    that don't have them, based on their manifest declarations.
    """
    
    print("\n" + "="*60)
    print("🗄️  Example: Auto-Creating Databases for Microservices")
    print("="*60 + "\n")
    
    framework = GravityFramework(ai_assist=True)
    
    print("Scenario: You have 3 microservices:")
    print("  1. auth-service (needs PostgreSQL)")
    print("  2. user-service (needs PostgreSQL + Redis)")
    print("  3. payment-service (needs MySQL + Redis)")
    print("\nNone of these services come with databases installed.")
    print("\nGravity Framework will:")
    print("  ✓ Detect database requirements from gravity-service.yaml")
    print("  ✓ Auto-create PostgreSQL, MySQL, and Redis instances")
    print("  ✓ Configure connections and credentials")
    print("  ✓ Inject DATABASE_URL environment variables")
    print("  ✓ Use AI to analyze schema relationships")
    print("\nAll automatically! 🚀")
    
    # The manifest would look like this:
    example_manifest = """
# auth-service/gravity-service.yaml
name: auth-service
version: 1.0.0
type: api

databases:
  - name: auth_db
    type: postgresql
    extensions: [uuid-ossp, pgcrypto]

# Framework auto-creates PostgreSQL with extensions
# Injects: AUTH_DB_URL=postgresql://user:pass@host:5432/auth_db
"""
    
    print("\n📄 Example Service Manifest:")
    print(example_manifest)


async def example_ai_troubleshooting():
    """Example: AI-powered troubleshooting."""
    
    print("\n" + "="*60)
    print("🔧 Example: AI-Powered Troubleshooting")
    print("="*60 + "\n")
    
    framework = GravityFramework(ai_assist=True)
    
    # Simulate an error
    error = "Connection refused: localhost:8000"
    
    print(f"❌ Error occurred: {error}\n")
    print("🤖 Asking AI assistant for help...\n")
    
    diagnosis = framework.ai_diagnose(error, {
        "service": "auth-service",
        "phase": "startup"
    })
    
    print("🔍 AI Diagnosis:")
    print(f"  Likely Cause: {diagnosis['likely_cause']}\n")
    print("  Suggested Solutions:")
    for i, solution in enumerate(diagnosis['solutions'], 1):
        print(f"    {i}. {solution}")
    
    print("\n💡 AI provides context-aware solutions instantly!")


if __name__ == "__main__":
    print("Choose an example to run:")
    print("1. Full AI-Powered Orchestration Demo")
    print("2. Database Auto-Creation Example")
    print("3. AI Troubleshooting Example")
    print("4. Run All Examples")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        asyncio.run(main())
    elif choice == "2":
        asyncio.run(example_database_auto_creation())
    elif choice == "3":
        asyncio.run(example_ai_troubleshooting())
    elif choice == "4":
        asyncio.run(main())
        asyncio.run(example_database_auto_creation())
        asyncio.run(example_ai_troubleshooting())
    else:
        print("Invalid choice. Running full demo...")
        asyncio.run(main())
