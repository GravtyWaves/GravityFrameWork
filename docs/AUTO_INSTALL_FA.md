# 🚀 نصب خودکار هوش مصنوعی

## خبر خوب!

**دیگه نیازی نیست هیچ چیزی نصب کنی!** 🎉

فریمورک خودش همه چیز رو نصب میکنه:
- ✅ Ollama
- ✅ مدل AI
- ✅ راه‌اندازی سرویس
- ✅ آماده استفاده!

## استفاده (خیلی ساده!)

```python
from gravity_framework import GravityFramework

# همین! کافیه فریمورک رو بسازی
framework = GravityFramework(ai_assist=True)

# بار اول: AI خودش نصب میشه (2-5 دقیقه، فقط یکبار)
# بارهای بعد: فوری آماده میشه!
```

## اولین بار چی میشه؟

وقتی اولین بار فریمورک رو میسازی:

```
🤖 Ollama not found. Installing automatically...
⏳ First-time setup (takes 2-5 minutes, only once)...
📥 Downloading Ollama...
🚀 Installing Ollama...
✓ Ollama installed successfully
📥 Downloading AI model: llama3.2:3b...
⏳ This may take a few minutes (first time only)...
✓ Model llama3.2:3b downloaded successfully
🎉 AI setup complete!
✅ AI Assistant enabled - Ollama (llama3.2:3b) ready
```

## دفعه‌های بعد چی میشه؟

```
✓ Ollama is already running
🤖 AI Assistant enabled - Ollama (llama3.2:3b) ready
```

**فوری!** چون همه چیز نصب شده.

## مثال کامل

```python
from gravity_framework import GravityFramework

# ساختن فریمورک (AI خودکار نصب میشه)
framework = GravityFramework(ai_assist=True)

# چک کنیم AI فعاله؟
if framework.ai.enabled:
    print("🤖 AI آماده!")
    
    # حالا میتونی استفاده کنی:
    
    # تحلیل میکروسرویس‌ها
    analysis = framework.ai_analyze()
    
    # پیشنهاد اتصالات (puzzle-solving)
    connections = framework.ai_suggest_connections()
    
    # تشخیص خطا
    diagnosis = framework.ai_diagnose("Service timeout")
    
    # بهینه‌سازی deployment
    optimization = framework.ai_optimize_deployment()
```

## اگه نخوای خودکار نصب کنه؟

```python
# غیرفعال کردن نصب خودکار
framework = GravityFramework(
    ai_assist=True,
    auto_install_ai=False  # فقط چک میکنه، نصب نمیکنه
)
```

## چیزایی که دانلود میشه

### بار اول (یکبار):
1. **Ollama** (~200MB) - نرم‌افزار AI
2. **llama3.2:3b** (~2GB) - مدل AI سبک و سریع

### مجموع: حدود 2.2 گیگ

**فقط یکبار!** بعدش دیگه چیزی دانلود نمیشه.

## مدل‌های مختلف

```python
# مدل سبک و سریع (پیش‌فرض - 2GB)
framework = GravityFramework(
    ai_assist=True,
    ollama_model="llama3.2:3b"
)

# مدل بهتر (7GB)
framework = GravityFramework(
    ai_assist=True,
    ollama_model="llama3.1:8b"
)

# مدل تخصصی کد (5GB)
framework = GravityFramework(
    ai_assist=True,
    ollama_model="deepseek-coder:6.7b"
)
```

## سوالات متداول

**Q: اولین بار چقدر طول میکشه؟**  
A: 2-5 دقیقه (بسته به سرعت اینترنت). بعدش فوری!

**Q: هر بار که برنامه رو اجرا میکنم، دوباره دانلود میشه؟**  
A: نه! فقط یکبار. بعدش همیشه آماده‌ست.

**Q: اگه اینترنت نداشته باشم چی؟**  
A: بعد از اولین نصب، دیگه اینترنت نمیخواد!

**Q: روی هر سیستم عاملی کار میکنه؟**  
A: آره! Windows, macOS, Linux

**Q: اگه نصب خودکار کار نکرد چی؟**  
A: میتونی دستی نصب کنی: https://ollama.com/download

**Q: چقدر حافظه RAM میخواد؟**  
A: با llama3.2:3b فقط 2-4 گیگ RAM

## مزایا

✅ **صفر تنظیمات** - فقط کد بنویس، بقیه خودکار  
✅ **رایگان** - هیچ هزینه‌ای نداره  
✅ **سریع** - بعد از اولین نصب، فوری  
✅ **آفلاین** - بعد از دانلود، اینترنت نمیخواد  
✅ **آسون** - یه خط کد کافیه!  

## مثال اجرا

```bash
# فایل بساز
cat > test_ai.py << 'EOF'
from gravity_framework import GravityFramework

framework = GravityFramework(ai_assist=True)

if framework.ai.enabled:
    print("🎉 AI کار میکنه!")
else:
    print("⚠️ AI فعال نیست")
EOF

# اجرا کن
python test_ai.py

# بار اول: نصب میشه (2-5 دقیقه)
# بار دوم: فوری!
```

---

**نکته مهم**: همه چیز روی کامپیوتر خودت نصب میشه، نه روی سرور. پس:
- 🔒 اطلاعاتت محفوظه (Privacy)
- ⚡ سریعتره (Local)
- 💰 رایگانه (No API costs)
- 🌐 آفلاین کار میکنه (No internet needed)
