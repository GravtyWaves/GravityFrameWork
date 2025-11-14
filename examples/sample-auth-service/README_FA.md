# راهنمای استفاده از نمونه سرویس احراز هویت

این یک نمونه کامل از یک میکروسرویس است که با Gravity Framework کار می‌کند.

## 🎯 ویژگی‌ها

- ✅ احراز هویت با JWT
- ✅ مدیریت کاربران
- ✅ Session Management با Redis
- ✅ API Documentation اتوماتیک
- ✅ Health Check
- ✅ Docker و Docker Compose
- ✅ تست‌های کامل
- ✅ آماده برای Production

## 🚀 نصب و راه‌اندازی

### روش اول: با Gravity Framework (توصیه می‌شود)

```bash
# 1. ابتدا Gravity Framework را نصب کنید
pip install gravity-framework

# 2. یک پروژه جدید بسازید
gravity init my-app

# 3. سرویس احراز هویت را اضافه کنید
cd my-app
gravity add ../sample-auth-service

# 4. سرویس‌ها را نصب کنید
gravity install

# 5. دیتابیس‌ها را بسازید (اتوماتیک)
# Gravity Framework به طور خودکار PostgreSQL و Redis را ایجاد می‌کند

# 6. سرویس را اجرا کنید
gravity start
```

### روش دوم: استقلال (بدون Gravity)

```bash
# 1. فایل محیطی را کپی کنید
cp .env.example .env

# 2. PostgreSQL و Redis را اجرا کنید
docker-compose up -d postgres redis

# 3. وابستگی‌ها را نصب کنید
pip install -r requirements.txt

# 4. سرویس را اجرا کنید
uvicorn app.main:app --reload
```

## 📝 استفاده از API

### ثبت نام کاربر جدید

```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "mypassword123"
  }'
```

### ورود

```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "mypassword123"
  }'
```

پاسخ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### دریافت اطلاعات کاربر

```bash
curl -X GET http://localhost:8001/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### خروج

```bash
curl -X POST http://localhost:8001/api/v1/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🧪 تست

```bash
# اجرای تست‌ها
pytest tests/ -v

# با Coverage
pytest tests/ -v --cov=app --cov-report=html

# گزارش Coverage در htmlcov/index.html
```

## 📊 مستندات API

پس از اجرای سرویس، به آدرس زیر بروید:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 🔧 تنظیمات

همه تنظیمات از طریق Environment Variables انجام می‌شود:

```env
# پایگاه داده (اتوماتیک توسط Gravity)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/auth_db

# Redis (اتوماتیک توسط Gravity)
REDIS_URL=redis://localhost:6379

# JWT (مهم: در Production تغییر دهید!)
JWT_SECRET=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# CORS
CORS_ORIGINS=http://localhost:3000
```

## 🐳 Docker

```bash
# Build
docker build -t auth-service:latest .

# Run
docker run -p 8001:8001 \
  -e DATABASE_URL=postgresql+asyncpg://... \
  -e REDIS_URL=redis://... \
  -e JWT_SECRET=your-secret \
  auth-service:latest
```

## 📁 ساختار پروژه

```
sample-auth-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # برنامه اصلی FastAPI
│   ├── config.py            # تنظیمات
│   ├── models.py            # مدل‌های دیتابیس
│   ├── database.py          # اتصال به دیتابیس
│   └── api/
│       └── v1/
│           └── auth.py      # Endpoint های احراز هویت
├── tests/
│   ├── conftest.py          # تنظیمات تست
│   └── test_auth.py         # تست‌های API
├── gravity-service.yaml     # Manifest فریم‌ورک
├── Dockerfile               # تصویر Docker
├── docker-compose.yml       # Compose برای توسعه
├── requirements.txt         # وابستگی‌ها
└── .env.example             # نمونه تنظیمات
```

## 🔐 امنیت

- ✅ رمزعبور با bcrypt هش می‌شود
- ✅ JWT Token برای احراز هویت
- ✅ Session Management با Redis
- ✅ Rate Limiting
- ✅ CORS Configuration
- ✅ Input Validation با Pydantic

## 📈 مانیتورینگ

```bash
# Health Check
curl http://localhost:8001/health

# Readiness Check
curl http://localhost:8001/ready

# Metrics (اگر فعال باشد)
curl http://localhost:9090/metrics
```

## 🤝 مشارکت

این یک نمونه آموزشی است. می‌توانید آن را تغییر دهید:

1. پیاده‌سازی کامل JWT و hashing
2. اضافه کردن Refresh Token
3. پیاده‌سازی Role-Based Access Control (RBAC)
4. اضافه کردن OAuth2 و Social Login
5. پیاده‌سازی Two-Factor Authentication (2FA)

## ⚠️ نکات مهم

1. حتماً `JWT_SECRET` را در production تغییر دهید
2. برای production از HTTPS استفاده کنید
3. Rate Limiting را فعال کنید
4. Log ها را مانیتور کنید
5. Backup از دیتابیس بگیرید

## 📚 منابع

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [Gravity Framework Documentation](../README.md)

---

ساخته شده با ❤️ توسط Gravity Framework Team
