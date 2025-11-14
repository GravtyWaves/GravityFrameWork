"""
================================================================================
PROJECT: Gravity Framework
FILE: examples/auto_ai_install_demo.py
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

def main():
    """Demo automatic AI installation."""
    
    print("=" * 60)
    print("🤖 Gravity Framework - Auto AI Installation Demo")
    print("=" * 60)
    print()
    print("Creating framework with AI enabled...")
    print("(First time: Will auto-install Ollama + AI model)")
    print("(Next time: Instant startup!)")
    print()
    
    # Just create the framework - AI installs automatically!
    framework = GravityFramework(
        ai_assist=True,  # Enable AI
        auto_install_ai=True  # Auto-install if missing (default)
    )
    
    print()
    print("=" * 60)
    
    if framework.ai.enabled:
        print("✅ AI is ready!")
        print(f"   Model: {framework.ai.ollama_model}")
        print()
        print("What the framework did automatically:")
        print("  1. ✅ Detected/Installed Ollama")
        print("  2. ✅ Downloaded AI model (llama3.2:3b)")
        print("  3. ✅ Started AI service")
        print("  4. ✅ Ready to analyze microservices!")
        print()
        print("You can now use:")
        print("  - framework.ai_analyze()")
        print("  - framework.ai_suggest_connections()")
        print("  - framework.ai_diagnose(error)")
        print("  - framework.ai_optimize_deployment()")
    else:
        print("⚠️  AI not available")
        print("   (Auto-install may have failed)")
        print()
        print("Manual install:")
        print("   https://ollama.com/download")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
