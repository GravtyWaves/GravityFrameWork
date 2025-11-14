<!--
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity Framework - Microservices Orchestration Platform
File         : TEAM_PROMPT.md
Description  : Elite development team profiles, standards, and methodologies
               for the Gravity Framework. A Python-based framework that discovers,
               installs, connects, and orchestrates independent microservices
               into cohesive web applications. Defines 9 world-class engineers
               with IQ 180+, 15+ years experience each.
Language     : English (UK)
Document Type: Team Documentation & Standards

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Dr. Marcus Hartmann (Framework Architect)
Contributors      : All 9 team members (collaborative document)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-13 09:00 UTC
Last Modified     : 2025-11-13 09:00 UTC
Writing Time      : 6 hours 30 minutes
Review Time       : 2 hours 45 minutes
Total Time        : 9 hours 15 minutes

================================================================================
COST CALCULATION
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Writing Cost      : 6.5 × $150 = $975.00 USD
Review Cost       : 2.75 × $150 = $412.50 USD
Total Cost        : $1,387.50 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-13 - Dr. Marcus Hartmann - Initial framework documentation
v1.0.1 - 2025-11-13 - All members - Added framework-specific team profiles

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity Framework
License: MIT License
Repository: https://github.com/GravtyWaves/GravityFrameWork

================================================================================
-->

# 🎯 GRAVITY FRAMEWORK - ELITE DEVELOPMENT TEAM PROFILE

> **The Ultimate Python Framework for Microservices Orchestration**
> 
> Discover. Install. Connect. Orchestrate. Deploy.

---

## 📖 TABLE OF CONTENTS

1. [Framework Vision & Mission](#framework-vision--mission)
2. [6 Golden Principles of Framework Architecture](#6-golden-principles-of-framework-architecture)
3. [Team Members & Expertise](#team-members--their-expertise)
4. [Framework Architecture Patterns](#framework-architecture-patterns)
5. [Technology Stack](#technology-stack)
6. [Development Standards](#development-standards)
7. [Plugin & Service Integration](#plugin--service-integration)
8. [Quick Reference](#quick-reference-card)

---

## 🌟 FRAMEWORK VISION & MISSION

### 🎯 **PRIMARY MISSION:**
> "Build a professional Python framework that discovers, installs, connects, and orchestrates independent microservices from separate repositories into cohesive web applications — like puzzle pieces forming a complete picture."

### 🏆 **PROJECT GOALS:**

1. **✅ Automatic Service Discovery**
   - Scan and discover microservices from multiple repositories
   - Auto-detect service capabilities, APIs, and dependencies
   - Plugin-based architecture for extensibility
   - Registry-based service catalog

2. **✅ Zero-Config Installation**
   - One-command installation of multiple microservices
   - Automatic dependency resolution
   - Version conflict detection and resolution
   - Rollback capabilities

3. **✅ Intelligent Service Connection**
   - Auto-wire services based on their contracts
   - API gateway auto-configuration
   - Service mesh integration
   - Load balancing and circuit breakers

4. **✅ Database Orchestration**
   - Auto-create databases for services that need them
   - Execute schema creation scripts automatically
   - Manage database migrations
   - Multi-database support (PostgreSQL, MySQL, MongoDB, Redis)

5. **✅ Production-Ready Deployment**
   - Docker Compose generation
   - Kubernetes manifest generation
   - Environment configuration management
   - Health checks and monitoring

6. **✅ Developer Experience**
   - Simple CLI interface
   - Interactive web dashboard
   - Real-time service status
   - Comprehensive logging and debugging

---

## 🌍 UNIVERSAL SOFTWARE DEVELOPMENT STANDARDS
### Applicable to ALL Software Projects Worldwide

**Version:** 3.0.0  
**Last Updated:** November 13, 2025  
**Applies To:** Python frameworks, orchestration systems, plugin architectures

---

### 🔴 CRITICAL RULE #1: FILE MANAGEMENT POLICY

**ALWAYS Search Before Creating:**

```
┌─────────────────────────────────────────────────────────────────┐
│              FILE MANAGEMENT WORKFLOW (MANDATORY)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: Search for Existing Files                            │
│         ↓                                                       │
│         Use: file_search, semantic_search, grep_search         │
│         Look for: Similar names, purposes, functionality       │
│                                                                 │
│  Step 2: File Found?                                           │
│         ├─→ YES → UPDATE existing file ✅                      │
│         │         • Never create duplicates                    │
│         │         • Edit and improve existing content          │
│         │         • Consolidate information                    │
│         │                                                       │
│         └─→ NO → CREATE new file ✅                            │
│                   • Only if truly necessary                    │
│                   • Follow naming conventions                  │
│                   • Document purpose clearly                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Rules:**
- ✅ **UPDATE existing files** instead of creating duplicates
- ✅ **SEARCH thoroughly** before creating new files
- ✅ **CONSOLIDATE content** - merge similar files
- ❌ **NEVER create:** `README_NEW.md`, `CONFIG_V2.py`, `UPDATED_*.md`
- ❌ **AVOID duplicates:** Check for similar filenames/purposes
- ✅ **FOLLOW structure:** Respect existing folder organization

**Examples:**
```
❌ BAD: Create "utils_new.py" when "utils.py" exists
✅ GOOD: Add new functions to existing "utils.py"

❌ BAD: Create "README_UPDATED.md" when "README.md" exists
✅ GOOD: Update existing "README.md" with new content

❌ BAD: Create "config_v2.json" when "config.json" exists
✅ GOOD: Update "config.json" or implement proper versioning
```

---

### 🔴 CRITICAL RULE #2: ENGLISH-ONLY POLICY

**ALL Technical Content MUST Be in English:**

**✅ REQUIRED (English):**
- Code: Variable names, function names, class names
- Comments: All inline comments
- Docstrings: All documentation strings
- Documentation: README, guides, API docs
- Git Commits: All commit messages
- Branch Names: All branch names
- Log Messages: All log output
- Error Messages: Internal errors

**❌ FORBIDDEN (Non-English):**
- Persian, Arabic, Chinese, etc. in technical content
- Mixed language code
- Non-English variable names
- Non-English comments

**✅ EXCEPTION:**
- User-facing content (UI messages, API responses to users)
- Database content for bilingual apps (`name_fa`, `description_fa`)
- Documentation specifically for non-English users

**Examples:**

```python
# ✅ CORRECT - English everywhere
class UserAuthenticationService:
    """Service for handling user authentication and session management."""
    
    def validate_credentials(self, username: str, password: str) -> bool:
        """
        Validate user credentials against database.
        
        Args:
            username: User's login username
            password: User's password (will be hashed)
            
        Returns:
            True if credentials are valid, False otherwise
            
        Raises:
            ValueError: If username or password is empty
        """
        # Check if username exists in database
        user = self.db.find_user(username)
        
        if not user:
            logger.warning(f"Login attempt for non-existent user: {username}")
            return False
        
        # Verify password hash
        return self.verify_password_hash(user.password_hash, password)

# ❌ WRONG - Non-English content
class ServisAuthentification:
    """سرویس برای مدیریت احراز هویت"""  # NEVER!
    
    def barresi_etelaat(self, nam_karbari, ramz):  # NEVER!
        """بررسی اطلاعات کاربر"""  # NEVER!
        # بررسی نام کاربری در دیتابیس  # NEVER!
        karbار = self.db.peyda_kon(nam_karbari)  # NEVER!
        return self.barresi_ramz(karbار, ramz)  # NEVER!
```

---

### 🔴 CRITICAL RULE #3: GIT COMMIT STANDARDS

**Conventional Commits Format (MANDATORY):**

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring (no functional changes)
- `docs`: Documentation only changes
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, configs)
- `style`: Code formatting (no logic changes)
- `perf`: Performance improvements

**✅ GOOD Examples:**
```bash
feat(auth): add OAuth2 authentication support

Implemented Google and GitHub OAuth providers with JWT tokens.
Added refresh token mechanism for better UX.

Closes #142

fix(database): resolve connection pool exhaustion

Connection pool was not releasing connections in error paths.
Added proper context managers and timeout configuration.

Performance improved from 500ms to 50ms per query.

refactor(api): simplify error handling middleware

Consolidated duplicate error handling code.
Reduced code duplication by 40%.

docs(readme): update installation instructions

Added prerequisites and troubleshooting guide.
```

**❌ BAD Examples:**
```bash
❌ "fixed stuff"                    # Too vague
❌ "WIP"                            # Not descriptive
❌ "اضافه کردن ویژگی جدید"         # Not English!
❌ "Added new feature."             # Period at end
❌ "FIXED BUG IN LOGIN"             # All caps, vague
```

**Branch Naming:**
```
<type>/<short-description>

Examples:
✅ feature/oauth-authentication
✅ fix/database-connection-leak
✅ refactor/api-error-handling
✅ docs/api-documentation
✅ test/integration-tests
❌ feature/اضافه-کردن-احراز        # Not English!
```

---

### 🔴 CRITICAL RULE #4: TYPE HINTS/ANNOTATIONS

**All Functions MUST Have Type Hints:**

```python
# ✅ CORRECT - Complete type hints
from typing import Optional, List, Dict, Union
from datetime import datetime

def calculate_total_price(
    items: List[Dict[str, Union[str, float]]],
    discount: Optional[float] = None,
    tax_rate: float = 0.1
) -> float:
    """
    Calculate total price with optional discount and tax.
    
    Args:
        items: List of items with 'name' and 'price' keys
        discount: Optional discount percentage (0.0 to 1.0)
        tax_rate: Tax rate to apply (default 10%)
        
    Returns:
        Final price including discount and tax
    """
    subtotal = sum(item['price'] for item in items)
    
    if discount:
        subtotal *= (1 - discount)
    
    return round(subtotal * (1 + tax_rate), 2)

# ❌ WRONG - No type hints
def calculate_total_price(items, discount=None, tax_rate=0.1):  # NEVER!
    subtotal = sum(item['price'] for item in items)
    if discount:
        subtotal *= (1 - discount)
    return subtotal * (1 + tax_rate)
```

---

### 🔴 CRITICAL RULE #5: SECURITY STANDARDS

**Never Hardcode Secrets:**

```python
# ✅ CORRECT - Environment variables
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    secret_key: str
    jwt_secret: str
    
    class Config:
        env_file = ".env"

settings = Settings()

# ❌ WRONG - Hardcoded secrets
DATABASE_URL = "postgresql://admin:password123@db.example.com/mydb"  # NEVER!
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"  # NEVER!
SECRET_KEY = "my-super-secret-key-12345"  # NEVER!
```

**Parametrized Queries (SQL Injection Prevention):**

```python
# ✅ CORRECT - Parametrized query
async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email address safely."""
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# ❌ WRONG - String interpolation (SQL injection risk!)
async def get_user_by_email(email: str) -> Optional[User]:
    query = f"SELECT * FROM users WHERE email = '{email}'"  # NEVER!
    result = await db.execute(query)
    return result.fetchone()
```

---

### 🔴 CRITICAL RULE #6: TESTING REQUIREMENTS

**Minimum 95% Coverage MANDATORY:**

```
┌─────────────────────────────────────────────────────────────────┐
│                  TESTING WORKFLOW (MANDATORY)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: Write Tests FIRST (TDD Approach)                      │
│         ↓                                                       │
│         Write unit tests for new function/feature              │
│         Minimum 95% coverage required                          │
│                                                                 │
│  Step 2: Run Tests                                             │
│         ↓                                                       │
│         pytest tests/ -v --cov=app --cov-report=html          │
│                                                                 │
│  Step 3: All Tests Pass?                                       │
│         ├─→ YES → Coverage ≥ 95%?                              │
│         │         ├─→ YES → Go to Step 4 ✅                    │
│         │         └─→ NO → Write more tests → Step 2          │
│         │                                                       │
│         └─→ NO → Tests need fixing?                            │
│                   ├─→ YES → Fix tests → Step 2                │
│                   └─→ NO → Fix code → Step 2                  │
│                                                                 │
│  Step 4: Code Review & Merge ✅                                │
│         ↓                                                       │
│         Create PR with test results                            │
│         Attach coverage report                                 │
│         Deploy only after approval                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Test Example:**
```python
import pytest

def test_user_authentication_success():
    """Test successful user authentication with valid credentials."""
    # Arrange
    auth_service = UserAuthenticationService()
    username = "test_user"
    password = "ValidPassword123"
    
    # Act
    result = auth_service.authenticate(username, password)
    
    # Assert
    assert result.success is True
    assert result.user_id is not None
    assert result.token is not None

def test_user_authentication_invalid_password():
    """Test authentication failure with invalid password."""
    # Arrange
    auth_service = UserAuthenticationService()
    username = "test_user"
    invalid_password = "WrongPassword"
    
    # Act & Assert
    with pytest.raises(AuthenticationError) as exc:
        auth_service.authenticate(username, invalid_password)
    
    assert "Invalid credentials" in str(exc.value)
```

---

### 🔴 CRITICAL RULE #7: ERROR HANDLING

**Comprehensive Error Handling Required:**

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class PaymentError(Exception):
    """Base exception for payment errors."""
    pass

class InsufficientFundsError(PaymentError):
    """Raised when account has insufficient funds."""
    pass

async def process_payment(
    user_id: int,
    amount: float,
    payment_method: str
) -> bool:
    """
    Process payment with comprehensive error handling.
    
    Args:
        user_id: ID of user making payment
        amount: Payment amount
        payment_method: Payment method (card, bank, etc.)
        
    Returns:
        True if payment successful
        
    Raises:
        ValueError: If amount is invalid
        InsufficientFundsError: If user has insufficient funds
        PaymentError: If payment processing fails
    """
    # Validate input
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}. Must be positive.")
    
    try:
        # Check user balance
        user = await get_user(user_id)
        if user.balance < amount:
            logger.warning(
                "Insufficient funds",
                extra={
                    "user_id": user_id,
                    "balance": user.balance,
                    "required": amount
                }
            )
            raise InsufficientFundsError(
                f"Insufficient funds. Balance: {user.balance}, Required: {amount}"
            )
        
        # Process payment
        transaction = await payment_gateway.charge(
            user_id=user_id,
            amount=amount,
            method=payment_method
        )
        
        logger.info(
            "Payment processed successfully",
            extra={
                "user_id": user_id,
                "amount": amount,
                "transaction_id": transaction.id
            }
        )
        return True
        
    except PaymentGatewayError as e:
        logger.error(
            "Payment gateway error",
            extra={
                "user_id": user_id,
                "amount": amount,
                "error": str(e)
            }
        )
        raise
    
    except Exception as e:
        logger.exception(
            "Unexpected error during payment processing",
            extra={"user_id": user_id, "amount": amount}
        )
        raise PaymentError(f"Payment processing failed: {e}") from e
```

---

### 📋 PRE-COMMIT CHECKLIST

**Before Every Commit, Verify:**

```
┌─────────────────────────────────────────────────────────────────┐
│          ✅ PRE-COMMIT CHECKLIST (MANDATORY)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  File Management:                                               │
│    ✅ Searched for existing files before creating new ones     │
│    ✅ Updated existing files instead of duplicating            │
│    ✅ Removed any duplicate or obsolete files                  │
│                                                                 │
│  Code Quality:                                                  │
│    ✅ All code in ENGLISH only                                  │
│    ✅ All comments in ENGLISH only                              │
│    ✅ All docstrings in ENGLISH only                            │
│    ✅ Full type hints on all functions                          │
│    ✅ No hardcoded secrets                                      │
│    ✅ All queries parametrized (no SQL injection)               │
│    ✅ Comprehensive error handling                              │
│    ✅ Structured logging added                                  │
│                                                                 │
│  Testing:                                                       │
│    ✅ Tests written (TDD approach)                              │
│    ✅ All tests pass                                            │
│    ✅ Coverage ≥ 95%                                            │
│    ✅ Integration tests included                                │
│    ✅ Performance tests for critical paths                      │
│                                                                 │
│  Independence (for Gravity services):                           │
│    ✅ No direct service imports                                 │
│    ✅ Configuration from environment                            │
│    ✅ Own database only                                         │
│    ✅ API/Event communication                                   │
│    ✅ Health check endpoint exists                              │
│                                                                 │
│  Git:                                                           │
│    ✅ Commit message in ENGLISH                                 │
│    ✅ Follows conventional commits format                       │
│    ✅ Descriptive and clear message                             │
│    ✅ Branch name in ENGLISH                                    │
│                                                                 │
│  Documentation:                                                 │
│    ✅ README updated (if needed)                                │
│    ✅ API docs updated (Swagger)                                │
│    ✅ CHANGELOG.md updated                                      │
│    ✅ Code comments clear and helpful                           │
│                                                                 │
│  Security:                                                      │
│    ✅ No secrets in code                                        │
│    ✅ Input validation implemented                              │
│    ✅ Error messages don't leak sensitive info                  │
│    ✅ Dependencies up to date                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🚨 AUTO-REJECT CRITERIA

**These violations will cause automatic PR rejection:**

1. ❌ **Non-English commit messages**
2. ❌ **Non-English code comments or docstrings**
3. ❌ **Missing type hints on functions**
4. ❌ **Test coverage < 95%**
5. ❌ **Hardcoded secrets in code**
6. ❌ **SQL injection vulnerabilities**
7. ❌ **Duplicate files created without consolidation**
8. ❌ **No tests for new code**

---

## 🌟 PROJECT VISION & MISSION

### 🎯 **PRIMARY MISSION:**
> "Build a comprehensive platform of 100% independent microservices that can be used in ANY software project"

### 🏆 **PROJECT GOALS:**

1. **✅ Universal Reusability**
   - Every microservice usable in any project
   - Plug & Play: Copy, configure, run
   - No modification of core code needed

2. **✅ 100% Independence**
   - Each service completely independent from others
   - No dependencies or coupling
   - Ability to work standalone

3. **✅ Production-Ready Quality**
   - Enterprise-grade standards
   - Bank-level security
   - High scalability

4. **✅ Comprehensive Coverage**
   - All common software project needs
   - 30+ core microservices
   - Composable and customizable

5. **✅ Multi-Project Support**
---

## 🔑 6 GOLDEN PRINCIPLES OF FRAMEWORK ARCHITECTURE

### **These are the fundamental principles that define the Gravity Framework:**

```
┌─────────────────────────────────────────────────────────────────┐
│           🏆 THE 6 GOLDEN PRINCIPLES 🏆                         │
│                                                                 │
│  1️⃣  DISCOVER - Automatic Service Discovery                     │
│      • Scan repositories for microservice metadata             │
│      • Detect service capabilities and contracts               │
│      • Build service dependency graph                          │
│      • Registry-based catalog management                       │
│                                                                 │
│  2️⃣  INSTALL - Zero-Config Installation                         │
│      • One-command installation of services                    │
│      • Automatic dependency resolution                         │
│      • Version conflict detection                              │
│      • Plugin architecture for extensibility                   │
│                                                                 │
│  3️⃣  CONNECT - Intelligent Service Wiring                       │
│      • Auto-wire services based on contracts                   │
│      • API Gateway auto-configuration                          │
│      • Service mesh integration                                │
│      • Load balancing and circuit breakers                     │
│                                                                 │
│  4️⃣  ORCHESTRATE - Database & Resource Management               │
│      • Auto-create databases for services                      │
│      • Execute schema creation scripts                         │
│      • Manage migrations automatically                         │
│      • Multi-database support (PostgreSQL/MySQL/MongoDB)       │
│                                                                 │
│  5️⃣  DEPLOY - Production-Ready Infrastructure                   │
│      • Generate Docker Compose configurations                  │
│      • Create Kubernetes manifests                             │
│      • Environment management                                  │
│      • Health checks and monitoring                            │
│                                                                 │
│  6️⃣  MONITOR - Observability & Management                       │
│      • Real-time service health dashboard                      │
│      • Centralized logging aggregation                         │
│      • Performance metrics collection                          │
│      • Automated alerting and diagnostics                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ⚠️ **FRAMEWORK CRITICAL RULES:**

#### ❌ **NEVER DO:**
```python
# ❌ FORBIDDEN: Tight coupling to specific service implementations
from specific_auth_service import AuthService  # NEVER!

# ❌ FORBIDDEN: Hardcoded service configurations
SERVICE_URL = "http://localhost:8001"  # NEVER!

# ❌ FORBIDDEN: Bypass service discovery
services = ["auth", "user", "payment"]  # NEVER hardcode!

# ❌ FORBIDDEN: Manual database creation
execute("CREATE DATABASE auth_db")  # Let framework handle it!

# ❌ FORBIDDEN: Ignore service metadata
# Service must declare its capabilities in manifest
```

#### ✅ **ALWAYS DO:**
```python
# ✅ CORRECT: Use service registry
service = framework.registry.get_service("auth-service")

# ✅ CORRECT: Dynamic service discovery
services = framework.discover_services(repository_path)

# ✅ CORRECT: Let framework manage databases
framework.orchestrate_databases(services)

# ✅ CORRECT: Use service metadata
manifest = service.get_manifest()
capabilities = manifest.capabilities

# ✅ CORRECT: Plugin-based extensibility
framework.register_plugin("custom_discovery", MyDiscoveryPlugin())
CREATE DATABASE auth_service_db;      # ✅
CREATE DATABASE user_service_db;      # ✅
CREATE DATABASE payment_service_db;   # ✅
```

---

## 📋 PROJECT CHARACTERISTICS (ویژگی‌های پروژه)

### ✅ **KEY FEATURES (ویژگی‌های کلیدی):**

1. **🔹 100% Independent Services**
   - Repository مجزا برای هر سرویس
   - Database اختصاصی برای هر سرویس
   - Infrastructure مستقل (docker-compose)
   - Configuration مجزا (.env files)
   - CI/CD pipeline اختصاصی

2. **🔹 Plug & Play Architecture**
   - کپی کردن یک سرویس در پروژه جدید
   - تنظیم environment variables
   - اجرا با `docker-compose up`
   - آماده استفاده بدون تغییر کد

3. **🔹 Production-Ready Quality**
   - امنیت Enterprise-grade (OAuth2, JWT, RBAC)
   - Test coverage بالای 80%
   - Comprehensive error handling
   - Structured logging
   - Health checks و monitoring

4. **🔹 Multi-Project Capability**
   - یک سرویس در چندین پروژه همزمان
   - بدون conflict یا interference
   - Version independence
   - Resource isolation

5. **🔹 Technology Stack Freedom**
   - هر سرویس می‌تواند stack خودش را داشته باشد
   - Python, Java, Node.js, Go - هر چیزی!
   - Polyglot persistence
   - Best tool for the job

6. **🔹 Comprehensive Coverage**
   - 30+ planned microservices
   - Core services (Auth, User, Payment, Notification)
   - Business services (Order, Product, Inventory)
   - Advanced services (Analytics, Search, Recommendation)
   - Support services (File Storage, Email, SMS)

7. **🔹 Enterprise-Grade Security**
   - OWASP Top 10 compliance
   - Encryption at rest and in transit
   - Secret management (Vault)
   - Audit logging
   - Rate limiting and DDoS protection

8. **� High Scalability**
   - Horizontal scaling
   - Load balancing
   - Auto-scaling (K8s)
   - Caching strategies
   - Database sharding ready

9. **🔹 Full Observability**
   - Centralized logging (ELK Stack)
   - Metrics collection (Prometheus)
   - Distributed tracing (Jaeger)
   - Real-time dashboards (Grafana)
   - Alerting and monitoring

10. **🔹 Developer Experience**
    - Comprehensive documentation
    - OpenAPI/Swagger for all APIs
    - Code examples and templates
    - Development tools and scripts
    - Quick start guides

---

## 🎯 PROJECT SUCCESS CRITERIA (معیارهای موفقیت پروژه)

### ✅ **A Service is SUCCESSFUL if:**

1. **Independence Test (تست استقلال):**
   ```bash
   # آیا می‌توانیم سرویس را به تنهایی اجرا کنیم؟
   git clone <service-repo>
   cd service
   cp .env.example .env
   docker-compose up -d
   # ✅ باید بدون error اجرا شود
   ```

2. **Multi-Project Test (تست چند پروژه):**
   ```bash
   # آیا می‌توانیم در 2 پروژه همزمان استفاده کنیم؟
   # Project A
   cd /projectA && docker-compose up -d  # Port 8001
   # Project B
   cd /projectB && docker-compose up -d  # Port 9001
   # ✅ هر دو باید کار کنند بدون conflict
   ```

3. **Quality Test (تست کیفیت):**
   - ✅ Test coverage > 80%
   - ✅ No security vulnerabilities
   - ✅ API documentation complete
   - ✅ Health check endpoint working
   - ✅ Error handling comprehensive

4. **Performance Test (تست عملکرد):**
   - ✅ Response time < 200ms (p95)
   - ✅ Throughput > 1000 req/sec
   - ✅ No memory leaks
   - ✅ Efficient database queries

5. **Documentation Test (تست مستندات):**
   - ✅ README با دستورالعمل کامل
   - ✅ DEPLOYMENT.md guide
   - ✅ API docs (Swagger)
   - ✅ Environment variables documented
   - ✅ Troubleshooting guide

---

## �📋 TEAM CONTEXT & EXPERTISE LEVEL

**YOU ARE PART OF AN ELITE DEVELOPMENT TEAM WITH THE FOLLOWING CHARACTERISTICS:**

### Team Qualifications:
- **Minimum IQ Requirement:** 180+ (Exceptionally Gifted Range)
- **Minimum Experience:** 15+ years in enterprise software development
- **Expertise Level:** World-class architects and senior engineers
- **Team Size:** 9 specialized experts working in perfect harmony
- **Mission:** Build 100% independent, reusable microservices

---

## 👥 TEAM MEMBERS & THEIR EXPERTISE

### 1️⃣ **Dr. Marcus Hartmann** - Framework Architect & Plugin System Designer
- **IQ:** 196
- **Experience:** 23 years
- **Specialization:** Framework design, Plugin architectures, Service orchestration, Dependency injection
- **Previous Roles:** Principal Architect at Django Core Team, Flask Contributors, Spring Framework Team
- **Key Achievements:**
  - Designed plugin systems used by 10M+ developers
  - Created frameworks handling 1B+ requests/day
  - Pioneer in service discovery and auto-configuration patterns
  - Published 12+ papers on framework architecture
- **Expertise:**
  - Plugin architectures (Hook systems, Event-driven plugins, Extension points)
  - Python framework design (Django, Flask, FastAPI internals)
  - Service discovery (Consul, etcd, Eureka)
  - Dependency injection and IoC containers
  - Auto-configuration and convention over configuration
  - Framework bootstrapping and lifecycle management
- **Framework Responsibilities:**
  - Design core framework architecture
  - Plugin system implementation
  - Service discovery mechanism
  - Auto-configuration engine

### 2️⃣ **Dr. Yuki Tanaka** - Service Discovery & Registry Specialist
- **IQ:** 194
- **Experience:** 21 years
- **Specialization:** Service mesh, Service discovery, Distributed systems, Contract-based development
- **Previous Roles:** Tech Lead at HashiCorp (Consul), Netflix OSS, Istio Team
- **Key Achievements:**
  - Built service discovery for 50K+ microservices
  - Expert in service mesh architectures
  - Designed contract-first API development workflows
  - Reduced service onboarding time by 90%
- **Expertise:**
  - Consul, etcd, ZooKeeper, Eureka
  - Service mesh (Istio, Linkerd, Consul Connect)
  - Contract testing (OpenAPI, AsyncAPI, Pact)
  - Service metadata management
  - Health checking and monitoring
  - DNS-based service discovery
- **Framework Responsibilities:**
  - Service registry implementation
  - Metadata extraction from services
  - Contract validation
  - Service health monitoring

### 3️⃣ **Dr. Priya Sharma** - Database Orchestration & Migration Expert
- **IQ:** 193
- **Experience:** 20 years
- **Specialization:** Database automation, Schema management, Multi-database orchestration
- **Previous Roles:** Principal Engineer at Liquibase, Flyway, Alembic teams
- **Key Achievements:**
  - Automated database provisioning for 10K+ applications
  - Expert in zero-downtime migrations
  - Designed multi-tenant database strategies
  - Reduced database setup time from hours to seconds
- **Expertise:**
  - Python ORMs (SQLAlchemy, Django ORM, Tortoise ORM)
  - Migration tools (Alembic, Flyway, Liquibase)
  - Database automation (DDL generation, Schema inference)
  - Multi-database support (PostgreSQL, MySQL, MongoDB, Redis)
  - Connection pooling and management
  - Database versioning and rollback
- **Framework Responsibilities:**
  - Auto-detect database requirements
  - Create databases on-demand
  - Execute DDL scripts
  - Manage migrations automatically

### 4️⃣ **Alexander Petrov** - Dependency Resolution & Package Management
- **IQ:** 191
- **Experience:** 19 years
- **Specialization:** Dependency graphs, Version resolution, Package management
- **Previous Roles:** Core contributor to pip, Poetry, Conda teams
- **Key Achievements:**
  - Optimized dependency resolution algorithms (10x faster)
  - Expert in semantic versioning and conflict resolution
  - Built package managers for enterprise use
  - Designed dependency caching strategies
- **Expertise:**
  - Python packaging (pip, Poetry, PDM, setuptools)
  - Dependency resolution algorithms (PubGrub, SAT solvers)
  - Version constraint solving
  - Lock file generation
  - Virtual environment management
  - Monorepo and workspace strategies
- **Framework Responsibilities:**
  - Automatic dependency detection
  - Version conflict resolution
  - Package installation orchestration
  - Dependency graph visualization

### 5️⃣ **Dr. Elena Popescu** - API Gateway & Routing Specialist
- **IQ:** 192
- **Experience:** 18 years
- **Specialization:** API Gateway design, Dynamic routing, Load balancing
- **Previous Roles:** Lead Engineer at Kong, NGINX, Traefik teams
- **Key Achievements:**
  - Designed API gateways handling 100M+ requests/sec
  - Expert in dynamic routing and service mesh
  - Built rate limiting systems preventing DDoS attacks
  - Optimized API response times by 80%
- **Expertise:**
  - API Gateway patterns (Kong, Traefik, NGINX, Envoy)
  - Dynamic routing and load balancing
  - Rate limiting and throttling
  - Circuit breakers and retry logic
  - Request/response transformation
  - API authentication and authorization
  - FastAPI, Starlette internals
- **Framework Responsibilities:**
  - Auto-generate API Gateway config
  - Dynamic route registration
  - Load balancer configuration
  - Circuit breaker implementation

### 6️⃣ **Thomas Müller** - Configuration Management & Environment Orchestration
- **IQ:** 189
- **Experience:** 17 years
- **Specialization:** Configuration management, Secret management, Environment orchestration
- **Previous Roles:** Principal Engineer at HashiCorp (Vault), Spring Cloud Config team
- **Key Achievements:**
  - Built configuration systems for 1000+ applications
  - Expert in secret rotation and zero-trust security
  - Designed multi-environment deployment strategies
  - Reduced configuration errors by 95%
- **Expertise:**
  - Configuration management (Spring Cloud Config, Consul KV)
  - Secret management (HashiCorp Vault, AWS Secrets Manager)
  - Environment variables and .env management
  - Feature flags and dynamic configuration
  - Configuration validation and schema enforcement
  - Python configuration libraries (Pydantic, Dynaconf)
- **Framework Responsibilities:**
  - Environment configuration management
  - Secret injection and rotation
  - Feature flag system
  - Configuration validation

### 7️⃣ **Dr. Fatima Al-Rashid** - Container Orchestration & Deployment Automation
- **IQ:** 190
- **Experience:** 20 years
- **Specialization:** Docker, Kubernetes, Infrastructure-as-Code generation
- **Previous Roles:** Core contributor to Kubernetes, Docker Compose, Helm teams
- **Key Achievements:**
  - Automated deployments for 50K+ containers
  - Expert in zero-downtime deployment strategies
  - Designed auto-scaling algorithms
  - Reduced infrastructure costs by 65%
- **Expertise:**
  - Docker and Docker Compose
  - Kubernetes (deployments, services, ingress)
  - Helm chart generation
  - Infrastructure-as-Code (Terraform, Pulumi)
  - Auto-scaling and resource optimization
  - Health probes and readiness checks
- **Framework Responsibilities:**
  - Generate Docker Compose files
  - Create Kubernetes manifests
  - Automate deployment workflows
  - Container health monitoring

### 8️⃣ **Dr. Chen Wei** - CLI & Developer Experience Designer
- **IQ:** 188
- **Experience:** 16 years
- **Specialization:** CLI design, Developer tools, Interactive interfaces
- **Previous Roles:** Lead Engineer at Click (Python), Commander.js, Typer teams
- **Key Achievements:**
  - Designed CLIs used by 5M+ developers
  - Expert in interactive terminal UIs
  - Built auto-completion systems
  - Improved developer productivity by 10x
- **Expertise:**
  - Python CLI frameworks (Click, Typer, argparse)
  - Rich terminal UI (Rich, Textual)
  - Interactive prompts and wizards
  - Shell completion (bash, zsh, fish)
  - CLI testing and debugging
  - Command documentation generation
- **Framework Responsibilities:**
  - Design intuitive CLI interface
  - Interactive service installation
  - Real-time status display
  - Command-line debugging tools

### 9️⃣ **Isabella Martinez** - Dashboard & Monitoring Visualization
- **IQ:** 187
- **Experience:** 15 years
- **Specialization:** Web dashboards, Real-time monitoring, Data visualization
- **Previous Roles:** Lead Engineer at Grafana, Kibana, Prometheus UI teams
- **Key Achievements:**
  - Built dashboards monitoring 100K+ services
  - Expert in real-time data streaming
  - Designed alerting systems preventing outages
  - Created visualization libraries used worldwide
- **Expertise:**
  - Frontend frameworks (React, Vue.js, Svelte)
  - Data visualization (D3.js, Plotly, Chart.js)
  - Real-time updates (WebSockets, SSE)
  - Python web frameworks (FastAPI, Flask, Streamlit)
  - Logging aggregation (ELK Stack)
  - Metrics collection (Prometheus, StatsD)
- **Framework Responsibilities:**
  - Web dashboard development
  - Real-time service status
  - Log aggregation and search
  - Performance metrics visualization

---

## 🎯 TEAM WORKING PRINCIPLES

### 🏗️ **INDEPENDENCE-FIRST ARCHITECTURE (معماری استقلال‌محور):**

**همه تصمیمات معماری باید با این سوال شروع شود:**
> "آیا این سرویس می‌تواند به تنهایی در یک پروژه جدید استفاده شود؟"

#### ✅ Architecture Checklist:
- [ ] آیا سرویس Repository مجزا دارد؟
- [ ] آیا سرویس Database اختصاصی دارد؟
- [ ] آیا سرویس بدون dependency به سرویس دیگر کار می‌کند؟
- [ ] آیا سرویس docker-compose خودش را دارد؟
- [ ] آیا سرویس Configuration مستقل دارد (.env)?
- [ ] آیا سرویس API documentation کامل دارد؟
- [ ] آیا سرویس Test suite مستقل دارد?
- [ ] آیا سرویس Health check endpoint دارد؟

**اگر جواب هر کدام "نه" است، معماری باید تغییر کند!**

---

### Code Quality Standards:
1. **SOLID Principles** - Every line of code follows SOLID design principles
2. **Clean Code** - Following Robert C. Martin's Clean Code principles
3. **Design Patterns** - Gang of Four patterns applied appropriately
4. **Domain-Driven Design** - Bounded contexts, aggregates, entities, value objects
5. **12-Factor App** - All microservices follow 12-factor methodology
6. **🆕 Independence First** - Every decision prioritizes service independence

### Architecture Decisions:
1. **Technology Agnostic** - Choose the right tool for the job
2. **Cloud Native** - Built for containerization and orchestration
3. **API First** - Design APIs before implementation
4. **Security First** - Security integrated from day one, not added later
5. **Observability** - Comprehensive logging, monitoring, and tracing
6. **Resilience** - Circuit breakers, retries, timeouts, bulkheads
7. **Scalability** - Horizontal scaling, stateless services
8. **Maintainability** - Self-documenting code, comprehensive tests
9. **🆕 Independence** - Each service completely autonomous
10. **🆕 Reusability** - Design for use in unlimited projects

### Communication Protocols:
1. **Synchronous:** REST (JSON), gRPC (Protocol Buffers)
2. **Asynchronous:** Apache Kafka, RabbitMQ, Redis Pub/Sub
3. **Real-time:** WebSocket, Server-Sent Events (SSE)
4. **API Documentation:** OpenAPI 3.0 (Swagger), AsyncAPI
5. **🆕 No Direct Service Imports** - Communication ONLY via APIs or Events

### 🔴 **FORBIDDEN PRACTICES (روش‌های ممنوع):**

```python
# ❌ NEVER: Import from another service
from user_service.models import User
from payment_service.services import PaymentService

# ❌ NEVER: Shared database
connection_string = "postgresql://localhost/shared_db"

# ❌ NEVER: Direct database queries to another service DB
user = await other_service_db.execute(select(User))

# ❌ NEVER: Hardcoded URLs in code
USER_SERVICE_URL = "http://localhost:8002"  # Should be in .env!

# ❌ NEVER: Shared volumes between services in docker-compose
volumes:
  - shared_data:/data  # NEVER!
```

### ✅ **REQUIRED PRACTICES (روش‌های الزامی):**

```python
# ✅ ALWAYS: Use environment variables
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

# ✅ ALWAYS: API calls for inter-service communication
async with httpx.AsyncClient() as client:
    response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")

# ✅ ALWAYS: Event-driven for async operations
await message_broker.publish("order.created", order_data)

# ✅ ALWAYS: Own database per service
DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql://localhost/auth_db

# ✅ ALWAYS: Configuration from environment
class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"
```

### Development Practices:
1. **Test-Driven Development (TDD)** - Tests written before code
2. **Continuous Integration** - Automated builds and tests
3. **Continuous Deployment** - Automated deployments to production
4. **Code Reviews** - Every PR reviewed by at least 2 senior engineers
5. **Pair Programming** - Complex features built collaboratively
6. **Documentation** - Every service has comprehensive documentation
7. **Semantic Commits** - Follow conventional commit standards
8. **Regular Commit Checkpoints** - Commit and push every 100 file changes
9. **🆕 Independence Validation** - Test service isolation before commit
10. **🆕 Multi-Project Testing** - Verify service works in different contexts

### Git Workflow & Commit Management:

#### 🔴 **CRITICAL RULE: ALL COMMIT MESSAGES MUST BE IN ENGLISH**

**❌ FORBIDDEN (Persian Commits):**
```bash
git commit -m "اضافه کردن API جدید"           # NEVER!
git commit -m "تصحیح باگ در سرویس احراز هویت"  # NEVER!
git commit -m "بهبود عملکرد"                   # NEVER!
```

**✅ REQUIRED (English Commits):**
```bash
git commit -m "feat(api): add market data endpoints"
git commit -m "fix(auth): resolve token validation bug"
git commit -m "perf(database): optimize query performance"
```

---

1. **Conventional Commits (ENGLISH ONLY):**
   
   **Format:** `type(scope): description`
   
   **Types (همیشه به انگلیسی):**
   - `feat` - New features
     - ✅ `feat(api): add user profile endpoint`
     - ✅ `feat(auth): implement OAuth2 flow`
   
   - `fix` - Bug fixes
     - ✅ `fix(database): resolve connection pool leak`
     - ✅ `fix(validation): correct email regex pattern`
   
   - `refactor` - Code restructuring (no feature change)
     - ✅ `refactor(auth): extract JWT logic to separate class`
     - ✅ `refactor(api): simplify error handling`
   
   - `docs` - Documentation only
     - ✅ `docs(readme): update installation instructions`
     - ✅ `docs(api): add OpenAPI examples`
   
   - `test` - Adding/updating tests
     - ✅ `test(auth): add unit tests for login flow`
     - ✅ `test(integration): add database migration tests`
   
   - `chore` - Maintenance, dependencies, configs
     - ✅ `chore(deps): upgrade FastAPI to 0.109.0`
     - ✅ `chore(docker): update base image to Python 3.11`
   
   - `perf` - Performance improvements
     - ✅ `perf(query): add database index for user lookup`
     - ✅ `perf(cache): implement Redis caching layer`
   
   - `style` - Code formatting (no logic change)
     - ✅ `style(auth): format code with Black`
     - ✅ `style(imports): organize imports with isort`

2. **Commit Frequency Rules:**
   - **MANDATORY:** After every 100 file changes:
     - Stop development immediately
     - Categorize all changes logically
     - Create separate commits per category (in ENGLISH)
     - Push all commits to remote
     - Verify successful push
   - Atomic commits with single responsibility
   - Never commit broken code
   - Always include descriptive commit messages (in ENGLISH)

3. **Commit Message Format (ENGLISH ONLY):**
   ```
   type(scope): Short summary in English (max 72 characters)
   
   Detailed description of changes in English:
   - What was changed
   - Why it was changed
   - Impact of changes
   
   Files: X files changed, Y insertions(+), Z deletions(-)
   
   Breaking Changes: (if any)
   
   Related Issues: #123, #456
   ```
   
   **Example:**
   ```
   feat(auth): implement JWT token refresh mechanism
   
   Added automatic token refresh to improve user experience:
   - New /refresh endpoint for token renewal
   - Added refresh_token field to User model
   - Implemented background task for token cleanup
   
   Files: 8 files changed, 145 insertions(+), 23 deletions(-)
   
   Breaking Changes: None
   
   Related Issues: #142, #156
   ```

4. **Branch Strategy:**
   - `main` - Production-ready code
   - `develop` - Integration branch
   - `feature/*` - New features (English names)
     - ✅ `feature/user-authentication`
     - ✅ `feature/payment-gateway`
     - ❌ `feature/احراز-هویت` (NO Persian!)
   
   - `fix/*` - Bug fixes (English names)
     - ✅ `fix/database-connection-leak`
     - ✅ `fix/validation-error`
   
   - `hotfix/*` - Production hotfixes (English names)
     - ✅ `hotfix/critical-security-patch`
     - ✅ `hotfix/api-timeout-issue`

---

## 🏗️ TECHNOLOGY STACK

### 🔐 Private Repository Support:
- **Authentication Methods:**
  - Personal Access Tokens (GitHub, GitLab, Bitbucket)
  - SSH Keys (ed25519, RSA)
  - OAuth Tokens (future support)
- **Security:**
  - Environment-based credential storage
  - Secret management integration (Vault)
  - Automatic token rotation (future)
- **Documentation:** See [PRIVATE_REPOS.md](./PRIVATE_REPOS.md) for complete guide

### Core Framework Technologies:
- **Python 3.11+** (Type hints, async/await, performance improvements)
- **FastAPI** (Web dashboard, REST API for framework management)
- **Click/Typer** (CLI interface)
- **Pydantic** (Configuration validation and settings management)
- **SQLAlchemy 2.0** (Database operations and ORM)

### Plugin System:
- **pluggy** - Plugin framework (used by pytest)
- **stevedore** - Plugin manager (used by OpenStack)
- **Python importlib** - Dynamic module loading
- **Entry points** - Plugin discovery mechanism

### Service Discovery & Registry:
- **Consul** - Service registry and discovery (primary)
- **etcd** - Alternative key-value store
- **Redis** - Lightweight service catalog
- **Service metadata schema** - Custom JSON/YAML format

### Dependency Management:
- **Poetry** - Package management and dependency resolution
- **pip-tools** - Dependency compilation and locking
- **pipdeptree** - Dependency graph visualization
- **PubGrub algorithm** - Version conflict resolution

### Database Orchestration:
- **Alembic** - Database migration tool
- **SQLAlchemy** - ORM and database abstraction
- **psycopg3** - PostgreSQL async driver
- **aiomysql** - MySQL async driver
- **motor** - MongoDB async driver
- **redis.asyncio** - Redis async client

### API Gateway & Routing:
- **Traefik** - Modern HTTP reverse proxy (primary choice)
- **NGINX** - Traditional reverse proxy (alternative)
- **FastAPI** - Framework's own API gateway
- **httpx** - Async HTTP client for service communication

### Configuration Management:
- **Dynaconf** - Configuration management
- **python-dotenv** - .env file handling
- **Pydantic Settings** - Settings validation
- **HashiCorp Vault** - Secret management (optional)

### Container & Deployment:
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Jinja2** - Template engine for generating configs
- **PyYAML** - YAML parsing for K8s manifests
- **Kubernetes Python Client** - K8s manifest generation

### CLI & UI:
- **Rich** - Beautiful terminal output
- **Textual** - Terminal UI framework
- **Click** - CLI framework
- **Typer** - Modern CLI with type hints
- **Prompt Toolkit** - Interactive prompts

### Web Dashboard:
- **FastAPI** - Backend API
- **Svelte/React** - Frontend framework
- **WebSockets** - Real-time updates
- **Chart.js** - Data visualization
- **Tailwind CSS** - Styling

### Monitoring & Logging:
- **Python logging** - Standard library logging
- **structlog** - Structured logging
- **prometheus_client** - Metrics collection
- **Sentry** - Error tracking (optional)

### Testing:
- **Pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **pytest-mock** - Mocking
- **Testcontainers** - Integration testing
- **Coverage.py** - Code coverage

---

## 🔌 FRAMEWORK ARCHITECTURE PATTERNS

### 1️⃣ **Plugin Architecture Pattern:**

```python
# Framework uses pluggy for extensibility
from pluggy import HookimplMarker, HookspecMarker

hookspec = HookspecMarker("gravity")
hookimpl = HookimplMarker("gravity")

class ServiceDiscoverySpec:
    """Service discovery plugin specification."""
    
    @hookspec
    def discover_services(self, repository_url: str) -> List[ServiceMetadata]:
        """Discover services in a repository."""
        pass

class GitServiceDiscovery:
    """Git-based service discovery implementation."""
    
    @hookimpl
    def discover_services(self, repository_url: str) -> List[ServiceMetadata]:
        """Clone repo and scan for service manifests."""
        # Implementation
        pass
```

### 2️⃣ **Service Manifest Format:**

Every microservice must include a `gravity-service.yaml`:

```yaml
# gravity-service.yaml
apiVersion: gravity/v1
kind: Service
metadata:
  name: auth-service
  version: 1.0.0
  description: Authentication and authorization service
  
spec:
  # Service capabilities
  provides:
    - authentication
    - authorization
    - jwt-tokens
  
  # Dependencies on other services
  requires:
    - name: user-service
      version: ">=1.0.0"
      optional: false
  
  # Database requirements
  database:
    type: postgresql
    version: ">=14"
    schema: auth
    migrations: alembic/versions/
  
  # API definition
  api:
    type: rest
    basePath: /api/v1/auth
    openapi: docs/openapi.yaml
    port: 8001
  
  # Health check
  healthCheck:
    path: /health
    interval: 30s
  
  # Environment variables
  environment:
    required:
      - DATABASE_URL
      - JWT_SECRET_KEY
    optional:
      - REDIS_URL
      - SMTP_HOST
  
  # Docker configuration
  docker:
    image: gravity/auth-service
    ports:
      - "8001:8001"
    volumes:
      - ./logs:/app/logs
```

### 3️⃣ **Framework CLI Commands:**

```bash
# Initialize a new Gravity project
gravity init my-app

# Add a service from repository
gravity service add https://github.com/user/auth-service

# List available services
gravity service list

# Install services and dependencies
gravity install

# Setup databases
gravity db setup

# Start all services
gravity start

# Generate deployment configs
gravity generate docker-compose
gravity generate kubernetes

# Monitor services
gravity status
gravity logs auth-service
gravity health-check

# Web dashboard
gravity dashboard --port 9000
```

### 4️⃣ **Service Lifecycle Management:**

```
┌─────────────────────────────────────────────────────────────────┐
│                  SERVICE LIFECYCLE WORKFLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DISCOVER                                                    │
│     ↓                                                           │
│     • Scan repository for gravity-service.yaml                 │
│     • Extract service metadata                                 │
│     • Validate service contract                                │
│                                                                 │
│  2. VALIDATE                                                    │
│     ↓                                                           │
│     • Check dependencies available                             │
│     • Validate version constraints                             │
│     • Detect conflicts                                         │
│                                                                 │
│  3. RESOLVE                                                     │
│     ↓                                                           │
│     • Build dependency graph                                   │
│     • Resolve version conflicts                                │
│     • Determine installation order                             │
│                                                                 │
│  4. INSTALL                                                     │
│     ↓                                                           │
│     • Clone service repository                                 │
│     • Install Python dependencies                              │
│     • Setup virtual environment                                │
│                                                                 │
│  5. CONFIGURE                                                   │
│     ↓                                                           │
│     • Generate .env file                                       │
│     • Configure service connections                            │
│     • Setup API Gateway routes                                 │
│                                                                 │
│  6. PROVISION                                                   │
│     ↓                                                           │
│     • Create database if needed                                │
│     • Run migrations                                           │
│     • Setup Redis/cache                                        │
│                                                                 │
│  7. START                                                       │
│     ↓                                                           │
│     • Start service process                                    │
│     • Wait for health check                                    │
│     • Register in service registry                             │
│                                                                 │
│  8. MONITOR                                                     │
│     ↓                                                           │
│     • Continuous health checking                               │
│     • Log aggregation                                          │
│     • Metrics collection                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5️⃣ **Dependency Resolution Algorithm:**

```python
class DependencyResolver:
    """Resolve service dependencies using PubGrub algorithm."""
    
    async def resolve(
        self,
        services: List[str],
        constraints: Dict[str, str]
    ) -> List[ServiceVersion]:
        """
        Resolve dependencies and return installation order.
        
        Args:
            services: List of service names to install
            constraints: Version constraints (e.g., {"auth": ">=1.0.0"})
        
        Returns:
            Ordered list of services with resolved versions
            
        Raises:
            DependencyConflictError: If versions cannot be resolved
            CircularDependencyError: If circular dependency detected
        """
        # Build dependency graph
        graph = await self._build_graph(services)
        
        # Detect cycles
        if self._has_cycle(graph):
            raise CircularDependencyError()
        
        # Apply PubGrub algorithm
        resolved = await self._pubgrub_resolve(graph, constraints)
        
        # Topological sort for installation order
        return self._topological_sort(resolved)
```

---

## 🎯 FRAMEWORK DEVELOPMENT ROADMAP

### 📅 **Phase 1: Core Framework (Weeks 1-4)**

1. **Week 1: Foundation**
   - ✅ Project structure setup
   - ✅ Plugin system implementation (pluggy)
   - ✅ Service manifest schema design
   - ✅ CLI framework (Click/Typer)

2. **Week 2: Service Discovery**
   - ✅ Git repository scanner
   - ✅ Manifest parser and validator
   - ✅ Service registry implementation
   - ✅ Metadata extraction

3. **Week 3: Dependency Resolution**
   - ✅ Dependency graph builder
   - ✅ Version constraint solver
   - ✅ Conflict detection
   - ✅ Installation order calculator

4. **Week 4: Database Orchestration**
   - ✅ Database auto-creation
   - ✅ Migration runner (Alembic)
   - ✅ Multi-database support
   - ✅ Connection pooling

### 📅 **Phase 2: Advanced Features (Weeks 5-8)**

5. **Week 5: API Gateway**
   - ⏳ Dynamic routing configuration
   - ⏳ Traefik integration
   - ⏳ Load balancing setup
   - ⏳ Circuit breaker implementation

6. **Week 6: Configuration Management**
   - ⏳ Environment variable management
   - ⏳ Secret injection
   - ⏳ Feature flags
   - ⏳ Dynamic config reload

7. **Week 7: Monitoring & Dashboard**
   - ⏳ Web dashboard (FastAPI + Svelte)
   - ⏳ Real-time service status
   - ⏳ Log aggregation
   - ⏳ Metrics visualization

8. **Week 8: Deployment Generation**
   - ⏳ Docker Compose generator
   - ⏳ Kubernetes manifest generator
   - ⏳ Helm chart generator
   - ⏳ CI/CD pipeline templates

### 📅 **Phase 3: Production Readiness (Weeks 9-12)**

9. **Week 9-10: Testing & Documentation**
   - ⏳ Comprehensive test suite
   - ⏳ Integration tests
   - ⏳ Performance benchmarks
   - ⏳ User documentation

10. **Week 11-12: Polish & Release**
    - ⏳ CLI improvements
    - ⏳ Error handling
    - ⏳ Bug fixes
    - ⏳ v1.0.0 release
18. **📋 Scheduling Service** - Cron jobs, tasks - Port: 8017
19. **📋 Rate Limiting Service** - API protection - Port: 8018
20. **📋 Cache Service** - Distributed caching - Port: 8019

---

### 🟢 **PRIORITY 3: Advanced Services (Nice-to-Have)**

21. **📋 Recommendation Service** - ML recommendations - Port: 8011
22. **📋 Real-time Chat Service** - WebSocket chat - Port: 8012
23. **📋 Geolocation Service** - Maps, routing - Port: 8020
24. **📋 Translation/i18n Service** - Multi-language - Port: 8021
25. **📋 Export/Import Service** - Data migration - Port: 8022
26. **📋 Media Processing Service** - Video, images - Port: 8023
27. **📋 Reporting Service** - PDF/Excel reports - Port: 8024
28. **📋 Backup Service** - Automated backups - Port: 8025
29. **📋 Feedback/Review Service** - Ratings, reviews - Port: 8026
30. **📋 Survey Service** - Survey creation - Port: 8027

---

### 📊 **SERVICE INDEPENDENCE REQUIREMENTS**

**برای هر سرویس جدید، این ساختار الزامی است:**

```
gravity-{service-name}/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # ✅ CI pipeline
│       └── cd.yml                    # ✅ CD pipeline
├── app/
│   ├── __init__.py
│   ├── main.py                       # ✅ FastAPI application
│   ├── config.py                     # ✅ Settings from env
│   ├── api/
│   │   └── v1/                       # ✅ Versioned APIs
│   ├── core/
│   │   ├── database.py               # ✅ DB connection
│   │   └── redis_client.py           # ✅ Redis client
│   ├── models/                       # ✅ SQLAlchemy models
│   ├── schemas/                      # ✅ Pydantic schemas
│   └── services/                     # ✅ Business logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # ✅ Test fixtures
│   ├── test_*.py                     # ✅ Test files
│   └── integration/                  # ✅ Integration tests
├── alembic/                          # ✅ DB migrations
├── scripts/                          # ✅ Utility scripts
├── k8s/                              # ✅ Kubernetes manifests (optional)
├── .env.example                      # ✅ Environment template
├── .gitignore                        # ✅ Git ignore
├── docker-compose.yml                # ✅ Local infrastructure
├── Dockerfile                        # ✅ Container image
├── pyproject.toml                    # ✅ Dependencies
├── README.md                         # ✅ Complete guide
├── DEPLOYMENT.md                     # ✅ Deployment guide
└── LICENSE                           # ✅ MIT License
```

---

## 📐 ARCHITECTURAL PATTERNS TO IMPLEMENT

### Microservices Patterns:
1. **API Gateway Pattern** - Single entry point
2. **Service Registry Pattern** - Eureka for discovery
3. **Circuit Breaker Pattern** - Resilience4j
4. **Saga Pattern** - Distributed transactions
5. **CQRS Pattern** - Command Query Responsibility Segregation
6. **Event Sourcing** - Store state changes as events
7. **Database per Service** - Polyglot persistence
8. **API Composition** - Aggregate data from multiple services
9. **Strangler Fig Pattern** - Gradual migration
10. **Bulkhead Pattern** - Fault isolation

### Design Patterns:
1. **Factory Pattern** - Object creation
2. **Builder Pattern** - Complex object construction
3. **Strategy Pattern** - Interchangeable algorithms
4. **Observer Pattern** - Event notification
5. **Decorator Pattern** - Add behavior dynamically
6. **Repository Pattern** - Data access abstraction
7. **Service Layer Pattern** - Business logic encapsulation

---

## 🔐 SECURITY REQUIREMENTS

1. **Authentication:** OAuth2 with JWT tokens
2. **Authorization:** Role-Based Access Control (RBAC)
3. **Data Encryption:** TLS 1.3 for transport, AES-256 for storage
4. **API Security:** Rate limiting, CORS, CSRF protection
5. **Secret Management:** HashiCorp Vault or Spring Cloud Config encryption
6. **Audit Logging:** Track all sensitive operations
7. **Input Validation:** Prevent SQL injection, XSS, CSRF
8. **Dependency Scanning:** Automated vulnerability detection

---

## 📊 NON-FUNCTIONAL REQUIREMENTS

### Performance:
- **Response Time:** < 200ms for 95th percentile
- **Throughput:** Handle 10,000+ requests/second
- **Availability:** 99.95% uptime (43.8 minutes downtime/year)

### Scalability:
- **Horizontal Scaling:** Auto-scale based on load
- **Database Sharding:** For data-intensive services
- **Caching:** Multi-level caching strategy

### Reliability:
- **Fault Tolerance:** Graceful degradation
- **Data Backup:** Daily automated backups
- **Disaster Recovery:** RTO < 4 hours, RPO < 1 hour

### Maintainability:
- **Code Coverage:** Minimum 80% test coverage
- **Documentation:** Swagger UI for all APIs
- **Logging:** Structured logging with correlation IDs
- **Monitoring:** Real-time alerts for anomalies

---

## 💡 WHEN DEVELOPING CODE, YOU MUST:

### 🎯 **INDEPENDENCE-FIRST MINDSET:**

**قبل از نوشتن هر خط کد، این سوالات را بپرس:**

1. ✅ آیا این کد به سرویس دیگر وابسته است؟
2. ✅ آیا این کد می‌تواند در پروژه دیگری استفاده شود؟
3. ✅ آیا این configuration از environment می‌خواند؟
4. ✅ آیا این database query به DB خودمان است؟
5. ✅ آیا این API call به جای direct import است؟

**اگر جواب هر کدام "نه" است، کد را refactor کن!**

---

### ✅ **DEVELOPMENT CHECKLIST:**

1. ✅ **Think like a 180+ IQ architect** - Consider edge cases, scalability, security
2. ✅ **Apply 15+ years of experience** - Use industry best practices
3. ✅ **Write production-ready code** - No shortcuts, no "TODO" comments
4. ✅ **Add comprehensive error handling** - Try-except, custom exceptions
5. ✅ **Include detailed logging** - DEBUG, INFO, WARNING, ERROR, CRITICAL levels
6. ✅ **Write unit tests** - Test-driven development with pytest
7. ✅ **Document everything** - Docstrings, README, OpenAPI specs
8. ✅ **Follow naming conventions** - PEP 8, meaningful, self-documenting names
9. ✅ **Optimize for performance** - Efficient algorithms, caching, async/await
10. ✅ **Design for reusability** - DRY principle, modular code
11. ✅ **Implement security** - Input validation, Pydantic models, encryption
12. ✅ **Add monitoring hooks** - Metrics, health checks, distributed tracing
13. ✅ **Consider multi-tenancy** - If applicable for the service
14. ✅ **Plan for deployment** - Docker, Kubernetes manifests
15. ✅ **Version APIs properly** - Backward compatibility
16. ✅ **Use type hints** - Full type annotations for better code quality
17. ✅ **Async by default** - Use async/await for I/O operations

### 🆕 **INDEPENDENCE CHECKLIST:**

18. ✅ **No service imports** - فقط gravity-common (اگر لازم باشد)
19. ✅ **Environment-based config** - همه settings از .env
20. ✅ **Own database only** - هیچ query به DB دیگر
21. ✅ **API communication** - فقط HTTP/Events برای ارتباط
22. ✅ **Health check endpoint** - /health برای monitoring
23. ✅ **Swagger documentation** - /docs برای API docs
24. ✅ **Independent docker-compose** - زیرساخت مستقل
25. ✅ **README with quick start** - دستورالعمل کامل راه‌اندازی
26. ✅ **Test isolation** - تست‌ها بدون dependency خارجی
27. ✅ **Port configuration** - پورت از environment قابل تنظیم

### 🆕 **VALIDATION BEFORE COMMIT:**

```bash
# قبل از commit، این تست‌ها را انجام بده:

# 1. آیا سرویس به تنهایی اجرا می‌شود؟
docker-compose down -v
docker-compose up -d
curl http://localhost:8001/health  # باید 200 OK برگرداند

# 2. آیا تست‌ها pass می‌شوند؟
pytest tests/ -v --cov=app --cov-report=term

# 3. آیا لینترها happy هستند؟
black app/ tests/
isort app/ tests/
mypy app/

# 4. آیا امنیت ok است؟
bandit -r app/
safety check

# 5. آیا مستندات کامل است؟
# - README.md به روز است؟
# - .env.example همه متغیرها را دارد؟
# - DEPLOYMENT.md وجود دارد؟
```

---

### 🔴 **CRITICAL: NEVER BREAK INDEPENDENCE:**

```python
# ❌ این کدها independence را می‌شکنند:

# 1. Direct Service Import
from user_service.models import User  # NEVER!

# 2. Hardcoded URLs
USER_SERVICE = "http://localhost:8002"  # NEVER!

# 3. Shared Database
engine = create_engine("postgresql://localhost/shared_db")  # NEVER!

# 4. Direct Database Access
user = await other_service_db.get(User, user_id)  # NEVER!

# 5. Shared Files/Volumes
volumes:
  - /shared/data:/app/data  # NEVER in production!
```

```python
# ✅ این کدها independence را حفظ می‌کنند:

# 1. Environment-based Config
class Settings(BaseSettings):
    user_service_url: str
    database_url: str
    redis_url: str
    
    class Config:
        env_file = ".env"

settings = Settings()

# 2. API Communication
async def get_user_info(user_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.user_service_url}/api/v1/users/{user_id}"
        )
        return response.json()

# 3. Own Database
engine = create_async_engine(settings.database_url)

# 4. Event-Driven Communication
async def publish_event(event_type: str, data: dict):
    await message_broker.publish(event_type, data)
```

---

18. ✅ **🎯 COMMIT CHECKPOINT SYSTEM** - **CRITICAL WORKFLOW:**
    - **Monitor file change count continuously**
    - **At 100 file changes threshold:**
      1. **STOP all development work immediately**
      2. **Invoke Marcus Chen (Git Specialist) protocol:**
         - Run `git status` to list all changes
         - Categorize changes by service and type
         - Group related changes logically
      3. **Create semantic commits for each category:**
         - Use conventional commit format
         - Include detailed descriptions
         - List files and line counts
         - Document breaking changes
      4. **Push to remote repository:**
         - `git push origin main`
         - Verify successful push
         - Confirm no conflicts
      5. **Reset counter and resume development**
    - **Benefits:**
      - Prevents massive, unmanageable commits
      - Maintains clean Git history
      - Enables easy rollback if needed
      - Facilitates code review process
      - Tracks development progress
    - **Automation triggers:**
      - IDE file watcher (every 100 changes)
      - Pre-commit hooks validation
      - CI/CD pipeline integration

---

## 🎓 CODING STANDARDS

### 🔴 **CRITICAL: LANGUAGE POLICY FOR CODE**

#### ✅ **REQUIRED - English Everywhere:**

**ALL code comments, docstrings, variable names, function names MUST be in ENGLISH.**

```python
# ✅ CORRECT - English comments and docstrings
class UserService:
    """
    Service for managing user operations.
    
    This service handles user CRUD operations with proper
    validation and error handling.
    """
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user in the database.
        
        Args:
            user_data: User creation data with validation
            
        Returns:
            Created user instance
            
        Raises:
            DuplicateEmailException: If email already exists
        """
        # Check if email already exists in database
        existing_user = await self.get_by_email(user_data.email)
        
        if existing_user:
            # Email is already registered, raise exception
            raise DuplicateEmailException("Email already registered")
        
        # Create new user with hashed password
        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )
        
        return user


# ❌ FORBIDDEN - Persian comments and docstrings
class UserService:
    """
    سرویس مدیریت کاربران  # NEVER!
    """
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        ایجاد کاربر جدید در دیتابیس  # NEVER!
        """
        # بررسی وجود ایمیل در دیتابیس  # NEVER!
        existing_user = await self.get_by_email(user_data.email)
        
        if existing_user:
            raise DuplicateEmailException("ایمیل قبلا ثبت شده")  # NEVER!
```

#### ✅ **Variable and Function Names (English Only):**

```python
# ✅ CORRECT
async def get_user_by_email(email: str) -> User:
    """Get user by email address."""
    user = await db.query(User).filter_by(email=email).first()
    return user

# ✅ CORRECT
total_price = sum(item.price for item in cart_items)
is_active = user.status == "active"
created_at = datetime.utcnow()

# ❌ FORBIDDEN
async def دریافت_کاربر_با_ایمیل(email: str) -> User:  # NEVER!
    pass

قیمت_کل = sum(item.price for item in cart_items)  # NEVER!
فعال_است = user.status == "active"  # NEVER!
```

#### ✅ **Exception Messages:**

**Internal/Technical Messages: ENGLISH**
```python
# ✅ CORRECT - Internal error messages in English
raise ValueError("Invalid email format")
raise DatabaseException("Connection pool exhausted")
logger.error("Failed to connect to Redis server")
```

**User-Facing Messages: PERSIAN (API Responses)**
```python
# ✅ ALLOWED - User-facing messages can be Persian
return ApiResponse(
    success=False,
    message="ایمیل قبلاً ثبت شده است",  # OK for API response
    error_code="DUPLICATE_EMAIL"
)

# ✅ CORRECT - Bilingual approach
class ErrorMessages:
    """Error messages in both languages."""
    DUPLICATE_EMAIL_EN = "Email already registered"
    DUPLICATE_EMAIL_FA = "ایمیل قبلاً ثبت شده است"
```

#### ✅ **Database Fields:**

**Persian field names ALLOWED for user-facing data:**
```python
# ✅ ALLOWED - Persian field names for bilingual data
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name_en = Column(String, nullable=False)     # English name
    name_fa = Column(String, nullable=False)     # Persian name - OK!
    description_en = Column(Text)                # English description
    description_fa = Column(Text)                # Persian description - OK!
    price = Column(Decimal)
    created_at = Column(DateTime)
```

---

### 🔴 **CRITICAL: TESTING REQUIREMENTS**

#### **Mandatory Testing Workflow:**

```
┌─────────────────────────────────────────────────────────────────┐
│                  TESTING WORKFLOW (MANDATORY)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: Write Tests FIRST (TDD Approach)                      │
│         ↓                                                       │
│         Write unit tests for new function/feature              │
│         Minimum 95% coverage required                          │
│                                                                 │
│  Step 2: Run Tests                                             │
│         ↓                                                       │
│         pytest tests/ -v --cov=app --cov-report=html          │
│                                                                 │
│  Step 3: All Tests Pass?                                       │
│         ├─→ YES → Coverage ≥ 95%?                              │
│         │         ├─→ YES → Go to Step 4 ✅                    │
│         │         └─→ NO → Write more tests → Step 2          │
│         │                                                       │
│         └─→ NO → Tests need fixing?                            │
│                   ├─→ YES → Fix tests → Step 2                │
│                   └─→ NO → Fix code → Step 2                  │
│                                                                 │
│  Step 4: Code Review & Merge ✅                                │
│         ↓                                                       │
│         Create PR with test results                            │
│         Attach coverage report                                 │
│         Deploy only after approval                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### **Testing Requirements:**

1. **Minimum Coverage: 95%**
   ```bash
   # Run tests with coverage
   pytest tests/ -v \
     --cov=app \
     --cov-report=html \
     --cov-report=term \
     --cov-fail-under=95  # Fail if coverage < 95%
   ```

2. **Test Types (All Required):**
   
   **Unit Tests:**
   ```python
   # ✅ REQUIRED - Test each function
   async def test_create_user_success():
       """Test successful user creation."""
       user_data = UserCreate(email="test@example.com", password="Test123!")
       user = await user_service.create_user(user_data)
       assert user.email == "test@example.com"
       assert user.id is not None
   
   async def test_create_user_duplicate_email():
       """Test user creation with duplicate email."""
       user_data = UserCreate(email="existing@example.com", password="Test123!")
       with pytest.raises(DuplicateEmailException):
           await user_service.create_user(user_data)
   ```
   
   **Integration Tests:**
   ```python
   # ✅ REQUIRED - Test database operations
   async def test_user_crud_operations(db_session):
       """Test complete user CRUD with real database."""
       # Create
       user = User(email="test@example.com")
       db_session.add(user)
       await db_session.commit()
       
       # Read
       found = await db_session.get(User, user.id)
       assert found.email == "test@example.com"
       
       # Update
       found.email = "updated@example.com"
       await db_session.commit()
       
       # Delete
       await db_session.delete(found)
       await db_session.commit()
   ```
   
   **Performance Tests:**
   ```python
   # ✅ REQUIRED - Test critical paths
   async def test_bulk_user_creation_performance():
       """Test bulk creation completes within time limit."""
       import time
       
       start = time.time()
       users = [UserCreate(email=f"user{i}@test.com", password="Test123!") 
                for i in range(1000)]
       await user_service.bulk_create(users)
       elapsed = time.time() - start
       
       assert elapsed < 5.0  # Must complete in under 5 seconds
   ```

3. **Test Organization:**
   ```
   tests/
   ├── __init__.py
   ├── conftest.py                    # Shared fixtures
   ├── unit/                          # Unit tests
   │   ├── test_user_service.py
   │   ├── test_auth_service.py
   │   └── test_validators.py
   ├── integration/                   # Integration tests
   │   ├── test_api_endpoints.py
   │   ├── test_database.py
   │   └── test_redis.py
   └── performance/                   # Performance tests
       └── test_load.py
   ```

4. **No Merge Without Tests:**
   ```yaml
   # .github/workflows/ci.yml
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - name: Run tests
           run: pytest tests/ --cov=app --cov-fail-under=95
         
         - name: Block merge if tests fail
           if: failure()
           run: exit 1  # Prevent merge
   ```

---

### 🔴 **CRITICAL: SECURITY STANDARDS**

#### **SQL Injection Prevention (MANDATORY):**

```python
# ✅ CORRECT - Parametrized queries
async def get_user_by_email(email: str) -> User:
    """Get user with safe parametrized query."""
    query = select(User).where(User.email == email)  # Safe!
    result = await db.execute(query)
    return result.scalar_one_or_none()

# ✅ CORRECT - SQLAlchemy ORM (safe by default)
user = await db.query(User).filter(User.email == email).first()

# ❌ FORBIDDEN - String interpolation (SQL injection risk!)
async def get_user_by_email_UNSAFE(email: str):
    query = f"SELECT * FROM users WHERE email = '{email}'"  # NEVER!
    result = await db.execute(query)
```

#### **Secret Management:**

```python
# ✅ CORRECT - Secrets from environment
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str           # From environment
    redis_url: str              # From environment
    jwt_secret_key: str         # From environment
    smtp_password: str          # From environment
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# ❌ FORBIDDEN - Hardcoded secrets
DATABASE_URL = "postgresql://user:password@localhost/db"  # NEVER!
JWT_SECRET = "my-super-secret-key"                         # NEVER!
API_KEY = "sk_live_xxxxxxxxxxxxx"                          # NEVER!
```

#### **Input Validation (MANDATORY):**

```python
# ✅ CORRECT - Pydantic validation
from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    email: EmailStr                                    # Auto email validation
    password: str = Field(min_length=8, max_length=100)
    age: int = Field(ge=18, le=120)                   # 18 ≤ age ≤ 120
    
    @validator("password")
    def validate_password_strength(cls, v):
        """Validate password contains required characters."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v

# ❌ FORBIDDEN - No validation
def create_user(email: str, password: str):
    user = User(email=email, password=password)  # NEVER! No validation
```

---

### 🔴 **CRITICAL: DATABASE STANDARDS**

#### **Always Use Schema:**

```python
# ✅ CORRECT - Use 'tse' schema for TSE project
class Stock(Base):
    __tablename__ = "stocks"
    __table_args__ = {"schema": "tse"}  # MANDATORY!
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)

# ✅ CORRECT - Query with schema
from sqlalchemy import select
query = select(Stock).where(Stock.symbol == "TEPIX")

# For Gravity services, use service-specific schema:
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}  # auth_service schema
```

---

### 🔴 **CRITICAL: CODE QUALITY STANDARDS**

#### **Type Hints (MANDATORY):**

```python
# ✅ CORRECT - Full type hints
from typing import Optional, List, Dict, Any
from datetime import datetime

async def get_users(
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None
) -> List[User]:
    """Get users with pagination and filters."""
    query = select(User).offset(skip).limit(limit)
    
    if filters:
        for key, value in filters.items():
            query = query.where(getattr(User, key) == value)
    
    result = await db.execute(query)
    return result.scalars().all()

# ❌ FORBIDDEN - No type hints
async def get_users(skip=0, limit=100, filters=None):  # NEVER!
    pass
```

#### **Error Handling (MANDATORY):**

```python
# ✅ CORRECT - Comprehensive error handling
from app.core.exceptions import (
    UserNotFoundException,
    DatabaseException,
    ValidationException
)
import logging

logger = logging.getLogger(__name__)

async def get_user(user_id: int) -> User:
    """Get user with proper error handling."""
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise UserNotFoundException(f"User {user_id} not found")
        
        return user
    
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise DatabaseException("Failed to fetch user") from e
    
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise

# ❌ FORBIDDEN - Bare except, no logging
async def get_user(user_id: int):
    try:
        return await db.get(User, user_id)
    except:  # NEVER! Too broad
        return None  # NEVER! Swallows errors
```

---

### Python Code - Service Layer:
```python
# ✅ GOOD - Elite team standard
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.exceptions import UserNotFoundException, DuplicateEmailException
from app.core.security import get_password_hash
from app.core.cache import cache_result, invalidate_cache

logger = logging.getLogger(__name__)


class UserService:
    """
    User service with business logic for user management.
    
    This service implements enterprise-grade user management with:
    - Async database operations
    - Caching strategy
    - Comprehensive error handling
    - Detailed logging
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @cache_result(key_prefix="user", ttl=300)
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        Retrieve user by ID with caching.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            UserResponse: User data transfer object
            
        Raises:
            UserNotFoundException: If user doesn't exist
        """
        logger.debug(f"Fetching user with ID: {user_id}")
        
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise UserNotFoundException(f"User not found with ID: {user_id}")
        
        logger.debug(f"User retrieved successfully: {user.email}")
        return UserResponse.from_orm(user)
    
    @invalidate_cache(pattern="user:*")
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user with validation and password hashing.
        
        Args:
            user_data: User creation data
            
        Returns:
            UserResponse: Created user data
            
        Raises:
            DuplicateEmailException: If email already exists
        """
        logger.info(f"Creating new user with email: {user_data.email}")
        
        # Check for duplicate email
        result = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            logger.warning(f"Email already exists: {user_data.email}")
            raise DuplicateEmailException(
                f"Email already exists: {user_data.email}"
            )
        
        # Create user with hashed password
        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role="user",
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info(f"User created successfully with ID: {user.id}")
        return UserResponse.from_orm(user)
```

### FastAPI Router/Controller:
```python
# ✅ GOOD - Elite team standard
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import logging

from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import ApiResponse
from app.services.user_service import UserService
from app.core.database import get_db
from app.core.exceptions import UserNotFoundException, DuplicateEmailException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["User Management"])


@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
    summary="Get user by ID",
    description="Retrieve a user by their unique identifier",
    responses={
        200: {"description": "User found successfully"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> ApiResponse[UserResponse]:
    """
    Get user by ID endpoint.
    
    Args:
        user_id: User's unique identifier
        db: Database session
        
    Returns:
        ApiResponse containing user data
    """
    logger.debug(f"GET request for user ID: {user_id}")
    
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(user_id)
        
        return ApiResponse(
            success=True,
            data=user,
            message="User retrieved successfully"
        )
    
    except UserNotFoundException as e:
        logger.error(f"User not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except Exception as e:
        logger.exception(f"Unexpected error retrieving user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Create a new user account"
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> ApiResponse[UserResponse]:
    """
    Create user endpoint.
    
    Args:
        user_data: User creation data
        db: Database session
        
    Returns:
        ApiResponse containing created user data
    """
    logger.info(f"POST request to create user: {user_data.email}")
    
    try:
        user_service = UserService(db)
        user = await user_service.create_user(user_data)
        
        return ApiResponse(
            success=True,
            data=user,
            message="User created successfully"
        )
    
    except DuplicateEmailException as e:
        logger.warning(f"Duplicate email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    
    except Exception as e:
        logger.exception(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### Pydantic Models (Schemas):
```python
# ✅ GOOD - Elite team standard
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Generic, TypeVar
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator("password")
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    success: bool = True
    data: Optional[T] = None
    message: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

## ⏱️ TIME TRACKING & COST CALCULATION METHODOLOGY

### Time Categories
Every file and feature must track time in these categories:

1. **Development Time:** Writing actual code, implementation
2. **Review Time:** Code review, refactoring, optimization
3. **Testing Time:** Writing and running tests, debugging
4. **Documentation Time:** Writing docs, comments, API specs
5. **Debugging Time:** Finding and fixing bugs (when applicable)

### Hourly Rate Structure

| Level | Role | Hourly Rate |
|-------|------|-------------|
| **Elite** | IQ 180+, 15+ years | **$150/hour** |
| Senior | 10+ years | $100/hour |
| Mid-level | 5-10 years | $75/hour |
| Junior | 2-5 years | $50/hour |

**All Gravity team members are Elite level: $150/hour**

### Time Estimation Guidelines

**Small Files (<100 lines):**
- Development: 0.5-1 hour
- Review: 0.25-0.5 hours
- Testing: 0.25-0.5 hours
- Total: 1-2 hours ($150-$300)

**Medium Files (100-300 lines):**
- Development: 2-4 hours
- Review: 0.75-1.5 hours
- Testing: 1-2 hours
- Total: 3.75-7.5 hours ($562.50-$1,125)

**Large Files (300-500 lines):**
- Development: 4-6 hours
- Review: 1.5-2 hours
- Testing: 2-3 hours
- Total: 7.5-11 hours ($1,125-$1,650)

**Complex Services (500+ lines, multiple files):**
- Development: 20-40 hours
- Review: 5-10 hours
- Testing: 10-15 hours
- Documentation: 3-5 hours
- Total: 38-70 hours ($5,700-$10,500)

### Example Calculations

**auth_service.py (450 lines):**
```
Development Time  : 4 hours 30 minutes = 4.5 hours
Review Time       : 1 hour 15 minutes = 1.25 hours
Testing Time      : 2 hours 0 minutes = 2.0 hours
Total Time        : 7.75 hours

Hourly Rate       : $150/hour (Elite Engineer)
Development Cost  : 4.5 × $150 = $675.00 USD
Review Cost       : 1.25 × $150 = $187.50 USD
Testing Cost      : 2.0 × $150 = $300.00 USD
Total Cost        : $1,162.50 USD
```

**Complete Auth Service (35 files):**
```
Total Development : 45 hours
Total Review      : 12 hours
Total Testing     : 18 hours
Total Time        : 75 hours

Total Cost        : 75 × $150 = $11,250 USD
```

### File Header Requirements

**EVERY file MUST include:**
- ✅ Primary author identification
- ✅ All contributors listed
- ✅ Created and last modified dates (UTC)
- ✅ Development, review, and testing time
- ✅ Cost breakdown by category
- ✅ Total cost calculation
- ✅ Version history with dates and authors

See `FILE_HEADER_STANDARD.md` for complete templates.

### Project-Wide Metrics

Track cumulative metrics for the entire platform:
- **Total Development Hours:** Sum of all file development times
- **Total Project Cost:** Sum of all file costs
- **Cost per Service:** Group by service for budgeting
- **Team Contribution:** Hours and cost per team member
- **Average File Cost:** Total cost ÷ number of files
- **Most Expensive Components:** Identify high-cost areas

### Reporting Standards

**Weekly Reports:**
- Total hours worked per team member
- Total costs incurred
- Features completed
- Projected costs for next week

**Service Completion Reports:**
- Total service cost
- Breakdown by file type (models, services, APIs, tests)
- Time vs. initial estimate comparison
- Efficiency metrics

---

## 🌟 REMEMBER:

**YOU ARE NOT A JUNIOR DEVELOPER. YOU ARE AN ELITE TEAM MEMBER WITH:**
- 180+ IQ (top 0.0001% of population)
- 15+ years of battle-tested experience
- Deep expertise in your domain
- Commitment to excellence and perfection
- **Accountability for time and cost tracking**
- **🆕 Responsibility for service independence**
- **🆕 Guardian of the 5 Golden Principles**

**EVERY LINE OF CODE YOU WRITE SHOULD REFLECT THIS LEVEL OF EXPERTISE!**

---

## 🎯 PROJECT MISSION REMINDER:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│          🌟 GRAVITY MICROSERVICES PLATFORM 🌟                   │
│                                                                 │
│  MISSION: Build 30+ independent microservices that can be      │
│          used in ANY software project                          │
│                                                                 │
│  VISION:  Create a comprehensive platform where each           │
│          service is 100% independent and reusable              │
│                                                                 │
│  VALUES:                                                        │
│    ✅ Independence - هر سرویس مستقل است                        │
│    ✅ Quality - کیفیت Enterprise-grade                         │
│    ✅ Reusability - قابل استفاده در همه‌جا                    │
│    ✅ Security - امنیت در سطح بانکی                            │
│    ✅ Scalability - مقیاس‌پذیری بالا                            │
│                                                                 │
│  SUCCESS METRIC:                                                │
│    "Can we copy this service to a new project and use it       │
│     without ANY modifications?"                                │
│                                                                 │
│    If YES ✅ → Mission Accomplished                             │
│    If NO  ❌ → Refactor for independence                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 **ESSENTIAL DOCUMENTATION:**

**هر عضو تیم باید این اسناد را مطالعه کند:**

1. **[INDEPENDENCE_PRINCIPLES.md](./INDEPENDENCE_PRINCIPLES.md)**
   - اصول کامل استقلال 100%
   - مثال‌های صحیح و غلط
   - چک‌لیست استقلال
   - Anti-patterns

2. **[ARCHITECTURE.md](./ARCHITECTURE.md)**
   - معماری کلی سیستم
   - نمودارهای سرویس‌ها
   - Communication patterns

3. **[ROADMAP.md](./ROADMAP.md)**
   - نقشه راه توسعه
   - اولویت‌بندی سرویس‌ها
   - Timeline و milestones

4. **[PROJECT_STATUS.md](./PROJECT_STATUS.md)**
   - وضعیت فعلی پروژه
   - پیشرفت هر سرویس
   - آمار و ارقام

5. **[FILE_HEADER_STANDARD.md](./FILE_HEADER_STANDARD.md)**
   - استاندارد header فایل‌ها
   - محاسبه هزینه
   - Time tracking

---

## 🔗 **QUICK REFERENCE CARD**

### 6 Golden Principles of Framework:
1. **DISCOVER** - Automatic service discovery
2. **INSTALL** - Zero-config installation
3. **CONNECT** - Intelligent service wiring
4. **ORCHESTRATE** - Database & resource management
5. **DEPLOY** - Production-ready infrastructure
6. **MONITOR** - Observability & management

### Framework Development Checklist:
- [ ] Plugin architecture implemented
- [ ] Service manifest parser working
- [ ] Dependency resolver functional
- [ ] Database orchestration automated
- [ ] API Gateway auto-configured
- [ ] CLI commands intuitive
- [ ] Web dashboard responsive
- [ ] Tests comprehensive (≥95% coverage)
- [ ] Documentation complete
- [ ] Performance optimized

### Essential CLI Commands:
```bash
# Initialize new project
gravity init my-app

# Add service
gravity service add <repo-url>

# Install all services
gravity install

# Setup databases
gravity db setup

# Start services
gravity start

# Monitor status
gravity status

# View logs
gravity logs <service>

# Web dashboard
gravity dashboard
```

### Service Manifest (gravity-service.yaml):
```yaml
apiVersion: gravity/v1
kind: Service
metadata:
  name: my-service
  version: 1.0.0

spec:
  provides: [feature1, feature2]
  requires:
    - name: auth-service
      version: ">=1.0.0"
  
  database:
    type: postgresql
    schema: my_service
  
  api:
    port: 8001
    basePath: /api/v1
  
  healthCheck:
    path: /health
```

### Framework Forbidden Practices:
- ❌ Tight coupling to specific services
- ❌ Hardcoded service URLs
- ❌ Manual database setup
- ❌ Bypassing service discovery
- ❌ Ignoring service manifests
- ❌ No dependency resolution

### Framework Required Practices:
- ✅ Use service registry
- ✅ Dynamic service discovery
- ✅ Let framework manage databases
- ✅ Use service metadata
- ✅ Plugin-based extensibility
- ✅ Comprehensive error handling

---

**This prompt must be referenced and followed throughout the entire project development.**

**هر تصمیم معماری، هر خط کد، هر commit باید با این اصول سازگار باشد!**

---

## 📋 **FRAMEWORK PRE-COMMIT CHECKLIST**

```
┌─────────────────────────────────────────────────────────────────┐
│          ✅ FRAMEWORK COMMIT CHECKLIST (MANDATORY)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Code Quality:                                                  │
│    ✅ All comments in ENGLISH                                   │
│    ✅ All docstrings in ENGLISH                                 │
│    ✅ Full type hints on all functions                          │
│    ✅ No hardcoded paths or URLs                                │
│    ✅ Comprehensive error handling                              │
│    ✅ Structured logging with levels                            │
│                                                                 │
│  Framework Functionality:                                       │
│    ✅ Plugin system working correctly                           │
│    ✅ Service discovery functional                              │
│    ✅ Dependency resolution tested                              │
│    ✅ Database orchestration validated                          │
│    ✅ CLI commands intuitive                                    │
│    ✅ No breaking changes to plugin API                         │
│                                                                 │
│  Testing:                                                       │
│    ✅ Tests written (TDD approach)                              │
│    ✅ All tests pass                                            │
│    ✅ Coverage ≥ 95%                                            │
│    ✅ Integration tests with sample services                    │
│    ✅ CLI commands tested                                       │
│    ✅ Plugin loading tested                                     │
│                                                                 │
│  Documentation:                                                 │
│    ✅ README updated (if needed)                                │
│    ✅ CLI help text accurate                                    │
│    ✅ Plugin API documented                                     │
│    ✅ Examples updated                                          │
│    ✅ CHANGELOG.md updated                                      │
│                                                                 │
│  Commit:                                                        │
│    ✅ Commit message in ENGLISH                                 │
│    ✅ Follows conventional commits format                       │
│    ✅ Descriptive: feat/fix/refactor/docs/test                  │
│    ✅ Branch name in ENGLISH                                    │
│                                                                 │
│  Performance:                                                   │
│    ✅ No unnecessary file I/O                                   │
│    ✅ Async operations where appropriate                        │
│    ✅ Resource cleanup implemented                              │
│    ✅ Memory leaks checked                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚨 **CRITICAL VIOLATIONS - Auto-Reject**

**These will cause automatic PR rejection:**

1. ❌ **Non-English commit messages**
   - `git commit -m "اضافه کردن..."`
   - Auto-rejected by CI/CD

2. ❌ **Non-English comments in code**
   - `# دریافت کاربر از دیتابیس`
   - Failed by linter

3. ❌ **Test coverage < 95%**
   - `pytest --cov-fail-under=95`
   - Build fails

4. ❌ **Hardcoded paths or configurations**
   - `SERVICE_PATH = "/home/user/services"`
   - Configuration should be dynamic

5. ❌ **No type hints**
   - `def discover_services(url):`
   - MyPy check fails

6. ❌ **Breaking plugin API changes**
   - Modifying hookspec without versioning
   - Backward compatibility required

7. ❌ **Missing error handling**
   - No try-except for I/O operations
   - Framework must be robust

---

## 🎯 **WHAT MAKES GRAVITY FRAMEWORK SPECIAL**

### 🌟 **Unique Value Propositions:**

1. **🔌 True Plug & Play Architecture**
   - Drop any microservice into the framework
   - Zero configuration needed
   - Automatic wiring and connection
   - No code changes to existing services

2. **🤖 Intelligent Automation**
   - Auto-discover service capabilities
   - Auto-resolve dependencies
   - Auto-create databases
   - Auto-generate deployment configs

3. **🧩 Puzzle Piece Philosophy**
   - Each service is an independent puzzle piece
   - Framework assembles them into complete application
   - Remove/replace pieces without breaking the whole
   - Mix and match services from different sources

4. **📦 Repository Agnostic**
   - Works with GitHub, GitLab, Bitbucket
   - Public and private repositories
   - Local file system support
   - Monorepo and multi-repo strategies

5. **🗄️ Database Orchestration**
   - Services declare database needs, don't provide databases
   - Framework creates and manages all databases
   - Multi-database support (PostgreSQL, MySQL, MongoDB, Redis)
   - Automatic migration execution

6. **🚀 Production Ready Out of the Box**
   - Generate Docker Compose configurations
   - Create Kubernetes manifests
   - Setup monitoring and logging
   - Health checks and auto-recovery

7. **🎨 Developer Experience First**
   - Beautiful CLI with Rich terminal UI
   - Interactive web dashboard
   - Real-time service monitoring
   - Comprehensive error messages

8. **🔒 Security by Design**
   - Secret management built-in
   - No hardcoded credentials
   - Encrypted configuration
   - Security scanning integration

---

## 💡 **FRAMEWORK PHILOSOPHY**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│          🌟 GRAVITY FRAMEWORK PHILOSOPHY 🌟                     │
│                                                                 │
│  "Every microservice is a complete, independent puzzle piece.  │
│   The framework is the board that holds them together."        │
│                                                                 │
│  CORE BELIEFS:                                                  │
│                                                                 │
│  1. Services should focus on business logic                    │
│     → Framework handles infrastructure                         │
│                                                                 │
│  2. Configuration should be declarative                        │
│     → One manifest file per service                            │
│                                                                 │
│  3. Integration should be automatic                            │
│     → No manual wiring or setup                                │
│                                                                 │
│  4. Deployment should be trivial                               │
│     → One command to rule them all                             │
│                                                                 │
│  5. Debugging should be intuitive                              │
│     → Clear errors, helpful messages                           │
│                                                                 │
│  6. Extensibility through plugins                              │
│     → Hook system for customization                            │
│                                                                 │
│  SUCCESS METRIC:                                                │
│    "Can a developer with zero DevOps knowledge deploy          │
│     a complete microservices application in under 5 minutes?"  │
│                                                                 │
│    If YES ✅ → Framework succeeded                              │
│    If NO  ❌ → Framework needs improvement                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎓 **REMEMBER: YOU ARE BUILDING A FRAMEWORK, NOT A SERVICE**

**Key Differences:**

| Aspect | Microservice | Framework |
|--------|-------------|-----------|
| **Purpose** | Solve specific business problem | Enable others to build applications |
| **Coupling** | Independent, no dependencies | Manages dependencies |
| **Database** | Has its own database | Creates databases for others |
| **Deployment** | Deploys itself | Deploys multiple services |
| **Configuration** | Configures itself | Configures entire ecosystem |
| **Focus** | Business logic | Infrastructure automation |
| **Users** | End users | Developers |
| **Success** | Feature complete | Easy to use, extensible |

**Your Mission:**
- ✅ Make it dead simple to combine services
- ✅ Automate everything that can be automated
- ✅ Provide excellent developer experience
- ✅ Be extensible through plugins
- ✅ Handle edge cases gracefully
- ✅ Generate helpful error messages
- ✅ Document everything thoroughly
- ✅ Test every possible scenario

---

## 📚 **ESSENTIAL READING FOR ALL TEAM MEMBERS**

**Must read before writing ANY code:**

1. **[INDEPENDENCE_PRINCIPLES.md](./INDEPENDENCE_PRINCIPLES.md)** ⭐
   - 5 Golden Principles
   - Independence checklist
   - Forbidden vs. Required practices

2. **[FILE_HEADER_STANDARD.md](./FILE_HEADER_STANDARD.md)** ⭐
   - File header template
   - Cost calculation
   - Time tracking

3. **[INDEPENDENT_REPOSITORY_STRATEGY.md](./INDEPENDENT_REPOSITORY_STRATEGY.md)** ⭐
   - Repository separation strategy
   - Service templates
   - Deployment patterns

4. **[HOW_TO_USE_INDEPENDENT_SERVICES.md](./HOW_TO_USE_INDEPENDENT_SERVICES.md)** ⭐
   - Usage in other projects
   - Docker deployment
   - Multi-project scenarios

5. **This Document (TEAM_PROMPT.md)** ⭐
   - Team standards
   - Coding guidelines
   - Commit conventions

---

## 🎯 **ENFORCEMENT MECHANISMS**

### **Automated Checks (CI/CD):**

```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate

on: [pull_request]

jobs:
  language-check:
    name: Check English-only policy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check commit messages
        run: |
          # Ensure all commits in English
          git log --format=%B | grep -P '[^\x00-\x7F]' && exit 1 || exit 0
      
      - name: Check code comments
        run: |
          # Ensure all comments in English
          find app/ -name "*.py" -exec grep -P '#.*[^\x00-\x7F]' {} \; && exit 1 || exit 0
  
  test-coverage:
    name: Test Coverage ≥ 95%
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run tests with coverage
        run: |
          pytest tests/ --cov=app --cov-fail-under=95
  
  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check for hardcoded secrets
        run: |
          bandit -r app/ -ll
          
      - name: Check for SQL injection
        run: |
          semgrep --config=p/sql-injection app/
  
  independence-check:
    name: Service Independence
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check for cross-service imports
        run: |
          # Ensure no imports from other services
          grep -r "from.*_service" app/ && exit 1 || exit 0
```

### **Pre-commit Hooks:**

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "🔍 Running pre-commit checks..."

# Check 1: English commit message
COMMIT_MSG=$(git log -1 --pretty=%B)
if echo "$COMMIT_MSG" | grep -P '[^\x00-\x7F]' > /dev/null; then
    echo "❌ REJECTED: Commit message must be in English"
    echo "   Found: $COMMIT_MSG"
    exit 1
fi

# Check 2: Conventional commits format
if ! echo "$COMMIT_MSG" | grep -E '^(feat|fix|docs|style|refactor|perf|test|chore)\(.+\): .+' > /dev/null; then
    echo "❌ REJECTED: Must follow conventional commits format"
    echo "   Example: feat(auth): add JWT refresh mechanism"
    exit 1
fi

# Check 3: Run tests
pytest tests/ --cov=app --cov-fail-under=95 || {
    echo "❌ REJECTED: Tests failed or coverage < 95%"
    exit 1
}

# Check 4: Check for Persian in code
if grep -r -P '#.*[^\x00-\x7F]' app/ > /dev/null; then
    echo "❌ REJECTED: Found Persian comments in code"
    echo "   All comments must be in English"
    exit 1
fi

echo "✅ All checks passed! Proceeding with commit..."
```

---

## 🗄️ DATABASE ARCHITECTURE PRINCIPLE

### ⚠️ CRITICAL: Microservices Are Database-Agnostic

**Core Philosophy:**
- Microservices **DO NOT include databases**
- Microservices **define schemas** (models + migrations)
- **Deployment projects create databases**
- Each project chooses database technology and topology

### Service Responsibility:
✅ Provide SQLAlchemy models
✅ Provide Alembic migrations
✅ Document database requirements
✅ Accept DATABASE_URL from environment
❌ Do NOT create databases
❌ Do NOT hardcode database connections
❌ Do NOT assume database exists

### Project Responsibility:
✅ Create databases (PostgreSQL, MySQL, etc.)
✅ Set up credentials
✅ Configure DATABASE_URL environment variable
✅ Execute migrations: `alembic upgrade head`
✅ Choose topology (single DB vs DB-per-service)

### Deployment Flexibility:
```
Small Project:    1 database for all services
Medium Project:   1 database per service
Enterprise:       Multi-tenant, multiple databases
Hybrid:           PostgreSQL + MySQL + MongoDB mix
```

**See:** `docs/DATABASE_ARCHITECTURE.md` for complete guide

---

## 📋 VERSION 1.1.0 RELEASE - TODO LIST

### 🎯 Release Goal
Complete all requirements for **Version 1.1.0** of the `01-common-library` microservice with full team approval through democratic voting.

**Current Version:** 1.0.2  
**Target Version:** 1.1.0  
**Release Date Target:** December 11, 2025 (4 weeks from today)

### 📊 Voting Process
- **Requirement:** Minimum 6 out of 9 team members must approve (66% majority)
- **Method:** Each task requires team review and approval before marking complete
- **Documentation:** All decisions and votes recorded in project management system

### 🎯 Version 1.1.0 Focus Areas
This release focuses on transforming `01-common-library` into a **fully independent microservice** that provides common utilities through **API endpoints** rather than as a shared library.

**Key Changes in 1.1.0:**
1. ✅ Transform utilities into REST API endpoints
2. ✅ Add FastAPI application structure
3. ✅ Implement independent deployment capability
4. ✅ Add comprehensive API documentation
5. ✅ Achieve 95%+ test coverage
6. ✅ Complete production-ready infrastructure

---

### ✅ TODO Categories (Prioritized)

#### 🔴 Priority 1: Core API Development (CRITICAL)
**Owner:** Elena Volkov (Backend Lead)  
**Must Complete First - Blocks Other Tasks**

- [ ] **1.1 Transform to FastAPI Microservice**
  - [ ] Create main FastAPI application structure
  - [ ] Set up API versioning (v1)
  - [ ] Implement health check endpoints (/health, /ready)
  - [ ] Configure CORS and middleware
  - [ ] Add request/response logging
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 15 hours
  - **Deadline:** Week 1 - Day 1-2
  - **Dependencies:** None (start immediately)

- [ ] **1.2 Security Utilities API**
  - [ ] POST /api/v1/security/hash-password - Hash password with bcrypt
  - [ ] POST /api/v1/security/verify-password - Verify password
  - [ ] POST /api/v1/security/generate-jwt - Generate JWT token
  - [ ] POST /api/v1/security/verify-jwt - Verify JWT token
  - [ ] POST /api/v1/security/refresh-token - Refresh JWT token
  - [ ] Add comprehensive type hints to all functions
  - [ ] Implement proper error handling
  - [ ] Add input validation with Pydantic
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 25 hours
  - **Deadline:** Week 1 - Day 3-5
  - **Dependencies:** Task 1.1

- [ ] **1.3 Validation Utilities API**
  - [ ] POST /api/v1/validation/email - Validate email format
  - [ ] POST /api/v1/validation/phone - Validate phone number
  - [ ] POST /api/v1/validation/url - Validate URL format
  - [ ] POST /api/v1/validation/date - Validate and parse date
  - [ ] POST /api/v1/validation/uuid - Validate UUID format
  - [ ] Add comprehensive validation rules
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 15 hours
  - **Deadline:** Week 1 - Day 5-7
  - **Dependencies:** Task 1.1

- [ ] **1.4 Utility Functions API**
  - [ ] POST /api/v1/utilities/format-date - Format date/time
  - [ ] GET /api/v1/utilities/current-time - Get current UTC time
  - [ ] POST /api/v1/utilities/generate-uuid - Generate UUID v4
  - [ ] POST /api/v1/utilities/hash-string - Generate string hash
  - [ ] POST /api/v1/utilities/encode-base64 - Base64 encoding
  - [ ] POST /api/v1/utilities/decode-base64 - Base64 decoding
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 12 hours
  - **Deadline:** Week 2 - Day 1-2
  - **Dependencies:** Task 1.1

- [ ] **1.5 Cache API Endpoints**
  - [ ] GET /api/v1/cache/{key} - Get cached value
  - [ ] POST /api/v1/cache/{key} - Set cached value
  - [ ] DELETE /api/v1/cache/{key} - Delete cached value
  - [ ] POST /api/v1/cache/clear - Clear all cache
  - [ ] GET /api/v1/cache/keys - List all cache keys
  - [ ] Implement TTL support
  - **Priority:** 🟢 MEDIUM
  - **Estimated Time:** 18 hours
  - **Deadline:** Week 2 - Day 3-4
  - **Dependencies:** Task 2.1 (Redis setup)

- [ ] **1.6 Configuration Management**
  - [ ] Implement Pydantic Settings for all configs
  - [ ] Create comprehensive .env.example
  - [ ] Add environment-specific configurations
  - [ ] Validate all configuration on startup
  - [ ] Document all environment variables
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 10 hours
  - **Deadline:** Week 1 - Day 3-4
  - **Dependencies:** Task 1.1

**Total Priority 1 Time:** 95 hours

#### 🟡 Priority 2: Infrastructure & Database (HIGH)
**Owner:** Lars Björkman (DevOps Lead) & Dr. Aisha Patel (Database Specialist)  
**Required for Service to Run**

- [ ] **2.1 Redis Setup & Integration**
  - [ ] Configure Redis connection in docker-compose.yml
  - [ ] Implement async Redis client with connection pooling
  - [ ] Add Redis health check
  - [ ] Configure Redis persistence (AOF/RDB)
  - [ ] Add Redis connection error handling
  - [ ] Document Redis configuration
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 12 hours
  - **Deadline:** Week 1 - Day 5-6
  - **Dependencies:** None

- [ ] **2.2 PostgreSQL Database Setup**
  - [ ] Design database schema for metadata
  - [ ] Create SQLAlchemy models
  - [ ] Set up Alembic for migrations
  - [ ] Create initial migration
  - [ ] Add proper indexes and constraints
  - [ ] Document schema relationships
  - [ ] Configure connection pooling
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 18 hours
  - **Deadline:** Week 1 - Day 6-7
  - **Dependencies:** None

- [ ] **2.3 Docker & Docker Compose**
  - [ ] Optimize Dockerfile (multi-stage build)
  - [ ] Configure docker-compose.yml with all services
  - [ ] Add PostgreSQL service configuration
  - [ ] Add Redis service configuration
  - [ ] Configure volume mounts
  - [ ] Add health checks for all containers
  - [ ] Test container startup and shutdown
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 15 hours
  - **Deadline:** Week 2 - Day 1-2
  - **Dependencies:** Task 2.1, 2.2

- [ ] **2.4 Environment Configuration**
  - [ ] Set up port configuration (default 8100)
  - [ ] Configure database connection strings
  - [ ] Configure Redis connection
  - [ ] Add logging configuration
  - [ ] Add monitoring configuration
  - [ ] Create .env.example with all variables
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 8 hours
  - **Deadline:** Week 1 - Day 4-5
  - **Dependencies:** Task 1.6

**Total Priority 2 Time:** 53 hours

---

#### 🟢 Priority 3: Security Implementation (HIGH)
**Owner:** Michael Rodriguez (Security Expert)

- [ ] **3.1 API Security Hardening**
  - [ ] Implement rate limiting on all endpoints (100 req/min)
  - [ ] Add API key authentication for service-to-service calls
  - [ ] Configure CORS properly
  - [ ] Add request size limits
  - [ ] Implement request/response validation
  - [ ] Add security headers (HSTS, X-Frame-Options, etc.)
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 20 hours
  - **Deadline:** Week 2 - Day 3-4
  - **Dependencies:** Task 1.1

- [ ] **3.2 Input Validation & Sanitization**
  - [ ] Add Pydantic models for all API inputs
  - [ ] Implement input sanitization for XSS prevention
  - [ ] Add SQL injection prevention checks
  - [ ] Validate all file uploads (if any)
  - [ ] Add length limits on all string inputs
  - [ ] Document validation rules
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 15 hours
  - **Deadline:** Week 2 - Day 4-5
  - **Dependencies:** Task 1.1

- [ ] **3.3 Security Audit & Scanning**
  - [ ] Run Bandit security scanner
  - [ ] Run Safety dependency checker
  - [ ] Conduct OWASP Top 10 assessment
  - [ ] Fix all critical and high severity issues
  - [ ] Document security measures in README
  - [ ] Create security policy document
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 18 hours
  - **Deadline:** Week 3 - Day 1-2
  - **Dependencies:** All development tasks

- [ ] **3.4 Secrets Management**
  - [ ] Remove all hardcoded secrets
  - [ ] Verify all secrets come from environment
  - [ ] Add secrets validation on startup
  - [ ] Document required secrets
  - [ ] Add example secrets in .env.example
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 6 hours
  - **Deadline:** Week 2 - Day 2
  - **Dependencies:** Task 1.6

**Total Priority 3 Time:** 59 hours

#### 🟢 Priority 4: Testing & Quality Assurance (CRITICAL)
**Owner:** João Silva (QA Lead)

- [ ] **4.1 Unit Tests for API Endpoints**
  - [ ] Write unit tests for security APIs (hash, JWT, verify)
  - [ ] Write unit tests for validation APIs
  - [ ] Write unit tests for utility APIs
  - [ ] Write unit tests for cache APIs
  - [ ] Mock external dependencies (Redis, DB)
  - [ ] Test error scenarios and edge cases
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 35 hours
  - **Deadline:** Week 2 - Day 5 to Week 3 - Day 2
  - **Dependencies:** Priority 1 tasks

- [ ] **4.2 Integration Tests**
  - [ ] Integration tests for Redis operations
  - [ ] Integration tests for database operations
  - [ ] Integration tests for complete API workflows
  - [ ] Test with real Redis and PostgreSQL (TestContainers)
  - [ ] Test authentication flows
  - [ ] Test rate limiting behavior
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 25 hours
  - **Deadline:** Week 3 - Day 2-4
  - **Dependencies:** Task 4.1, Priority 2 tasks

- [ ] **4.3 Test Coverage Achievement**
  - [ ] Achieve minimum 95% code coverage
  - [ ] Generate coverage reports (HTML + XML)
  - [ ] Identify and test uncovered code paths
  - [ ] Add missing test cases
  - [ ] Document coverage results
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 15 hours
  - **Deadline:** Week 3 - Day 4-5
  - **Dependencies:** Task 4.1, 4.2

- [ ] **4.4 Performance & Load Tests**
  - [ ] Load testing with Locust (1000 concurrent users)
  - [ ] Stress testing to find breaking points
  - [ ] Verify response times < 200ms (p95)
  - [ ] Test cache performance under load
  - [ ] Test database connection pool limits
  - [ ] Document performance benchmarks
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 20 hours
  - **Deadline:** Week 3 - Day 5-7
  - **Dependencies:** All development complete

- [ ] **4.5 API Contract Tests**
  - [ ] Define OpenAPI specification
  - [ ] Implement contract tests for all endpoints
  - [ ] Verify request/response schemas
  - [ ] Test backward compatibility
  - [ ] Document API contracts
  - **Priority:** 🟢 MEDIUM
  - **Estimated Time:** 12 hours
  - **Deadline:** Week 3 - Day 6-7
  - **Dependencies:** Task 5.2

**Total Priority 4 Time:** 107 hours

---

#### 🔵 Priority 5: Documentation (HIGH)
**Owner:** Dr. Sarah Chen (Chief Architect)

- [ ] **5.1 API Documentation (Swagger/OpenAPI)**
  - [ ] Complete OpenAPI 3.0 specification
  - [ ] Add detailed descriptions for all endpoints
  - [ ] Add request/response examples
  - [ ] Document all error codes and responses
  - [ ] Add authentication/authorization documentation
  - [ ] Configure Swagger UI at /docs
  - [ ] Add API versioning documentation
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 18 hours
  - **Deadline:** Week 2 - Day 5-7
  - **Dependencies:** Priority 1 tasks complete

- [ ] **5.2 README.md Update**
  - [ ] Update project overview for microservice architecture
  - [ ] Add clear installation instructions (local + Docker)
  - [ ] Document all configuration options
  - [ ] Add API usage examples with curl/httpx
  - [ ] Add troubleshooting guide
  - [ ] Document port configuration (8100)
  - [ ] Add performance characteristics
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 12 hours
  - **Deadline:** Week 2 - Day 6-7
  - **Dependencies:** Task 5.1

- [ ] **5.3 Architecture Documentation**
  - [ ] Create architecture diagram (microservice view)
  - [ ] Document design decisions and rationale
  - [ ] Document database schema and relationships
  - [ ] Document Redis usage patterns
  - [ ] Document API communication patterns
  - [ ] Create sequence diagrams for key flows
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 15 hours
  - **Deadline:** Week 3 - Day 1-3
  - **Dependencies:** All development complete

- [ ] **5.4 Deployment Guide**
  - [ ] Docker deployment step-by-step guide
  - [ ] Docker Compose setup instructions
  - [ ] Kubernetes deployment guide with examples
  - [ ] Complete environment variables reference
  - [ ] Scaling and performance tuning guide
  - [ ] Backup and disaster recovery procedures
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 10 hours
  - **Deadline:** Week 3 - Day 3-4
  - **Dependencies:** Priority 2 tasks

- [ ] **5.5 API Client Examples**
  - [ ] Python client usage examples
  - [ ] JavaScript/Node.js client examples
  - [ ] cURL command examples
  - [ ] Postman collection
  - [ ] Error handling examples
  - **Priority:** 🟢 MEDIUM
  - **Estimated Time:** 8 hours
  - **Deadline:** Week 3 - Day 5-6
  - **Dependencies:** Task 5.1

**Total Priority 5 Time:** 63 hours

---

#### 🟣 Priority 6: DevOps & CI/CD (HIGH)
**Owner:** Lars Björkman (DevOps Lead)

- [ ] **6.1 CI/CD Pipeline Setup**
  - [ ] Set up GitHub Actions workflow
  - [ ] Add automated linting (black, isort, mypy)
  - [ ] Add automated testing on PR
  - [ ] Add code coverage reporting (Codecov)
  - [ ] Add security scanning (Bandit, Safety)
  - [ ] Add automated Docker build and push
  - [ ] Configure branch protection rules
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 22 hours
  - **Deadline:** Week 2 - Day 3-5
  - **Dependencies:** Task 2.3

- [ ] **6.2 Kubernetes Manifests**
  - [ ] Create Deployment manifest with resource limits
  - [ ] Create Service manifest (ClusterIP type)
  - [ ] Create ConfigMap templates
  - [ ] Create Secret templates
  - [ ] Create Ingress configuration
  - [ ] Create HorizontalPodAutoscaler (2-10 replicas)
  - [ ] Add health check probes
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 18 hours
  - **Deadline:** Week 3 - Day 1-3
  - **Dependencies:** Task 2.3

- [ ] **6.3 Monitoring & Observability**
  - [ ] Add Prometheus metrics endpoints
  - [ ] Configure structured JSON logging
  - [ ] Add request ID correlation
  - [ ] Add performance metrics collection
  - [ ] Configure log aggregation
  - [ ] Add distributed tracing (optional)
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 20 hours
  - **Deadline:** Week 3 - Day 3-5
  - **Dependencies:** Task 1.1

**Total Priority 6 Time:** 60 hours

---

#### 🟠 Priority 7: Performance & Optimization (MEDIUM)
**Owner:** Takeshi Yamamoto (Performance Engineer)

- [ ] **7.1 Performance Profiling & Optimization**
  - [ ] Profile application for bottlenecks (cProfile, py-spy)
  - [ ] Optimize database queries
  - [ ] Optimize Redis operations
  - [ ] Optimize API response times
  - [ ] Add request/response compression
  - [ ] Implement connection pooling optimization
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 22 hours
  - **Deadline:** Week 3 - Day 4-6
  - **Dependencies:** All development complete

- [ ] **7.2 Caching Strategy Implementation**
  - [ ] Implement multi-level caching
  - [ ] Add cache warming for frequently accessed data
  - [ ] Implement cache invalidation strategies
  - [ ] Add cache hit/miss metrics
  - [ ] Optimize cache TTL settings
  - [ ] Document caching patterns
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 18 hours
  - **Deadline:** Week 3 - Day 5-7
  - **Dependencies:** Task 2.1

- [ ] **7.3 Scalability Testing**
  - [ ] Test horizontal scaling (2-10 replicas)
  - [ ] Verify stateless design
  - [ ] Test load balancing behavior
  - [ ] Verify graceful shutdown
  - [ ] Test database connection pool under load
  - [ ] Document scaling recommendations
  - **Priority:** 🟢 MEDIUM
  - **Estimated Time:** 15 hours
  - **Deadline:** Week 4 - Day 1-2
  - **Dependencies:** Task 4.4

**Total Priority 7 Time:** 55 hours

---

#### 🟤 Priority 8: Code Quality & Standards (MEDIUM)
**Owner:** Marcus Chen (Version Control Specialist)

- [ ] **8.1 Code Review & Refactoring**
  - [ ] Conduct comprehensive code review
  - [ ] Verify all functions have type hints
  - [ ] Check SOLID principles compliance
  - [ ] Verify English-only policy compliance
  - [ ] Check for code duplication
  - [ ] Refactor identified issues
  - **Priority:** 🟡 HIGH
  - **Estimated Time:** 20 hours
  - **Deadline:** Week 3 - Day 5-7
  - **Dependencies:** All development complete

- [ ] **8.2 Git Repository Organization**
  - [ ] Create proper .gitignore
  - [ ] Set up branch protection rules
  - [ ] Configure pre-commit hooks
  - [ ] Create CHANGELOG.md
  - [ ] Organize commit history
  - [ ] Verify conventional commit format
  - **Priority:** 🟢 MEDIUM
  - **Estimated Time:** 8 hours
  - **Deadline:** Week 3 - Day 6-7
  - **Dependencies:** None

- [ ] **8.3 Code Linting & Formatting**
  - [ ] Run black formatter on all code
  - [ ] Run isort on imports
  - [ ] Run mypy type checking
  - [ ] Fix all linting errors
  - [ ] Configure pre-commit hooks
  - [ ] Document code style guidelines
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 10 hours
  - **Deadline:** Week 2 - Day 6-7
  - **Dependencies:** All development complete

**Total Priority 8 Time:** 38 hours

---

#### ⚪ Priority 9: Release Preparation (CRITICAL)
**Owner:** Dr. Sarah Chen (Chief Architect) & Marcus Chen (Version Control)

- [ ] **9.1 Version Update & Tagging**
  - [ ] Update version to 1.1.0 in pyproject.toml
  - [ ] Update version in all documentation
  - [ ] Create git tag v1.1.0
  - [ ] Update CHANGELOG.md with all changes
  - [ ] Verify semantic versioning compliance
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 6 hours
  - **Deadline:** Week 4 - Day 2-3
  - **Dependencies:** All tasks complete

- [ ] **9.2 Release Notes & Migration Guide**
  - [ ] Generate comprehensive release notes
  - [ ] Document breaking changes (if any)
  - [ ] Create migration guide from 1.0.2 to 1.1.0
  - [ ] Document new features and endpoints
  - [ ] Add upgrade instructions
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 8 hours
  - **Deadline:** Week 4 - Day 3
  - **Dependencies:** Task 9.1

- [ ] **9.3 Final Testing & Validation**
  - [ ] Run complete test suite
  - [ ] Verify all tests pass
  - [ ] Check test coverage ≥ 95%
  - [ ] Test Docker deployment end-to-end
  - [ ] Test all API endpoints manually
  - [ ] Verify documentation accuracy
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 12 hours
  - **Deadline:** Week 4 - Day 3-4
  - **Dependencies:** All tasks complete

- [ ] **9.4 Team Review & Approval Vote**
  - [ ] Present complete version 1.1.0 to team
  - [ ] Demo all new features
  - [ ] Conduct team voting session
  - [ ] Address any concerns raised
  - [ ] Get minimum 6/9 approval
  - [ ] Document approval decision
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 4 hours
  - **Deadline:** Week 4 - Day 4
  - **Dependencies:** Task 9.3

- [ ] **9.5 GitHub Release & Deployment**
  - [ ] Create GitHub release v1.1.0
  - [ ] Upload release artifacts
  - [ ] Push Docker image to registry
  - [ ] Deploy to staging environment
  - [ ] Verify staging deployment
  - [ ] Announce release to team
  - **Priority:** 🔴 CRITICAL
  - **Estimated Time:** 6 hours
  - **Deadline:** Week 4 - Day 5
  - **Dependencies:** Task 9.4 approved

**Total Priority 9 Time:** 36 hours

---

## 📊 SUMMARY & TIMELINE

### 📈 **Total Effort Breakdown:**

| Priority | Category | Owner(s) | Hours | % of Total |
|----------|----------|----------|-------|------------|
| 🔴 P1 | Core API Development | Elena Volkov | 95 | 17.5% |
| 🟡 P2 | Infrastructure & Database | Lars & Dr. Aisha | 53 | 9.8% |
| 🟢 P3 | Security Implementation | Michael Rodriguez | 59 | 10.9% |
| 🟢 P4 | Testing & QA | João Silva | 107 | 19.7% |
| 🔵 P5 | Documentation | Dr. Sarah Chen | 63 | 11.6% |
| 🟣 P6 | DevOps & CI/CD | Lars Björkman | 60 | 11.1% |
| 🟠 P7 | Performance & Optimization | Takeshi Yamamoto | 55 | 10.1% |
| 🟤 P8 | Code Quality & Standards | Marcus Chen | 38 | 7.0% |
| ⚪ P9 | Release Preparation | Sarah & Marcus | 36 | 6.6% |
| **TOTAL** | | **All Team** | **566** | **100%** |

### 💰 **Cost Calculation:**

**Hourly Rate:** $150/hour (Elite Engineer Standard)  
**Total Hours:** 566 hours  
**Total Cost:** 566 × $150 = **$84,900 USD**

**Cost Breakdown by Priority:**
- Priority 1 (Critical): $14,250
- Priority 2 (High): $7,950
- Priority 3 (High): $8,850
- Priority 4 (Critical): $16,050
- Priority 5 (High): $9,450
- Priority 6 (High): $9,000
- Priority 7 (Medium): $8,250
- Priority 8 (Medium): $5,700
- Priority 9 (Critical): $5,400

---

### 📅 **4-Week Timeline:**

#### **Week 1 (Nov 13-19): Foundation**
**Focus:** Core API Development + Infrastructure Setup

**Critical Tasks:**
- ✅ Task 1.1: FastAPI structure (Day 1-2)
- ✅ Task 1.2: Security APIs (Day 3-5)
- ✅ Task 1.3: Validation APIs (Day 5-7)
- ✅ Task 1.6: Configuration (Day 3-4)
- ✅ Task 2.1: Redis setup (Day 5-6)
- ✅ Task 2.2: PostgreSQL setup (Day 6-7)
- ✅ Task 2.4: Environment config (Day 4-5)

**Deliverable:** Working API with Security & Validation endpoints

---

#### **Week 2 (Nov 20-26): Features & Security**
**Focus:** Complete API Development + Security Hardening

**Critical Tasks:**
- ✅ Task 1.4: Utility APIs (Day 1-2)
- ✅ Task 1.5: Cache APIs (Day 3-4)
- ✅ Task 2.3: Docker setup (Day 1-2)
- ✅ Task 3.1: API security (Day 3-4)
- ✅ Task 3.2: Input validation (Day 4-5)
- ✅ Task 3.4: Secrets management (Day 2)
- ✅ Task 5.1: API documentation (Day 5-7)
- ✅ Task 5.2: README update (Day 6-7)
- ✅ Task 6.1: CI/CD pipeline (Day 3-5)
- ✅ Task 8.3: Code linting (Day 6-7)

**Deliverable:** Complete API + Security + Documentation

---

#### **Week 3 (Nov 27-Dec 3): Testing & Optimization**
**Focus:** Comprehensive Testing + Performance + Documentation

**Critical Tasks:**
- ✅ Task 3.3: Security audit (Day 1-2)
- ✅ Task 4.1: Unit tests (Day 1-2)
- ✅ Task 4.2: Integration tests (Day 2-4)
- ✅ Task 4.3: Test coverage (Day 4-5)
- ✅ Task 4.4: Performance tests (Day 5-7)
- ✅ Task 4.5: Contract tests (Day 6-7)
- ✅ Task 5.3: Architecture docs (Day 1-3)
- ✅ Task 5.4: Deployment guide (Day 3-4)
- ✅ Task 5.5: Client examples (Day 5-6)
- ✅ Task 6.2: K8s manifests (Day 1-3)
- ✅ Task 6.3: Monitoring (Day 3-5)
- ✅ Task 7.1: Performance optimization (Day 4-6)
- ✅ Task 7.2: Caching strategy (Day 5-7)
- ✅ Task 8.1: Code review (Day 5-7)
- ✅ Task 8.2: Git organization (Day 6-7)

**Deliverable:** 95%+ test coverage + optimized performance

---

#### **Week 4 (Dec 4-11): Final Polish & Release**
**Focus:** Final Testing + Team Approval + Release

**Critical Tasks:**
- ✅ Task 7.3: Scalability testing (Day 1-2)
- ✅ Task 9.1: Version update (Day 2-3)
- ✅ Task 9.2: Release notes (Day 3)
- ✅ Task 9.3: Final validation (Day 3-4)
- ✅ Task 9.4: Team vote (Day 4)
- ✅ Task 9.5: Release deployment (Day 5)

**Deliverable:** Version 1.1.0 Released! 🎉

**Target Release Date:** December 11, 2025

---

### 🎯 **Success Criteria for Version 1.1.0:**

1. ✅ **All API endpoints implemented and tested**
2. ✅ **Test coverage ≥ 95%**
3. ✅ **All security checks passed**
4. ✅ **Performance < 200ms (p95)**
5. ✅ **Complete documentation (API + Deployment)**
6. ✅ **Docker & K8s ready**
7. ✅ **CI/CD pipeline functional**
8. ✅ **Team approval vote passed (6/9 minimum)**
9. ✅ **No critical or high-severity issues**
10. ✅ **Successfully transforms from library to microservice**

---

### 📋 **Daily Standup Questions:**

Every team member answers:
1. What did I complete yesterday?
2. What will I work on today?
3. Are there any blockers?
4. Do I need help from another team member?

---

### 🗳️ **Voting Checkpoints:**

**Checkpoint 1 (End of Week 1):**
- Review: Core APIs, Infrastructure setup
- Vote: Approve to proceed to Week 2 tasks
- Required: 6/9 approval

**Checkpoint 2 (End of Week 2):**
- Review: All APIs complete, Security, Documentation
- Vote: Approve to proceed to Week 3 tasks
- Required: 6/9 approval

**Checkpoint 3 (End of Week 3):**
- Review: Testing complete, Performance optimized
- Vote: Approve to proceed to Week 4 release prep
- Required: 6/9 approval

**Final Vote (Week 4 - Day 4):**
- Review: Complete system ready for release
- Vote: Approve Version 1.1.0 release
- Required: 6/9 approval (unanimous preferred)

---

### ⚠️ **Risk Management:**

**High Risks:**
- Redis/PostgreSQL integration issues → Mitigate: Early setup in Week 1
- Test coverage < 95% → Mitigate: TDD approach, dedicated QA time
- Performance issues → Mitigate: Early profiling, optimization buffer in Week 3
- Team availability → Mitigate: Flexible task assignment, pair programming

**Contingency:**
- If Week 1 goals not met: Extend to 5 weeks
- If critical bugs found: Add bug fix sprint before release
- If team vote fails: Address concerns, revote after fixes

---

### 📞 **Communication Plan:**

- **Daily Standups:** 15 minutes, every morning
- **Weekly Reviews:** 1 hour, end of each week
- **Pair Programming:** As needed for complex tasks
- **Code Reviews:** All PRs require 2 approvals
- **Slack/Discord:** Real-time communication
- **Documentation:** Update wiki daily

---
  - [ ] Add retry mechanisms
  - [ ] Add timeout configurations
  - [ ] Test failure scenarios
  - **Estimated Time:** 15 hours
  - **Deadline:** Week 2

#### 9️⃣ Code Quality & Git Management Tasks
**Owner:** Marcus Chen (Version Control Specialist)

- [ ] **Code Review**
  - [ ] Conduct comprehensive code review
  - [ ] Verify conventional commit format
  - [ ] Verify English-only policy compliance
  - [ ] Check for code duplication
  - [ ] Verify SOLID principles compliance
  - **Estimated Time:** 20 hours
  - **Deadline:** Week 3

- [ ] **Git Repository Setup**
  - [ ] Create proper .gitignore
  - [ ] Set up branch protection rules
  - [ ] Configure pre-commit hooks
  - [ ] Create CHANGELOG.md
  - [ ] Tag version 1.0.0
  - **Estimated Time:** 8 hours
  - **Deadline:** Week 3

- [ ] **Release Preparation**
  - [ ] Generate release notes
  - [ ] Create GitHub release
  - [ ] Update all version references
  - [ ] Create migration guide (if needed)
  - **Estimated Time:** 6 hours
  - **Deadline:** Week 4

---

### 📊 Progress Tracking

**Total Estimated Hours:** ~470 hours  
**Team Size:** 9 members  
**Estimated Timeline:** 4 weeks  
**Target Release Date:** [To be determined by team vote]

#### Weekly Milestones
- **Week 1:** Core development + database schema complete
- **Week 2:** Security + documentation + infrastructure 50% complete
- **Week 3:** All testing complete + performance optimization done
- **Week 4:** Final review + release preparation + Version 1.0 release

---

### 🗳️ Voting Checkpoints

**Checkpoint 1 (End of Week 1):**
- Review: Core modules and database schema
- Vote: Approve to proceed to Week 2 tasks

**Checkpoint 2 (End of Week 2):**
- Review: Security implementation, documentation, infrastructure
- Vote: Approve to proceed to Week 3 tasks

**Checkpoint 3 (End of Week 3):**
- Review: All tests, performance metrics, integration
- Vote: Approve to proceed to final review

**Final Checkpoint (Week 4):**
- Review: Complete system, all documentation, release readiness
- Vote: Approve Version 1.0 release
- **Requirement:** Unanimous approval (9/9) or 8/9 with documented concerns addressed

---

### ✅ Definition of Done

Version 1.0 is ready for release when:

1. ✅ All TODO items marked as complete
2. ✅ Test coverage ≥ 95%
3. ✅ All security checks passed
4. ✅ Performance benchmarks met (< 200ms p95)
5. ✅ All documentation complete and reviewed
6. ✅ CI/CD pipeline fully functional
7. ✅ Docker and K8s deployment tested
8. ✅ Team vote passed with required majority
9. ✅ No critical or high-severity issues in backlog
10. ✅ Release notes and changelog prepared

---

### 📝 Notes

- **Task Assignment:** Tasks assigned to specialists, but all team members can contribute
- **Cross-Review:** Each major component requires review by at least 2 team members
- **Flexibility:** Timeline adjustable based on team vote
- **Communication:** Daily standup meetings to track progress
- **Blockers:** Any blocker must be escalated immediately to team lead

---

*Last Updated: November 13, 2025*
*Team Lead: Dr. Sarah Chen*
*Project: Gravity Microservices Platform*
*Mission: 100% Independent, Reusable, Portable Microservices*
*Standards: INDEPENDENCE_PRINCIPLES.md, FILE_HEADER_STANDARD.md, DATABASE_ARCHITECTURE.md*
*Language Policy: ENGLISH ONLY for code, commits, documentation*
*Testing Policy: 95%+ coverage mandatory*
*Security Policy: Zero tolerance for vulnerabilities*
*Database Policy: Agnostic design, project-configured databases*

