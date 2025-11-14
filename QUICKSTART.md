# 🚀 Gravity Framework - Quick Start Guide

این راهنما شما را در 10 دقیقه با Gravity Framework آشنا می‌کند.

## 📦 نصب

```bash
pip install gravity-framework
```

## 🎯 گام ۱: ایجاد پروژه

```bash
# پروژه جدید بسازید
gravity init my-microservices-app

# وارد دایرکتوری پروژه شوید
cd my-microservices-app
```

این دستور ساختار زیر را ایجاد می‌کند:
```
my-microservices-app/
├── .gravity/
│   └── config.yaml
├── services/
└── config/
```

## 🔍 گام ۲: اضافه کردن سرویس‌ها

```bash
# از Git repository
gravity add https://github.com/your-org/auth-service

# از مسیر محلی
gravity add ./my-local-service

# با انتخاب branch خاص
gravity add https://github.com/your-org/user-service --branch develop
```

## 📋 گام ۳: مشاهده سرویس‌های کشف شده

```bash
gravity list
```

خروجی:
```
┌──────────────────────────────────────────────────┐
│              Discovered Services                  │
├────────────────┬─────────┬────────┬──────────────┤
│ Name           │ Version │ Type   │ Status       │
├────────────────┼─────────┼────────┼──────────────┤
│ auth-service   │ 1.0.0   │ api    │ discovered   │
│ user-service   │ 2.1.0   │ api    │ discovered   │
└────────────────┴─────────┴────────┴──────────────┘
```

## 📦 گام ۴: نصب سرویس‌ها

```bash
# نصب همه سرویس‌ها
gravity install
```

این دستور:
- ✅ Dependencies را حل می‌کند
- ✅ پایگاه‌داده‌ها را خودکار می‌سازد
- ✅ سرویس‌ها را به ترتیب صحیح نصب می‌کند

## 🚀 گام ۵: اجرای سرویس‌ها

```bash
# شروع همه سرویس‌ها
gravity start
```

Gravity:
- ✅ هر سرویس را در Docker container جداگانه اجرا می‌کند
- ✅ Connection string های دیتابیس را تزریق می‌کند
- ✅ Portها را به صورت خودکار map می‌کند
- ✅ Health check را راه‌اندازی می‌کند

## 📊 گام ۶: مانیتورینگ

### مشاهده وضعیت
```bash
gravity status
```

خروجی:
```
Total Services: 2
Running: 2 | Stopped: 0 | Error: 0

┌──────────────┬─────────┬──────┬─────────┬───────────┬──────────────┐
│ Service      │ Version │ Type │ Status  │ Ports     │ Databases    │
├──────────────┼─────────┼──────┼─────────┼───────────┼──────────────┤
│ auth-service │ 1.0.0   │ api  │ running │ 8000→8001 │ auth_db      │
│ user-service │ 2.1.0   │ api  │ running │ 8000→8002 │ users_db     │
└──────────────┴─────────┴──────┴─────────┴───────────┴──────────────┘
```

### چک کردن سلامت
```bash
gravity health
```

### مشاهده لاگ‌ها
```bash
# لاگ‌های یک سرویس خاص
gravity logs auth-service

# 50 خط آخر
gravity logs auth-service --tail 50

# Follow کردن لاگ‌ها (real-time)
gravity logs auth-service -f
```

## 🛑 گام ۷: مدیریت سرویس‌ها

```bash
# توقف همه
gravity stop

# توقف یک سرویس خاص
gravity stop auth-service

# Restart
gravity restart auth-service

# Restart همه
gravity restart
```

## 📝 ساخت Service Manifest

برای اینکه سرویس شما توسط Gravity قابل شناسایی باشد، فایل `gravity-service.yaml` ایجاد کنید:

```yaml
# gravity-service.yaml
name: my-service
version: 1.0.0
description: My awesome microservice
type: api

# Dependencies
dependencies:
  - name: other-service
    version: ">=1.0.0"

# Databases (خودکار ساخته می‌شوند!)
databases:
  - name: my_service_db
    type: postgresql
    extensions:
      - uuid-ossp

# Runtime
runtime: python:3.11
command: uvicorn main:app --host 0.0.0.0 --port 8000
working_dir: /app

# Ports
ports:
  - container: 8000
    host: 8001  # اختیاری، اگر ندهید خودکار assign می‌شود

# Health Check
health_check:
  endpoint: /health
  interval: 30
  timeout: 5
  retries: 3

# Environment Variables
environment:
  variables:
    LOG_LEVEL: info
    DEBUG: "false"
  secrets:
    - API_SECRET
    - DB_PASSWORD

# API Gateway
api_prefix: /api/myservice
public: true

# Resource Limits
cpu_limit: "1.0"
memory_limit: "512M"
```

## 🗄️ مثال: Automatic Database Creation

```yaml
# در gravity-service.yaml
databases:
  # PostgreSQL با extension
  - name: main_db
    type: postgresql
    version: "15"
    extensions:
      - uuid-ossp
      - pgcrypto

  # MySQL با charset
  - name: legacy_db
    type: mysql
    version: "8.0"
    charset: utf8mb4
    collation: utf8mb4_unicode_ci

  # MongoDB
  - name: analytics_db
    type: mongodb
    version: "6.0"

  # Redis
  - name: cache
    type: redis
    version: "7"
```

Gravity به طور خودکار:
1. ✅ تمام دیتابیس‌ها را می‌سازد
2. ✅ Extensions را نصب می‌کند
3. ✅ Connection strings می‌سازد
4. ✅ به عنوان environment variable تزریق می‌کند:
   - `MAIN_DB_URL=postgresql://...`
   - `LEGACY_DB_URL=mysql://...`
   - `ANALYTICS_DB_URL=mongodb://...`
   - `CACHE_URL=redis://...`

## 🔗 مثال: Dependency Resolution

```yaml
# auth-service/gravity-service.yaml
name: auth-service
version: 2.0.0
dependencies:
  - name: user-service
    version: ">=1.5.0"
  - name: redis-cache
    version: "^3.0.0"

# user-service/gravity-service.yaml
name: user-service
version: 1.8.0
dependencies:
  - name: database-service
    version: "~2.1.0"

# database-service/gravity-service.yaml
name: database-service
version: 2.1.3
dependencies: []
```

Gravity:
- ✅ حل می‌کند: `database-service` → `user-service` → `auth-service`
- ✅ به همین ترتیب نصب و start می‌کند
- ✅ Version conflict ها را شناسایی می‌کند
- ✅ Circular dependency ها را detect می‌کند

## 🎓 دستورات کامل CLI

### مدیریت پروژه
```bash
gravity init <project>          # ایجاد پروژه
gravity add <repo-url>           # اضافه کردن سرویس
gravity list                     # لیست سرویس‌ها
```

### نصب و اجرا
```bash
gravity install                  # نصب همه
gravity install <service>        # نصب یک سرویس
gravity start                    # شروع همه
gravity start <service>          # شروع یک سرویس
gravity stop                     # توقف همه
gravity stop <service>           # توقف یک سرویس
gravity restart                  # Restart همه
gravity restart <service>        # Restart یک سرویس
```

### مانیتورینگ
```bash
gravity status                   # وضعیت سرویس‌ها
gravity health                   # سلامت سرویس‌ها
gravity logs <service>           # لاگ‌های سرویس
gravity logs <service> -f        # Follow logs
gravity logs <service> --tail 50 # 50 خط آخر
```

### پیشرفته (Coming Soon)
```bash
gravity dashboard                # Web UI
gravity db list                  # لیست دیتابیس‌ها
gravity db shell <dbname>        # اتصال به DB
gravity config show              # نمایش تنظیمات
```

## 💡 Tips & Best Practices

### 1. استفاده از .gitignore
```gitignore
# در پروژه اصلی
services/
.gravity/state.json
*.log
```

### 2. Environment Variables
از فایل `.env` برای secrets استفاده کنید:
```bash
# .env
POSTGRES_PASSWORD=secretpass123
REDIS_PASSWORD=redis123
JWT_SECRET=mysecret
```

### 3. Development vs Production
```yaml
# gravity-service.yaml
environment:
  variables:
    ENV: ${ENVIRONMENT:development}
    DEBUG: ${DEBUG:true}
```

### 4. Health Checks
همیشه health check endpoint تعریف کنید:
```python
# FastAPI example
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### 5. Logging
از structured logging استفاده کنید:
```python
import structlog
logger = structlog.get_logger()
```

## 🐛 Troubleshooting

### مشکل: سرویس شروع نمی‌شود
```bash
# چک کردن لاگ‌ها
gravity logs <service>

# چک کردن وضعیت
gravity status

# Restart
gravity restart <service>
```

### مشکل: Dependency conflict
```bash
# لیست Dependencies
gravity list

# نصب مجدد
gravity install --force
```

### مشکل: Database connection error
```bash
# چک کردن دیتابیس‌های ساخته شده
gravity db list

# بررسی environment variables
gravity logs <service> | grep "DB_URL"
```

## 📚 منابع بیشتر

- [Full Documentation](https://gravity-framework.readthedocs.io)
- [Service Manifest Reference](docs/manifest-format.md)
- [CLI Reference](docs/cli-reference.md)
- [Architecture](docs/architecture.md)
- [Examples](examples/)

## 🎉 شما آماده‌اید!

اکنون می‌توانید:
- ✅ سرویس‌های خود را با Gravity مدیریت کنید
- ✅ Dependencies را به صورت خودکار حل کنید
- ✅ Databases را بدون configuration بسازید
- ✅ تمام سرویس‌ها را با یک دستور start کنید

**Welcome to Gravity Framework! 🚀**
