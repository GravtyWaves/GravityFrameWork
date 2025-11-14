"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/devops/automation.py
PURPOSE: DevOps automation (Docker, Kubernetes, CI/CD)
DESCRIPTION: Automates DevOps tasks including Docker containerization, Kubernetes
             deployment, and CI/CD pipeline generation.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""


import logging
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any
import yaml
import json

from gravity_framework.models.service import Service, ServiceType

logger = logging.getLogger(__name__)


class DevOpsAutomation:
    """Automates ALL DevOps tasks for web applications."""
    
    def __init__(self, project_path: Path):
        """Initialize DevOps automation.
        
        Args:
            project_path: Project root directory
        """
        self.project_path = project_path
        self.infra_dir = project_path / "infrastructure"
        self.infra_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.infra_dir / "nginx").mkdir(exist_ok=True)
        (self.infra_dir / "monitoring").mkdir(exist_ok=True)
        (self.infra_dir / "scripts").mkdir(exist_ok=True)
        (self.infra_dir / "backups").mkdir(exist_ok=True)
    
    def setup_complete_infrastructure(self, services: List[Service]) -> Dict[str, Any]:
        """Setup complete web application infrastructure.
        
        Args:
            services: Discovered services
            
        Returns:
            Infrastructure setup summary
        """
        logger.info("🚀 Setting up COMPLETE web application infrastructure...")
        
        results = {
            "nginx": False,
            "docker": False,
            "monitoring": False,
            "ci_cd": False,
            "backups": False,
            "ssl": False
        }
        
        # 1. Setup Nginx reverse proxy
        logger.info("📦 Step 1/6: Configuring Nginx reverse proxy...")
        results["nginx"] = self._setup_nginx(services)
        
        # 2. Generate Docker infrastructure
        logger.info("🐳 Step 2/6: Generating Docker infrastructure...")
        results["docker"] = self._setup_docker_infrastructure(services)
        
        # 3. Setup monitoring (Prometheus + Grafana)
        logger.info("📊 Step 3/6: Setting up monitoring stack...")
        results["monitoring"] = self._setup_monitoring(services)
        
        # 4. Generate CI/CD pipeline
        logger.info("🔄 Step 4/6: Generating CI/CD pipeline...")
        results["ci_cd"] = self._setup_cicd(services)
        
        # 5. Setup backup automation
        logger.info("💾 Step 5/6: Configuring automated backups...")
        results["backup"] = self._setup_backups(services)
        
        # 6. Setup SSL/TLS
        logger.info("🔒 Step 6/6: Configuring SSL/TLS certificates...")
        results["ssl"] = self._setup_ssl()
        
        # Generate deployment script
        self._generate_deployment_script(services)
        
        logger.info("✅ Complete infrastructure setup finished!")
        return results
    
    def _setup_nginx(self, services: List[Service]) -> bool:
        """Setup Nginx reverse proxy with load balancing.
        
        Args:
            services: List of services
            
        Returns:
            True if successful
        """
        try:
            # Find web services and APIs
            web_services = [s for s in services if s.manifest.type == ServiceType.WEB]
            api_services = [s for s in services if s.manifest.type == ServiceType.API]
            
            # Generate main Nginx config
            nginx_conf = self._generate_nginx_config(web_services, api_services)
            
            nginx_file = self.infra_dir / "nginx" / "nginx.conf"
            nginx_file.write_text(nginx_conf)
            
            # Generate upstream configs for load balancing
            for service in api_services:
                upstream_conf = self._generate_upstream_config(service)
                upstream_file = self.infra_dir / "nginx" / f"{service.manifest.name}-upstream.conf"
                upstream_file.write_text(upstream_conf)
            
            logger.info(f"✓ Nginx configuration generated: {nginx_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Nginx: {e}")
            return False
    
    def _generate_nginx_config(self, web_services: List[Service], api_services: List[Service]) -> str:
        """Generate Nginx configuration."""
        
        config = """# Gravity Framework - Auto-generated Nginx Configuration
# DO NOT EDIT MANUALLY - Generated by DevOps Automation

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

"""
        
        # Add upstream definitions for APIs
        for service in api_services:
            config += f"""
    # Upstream for {service.manifest.name}
    upstream {service.manifest.name}_backend {{
        least_conn;
        server {service.manifest.name}:8000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }}
"""
        
        # Main server block
        config += """
    # Main application server
    server {
        listen 80;
        listen [::]:80;
        server_name localhost;

        # Security
        client_max_body_size 100M;
        
"""
        
        # Add API routes
        for service in api_services:
            api_prefix = service.manifest.api_prefix or f"/api/{service.manifest.name}"
            config += f"""
        # {service.manifest.name} API
        location {api_prefix} {{
            proxy_pass http://{service.manifest.name}_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }}
"""
        
        # Add frontend routes
        for service in web_services:
            config += f"""
        # {service.manifest.name} Frontend
        location / {{
            proxy_pass http://{service.manifest.name}:3000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }}
"""
        
        config += """
        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }
    }
}
"""
        
        return config
    
    def _generate_upstream_config(self, service: Service) -> str:
        """Generate upstream configuration for load balancing."""
        
        return f"""# Upstream configuration for {service.manifest.name}
# Load balancing with health checks

upstream {service.manifest.name}_backend {{
    least_conn;  # Load balancing algorithm
    
    # Primary instances
    server {service.manifest.name}_1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server {service.manifest.name}_2:8000 weight=1 max_fails=3 fail_timeout=30s;
    
    # Backup instance
    server {service.manifest.name}_backup:8000 backup;
    
    # Connection pooling
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}}
"""
    
    def _setup_docker_infrastructure(self, services: List[Service]) -> bool:
        """Generate complete Docker infrastructure."""
        
        try:
            # Generate production docker-compose
            compose = self._generate_production_compose(services)
            compose_file = self.project_path / "docker-compose.production.yml"
            compose_file.write_text(yaml.dump(compose, default_flow_style=False, sort_keys=False))
            
            # Generate Dockerfiles for each service
            for service in services:
                if service.path:
                    dockerfile = self._generate_dockerfile(service)
                    df_path = Path(service.path) / "Dockerfile.production"
                    df_path.write_text(dockerfile)
            
            # Generate .dockerignore
            dockerignore = self._generate_dockerignore()
            (self.project_path / ".dockerignore").write_text(dockerignore)
            
            logger.info("✓ Docker infrastructure generated")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Docker: {e}")
            return False
    
    def _generate_production_compose(self, services: List[Service]) -> Dict:
        """Generate production-ready docker-compose.yml."""
        
        compose = {
            "version": "3.8",
            "services": {},
            "networks": {
                "frontend": {"driver": "bridge"},
                "backend": {"driver": "bridge"},
                "monitoring": {"driver": "bridge"}
            },
            "volumes": {}
        }
        
        # Add Nginx
        compose["services"]["nginx"] = {
            "image": "nginx:alpine",
            "ports": ["80:80", "443:443"],
            "volumes": [
                "./infrastructure/nginx/nginx.conf:/etc/nginx/nginx.conf:ro",
                "./infrastructure/nginx/ssl:/etc/nginx/ssl:ro"
            ],
            "networks": ["frontend", "backend"],
            "depends_on": [s.manifest.name for s in services],
            "restart": "unless-stopped",
            "healthcheck": {
                "test": ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"],
                "interval": "30s",
                "timeout": "10s",
                "retries": 3
            }
        }
        
        # Add each service
        for service in services:
            service_config = {
                "build": {
                    "context": f"./{Path(service.path).name}" if service.path else ".",
                    "dockerfile": "Dockerfile.production"
                },
                "image": f"{service.manifest.name}:latest",
                "restart": "unless-stopped",
                "networks": ["backend"],
                "healthcheck": {
                    "test": ["CMD", "curl", "-f", "http://localhost:8000/health"],
                    "interval": "30s",
                    "timeout": "10s",
                    "retries": 3,
                    "start_period": "40s"
                }
            }
            
            # Add environment variables
            if service.manifest.environment:
                service_config["environment"] = service.manifest.environment.variables
            
            # Add resource limits
            if service.manifest.cpu_limit or service.manifest.memory_limit:
                service_config["deploy"] = {
                    "resources": {
                        "limits": {}
                    }
                }
                if service.manifest.cpu_limit:
                    service_config["deploy"]["resources"]["limits"]["cpus"] = service.manifest.cpu_limit
                if service.manifest.memory_limit:
                    service_config["deploy"]["resources"]["limits"]["memory"] = service.manifest.memory_limit
            
            compose["services"][service.manifest.name] = service_config
        
        # Add databases
        compose["services"]["postgres"] = {
            "image": "postgres:15-alpine",
            "environment": {
                "POSTGRES_PASSWORD": "${POSTGRES_PASSWORD}",
                "POSTGRES_USER": "${POSTGRES_USER:-postgres}",
                "POSTGRES_DB": "${POSTGRES_DB:-app}"
            },
            "volumes": ["postgres_data:/var/lib/postgresql/data"],
            "networks": ["backend"],
            "restart": "unless-stopped",
            "healthcheck": {
                "test": ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"],
                "interval": "10s",
                "timeout": "5s",
                "retries": 5
            }
        }
        
        compose["services"]["redis"] = {
            "image": "redis:7-alpine",
            "command": "redis-server --appendonly yes",
            "volumes": ["redis_data:/data"],
            "networks": ["backend"],
            "restart": "unless-stopped",
            "healthcheck": {
                "test": ["CMD", "redis-cli", "ping"],
                "interval": "10s",
                "timeout": "3s",
                "retries": 5
            }
        }
        
        # Add volumes
        compose["volumes"] = {
            "postgres_data": {},
            "redis_data": {},
            "backup_data": {}
        }
        
        return compose
    
    def _generate_dockerfile(self, service: Service) -> str:
        """Generate production-optimized Dockerfile."""
        
        if service.manifest.runtime.startswith("python"):
            return f"""# Multi-stage build for {service.manifest.name}
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application
COPY . .

# Make sure scripts are executable
RUN chmod +x *.sh || true

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        else:
            return f"""# Dockerfile for {service.manifest.name}
FROM {service.manifest.runtime}

WORKDIR /app

COPY . .

RUN chmod +x *.sh || true

EXPOSE 8000

CMD ["sh", "-c", "{service.manifest.command or 'npm start'}"]
"""
    
    def _generate_dockerignore(self) -> str:
        """Generate .dockerignore file."""
        
        return """# Git
.git
.gitignore
.gitattributes

# Python
__pycache__
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt

# Node
node_modules/
npm-debug.log
yarn-error.log

# IDE
.vscode
.idea
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Tests
.pytest_cache
.coverage
htmlcov/
.tox/

# Documentation
docs/
*.md

# CI/CD
.github/
.gitlab-ci.yml

# Logs
*.log
logs/

# Environment
.env
.env.local
.env.*.local

# Build
dist/
build/
*.egg-info/
"""
    
    def _setup_monitoring(self, services: List[Service]) -> bool:
        """Setup Prometheus + Grafana monitoring."""
        
        try:
            # Generate Prometheus config
            prometheus_config = self._generate_prometheus_config(services)
            prom_file = self.infra_dir / "monitoring" / "prometheus.yml"
            prom_file.write_text(prometheus_config)
            
            # Generate Grafana dashboards
            dashboard = self._generate_grafana_dashboard(services)
            dashboard_file = self.infra_dir / "monitoring" / "dashboard.json"
            dashboard_file.write_text(json.dumps(dashboard, indent=2))
            
            logger.info("✓ Monitoring stack configured")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup monitoring: {e}")
            return False
    
    def _generate_prometheus_config(self, services: List[Service]) -> str:
        """Generate Prometheus configuration."""
        
        config = """# Prometheus configuration
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:9113']

"""
        
        for service in services:
            config += f"""  - job_name: '{service.manifest.name}'
    static_configs:
      - targets: ['{service.manifest.name}:8000']
    metrics_path: '/metrics'
    
"""
        
        return config
    
    def _generate_grafana_dashboard(self, services: List[Service]) -> Dict:
        """Generate Grafana dashboard JSON."""
        
        return {
            "dashboard": {
                "title": "Gravity Framework - Services Dashboard",
                "panels": [
                    {
                        "title": f"{service.manifest.name} - Requests/sec",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": f"rate(http_requests_total{{job='{service.manifest.name}'}}[5m])"
                            }
                        ]
                    }
                    for service in services
                ]
            }
        }
    
    def _setup_cicd(self, services: List[Service]) -> bool:
        """Generate CI/CD pipeline (GitHub Actions)."""
        
        try:
            github_dir = self.project_path / ".github" / "workflows"
            github_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate deployment workflow
            workflow = self._generate_github_actions_workflow(services)
            workflow_file = github_dir / "deploy.yml"
            workflow_file.write_text(workflow)
            
            logger.info("✓ CI/CD pipeline generated")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup CI/CD: {e}")
            return False
    
    def _generate_github_actions_workflow(self, services: List[Service]) -> str:
        """Generate GitHub Actions workflow."""
        
        return """name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          docker-compose -f docker-compose.test.yml up --abort-on-container-exit
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build images
        run: |
          docker-compose -f docker-compose.production.yml build
      
      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker-compose -f docker-compose.production.yml push
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/app
            docker-compose -f docker-compose.production.yml pull
            docker-compose -f docker-compose.production.yml up -d
            docker system prune -f
"""
    
    def _setup_backups(self, services: List[Service]) -> bool:
        """Setup automated database backups."""
        
        try:
            backup_script = self._generate_backup_script()
            script_file = self.infra_dir / "scripts" / "backup.sh"
            script_file.write_text(backup_script)
            script_file.chmod(0o755)
            
            # Generate cron job
            cron_config = """# Database backup cron job
0 2 * * * /opt/app/infrastructure/scripts/backup.sh >> /var/log/backup.log 2>&1
"""
            cron_file = self.infra_dir / "scripts" / "backup.cron"
            cron_file.write_text(cron_config)
            
            logger.info("✓ Backup automation configured")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup backups: {e}")
            return False
    
    def _generate_backup_script(self) -> str:
        """Generate backup script."""
        
        return """#!/bin/bash
# Automated database backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/app/infrastructure/backups"

# Backup PostgreSQL
docker exec postgres pg_dumpall -U postgres | gzip > "$BACKUP_DIR/postgres_$DATE.sql.gz"

# Backup Redis
docker exec redis redis-cli --rdb /data/dump.rdb
docker cp redis:/data/dump.rdb "$BACKUP_DIR/redis_$DATE.rdb"

# Keep only last 7 days
find "$BACKUP_DIR" -name "*.gz" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.rdb" -mtime +7 -delete

echo "Backup completed: $DATE"
"""
    
    def _setup_ssl(self) -> bool:
        """Setup SSL/TLS with Let's Encrypt."""
        
        try:
            certbot_script = """#!/bin/bash
# SSL certificate setup with Let's Encrypt

docker run -it --rm \
  -v /opt/app/infrastructure/nginx/ssl:/etc/letsencrypt \
  certbot/certbot certonly --webroot \
  -w /var/www/certbot \
  -d example.com \
  --email admin@example.com \
  --agree-tos \
  --no-eff-email

# Auto-renewal cron job
# 0 0 * * * docker run --rm -v /opt/app/infrastructure/nginx/ssl:/etc/letsencrypt certbot/certbot renew
"""
            
            ssl_script = self.infra_dir / "scripts" / "setup-ssl.sh"
            ssl_script.write_text(certbot_script)
            ssl_script.chmod(0o755)
            
            logger.info("✓ SSL/TLS setup script generated")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup SSL: {e}")
            return False
    
    def _generate_deployment_script(self, services: List[Service]):
        """Generate master deployment script."""
        
        deploy_script = """#!/bin/bash
# Master deployment script - One command deployment!

set -e

echo "🚀 Starting deployment..."

# 1. Build all services
echo "📦 Building services..."
docker-compose -f docker-compose.production.yml build

# 2. Run database migrations
echo "🔄 Running migrations..."
for service in $(docker-compose -f docker-compose.production.yml config --services); do
    if docker-compose -f docker-compose.production.yml run --rm $service python manage.py migrate 2>/dev/null; then
        echo "✓ Migrations for $service"
    fi
done

# 3. Start services
echo "🚀 Starting services..."
docker-compose -f docker-compose.production.yml up -d

# 4. Wait for health checks
echo "🏥 Waiting for services to be healthy..."
sleep 10

# 5. Run smoke tests
echo "🧪 Running smoke tests..."
curl -f http://localhost/health || exit 1

echo "✅ Deployment completed successfully!"
echo "🌐 Application is live at: http://localhost"
"""
        
        script_file = self.project_path / "deploy.sh"
        script_file.write_text(deploy_script)
        script_file.chmod(0o755)
        
        logger.info(f"✓ Master deployment script: {script_file}")
