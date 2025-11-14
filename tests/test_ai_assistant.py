"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_ai_assistant.py
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

import pytest
from unittest.mock import Mock, patch
from gravity_framework.ai.assistant import AIAssistant
from gravity_framework.models.service import (
    Service,
    ServiceManifest,
    ServiceDependency,
    DatabaseRequirement,
    DatabaseType,
    ServiceType
)


class TestAIAssistant:
    """Tests for AI Assistant functionality."""
    
    def test_ai_assistant_init_enabled(self):
        """Test AI assistant initialization when enabled."""
        assistant = AIAssistant(enabled=True)
        
        # Should initialize (even if Copilot not detected, for testing)
        assert assistant is not None
    
    def test_ai_assistant_init_disabled(self):
        """Test AI assistant initialization when disabled."""
        assistant = AIAssistant(enabled=False)
        
        assert assistant.enabled is False
    
    def test_detect_ollama_not_found(self):
        """Test Ollama detection when not installed."""
        assistant = AIAssistant(enabled=False)
        
        # Should return False when Ollama is not detected
        with patch('requests.get', side_effect=Exception("Connection refused")):
            result = assistant._detect_ollama()
            assert result is False
    
    def test_analyze_services_disabled(self):
        """Test analyze_services when AI is disabled."""
        assistant = AIAssistant(enabled=False)
        
        services = []
        result = assistant.analyze_services(services)
        
        assert result['enabled'] is False
        assert 'message' in result
    
    def test_analyze_services_with_dependencies(self):
        """Test service analysis with dependencies."""
        assistant = AIAssistant(enabled=True)
        
        # Create services with dependencies
        manifest1 = ServiceManifest(
            name="auth-service",
            version="1.0.0",
            repository="https://github.com/test/auth"
        )
        service1 = Service(manifest=manifest1)
        
        manifest2 = ServiceManifest(
            name="user-service",
            version="1.0.0",
            repository="https://github.com/test/user",
            dependencies=[
                ServiceDependency(name="auth-service", version=">=1.0.0")
            ]
        )
        service2 = Service(manifest=manifest2)
        
        services = [service1, service2]
        
        # Allow AI to work even without Copilot for testing
        assistant.enabled = True
        result = assistant.analyze_services(services)
        
        assert result['total_services'] == 2
        assert 'recommendations' in result
        assert len(result['recommendations']) > 0
    
    def test_analyze_services_with_databases(self):
        """Test service analysis with database requirements."""
        assistant = AIAssistant(enabled=True)
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            databases=[
                DatabaseRequirement(name="testdb", type=DatabaseType.POSTGRESQL),
                DatabaseRequirement(name="cache", type=DatabaseType.REDIS)
            ]
        )
        service = Service(manifest=manifest)
        
        result = assistant.analyze_services([service])
        
        assert result['total_services'] == 1
    
    def test_analyze_services_shared_database(self):
        """Test detection of shared databases."""
        assistant = AIAssistant(enabled=True)
        
        # Two services with same database name
        manifest1 = ServiceManifest(
            name="service1",
            version="1.0.0",
            repository="https://github.com/test/s1",
            databases=[DatabaseRequirement(name="shared_db", type=DatabaseType.POSTGRESQL)]
        )
        service1 = Service(manifest=manifest1)
        
        manifest2 = ServiceManifest(
            name="service2",
            version="1.0.0",
            repository="https://github.com/test/s2",
            databases=[DatabaseRequirement(name="shared_db", type=DatabaseType.POSTGRESQL)]
        )
        service2 = Service(manifest=manifest2)
        
        result = assistant.analyze_services([service1, service2])
        
        assert 'warnings' in result
        # Should detect shared database
        has_shared_db_warning = any(
            w.get('type') == 'shared_database' 
            for w in result.get('warnings', [])
        )
        assert has_shared_db_warning
    
    def test_analyze_services_recommends_cache(self):
        """Test cache recommendation for multiple services."""
        assistant = AIAssistant(enabled=True)
        
        # Create 4 services without Redis
        services = []
        for i in range(4):
            manifest = ServiceManifest(
                name=f"service{i}",
                version="1.0.0",
                repository=f"https://github.com/test/s{i}"
            )
            services.append(Service(manifest=manifest))
        
        result = assistant.analyze_services(services)
        
        # Should recommend caching
        has_cache_rec = any(
            r.get('type') == 'caching'
            for r in result.get('recommendations', [])
        )
        assert has_cache_rec
    
    def test_analyze_services_recommends_api_gateway(self):
        """Test API gateway recommendation for many services."""
        assistant = AIAssistant(enabled=True)
        
        # Create 6 services
        services = []
        for i in range(6):
            manifest = ServiceManifest(
                name=f"service{i}",
                version="1.0.0",
                repository=f"https://github.com/test/s{i}"
            )
            services.append(Service(manifest=manifest))
        
        result = assistant.analyze_services(services)
        
        # Should recommend API gateway
        has_gateway_opt = any(
            o.get('type') == 'api_gateway'
            for o in result.get('optimizations', [])
        )
        assert has_gateway_opt
    
    def test_suggest_connections_auth_service(self):
        """Test connection suggestions with auth service."""
        assistant = AIAssistant(enabled=True)
        
        # Auth service
        auth_manifest = ServiceManifest(
            name="auth-service",
            version="1.0.0",
            repository="https://github.com/test/auth",
            type=ServiceType.API,
            api_prefix="/api/auth"
        )
        auth_service = Service(manifest=auth_manifest)
        
        # Other service
        user_manifest = ServiceManifest(
            name="user-service",
            version="1.0.0",
            repository="https://github.com/test/user",
            type=ServiceType.API
        )
        user_service = Service(manifest=user_manifest)
        
        services = [auth_service, user_service]
        suggestions = assistant.suggest_connections(services)
        
        # Should suggest auth connection
        assert len(suggestions) > 0
        auth_suggestions = [s for s in suggestions if s['type'] == 'authentication']
        assert len(auth_suggestions) > 0
    
    def test_suggest_connections_frontend_api(self):
        """Test connection suggestions between frontend and API."""
        assistant = AIAssistant(enabled=True)
        
        # Frontend (using WEB type)
        frontend_manifest = ServiceManifest(
            name="frontend",
            version="1.0.0",
            repository="https://github.com/test/frontend",
            type=ServiceType.WEB
        )
        frontend = Service(manifest=frontend_manifest)
        
        # API
        api_manifest = ServiceManifest(
            name="api-service",
            version="1.0.0",
            repository="https://github.com/test/api",
            type=ServiceType.API,
            api_prefix="/api"
        )
        api = Service(manifest=api_manifest)
        
        services = [frontend, api]
        suggestions = assistant.suggest_connections(services)
        
        # Should suggest API consumption
        api_suggestions = [s for s in suggestions if s['type'] == 'api_consumption']
        assert len(api_suggestions) > 0
    
    def test_diagnose_connection_refused(self):
        """Test diagnosis of connection refused error."""
        assistant = AIAssistant(enabled=True)
        
        error = "Connection refused on port 8000"
        context = {"service": "auth-service"}
        
        diagnosis = assistant.diagnose_issue(error, context)
        
        assert 'likely_cause' in diagnosis
        assert 'solutions' in diagnosis
        assert len(diagnosis['solutions']) > 0
        assert 'port' in diagnosis['likely_cause'].lower() or 'running' in diagnosis['likely_cause'].lower()
    
    def test_diagnose_database_error(self):
        """Test diagnosis of database error."""
        assistant = AIAssistant(enabled=True)
        
        error = "Database connection failed"
        diagnosis = assistant.diagnose_issue(error, {})
        
        assert 'database' in diagnosis['likely_cause'].lower()
        assert len(diagnosis['solutions']) > 0
    
    def test_diagnose_timeout_error(self):
        """Test diagnosis of timeout error."""
        assistant = AIAssistant(enabled=True)
        
        error = "Request timeout after 30 seconds"
        diagnosis = assistant.diagnose_issue(error, {})
        
        assert 'long' in diagnosis['likely_cause'].lower() or 'respond' in diagnosis['likely_cause'].lower()
        assert len(diagnosis['solutions']) > 0
    
    def test_optimize_deployment_disabled(self):
        """Test deployment optimization when AI is disabled."""
        assistant = AIAssistant(enabled=False)
        
        services = []
        result = assistant.optimize_deployment(services)
        
        assert result['enabled'] is False
    
    def test_optimize_deployment_with_databases(self):
        """Test deployment optimization for services with databases."""
        assistant = AIAssistant(enabled=True)
        
        manifest = ServiceManifest(
            name="test-service",
            version="1.0.0",
            repository="https://github.com/test/test",
            databases=[DatabaseRequirement(name="testdb", type=DatabaseType.POSTGRESQL)]
        )
        service = Service(manifest=manifest)
        
        result = assistant.optimize_deployment([service])
        
        assert 'resource_allocation' in result
        # Should recommend extra memory for database connections
        assert len(result['resource_allocation']) > 0
    
    def test_optimize_deployment_scaling(self):
        """Test scaling recommendations."""
        assistant = AIAssistant(enabled=True)
        
        # Multiple API services
        services = []
        for i in range(3):
            manifest = ServiceManifest(
                name=f"api-service-{i}",
                version="1.0.0",
                repository=f"https://github.com/test/api{i}",
                type=ServiceType.API
            )
            services.append(Service(manifest=manifest))
        
        result = assistant.optimize_deployment(services)
        
        assert 'scaling' in result
        # Should recommend load balancer
        assert len(result['scaling']) > 0
    
    def test_optimize_deployment_performance_cache(self):
        """Test performance optimization - caching."""
        assistant = AIAssistant(enabled=True)
        
        # Services without Redis
        services = []
        for i in range(2):
            manifest = ServiceManifest(
                name=f"service-{i}",
                version="1.0.0",
                repository=f"https://github.com/test/s{i}"
            )
            services.append(Service(manifest=manifest))
        
        result = assistant.optimize_deployment(services)
        
        assert 'performance' in result
        # Should recommend adding cache
        cache_opts = [p for p in result['performance'] if p.get('type') == 'caching']
        assert len(cache_opts) > 0
    
    def test_generate_migration_suggestions_disabled(self):
        """Test migration generation when AI is disabled."""
        assistant = AIAssistant(enabled=False)
        
        from_schema = {}
        to_schema = {}
        
        result = assistant.generate_migration_suggestions(from_schema, to_schema)
        
        assert len(result) > 0
        assert "not available" in result[0]
    
    def test_generate_migration_suggestions_new_table(self):
        """Test migration suggestions for new tables."""
        assistant = AIAssistant(enabled=True)
        
        from_schema = {
            "tables": {
                "users": {"columns": ["id", "name"]}
            }
        }
        
        to_schema = {
            "tables": {
                "users": {"columns": ["id", "name"]},
                "posts": {"columns": ["id", "title", "user_id"]}
            }
        }
        
        result = assistant.generate_migration_suggestions(from_schema, to_schema)
        
        # Should detect new table
        migration_text = '\n'.join(result)
        assert 'posts' in migration_text.lower()
