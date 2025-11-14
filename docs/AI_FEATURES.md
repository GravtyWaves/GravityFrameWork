# 🤖 AI-Powered Features Guide

Gravity Framework integrates **100% FREE AI assistance** using Ollama (local AI models) to provide intelligent microservice orchestration.

## 🎯 Overview

The AI assistant helps you:
- **Connect microservices** like puzzle pieces
- **Auto-create databases** for services that don't have them
- **Analyze database schemas** across multiple services
- **Diagnose errors** with intelligent solutions
- **Optimize deployment** for performance and scalability

**Best part? It's 100% FREE for EVERYONE!** 
- Uses Ollama (completely free, runs locally)
- No API keys, no subscriptions, no internet after setup
- Works for students, professionals, companies - anyone!

## 🚀 Quick Start

### Step 1: Install Ollama (2 minutes)

```bash
# Download from: https://ollama.com/download

# Or use package manager:
# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download installer from ollama.com
```

### Step 2: Get a Free AI Model

```bash
# Recommended: Fast & lightweight (2GB)
ollama pull llama3.2:3b

# Alternative: Better quality (7GB)
ollama pull llama3.1:8b

# For code-heavy tasks (5GB)
ollama pull deepseek-coder:6.7b
```

### Step 3: Start Ollama

```bash
ollama serve
# Ollama runs at http://localhost:11434
```

### Step 4: Use Gravity with AI

```python
from gravity_framework import GravityFramework

# AI assistance enabled by default (auto-detects Ollama)
framework = GravityFramework(ai_assist=True)

# Or specify a model
framework = GravityFramework(
    ai_assist=True,
    ollama_model="llama3.2:3b"  # Use your preferred model
)

# Discover services
framework.discover_services("https://github.com/org/auth-service")
framework.discover_services("https://github.com/org/user-service")

# Get AI analysis
analysis = framework.ai_analyze()
print(analysis)
```

### Check AI Availability

```python
if framework.ai.enabled:
    print(f"🤖 AI Assistant active - powered by Ollama ({framework.ai.ollama_model})")
else:
    print("⚠️ Install Ollama for FREE AI: https://ollama.com/download")
```

## 🧩 Intelligent Service Connection (Puzzle-Solving)

The AI analyzes your microservices and suggests how they should connect:

```python
# Get connection suggestions
connections = framework.ai_suggest_connections()

for conn in connections:
    print(f"{conn['from']} → {conn['to']}")
    print(f"  Method: {conn['method']}")
    print(f"  Endpoint: {conn['endpoint']}")
    print(f"  Priority: {conn['priority']}")
```

**Example Output:**
```
user-service → auth-service
  Method: JWT tokens via API
  Endpoint: /api/auth/verify
  Priority: high

frontend-app → user-service
  Method: HTTP REST
  Endpoint: /api/users
  Priority: medium
```

## 🗄️ Database Auto-Creation

**Key Feature**: Microservices don't need to come with databases. Gravity creates them automatically!

### How It Works

1. **Declare database needs** in your service manifest:

```yaml
# auth-service/gravity-service.yaml
name: auth-service
version: 1.0.0
type: api

databases:
  - name: auth_db
    type: postgresql
    extensions: [uuid-ossp, pgcrypto]
  - name: sessions
    type: redis
```

2. **Framework auto-creates** everything:

```python
# Install services - databases created automatically
await framework.install()

# Framework:
# ✓ Creates PostgreSQL database "auth_db"
# ✓ Installs uuid-ossp and pgcrypto extensions
# ✓ Creates Redis instance "sessions"
# ✓ Generates secure credentials
# ✓ Injects environment variables:
#   - AUTH_DB_URL=postgresql://user:pass@host:5432/auth_db
#   - SESSIONS_URL=redis://host:6379
```

3. **Services use environment variables**:

```python
# In your auth-service code
import os
from sqlalchemy import create_engine

# Connection string automatically injected by Gravity
DATABASE_URL = os.getenv("AUTH_DB_URL")
engine = create_engine(DATABASE_URL)
```

### Supported Database Types

- **PostgreSQL** - Full-featured with extensions
- **MySQL** - With charset/collation support
- **MongoDB** - NoSQL document database
- **Redis** - In-memory cache/sessions
- **SQLite** - Lightweight, file-based

### AI Schema Analysis

When you have multiple services with databases, the AI:

```python
analysis = framework.ai_analyze()

# AI detects:
# - Shared database schemas between services
# - Missing foreign key relationships
# - Opportunities for consolidation
# - Performance optimization suggestions
```

**Example AI Analysis:**
```json
{
  "warnings": [
    {
      "type": "shared_database",
      "message": "user-service and auth-service both access 'users' table",
      "recommendation": "Consider database-per-service pattern or shared schema service"
    }
  ],
  "optimizations": [
    {
      "type": "indexing",
      "table": "users",
      "columns": ["email", "username"],
      "benefit": "30% faster authentication queries"
    }
  ]
}
```

## 🔍 AI-Powered Error Diagnosis

Get intelligent solutions for errors:

```python
# When an error occurs
diagnosis = framework.ai_diagnose(
    "Connection refused on port 8000",
    context={"service": "auth-service"}
)

print(diagnosis['likely_cause'])
# "Service not running or incorrect port configuration"

for solution in diagnosis['solutions']:
    print(f"  • {solution}")
# • Check if the service container is running: gravity status
# • Verify port mappings in gravity-service.yaml
# • Ensure Docker is running and containers are healthy
```

## ⚙️ Deployment Optimization

Get AI recommendations for better deployment:

```python
optimizations = framework.ai_optimize_deployment()

# Resource allocation
for rec in optimizations['resource_allocation']:
    print(f"{rec['service']}: {rec['recommendation']}")

# Scaling recommendations
for scale in optimizations['scaling']:
    print(f"Type: {scale['type']}")
    print(f"Recommendation: {scale['recommendation']}")

# Performance improvements
for perf in optimizations['performance']:
    print(f"{perf['recommendation']}")
    print(f"Impact: {perf['impact']}")
```

**Example Output:**
```
Resource Allocation:
  auth-service: Allocate extra memory for database connections (512MB minimum)
  
Scaling:
  Type: horizontal
  Recommendation: Consider load balancer for API services (Nginx or Traefik)
  
Performance:
  Recommendation: Add Redis cache layer
  Impact: 30-50% performance improvement
```

## 🆓 How to Get Free AI Access

### Option 1: GitHub Copilot (Recommended)

**Free for:**
- Students (via GitHub Education)
- Open-source project maintainers
- Some free trials

**Install:**
1. Visit [GitHub Copilot](https://github.com/features/copilot)
2. Sign up for free access
3. Install VS Code extension
4. Gravity automatically detects and uses it

### Option 2: VS Code AI

VS Code has built-in AI features that Gravity can leverage:
- IntelliCode
- AI-assisted code completion
- Smart suggestions

### Option 3: GitHub CLI with Copilot

```bash
# Install GitHub CLI
gh extension install github/gh-copilot

# Gravity can use it via CLI
gh copilot suggest
```

## 🎓 Use Cases

### 1. Building E-Commerce Platform

```python
framework = GravityFramework(ai_assist=True)

# Discover microservices
framework.discover_services("https://github.com/myshop/auth-service")
framework.discover_services("https://github.com/myshop/product-service")
framework.discover_services("https://github.com/myshop/cart-service")
framework.discover_services("https://github.com/myshop/payment-service")
framework.discover_services("https://github.com/myshop/frontend")

# AI analyzes and suggests architecture
analysis = framework.ai_analyze()

# AI might suggest:
# • Add API Gateway for unified access
# • Share Redis cache between cart and product services
# • Connect payment-service to auth-service for user verification
# • Use event-driven architecture for order processing
```

### 2. Adding New Service to Existing System

```python
# You have 5 existing services
# Now adding a new notification service

framework.discover_services("https://github.com/org/notification-service")

# AI analyzes how new service fits
connections = framework.ai_suggest_connections()

# AI suggests:
# notification-service should:
# - Subscribe to events from order-service
# - Use auth-service for user preferences
# - Share Redis with existing services for queuing
```

### 3. Troubleshooting Production Issues

```python
# Service failing in production
error = "Database connection timeout"

diagnosis = framework.ai_diagnose(error, {
    "service": "user-service",
    "environment": "production",
    "load": "high"
})

# AI provides context-aware solutions:
# - Check database connection pool settings
# - Increase timeout values in production config
# - Consider read replicas for high load
# - Monitor slow queries with EXPLAIN ANALYZE
```

## 🧪 Testing AI Features

```python
import pytest
from gravity_framework import GravityFramework

def test_ai_analysis():
    framework = GravityFramework(ai_assist=True)
    
    # Add test services
    framework.discover_services("test-service-1")
    framework.discover_services("test-service-2")
    
    # Get AI analysis
    analysis = framework.ai_analyze()
    
    assert 'recommendations' in analysis
    assert 'optimizations' in analysis
    assert analysis['total_services'] == 2

def test_ai_disabled():
    # AI can be disabled for testing
    framework = GravityFramework(ai_assist=False)
    
    assert framework.ai.enabled == False
```

## 📚 Advanced Features

### Custom AI Prompts (Coming Soon)

```python
# Extend AI with custom analysis
framework.ai.add_custom_analyzer(
    name="security_audit",
    prompt="Analyze services for security vulnerabilities"
)

results = framework.ai.custom_analyze("security_audit")
```

### AI Learning from Your Architecture

The AI learns from your patterns:
- Service naming conventions
- Database naming patterns
- API endpoint structures
- Error handling approaches

Over time, suggestions become more tailored to your specific architecture.

## 🤝 Contributing AI Improvements

We welcome contributions to make the AI smarter:

1. **Better error diagnosis patterns**
2. **More connection suggestion rules**
3. **Database schema analysis improvements**
4. **Deployment optimization strategies**

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## 🔒 Privacy & Security

- **All AI processing respects your privacy**
- **Code is not sent to external servers** (uses local Copilot)
- **No data collection** beyond what Copilot normally does
- **You control when AI features are enabled**

## 📞 Support

Questions about AI features?
- Check [GitHub Discussions](https://github.com/GravtyWaves/GravityFrameWork/discussions)
- File an issue with `ai` label
- Join our community chat

---

**Remember**: AI is here to assist, not replace your judgment. Always review AI suggestions before applying them to production systems! 🧠✨
