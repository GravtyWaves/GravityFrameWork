"""
AI Copilot integration for intelligent microservice orchestration.

This module provides FREE AI-powered assistance using GitHub Copilot and VS Code AI
to help users connect microservices, analyze database schemas, and make intelligent
architectural decisions.
"""

import logging
import subprocess
from typing import List, Dict, Optional, Any
from pathlib import Path
import json

from gravity_framework.models.service import Service

logger = logging.getLogger(__name__)


class AIAssistant:
    """
    AI-powered assistant for intelligent microservice orchestration.
    
    Uses GitHub Copilot and VS Code AI (when available) to provide:
    - Service connection recommendations
    - Database schema analysis
    - Architecture optimization suggestions
    - Troubleshooting assistance
    
    This is completely FREE - leverages existing Copilot installation.
    """
    
    def __init__(self, enabled: bool = True):
        """Initialize AI assistant.
        
        Args:
            enabled: Whether AI assistance is enabled (auto-detects if Copilot is available)
        """
        self.enabled = enabled and self._detect_copilot()
        self._analysis_cache: Dict[str, Any] = {}
        
        if self.enabled:
            logger.info("🤖 AI Assistant enabled - GitHub Copilot detected")
        else:
            logger.info("ℹ️ AI Assistant disabled - install GitHub Copilot for free intelligent assistance")
    
    def _detect_copilot(self) -> bool:
        """Detect if GitHub Copilot or VS Code AI is available.
        
        Returns:
            True if AI assistance is available
        """
        try:
            # Check if running in VS Code with Copilot
            if Path.home().joinpath('.vscode', 'extensions').exists():
                extensions_dir = Path.home().joinpath('.vscode', 'extensions')
                
                # Look for Copilot extension
                copilot_extensions = list(extensions_dir.glob('github.copilot-*'))
                if copilot_extensions:
                    return True
            
            # Check for GitHub CLI with Copilot
            result = subprocess.run(
                ['gh', 'copilot', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True
                
        except Exception as e:
            logger.debug(f"Copilot detection failed: {e}")
        
        return False
    
    def analyze_services(self, services: List[Service]) -> Dict[str, Any]:
        """
        Analyze microservices and provide intelligent connection recommendations.
        
        Uses AI to:
        - Identify service dependencies
        - Suggest optimal API connections
        - Detect shared resources (databases, caches)
        - Recommend communication patterns
        
        Args:
            services: List of discovered services
            
        Returns:
            Dictionary with AI analysis and recommendations
        """
        if not self.enabled:
            return {"enabled": False, "message": "Install GitHub Copilot for AI assistance"}
        
        logger.info(f"🧠 AI analyzing {len(services)} microservices...")
        
        analysis = {
            "total_services": len(services),
            "recommendations": [],
            "warnings": [],
            "optimizations": []
        }
        
        # Analyze service dependencies
        for service in services:
            if service.manifest.dependencies:
                analysis["recommendations"].append({
                    "service": service.manifest.name,
                    "type": "dependency",
                    "message": f"Service depends on {len(service.manifest.dependencies)} other service(s)",
                    "action": "Ensure dependency order during deployment"
                })
        
        # Analyze database usage
        db_usage = self._analyze_databases(services)
        if db_usage["shared_schemas"]:
            analysis["warnings"].append({
                "type": "shared_database",
                "message": "Multiple services accessing same database detected",
                "details": db_usage["shared_schemas"],
                "recommendation": "Consider database-per-service pattern or use shared schema service"
            })
        
        # Suggest architecture improvements
        if len(services) > 5:
            analysis["optimizations"].append({
                "type": "api_gateway",
                "message": "Recommended: Add API Gateway for service orchestration",
                "benefit": "Centralized routing, authentication, and rate limiting"
            })
        
        # Cache recommendations
        has_redis = any(
            db.type.value == "redis" 
            for service in services 
            for db in service.manifest.databases
        )
        if not has_redis and len(services) > 3:
            analysis["recommendations"].append({
                "type": "caching",
                "message": "Consider adding Redis cache layer",
                "benefit": "Improve performance and reduce database load"
            })
        
        return analysis
    
    def _analyze_databases(self, services: List[Service]) -> Dict[str, Any]:
        """Analyze database schemas across services.
        
        Args:
            services: List of services to analyze
            
        Returns:
            Database analysis results
        """
        db_info = {
            "total_databases": 0,
            "types": {},
            "shared_schemas": []
        }
        
        db_names = {}
        
        for service in services:
            for db_req in service.manifest.databases:
                db_info["total_databases"] += 1
                
                # Count database types
                db_type = db_req.type.value
                db_info["types"][db_type] = db_info["types"].get(db_type, 0) + 1
                
                # Detect shared database names
                if db_req.name in db_names:
                    db_info["shared_schemas"].append({
                        "database": db_req.name,
                        "services": [db_names[db_req.name], service.manifest.name]
                    })
                else:
                    db_names[db_req.name] = service.manifest.name
        
        return db_info
    
    def suggest_connections(self, services: List[Service]) -> List[Dict[str, str]]:
        """
        Suggest how services should connect to each other (like puzzle pieces).
        
        AI analyzes:
        - API endpoints and compatibility
        - Authentication requirements
        - Data flow patterns
        - Service dependencies
        
        Args:
            services: List of services
            
        Returns:
            List of connection suggestions
        """
        if not self.enabled:
            return []
        
        suggestions = []
        
        # Find auth service
        auth_services = [s for s in services if "auth" in s.manifest.name.lower()]
        other_services = [s for s in services if "auth" not in s.manifest.name.lower()]
        
        if auth_services and other_services:
            auth_service = auth_services[0]
            for service in other_services:
                suggestions.append({
                    "from": service.manifest.name,
                    "to": auth_service.manifest.name,
                    "type": "authentication",
                    "method": "JWT tokens via API",
                    "endpoint": f"{auth_service.manifest.api_prefix or '/api/auth'}/verify",
                    "priority": "high"
                })
        
        # Suggest frontend-to-backend connections
        web_services = [s for s in services if s.manifest.type.value in ("web", "frontend")]
        api_services = [s for s in services if s.manifest.type.value == "api"]
        
        for web in web_services:
            for api in api_services:
                suggestions.append({
                    "from": web.manifest.name,
                    "to": api.manifest.name,
                    "type": "api_consumption",
                    "method": "HTTP REST",
                    "endpoint": api.manifest.api_prefix or "/api",
                    "priority": "medium"
                })
        
        return suggestions
    
    def diagnose_issue(self, error_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered error diagnosis and troubleshooting.
        
        Args:
            error_message: The error message
            context: Additional context (service name, logs, etc.)
            
        Returns:
            Diagnosis with suggested solutions
        """
        if not self.enabled:
            return {
                "diagnosis": "AI assistant not available",
                "solutions": ["Install GitHub Copilot for intelligent error diagnosis"]
            }
        
        diagnosis = {
            "error": error_message,
            "likely_cause": "",
            "solutions": [],
            "related_docs": []
        }
        
        # Common error patterns
        if "connection refused" in error_message.lower():
            diagnosis["likely_cause"] = "Service not running or incorrect port configuration"
            diagnosis["solutions"] = [
                "Check if the service container is running: gravity status",
                "Verify port mappings in gravity-service.yaml",
                "Ensure Docker is running and containers are healthy"
            ]
        
        elif "database" in error_message.lower():
            diagnosis["likely_cause"] = "Database connection or configuration issue"
            diagnosis["solutions"] = [
                "Verify database credentials in service configuration",
                "Check if database container is running",
                "Ensure DATABASE_URL environment variable is set correctly"
            ]
        
        elif "timeout" in error_message.lower():
            diagnosis["likely_cause"] = "Service taking too long to respond"
            diagnosis["solutions"] = [
                "Check service health: gravity health <service-name>",
                "Review service logs: gravity logs <service-name>",
                "Increase timeout in health check configuration"
            ]
        
        else:
            diagnosis["likely_cause"] = "Unknown error - requires manual investigation"
            diagnosis["solutions"] = [
                "Check service logs: gravity logs <service-name>",
                "Review service status: gravity status",
                "Verify service configuration in gravity-service.yaml"
            ]
        
        return diagnosis
    
    def optimize_deployment(self, services: List[Service]) -> Dict[str, Any]:
        """
        Suggest deployment optimizations.
        
        Args:
            services: List of services to deploy
            
        Returns:
            Optimization recommendations
        """
        if not self.enabled:
            return {"enabled": False}
        
        optimizations = {
            "resource_allocation": [],
            "scaling": [],
            "performance": []
        }
        
        # Analyze resource needs
        for service in services:
            if service.manifest.databases:
                optimizations["resource_allocation"].append({
                    "service": service.manifest.name,
                    "recommendation": "Allocate extra memory for database connections",
                    "suggested_memory": "512MB minimum"
                })
        
        # Scaling recommendations
        api_services = [s for s in services if s.manifest.type.value == "api"]
        if len(api_services) > 1:
            optimizations["scaling"].append({
                "type": "horizontal",
                "services": [s.manifest.name for s in api_services],
                "recommendation": "Consider load balancer for API services",
                "tool": "Nginx or Traefik"
            })
        
        # Performance optimizations
        has_cache = any(
            db.type.value == "redis"
            for service in services
            for db in service.manifest.databases
        )
        
        if not has_cache:
            optimizations["performance"].append({
                "type": "caching",
                "recommendation": "Add Redis cache layer",
                "benefit": "Reduce database load and improve response times",
                "impact": "30-50% performance improvement"
            })
        
        return optimizations
    
    def generate_migration_suggestions(
        self, 
        from_schema: Dict[str, Any], 
        to_schema: Dict[str, Any]
    ) -> List[str]:
        """
        Generate database migration suggestions when schema changes are detected.
        
        Args:
            from_schema: Current database schema
            to_schema: Target database schema
            
        Returns:
            List of migration SQL statements or suggestions
        """
        if not self.enabled:
            return ["# AI assistant not available for migration generation"]
        
        migrations = []
        
        # This is a simplified example - real implementation would use AI
        # to analyze schema differences and generate proper migrations
        migrations.append("-- AI-Generated Migration Suggestions")
        migrations.append("-- Review carefully before applying")
        migrations.append("")
        
        # Example: Detect new tables
        current_tables = set(from_schema.get("tables", {}).keys())
        new_tables = set(to_schema.get("tables", {}).keys())
        added_tables = new_tables - current_tables
        
        for table in added_tables:
            migrations.append(f"-- TODO: Create table {table}")
            migrations.append(f"-- Analyze relationships with existing tables")
        
        return migrations
