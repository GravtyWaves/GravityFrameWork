# 🤖 راهنمای تعاملی هوشمند

## ویژگی جدید: راهنمای گام به گام خودکار!

فریمورک حالا میکروسرویس‌هایت رو **کامل آنالیز** میکنه و **مرحله به مرحله** بهت میگه چیکار کنی.

## چیکار میکنه؟

### ✅ آنالیز عمیق میکروسرویس‌ها:
- 📄 README رو می‌خونه و دستورات نصب رو پیدا میکنه
- 📦 `requirements.txt` رو چک میکنه
- 🐳 `Dockerfile` و `docker-compose.yml` رو بررسی میکنه
- 🗄️ دیتابیس‌های مورد نیاز رو شناسایی میکنه
- 🔗 وابستگی‌ها رو پیدا میکنه
- 🔧 Environment variables مورد نیاز رو لیست میکنه

### 🤖 اجرای خودکار دستورات:
- ✅ دیتابیس‌ها رو خودش میسازه
- ✅ `pip install` رو خودش اجرا میکنه
- ✅ Environment variables رو تنظیم میکنه
- ✅ سرویس‌ها رو استارت میکنه

### 👤 تعامل با کاربر:
- نشون میده چی کار میکنه
- پیشرفت رو نمایش میده
- اگه خطایی بود، میپرسه ادامه بدی یا نه
- در آخر خلاصه کامل میده

## استفاده

### ساده‌ترین روش:

```python
from gravity_framework import GravityFramework

# ساختن فریمورک
framework = GravityFramework(ai_assist=True)

# اضافه کردن میکروسرویس‌ها
framework.discover_services("https://github.com/user/auth-service")
framework.discover_services("https://github.com/user/api-service")

# شروع راهنمای تعاملی
summary = framework.interactive_setup()
```

## چی میبینی؟

```
🤖 Gravity Framework - Interactive Guide
I'll analyze your microservices and guide you step-by-step

⏳ Analyzing your microservices...
```

**آنالیز میکنه:**
- هر میکروسرویس چی نیاز داره
- چه دیتابیسی بخواد
- چه dependency هایی داره
- چه environment variable هایی میخواد

```
✅ Analysis Complete!

┌─────────────────────────────────────┐
│   Microservices Overview            │
├──────────────┬──────┬──────┬────────┤
│ Service      │ Type │ DBs  │ Status │
├──────────────┼──────┼──────┼────────┤
│ auth-service │ api  │ 1    │ 🔨 Needs Build │
│ user-service │ api  │ 1    │ 🔨 Needs Build │
│ api-gateway  │ web  │ 0    │ ✅ Ready │
└──────────────┴──────┴──────┴────────┘

📋 Setup Plan (4 steps):
  1. 🤖 Auto - Create Databases
  2. 🤖 Auto - Install auth-service Dependencies
  3. 🤖 Auto - Install user-service Dependencies
  4. 🤖 Auto - Start All Services

Ready to set up your microservices? [Y/n]: 
```

**اگه بگی بله (Y):**

```
🚀 Starting Setup Process
============================================================

Step 1/4: Create Databases
Create 2 database(s) for your services

🗄️  Creating databases...
  ✓ postgresql database: auth_db (for auth-service)
  ✓ postgresql database: user_db (for user-service)
✅ Create Databases completed!

Step 2/4: Install auth-service Dependencies
Install Python dependencies for auth-service

📦 Installing dependencies for auth-service...
Running: pip install -r requirements.txt
✓ Dependencies installed
✅ Install auth-service Dependencies completed!

Step 3/4: Install user-service Dependencies
Install Python dependencies for user-service

📦 Installing dependencies for user-service...
Running: pip install -r requirements.txt
✓ Dependencies installed
✅ Install user-service Dependencies completed!

Step 4/4: Start All Services
Start all 3 microservices

🚀 Starting services...
  ✓ auth-service will start on port auto
  ✓ user-service will start on port auto
  ✓ api-gateway will start on port auto
✅ Start All Services completed!

============================================================
📊 Setup Summary
============================================================

✅ Completed: 4
❌ Failed: 0
📈 Success Rate: 100.0%

Completed steps:
  ✓ create_databases
  ✓ install_auth-service
  ✓ install_user-service
  ✓ start_services

============================================================
```

## ویژگی‌های خاص

### 1. خواندن README

فریمورک README هر میکروسرویس رو می‌خونه و:
- دستورات نصب (`## Installation`) رو پیدا میکنه
- دستورات اجرا (`## Run`) رو استخراج میکنه
- Environment variables مورد نیاز رو لیست میکنه

### 2. اجرای خودکار دستورات

تا جایی که ممکنه خودش دستورات رو اجرا میکنه:

```python
# اینا خودکار انجام میشه:
subprocess.run("pip install -r requirements.txt", cwd=service_path)
subprocess.run("npm install", cwd=service_path)
subprocess.run("docker-compose up -d", cwd=service_path)
```

### 3. نمایش پیشرفت

با Rich library، پیشرفت رو نشون میده:
- Progress bar برای آنالیز
- Color coding برای موفقیت/خطا
- Table برای نمایش اطلاعات
- Panel برای دستورات مهم

### 4. مدیریت خطا

اگه خطایی رخ داد:
```
❌ Install auth-service Dependencies failed!

Continue anyway? [Y/n]: 
```

کاربر میتونه تصمیم بگیره ادامه بده یا نه.

## مثال کامل

```python
from gravity_framework import GravityFramework
from pathlib import Path

# ساختن فریمورک
framework = GravityFramework(
    project_path=Path("./my-project"),
    ai_assist=True  # AI هم فعاله
)

# کشف میکروسرویس‌ها
print("📍 Discovering services...")
framework.discover_services("https://github.com/myorg/auth-service")
framework.discover_services("https://github.com/myorg/user-service")
framework.discover_services("https://github.com/myorg/payment-service")

# راهنمای تعاملی
print("\n🚀 Starting interactive setup...")
summary = framework.interactive_setup()

# بررسی نتیجه
if summary['success_rate'] == 100:
    print("🎉 All services ready!")
    
    # استارت سرویس‌ها
    framework.start()
else:
    print(f"⚠️ Setup {summary['success_rate']:.0f}% successful")
    print(f"Failed steps: {summary['failed']}")
```

## خروجی خلاصه

در آخر، یه خلاصه کامل میده:

```python
summary = {
    'total_steps': 4,
    'completed': 4,
    'failed': 0,
    'success_rate': 100.0
}
```

## مزایا

✅ **صفر سردرگمی** - میگه چیکار کنی  
✅ **خودکار** - خودش دستورات رو اجرا میکنه  
✅ **هوشمند** - README رو می‌خونه  
✅ **تعاملی** - نمایش زنده پیشرفت  
✅ **ایمن** - اگه خطا بود، میپرسه  
✅ **شفاف** - همه چیز رو نشون میده  

## CLI

از طریق خط فرمان هم میتونی استفاده کنی:

```bash
# کشف سرویس‌ها
gravity discover https://github.com/org/auth-service
gravity discover https://github.com/org/user-service

# شروع راهنمای تعاملی
gravity setup --interactive

# یا به صورت خودکار همه چیز
gravity auto-setup
```

## مقایسه

### قبل (دستی):
```bash
# خودت باید:
cd services/auth-service
pip install -r requirements.txt
createdb auth_db
export DATABASE_URL=postgresql://...
python main.py &

cd ../user-service
pip install -r requirements.txt
createdb user_db
export DATABASE_URL=postgresql://...
python main.py &

# ... برای هر سرویس
```

### حالا (خودکار):
```python
framework.interactive_setup()
# همین!
```

## تنظیمات

میتونی رفتار رو تنظیم کنی:

```python
# غیرفعال کردن اجرای خودکار
guide = InteractiveGuide(services)
guide.auto_execute = False  # همه چیز رو نشون میده ولی اجرا نمیکنه

# یا فقط نمایش
guide.show_only = True  # فقط نشون میده چیکار باید کنی
```

---

**نکته**: این ویژگی با AI هم کار میکنه! اگه AI فعال باشه، پیشنهادات هوشمندانه‌تری میده:
- بهترین ترتیب نصب
- بهینه‌سازی‌های ممکن
- هشدارهای امنیتی
- پیشنهادات معماری
