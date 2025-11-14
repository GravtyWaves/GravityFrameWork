# 📁 Gravity Framework - Project Structure

## 🗂️ Directory Overview

```
GravityFrameWork/
│
├── 📄 Core Files
│   ├── README.md                    # Main documentation
│   ├── LICENSE                      # MIT License
│   ├── CHANGELOG.md                 # Version history
│   ├── QUICKSTART.md                # 5-minute quickstart
│   ├── ROADMAP.md                   # Future plans & known issues
│   ├── TEAM_PROMPT.md               # Team guidance
│   ├── ARCHITECTURE.md              # System architecture
│   └── PROJECT_STRUCTURE.md         # This file
│
├── 📦 Package Configuration
│   ├── setup.py                     # Package setup
│   ├── pyproject.toml               # Modern Python config
│   ├── requirements.txt             # Dependencies
│   └── pytest.ini                   # Test configuration
│
├── 🐍 Source Code
│   └── gravity_framework/           # Main package
│       ├── __init__.py              # Package exports
│       │
│       ├── ai/                      # AI & Autonomous Development
│       │   ├── assistant.py         # AI assistant (Ollama)
│       │   ├── installer.py         # Ollama installer
│       │   ├── team_generator.py    # Dynamic team generation
│       │   └── autonomous_dev.py    # Autonomous development system
│       │
│       ├── core/                    # Core Framework
│       │   ├── framework.py         # Main GravityFramework class
│       │   └── manager.py           # Service manager
│       │
│       ├── models/                  # Data Models
│       │   └── service.py           # Service models & registry
│       │
│       ├── discovery/               # Service Discovery
│       │   └── scanner.py           # Git & local scanner
│       │
│       ├── resolver/                # Dependency Resolution
│       │   └── dependency.py        # PubGrub resolver
│       │
│       ├── database/                # Database Management
│       │   ├── orchestrator.py      # DB orchestrator
│       │   └── multi_access.py      # Multi-DB access
│       │
│       ├── learning/                # Continuous Learning
│       │   └── system.py            # Learning system
│       │
│       ├── git/                     # Git Integration
│       │   ├── integration.py       # Git operations
│       │   └── commit_manager.py    # Smart commits
│       │
│       ├── devops/                  # DevOps Automation
│       │   └── automation.py        # Container & deployment
│       │
│       ├── standards/               # Code Standards
│       │   └── enforcer.py          # Standards enforcement
│       │
│       ├── project/                 # Project Management
│       │   └── manager.py           # Project manager
│       │
│       └── cli/                     # Command Line Interface
│           └── main.py              # CLI commands
│
├── 📚 Documentation
│   └── docs/
│       ├── guides/                  # User guides
│       ├── api/                     # API reference
│       ├── examples/                # Example documentation
│       │
│       ├── AUTONOMOUS_DEVELOPMENT_FA.md      # Autonomous dev (Persian)
│       ├── AUTONOMOUS_DEVELOPMENT.md         # Autonomous dev (English)
│       ├── CONTINUOUS_LEARNING_FA.md         # Learning system (Persian)
│       ├── MULTI_DATABASE_ACCESS_FA.md       # Multi-DB (Persian)
│       ├── COMMIT_MANAGEMENT_FA.md           # Commit management (Persian)
│       ├── INTERACTIVE_GUIDE_FA.md           # Interactive guide (Persian)
│       ├── OLLAMA_INSTALL_FA.md              # Ollama installation (Persian)
│       └── COMPLETE_FEATURES_FA.md           # All features (Persian)
│
├── 💡 Examples
│   └── examples/
│       ├── autonomous_development.py         # 8 autonomous dev examples
│       ├── continuous_learning.py            # 8 learning examples
│       ├── multi_database_access.py          # 9 database examples
│       ├── project_management.py             # Project management examples
│       │
│       ├── sample-services/                  # Sample microservices
│       │   └── (To be added)
│       │
│       └── gravity-service.yaml              # Service configuration example
│
├── 🧪 Tests
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py              # Pytest configuration
│       │
│       ├── Unit Tests
│       ├── test_framework.py        # Framework tests
│       ├── test_scanner.py          # Scanner tests
│       ├── test_resolver.py         # Resolver tests
│       ├── test_orchestrator.py     # Database tests
│       ├── test_manager.py          # Manager tests
│       ├── test_cli.py              # CLI tests
│       │
│       ├── integration/             # Integration tests
│       │   └── (To be added)
│       │
│       └── e2e/                     # End-to-end tests
│           └── (To be added)
│
├── 🗄️ Archive
│   └── archive/                     # Archived/deprecated files
│       └── ROADMAP_V1.md
│
├── 🔧 Development
│   ├── .venv/                       # Virtual environment
│   ├── .pytest_cache/               # Pytest cache
│   ├── .coverage                    # Coverage data
│   └── cleanup.py                   # Cleanup script
│
└── 🚫 Ignored (in .gitignore)
    ├── .gravity/                    # Runtime data
    ├── __pycache__/                 # Python cache
    └── *.egg-info/                  # Build artifacts
```

---

## 📦 Package Structure

### Main Package: `gravity_framework`

```python
gravity_framework/
├── __init__.py           # Exports: GravityFramework, AIProvider, etc.
├── ai/                   # AI-powered features
├── core/                 # Core framework logic
├── models/               # Data models
├── discovery/            # Service discovery
├── resolver/             # Dependency resolution
├── database/             # Database management
├── learning/             # Continuous learning
├── git/                  # Git integration
├── devops/               # DevOps automation
├── standards/            # Code standards
├── project/              # Project management
└── cli/                  # Command-line interface
```

---

## 🎯 Key Files Explained

### Core Configuration

- **`setup.py`**: Traditional setup file for `pip install`
- **`pyproject.toml`**: Modern Python project metadata
- **`requirements.txt`**: Runtime dependencies

### Documentation

- **`README.md`**: Main entry point, overview, quickstart
- **`QUICKSTART.md`**: 5-minute getting started guide
- **`ROADMAP.md`**: Development roadmap and known issues
- **`ARCHITECTURE.md`**: System architecture and design
- **`TEAM_PROMPT.md`**: Team standards and best practices

### Persian Documentation (`docs/`)

All feature guides in Persian for Persian-speaking developers:
- **Autonomous Development** (Persian + English)
- **Continuous Learning** 
- **Multi-Database Access**
- **Commit Management**
- **Interactive Guide**
- **Ollama Installation**
- **Complete Features Summary**

### Examples (`examples/`)

Working code examples showing all features:
- **`autonomous_development.py`**: 8 examples of AI team development
- **`continuous_learning.py`**: 8 examples of learning system
- **`multi_database_access.py`**: 9 examples of database access
- **`project_management.py`**: Project management examples

---

## 🚀 Getting Started

### For Users

1. Install package:
   ```bash
   pip install gravity-framework
   ```

2. Read quickstart:
   ```bash
   cat QUICKSTART.md
   ```

3. Try examples:
   ```bash
   python examples/autonomous_development.py
   ```

### For Developers

1. Clone repository:
   ```bash
   git clone https://github.com/GravtyWaves/GravityFrameWork.git
   cd GravityFrameWork
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

4. Run tests:
   ```bash
   pytest
   ```

5. Check coverage:
   ```bash
   pytest --cov=gravity_framework --cov-report=html
   ```

---

## 📝 File Naming Conventions

### Python Files
- `snake_case.py` for all Python files
- `test_*.py` for test files
- `__init__.py` for package initialization

### Documentation
- `UPPERCASE.md` for root-level docs (README, CHANGELOG, etc.)
- `TitleCase.md` for feature docs
- `FEATURE_NAME_FA.md` for Persian documentation

### Examples
- `lowercase_with_underscores.py`
- Descriptive names showing what they demonstrate

---

## 🔍 Finding Things

### "Where is the main framework class?"
→ `gravity_framework/core/framework.py`

### "Where are the AI features?"
→ `gravity_framework/ai/` directory

### "Where is autonomous development?"
→ `gravity_framework/ai/autonomous_dev.py`

### "Where are the examples?"
→ `examples/` directory

### "Where is the documentation?"
→ `docs/` directory (Persian) + `README.md` (English)

### "Where are the tests?"
→ `tests/` directory

### "How do I import the framework?"
```python
from gravity_framework import GravityFramework
```

---

## 🧹 Maintenance

### Clean Up
```bash
python cleanup.py
```

### Remove Cache
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

---

## 📊 Project Statistics

- **Total Lines of Code**: ~15,500+
- **Documentation Lines**: ~16,000+
- **Test Coverage**: ~75% (target: 95%+)
- **Python Version**: 3.11+
- **Dependencies**: ~30 packages
- **Supported Databases**: 5 (PostgreSQL, MySQL, MongoDB, Redis, SQLite)
- **AI Providers**: 1 (Ollama - FREE, local, no API keys)

---

## 🎯 Next Steps

See `ROADMAP.md` for:
- Known issues and their solutions
- Planned improvements
- Feature roadmap
- Priority tasks

---

**Last Updated**: After project cleanup and reorganization
**Maintained By**: Gravity Framework Team
