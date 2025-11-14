"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/discovery/scanner.py
PURPOSE: Service discovery from Git repositories and local paths
DESCRIPTION: Scans Git repositories and local directories to discover microservices
             and parse their manifests. Supports PRIVATE repositories with
             authentication (SSH keys, Personal Access Tokens, OAuth).

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict
import git
import yaml
from jsonschema import validate, ValidationError

from gravity_framework.models.service import Service, ServiceManifest, ServiceStatus

logger = logging.getLogger(__name__)

# Manifest schema for validation
MANIFEST_SCHEMA = {
    "type": "object",
    "required": ["name", "version"],
    "properties": {
        "name": {"type": "string"},
        "version": {"type": "string"},
        "description": {"type": "string"},
        "repository": {"type": "string"},
        "branch": {"type": "string"}
    }
}


class ServiceScanner:
    """
    Service scanner with private repository support.
    
    Supports authentication for private GitHub/GitLab/Bitbucket repositories using:
    - Personal Access Tokens (HTTPS)
    - SSH Keys
    - OAuth (future support)
    """
    
    def __init__(
        self, 
        services_dir: Path,
        auth_token: Optional[str] = None,
        ssh_key_path: Optional[Path] = None
    ):
        """Initialize scanner with authentication support.
        
        Args:
            services_dir: Directory where services are cloned
            auth_token: Personal Access Token for HTTPS authentication (GitHub/GitLab/Bitbucket)
            ssh_key_path: Path to SSH private key for SSH authentication
        """
        self.services_dir = services_dir
        self.services_dir.mkdir(parents=True, exist_ok=True)
        
        # Authentication credentials
        self.auth_token = auth_token or os.getenv('GIT_AUTH_TOKEN')
        self.ssh_key_path = ssh_key_path or os.getenv('GIT_SSH_KEY_PATH')
        
        logger.info("Scanner initialized with authentication support")
    
    def discover_from_git(self, repo_url: str, branch: str = "main") -> Optional[Service]:
        """Discover service from Git repository (supports private repos).
        
        Authentication methods:
        1. SSH: Uses SSH key from ssh_key_path or ~/.ssh/id_rsa
        2. HTTPS + Token: Uses Personal Access Token (GitHub/GitLab/Bitbucket)
        3. OAuth: Future support for OAuth flow
        
        Args:
            repo_url: Git repository URL (HTTPS or SSH format)
                     Examples:
                     - https://github.com/user/repo.git
                     - git@github.com:user/repo.git
                     - https://gitlab.com/user/repo.git
            branch: Git branch name
            
        Returns:
            Discovered service or None if not found
        """
        logger.info(f"Discovering service from {repo_url} (branch: {branch})")
        
        try:
            # Extract repo name
            repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
            service_path = self.services_dir / repo_name
            
            # Prepare authentication
            clone_url = self._prepare_authenticated_url(repo_url)
            git_env = self._prepare_git_environment()
            
            # Clone or update repository
            if service_path.exists():
                logger.info(f"Updating existing repository: {repo_name}")
                repo = git.Repo(service_path)
                
                # Set authentication for private repos
                if self.auth_token and repo_url.startswith("https://"):
                    # Update remote URL with token
                    repo.remotes.origin.set_url(clone_url)
                
                # Pull latest changes
                with repo.git.custom_environment(**git_env):
                    repo.remotes.origin.pull(branch)
            else:
                logger.info(f"Cloning repository: {repo_name}")
                
                # Clone with authentication
                if git_env:
                    # SSH authentication
                    repo = git.Repo.clone_from(
                        repo_url, 
                        service_path, 
                        branch=branch,
                        env=git_env
                    )
                else:
                    # HTTPS with token
                    repo = git.Repo.clone_from(
                        clone_url, 
                        service_path, 
                        branch=branch
                    )
            
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
            logger.error("Possible causes:")
            logger.error("  - Repository is private and requires authentication")
            logger.error("  - Invalid credentials (check GIT_AUTH_TOKEN or SSH key)")
            logger.error("  - Repository does not exist")
            logger.error("  - Network connection issues")
            return None
        except Exception as e:
            logger.error(f"Error discovering service: {e}")
            return None
    
    def _prepare_authenticated_url(self, repo_url: str) -> str:
        """Prepare repository URL with authentication for HTTPS.
        
        Args:
            repo_url: Original repository URL
            
        Returns:
            URL with authentication token embedded (for HTTPS)
        """
        # SSH URLs don't need token authentication
        if repo_url.startswith("git@"):
            return repo_url
        
        # No token provided, return original URL
        if not self.auth_token:
            return repo_url
        
        # Inject token into HTTPS URL
        # From: https://github.com/user/repo.git
        # To:   https://token@github.com/user/repo.git
        if repo_url.startswith("https://"):
            # GitHub/GitLab/Bitbucket support this format
            return repo_url.replace("https://", f"https://{self.auth_token}@")
        
        return repo_url
    
    def _prepare_git_environment(self) -> Dict[str, str]:
        """Prepare Git environment variables for SSH authentication.
        
        Returns:
            Environment variables dictionary
        """
        env = {}
        
        # SSH key authentication
        if self.ssh_key_path:
            ssh_key = Path(self.ssh_key_path).expanduser()
            if ssh_key.exists():
                # Set GIT_SSH_COMMAND to use specific SSH key
                env['GIT_SSH_COMMAND'] = f'ssh -i {ssh_key} -o StrictHostKeyChecking=no'
                logger.debug(f"Using SSH key: {ssh_key}")
            else:
                logger.warning(f"SSH key not found: {ssh_key}")
        
        return env
    
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
