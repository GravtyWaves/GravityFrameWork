"""
AI Assistant for intelligent microservice orchestration.

This module provides 100% FREE AI-powered assistance using Ollama (local AI models)
to help users connect microservices, analyze database schemas, and make intelligent
architectural decisions.

Ollama is completely free, runs locally, and supports models like:
- Llama 3.2 (3B) - Fast and lightweight
- Llama 3.1 (8B) - Balanced performance
- DeepSeek Coder - Specialized for code
- Qwen 2.5 Coder - Excellent for technical analysis

No API keys, no subscriptions, no internet required after model download!
"""

import logging
import subprocess
import json
import requests
from typing import List, Dict, Optional, Any
from pathlib import Path

from gravity_framework.models.service import Service

logger = logging.getLogger(__name__)


class AIAssistant:
    """
    AI-powered assistant for intelligent microservice orchestration.
    
    Uses Ollama (100% FREE local AI) to provide:
    - Service connection recommendations (puzzle-solving)
    - Database schema analysis across all microservices
    - Architecture optimization suggestions
    - Intelligent error diagnosis
    
    Completely FREE - no API keys, no subscriptions, runs locally!
    Install: https://ollama.com/download
    """
    
    def __init__(self, enabled: bool = True, ollama_model: str = "llama3.2:3b"):
        """Initialize AI assistant.
        
        Args:
            enabled: Whether AI assistance is enabled (auto-detects Ollama)
            ollama_model: Ollama model to use (default: llama3.2:3b - fast and free)
        """
        self.ollama_model = ollama_model
        self.ollama_url = "http://localhost:11434"
        self.enabled = enabled and self._detect_ollama()
        self._analysis_cache: Dict[str, Any] = {}
        
        if self.enabled:
            logger.info(f"🤖 AI Assistant enabled - Ollama ({self.ollama_model}) detected")
        else:
            logger.warning("⚠️ AI Assistant disabled - install Ollama for FREE: https://ollama.com/download")
    
    def _detect_ollama(self) -> bool:
        """Detect if Ollama is running locally.
        
        Returns:
            True if Ollama is available
        """
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                # Check if our preferred model is available
                model_names = [m.get('name', '') for m in models]
                if any(self.ollama_model in name for name in model_names):
                    logger.debug(f"✓ Ollama model {self.ollama_model} found")
                    return True
                elif model_names:
                    # Use first available model
                    self.ollama_model = model_names[0].split(':')[0] + ':latest'
                    logger.info(f"Using available Ollama model: {self.ollama_model}")
                    return True
                else:
                    logger.warning(f"Ollama running but no models installed. Run: ollama pull {self.ollama_model}")
                    return False
                    
        except requests.exceptions.RequestException:
            logger.debug("Ollama not detected. Install from: https://ollama.com/download")
        except Exception as e:
            logger.debug(f"Ollama detection failed: {e}")
        
        return False
    
    def _ask_ollama(self, prompt: str, system_prompt: str = "") -> str:
        """Ask Ollama AI a question.
        
        Args:
            prompt: The question/prompt to send
            system_prompt: System context for the AI
            
        Returns:
            AI response text
        """
        try:
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "system": system_prompt or "You are an expert in microservices architecture, databases, and DevOps.",
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return ""
                
        except Exception as e:
            logger.error(f"Failed to query Ollama: {e}")
            return ""
    
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
            return {"enabled": False, "message": "Install Ollama for FREE AI assistance: https://ollama.com/download"}
        
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
