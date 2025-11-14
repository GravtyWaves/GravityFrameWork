# 🌟 Gravity Framework

<div align="center">

**The Ultimate Python Framework for Microservices Orchestration**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*Discover. Install. Connect. Orchestrate. Deploy. Monitor.*

</div>

---

## 🚀 What is Gravity Framework?

Gravity Framework is a **complete microservices orchestration platform** that transforms independent services from separate repositories into a unified, production-ready application — automatically.

Simply provide **GitHub repository URLs** of your microservices, and Gravity handles everything: discovery, dependency resolution, database setup, containerization, and deployment.

### ✨ Core Capabilities

- 🔍 **Smart Discovery** - Automatically detect services from **GitHub URLs**
- 📦 **Auto Installation** - Resolve dependencies and install in correct order
- 🗄️ **Multi-Database Support** - **PostgreSQL, SQLite, MySQL, MongoDB, Redis** - all created automatically
- 🎨 **Frontend Integration** - Support for React, Vue, Angular, and static frontends
- 🔗 **Service Wiring** - Connect services with zero manual configuration
- 🐳 **Container Management** - Run each service in isolated Docker containers
- ⚡ **Dependency Resolution** - Handle version conflicts with PubGrub algorithm
- 🌐 **API Gateway** - Route requests with automatic service discovery
- 📊 **Health Monitoring** - Real-time status, logs, and health checks

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

## 🗄️ Multi-Database Support

Gravity Framework supports **SQLite, PostgreSQL, MySQL, MongoDB, and Redis**. Services declare database needs in their manifest:

```yaml
databases:
  - name: auth_db
    type: postgresql
    extensions: [uuid-ossp]
  - name: cache_db
    type: sqlite
  - name: sessions
    type: redis
```

Gravity **automatically creates and configures**:
- ✅ **SQLite** - Lightweight file-based database
- ✅ **PostgreSQL** - With extensions and proper charset
- ✅ **MySQL** - With charset/collation configuration
- ✅ **MongoDB** - NoSQL document database
- ✅ **Redis** - In-memory cache and sessions

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
