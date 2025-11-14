"""Service discovery scanner for Git repositories."""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml
import git
from jsonschema import validate, ValidationError

from gravity_framework.models.service import ServiceManifest, Service, ServiceStatus

logger = logging.getLogger(__name__)


MANIFEST_SCHEMA = {
    "type": "object",
    "required": ["name", "version", "repository"],
    "properties": {
        "name": {"type": "string", "pattern": "^[a-z0-9_-]+$"},
        "version": {"type": "string"},
        "description": {"type": "string"},
        "type": {"type": "string", "enum": ["api", "web", "worker", "cron", "database", "cache"]},
        "repository": {"type": "string"},
        "branch": {"type": "string"},
        "dependencies": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "version": {"type": "string"},
                    "optional": {"type": "boolean"}
                }
            }
        },
        "databases": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "type"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string", "enum": ["postgresql", "mysql", "mongodb", "redis"]},
                    "version": {"type": "string"},
                    "charset": {"type": "string"},
                    "collation": {"type": "string"},
                    "extensions": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "runtime": {"type": "string"},
        "command": {"type": "string"},
        "working_dir": {"type": "string"},
        "ports": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["container"],
                "properties": {
                    "container": {"type": "integer"},
                    "host": {"type": "integer"},
                    "protocol": {"type": "string"}
                }
            }
        },
        "health_check": {
            "type": "object",
            "properties": {
                "endpoint": {"type": "string"},
                "interval": {"type": "integer"},
                "timeout": {"type": "integer"},
                "retries": {"type": "integer"}
            }
        },
        "environment": {
            "type": "object",
            "properties": {
                "variables": {"type": "object"},
                "secrets": {"type": "array", "items": {"type": "string"}}
            }
        },
        "api_prefix": {"type": "string"},
        "public": {"type": "boolean"},
        "cpu_limit": {"type": "string"},
        "memory_limit": {"type": "string"},
        "install_script": {"type": "string"},
        "build_args": {"type": "object"}
    }
}


class ServiceScanner:
    """Service discovery scanner."""
    
    def __init__(self, services_dir: Path):
        """Initialize scanner.
        
        Args:
            services_dir: Directory where services are cloned
        """
        self.services_dir = services_dir
        self.services_dir.mkdir(parents=True, exist_ok=True)
    
    def discover_from_git(self, repo_url: str, branch: str = "main") -> Optional[Service]:
        """Discover service from Git repository.
        
        Args:
            repo_url: Git repository URL
            branch: Git branch name
            
        Returns:
            Discovered service or None if not found
        """
        logger.info(f"Discovering service from {repo_url} (branch: {branch})")
        
        try:
            # Extract repo name
            repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
            service_path = self.services_dir / repo_name
            
            # Clone or update repository
            if service_path.exists():
                logger.info(f"Updating existing repository: {repo_name}")
                repo = git.Repo(service_path)
                repo.remotes.origin.pull(branch)
            else:
                logger.info(f"Cloning repository: {repo_name}")
                repo = git.Repo.clone_from(repo_url, service_path, branch=branch)
            
            # Look for manifest file
            manifest_path = service_path / "gravity-service.yaml"
            if not manifest_path.exists():
                # Try alternative names
                for alt_name in ["gravity-service.yml", ".gravity-service.yaml", ".gravity.yaml"]:
                    alt_path = service_path / alt_name
                    if alt_path.exists():
                        manifest_path = alt_path
                        break
                else:
                    logger.warning(f"No gravity-service.yaml found in {repo_name}")
                    return None
            
            # Parse manifest
            manifest = self._parse_manifest(manifest_path, repo_url, branch)
            if not manifest:
                return None
            
            # Create service instance
            service = Service(
                manifest=manifest,
                status=ServiceStatus.DISCOVERED,
                path=str(service_path)
            )
            
            logger.info(f"✓ Discovered service: {manifest.name} v{manifest.version}")
            return service
            
        except git.GitCommandError as e:
            logger.error(f"Git error while discovering service: {e}")
            return None
        except Exception as e:
            logger.error(f"Error discovering service: {e}")
            return None
    
    def discover_from_path(self, path: Path) -> Optional[Service]:
        """Discover service from local path.
        
        Args:
            path: Local path to service
            
        Returns:
            Discovered service or None if not found
        """
        logger.info(f"Discovering service from {path}")
        
        manifest_path = path / "gravity-service.yaml"
        if not manifest_path.exists():
            logger.warning(f"No gravity-service.yaml found in {path}")
            return None
        
        manifest = self._parse_manifest(manifest_path, str(path), "local")
        if not manifest:
            return None
        
        service = Service(
            manifest=manifest,
            status=ServiceStatus.DISCOVERED,
            path=str(path)
        )
        
        logger.info(f"✓ Discovered service: {manifest.name} v{manifest.version}")
        return service
    
    def discover_all(self) -> List[Service]:
        """Discover all services in services directory.
        
        Returns:
            List of discovered services
        """
        logger.info(f"Scanning for services in {self.services_dir}")
        services = []
        
        for service_dir in self.services_dir.iterdir():
            if not service_dir.is_dir() or service_dir.name.startswith("."):
                continue
            
            service = self.discover_from_path(service_dir)
            if service:
                services.append(service)
        
        logger.info(f"✓ Discovered {len(services)} service(s)")
        return services
    
    def _parse_manifest(self, manifest_path: Path, repo: str, branch: str) -> Optional[ServiceManifest]:
        """Parse service manifest file.
        
        Args:
            manifest_path: Path to manifest file
            repo: Repository URL or path
            branch: Branch name
            
        Returns:
            Parsed manifest or None if invalid
        """
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            if not data:
                logger.error(f"Empty manifest file: {manifest_path}")
                return None
            
            # Validate against JSON schema
            validate(instance=data, schema=MANIFEST_SCHEMA)
            
            # Ensure repository and branch are set
            data.setdefault("repository", repo)
            data.setdefault("branch", branch)
            
            # Parse into Pydantic model
            manifest = ServiceManifest(**data)
            
            logger.debug(f"Parsed manifest for {manifest.name}")
            return manifest
            
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {manifest_path}: {e}")
            return None
        except ValidationError as e:
            logger.error(f"Manifest validation error in {manifest_path}: {e.message}")
            return None
        except Exception as e:
            logger.error(f"Error parsing manifest {manifest_path}: {e}")
            return None
