# 🏗️ Gravity Framework - Technical Architecture

> **Detailed technical architecture for the microservices orchestration platform**

---

## 🎯 System Overview

Gravity Framework acts as an intelligent orchestrator that transforms independent microservices into a cohesive application through automated discovery, dependency resolution, database provisioning, and service wiring.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         GRAVITY FRAMEWORK                            │
│                                                                      │
│  Input: Multiple Git Repos (Microservices)                         │
│         ↓                                                            │
│  Process: Discovery → Resolution → Provision → Connect → Deploy    │
│         ↓                                                            │
│  Output: Running, Connected Application                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Core Components

### 1. Service Discovery Engine

**Location:** `gravity_framework/discovery/scanner.py`

**Purpose:** Automatically detect and parse microservices from various sources

**Flow:**
```
User Command: gravity add https://github.com/org/auth-service
        ↓
    Clone Repository
        ↓
    Find gravity-service.yaml
        ↓
    Parse & Validate Manifest
        ↓
    Extract Metadata:
    - Service name, version
    - Dependencies
    - Database requirements
    - API contracts
    - Runtime configuration
        ↓
    Register in ServiceRegistry
```

**Implementation:**
```python
class ServiceScanner:
    """Discovers services from Git repositories and local paths."""
    
    async def discover_from_git(self, repo_url: str, branch: str = "main") -> Service:
        """
        1. Clone repository to temporary directory
        2. Locate gravity-service.yaml
        3. Parse YAML with schema validation
        4. Create Service object
        5. Return for registration
        """
        
    async def discover_from_local(self, path: Path) -> Service:
        """Scan local directory for service manifest."""
        
    def validate_manifest(self, manifest_data: dict) -> ServiceManifest:
        """Validate against JSON schema."""
```

---

### 2. Dependency Resolver

**Location:** `gravity_framework/resolver/dependency.py`

**Purpose:** Resolve service dependencies and determine installation order

**Algorithm:** Modified PubGrub (used by Dart, Poetry)

**Flow:**
```
Services: [auth-service, user-service, payment-service]
        ↓
    Build Dependency Graph
        auth-service (1.0.0)
            requires: user-service >=1.0.0
        user-service (1.5.0)
            requires: database-service ~2.1.0
        payment-service (2.0.0)
            requires: user-service >=1.2.0
        ↓
    Detect Conflicts
        - user-service: >=1.0.0 AND >=1.2.0 → OK (1.5.0 satisfies both)
        - Check for circular dependencies
        ↓
    Topological Sort
        database-service → user-service → [auth-service, payment-service]
        ↓
    Return Installation Order
```

**Implementation:**
```python
class DependencyResolver:
    """Resolves service dependencies with version constraints."""
    
    def resolve(self, services: List[Service]) -> List[Service]:
        """
        Returns services in installation order.
        
        Raises:
            CircularDependencyError: If circular deps detected
            VersionConflictError: If versions incompatible
        """
        
    def _build_graph(self, services: List[Service]) -> nx.DiGraph:
        """Build directed graph of dependencies."""
        
    def _detect_cycles(self, graph: nx.DiGraph) -> List[List[str]]:
        """Find circular dependencies."""
        
    def _topological_sort(self, graph: nx.DiGraph) -> List[str]:
        """Return installation order using Kahn's algorithm."""
```

---

### 3. Database Orchestrator

**Location:** `gravity_framework/database/orchestrator.py`

**Purpose:** Automatically create and configure databases for services

**Supported Databases:**
- PostgreSQL (with extensions)
- MySQL (with charset/collation)
- MongoDB (with replica sets)
- Redis (with persistence)

**Flow:**
```
Service Manifest:
    databases:
      - name: auth_db
        type: postgresql
        version: "15"
        extensions: [uuid-ossp, pgcrypto]
        ↓
    Check if PostgreSQL Container Running
        ↓ No
    Start PostgreSQL Container
        ↓
    Wait for Healthy
        ↓
    Connect to PostgreSQL
        ↓
    CREATE DATABASE auth_db
        ↓
    CREATE EXTENSION "uuid-ossp"
    CREATE EXTENSION "pgcrypto"
        ↓
    Generate Connection String:
        postgresql://user:pass@postgres:5432/auth_db
        ↓
    Store in Environment:
        AUTH_DB_URL=postgresql://...
```

**Implementation:**
```python
class DatabaseOrchestrator:
    """Manages database creation for all supported types."""
    
    async def create_database(self, db_req: DatabaseRequirement) -> str:
        """
        Create database and return connection string.
        
        Returns:
            Connection string for injection
        """
        
    async def _create_postgresql(self, db_req: DatabaseRequirement) -> str:
        """PostgreSQL-specific creation with extensions."""
        
    async def _create_mysql(self, db_req: DatabaseRequirement) -> str:
        """MySQL-specific with charset/collation."""
        
    async def _create_mongodb(self, db_req: DatabaseRequirement) -> str:
        """MongoDB database creation."""
        
    async def _create_redis(self, db_req: DatabaseRequirement) -> str:
        """Redis instance setup."""
```

---

### 4. Service Manager

**Location:** `gravity_framework/core/manager.py`

**Purpose:** Manage Docker containers for each service

**Responsibilities:**
- Start/stop/restart containers
- Health check monitoring
- Log collection
- Resource management
- Port allocation

**Flow:**
```
gravity start auth-service
        ↓
    Load Service Manifest
        ↓
    Prepare Environment Variables:
        - Database URLs
        - Dependency service URLs
        - Custom variables
        ↓
    Create Docker Container:
        - Image: python:3.11 (or service.runtime)
        - Command: uvicorn main:app
        - Ports: 8000 → 8001
        - Network: gravity-net
        - Environment: {...}
        - Volumes: [./auth-service:/app]
        ↓
    Start Container
        ↓
    Wait for Health Check:
        GET http://auth-service:8000/health
        ↓ 200 OK
    Mark as Running
        ↓
    Register in Service Discovery
```

**Implementation:**
```python
class ServiceManager:
    """Manages Docker containers for services."""
    
    async def start_service(self, service: Service) -> Container:
        """
        Start service in Docker container.
        
        Steps:
        1. Prepare environment
        2. Allocate port
        3. Create container
        4. Start container
        5. Wait for health check
        6. Return container info
        """
        
    async def stop_service(self, service_name: str):
        """Gracefully stop service container."""
        
    async def restart_service(self, service_name: str):
        """Restart service (stop + start)."""
        
    async def health_check(self, service: Service) -> bool:
        """Check if service is healthy."""
```

---

### 5. API Gateway Configurator

**Location:** `gravity_framework/gateway/traefik.py`

**Purpose:** Auto-configure API Gateway for routing requests

**Technology:** Traefik (dynamic configuration)

**Flow:**
```
Services Registered:
    - auth-service: /api/auth → localhost:8001
    - user-service: /api/users → localhost:8002
    - payment-service: /api/payments → localhost:8003
        ↓
    Generate Traefik Configuration:
        routers:
          auth-router:
            rule: PathPrefix(`/api/auth`)
            service: auth-service
          user-router:
            rule: PathPrefix(`/api/users`)
            service: user-service
        services:
          auth-service:
            loadBalancer:
              servers:
                - url: http://auth-service:8000
        ↓
    Write to traefik.yml
        ↓
    Reload Traefik
        ↓
    Routes Active:
        http://localhost/api/auth → auth-service
        http://localhost/api/users → user-service
```

**Implementation:**
```python
class TraefikConfigurator:
    """Configures Traefik API Gateway dynamically."""
    
    async def generate_config(self, services: List[Service]) -> dict:
        """Generate Traefik YAML configuration."""
        
    async def update_routes(self, service: Service):
        """Add/update routes for new service."""
        
    async def remove_routes(self, service_name: str):
        """Remove routes for stopped service."""
```

---

## 🔄 Complete Orchestration Flow

### Step-by-Step: `gravity init my-app` → Running Application

```
STEP 1: Initialize Project
    $ gravity init my-app
        ↓
    Create directory structure:
        my-app/
        ├── .gravity/
        │   ├── config.yaml
        │   ├── registry.json
        │   └── state.json
        ├── services/
        └── config/

STEP 2: Add Services
    $ cd my-app
    $ gravity add https://github.com/org/auth-service
        ↓
    ServiceScanner:
        - Clone repository
        - Parse gravity-service.yaml
        - Validate manifest
        ↓
    ServiceRegistry:
        - Register auth-service v1.0.0
        - Store metadata
        ↓
    $ gravity add https://github.com/org/user-service
        ↓
    (Repeat for user-service)

STEP 3: List Discovered Services
    $ gravity list
        ↓
    ┌──────────────┬─────────┬──────┬──────────────┐
    │ Name         │ Version │ Type │ Status       │
    ├──────────────┼─────────┼──────┼──────────────┤
    │ auth-service │ 1.0.0   │ api  │ discovered   │
    │ user-service │ 1.5.0   │ api  │ discovered   │
    └──────────────┴─────────┴──────┴──────────────┘

STEP 4: Resolve Dependencies & Install
    $ gravity install
        ↓
    DependencyResolver:
        - Build dependency graph
        - Detect auth-service requires user-service >=1.0.0
        - user-service v1.5.0 satisfies constraint
        - Installation order: user-service, auth-service
        ↓
    DatabaseOrchestrator:
        - user-service needs PostgreSQL → Create user_db
        - auth-service needs PostgreSQL → Create auth_db
        - auth-service needs Redis → Create auth_cache
        ↓
    Status: Ready to start

STEP 5: Start All Services
    $ gravity start
        ↓
    ServiceManager (for user-service):
        1. Prepare environment:
            USER_DB_URL=postgresql://user:pass@postgres:5432/user_db
        2. Start container:
            docker run -d \
              --name user-service \
              --network gravity-net \
              -p 8002:8000 \
              -e USER_DB_URL=... \
              user-service-image
        3. Health check:
            GET http://user-service:8000/health → 200 OK
        4. Mark as running
        ↓
    ServiceManager (for auth-service):
        1. Prepare environment:
            AUTH_DB_URL=postgresql://...
            AUTH_CACHE_URL=redis://...
            USER_SERVICE_URL=http://user-service:8000
        2. Start container (same process)
        3. Health check → 200 OK
        4. Mark as running
        ↓
    TraefikConfigurator:
        - Generate routes for all services
        - Start Traefik container
        - Routes active

STEP 6: Verify Status
    $ gravity status
        ↓
    Total Services: 2
    Running: 2 | Stopped: 0 | Error: 0

    ┌──────────────┬─────────┬──────┬─────────┬───────────┬──────────────┐
    │ Service      │ Version │ Type │ Status  │ Ports     │ Databases    │
    ├──────────────┼─────────┼──────┼─────────┼───────────┼──────────────┤
    │ user-service │ 1.5.0   │ api  │ running │ 8000→8002 │ user_db      │
    │ auth-service │ 1.0.0   │ api  │ running │ 8000→8001 │ auth_db,     │
    │              │         │      │         │           │ auth_cache   │
    └──────────────┴─────────┴──────┴─────────┴───────────┴──────────────┘

STEP 7: Access Application
    - Direct: http://localhost:8001/api/auth/login
    - Gateway: http://localhost/api/auth/login
    - Dashboard: http://localhost:9000 (gravity dashboard)
```

---

## 🌐 Network Architecture

### Container Network: `gravity-net`

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Network: gravity-net            │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │ auth-service │    │ user-service │    │payment-service│ │
│  │ :8000        │───→│ :8000        │    │ :8000        │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │         │
│         ↓                    ↓                    ↓         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │ postgres     │    │ postgres     │    │ mysql        │ │
│  │ (auth_db)    │    │ (user_db)    │    │ (payment_db) │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Traefik API Gateway                      │  │
│  │  /api/auth → auth-service:8000                       │  │
│  │  /api/users → user-service:8000                      │  │
│  │  /api/payments → payment-service:8000                │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                    ┌───────┴───────┐
                    │ Port 80/443   │
                    │ (External)    │
                    └───────────────┘
```

### Service Communication:

1. **Internal (Service-to-Service):**
   - DNS: `http://user-service:8000`
   - No need for port mapping
   - Automatic service discovery

2. **External (Client-to-Service):**
   - Via API Gateway: `http://localhost/api/auth`
   - Traefik routes to correct service
   - Load balancing included

---

## 📊 Data Flow Example: User Login

```
1. Client Request:
    POST http://localhost/api/auth/login
    {email: "user@example.com", password: "secret"}
        ↓
2. Traefik API Gateway:
    - Receives request on :80
    - Matches rule: PathPrefix(`/api/auth`)
    - Routes to: auth-service:8000
        ↓
3. Auth Service:
    - Validates credentials
    - Needs to check if user exists
    - Makes request to user-service:
        GET http://user-service:8000/api/users/by-email/user@example.com
        ↓
4. User Service:
    - Queries database:
        SELECT * FROM users WHERE email = 'user@example.com'
    - Returns user data
        ↓
5. Auth Service:
    - Verifies password hash
    - Generates JWT token
    - Stores session in Redis:
        SET session:abc123 {user_id: 1, ...} EX 3600
    - Returns token to client
        ↓
6. Client Receives:
    {token: "eyJhbGciOiJ...", user: {...}}
```

**Key Points:**
- ✅ Services communicate via HTTP (REST APIs)
- ✅ Each service has its own database
- ✅ No direct database access between services
- ✅ Environment variables provide service URLs

---

## 🔐 Security Architecture

### 1. Network Isolation
```
┌─────────────────────────────────────────┐
│     External Network (Internet)         │
└────────────────┬────────────────────────┘
                 │ (Only port 80/443)
          ┌──────┴──────┐
          │   Traefik   │ ← TLS termination
          │  (Gateway)  │ ← Rate limiting
          └──────┬──────┘ ← Authentication
                 │
┌────────────────┴────────────────────────┐
│    Internal Network (gravity-net)       │
│  - Services can only talk to each other │
│  - Databases not exposed externally     │
│  - No direct internet access            │
└─────────────────────────────────────────┘
```

### 2. Secret Management
```python
# Bad (hardcoded)
DATABASE_URL = "postgresql://user:password@localhost/db"

# Good (environment)
DATABASE_URL = os.getenv("DATABASE_URL")

# Better (secrets manager)
DATABASE_URL = await vault.get_secret("database/url")
```

### 3. Authentication Flow
```
Client → Gateway (API Key check) → Service (JWT validation) → Database
```

---

## 📈 Scalability Strategy

### Horizontal Scaling

```yaml
# gravity-service.yaml
scaling:
  min_instances: 2
  max_instances: 10
  metrics:
    - type: cpu
      target: 70%
    - type: memory
      target: 80%
```

**Implementation:**
```
gravity scale auth-service --replicas 3
    ↓
Creates 3 containers:
    - auth-service-1 :8001
    - auth-service-2 :8002
    - auth-service-3 :8003
    ↓
Traefik load balances:
    Round-robin between instances
```

---

## 🎛️ Configuration Hierarchy

```
1. Default (framework defaults)
    ↓
2. Service Manifest (gravity-service.yaml)
    ↓
3. Environment Variables (.env)
    ↓
4. Runtime Arguments (CLI flags)
```

**Example:**
```yaml
# Service manifest
port: 8000

# .env
AUTH_SERVICE_PORT=8001

# CLI
gravity start auth-service --port 8002

# Result: Uses 8002 (highest priority)
```

---

## 🧪 Testing Strategy

### 1. Unit Tests
```python
# Test dependency resolver
def test_resolve_simple_dependency():
    services = [service_a, service_b]
    resolver = DependencyResolver()
    order = resolver.resolve(services)
    assert order == [service_b, service_a]
```

### 2. Integration Tests
```python
# Test complete orchestration
async def test_orchestrate_two_services():
    framework = GravityFramework()
    await framework.add_service("https://github.com/org/auth")
    await framework.install()
    await framework.start()
    
    # Verify both running
    status = await framework.get_status()
    assert all(s.status == "running" for s in status)
```

### 3. End-to-End Tests
```bash
# Real scenario test
gravity init test-app
gravity add https://github.com/gravity/auth-service
gravity install
gravity start
curl http://localhost/api/auth/health
# Expect: 200 OK
```

---

## 📚 Plugin System Architecture

### Plugin Types:

1. **Discovery Plugins**
   - GitLab support
   - Bitbucket support
   - Local file system
   - Docker Hub

2. **Database Plugins**
   - PostgreSQL (built-in)
   - MySQL (built-in)
   - MongoDB (built-in)
   - Redis (built-in)
   - CockroachDB
   - Cassandra

3. **Gateway Plugins**
   - Traefik (default)
   - NGINX
   - Kong
   - Envoy

4. **Deployment Plugins**
   - Docker Compose (built-in)
   - Kubernetes
   - Docker Swarm
   - Nomad

### Plugin Interface:

```python
from gravity_framework.plugins import Plugin

class CustomDatabasePlugin(Plugin):
    """Plugin for CockroachDB support."""
    
    name = "cockroachdb"
    version = "1.0.0"
    
    async def create_database(self, config: dict) -> str:
        """Create database and return connection string."""
        
    async def drop_database(self, name: str):
        """Drop database."""
```

---

## 🔮 Future Architecture Enhancements

### 1. Event-Driven Architecture
```python
# Service publishes event
await event_bus.publish("user.created", {user_id: 123})

# Other services subscribe
@subscribe("user.created")
async def on_user_created(event):
    # Send welcome email
    pass
```

### 2. GraphQL Federation
```graphql
# Unified API across all services
type Query {
  user(id: ID!): User @service(name: "user-service")
  orders(userId: ID!): [Order] @service(name: "order-service")
}
```

### 3. Service Mesh Integration (Istio)
```yaml
# Automatic mutual TLS
# Automatic retry policies
# Automatic circuit breakers
# Distributed tracing
```

---

**This architecture ensures Gravity Framework is:**
- 🚀 **Fast** - Minimal overhead
- 🛡️ **Secure** - Defense in depth
- 📈 **Scalable** - Horizontal scaling ready
- 🔧 **Maintainable** - Clean separation of concerns
- 🎯 **User-friendly** - Simple CLI, powerful features

---

*For implementation details, see ROADMAP.md*
*For team standards, see TEAM_PROMPT.md*
