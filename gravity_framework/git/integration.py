"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/git/integration.py
PURPOSE: Git and GitHub integration
DESCRIPTION: Handles Git operations and GitHub API integration for repository
             management and service discovery.

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
import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GitIntegration:
    """
    Intelligent Git integration with automatic standards enforcement.
    
    This class ensures all Git operations follow TEAM_PROMPT.md standards:
    - Conventional Commits format
    - English-only messages
    - Code quality validation
    - Automated testing before commit
    """
    
    def __init__(self, repo_path: Path, ai_assistant=None):
        """
        Initialize Git integration.
        
        Args:
            repo_path: Path to the Git repository
            ai_assistant: AI assistant instance for intelligent operations
        """
        self.repo_path = Path(repo_path)
        self.ai = ai_assistant
        
        # Validate Git repository
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Not a Git repository: {repo_path}")
    
    def run_git_command(
        self, 
        command: List[str], 
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Run a Git command in the repository.
        
        Args:
            command: Git command as list (e.g., ['git', 'status'])
            check: Whether to raise exception on non-zero exit code
            
        Returns:
            CompletedProcess instance with command results
        """
        try:
            result = subprocess.run(
                command,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(command)}")
            logger.error(f"Error: {e.stderr}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current Git status.
        
        Returns:
            Dictionary with:
            - branch: Current branch name
            - staged: List of staged files
            - unstaged: List of unstaged files
            - untracked: List of untracked files
        """
        # Get branch name
        branch_result = self.run_git_command(['git', 'branch', '--show-current'])
        branch = branch_result.stdout.strip()
        
        # Get status
        status_result = self.run_git_command(['git', 'status', '--porcelain'])
        
        staged = []
        unstaged = []
        untracked = []
        
        for line in status_result.stdout.splitlines():
            if not line:
                continue
            
            status = line[:2]
            filepath = line[3:]
            
            if status[0] != ' ' and status[0] != '?':
                staged.append(filepath)
            if status[1] != ' ' and status[1] != '?':
                unstaged.append(filepath)
            if status.startswith('??'):
                untracked.append(filepath)
        
        return {
            'branch': branch,
            'staged': staged,
            'unstaged': unstaged,
            'untracked': untracked
        }
    
    def validate_commit_message(self, message: str) -> Tuple[bool, List[str]]:
        """
        Validate commit message follows TEAM_PROMPT standards.
        
        Standards checked:
        - English language only
        - Conventional Commits format
        - No trailing period
        - Proper capitalization
        
        Args:
            message: Commit message to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if message is empty
        if not message or not message.strip():
            errors.append("Commit message cannot be empty")
            return False, errors
        
        lines = message.strip().split('\n')
        subject = lines[0]
        
        # Check for non-English characters (Persian, Arabic, etc.)
        # Allow only ASCII + common punctuation
        if not all(ord(char) < 128 or char in '(),:;-_' for char in subject):
            errors.append("Commit message must be in ENGLISH only (no Persian/Arabic)")
        
        # Check Conventional Commits format
        # Format: type(scope): subject
        conventional_pattern = r'^(feat|fix|refactor|docs|test|chore|style|perf)(\([a-z0-9\-]+\))?: .+'
        if not re.match(conventional_pattern, subject):
            errors.append(
                "Must follow Conventional Commits format: "
                "type(scope): subject\n"
                "Valid types: feat, fix, refactor, docs, test, chore, style, perf"
            )
        
        # Check for trailing period
        if subject.endswith('.'):
            errors.append("Subject line should not end with a period")
        
        # Check subject line length (recommended: 50-72 characters)
        if len(subject) > 72:
            errors.append("Subject line too long (max 72 characters)")
        
        # Check capitalization after colon
        match = re.match(r'^[a-z]+(\([a-z0-9\-]+\))?: (.+)', subject)
        if match:
            description = match.group(2)
            if description and description[0].isupper():
                errors.append("Description after colon should start with lowercase")
        
        return len(errors) == 0, errors
    
    def generate_commit_message(
        self, 
        files: Optional[List[str]] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Generate intelligent commit message using AI.
        
        AI analyzes the changes and generates a commit message that:
        - Follows Conventional Commits format
        - Is in English
        - Accurately describes the changes
        - Includes proper type and scope
        
        Args:
            files: List of files to analyze (default: all staged files)
            context: Optional context about the changes
            
        Returns:
            Generated commit message
        """
        if not self.ai:
            raise ValueError("AI assistant required for commit message generation")
        
        # Get changed files if not provided
        if files is None:
            status = self.get_status()
            files = status['staged']
        
        if not files:
            raise ValueError("No files to commit")
        
        # Get diff for analysis
        diff_result = self.run_git_command(
            ['git', 'diff', '--cached'] if files else ['git', 'diff']
        )
        diff_content = diff_result.stdout
        
        # Use AI to generate commit message
        prompt = f"""
        Analyze the following Git diff and generate a commit message.
        
        CRITICAL REQUIREMENTS (from TEAM_PROMPT.md):
        1. MUST be in ENGLISH only
        2. MUST follow Conventional Commits format: type(scope): subject
        3. Valid types: feat, fix, refactor, docs, test, chore, style, perf
        4. Subject must start with lowercase after colon
        5. No trailing period
        6. Max 72 characters for subject line
        
        Files changed:
        {', '.join(files)}
        
        {'Context: ' + context if context else ''}
        
        Git diff:
        {diff_content[:2000]}  # Limit diff size
        
        Generate ONLY the commit message (subject line). No explanation.
        """
        
        message = self.ai.query(prompt)
        
        # Validate generated message
        is_valid, errors = self.validate_commit_message(message)
        if not is_valid:
            logger.warning(f"AI generated invalid commit message: {errors}")
            # Try to fix common issues
            message = self._fix_commit_message(message)
        
        return message.strip()
    
    def _fix_commit_message(self, message: str) -> str:
        """
        Attempt to fix common commit message issues.
        
        Args:
            message: Original commit message
            
        Returns:
            Fixed commit message
        """
        # Remove trailing period
        if message.endswith('.'):
            message = message[:-1]
        
        # Ensure lowercase after colon
        match = re.match(r'^([a-z]+(\([a-z0-9\-]+\))?): (.+)', message)
        if match:
            prefix = match.group(1)
            description = match.group(3)
            if description and description[0].isupper():
                description = description[0].lower() + description[1:]
            message = f"{prefix}: {description}"
        
        return message
    
    def pre_commit_checks(self) -> Dict[str, Any]:
        """
        Run comprehensive pre-commit checks (TEAM_PROMPT standards).
        
        Checks performed:
        1. Code quality (linting)
        2. Type hints validation
        3. Tests execution
        4. Test coverage (min 95%)
        5. Security scan
        6. No hardcoded secrets
        
        Returns:
            Dictionary with check results:
            - passed: Boolean indicating if all checks passed
            - results: Dict of individual check results
        """
        results = {}
        all_passed = True
        
        logger.info("Running pre-commit checks...")
        
        # 1. Check for Python files
        python_files = self._get_python_files()
        if not python_files:
            logger.info("No Python files to check")
            return {'passed': True, 'results': {}}
        
        # 2. Code formatting (Black)
        logger.info("Checking code formatting...")
        black_result = self.run_git_command(
            ['black', '--check', '.'],
            check=False
        )
        results['formatting'] = {
            'passed': black_result.returncode == 0,
            'message': 'Code formatting OK' if black_result.returncode == 0 
                      else 'Code needs formatting (run: black .)'
        }
        if black_result.returncode != 0:
            all_passed = False
        
        # 3. Import sorting (isort)
        logger.info("Checking import sorting...")
        isort_result = self.run_git_command(
            ['isort', '--check-only', '.'],
            check=False
        )
        results['imports'] = {
            'passed': isort_result.returncode == 0,
            'message': 'Import sorting OK' if isort_result.returncode == 0
                      else 'Imports need sorting (run: isort .)'
        }
        if isort_result.returncode != 0:
            all_passed = False
        
        # 4. Type checking (mypy)
        logger.info("Checking type hints...")
        mypy_result = self.run_git_command(
            ['mypy', '.'],
            check=False
        )
        results['type_hints'] = {
            'passed': mypy_result.returncode == 0,
            'message': 'Type hints OK' if mypy_result.returncode == 0
                      else f'Type hint issues:\n{mypy_result.stdout}'
        }
        if mypy_result.returncode != 0:
            all_passed = False
        
        # 5. Run tests
        logger.info("Running tests...")
        test_result = self.run_git_command(
            ['pytest', 'tests/', '-v', '--cov=.', '--cov-report=term'],
            check=False
        )
        
        # Extract coverage from output
        coverage_match = re.search(r'TOTAL.*?(\d+)%', test_result.stdout)
        coverage = int(coverage_match.group(1)) if coverage_match else 0
        
        results['tests'] = {
            'passed': test_result.returncode == 0 and coverage >= 95,
            'coverage': coverage,
            'message': f'Tests passed, coverage: {coverage}%' 
                      if test_result.returncode == 0 and coverage >= 95
                      else f'Tests failed or coverage < 95% (current: {coverage}%)'
        }
        if test_result.returncode != 0 or coverage < 95:
            all_passed = False
        
        # 6. Security scan (bandit)
        logger.info("Running security scan...")
        bandit_result = self.run_git_command(
            ['bandit', '-r', '.', '-f', 'json'],
            check=False
        )
        results['security'] = {
            'passed': bandit_result.returncode == 0,
            'message': 'Security scan OK' if bandit_result.returncode == 0
                      else 'Security issues found'
        }
        if bandit_result.returncode != 0:
            all_passed = False
        
        # 7. Check for secrets (basic regex patterns)
        logger.info("Checking for hardcoded secrets...")
        secrets_found = self._check_for_secrets()
        results['secrets'] = {
            'passed': not secrets_found,
            'message': 'No secrets found' if not secrets_found
                      else f'Hardcoded secrets detected: {secrets_found}'
        }
        if secrets_found:
            all_passed = False
        
        return {
            'passed': all_passed,
            'results': results
        }
    
    def _get_python_files(self) -> List[str]:
        """Get list of Python files in repository."""
        result = self.run_git_command(['git', 'ls-files', '*.py'])
        return [f for f in result.stdout.splitlines() if f]
    
    def _check_for_secrets(self) -> List[str]:
        """
        Check for hardcoded secrets in staged files.
        
        Returns:
            List of files containing potential secrets
        """
        # Common secret patterns
        patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        
        status = self.get_status()
        files_with_secrets = []
        
        for file in status['staged']:
            if not file.endswith('.py'):
                continue
            
            try:
                with open(self.repo_path / file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            files_with_secrets.append(file)
                            break
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")
        
        return files_with_secrets
    
    def smart_commit(
        self, 
        message: Optional[str] = None,
        files: Optional[List[str]] = None,
        auto_fix: bool = True,
        skip_checks: bool = False
    ) -> Dict[str, Any]:
        """
        Intelligent commit with automatic standards enforcement.
        
        Process:
        1. Stage files (if specified)
        2. Run pre-commit checks
        3. Auto-fix issues (if enabled)
        4. Generate/validate commit message
        5. Create commit
        
        Args:
            message: Commit message (will be generated if not provided)
            files: Files to commit (default: all staged files)
            auto_fix: Automatically fix code quality issues
            skip_checks: Skip pre-commit checks (NOT RECOMMENDED)
            
        Returns:
            Dictionary with commit results
        """
        # Stage files if specified
        if files:
            for file in files:
                self.run_git_command(['git', 'add', file])
        
        # Run pre-commit checks
        if not skip_checks:
            logger.info("Running pre-commit checks...")
            checks = self.pre_commit_checks()
            
            if not checks['passed']:
                if auto_fix:
                    logger.info("Attempting to auto-fix issues...")
                    self._auto_fix_issues(checks['results'])
                    
                    # Re-run checks
                    checks = self.pre_commit_checks()
                    if not checks['passed']:
                        return {
                            'success': False,
                            'error': 'Pre-commit checks failed even after auto-fix',
                            'checks': checks
                        }
                else:
                    return {
                        'success': False,
                        'error': 'Pre-commit checks failed',
                        'checks': checks
                    }
        
        # Generate or validate commit message
        if message is None:
            logger.info("Generating commit message with AI...")
            message = self.generate_commit_message(files)
        else:
            is_valid, errors = self.validate_commit_message(message)
            if not is_valid:
                return {
                    'success': False,
                    'error': 'Invalid commit message',
                    'validation_errors': errors
                }
        
        # Create commit
        logger.info(f"Creating commit: {message}")
        commit_result = self.run_git_command(['git', 'commit', '-m', message])
        
        return {
            'success': True,
            'message': message,
            'commit_hash': self._get_last_commit_hash(),
            'output': commit_result.stdout
        }
    
    def _auto_fix_issues(self, check_results: Dict[str, Any]):
        """
        Automatically fix code quality issues.
        
        Args:
            check_results: Results from pre_commit_checks()
        """
        # Fix formatting
        if not check_results.get('formatting', {}).get('passed'):
            logger.info("Auto-fixing code formatting...")
            self.run_git_command(['black', '.'])
        
        # Fix import sorting
        if not check_results.get('imports', {}).get('passed'):
            logger.info("Auto-fixing import sorting...")
            self.run_git_command(['isort', '.'])
    
    def _get_last_commit_hash(self) -> str:
        """Get hash of last commit."""
        result = self.run_git_command(['git', 'rev-parse', 'HEAD'])
        return result.stdout.strip()
    
    def create_branch(
        self, 
        branch_name: str, 
        branch_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new branch following naming conventions.
        
        Branch naming format: <type>/<short-description>
        Valid types: feature, fix, refactor, docs, test
        
        Args:
            branch_name: Branch name or description
            branch_type: Branch type (feature, fix, etc.)
            
        Returns:
            Dictionary with branch creation results
        """
        # Validate branch name is in English
        if not all(ord(char) < 128 or char in '-_/' for char in branch_name):
            return {
                'success': False,
                'error': 'Branch name must be in English only'
            }
        
        # Add type prefix if not present
        if branch_type and not branch_name.startswith(f"{branch_type}/"):
            branch_name = f"{branch_type}/{branch_name}"
        
        # Validate format
        valid_types = ['feature', 'fix', 'refactor', 'docs', 'test', 'chore']
        if '/' in branch_name:
            prefix = branch_name.split('/')[0]
            if prefix not in valid_types:
                return {
                    'success': False,
                    'error': f'Invalid branch type. Valid types: {", ".join(valid_types)}'
                }
        
        # Create branch
        logger.info(f"Creating branch: {branch_name}")
        self.run_git_command(['git', 'checkout', '-b', branch_name])
        
        return {
            'success': True,
            'branch': branch_name,
            'message': f'Branch {branch_name} created successfully'
        }


class GitHubIntegration:
    """
    GitHub-specific integration for pull requests, actions, etc.
    """
    
    def __init__(self, repo_path: Path, token: Optional[str] = None):
        """
        Initialize GitHub integration.
        
        Args:
            repo_path: Path to Git repository
            token: GitHub API token (or from environment)
        """
        self.repo_path = Path(repo_path)
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.git = GitIntegration(repo_path)
    
    def create_pull_request(
        self,
        title: str,
        body: str,
        base: str = 'main',
        head: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a pull request with AI-generated description.
        
        Args:
            title: PR title
            body: PR description
            base: Base branch (default: main)
            head: Head branch (default: current branch)
            
        Returns:
            Dictionary with PR creation results
        """
        # Implementation would use GitHub API
        # This is a placeholder for the actual implementation
        pass
