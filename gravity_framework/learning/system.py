"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/learning/system.py
PURPOSE: Continuous learning and knowledge management
DESCRIPTION: Implements continuous learning system that learns from framework usage
             and provides intelligent recommendations.

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
from datetime import datetime
import json
import logging
import importlib
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)


class AIProvider(Enum):
    """Supported AI providers - ONLY Ollama (free, local)."""
    OLLAMA = "ollama"  # Free, local - ONLY option


class LearningEvent:
    """Represents a learning event."""
    
    def __init__(
        self,
        event_type: str,
        context: Dict[str, Any],
        outcome: str,
        success: bool,
        timestamp: Optional[datetime] = None
    ):
        """Initialize learning event."""
        self.event_type = event_type
        self.context = context
        self.outcome = outcome
        self.success = success
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'event_type': self.event_type,
            'context': self.context,
            'outcome': self.outcome,
            'success': self.success,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningEvent':
        """Create from dictionary."""
        return cls(
            event_type=data['event_type'],
            context=data['context'],
            outcome=data['outcome'],
            success=data['success'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )


class KnowledgeBase:
    """
    Persistent knowledge base that grows with usage.
    
    Stores:
    - User patterns
    - Common issues and solutions
    - Best practices learned
    - Service configurations that worked
    - Error patterns and fixes
    """
    
    def __init__(self, storage_path: Path):
        """Initialize knowledge base."""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.events: List[LearningEvent] = []
        self.patterns: Dict[str, Any] = {}
        self.solutions: Dict[str, List[str]] = {}
        self.recommendations: Dict[str, Any] = {}
        
        self._load()
    
    def record_event(self, event: LearningEvent) -> None:
        """Record a learning event."""
        self.events.append(event)
        
        # Update patterns
        self._update_patterns(event)
        
        # Save periodically
        if len(self.events) % 10 == 0:
            self._save()
    
    def _update_patterns(self, event: LearningEvent) -> None:
        """Update patterns based on event."""
        event_type = event.event_type
        
        if event_type not in self.patterns:
            self.patterns[event_type] = {
                'total': 0,
                'successful': 0,
                'failed': 0,
                'common_contexts': {}
            }
        
        pattern = self.patterns[event_type]
        pattern['total'] += 1
        
        if event.success:
            pattern['successful'] += 1
            
            # Record successful solution
            if event_type not in self.solutions:
                self.solutions[event_type] = []
            
            solution = json.dumps(event.context, sort_keys=True)
            if solution not in self.solutions[event_type]:
                self.solutions[event_type].append(solution)
        else:
            pattern['failed'] += 1
        
        # Track common contexts
        context_key = self._hash_context(event.context)
        if context_key not in pattern['common_contexts']:
            pattern['common_contexts'][context_key] = {
                'count': 0,
                'context': event.context
            }
        pattern['common_contexts'][context_key]['count'] += 1
    
    def _hash_context(self, context: Dict[str, Any]) -> str:
        """Create hash of context for tracking."""
        context_str = json.dumps(context, sort_keys=True)
        return hashlib.md5(context_str.encode()).hexdigest()
    
    def get_recommendations(self, event_type: str, context: Dict[str, Any]) -> List[str]:
        """
        Get recommendations based on learned patterns.
        
        Args:
            event_type: Type of event
            context: Current context
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check if we have patterns for this event type
        if event_type in self.patterns:
            pattern = self.patterns[event_type]
            
            # Success rate
            success_rate = pattern['successful'] / pattern['total'] if pattern['total'] > 0 else 0
            
            if success_rate < 0.5:
                recommendations.append(
                    f"⚠️  This operation has a {success_rate*100:.1f}% success rate. Proceed with caution."
                )
            
            # Find similar successful contexts
            if event_type in self.solutions:
                recommendations.append(
                    f"💡 Found {len(self.solutions[event_type])} successful configurations for this operation."
                )
        
        # Check for similar contexts
        context_hash = self._hash_context(context)
        if event_type in self.patterns:
            common = self.patterns[event_type]['common_contexts']
            if context_hash in common:
                count = common[context_hash]['count']
                recommendations.append(
                    f"📊 This configuration has been used {count} times before."
                )
        
        return recommendations
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics."""
        total_events = len(self.events)
        successful_events = sum(1 for e in self.events if e.success)
        
        return {
            'total_events': total_events,
            'successful_events': successful_events,
            'failed_events': total_events - successful_events,
            'success_rate': (successful_events / total_events * 100) if total_events > 0 else 0,
            'event_types': len(self.patterns),
            'solutions_learned': sum(len(sols) for sols in self.solutions.values())
        }
    
    def _save(self) -> None:
        """Save knowledge base to disk."""
        data = {
            'events': [e.to_dict() for e in self.events[-1000:]],  # Keep last 1000
            'patterns': self.patterns,
            'solutions': self.solutions,
            'recommendations': self.recommendations
        }
        
        kb_file = self.storage_path / 'knowledge_base.json'
        with open(kb_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Knowledge base saved: {len(self.events)} events")
    
    def _load(self) -> None:
        """Load knowledge base from disk."""
        kb_file = self.storage_path / 'knowledge_base.json'
        
        if not kb_file.exists():
            return
        
        try:
            with open(kb_file, 'r') as f:
                data = json.load(f)
            
            self.events = [LearningEvent.from_dict(e) for e in data.get('events', [])]
            self.patterns = data.get('patterns', {})
            self.solutions = data.get('solutions', {})
            self.recommendations = data.get('recommendations', {})
            
            logger.info(f"Knowledge base loaded: {len(self.events)} events")
            
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")


class MultiModelAI:
    """
    Ollama-only AI system for free, local AI assistance.
    
    Features:
    - 100% FREE - no API keys needed
    - Runs locally on your machine
    - Complete privacy - no data sent to cloud
    - Supports multiple Ollama models (llama3.2, codellama, mistral, etc.)
    """
    
    def __init__(
        self,
        model: str = "llama3.2:3b"
    ):
        """
        Initialize Ollama AI client.
        
        Args:
            model: Ollama model name (default: llama3.2:3b)
        """
        self.model = model
        self.client: Any = None
        self._initialize_ollama()
    
    def _initialize_ollama(self) -> None:
        """Initialize Ollama client."""
        try:
            ollama = importlib.import_module("ollama")
            self.client = ollama
            logger.info(f"Ollama client initialized with model: {self.model}")
        except ModuleNotFoundError:
            logger.error(
                "Ollama not installed. Install with: pip install ollama\n"
                "Also install Ollama from: https://ollama.ai"
            )
            raise RuntimeError("Ollama is required but not installed")
        except Exception as exc:
            logger.error(f"Ollama initialization failed: {exc}")
            raise
    
    def query(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_retries: int = 3
    ) -> str:
        """
        Query Ollama model.
        
        Args:
            prompt: Query prompt
            model: Specific model name (optional, uses default if not provided)
            max_retries: Maximum retry attempts
            
        Returns:
            AI response
        """
        if not self.client:
            raise RuntimeError("Ollama client not initialized")
        
        model_to_use = model or self.model
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat(
                    model=model_to_use,
                    messages=[{'role': 'user', 'content': prompt}]
                )
                
                return response['message']['content']
                
            except Exception as e:
                logger.warning(f"Ollama query attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"Ollama query failed after {max_retries} attempts: {e}")
                continue
        
        raise Exception("Ollama query failed")


class ContinuousLearningSystem:
    """
    Continuous learning system that improves with usage.
    
    Features:
    - Records all interactions
    - Learns from successes and failures
    - Provides smarter recommendations over time
    - Adapts to user patterns
    - FREE AI support via Ollama (local)
    """
    
    def __init__(
        self,
        storage_path: Path,
        ollama_model: str = "llama3.2:3b"
    ):
        """
        Initialize learning system.
        
        Args:
            storage_path: Path to store knowledge base
            ollama_model: Ollama model to use (default: llama3.2:3b)
        """
        self.storage_path = Path(storage_path)
        self.knowledge_base = KnowledgeBase(self.storage_path / 'knowledge')
        
        # Ollama AI (100% free, local)
        try:
            self.ai = MultiModelAI(model=ollama_model)
        except Exception as e:
            logger.warning(f"AI initialization failed: {e}. Continuing without AI features.")
            self.ai = None
    
    def record_service_discovery(
        self,
        services: List[str],
        success: bool,
        errors: Optional[List[str]] = None
    ) -> None:
        """Record service discovery event."""
        event = LearningEvent(
            event_type='service_discovery',
            context={
                'service_count': len(services),
                'services': services,
                'errors': errors or []
            },
            outcome='success' if success else 'failure',
            success=success
        )
        
        self.knowledge_base.record_event(event)
    
    def record_dependency_resolution(
        self,
        dependencies: List[str],
        conflicts: List[str],
        success: bool
    ) -> None:
        """Record dependency resolution event."""
        event = LearningEvent(
            event_type='dependency_resolution',
            context={
                'dependency_count': len(dependencies),
                'conflict_count': len(conflicts),
                'dependencies': dependencies,
                'conflicts': conflicts
            },
            outcome='success' if success else 'failure',
            success=success
        )
        
        self.knowledge_base.record_event(event)
    
    def record_deployment(
        self,
        environment: str,
        services: List[str],
        success: bool,
        duration: float
    ) -> None:
        """Record deployment event."""
        event = LearningEvent(
            event_type='deployment',
            context={
                'environment': environment,
                'service_count': len(services),
                'services': services,
                'duration': duration
            },
            outcome='success' if success else 'failure',
            success=success
        )
        
        self.knowledge_base.record_event(event)
    
    def get_smart_recommendations(
        self,
        operation: str,
        context: Dict[str, Any]
    ) -> List[str]:
        """
        Get AI-powered recommendations based on learning.
        
        Args:
            operation: Operation type
            context: Current context
            
        Returns:
            List of smart recommendations
        """
        # Get knowledge-based recommendations
        kb_recommendations = self.knowledge_base.get_recommendations(operation, context)
        
        # Get AI-powered recommendations
        if self.ai:
            ai_recommendations = self._get_ai_recommendations(operation, context)
            kb_recommendations.extend(ai_recommendations)
        
        return kb_recommendations
    
    def _get_ai_recommendations(
        self,
        operation: str,
        context: Dict[str, Any]
    ) -> List[str]:
        """Get AI-powered recommendations."""
        # Get relevant patterns
        patterns = self.knowledge_base.patterns.get(operation, {})
        
        prompt = f"""
        Based on historical data, provide recommendations for this operation:
        
        Operation: {operation}
        Current Context: {json.dumps(context, indent=2)}
        
        Historical Patterns:
        - Total attempts: {patterns.get('total', 0)}
        - Successful: {patterns.get('successful', 0)}
        - Failed: {patterns.get('failed', 0)}
        
        Provide 3-5 specific, actionable recommendations to improve success rate.
        Format as bullet points.
        """
        
        try:
            response = self.ai.query(prompt)
            
            # Parse recommendations
            recommendations = [
                line.strip('- ').strip()
                for line in response.split('\n')
                if line.strip().startswith('-') or line.strip().startswith('•')
            ]
            
            return recommendations[:5]  # Max 5
            
        except Exception as e:
            logger.error(f"AI recommendations failed: {e}")
            return []
    
    def learn_from_error(
        self,
        error_type: str,
        error_message: str,
        context: Dict[str, Any],
        solution: Optional[str] = None
    ) -> Optional[str]:
        """
        Learn from error and suggest solution.
        
        Args:
            error_type: Type of error
            error_message: Error message
            context: Error context
            solution: Known solution (if available)
            
        Returns:
            Suggested solution
        """
        # Record the error
        event = LearningEvent(
            event_type=f'error_{error_type}',
            context={
                'error_message': error_message,
                **context
            },
            outcome=solution or 'unknown',
            success=solution is not None
        )
        
        self.knowledge_base.record_event(event)
        
        # Check if we've seen this error before
        event_type = f'error_{error_type}'
        if event_type in self.knowledge_base.solutions:
            solutions = self.knowledge_base.solutions[event_type]
            if solutions:
                logger.info(f"Found {len(solutions)} known solutions for this error")
                return f"Known solutions found: {len(solutions)} similar cases resolved"
        
        # Ask AI for solution
        if self.ai:
            return self._get_ai_solution(error_type, error_message, context)
        
        return None
    
    def _get_ai_solution(
        self,
        error_type: str,
        error_message: str,
        context: Dict[str, Any]
    ) -> str:
        """Get AI-powered error solution."""
        prompt = f"""
        Analyze this error and provide a solution:
        
        Error Type: {error_type}
        Error Message: {error_message}
        Context: {json.dumps(context, indent=2)}
        
        Provide:
        1. Root cause analysis
        2. Step-by-step solution
        3. Prevention tips
        
        Be specific and actionable.
        """
        
        try:
            return self.ai.query(prompt)
        except Exception as e:
            logger.error(f"AI solution failed: {e}")
            return "Unable to generate AI solution"
    
    def get_learning_report(self) -> Dict[str, Any]:
        """Get comprehensive learning report."""
        stats = self.knowledge_base.get_statistics()
        
        return {
            'statistics': stats,
            'top_operations': self._get_top_operations(),
            'improvement_areas': self._get_improvement_areas(),
            'knowledge_growth': self._get_knowledge_growth()
        }
    
    async def learn_from_database_data(
        self,
        multi_db_manager: Any
    ) -> Dict[str, Any]:
        """
        Learn from data in all microservice databases.
        
        Args:
            multi_db_manager: MultiDatabaseAccessManager instance
            
        Returns:
            Learning insights from database data
        """
        insights = {
            'data_patterns': {},
            'common_structures': {},
            'usage_patterns': {},
            'recommendations': []
        }
        
        try:
            # Get all schemas
            schemas = await multi_db_manager.discover_all_schemas()
            
            # Analyze each service's data
            for service_name, schema in schemas.items():
                if 'error' in schema:
                    continue
                
                service_insights = await self._analyze_service_data(
                    service_name,
                    schema,
                    multi_db_manager
                )
                
                insights['data_patterns'][service_name] = service_insights
            
            # Find common structures
            insights['common_structures'] = self._find_common_structures(schemas)
            
            # Generate recommendations
            insights['recommendations'] = self._generate_data_recommendations(insights)
            
            # Record learning event
            event = LearningEvent(
                event_type='database_learning',
                context={
                    'services_analyzed': len(schemas),
                    'patterns_found': len(insights['data_patterns'])
                },
                outcome='insights_generated',
                success=True
            )
            self.knowledge_base.record_event(event)
            
        except Exception as e:
            logger.error(f"Database learning failed: {e}")
            insights['error'] = str(e)
        
        return insights
    
    async def _analyze_service_data(
        self,
        service_name: str,
        schema: Dict[str, Any],
        multi_db_manager: Any
    ) -> Dict[str, Any]:
        """Analyze data patterns in a service."""
        patterns = {
            'tables': {},
            'data_types': {},
            'relationships': []
        }
        
        for table_name, table_schema in schema.get('tables', {}).items():
            # Analyze table structure
            columns = table_schema.get('columns', [])
            
            patterns['tables'][table_name] = {
                'column_count': len(columns),
                'has_timestamps': any(
                    'created_at' in c['name'].lower() or
                    'updated_at' in c['name'].lower()
                    for c in columns
                ),
                'has_id': any(c['name'] == 'id' for c in columns),
                'nullable_columns': sum(1 for c in columns if c['nullable'])
            }
            
            # Track data types
            for column in columns:
                dtype = column['type']
                patterns['data_types'][dtype] = patterns['data_types'].get(dtype, 0) + 1
            
            # Detect relationships
            for column in columns:
                if column['name'].endswith('_id') and column['name'] != 'id':
                    patterns['relationships'].append({
                        'table': table_name,
                        'column': column['name'],
                        'references': column['name'][:-3]
                    })
        
        # Get row counts
        try:
            stats = await multi_db_manager.connections[service_name].get_tables()
            patterns['table_count'] = len(stats)
        except:
            pass
        
        return patterns
    
    def _find_common_structures(
        self,
        schemas: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Find common table structures across services."""
        table_occurrences = {}
        
        for service_name, schema in schemas.items():
            if 'error' in schema:
                continue
            
            for table_name in schema.get('tables', {}).keys():
                if table_name not in table_occurrences:
                    table_occurrences[table_name] = []
                table_occurrences[table_name].append(service_name)
        
        # Find tables that appear in multiple services
        common = {
            table: services
            for table, services in table_occurrences.items()
            if len(services) > 1
        }
        
        return common
    
    def _generate_data_recommendations(
        self,
        insights: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on data analysis."""
        recommendations = []
        
        # Check for common tables
        common = insights.get('common_structures', {})
        if common:
            recommendations.append(
                f"📊 Found {len(common)} common tables across services - "
                "consider standardizing schemas"
            )
        
        # Check for missing timestamps
        for service, patterns in insights.get('data_patterns', {}).items():
            for table, info in patterns.get('tables', {}).items():
                if not info.get('has_timestamps'):
                    recommendations.append(
                        f"⏰ {service}.{table} missing timestamps - "
                        "add created_at/updated_at for better tracking"
                    )
        
        # Check for relationships
        total_relationships = sum(
            len(p.get('relationships', []))
            for p in insights.get('data_patterns', {}).values()
        )
        
        if total_relationships > 0:
            recommendations.append(
                f"🔗 Detected {total_relationships} relationships - "
                "ensure foreign key constraints for data integrity"
            )
        
        return recommendations[:10]  # Top 10
    
    def _get_top_operations(self) -> List[Dict[str, Any]]:
        """Get most common operations."""
        operations = []
        
        for event_type, pattern in self.knowledge_base.patterns.items():
            success_rate = (
                pattern['successful'] / pattern['total'] * 100
                if pattern['total'] > 0 else 0
            )
            
            operations.append({
                'operation': event_type,
                'total': pattern['total'],
                'success_rate': round(success_rate, 2)
            })
        
        return sorted(operations, key=lambda x: x['total'], reverse=True)[:10]
    
    def _get_improvement_areas(self) -> List[str]:
        """Identify areas needing improvement."""
        areas = []
        
        for event_type, pattern in self.knowledge_base.patterns.items():
            success_rate = (
                pattern['successful'] / pattern['total']
                if pattern['total'] > 0 else 0
            )
            
            if success_rate < 0.7 and pattern['total'] >= 5:
                areas.append(
                    f"{event_type}: {success_rate*100:.1f}% success rate ({pattern['total']} attempts)"
                )
        
        return areas
    
    def _get_knowledge_growth(self) -> Dict[str, int]:
        """Track knowledge base growth."""
        # Events per month (simplified)
        return {
            'total_events': len(self.knowledge_base.events),
            'patterns_learned': len(self.knowledge_base.patterns),
            'solutions_discovered': sum(
                len(sols) for sols in self.knowledge_base.solutions.values()
            )
        }
    
    async def record_autonomous_development(
        self,
        description: str,
        industry: str,
        result: Dict[str, Any],
        report: Dict[str, Any]
    ) -> None:
        """
        Record autonomous development event for learning.
        
        Args:
            description: Application description
            industry: Industry type
            result: Development results
            report: Development report
        """
        # Extract key information
        approval_rate = report.get('approval_rate', 0)
        team_size = report.get('team', {}).get('size', 0)
        total_votes = len(report.get('decisions', []))
        
        # Determine success
        success = approval_rate >= 70
        
        # Create learning event
        event = LearningEvent(
            event_type='autonomous_development',
            context={
                'description': description[:200],  # Truncate
                'industry': industry,
                'team_size': team_size,
                'total_votes': total_votes,
                'phases': list(result.get('phases', {}).keys())
            },
            outcome=f"Approval rate: {approval_rate:.1f}%",
            success=success
        )
        
        self.knowledge_base.record_event(event)
        
        # Learn patterns from decisions
        for decision in report.get('decisions', []):
            phase = decision.get('phase')
            approved = decision.get('result', {}).get('approved', False)
            
            # Track phase success rates
            if phase not in self.knowledge_base.patterns:
                self.knowledge_base.patterns[phase] = {
                    'total': 0,
                    'successful': 0,
                    'common_contexts': []
                }
            
            self.knowledge_base.patterns[phase]['total'] += 1
            if approved:
                self.knowledge_base.patterns[phase]['successful'] += 1
        
        # Save knowledge
        self.knowledge_base._save()
        
        logger.info(
            f"Recorded autonomous development: "
            f"{industry}, approval={approval_rate:.1f}%"
        )

