"""
================================================================================
PROJECT: Gravity Framework
FILE: examples/multi_database_access.py
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
import asyncio
import json


async def example_1_register_databases():
    """Example 1: Register all service databases."""
    print("\n" + "="*60)
    print("Example 1: Register Service Databases")
    print("="*60)
    
    framework = GravityFramework()
    
    print("\n1. Discovering services...")
    services = framework.discover_services()
    print(f"   Found {len(services)} services")
    
    print("\n2. Installing services...")
    await framework.install()
    print("   ✓ Services installed")
    
    print("\n3. Registering databases for multi-access...")
    count = await framework.register_service_databases()
    print(f"   ✓ Registered {count} databases")
    
    print("\n4. Getting database statistics...")
    stats = await framework.get_all_database_stats()
    
    print(f"\n   📊 Database Statistics:")
    for service, data in stats.items():
        if 'error' not in data:
            print(f"\n   {service}:")
            print(f"     Tables: {data['table_count']}")
            print(f"     Total rows: {data['total_rows']}")
            
            for table, table_stats in data['tables'].items():
                print(f"       - {table}: {table_stats['row_count']} rows")


async def example_2_query_service_database():
    """Example 2: Query specific service database."""
    print("\n" + "="*60)
    print("Example 2: Query Service Database")
    print("="*60)
    
    framework = GravityFramework()
    await framework.register_service_databases()
    
    print("\n1. Query auth service users...")
    try:
        users = await framework.query_service_database(
            'auth-service',
            'SELECT id, email, username, created_at FROM users LIMIT 10'
        )
        
        print(f"   Found {len(users)} users:")
        for user in users:
            print(f"     - {user.get('email')} ({user.get('username')})")
    
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. Query with parameters...")
    try:
        active_users = await framework.query_service_database(
            'auth-service',
            'SELECT COUNT(*) as count FROM users WHERE active = :active',
            {'active': True}
        )
        
        if active_users:
            print(f"   Active users: {active_users[0]['count']}")
    
    except Exception as e:
        print(f"   Error: {e}")


async def example_3_search_all_databases():
    """Example 3: Search across all databases."""
    print("\n" + "="*60)
    print("Example 3: Search All Databases")
    print("="*60)
    
    framework = GravityFramework()
    await framework.register_service_databases()
    
    search_term = "admin"
    
    print(f"\n1. Searching for '{search_term}' across all databases...")
    results = await framework.search_all_databases(search_term)
    
    print(f"\n   🔍 Search Results:")
    for service, matches in results.items():
        if matches:
            print(f"\n   {service}:")
            for match in matches:
                table = match['table']
                count = match['count']
                print(f"     - {table}: {count} matches")
                
                for row in match['matches'][:3]:  # Show first 3
                    print(f"       {row}")


async def example_4_learn_from_data():
    """Example 4: Learn patterns from all data."""
    print("\n" + "="*60)
    print("Example 4: Learn from All Data")
    print("="*60)
    
    framework = GravityFramework()
    await framework.register_service_databases()
    
    print("\n1. Analyzing data across all services...")
    insights = await framework.learn_from_all_data()
    
    print(f"\n   📚 Learning Insights:")
    
    print("\n   Schemas Discovered:")
    for service, schema in insights['schemas'].items():
        if 'error' not in schema:
            tables = schema.get('tables', {})
            print(f"     {service}: {len(tables)} tables")
            for table_name in list(tables.keys())[:3]:
                print(f"       - {table_name}")
    
    print("\n   Patterns Found:")
    for service, patterns in insights['patterns'].items():
        print(f"     {service}:")
        for table, pattern in patterns.items():
            print(f"       {table}: {pattern}")
    
    print("\n   Relationships Detected:")
    for service, relationships in insights['relationships'].items():
        if relationships:
            print(f"     {service}: {len(relationships)} relationships")
            for rel in relationships[:3]:
                print(f"       {rel['table']}.{rel['column']} -> {rel['likely_references']}")


async def example_5_answer_questions():
    """Example 5: Answer questions with data."""
    print("\n" + "="*60)
    print("Example 5: Answer User Questions")
    print("="*60)
    
    framework = GravityFramework()
    await framework.register_service_databases()
    
    questions = [
        "How many users do we have?",
        "What are the recent orders?",
        "Show me admin users"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        
        answer = await framework.answer_with_data(question)
        
        print(f"\n   Answer:")
        print(f"     Services searched: {answer['total_services']}")
        print(f"     Results found: {len(answer['search_results'])}")
        
        for service, results in answer['search_results'].items():
            if results:
                print(f"\n     {service}:")
                for result in results[:2]:  # Show first 2
                    print(f"       - {result['table']}: {result['count']} matches")


async def example_6_federated_query():
    """Example 6: Federated query across services."""
    print("\n" + "="*60)
    print("Example 6: Federated Query")
    print("="*60)
    
    framework = GravityFramework()
    await framework.register_service_databases()
    
    print("\n1. Query 'users' table across all services...")
    all_users = await framework.federated_query(
        'users',
        where='active = true',
        limit=5
    )
    
    print(f"\n   Found {len(all_users)} users across all services:")
    for user in all_users:
        source = user.pop('_source_service')
        email = user.get('email', 'N/A')
        print(f"     {email} (from {source})")


async def example_7_aggregate_data():
    """Example 7: Aggregate data across services."""
    print("\n" + "="*60)
    print("Example 7: Data Aggregation")
    print("="*60)
    
    framework = GravityFramework()
    await framework.register_service_databases()
    
    print("\n1. Count users across all services...")
    result = await framework.aggregate_data('users', 'COUNT(*)')
    
    print(f"\n   📊 User Count:")
    print(f"     Total: {result['total']}")
    print(f"\n     By Service:")
    for service, count in result['by_service'].items():
        print(f"       {service}: {count}")
    
    print("\n2. Calculate total revenue (if orders table exists)...")
    try:
        result = await framework.aggregate_data('orders', 'SUM(total)')
        
        print(f"\n   💰 Total Revenue:")
        print(f"     Total: ${result['total']:.2f}")
        print(f"\n     By Service:")
        for service, amount in result['by_service'].items():
            if amount:
                print(f"       {service}: ${amount:.2f}")
    
    except Exception as e:
        print(f"   Orders table not found: {e}")


async def example_8_real_time_insights():
    """Example 8: Real-time insights from data."""
    print("\n" + "="*60)
    print("Example 8: Real-Time Insights")
    print("="*60)
    
    framework = GravityFramework()
    await framework.register_service_databases()
    
    print("\n1. Getting comprehensive insights...")
    
    # Get all stats
    stats = await framework.get_all_database_stats()
    
    # Calculate totals
    total_services = len(stats)
    total_tables = sum(
        s.get('table_count', 0) 
        for s in stats.values() 
        if 'error' not in s
    )
    total_rows = sum(
        s.get('total_rows', 0) 
        for s in stats.values() 
        if 'error' not in s
    )
    
    print(f"\n   📈 Platform Insights:")
    print(f"     Services: {total_services}")
    print(f"     Total Tables: {total_tables}")
    print(f"     Total Rows: {total_rows:,}")
    
    # Get learning insights
    insights = await framework.learn_from_all_data()
    
    print(f"\n   🧠 Learning Progress:")
    if framework.learning:
        report = framework.learning.get_learning_report()
        print(f"     Events Learned: {report['statistics']['total_events']}")
        print(f"     Success Rate: {report['statistics']['success_rate']:.1f}%")
        print(f"     Patterns Discovered: {len(insights['patterns'])}")


async def example_9_cross_service_analytics():
    """Example 9: Cross-service analytics."""
    print("\n" + "="*60)
    print("Example 9: Cross-Service Analytics")
    print("="*60)
    
    framework = GravityFramework()
    await framework.register_service_databases()
    
    print("\n1. Analyzing user distribution across services...")
    
    # Query each service
    user_counts = {}
    for service in ['auth-service', 'user-service', 'admin-service']:
        try:
            result = await framework.query_service_database(
                service,
                'SELECT COUNT(*) as count FROM users'
            )
            
            if result:
                user_counts[service] = result[0]['count']
        
        except Exception:
            pass
    
    if user_counts:
        print(f"\n   👥 User Distribution:")
        for service, count in user_counts.items():
            print(f"     {service}: {count} users")
        
        total = sum(user_counts.values())
        print(f"\n     Total: {total} users")
    
    print("\n2. Finding common tables across services...")
    
    insights = await framework.learn_from_all_data()
    
    # Find tables that appear in multiple services
    table_counts = {}
    for service, schema in insights['schemas'].items():
        if 'error' not in schema:
            for table in schema.get('tables', {}).keys():
                table_counts[table] = table_counts.get(table, 0) + 1
    
    common_tables = {
        table: count 
        for table, count in table_counts.items() 
        if count > 1
    }
    
    if common_tables:
        print(f"\n   🔗 Common Tables:")
        for table, count in common_tables.items():
            print(f"     {table}: appears in {count} services")


async def main():
    """Run all examples."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*12 + "MULTI-DATABASE ACCESS EXAMPLES" + " "*16 + "║")
    print("╚" + "="*58 + "╝")
    
    examples = [
        ("Register Databases", example_1_register_databases),
        ("Query Service Database", example_2_query_service_database),
        ("Search All Databases", example_3_search_all_databases),
        ("Learn from Data", example_4_learn_from_data),
        ("Answer Questions", example_5_answer_questions),
        ("Federated Query", example_6_federated_query),
        ("Aggregate Data", example_7_aggregate_data),
        ("Real-Time Insights", example_8_real_time_insights),
        ("Cross-Service Analytics", example_9_cross_service_analytics),
    ]
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n\n{'='*60}")
        print(f"Running Example {i}/{len(examples)}: {name}")
        print('='*60)
        
        try:
            await func()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
