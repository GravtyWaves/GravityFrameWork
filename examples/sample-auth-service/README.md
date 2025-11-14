# Sample Microservice for Gravity Framework

This is a complete example of a microservice that works with Gravity Framework.

## Structure

```
sample-auth-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration from environment
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   └── api/
│       └── v1/
│           └── auth.py      # Auth endpoints
├── tests/
│   └── test_auth.py
├── alembic/
│   └── versions/
├── gravity-service.yaml     # Gravity manifest
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

## Quick Start

### Option 1: Using Gravity Framework

```bash
# Add to your Gravity project
gravity add ./sample-auth-service

# Install
gravity install

# Start
gravity start
```

### Option 2: Standalone

```bash
# Copy .env.example to .env and configure
cp .env.example .env

# Start with Docker Compose
docker-compose up -d

# The service will be available at http://localhost:8001
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Authentication
```bash
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/auth_db

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Service
SERVICE_PORT=8001
SERVICE_HOST=0.0.0.0
DEBUG=false
```

## Database Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(id),
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Testing

```bash
pytest tests/ -v --cov=app
```

## Deployment

### Docker

```bash
docker build -t sample-auth-service:latest .
docker run -p 8001:8001 sample-auth-service:latest
```

### Kubernetes

```bash
kubectl apply -f k8s/
```
