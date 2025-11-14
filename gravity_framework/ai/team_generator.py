"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/ai/team_generator.py
PURPOSE: Dynamic AI team generation for projects
DESCRIPTION: Generates project-specific AI expert teams based on project requirements
             and technology stack.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""


from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DynamicTeamGenerator:
    """
    Generate custom expert teams based on project requirements.
    
    This class analyzes project descriptions and creates tailored
    AI team profiles with relevant expertise for the specific domain.
    """
    
    def __init__(self, ai_assistant):
        """
        Initialize team generator.
        
        Args:
            ai_assistant: AI assistant instance for team generation
        """
        self.ai = ai_assistant
        
        # Base team template following TEAM_PROMPT.md standards
        self.base_standards = self._load_base_standards()
    
    def _load_base_standards(self) -> Dict[str, Any]:
        """
        Load base standards from TEAM_PROMPT.md.
        
        Returns:
            Dictionary with base coding standards and principles
        """
        return {
            'iq_requirement': '180+',
            'experience_requirement': '15+ years',
            'expertise_level': 'World-class architects and senior engineers',
            'coding_standards': {
                'language': 'English only',
                'commits': 'Conventional Commits format',
                'type_hints': 'Required on all functions',
                'test_coverage': 'Minimum 95%',
                'security': 'OWASP Top 10 compliance',
                'documentation': 'Comprehensive docs required'
            },
            'architecture_principles': [
                'SOLID Principles',
                'Clean Code',
                'Design Patterns',
                'Domain-Driven Design',
                '12-Factor App',
                'Independence First',
                'API First',
                'Security First'
            ]
        }
    
    def analyze_project(self, project_description: str) -> Dict[str, Any]:
        """
        Analyze project and determine required expertise.
        
        Args:
            project_description: User's description of their project
            
        Returns:
            Dictionary with project analysis:
            - domain: Project domain (e-commerce, fintech, etc.)
            - technologies: Required technologies
            - expertise_areas: List of expertise areas needed
            - complexity: Project complexity level
        """
        prompt = f"""
        Analyze this project description and determine:
        1. Project domain
        2. Required technologies
        3. Expertise areas needed
        4. Complexity level (low/medium/high/expert)
        
        Project description:
        {project_description}
        
        Return as JSON:
        {{
            "domain": "...",
            "technologies": [...],
            "expertise_areas": [...],
            "complexity": "...",
            "key_challenges": [...]
        }}
        """
        
        analysis = self.ai.query(prompt)
        
        # Parse JSON response
        import json
        try:
            return json.loads(analysis)
        except json.JSONDecodeError:
            logger.warning("Failed to parse AI response, using defaults")
            return {
                'domain': 'general',
                'technologies': [],
                'expertise_areas': ['full-stack development'],
                'complexity': 'medium',
                'key_challenges': []
            }
    
    def generate_team(
        self, 
        project_description: str,
        team_size: int = 9
    ) -> Dict[str, Any]:
        """
        Generate custom expert team for the project.
        
        Args:
            project_description: User's project description
            team_size: Number of team members (default: 9)
            
        Returns:
            Dictionary with team profile:
            - team_members: List of expert profiles
            - team_prompt: Complete team prompt for AI
            - expertise_coverage: Coverage of required areas
        """
        # Analyze project
        analysis = self.analyze_project(project_description)
        
        # Generate team members
        prompt = f"""
        Generate a team of {team_size} world-class experts for this project.
        
        Project Analysis:
        - Domain: {analysis['domain']}
        - Technologies: {', '.join(analysis['technologies'])}
        - Expertise needed: {', '.join(analysis['expertise_areas'])}
        - Complexity: {analysis['complexity']}
        
        Team Requirements:
        - Minimum IQ: 180+
        - Minimum Experience: 15+ years
        - Each member MUST have specialized expertise relevant to project
        
        For each team member, provide:
        1. Name (realistic, diverse backgrounds)
        2. Title/Role
        3. IQ (180-200 range)
        4. Years of experience (15-25)
        5. Specialization (specific to project needs)
        6. Previous roles (relevant companies/projects)
        7. Key achievements (quantified results)
        8. Expertise areas (technologies, patterns, practices)
        9. Project responsibilities
        
        Return as JSON array of team members.
        """
        
        team_data = self.ai.query(prompt)
        
        # Parse team data
        import json
        try:
            team_members = json.loads(team_data)
        except json.JSONDecodeError:
            logger.error("Failed to parse team data")
            team_members = self._generate_default_team()
        
        # Generate complete team prompt
        team_prompt = self._generate_team_prompt(
            team_members, 
            analysis, 
            project_description
        )
        
        return {
            'team_members': team_members,
            'team_prompt': team_prompt,
            'project_analysis': analysis,
            'expertise_coverage': self._calculate_coverage(
                team_members, 
                analysis['expertise_areas']
            )
        }
    
    def _generate_team_prompt(
        self,
        team_members: List[Dict[str, Any]],
        analysis: Dict[str, Any],
        project_description: str
    ) -> str:
        """
        Generate complete team prompt combining base standards and team profiles.
        
        Args:
            team_members: List of team member profiles
            analysis: Project analysis
            project_description: Original project description
            
        Returns:
            Complete team prompt string
        """
        prompt_sections = []
        
        # Header
        prompt_sections.append(f"""
# 🎯 EXPERT TEAM FOR {analysis['domain'].upper()} PROJECT

> **Custom AI Team Generated for Your Project**
> 
> {project_description}

---

## 📋 PROJECT ANALYSIS

**Domain:** {analysis['domain']}
**Technologies:** {', '.join(analysis['technologies'])}
**Complexity:** {analysis['complexity']}
**Key Challenges:** {', '.join(analysis.get('key_challenges', []))}

---

## 👥 YOUR EXPERT TEAM

**Team Size:** {len(team_members)} world-class experts
**Average IQ:** {sum(m.get('iq', 180) for m in team_members) / len(team_members):.0f}
**Combined Experience:** {sum(m.get('experience', 15) for m in team_members)} years

---
""")
        
        # Team members
        for i, member in enumerate(team_members, 1):
            prompt_sections.append(f"""
### {i}️⃣ **{member.get('name')}** - {member.get('title')}

- **IQ:** {member.get('iq', 180)}
- **Experience:** {member.get('experience', 15)} years
- **Specialization:** {member.get('specialization', 'Software Architecture')}
- **Previous Roles:** {member.get('previous_roles', 'Senior Engineer')}

**Key Achievements:**
{chr(10).join('  - ' + achievement for achievement in member.get('achievements', ['Built enterprise systems']))}

**Expertise:**
{chr(10).join('  - ' + skill for skill in member.get('expertise', ['Software development']))}

**Project Responsibilities:**
{chr(10).join('  - ' + resp for resp in member.get('responsibilities', ['Code implementation']))}

---
""")
        
        # Base standards
        prompt_sections.append(f"""
## 🌍 UNIVERSAL CODING STANDARDS

All team members MUST follow these standards:

### 🔴 CRITICAL RULES:

1. **English Only:**
   - All code, comments, docstrings in ENGLISH
   - Commit messages in ENGLISH
   - Variable/function names in ENGLISH

2. **Conventional Commits:**
   - Format: type(scope): subject
   - Valid types: feat, fix, refactor, docs, test, chore, style, perf
   - No trailing period
   - Lowercase after colon

3. **Type Hints:**
   - ALL functions must have type hints
   - Parameters and return types
   - Use typing module (Optional, List, Dict, etc.)

4. **Test Coverage:**
   - Minimum 95% coverage MANDATORY
   - Write tests FIRST (TDD)
   - pytest for testing

5. **Security:**
   - No hardcoded secrets
   - Use environment variables
   - Parametrized SQL queries
   - Input validation

6. **Documentation:**
   - Docstrings for all public functions/classes
   - README with setup instructions
   - API documentation (Swagger)

---

## 🏗️ ARCHITECTURE PRINCIPLES

{chr(10).join('- ' + principle for principle in self.base_standards['architecture_principles'])}

---

## 💡 DEVELOPMENT WORKFLOW

1. **Before Writing Code:**
   - Think like a 180+ IQ architect
   - Consider edge cases, scalability, security
   - Design for reusability

2. **Code Quality:**
   - Production-ready code (no TODOs)
   - Comprehensive error handling
   - Structured logging
   - Performance optimization

3. **Before Commit:**
   - Run all tests (must pass)
   - Check coverage (≥ 95%)
   - Validate type hints
   - Security scan
   - Format code (black, isort)

4. **Git Workflow:**
   - Descriptive commit messages (English)
   - Conventional Commits format
   - Branch naming: type/description

---

## 🎯 PROJECT-SPECIFIC REQUIREMENTS

**Technologies to use:**
{chr(10).join('- ' + tech for tech in analysis['technologies'])}

**Key challenges to address:**
{chr(10).join('- ' + challenge for challenge in analysis.get('key_challenges', []))}

---

## ✅ SUCCESS CRITERIA

Your code is SUCCESSFUL if:
- ✅ Follows all coding standards
- ✅ Test coverage ≥ 95%
- ✅ No hardcoded secrets
- ✅ All in English
- ✅ Proper type hints
- ✅ Comprehensive documentation
- ✅ Production-ready quality

---

## 🚀 LET'S BUILD SOMETHING AMAZING!

Remember: You are world-class experts. Every line of code should reflect that.
""")
        
        return '\n'.join(prompt_sections)
    
    def _calculate_coverage(
        self, 
        team_members: List[Dict[str, Any]],
        required_areas: List[str]
    ) -> Dict[str, Any]:
        """
        Calculate how well the team covers required expertise areas.
        
        Args:
            team_members: List of team member profiles
            required_areas: List of required expertise areas
            
        Returns:
            Coverage analysis
        """
        # Extract all expertise from team
        team_expertise = []
        for member in team_members:
            team_expertise.extend(member.get('expertise', []))
        
        # Calculate coverage
        covered = []
        missing = []
        
        for area in required_areas:
            area_lower = area.lower()
            if any(area_lower in skill.lower() for skill in team_expertise):
                covered.append(area)
            else:
                missing.append(area)
        
        coverage_percentage = (len(covered) / len(required_areas) * 100) if required_areas else 100
        
        return {
            'coverage_percentage': coverage_percentage,
            'covered_areas': covered,
            'missing_areas': missing,
            'total_expertise': len(set(team_expertise))
        }
    
    def _generate_default_team(self) -> List[Dict[str, Any]]:
        """
        Generate default team if AI generation fails.
        
        Returns:
            List of default team member profiles
        """
        return [
            {
                'name': 'Dr. Alex Chen',
                'title': 'Lead Architect',
                'iq': 195,
                'experience': 20,
                'specialization': 'System Architecture',
                'achievements': ['Designed systems for 10M+ users'],
                'expertise': ['Python', 'Microservices', 'Cloud Architecture'],
                'responsibilities': ['Overall architecture design']
            },
            # Add more default members...
        ]
    
    def save_team_prompt(
        self, 
        team_data: Dict[str, Any],
        output_path: Path
    ) -> Path:
        """
        Save generated team prompt to file.
        
        Args:
            team_data: Team data from generate_team()
            output_path: Path to save prompt
            
        Returns:
            Path to saved file
        """
        output_file = Path(output_path) / 'TEAM_PROMPT.md'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(team_data['team_prompt'])
        
        logger.info(f"Team prompt saved to: {output_file}")
        return output_file


class ProjectConfigGenerator:
    """
    Generate project configuration based on team and requirements.
    """
    
    def __init__(self, ai_assistant):
        self.ai = ai_assistant
    
    def generate_config(
        self,
        project_description: str,
        team_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate complete project configuration.
        
        Args:
            project_description: Project description
            team_data: Team data from DynamicTeamGenerator
            
        Returns:
            Complete project configuration
        """
        analysis = team_data['project_analysis']
        
        return {
            'project': {
                'name': self._extract_project_name(project_description),
                'description': project_description,
                'domain': analysis['domain'],
                'complexity': analysis['complexity']
            },
            'technologies': analysis['technologies'],
            'team': {
                'size': len(team_data['team_members']),
                'members': team_data['team_members'],
                'expertise_coverage': team_data['expertise_coverage']
            },
            'standards': {
                'language': 'English',
                'commit_format': 'Conventional Commits',
                'test_coverage': '95%',
                'code_style': 'PEP 8',
                'security': 'OWASP Top 10'
            },
            'automation': {
                'pre_commit_checks': True,
                'auto_fix': True,
                'ai_code_review': True,
                'auto_testing': True
            }
        }
    
    def _extract_project_name(self, description: str) -> str:
        """Extract project name from description."""
        # Use AI to extract name
        prompt = f"""
        Extract a short project name from this description.
        Return only the name, no explanation.
        
        Description: {description}
        """
        return self.ai.query(prompt).strip()
