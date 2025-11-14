"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/project/manager.py
PURPOSE: Project management and scaffolding
DESCRIPTION: Manages project initialization, configuration, and provides project
             management utilities.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""


from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
import logging
import json

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    """Task status levels."""
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task:
    """Represents a project task."""
    
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        priority: TaskPriority,
        status: TaskStatus = TaskStatus.NOT_STARTED,
        assignee: Optional[str] = None,
        dependencies: Optional[List[int]] = None,
        estimated_hours: Optional[float] = None,
        actual_hours: Optional[float] = None,
        created_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ):
        """Initialize task."""
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.assignee = assignee
        self.dependencies = dependencies or []
        self.estimated_hours = estimated_hours
        self.actual_hours = actual_hours
        self.created_at = created_at or datetime.now()
        self.completed_at = completed_at
        self.tags = tags or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'assignee': self.assignee,
            'dependencies': self.dependencies,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            priority=TaskPriority(data['priority']),
            status=TaskStatus(data['status']),
            assignee=data.get('assignee'),
            dependencies=data.get('dependencies', []),
            estimated_hours=data.get('estimated_hours'),
            actual_hours=data.get('actual_hours'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            tags=data.get('tags', [])
        )


class ProjectManager:
    """
    Intelligent AI-powered project manager.
    
    This class:
    1. Analyzes project requirements and creates comprehensive task lists
    2. Assigns tasks to appropriate team members based on expertise
    3. Tracks progress and identifies blockers
    4. Generates reports and recommendations
    5. Manages dependencies and scheduling
    
    Led by: Dr. Marcus Hartmann (IQ 197, 23 years experience)
    """
    
    def __init__(
        self,
        project_path: Path,
        ai_assistant=None,
        team_members: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize project manager.
        
        Args:
            project_path: Path to project directory
            ai_assistant: AI assistant for intelligent planning
            team_members: List of team member profiles
        """
        self.project_path = Path(project_path)
        self.ai = ai_assistant
        self.team_members = team_members or self._get_default_team()
        self.tasks: Dict[int, Task] = {}
        self.next_task_id = 1
        
        # Load existing tasks if any
        self._load_tasks()
    
    def _get_default_team(self) -> List[Dict[str, Any]]:
        """Get default Gravity Framework team."""
        return [
            {
                'name': 'Dr. Marcus Hartmann',
                'role': 'Framework Architect',
                'expertise': ['architecture', 'core', 'planning'],
                'iq': 197,
                'experience': 23
            },
            {
                'name': 'Dr. Yuki Tanaka',
                'role': 'Service Discovery Engineer',
                'expertise': ['discovery', 'scanning', 'git'],
                'iq': 189,
                'experience': 16
            },
            {
                'name': 'Dr. Priya Sharma',
                'role': 'Database Orchestration Expert',
                'expertise': ['database', 'sql', 'nosql'],
                'iq': 193,
                'experience': 19
            },
            {
                'name': 'Alexander Petrov',
                'role': 'Dependency Resolution Specialist',
                'expertise': ['dependencies', 'algorithms', 'pubgrub'],
                'iq': 191,
                'experience': 17
            },
            {
                'name': 'Dr. Chen Wei',
                'role': 'CLI & Developer Experience Designer',
                'expertise': ['cli', 'ux', 'git', 'workflow'],
                'iq': 191,
                'experience': 18
            },
            {
                'name': 'Sarah Chen',
                'role': 'Container Orchestration Lead',
                'expertise': ['docker', 'containers', 'deployment'],
                'iq': 186,
                'experience': 15
            },
            {
                'name': 'Dr. AI Integration Specialist',
                'role': 'AI Integration Lead',
                'expertise': ['ai', 'ml', 'ollama', 'automation'],
                'iq': 195,
                'experience': 20
            },
            {
                'name': 'DevOps Automation Expert',
                'role': 'DevOps Lead',
                'expertise': ['devops', 'ci-cd', 'infrastructure'],
                'iq': 188,
                'experience': 17
            }
        ]
    
    def analyze_project(self, description: str) -> Dict[str, Any]:
        """
        Analyze project and generate comprehensive task breakdown.
        
        Args:
            description: Project description or requirements
            
        Returns:
            Dictionary with project analysis and task recommendations
        """
        if not self.ai:
            logger.warning("AI not available, using basic analysis")
            return self._basic_project_analysis(description)
        
        logger.info("Analyzing project with AI...")
        
        prompt = f"""
        You are Dr. Marcus Hartmann, Framework Architect with IQ 197 and 23 years experience.
        
        Analyze this project and create a comprehensive task breakdown:
        
        PROJECT DESCRIPTION:
        {description}
        
        TEAM MEMBERS:
        {json.dumps([m['name'] + ' - ' + m['role'] for m in self.team_members], indent=2)}
        
        Create a detailed task breakdown including:
        1. Major milestones
        2. Specific tasks for each milestone
        3. Dependencies between tasks
        4. Estimated hours for each task
        5. Appropriate assignee based on expertise
        6. Priority levels
        7. Risk assessment
        
        Format as JSON:
        {{
            "milestones": [
                {{
                    "name": "Milestone name",
                    "description": "Description",
                    "tasks": [
                        {{
                            "title": "Task title",
                            "description": "Detailed description",
                            "priority": "high/medium/low/critical",
                            "assignee": "Team member name",
                            "estimated_hours": 8,
                            "dependencies": [],
                            "tags": ["tag1", "tag2"]
                        }}
                    ]
                }}
            ],
            "risks": ["Risk 1", "Risk 2"],
            "recommendations": ["Recommendation 1", "Recommendation 2"]
        }}
        
        Be thorough and realistic. Use your 23 years of experience.
        """
        
        response = self.ai.query(prompt)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            analysis = json.loads(json_str)
            
            logger.info(f"Analysis complete: {len(analysis.get('milestones', []))} milestones")
            
            return analysis
            
        except json.JSONDecodeError:
            logger.error("Failed to parse AI response, using basic analysis")
            return self._basic_project_analysis(description)
    
    def _basic_project_analysis(self, description: str) -> Dict[str, Any]:
        """Basic project analysis without AI."""
        return {
            'milestones': [
                {
                    'name': 'Project Setup',
                    'description': 'Initial project setup and configuration',
                    'tasks': [
                        {
                            'title': 'Initialize project structure',
                            'description': description,
                            'priority': 'high',
                            'assignee': 'Dr. Marcus Hartmann',
                            'estimated_hours': 8,
                            'dependencies': [],
                            'tags': ['setup']
                        }
                    ]
                }
            ],
            'risks': ['Project scope unclear'],
            'recommendations': ['Define clear requirements', 'Set up communication channels']
        }
    
    def create_tasks_from_analysis(
        self,
        analysis: Dict[str, Any]
    ) -> List[Task]:
        """
        Create tasks from project analysis.
        
        Args:
            analysis: Project analysis from analyze_project()
            
        Returns:
            List of created tasks
        """
        created_tasks = []
        
        for milestone in analysis.get('milestones', []):
            for task_data in milestone.get('tasks', []):
                task = self.create_task(
                    title=f"[{milestone['name']}] {task_data['title']}",
                    description=task_data['description'],
                    priority=TaskPriority(task_data.get('priority', 'medium')),
                    assignee=task_data.get('assignee'),
                    estimated_hours=task_data.get('estimated_hours'),
                    dependencies=task_data.get('dependencies', []),
                    tags=task_data.get('tags', []) + [milestone['name']]
                )
                created_tasks.append(task)
        
        logger.info(f"Created {len(created_tasks)} tasks from analysis")
        
        return created_tasks
    
    def create_task(
        self,
        title: str,
        description: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        assignee: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        dependencies: Optional[List[int]] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Create a new task."""
        task = Task(
            id=self.next_task_id,
            title=title,
            description=description,
            priority=priority,
            assignee=assignee,
            estimated_hours=estimated_hours,
            dependencies=dependencies,
            tags=tags
        )
        
        self.tasks[task.id] = task
        self.next_task_id += 1
        
        self._save_tasks()
        
        logger.info(f"Created task #{task.id}: {task.title}")
        
        return task
    
    def update_task_status(
        self,
        task_id: int,
        status: TaskStatus,
        actual_hours: Optional[float] = None
    ) -> Task:
        """Update task status."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        task.status = status
        
        if actual_hours is not None:
            task.actual_hours = actual_hours
        
        if status == TaskStatus.COMPLETED:
            task.completed_at = datetime.now()
        
        self._save_tasks()
        
        logger.info(f"Updated task #{task_id} status: {status.value}")
        
        return task
    
    def get_task_list(
        self,
        status: Optional[TaskStatus] = None,
        assignee: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        tags: Optional[List[str]] = None
    ) -> List[Task]:
        """Get filtered task list."""
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        if assignee:
            tasks = [t for t in tasks if t.assignee == assignee]
        
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        
        if tags:
            tasks = [t for t in tasks if any(tag in t.tags for tag in tags)]
        
        return tasks
    
    def get_progress_report(self) -> Dict[str, Any]:
        """Generate comprehensive progress report."""
        total_tasks = len(self.tasks)
        
        if total_tasks == 0:
            return {
                'total_tasks': 0,
                'message': 'No tasks created yet'
            }
        
        completed = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        in_progress = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
        blocked = len([t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED])
        not_started = len([t for t in self.tasks.values() if t.status == TaskStatus.NOT_STARTED])
        
        completion_rate = (completed / total_tasks) * 100
        
        # Calculate estimated vs actual hours
        total_estimated = sum(t.estimated_hours or 0 for t in self.tasks.values())
        total_actual = sum(t.actual_hours or 0 for t in self.tasks.values())
        
        # Group by assignee
        by_assignee = {}
        for task in self.tasks.values():
            if task.assignee:
                if task.assignee not in by_assignee:
                    by_assignee[task.assignee] = {
                        'total': 0,
                        'completed': 0,
                        'in_progress': 0
                    }
                by_assignee[task.assignee]['total'] += 1
                if task.status == TaskStatus.COMPLETED:
                    by_assignee[task.assignee]['completed'] += 1
                elif task.status == TaskStatus.IN_PROGRESS:
                    by_assignee[task.assignee]['in_progress'] += 1
        
        # Find blockers
        blockers = [
            {
                'id': t.id,
                'title': t.title,
                'assignee': t.assignee
            }
            for t in self.tasks.values()
            if t.status == TaskStatus.BLOCKED
        ]
        
        return {
            'total_tasks': total_tasks,
            'completed': completed,
            'in_progress': in_progress,
            'blocked': blocked,
            'not_started': not_started,
            'completion_rate': round(completion_rate, 2),
            'total_estimated_hours': total_estimated,
            'total_actual_hours': total_actual,
            'efficiency_rate': round((total_estimated / total_actual * 100) if total_actual > 0 else 100, 2),
            'by_assignee': by_assignee,
            'blockers': blockers
        }
    
    def get_next_tasks(self, assignee: Optional[str] = None) -> List[Task]:
        """
        Get next tasks to work on.
        
        Considers:
        - Task dependencies (must be completed first)
        - Priority levels
        - Current workload
        
        Args:
            assignee: Filter by assignee
            
        Returns:
            List of tasks ready to start
        """
        # Get tasks that are not started
        available = [
            t for t in self.tasks.values()
            if t.status == TaskStatus.NOT_STARTED
        ]
        
        if assignee:
            available = [t for t in available if t.assignee == assignee]
        
        # Filter by dependencies
        ready = []
        for task in available:
            # Check if all dependencies are completed
            dependencies_met = all(
                self.tasks[dep_id].status == TaskStatus.COMPLETED
                for dep_id in task.dependencies
                if dep_id in self.tasks
            )
            
            if dependencies_met:
                ready.append(task)
        
        # Sort by priority
        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3
        }
        
        ready.sort(key=lambda t: priority_order[t.priority])
        
        return ready
    
    def generate_todo_list(
        self,
        format: str = 'markdown'
    ) -> str:
        """
        Generate formatted TODO list.
        
        Args:
            format: Output format ('markdown', 'json', 'text')
            
        Returns:
            Formatted TODO list
        """
        if format == 'markdown':
            return self._generate_markdown_todo()
        elif format == 'json':
            return json.dumps(
                [t.to_dict() for t in self.tasks.values()],
                indent=2
            )
        else:
            return self._generate_text_todo()
    
    def _generate_markdown_todo(self) -> str:
        """Generate Markdown TODO list."""
        lines = [
            "# Project TODO List",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            ""
        ]
        
        # Progress summary
        report = self.get_progress_report()
        lines.extend([
            "## Progress Summary",
            "",
            f"- Total Tasks: {report['total_tasks']}",
            f"- Completed: {report['completed']} ({report['completion_rate']}%)",
            f"- In Progress: {report['in_progress']}",
            f"- Blocked: {report['blocked']}",
            f"- Not Started: {report['not_started']}",
            ""
        ])
        
        # Tasks by priority
        for priority in [TaskPriority.CRITICAL, TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW]:
            priority_tasks = [t for t in self.tasks.values() if t.priority == priority]
            
            if priority_tasks:
                lines.extend([
                    f"## {priority.value.upper()} Priority",
                    ""
                ])
                
                for task in priority_tasks:
                    status_icon = {
                        TaskStatus.COMPLETED: "✅",
                        TaskStatus.IN_PROGRESS: "🔄",
                        TaskStatus.BLOCKED: "🚫",
                        TaskStatus.NOT_STARTED: "⬜"
                    }[task.status]
                    
                    lines.append(f"### {status_icon} #{task.id}: {task.title}")
                    lines.append("")
                    lines.append(f"**Status:** {task.status.value}")
                    if task.assignee:
                        lines.append(f"**Assignee:** {task.assignee}")
                    if task.estimated_hours:
                        lines.append(f"**Estimated:** {task.estimated_hours}h")
                    if task.actual_hours:
                        lines.append(f"**Actual:** {task.actual_hours}h")
                    if task.dependencies:
                        lines.append(f"**Dependencies:** {', '.join(f'#{d}' for d in task.dependencies)}")
                    if task.tags:
                        lines.append(f"**Tags:** {', '.join(task.tags)}")
                    lines.append("")
                    lines.append(task.description)
                    lines.append("")
        
        return "\n".join(lines)
    
    def _generate_text_todo(self) -> str:
        """Generate plain text TODO list."""
        lines = ["PROJECT TODO LIST", "=" * 80, ""]
        
        for task in self.tasks.values():
            lines.append(f"[{task.status.value.upper()}] #{task.id}: {task.title}")
            if task.assignee:
                lines.append(f"  Assignee: {task.assignee}")
            if task.estimated_hours:
                lines.append(f"  Estimated: {task.estimated_hours}h")
            lines.append("")
        
        return "\n".join(lines)
    
    def _save_tasks(self) -> None:
        """Save tasks to file."""
        tasks_file = self.project_path / '.gravity' / 'tasks.json'
        tasks_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'next_task_id': self.next_task_id,
            'tasks': [t.to_dict() for t in self.tasks.values()]
        }
        
        with open(tasks_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_tasks(self) -> None:
        """Load tasks from file."""
        tasks_file = self.project_path / '.gravity' / 'tasks.json'
        
        if not tasks_file.exists():
            return
        
        try:
            with open(tasks_file, 'r') as f:
                data = json.load(f)
            
            self.next_task_id = data.get('next_task_id', 1)
            
            for task_data in data.get('tasks', []):
                task = Task.from_dict(task_data)
                self.tasks[task.id] = task
            
            logger.info(f"Loaded {len(self.tasks)} tasks from file")
            
        except Exception as e:
            logger.error(f"Failed to load tasks: {e}")
