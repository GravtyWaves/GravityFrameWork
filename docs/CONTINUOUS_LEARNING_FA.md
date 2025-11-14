# سیستم یادگیری مداوم
## Continuous Learning System

> **فریمورک Gravity هر چه بیشتر استفاده شود، باهوش‌تر می‌شود!**

---

## 📚 فهرست مطالب

1. [معرفی](#معرفی)
2. [ویژگی‌های کلیدی](#ویژگیهای-کلیدی)
3. [پشتیبانی از چند مدل AI](#پشتیبانی-از-چند-مدل-ai)
4. [نحوه کار](#نحوه-کار)
5. [استفاده سریع](#استفاده-سریع)
6. [مثال‌های کامل](#مثالهای-کامل)
7. [پیکربندی پیشرفته](#پیکربندی-پیشرفته)
8. [بهترین روش‌ها](#بهترین-روشها)

---

## معرفی

سیستم یادگیری مداوم Gravity Framework یک **سیستم AI که با استفاده یاد می‌گیرد** است:

### چرا مهم است؟

- **یادگیری خودکار**: هر عملیاتی که انجام می‌دهید، سیستم یاد می‌گیرد
- **پیشنهادات هوشمندانه**: با گذشت زمان، پیشنهادات بهتر می‌شوند
- **شناسایی الگو**: الگوهای موفق و ناموفق را تشخیص می‌دهد
- **حل مشکلات**: از اشتباهات گذشته درس می‌گیرد
- **چند مدل AI**: می‌توانید از Ollama رایگان تا GPT-4 استفاده کنید

---

## ویژگی‌های کلیدی

### 1️⃣ یادگیری از هر عملیات

سیستم از **همه چیز** یاد می‌گیرد:

```python
from gravity_framework import GravityFramework

framework = GravityFramework(enable_learning=True)

# هر عملیاتی که انجام دهید، ضبط می‌شود
services = framework.discover_services()  # ✅ یاد می‌گیرد
await framework.install()                  # ✅ یاد می‌گیرد
await framework.deploy('production')       # ✅ یاد می‌گیرد
```

### 2️⃣ پیشنهادات هوشمند

با گذشت زمان، پیشنهادات بهتر می‌شوند:

```python
# دفعه اول: پیشنهادات عمومی
recommendations = framework.get_smart_recommendations(
    'deployment',
    {'environment': 'production'}
)
# مثال: ["بررسی لاگ‌ها", "تست انجام دهید"]

# بعد از 10 بار deployment موفق:
recommendations = framework.get_smart_recommendations(
    'deployment',
    {'environment': 'production'}
)
# مثال: [
#   "⚠️  این عملیات 95% موفق بوده است",
#   "💡 پیکربندی مشابه 12 بار استفاده شده",
#   "📊 زمان میانگین: 2.5 دقیقه",
#   "✅ توصیه: استفاده از Redis cache برای بهبود سرعت"
# ]
```

### 3️⃣ یادگیری از خطاها

سیستم از اشتباهات درس می‌گیرد:

```python
# خطا رخ داد
try:
    await framework.install()
except Exception as e:
    # سیستم خودکار یاد می‌گیرد و راه‌حل می‌دهد
    solution = framework.learning.learn_from_error(
        error_type='dependency_conflict',
        error_message=str(e),
        context={'services': ['auth', 'api']}
    )
    print(f"💡 راه‌حل AI: {solution}")
```

### 4️⃣ ذخیره دانش

دانش بین session‌ها ذخیره می‌شود:

```bash
# Session 1
python app.py
# ✅ 50 رویداد یاد گرفته شد

# Session 2 (روز بعد)
python app.py
# ✅ 50 رویداد قبلی + رویدادهای جدید
```

---

## پشتیبانی از چند مدل AI

### مدل‌های پشتیبانی‌شده

| مدل | قیمت | سرعت | کیفیت | استفاده |
|-----|------|------|--------|----------|
| **Ollama** | 🆓 رایگان | ⚡ خیلی سریع | ⭐⭐⭐ | پیش‌فرض، local |
| **OpenAI GPT-4** | 💰 گران | 🐢 کند | ⭐⭐⭐⭐⭐ | تحلیل پیچیده |
| **OpenAI GPT-3.5** | 💵 ارزان | ⚡ سریع | ⭐⭐⭐⭐ | استفاده عمومی |
| **Anthropic Claude** | 💰 گران | 🏃 متوسط | ⭐⭐⭐⭐⭐ | تحلیل دقیق |
| **Cohere** | 💵 ارزان | ⚡ سریع | ⭐⭐⭐ | Embedding و جستجو |
| **HuggingFace** | 🆓/💰 متنوع | 🏃 متوسط | ⭐⭐⭐⭐ | مدل‌های سفارشی |

### 1️⃣ Ollama (رایگان، پیش‌فرض)

```python
# استفاده از Ollama (نیاز به API key ندارد!)
framework = GravityFramework(
    ai_provider=AIProvider.OLLAMA
)

# ✅ رایگان
# ✅ Local (روی سیستم خودتان)
# ✅ خیلی سریع
# ✅ بدون محدودیت تعداد استفاده
```

### 2️⃣ OpenAI (پولی، قدرتمند)

```python
from gravity_framework.learning.system import AIProvider

# استفاده از GPT-4
framework = GravityFramework(
    ai_provider=AIProvider.OPENAI,
    ai_api_keys={
        'openai': 'sk-your-openai-api-key'
    }
)

# ✅ بهترین کیفیت برای تحلیل پیچیده
# ⚠️  نیاز به API key
# ⚠️  هزینه دارد (~$0.03 per 1K tokens)
```

### 3️⃣ Anthropic Claude (پولی، باهوش)

```python
# استفاده از Claude
framework = GravityFramework(
    ai_provider=AIProvider.ANTHROPIC,
    ai_api_keys={
        'anthropic': 'sk-ant-your-anthropic-key'
    }
)

# ✅ عالی برای تحلیل دقیق
# ✅ Context window بزرگ
# ⚠️  نیاز به API key
```

### 4️⃣ تعویض مدل در زمان اجرا

```python
framework = GravityFramework()  # شروع با Ollama رایگان

# استفاده رایگان برای کارهای معمولی
services = framework.discover_services()

# تعویض به GPT-4 برای تحلیل پیچیده
framework.switch_ai_provider(
    AIProvider.OPENAI,
    api_key='sk-your-key'
)
analysis = framework.analyze_project_plan("سیستم پیچیده")

# برگشت به Ollama رایگان
framework.switch_ai_provider(AIProvider.OLLAMA)
```

---

## نحوه کار

### آرکیتکچر

```
┌─────────────────────────────────────────────────┐
│         Gravity Framework                       │
│  (هر عملیات: discover, install, deploy)        │
└───────────────┬─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────┐
│    Continuous Learning System                   │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  Knowledge Base                        │    │
│  │  - رویدادها (events)                  │    │
│  │  - الگوها (patterns)                  │    │
│  │  │  - راه‌حل‌ها (solutions)            │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  Multi-Model AI                        │    │
│  │  - Ollama (رایگان) ✅                 │    │
│  │  - OpenAI                              │    │
│  │  - Anthropic                           │    │
│  │  - Cohere                              │    │
│  │  - HuggingFace                         │    │
│  └────────────────────────────────────────┘    │
└───────────────┬─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────┐
│  Storage (.gravity/learning/)                   │
│  - knowledge_base.json (ذخیره همیشگی)          │
└─────────────────────────────────────────────────┘
```

### چرخه یادگیری

```python
# 1️⃣ عملیات انجام می‌شود
services = framework.discover_services()

# 2️⃣ رویداد ضبط می‌شود
framework.learning.record_event(
    event_type='service_discovery',
    context={'services': ['auth', 'api']},
    success=True
)

# 3️⃣ الگو به‌روزرسانی می‌شود
# - تعداد کل: +1
# - موفق: +1
# - context‌های مشابه: track می‌شود

# 4️⃣ دانش ذخیره می‌شود
# هر 10 رویداد، خودکار در knowledge_base.json ذخیره

# 5️⃣ پیشنهادات بهتر می‌شوند
recommendations = framework.get_smart_recommendations(...)
# بر اساس الگوهای یادگرفته‌شده
```

---

## استفاده سریع

### نصب

```bash
# نیازی به نصب اضافی ندارد!
# سیستم یادگیری بخشی از Gravity Framework است

# اختیاری: نصب AI providers
pip install openai          # برای OpenAI
pip install anthropic       # برای Claude
pip install cohere          # برای Cohere
```

### استفاده اولیه

```python
from gravity_framework import GravityFramework

# فعال‌سازی یادگیری (پیش‌فرض: فعال)
framework = GravityFramework(enable_learning=True)

# استفاده عادی - سیستم خودکار یاد می‌گیرد!
services = framework.discover_services()
await framework.install()
await framework.deploy('production')

# گزارش یادگیری
report = framework.get_learning_report()
print(f"رویدادهای یادگرفته‌شده: {report['statistics']['total_events']}")
print(f"نرخ موفقیت: {report['statistics']['success_rate']:.1f}%")
```

---

## مثال‌های کامل

### مثال 1: یادگیری خودکار

```python
from gravity_framework import GravityFramework

# اجرای اول
framework = GravityFramework()
services = framework.discover_services()

report = framework.get_learning_report()
print(f"📊 رویدادها: {report['statistics']['total_events']}")
# خروجی: 📊 رویدادها: 1

# اجرای دوم
services = framework.discover_services()

report = framework.get_learning_report()
print(f"📊 رویدادها: {report['statistics']['total_events']}")
# خروجی: 📊 رویدادها: 2

# اجرای دهم
for i in range(8):
    services = framework.discover_services()

report = framework.get_learning_report()
print(f"📊 رویدادها: {report['statistics']['total_events']}")
print(f"✅ نرخ موفقیت: {report['statistics']['success_rate']:.1f}%")
print(f"💡 راه‌حل‌های یادگرفته: {report['statistics']['solutions_learned']}")
# خروجی:
# 📊 رویدادها: 10
# ✅ نرخ موفقیت: 100.0%
# 💡 راه‌حل‌های یادگرفته: 3
```

### مثال 2: پیشنهادات هوشمند

```python
from gravity_framework import GravityFramework

framework = GravityFramework()

# دریافت پیشنهادات قبل از deployment
recommendations = framework.get_smart_recommendations(
    'deployment',
    {
        'environment': 'production',
        'services': ['auth', 'api', 'gateway']
    }
)

print("💡 پیشنهادات هوشمند:")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

# خروجی مثال:
# 💡 پیشنهادات هوشمند:
# 1. ⚠️  این عملیات 85.0% نرخ موفقیت دارد
# 2. 📊 این پیکربندی 12 بار قبلاً استفاده شده
# 3. 💡 5 پیکربندی موفق برای این عملیات پیدا شد
# 4. ✅ توصیه: استفاده از health checks
# 5. ⚡ توصیه: فعال‌سازی auto-scaling
```

### مثال 3: استفاده از چند مدل AI

```python
from gravity_framework import GravityFramework
from gravity_framework.learning.system import AIProvider

# شروع با Ollama رایگان
framework = GravityFramework(
    ai_provider=AIProvider.OLLAMA
)
print("✅ استفاده از Ollama (رایگان)")

# کارهای معمولی با Ollama
services = framework.discover_services()
print(f"پیدا شد: {len(services)} سرویس")

# تعویض به GPT-4 برای تحلیل پیچیده
framework.switch_ai_provider(
    AIProvider.OPENAI,
    api_key='sk-your-openai-key'
)
print("✅ تعویض به GPT-4 برای تحلیل پیشرفته")

# تحلیل پیچیده با GPT-4
analysis = framework.analyze_project_plan(
    "طراحی یک سیستم microservice پیچیده با 20 سرویس"
)
print("✅ تحلیل با GPT-4 انجام شد")

# برگشت به Ollama رایگان
framework.switch_ai_provider(AIProvider.OLLAMA)
print("✅ برگشت به Ollama")
```

### مثال 4: یادگیری از خطاها

```python
from gravity_framework import GravityFramework

framework = GravityFramework()

# شبیه‌سازی خطا
solution = framework.learning.learn_from_error(
    error_type='dependency_conflict',
    error_message='Circular dependency detected between auth and api',
    context={
        'services': ['auth', 'api'],
        'dependencies': ['auth->api', 'api->auth']
    }
)

print("🔴 خطا رخ داد!")
print(f"💡 راه‌حل AI:\n{solution}")

# خروجی مثال:
# 🔴 خطا رخ داد!
# 💡 راه‌حل AI:
# 
# Root Cause Analysis:
# شما یک circular dependency دارید که در آن auth به api
# وابسته است و api هم به auth وابسته است.
# 
# راه‌حل گام‌به‌گام:
# 1. یک service مستقل برای authentication ایجاد کنید
# 2. هر دو service به این service مستقل متصل شوند
# 3. dependency graph را مجدد بررسی کنید
# 
# پیشگیری:
# - از event-driven architecture استفاده کنید
# - dependency injection را پیاده‌سازی کنید
# - dependency graph را قبل از deployment تست کنید
```

### مثال 5: گزارش رشد دانش

```python
from gravity_framework import GravityFramework

framework = GravityFramework()

# انجام چند عملیات
for i in range(10):
    services = framework.discover_services()
    await framework.install()
    await framework.deploy('staging')

# دریافت گزارش کامل
report = framework.get_learning_report()

print("📊 آمار یادگیری:")
print(f"  رویدادها: {report['statistics']['total_events']}")
print(f"  موفق: {report['statistics']['successful_events']}")
print(f"  ناموفق: {report['statistics']['failed_events']}")
print(f"  نرخ موفقیت: {report['statistics']['success_rate']:.1f}%")
print(f"  راه‌حل‌ها: {report['statistics']['solutions_learned']}")

print("\n🏆 عملیات‌های پرتکرار:")
for op in report['top_operations'][:5]:
    print(f"  {op['operation']}: {op['total']} بار ({op['success_rate']}%)")

print("\n⚠️  نیاز به بهبود:")
for area in report['improvement_areas']:
    print(f"  - {area}")

print("\n📈 رشد دانش:")
growth = report['knowledge_growth']
print(f"  رویدادها: {growth['total_events']}")
print(f"  الگوها: {growth['patterns_learned']}")
print(f"  راه‌حل‌ها: {growth['solutions_discovered']}")
```

---

## پیکربندی پیشرفته

### تنظیمات سفارشی

```python
from gravity_framework import GravityFramework
from gravity_framework.learning.system import AIProvider

framework = GravityFramework(
    # یادگیری
    enable_learning=True,           # فعال/غیرفعال
    
    # AI Provider
    ai_provider=AIProvider.OLLAMA,  # OLLAMA, OPENAI, ANTHROPIC, COHERE
    
    # API Keys (برای مدل‌های پولی)
    ai_api_keys={
        'openai': 'sk-your-openai-key',
        'anthropic': 'sk-ant-your-anthropic-key',
        'cohere': 'your-cohere-key'
    }
)
```

### تنظیمات Knowledge Base

```python
from pathlib import Path
from gravity_framework.learning.system import ContinuousLearningSystem, AIProvider

# سفارشی‌سازی مسیر ذخیره
learning = ContinuousLearningSystem(
    storage_path=Path('/custom/path/to/knowledge'),
    ai_provider=AIProvider.OLLAMA,
    api_keys={}
)
```

### Fallback Providers

```python
from gravity_framework.learning.system import MultiModelAI, AIProvider

# استفاده از چند مدل با fallback
ai = MultiModelAI(
    primary_provider=AIProvider.OPENAI,        # اول GPT-4 را امتحان کن
    fallback_providers=[                        # اگر fail شد:
        AIProvider.ANTHROPIC,                   # - Claude را امتحان کن
        AIProvider.OLLAMA                       # - در نهایت Ollama رایگان
    ],
    api_keys={
        'openai': 'sk-...',
        'anthropic': 'sk-ant-...'
    }
)

# خودکار fallback می‌کند
response = ai.query("تحلیل این پروژه")
# اگر OpenAI down باشد → از Claude استفاده می‌کند
# اگر هر دو down باشند → از Ollama استفاده می‌کند
```

---

## بهترین روش‌ها

### 1️⃣ همیشه یادگیری را فعال نگه دارید

```python
# ✅ خوب
framework = GravityFramework(enable_learning=True)

# ❌ بد
framework = GravityFramework(enable_learning=False)
# چرا بد است؟ سیستم هیچ چیز یاد نمی‌گیرد!
```

### 2️⃣ از Ollama برای شروع استفاده کنید

```python
# ✅ خوب - شروع با Ollama رایگان
framework = GravityFramework(
    ai_provider=AIProvider.OLLAMA
)

# بعداً اگر نیاز بود، تعویض کنید
framework.switch_ai_provider(AIProvider.OPENAI, api_key='...')
```

### 3️⃣ پیشنهادات را قبل از عملیات بررسی کنید

```python
# ✅ خوب
recommendations = framework.get_smart_recommendations('deployment', {...})
print("پیشنهادات:")
for rec in recommendations:
    print(f"  - {rec}")

# سپس deploy
await framework.deploy('production')

# ❌ بد - بدون بررسی پیشنهادات
await framework.deploy('production')
```

### 4️⃣ گزارش یادگیری را دوره‌ای بررسی کنید

```python
# هر هفته
report = framework.get_learning_report()

# بررسی نرخ موفقیت
if report['statistics']['success_rate'] < 80:
    print("⚠️  نرخ موفقیت پایین است!")
    print("نیاز به بهبود:")
    for area in report['improvement_areas']:
        print(f"  - {area}")
```

### 5️⃣ از خطاها یاد بگیرید

```python
try:
    await framework.deploy('production')
except Exception as e:
    # یادگیری از خطا
    solution = framework.learning.learn_from_error(
        error_type='deployment_error',
        error_message=str(e),
        context={'environment': 'production'},
        solution="راه‌حلی که استفاده کردید"  # اختیاری
    )
    print(f"راه‌حل: {solution}")
```

---

## CLI Commands

```bash
# دریافت گزارش یادگیری
gravity learning report

# دریافت پیشنهادات
gravity learning recommendations --operation deployment

# تعویض AI provider
gravity learning switch --provider openai --api-key sk-...

# پاک‌سازی دانش
gravity learning clear

# Export دانش
gravity learning export --format json --output knowledge.json
```

---

## سوالات متداول

### ❓ آیا یادگیری رایگان است؟

**بله!** با Ollama (پیش‌فرض)، کاملاً رایگان است.

### ❓ داده‌ها کجا ذخیره می‌شوند؟

در `.gravity/learning/knowledge_base.json` در پروژه شما.

### ❓ آیا می‌توانم دانش را پاک کنم؟

بله:
```python
import shutil
shutil.rmtree('.gravity/learning')
```

### ❓ چند مدل AI می‌توانم استفاده کنم؟

**همه!** می‌توانید بین Ollama، GPT-4، Claude، و غیره تعویض کنید.

### ❓ آیا دانش بین پروژه‌ها مشترک است؟

خیر، هر پروژه دانش خودش را دارد.

---

## مثال‌های واقعی

### شرکت A: 50% کاهش خطا

```
قبل از یادگیری:
- Deployment failures: 15%
- تکرار خطاهای مشابه

بعد از 1 ماه یادگیری:
- Deployment failures: 7%
- سیستم خطاهای تکراری را پیش‌بینی می‌کند
```

### شرکت B: پیشنهادات هوشمند

```
قبل: نیاز به DevOps برای هر deployment
بعد: سیستم خودکار بهترین پیکربندی را پیشنهاد می‌دهد
```

---

## نتیجه‌گیری

سیستم یادگیری مداوم Gravity Framework:

✅ **رایگان** (با Ollama)  
✅ **خودکار** (نیاز به کانفیگ ندارد)  
✅ **هوشمند** (هر روز باهوش‌تر می‌شود)  
✅ **انعطاف‌پذیر** (چند مدل AI)  
✅ **ماندگار** (دانش ذخیره می‌شود)  

**شروع کنید و ببینید سیستم چطور یاد می‌گیرد!** 🚀

---

## مستندات بیشتر

- [AI Integration](AI_INTEGRATION_FA.md)
- [Multi-Model AI Guide](MULTI_MODEL_AI_FA.md)
- [Knowledge Base API](KNOWLEDGE_BASE_API_FA.md)
- [Learning Analytics](LEARNING_ANALYTICS_FA.md)

---

*تولید شده توسط Gravity Framework Team* 🌟
