# 🌟 Gravity Framework

<div align="center">

**The Ultimate AI-Powered Python Framework for Microservices Orchestration**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![AI-Powered](https://img.shields.io/badge/AI-Powered-brightgreen.svg)](https://github.com/features/copilot)

*Discover. Install. Connect. Orchestrate. Deploy. Monitor. **With AI Intelligence.***

</div>

---

## 🚀 What is Gravity Framework?

Gravity Framework is a **complete microservices orchestration platform** that transforms independent services from separate repositories into a unified, production-ready application — automatically.

Simply provide **GitHub repository URLs** of your microservices, and Gravity handles everything: discovery, dependency resolution, database setup, containerization, and deployment.

### ✨ Core Capabilities

- 🤖 **AI-Powered Orchestration** - **100% FREE** Ollama integration for intelligent service connection (no API keys!)
- 🔍 **Smart Discovery** - Automatically detect services from **GitHub URLs**
- 📦 **Auto Installation** - Resolve dependencies and install in correct order
- 🗄️ **Intelligent Database Management** - Auto-create databases for microservices that don't have them
  - **PostgreSQL, MySQL, MongoDB, Redis, SQLite** - all created and connected automatically
  - **AI Schema Analysis** - Automatically understand and connect database schemas across services
  - **Zero Configuration** - Microservices declare needs, framework handles creation
- 🎨 **Frontend Integration** - Support for React, Vue, Angular, and static frontends
- 🔗 **AI Service Wiring** - Intelligently connect services like puzzle pieces using AI analysis
- 🐳 **Container Management** - Run each service in isolated Docker containers
- ⚡ **Dependency Resolution** - Handle version conflicts with PubGrub algorithm
- 🌐 **API Gateway** - Route requests with automatic service discovery
- 📊 **Health Monitoring** - Real-time status, logs, and health checks
- 💡 **AI Assistant** - Your free AI advisor for architecture decisions and troubleshooting

## 📋 Quick Start

### Installation
```bash
pip install gravity-framework
```

### Create Your First App
```bash
# Initialize project
gravity init my-app
cd my-app

# Add services from GitHub URLs
gravity add https://github.com/your-org/auth-service
gravity add https://github.com/your-org/user-service
gravity add https://github.com/your-org/frontend-app

# Install & start
gravity install
gravity start

# Monitor
gravity status
```

## 🗄️ Intelligent Database Management

### Auto-Create Databases for Any Microservice

**Microservices don't need to come with databases** - Gravity creates them automatically! Simply declare what you need:

```yaml
# In your microservice's gravity-service.yaml
databases:
  - name: auth_db
    type: postgresql
    extensions: [uuid-ossp]
  - name: user_cache
    type: redis
  - name: sessions
    type: sqlite
```

**Gravity automatically**:
1. ✅ Creates the databases (PostgreSQL, MySQL, MongoDB, Redis, SQLite)
2. ✅ Configures connections with proper credentials
3. ✅ Injects connection strings as environment variables
4. ✅ Sets up extensions, charset, and collations
5. ✅ **Uses AI to analyze and connect schemas across microservices**

### AI-Powered Schema Analysis

When you have multiple microservices, Gravity's AI assistant:
- 🧠 **Analyzes database schemas** across all services
- 🔗 **Discovers relationships** between tables in different microservices
- 🎯 **Suggests optimal connections** and foreign key relationships
- ⚡ **Auto-generates migration scripts** when needed
- 💡 **Recommends best practices** for data consistency

**Supported Databases:**
- ✅ **SQLite** - Lightweight, file-based, perfect for development
- ✅ **PostgreSQL** - Production-grade with extensions support
- ✅ **MySQL** - With charset/collation configuration
- ✅ **MongoDB** - NoSQL document database
- ✅ **Redis** - In-memory cache and sessions

## 🤖 AI-Powered Intelligence (100% FREE - No API Keys!)

Gravity Framework integrates **Ollama** (completely free local AI) to provide intelligent assistance:

### 🧩 Intelligent Service Connection

```bash
# The AI analyzes your microservices and suggests optimal connections
gravity connect --ai-assist

🤖 AI Analysis Complete:
  ✓ Found 5 microservices
  ✓ Identified 3 shared database schemas
  ✓ Discovered 12 API dependencies
  
  Suggestions:
  → auth-service should connect to user-service via /api/users
  → payment-service needs access to order-service database
  → Recommended: Add Redis cache layer between frontend and API gateway
```

### 💡 AI Assistant Features

1. **Puzzle-Solving Architecture**
   - AI understands how to piece together different microservices
   - Automatically maps API endpoints and database connections
   - Suggests optimal service-to-service communication patterns

2. **Database Schema Intelligence**
   - Analyzes all database tables across microservices
   - Detects duplicate schemas and suggests consolidation
   - Identifies missing foreign keys and relationships
   - Recommends indexing strategies for performance

3. **Advisory & Troubleshooting**
   - Real-time suggestions while you develop
   - Error diagnosis with AI-powered solutions
   - Best practices recommendations
   - Performance optimization tips

4. **Zero Cost - Truly Free for Everyone**
   - Uses **Ollama** (100% free, no API keys needed)
   - Runs **locally** on your machine (no internet after download)
   - No subscriptions, no credits, no limits
   - Works for students, professionals, everyone!

### 🎯 How It Works

```python
# Gravity automatically uses AI when available
from gravity_framework import GravityFramework

framework = GravityFramework(ai_assist=True)  # Auto-detects Copilot

# AI analyzes services and suggests connections
services = framework.discover_services([
    "https://github.com/org/auth-service",
    "https://github.com/org/user-service",
    "https://github.com/org/payment-service"
])

# AI provides intelligent recommendations
recommendations = framework.ai_analyze()
# → "user-service and auth-service share 'users' table - consider consolidating"
# → "payment-service should use auth-service JWT tokens"
# → "Recommended: Add API gateway between frontend and backend services"
```

### 🔧 AI Setup (ZERO Configuration Required!)

**The framework automatically installs everything for you!**

```python
from gravity_framework import GravityFramework

# That's it! Just create the framework and AI will auto-install
framework = GravityFramework(ai_assist=True)  # AI installs automatically!

# First time: Ollama downloads (2-5 min, only once)
# Next time: Instant - everything ready!
```

**What happens automatically:**
1. ✅ Detects if Ollama is installed
2. ✅ Downloads and installs Ollama if missing
3. ✅ Downloads AI model (llama3.2:3b - 2GB)
4. ✅ Starts Ollama service
5. ✅ Ready to use!

**No manual steps needed!** Just use the framework.

---

<details>
<summary>🔧 Manual Installation (Optional - if you prefer)</summary>

**Step 1: Install Ollama** (2 minutes)
```bash
# Windows/Mac/Linux - Download from:
https://ollama.com/download

# Or use package manager:
# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

**Step 2: Download a Free Model**
```bash
# Fast & Lightweight (recommended - 2GB)
ollama pull llama3.2:3b

# Better quality (7GB)
ollama pull llama3.1:8b

# Best for code (5GB)
ollama pull deepseek-coder:6.7b
```

**Step 3: Start Ollama**
```bash
ollama serve
```

</details>

**Disable Auto-Install (if needed):**
```python
# Disable automatic installation
framework = GravityFramework(
    ai_assist=True,
    auto_install_ai=False  # Won't auto-install, will just detect
)
```

**That's it!** Gravity automatically detects and uses Ollama. No API keys, no configuration!

**CLI:**
```bash
# Enable AI assistance globally
gravity config set ai_assist true

# Use AI for specific commands
gravity connect --ai-analyze
gravity deploy --ai-optimize
gravity troubleshoot --ai-diagnose
```

## 🎨 Frontend Support

Gravity seamlessly integrates frontend applications:

- **React/Next.js** - Modern React applications
- **Vue/Nuxt** - Vue.js frameworks
- **Angular** - Angular applications
- **Static Sites** - HTML/CSS/JS served via nginx
- **API-First** - Any frontend consuming your microservices

Simply specify `type: frontend` in your service manifest.

## 📊 CLI Commands

### Service Management
```bash
gravity add <repo>              # Add service from Git
gravity list                    # List all services
gravity install                 # Install all
gravity start                   # Start all
gravity stop                    # Stop all
gravity restart <service>       # Restart service
```

### Monitoring
```bash
gravity status                  # Service status
gravity health                  # Health checks
gravity logs <service>          # View logs
```

## 🏗️ Service Manifest

Create `gravity-service.yaml` in your service:

```yaml
name: auth-service
version: 1.0.0
type: api

dependencies:
  - name: user-service
    version: ">=1.0.0"

databases:
  - name: auth_db
    type: postgresql

runtime: python:3.11
command: uvicorn main:app --host 0.0.0.0 --port 8000

ports:
  - container: 8000
    host: 8001

health_check:
  endpoint: /health
  interval: 30

api_prefix: /api/auth
```

See [examples/gravity-service.yaml](examples/gravity-service.yaml) for full example.

## 🛠️ Technology Stack

- **Python 3.11+** - Modern Python features
- **Typer + Rich** - Beautiful CLI
- **Docker SDK** - Container management
- **SQLAlchemy 2.0** - Database orchestration
- **PubGrub** - Dependency resolution
- **FastAPI** - API gateway
- **Pytest** - Testing (95%+ coverage)

## 👥 Development Team

- 🏗️ **Dr. Marcus Hartmann** - Framework Architect
- 🔍 **Dr. Yuki Tanaka** - Service Discovery
- 🗄️ **Dr. Priya Sharma** - Database Orchestration
- 🔗 **Alexander Petrov** - Dependency Resolution
- 🐳 **Sarah Chen** - Container Orchestration
- 🌐 **Mohammed Al-Rashid** - API Gateway
- 🔒 **Dr. Elena Volkov** - Security & Config
- 📊 **James O'Brien** - Monitoring
- ⚙️ **Kenji Watanabe** - DevOps & CLI

See [TEAM_PROMPT.md](TEAM_PROMPT.md) for complete details.

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**Built with ❤️ by the Gravity Framework Team**

*Making microservices orchestration effortless*

</div>
