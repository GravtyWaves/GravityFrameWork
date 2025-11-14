"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_commit_manager.py
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
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from gravity_framework.git.commit_manager import CommitManager, AutoCommitScheduler


class TestCommitManager:
    """Test CommitManager class."""
    
    @pytest.fixture
    def mock_git(self):
        """Create mock Git integration."""
        git = Mock()
        git.get_status.return_value = {
            'staged': [],
            'unstaged': [],
            'untracked': []
        }
        git.run_git_command.return_value = Mock(stdout='', stderr='')
        git.pre_commit_checks.return_value = {
            'passed': True,
            'results': {}
        }
        return git
    
    @pytest.fixture
    def mock_ai(self):
        """Create mock AI assistant."""
        ai = Mock()
        ai.query.return_value = "feat(test): add test feature"
        return ai
    
    @pytest.fixture
    def manager(self, mock_git, mock_ai):
        """Create CommitManager instance."""
        return CommitManager(mock_git, mock_ai)
    
    def test_analyze_no_changes(self, manager, mock_git):
        """Test analyze_changes with no changes."""
        result = manager.analyze_changes()
        
        assert result['groups'] == {}
        assert result['summary'] == 'No changes to commit'
        assert result['recommendations'] == []
        assert result['total_files'] == 0
    
    def test_analyze_with_changes(self, manager, mock_git):
        """Test analyze_changes with various file types."""
        mock_git.get_status.return_value = {
            'staged': [
                'gravity_framework/ai/team_generator.py',
                'gravity_framework/git/integration.py'
            ],
            'unstaged': [
                'tests/test_git.py',
                'docs/README.md'
            ],
            'untracked': [
                'examples/example.py'
            ]
        }
        
        result = manager.analyze_changes()
        
        assert result['total_files'] == 5
        assert 'groups' in result
        assert 'summary' in result
        assert 'recommendations' in result
        
        # Check groups
        groups = result['groups']
        assert 'features-ai' in groups
        assert 'features-git' in groups
        assert 'tests' in groups
        assert 'docs-readme' in groups
        assert 'examples' in groups
    
    def test_categorize_feature_files(self, manager):
        """Test categorization of feature files."""
        files = [
            'gravity_framework/ai/assistant.py',
            'gravity_framework/git/commit_manager.py',
            'gravity_framework/devops/automation.py',
            'gravity_framework/database/orchestrator.py'
        ]
        
        groups = manager._categorize_files(files)
        
        assert 'features-ai' in groups
        assert 'features-git' in groups
        assert 'features-devops' in groups
        assert 'features-database' in groups
    
    def test_categorize_test_files(self, manager):
        """Test categorization of test files."""
        files = [
            'tests/test_git.py',
            'tests/test_framework.py',
            'gravity_framework/test_helper.py'
        ]
        
        groups = manager._categorize_files(files)
        
        assert 'tests' in groups
        assert len(groups['tests']) == 3
    
    def test_categorize_doc_files(self, manager):
        """Test categorization of documentation files."""
        files = [
            'README.md',
            'QUICKSTART.md',
            'docs/GUIDE.md',
            'CHANGELOG.md'
        ]
        
        groups = manager._categorize_files(files)
        
        assert 'docs-readme' in groups
        assert 'docs' in groups
    
    def test_categorize_config_files(self, manager):
        """Test categorization of config files."""
        files = [
            'pyproject.toml',
            'requirements.txt',
            'setup.py',
            'config.py'
        ]
        
        groups = manager._categorize_files(files)
        
        assert 'config' in groups
        assert len(groups['config']) == 4
    
    def test_categorize_infrastructure_files(self, manager):
        """Test categorization of infrastructure files."""
        files = [
            'Dockerfile',
            'docker-compose.yml',
            '.github/workflows/test.yml',
            'nginx/nginx.conf'
        ]
        
        groups = manager._categorize_files(files)
        
        assert 'infrastructure-docker' in groups
        assert 'infrastructure-cicd' in groups
        assert 'infrastructure-deployment' in groups
    
    def test_generate_summary(self, manager):
        """Test summary generation."""
        groups = {
            'features-ai': ['file1.py', 'file2.py'],
            'tests': ['test1.py'],
            'docs': ['doc1.md']
        }
        
        summary = manager._generate_summary(groups)
        
        assert 'features-ai: 2 files' in summary
        assert 'tests: 1 files' in summary
        assert 'docs: 1 files' in summary
        assert 'Total: 4 files' in summary
    
    def test_generate_recommendations(self, manager):
        """Test recommendation generation."""
        groups = {
            'features-ai': ['ai.py'],
            'tests': ['test.py'],
            'docs': ['doc.md']
        }
        
        recommendations = manager._generate_recommendations(groups)
        
        assert len(recommendations) == 3
        
        # Check AI recommendation
        ai_rec = next(r for r in recommendations if r['category'] == 'features-ai')
        assert ai_rec['commit_type'] == 'feat'
        assert ai_rec['scope'] == 'ai'
        assert 'feat(ai)' in ai_rec['suggested_message']
        
        # Check test recommendation
        test_rec = next(r for r in recommendations if r['category'] == 'tests')
        assert test_rec['commit_type'] == 'test'
        assert test_rec['scope'] == 'tests'
        
        # Check docs recommendation
        docs_rec = next(r for r in recommendations if r['category'] == 'docs')
        assert docs_rec['commit_type'] == 'docs'
        assert docs_rec['scope'] == 'docs'
    
    def test_create_organized_commits_no_changes(self, manager, mock_git):
        """Test create_organized_commits with no changes."""
        result = manager.create_organized_commits()
        
        assert result['success'] is True
        assert result['message'] == 'No changes to commit'
        assert result['commits'] == []
    
    def test_create_organized_commits_success(self, manager, mock_git, mock_ai):
        """Test create_organized_commits with successful commits."""
        mock_git.get_status.return_value = {
            'staged': [],
            'unstaged': ['file1.py', 'file2.py'],
            'untracked': []
        }
        mock_git._get_last_commit_hash.return_value = 'abc123def456'
        
        result = manager.create_organized_commits(
            auto_generate_messages=False,
            push_after_commit=False
        )
        
        assert result['success'] is True
        assert result['total_commits'] > 0
        assert len(result['commits']) > 0
        assert len(result['failed_commits']) == 0
    
    def test_generate_intelligent_message(self, manager, mock_git, mock_ai):
        """Test intelligent message generation."""
        recommendation = {
            'commit_type': 'feat',
            'scope': 'ai',
            'description': 'AI features',
            'category': 'features-ai'
        }
        files = ['ai.py']
        
        mock_git.run_git_command.return_value = Mock(stdout='+ new code')
        mock_git.validate_commit_message.return_value = (True, [])
        
        message = manager._generate_intelligent_message(recommendation, files)
        
        assert isinstance(message, str)
        assert len(message) > 0
        mock_ai.query.assert_called_once()
    
    def test_push_commits_success(self, manager, mock_git):
        """Test successful push."""
        mock_git.run_git_command.side_effect = [
            Mock(stdout='main\n'),  # branch name
            Mock(stdout='Pushed successfully')  # push result
        ]
        
        result = manager._push_commits()
        
        assert result['success'] is True
        assert result['branch'] == 'main'
        assert 'output' in result
    
    def test_push_commits_failure(self, manager, mock_git):
        """Test failed push."""
        mock_git.run_git_command.side_effect = Exception("Push failed")
        
        result = manager._push_commits()
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_smart_commit_and_push(self, manager, mock_git, mock_ai):
        """Test complete smart commit and push workflow."""
        mock_git.get_status.return_value = {
            'staged': [],
            'unstaged': ['file1.py'],
            'untracked': []
        }
        mock_git._get_last_commit_hash.return_value = 'abc123'
        mock_git.run_git_command.side_effect = [
            Mock(stdout=''),  # git add
            Mock(stdout='main\n'),  # branch name
            Mock(stdout='Pushed')  # push
        ]
        
        result = manager.smart_commit_and_push(auto_generate=False)
        
        assert 'success' in result
        assert 'analysis' in result
        assert 'commits' in result
        assert 'push' in result
        assert 'summary' in result


class TestAutoCommitScheduler:
    """Test AutoCommitScheduler class."""
    
    @pytest.fixture
    def mock_manager(self):
        """Create mock CommitManager."""
        manager = Mock()
        manager.analyze_changes.return_value = {'total_files': 0}
        manager.smart_commit_and_push.return_value = {
            'success': True,
            'summary': 'Test summary'
        }
        return manager
    
    @pytest.fixture
    def scheduler(self, mock_manager):
        """Create AutoCommitScheduler instance."""
        return AutoCommitScheduler(mock_manager, threshold=100)
    
    def test_check_below_threshold(self, scheduler, mock_manager):
        """Test check when below threshold."""
        mock_manager.analyze_changes.return_value = {'total_files': 50}
        
        result = scheduler.check_and_commit()
        
        assert result is None
        mock_manager.smart_commit_and_push.assert_not_called()
    
    def test_check_at_threshold(self, scheduler, mock_manager):
        """Test check when at threshold."""
        mock_manager.analyze_changes.return_value = {'total_files': 100}
        
        result = scheduler.check_and_commit()
        
        assert result is not None
        assert result['success'] is True
        mock_manager.smart_commit_and_push.assert_called_once()
    
    def test_check_above_threshold(self, scheduler, mock_manager):
        """Test check when above threshold."""
        mock_manager.analyze_changes.return_value = {'total_files': 150}
        
        result = scheduler.check_and_commit()
        
        assert result is not None
        mock_manager.smart_commit_and_push.assert_called_once()
    
    def test_force_commit(self, scheduler, mock_manager):
        """Test force commit regardless of threshold."""
        mock_manager.analyze_changes.return_value = {'total_files': 10}
        
        result = scheduler.force_commit()
        
        assert result is not None
        assert result['success'] is True
        mock_manager.smart_commit_and_push.assert_called_once()
    
    def test_custom_threshold(self, mock_manager):
        """Test custom threshold value."""
        scheduler = AutoCommitScheduler(mock_manager, threshold=50)
        mock_manager.analyze_changes.return_value = {'total_files': 50}
        
        result = scheduler.check_and_commit()
        
        assert result is not None
        mock_manager.smart_commit_and_push.assert_called_once()
    
    def test_counter_reset(self, scheduler, mock_manager):
        """Test file counter resets after commit."""
        mock_manager.analyze_changes.return_value = {'total_files': 100}
        
        # First check - should commit
        result1 = scheduler.check_and_commit()
        assert result1 is not None
        
        # Counter should be reset
        assert scheduler._file_count == 0


class TestIntegration:
    """Integration tests for commit management."""
    
    def test_complete_workflow(self):
        """Test complete commit management workflow."""
        # This would be a full integration test
        # Requires actual Git repository
        pass
    
    def test_categorization_accuracy(self):
        """Test categorization accuracy with real file paths."""
        git = Mock()
        git.get_status.return_value = {
            'staged': [],
            'unstaged': [],
            'untracked': []
        }
        
        manager = CommitManager(git)
        
        test_files = [
            ('gravity_framework/ai/assistant.py', 'features-ai'),
            ('tests/test_ai.py', 'tests'),
            ('README.md', 'docs-readme'),
            ('Dockerfile', 'infrastructure-docker'),
            ('.github/workflows/test.yml', 'infrastructure-cicd'),
            ('pyproject.toml', 'config'),
        ]
        
        for file_path, expected_category in test_files:
            path = Path(file_path)
            category = manager._determine_category(path)
            assert category == expected_category, \
                f"File {file_path} should be {expected_category}, got {category}"
