"""
================================================================================
PROJECT: Gravity Framework
FILE: examples/project_management.py
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
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def example_analyze_project():
    """Example: Analyze project and generate tasks."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: AI Project Analysis")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Project description
    project_description = """
    Build a complete e-commerce platform with the following features:
    
    1. User Management:
       - User registration and authentication
       - Profile management
       - Role-based access control (admin, customer)
    
    2. Product Catalog:
       - Product listing and search
       - Categories and filters
       - Product reviews and ratings
    
    3. Shopping Cart:
       - Add/remove items
       - Cart persistence
       - Price calculations
    
    4. Payment Processing:
       - Multiple payment methods (credit card, PayPal)
       - Secure checkout
       - Payment confirmation
    
    5. Order Management:
       - Order tracking
       - Order history
       - Admin order management
    
    6. Notifications:
       - Email notifications
       - Order status updates
    
    Technology Stack:
    - Backend: Python FastAPI
    - Database: PostgreSQL
    - Frontend: React
    - Payment: Stripe integration
    """
    
    print("\nAnalyzing project with AI (Dr. Marcus Hartmann)...")
    print("This may take a moment...\n")
    
    # Analyze project
    analysis = framework.analyze_project_plan(project_description)
    
    # Print results
    print("📊 PROJECT ANALYSIS COMPLETE")
    print("=" * 80)
    
    print(f"\n📋 Milestones: {len(analysis.get('milestones', []))}")
    
    for i, milestone in enumerate(analysis.get('milestones', []), 1):
        print(f"\n{i}. {milestone['name']}")
        print(f"   Description: {milestone['description']}")
        print(f"   Tasks: {len(milestone.get('tasks', []))}")
        
        # Show first 3 tasks
        for j, task in enumerate(milestone.get('tasks', [])[:3], 1):
            print(f"   {i}.{j} {task['title']}")
            print(f"       Priority: {task['priority']}")
            print(f"       Assignee: {task['assignee']}")
            print(f"       Estimated: {task['estimated_hours']}h")
        
        if len(milestone.get('tasks', [])) > 3:
            print(f"   ... and {len(milestone['tasks']) - 3} more tasks")
    
    # Risks
    if analysis.get('risks'):
        print(f"\n⚠️  RISKS IDENTIFIED:")
        for risk in analysis['risks']:
            print(f"   - {risk}")
    
    # Recommendations
    if analysis.get('recommendations'):
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in analysis['recommendations']:
            print(f"   - {rec}")
    
    return analysis


def example_create_tasks():
    """Example: Create tasks from project description."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Create Project Tasks")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Simple project
    project_description = """
    Create a REST API for a blog platform:
    - User authentication (JWT)
    - Blog post CRUD operations
    - Comments system
    - PostgreSQL database
    - FastAPI backend
    """
    
    print("\nCreating tasks...")
    
    # This will:
    # 1. Analyze project with AI
    # 2. Create all tasks
    # 3. Save to .gravity/tasks.json
    
    tasks = framework.create_project_tasks(project_description)
    
    print(f"\n✅ Created {len(tasks)} tasks!")
    
    # Show tasks
    for task in tasks:
        print(f"\n#{task.id}: {task.title}")
        print(f"   Status: {task.status.value}")
        print(f"   Priority: {task.priority.value}")
        print(f"   Assignee: {task.assignee}")
        if task.estimated_hours:
            print(f"   Estimated: {task.estimated_hours}h")


def example_get_next_tasks():
    """Example: Get next tasks to work on."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Get Next Tasks")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Get next tasks (considers dependencies and priority)
    next_tasks = framework.get_next_tasks()
    
    if not next_tasks:
        print("\n✅ No tasks available (all done or blocked)")
        return
    
    print(f"\n📌 NEXT TASKS TO WORK ON ({len(next_tasks)} tasks):")
    
    for i, task in enumerate(next_tasks[:5], 1):  # Top 5
        print(f"\n{i}. {task.title}")
        print(f"   Priority: {task.priority.value.upper()}")
        print(f"   Assignee: {task.assignee}")
        print(f"   Estimated: {task.estimated_hours}h")
        print(f"   Description: {task.description[:100]}...")


def example_progress_report():
    """Example: Get project progress report."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Project Progress Report")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Get progress
    progress = framework.get_project_progress()
    
    if progress.get('total_tasks', 0) == 0:
        print("\n📊 No tasks created yet")
        return
    
    print(f"\n📊 PROJECT PROGRESS")
    print("=" * 80)
    
    print(f"\nTotal Tasks: {progress['total_tasks']}")
    print(f"Completed: {progress['completed']} ({progress['completion_rate']}%)")
    print(f"In Progress: {progress['in_progress']}")
    print(f"Not Started: {progress['not_started']}")
    print(f"Blocked: {progress['blocked']}")
    
    if progress['total_estimated_hours'] > 0:
        print(f"\nEstimated Hours: {progress['total_estimated_hours']}h")
        print(f"Actual Hours: {progress['total_actual_hours']}h")
        print(f"Efficiency: {progress['efficiency_rate']}%")
    
    # Progress by assignee
    if progress['by_assignee']:
        print("\n👥 PROGRESS BY TEAM MEMBER:")
        for assignee, stats in progress['by_assignee'].items():
            completion = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"\n{assignee}:")
            print(f"   Total: {stats['total']}")
            print(f"   Completed: {stats['completed']} ({completion:.1f}%)")
            print(f"   In Progress: {stats['in_progress']}")
    
    # Blockers
    if progress['blockers']:
        print("\n🚫 BLOCKERS:")
        for blocker in progress['blockers']:
            print(f"   - #{blocker['id']}: {blocker['title']}")
            print(f"     Assignee: {blocker['assignee']}")


def example_generate_todo():
    """Example: Generate TODO list."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Generate TODO List")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Generate Markdown TODO
    print("\nGenerating TODO.md...")
    
    todo_md = framework.generate_todo_list('markdown')
    
    # Save to file
    with open('TODO.md', 'w') as f:
        f.write(todo_md)
    
    print("✅ Saved to TODO.md")
    
    # Show preview
    print("\nPREVIEW:")
    print("=" * 80)
    print(todo_md[:500])
    print("\n... (truncated)")


def example_complete_workflow():
    """Example: Complete project management workflow."""
    print("\n" + "=" * 80)
    print("COMPLETE PROJECT MANAGEMENT WORKFLOW")
    print("=" * 80)
    
    framework = GravityFramework()
    
    # Step 1: Define project
    print("\n1️⃣  Define Project")
    project = """
    Build a task management API:
    - User authentication
    - Task CRUD
    - Task assignments
    - Due dates and reminders
    - PostgreSQL database
    """
    print(f"   Project: {project.strip()[:50]}...")
    
    # Step 2: Analyze and create tasks
    print("\n2️⃣  Analyze Project with AI")
    print("   AI Project Manager (Dr. Marcus Hartmann) analyzing...")
    
    tasks = framework.create_project_tasks(project)
    print(f"   ✅ Created {len(tasks)} tasks")
    
    # Step 3: Get next tasks
    print("\n3️⃣  Get Next Tasks to Work On")
    next_tasks = framework.get_next_tasks()
    print(f"   📌 {len(next_tasks)} tasks ready to start")
    
    if next_tasks:
        print(f"\n   Top priority task:")
        task = next_tasks[0]
        print(f"   - {task.title}")
        print(f"   - Priority: {task.priority.value}")
        print(f"   - Assignee: {task.assignee}")
    
    # Step 4: Check progress
    print("\n4️⃣  Check Progress")
    progress = framework.get_project_progress()
    print(f"   📊 Completion: {progress['completion_rate']}%")
    print(f"   📋 Total: {progress['total_tasks']} tasks")
    
    # Step 5: Generate TODO
    print("\n5️⃣  Generate TODO List")
    todo = framework.generate_todo_list('markdown')
    with open('TODO.md', 'w') as f:
        f.write(todo)
    print("   ✅ Saved to TODO.md")
    
    print("\n✅ WORKFLOW COMPLETE!")
    print("\nNext steps:")
    print("   1. Review TODO.md")
    print("   2. Start working on top priority tasks")
    print("   3. Update task status as you progress")
    print("   4. Check progress regularly")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("GRAVITY FRAMEWORK - AI PROJECT MANAGEMENT")
    print("=" * 80)
    print("\nProject Manager: Dr. Marcus Hartmann")
    print("IQ: 197")
    print("Experience: 23 years")
    print("Specialization: Framework architecture, project planning")
    print("\n" + "=" * 80)
    
    try:
        # Example 1: Analyze project
        analysis = example_analyze_project()
        
        input("\nPress Enter to continue...")
        
        # Example 2: Create tasks
        example_create_tasks()
        
        input("\nPress Enter to continue...")
        
        # Example 3: Get next tasks
        example_get_next_tasks()
        
        input("\nPress Enter to continue...")
        
        # Example 4: Progress report
        example_progress_report()
        
        input("\nPress Enter to continue...")
        
        # Example 5: Generate TODO
        example_generate_todo()
        
        input("\nPress Enter to see complete workflow...")
        
        # Complete workflow
        example_complete_workflow()
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
    print("\nCheck the generated TODO.md file for your project tasks!")
