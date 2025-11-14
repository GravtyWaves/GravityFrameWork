"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/git/commit_manager.py
PURPOSE: Smart commit management and auto-commit
DESCRIPTION: Intelligently categorizes changes, generates commit messages, and
             handles automatic commits when file count exceeds threshold.

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
from collections import defaultdict
import logging
import re

logger = logging.getLogger(__name__)


class CommitManager:
    """
    Intelligent commit management with automatic file grouping.
    
    This class:
    1. Groups changed files by category (features, fixes, refactoring, etc.)
    2. Creates separate commits for each logical group
    3. Generates appropriate commit messages
    4. Pushes commits to remote
    
    All following TEAM_PROMPT.md standards.
    """
    
    def __init__(self, git_integration, ai_assistant=None):
        """
        Initialize commit manager.
        
        Args:
            git_integration: GitIntegration instance
            ai_assistant: AI assistant for intelligent grouping
        """
        self.git = git_integration
        self.ai = ai_assistant
    
    def analyze_changes(self) -> Dict[str, Any]:
        """
        Analyze all changed files and group them logically.
        
        Groups files by:
        - Feature additions (new functionality)
        - Bug fixes (corrections)
        - Refactoring (code improvements)
        - Documentation (docs, README)
        - Tests (test files)
        - Configuration (config files)
        - Infrastructure (Docker, CI/CD)
        
        Returns:
            Dictionary with:
            - groups: Dict of categorized files
            - summary: Summary of changes
            - recommendations: Commit recommendations
        """
        # Get Git status
        status = self.git.get_status()
        
        all_files = (
            status['staged'] + 
            status['unstaged'] + 
            status['untracked']
        )
        
        if not all_files:
            return {
                'groups': {},
                'summary': 'No changes to commit',
                'recommendations': []
            }
        
        # Categorize files
        groups = self._categorize_files(all_files)
        
        # Generate summary
        summary = self._generate_summary(groups)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(groups)
        
        return {
            'groups': groups,
            'summary': summary,
            'recommendations': recommendations,
            'total_files': len(all_files)
        }
    
    def _categorize_files(self, files: List[str]) -> Dict[str, List[str]]:
        """
        Categorize files into logical groups.
        
        Args:
            files: List of file paths
            
        Returns:
            Dictionary with categorized files
        """
        groups = defaultdict(list)
        
        for file_path in files:
            path = Path(file_path)
            
            # Determine category
            category = self._determine_category(path)
            groups[category].append(file_path)
        
        return dict(groups)
    
    def _determine_category(self, path: Path) -> str:
        """
        Determine file category based on path and content.
        
        Args:
            path: File path
            
        Returns:
            Category name
        """
        path_str = str(path).lower()
        
        # Test files
        if 'test' in path_str or path.name.startswith('test_'):
            return 'tests'
        
        # Documentation
        if path.suffix in ['.md', '.rst', '.txt']:
            if 'readme' in path_str:
                return 'docs-readme'
            return 'docs'
        
        # Configuration
        if path.name in [
            '.env', '.env.example', 'config.py', 'settings.py',
            'pyproject.toml', 'requirements.txt', 'setup.py'
        ]:
            return 'config'
        
        # Infrastructure
        if path.name in ['Dockerfile', 'docker-compose.yml', '.dockerignore']:
            return 'infrastructure-docker'
        
        if '.github' in path_str or '.gitlab' in path_str:
            return 'infrastructure-cicd'
        
        if 'nginx' in path_str or 'monitoring' in path_str:
            return 'infrastructure-deployment'
        
        # AI/ML files
        if 'ai' in path_str or 'ml' in path_str:
            return 'features-ai'
        
        # Git integration
        if 'git' in path_str and path.suffix == '.py':
            return 'features-git'
        
        # DevOps automation
        if 'devops' in path_str:
            return 'features-devops'
        
        # Core framework
        if 'core' in path_str or 'framework' in path_str:
            return 'core'
        
        # Database related
        if 'database' in path_str or 'models' in path_str:
            return 'features-database'
        
        # API files
        if 'api' in path_str or 'routes' in path_str:
            return 'features-api'
        
        # Services
        if 'service' in path_str:
            return 'features-services'
        
        # Examples
        if 'example' in path_str:
            return 'examples'
        
        # Python source files (general)
        if path.suffix == '.py':
            return 'features-general'
        
        # Other
        return 'other'
    
    def _generate_summary(self, groups: Dict[str, List[str]]) -> str:
        """
        Generate summary of changes.
        
        Args:
            groups: Categorized files
            
        Returns:
            Summary string
        """
        lines = ["Changes Summary:", ""]
        
        for category, files in sorted(groups.items()):
            lines.append(f"• {category}: {len(files)} files")
        
        lines.append("")
        lines.append(f"Total: {sum(len(f) for f in groups.values())} files")
        
        return "\n".join(lines)
    
    def _generate_recommendations(
        self, 
        groups: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """
        Generate commit recommendations.
        
        Args:
            groups: Categorized files
            
        Returns:
            List of commit recommendations
        """
        recommendations = []
        
        # Map categories to commit types
        category_to_type = {
            'features-ai': ('feat', 'ai', 'AI integration and intelligent features'),
            'features-git': ('feat', 'git', 'Git integration and automation'),
            'features-devops': ('feat', 'devops', 'DevOps automation'),
            'features-database': ('feat', 'database', 'database orchestration'),
            'features-api': ('feat', 'api', 'API endpoints'),
            'features-services': ('feat', 'services', 'service implementation'),
            'features-general': ('feat', 'core', 'core functionality'),
            'tests': ('test', 'tests', 'test coverage and validation'),
            'docs': ('docs', 'docs', 'documentation updates'),
            'docs-readme': ('docs', 'readme', 'README and guides'),
            'config': ('chore', 'config', 'configuration updates'),
            'infrastructure-docker': ('chore', 'docker', 'Docker infrastructure'),
            'infrastructure-cicd': ('chore', 'cicd', 'CI/CD pipeline'),
            'infrastructure-deployment': ('chore', 'deploy', 'deployment infrastructure'),
            'core': ('refactor', 'core', 'core framework'),
            'examples': ('docs', 'examples', 'example code and demos'),
        }
        
        for category, files in sorted(groups.items()):
            if category not in category_to_type:
                commit_type = 'chore'
                scope = 'misc'
                description = category.replace('-', ' ')
            else:
                commit_type, scope, description = category_to_type[category]
            
            recommendations.append({
                'category': category,
                'files': files,
                'commit_type': commit_type,
                'scope': scope,
                'description': description,
                'suggested_message': f"{commit_type}({scope}): add {description}"
            })
        
        return recommendations
    
    def create_organized_commits(
        self,
        auto_generate_messages: bool = True,
        push_after_commit: bool = False
    ) -> Dict[str, Any]:
        """
        Create organized commits based on file categories.
        
        Process:
        1. Analyze and group changed files
        2. Create separate commit for each logical group
        3. Generate appropriate commit messages (with AI)
        4. Optionally push commits to remote
        
        Args:
            auto_generate_messages: Use AI to generate commit messages
            push_after_commit: Push commits after creating them
            
        Returns:
            Dictionary with commit results
        """
        logger.info("Analyzing changes for organized commits...")
        
        # Analyze changes
        analysis = self.analyze_changes()
        
        if not analysis['groups']:
            return {
                'success': True,
                'message': 'No changes to commit',
                'commits': []
            }
        
        logger.info(f"\n{analysis['summary']}\n")
        
        # Create commits
        commits = []
        failed_commits = []
        
        for recommendation in analysis['recommendations']:
            category = recommendation['category']
            files = recommendation['files']
            
            logger.info(f"Creating commit for: {category} ({len(files)} files)")
            
            # Generate commit message
            if auto_generate_messages and self.ai:
                message = self._generate_intelligent_message(
                    recommendation, 
                    files
                )
            else:
                message = recommendation['suggested_message']
            
            # Create commit
            try:
                # Stage files
                for file in files:
                    self.git.run_git_command(['git', 'add', file])
                
                # Run pre-commit checks
                checks = self.git.pre_commit_checks()
                
                if not checks['passed']:
                    logger.warning(f"Pre-commit checks failed for {category}")
                    
                    # Try auto-fix
                    self.git._auto_fix_issues(checks['results'])
                    
                    # Re-run checks
                    checks = self.git.pre_commit_checks()
                    
                    if not checks['passed']:
                        failed_commits.append({
                            'category': category,
                            'files': files,
                            'error': 'Pre-commit checks failed',
                            'checks': checks
                        })
                        continue
                
                # Create commit
                result = self.git.run_git_command(['git', 'commit', '-m', message])
                
                commit_hash = self.git._get_last_commit_hash()
                
                commits.append({
                    'category': category,
                    'files': files,
                    'message': message,
                    'hash': commit_hash,
                    'success': True
                })
                
                logger.info(f"✅ Committed: {message}")
                
            except Exception as e:
                logger.error(f"Failed to commit {category}: {e}")
                failed_commits.append({
                    'category': category,
                    'files': files,
                    'error': str(e)
                })
        
        # Push commits if requested
        push_result = None
        if push_after_commit and commits:
            logger.info("Pushing commits to remote...")
            push_result = self._push_commits()
        
        return {
            'success': len(failed_commits) == 0,
            'commits': commits,
            'failed_commits': failed_commits,
            'total_commits': len(commits),
            'push_result': push_result
        }
    
    def _generate_intelligent_message(
        self,
        recommendation: Dict[str, Any],
        files: List[str]
    ) -> str:
        """
        Generate intelligent commit message using AI.
        
        Args:
            recommendation: Commit recommendation
            files: Files to commit
            
        Returns:
            Generated commit message
        """
        # Get diff for these files
        diff_parts = []
        for file in files[:5]:  # Limit to first 5 files
            try:
                result = self.git.run_git_command(
                    ['git', 'diff', '--cached', file],
                    check=False
                )
                if result.stdout:
                    diff_parts.append(f"File: {file}\n{result.stdout[:500]}")
            except:
                pass
        
        diff_content = "\n\n".join(diff_parts)
        
        prompt = f"""
        Generate a commit message for these changes.
        
        REQUIREMENTS (from TEAM_PROMPT.md):
        1. Format: {recommendation['commit_type']}({recommendation['scope']}): <subject>
        2. Subject in lowercase after colon
        3. No trailing period
        4. Max 72 characters
        5. English only
        
        Category: {recommendation['category']}
        Files: {len(files)} files
        Suggested description: {recommendation['description']}
        
        Sample diff:
        {diff_content[:1000]}
        
        Generate ONLY the commit message (one line). No explanation.
        """
        
        message = self.ai.query(prompt).strip()
        
        # Validate and fix if needed
        is_valid, errors = self.git.validate_commit_message(message)
        if not is_valid:
            message = self.git._fix_commit_message(message)
        
        return message
    
    def _push_commits(self) -> Dict[str, Any]:
        """
        Push commits to remote repository.
        
        Returns:
            Push results
        """
        try:
            # Get current branch
            branch_result = self.git.run_git_command(
                ['git', 'branch', '--show-current']
            )
            branch = branch_result.stdout.strip()
            
            logger.info(f"Pushing to origin/{branch}...")
            
            # Push commits
            push_result = self.git.run_git_command(
                ['git', 'push', 'origin', branch]
            )
            
            logger.info("✅ Pushed successfully!")
            
            return {
                'success': True,
                'branch': branch,
                'output': push_result.stdout
            }
            
        except Exception as e:
            logger.error(f"Push failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def smart_commit_and_push(
        self,
        batch_size: int = 5,
        auto_generate: bool = True
    ) -> Dict[str, Any]:
        """
        Smart commit and push workflow.
        
        This is the complete workflow:
        1. Analyze all changes
        2. Group files logically
        3. Create organized commits
        4. Push to remote
        
        Args:
            batch_size: Max files per commit
            auto_generate: Use AI for commit messages
            
        Returns:
            Complete workflow results
        """
        logger.info("=" * 80)
        logger.info("SMART COMMIT & PUSH WORKFLOW")
        logger.info("=" * 80)
        logger.info("")
        
        # Step 1: Analyze
        logger.info("Step 1: Analyzing changes...")
        analysis = self.analyze_changes()
        
        if not analysis['groups']:
            return {
                'success': True,
                'message': 'No changes to commit'
            }
        
        logger.info(f"\n{analysis['summary']}\n")
        
        # Step 2: Create commits
        logger.info("Step 2: Creating organized commits...")
        result = self.create_organized_commits(
            auto_generate_messages=auto_generate,
            push_after_commit=False  # We'll push separately
        )
        
        if not result['commits']:
            return {
                'success': False,
                'message': 'No commits created',
                'result': result
            }
        
        logger.info(f"\n✅ Created {result['total_commits']} commits\n")
        
        # Step 3: Push
        logger.info("Step 3: Pushing commits to remote...")
        push_result = self._push_commits()
        
        if push_result['success']:
            logger.info("\n✅ All commits pushed successfully!\n")
        else:
            logger.error(f"\n❌ Push failed: {push_result['error']}\n")
        
        logger.info("=" * 80)
        
        return {
            'success': result['success'] and push_result['success'],
            'analysis': analysis,
            'commits': result,
            'push': push_result,
            'summary': self._generate_workflow_summary(
                analysis, 
                result, 
                push_result
            )
        }
    
    def _generate_workflow_summary(
        self,
        analysis: Dict[str, Any],
        commits: Dict[str, Any],
        push: Dict[str, Any]
    ) -> str:
        """Generate workflow summary."""
        lines = [
            "WORKFLOW SUMMARY",
            "=" * 80,
            "",
            f"Files analyzed: {analysis['total_files']}",
            f"Commits created: {commits['total_commits']}",
            f"Commits failed: {len(commits['failed_commits'])}",
            f"Push status: {'✅ Success' if push['success'] else '❌ Failed'}",
            "",
            "Commits created:",
        ]
        
        for commit in commits['commits']:
            lines.append(f"  • {commit['hash'][:8]} - {commit['message']}")
        
        if commits['failed_commits']:
            lines.append("")
            lines.append("Failed commits:")
            for failed in commits['failed_commits']:
                lines.append(f"  • {failed['category']}: {failed['error']}")
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)


class AutoCommitScheduler:
    """
    Automatic commit scheduling based on file count threshold.
    
    As per TEAM_PROMPT.md:
    "Commit and push every 100 file changes"
    """
    
    def __init__(self, commit_manager: CommitManager, threshold: int = 100):
        """
        Initialize auto-commit scheduler.
        
        Args:
            commit_manager: CommitManager instance
            threshold: File change threshold (default: 100)
        """
        self.manager = commit_manager
        self.threshold = threshold
        self._file_count = 0
    
    def check_and_commit(self) -> Optional[Dict[str, Any]]:
        """
        Check if threshold reached and auto-commit if needed.
        
        Returns:
            Commit results if threshold reached, None otherwise
        """
        # Get current file count
        analysis = self.manager.analyze_changes()
        total_files = analysis.get('total_files', 0)
        
        if total_files >= self.threshold:
            logger.info(f"⚠️  Threshold reached: {total_files} files changed")
            logger.info("Starting automatic commit and push...")
            
            result = self.manager.smart_commit_and_push()
            
            self._file_count = 0  # Reset counter
            
            return result
        else:
            logger.info(f"File count: {total_files}/{self.threshold}")
            return None
    
    def force_commit(self) -> Dict[str, Any]:
        """Force commit regardless of threshold."""
        return self.manager.smart_commit_and_push()
