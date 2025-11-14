"""
================================================================================
PROJECT: Gravity Framework
FILE: examples/continuous_learning.py
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
from gravity_framework.learning.system import AIProvider
import asyncio
import json


def example_1_basic_learning():
    """Example 1: Basic learning - system learns from operations."""
    print("\n" + "="*60)
    print("Example 1: Basic Learning")
    print("="*60)
    
    # Initialize with learning enabled (default)
    framework = GravityFramework(enable_learning=True)
    
    print("\n1. Discovering services...")
    services = framework.discover_services()
    print(f"   Found {len(services)} services")
    
    print("\n2. Get learning report...")
    report = framework.get_learning_report()
    
    print(f"\n   📊 Learning Statistics:")
    stats = report['statistics']
    print(f"   - Total events: {stats['total_events']}")
    print(f"   - Successful: {stats['successful_events']}")
    print(f"   - Failed: {stats['failed_events']}")
    print(f"   - Success rate: {stats['success_rate']:.1f}%")
    print(f"   - Solutions learned: {stats['solutions_learned']}")


def example_2_smart_recommendations():
    """Example 2: Get smart recommendations based on learning."""
    print("\n" + "="*60)
    print("Example 2: Smart Recommendations")
    print("="*60)
    
    framework = GravityFramework()
    
    print("\n1. Get recommendations for service discovery...")
    recommendations = framework.get_smart_recommendations(
        'service_discovery',
        {
            'source': 'local',
            'service_count': 5
        }
    )
    
    if recommendations:
        print(f"\n   💡 Smart Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print("   No recommendations yet (system is still learning)")
    
    print("\n2. Get recommendations for deployment...")
    recommendations = framework.get_smart_recommendations(
        'deployment',
        {
            'environment': 'production',
            'services': ['auth', 'api', 'gateway']
        }
    )
    
    if recommendations:
        print(f"\n   💡 Deployment Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")


def example_3_multi_model_ai():
    """Example 3: Use multiple AI models."""
    print("\n" + "="*60)
    print("Example 3: Multi-Model AI")
    print("="*60)
    
    print("\n1. Start with free Ollama (default)...")
    framework = GravityFramework(
        ai_provider=AIProvider.OLLAMA
    )
    print("   ✓ Using Ollama (free, local)")
    
    # Simulate some operations
    services = framework.discover_services()
    print(f"   Found {len(services)} services with Ollama")
    
    print("\n2. Switch to GPT-4 for complex analysis...")
    # Note: Requires OpenAI API key
    # framework.switch_ai_provider(
    #     AIProvider.OPENAI,
    #     api_key='sk-your-openai-key'
    # )
    # print("   ✓ Switched to OpenAI GPT-4")
    print("   (Uncomment to use OpenAI - requires API key)")
    
    print("\n3. Or use Claude for advanced reasoning...")
    # framework.switch_ai_provider(
    #     AIProvider.ANTHROPIC,
    #     api_key='sk-ant-your-anthropic-key'
    # )
    # print("   ✓ Switched to Anthropic Claude")
    print("   (Uncomment to use Claude - requires API key)")
    
    print("\n4. Switch back to free Ollama...")
    framework.switch_ai_provider(AIProvider.OLLAMA)
    print("   ✓ Back to Ollama (free)")


def example_4_learning_from_errors():
    """Example 4: System learns from errors."""
    print("\n" + "="*60)
    print("Example 4: Learning from Errors")
    print("="*60)
    
    framework = GravityFramework()
    
    if not framework.learning:
        print("Learning system not enabled")
        return
    
    print("\n1. Simulate an error...")
    solution = framework.learning.learn_from_error(
        error_type='dependency_conflict',
        error_message='Circular dependency detected between auth and api',
        context={
            'services': ['auth', 'api'],
            'dependencies': ['auth->api', 'api->auth']
        }
    )
    
    if solution:
        print(f"\n   💡 AI Solution:")
        print(f"   {solution}")
    
    print("\n2. Report the same error again...")
    solution = framework.learning.learn_from_error(
        error_type='dependency_conflict',
        error_message='Circular dependency detected',
        context={
            'services': ['gateway', 'auth'],
            'dependencies': ['gateway->auth', 'auth->gateway']
        }
    )
    
    print("\n   📚 System now has experience with this error type")
    print("   Next time it will provide better recommendations")


def example_5_knowledge_growth():
    """Example 5: Track knowledge growth over time."""
    print("\n" + "="*60)
    print("Example 5: Knowledge Growth Tracking")
    print("="*60)
    
    framework = GravityFramework()
    
    print("\n1. Perform multiple operations...")
    
    # Discover services multiple times
    for i in range(3):
        services = framework.discover_services()
        print(f"   Discovery {i+1}: {len(services)} services")
    
    print("\n2. Check knowledge growth...")
    report = framework.get_learning_report()
    
    print(f"\n   📈 Knowledge Growth:")
    growth = report['knowledge_growth']
    print(f"   - Total events: {growth['total_events']}")
    print(f"   - Patterns learned: {growth['patterns_learned']}")
    print(f"   - Solutions discovered: {growth['solutions_discovered']}")
    
    print(f"\n   🏆 Top Operations:")
    for op in report['top_operations'][:5]:
        print(f"   - {op['operation']}: {op['total']} times ({op['success_rate']}% success)")
    
    if report['improvement_areas']:
        print(f"\n   ⚠️  Improvement Areas:")
        for area in report['improvement_areas']:
            print(f"   - {area}")


async def example_6_intelligent_deployment():
    """Example 6: Intelligent deployment with recommendations."""
    print("\n" + "="*60)
    print("Example 6: Intelligent Deployment")
    print("="*60)
    
    framework = GravityFramework()
    
    print("\n1. Get recommendations before deployment...")
    recommendations = framework.get_smart_recommendations(
        'deployment',
        {
            'environment': 'production',
            'services': ['auth', 'api', 'gateway', 'database'],
            'first_deployment': False
        }
    )
    
    if recommendations:
        print(f"\n   💡 Pre-Deployment Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    print("\n2. Deploy with monitoring...")
    # This would normally deploy
    # result = await framework.deploy('production')
    print("   (Deployment would happen here)")
    
    # Record the deployment
    if framework.learning:
        framework.learning.record_deployment(
            environment='production',
            services=['auth', 'api', 'gateway', 'database'],
            success=True,
            duration=120.5  # seconds
        )
    
    print("\n3. Check learning report after deployment...")
    report = framework.get_learning_report()
    print(f"\n   System learned from deployment!")
    print(f"   Total events: {report['statistics']['total_events']}")


def example_7_custom_ai_provider():
    """Example 7: Initialize with custom AI provider."""
    print("\n" + "="*60)
    print("Example 7: Custom AI Provider")
    print("="*60)
    
    print("\n1. Option A: Free Ollama (default)...")
    framework1 = GravityFramework(
        ai_provider=AIProvider.OLLAMA
    )
    print("   ✓ No API key needed, runs locally")
    print("   ✓ Models: llama3.2:3b, codellama, mistral, etc.")
    
    print("\n2. Option B: OpenAI (paid)...")
    # framework2 = GravityFramework(
    #     ai_provider=AIProvider.OPENAI,
    #     ai_api_keys={'openai': 'sk-your-key'}
    # )
    print("   ✓ Best for complex reasoning")
    print("   ✓ Models: GPT-4, GPT-3.5-turbo")
    print("   (Uncomment to use - requires API key)")
    
    print("\n3. Option C: Anthropic Claude (paid)...")
    # framework3 = GravityFramework(
    #     ai_provider=AIProvider.ANTHROPIC,
    #     ai_api_keys={'anthropic': 'sk-ant-your-key'}
    # )
    print("   ✓ Best for detailed analysis")
    print("   ✓ Models: Claude-3 Opus, Sonnet, Haiku")
    print("   (Uncomment to use - requires API key)")
    
    print("\n4. Option D: Cohere (free tier available)...")
    # framework4 = GravityFramework(
    #     ai_provider=AIProvider.COHERE,
    #     ai_api_keys={'cohere': 'your-cohere-key'}
    # )
    print("   ✓ Good for embeddings and search")
    print("   ✓ Has free tier")
    print("   (Uncomment to use - requires API key)")


def example_8_learning_persistence():
    """Example 8: Learning persists between sessions."""
    print("\n" + "="*60)
    print("Example 8: Learning Persistence")
    print("="*60)
    
    print("\n1. First session - learn from operations...")
    framework1 = GravityFramework()
    
    # Do some operations
    services = framework1.discover_services()
    print(f"   Session 1: Discovered {len(services)} services")
    
    report1 = framework1.get_learning_report()
    events1 = report1['statistics']['total_events']
    print(f"   Session 1: {events1} events learned")
    
    print("\n2. Second session - knowledge persists...")
    framework2 = GravityFramework()
    
    report2 = framework2.get_learning_report()
    events2 = report2['statistics']['total_events']
    print(f"   Session 2: {events2} events loaded from disk")
    
    if events2 >= events1:
        print("   ✓ Knowledge persisted between sessions!")
    
    print("\n3. Do more operations...")
    services = framework2.discover_services()
    
    report3 = framework2.get_learning_report()
    events3 = report3['statistics']['total_events']
    print(f"   Session 2: Now {events3} events total")
    print(f"   Growth: +{events3 - events2} new events")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "CONTINUOUS LEARNING EXAMPLES" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    
    examples = [
        ("Basic Learning", example_1_basic_learning),
        ("Smart Recommendations", example_2_smart_recommendations),
        ("Multi-Model AI", example_3_multi_model_ai),
        ("Learning from Errors", example_4_learning_from_errors),
        ("Knowledge Growth", example_5_knowledge_growth),
        ("Intelligent Deployment", example_6_intelligent_deployment),
        ("Custom AI Provider", example_7_custom_ai_provider),
        ("Learning Persistence", example_8_learning_persistence),
    ]
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n\n{'='*60}")
        print(f"Running Example {i}/{len(examples)}: {name}")
        print('='*60)
        
        try:
            if asyncio.iscoroutinefunction(func):
                asyncio.run(func())
            else:
                func()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
