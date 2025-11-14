# مدیریت هوشمند کامیت‌ها

## معرفی

این ماژول **مدیریت هوشمند کامیت‌ها** را فراهم می‌کند که به صورت خودکار:

1. ✅ فایل‌های تغییر یافته را **دسته‌بندی** می‌کند
2. ✅ کامیت‌های **منظم و منطقی** ایجاد می‌کند
3. ✅ پیام‌های کامیت را **با AI تولید** می‌کند
4. ✅ تمام **استانداردهای TEAM_PROMPT.md** را رعایت می‌کند
5. ✅ به صورت خودکار کامیت‌ها را **پوش** می‌کند

**مسئول این بخش:**
- Dr. Chen Wei - طراح تجربه توسعه‌دهنده
- تخصص: اتوماسیون Git workflow

---

## ویژگی‌های کلیدی

### 1. دسته‌بندی خودکار فایل‌ها

سیستم فایل‌ها را به دسته‌های زیر تقسیم می‌کند:

```python
دسته‌بندی‌ها:
├── features-ai          # ویژگی‌های AI
├── features-git         # یکپارچه‌سازی Git
├── features-devops      # اتوماسیون DevOps
├── features-database    # پایگاه داده
├── features-api         # API endpoints
├── features-services    # سرویس‌ها
├── tests               # تست‌ها
├── docs                # مستندات
├── docs-readme         # README
├── config              # تنظیمات
├── infrastructure-docker    # Docker
├── infrastructure-cicd      # CI/CD
└── infrastructure-deployment # استقرار
```

### 2. تولید خودکار پیام‌های کامیت

با استفاده از AI، پیام‌های کامیت را بر اساس **Conventional Commits** تولید می‌کند:

```
feat(ai): add intelligent team generation
feat(git): add smart commit automation
fix(database): resolve connection pooling issue
docs(readme): update installation guide
test(core): add framework integration tests
```

### 3. کامیت خودکار (100 فایل)

طبق `TEAM_PROMPT.md`: "هر 100 تغییر فایل، کامیت و پوش کن"

```python
# به صورت خودکار بررسی می‌کند
framework.check_auto_commit()
# اگر 100+ فایل تغییر کرده باشد → کامیت و پوش خودکار!
```

---

## نحوه استفاده

### مثال 1: تحلیل تغییرات

```python
from gravity_framework import GravityFramework

framework = GravityFramework()

# تحلیل فایل‌های تغییر یافته
analysis = framework.analyze_commits()

print(analysis['summary'])
# خروجی:
# Changes Summary:
# 
# • features-git: 2 files
# • docs: 1 files
# • tests: 3 files
# 
# Total: 6 files

# توصیه‌ها برای کامیت
for rec in analysis['recommendations']:
    print(rec['suggested_message'])
# خروجی:
# feat(git): add git integration features
# docs(docs): add documentation updates
# test(tests): add test coverage and validation
```

### مثال 2: ساخت کامیت‌های منظم

```python
# ساخت کامیت‌های دسته‌بندی شده (بدون پوش)
result = framework.organize_and_commit(
    auto_generate_messages=True,  # استفاده از AI برای پیام‌ها
    push=False                     # بدون پوش
)

print(f"تعداد کامیت‌ها: {result['total_commits']}")

for commit in result['commits']:
    print(f"{commit['hash'][:8]} - {commit['message']}")
# خروجی:
# a1b2c3d4 - feat(git): add smart commit automation
# e5f6g7h8 - docs(readme): update usage examples
# i9j0k1l2 - test(git): add commit manager tests
```

### مثال 3: کامیت و پوش هوشمند (یک دستور!)

```python
# تمام کار با یک دستور!
result = framework.smart_commit_push()

# این دستور:
# 1. همه فایل‌ها را تحلیل می‌کند
# 2. دسته‌بندی منطقی انجام می‌دهد
# 3. کامیت‌های جداگانه می‌سازد
# 4. به remote پوش می‌کند

print(result['summary'])
# خروجی:
# WORKFLOW SUMMARY
# ================
# Files analyzed: 15
# Commits created: 4
# Commits failed: 0
# Push status: ✅ Success
# 
# Commits created:
#   • a1b2c3d4 - feat(ai): add team generation
#   • e5f6g7h8 - feat(git): add commit manager
#   • i9j0k1l2 - docs(docs): add Persian guides
#   • m3n4o5p6 - test(tests): add integration tests
```

### مثال 4: کامیت خودکار (100 فایل)

```python
# بررسی آستانه 100 فایل
result = framework.check_auto_commit()

if result:
    print("کامیت خودکار انجام شد!")
    print(f"{result['summary']}")
else:
    print("هنوز به آستانه نرسیده")
```

---

## Workflow کامل توسعه

```python
from gravity_framework import GravityFramework

framework = GravityFramework()

# مرحله 1: تغییرات خود را ایجاد کنید
# ... کد می‌نویسید ...

# مرحله 2: اعتبارسنجی استانداردها
validation = framework.validate_standards()

if not validation['valid']:
    # اصلاح خودکار مشکلات
    framework.auto_fix_standards()

# مرحله 3: کامیت و پوش هوشمند
framework.smart_commit_push()

# ✅ تمام! همه چیز کامیت و پوش شد!
```

---

## دسته‌بندی فایل‌ها

### فایل‌های Feature

```python
دسته: features-ai
فایل‌ها:
  - gravity_framework/ai/team_generator.py
  - gravity_framework/ai/assistant.py
نوع کامیت: feat(ai)
پیام: "add AI-powered team generation"

دسته: features-git
فایل‌ها:
  - gravity_framework/git/integration.py
  - gravity_framework/git/commit_manager.py
نوع کامیت: feat(git)
پیام: "add intelligent Git integration"
```

### فایل‌های تست

```python
دسته: tests
فایل‌ها:
  - tests/test_git.py
  - tests/test_commit_manager.py
نوع کامیت: test(tests)
پیام: "add commit management tests"
```

### فایل‌های مستندات

```python
دسته: docs
فایل‌ها:
  - docs/COMMIT_MANAGEMENT_FA.md
  - docs/GIT_INTEGRATION_FA.md
نوع کامیت: docs(docs)
پیام: "add Persian documentation"

دسته: docs-readme
فایل‌ها:
  - README.md
  - QUICKSTART.md
نوع کامیت: docs(readme)
پیام: "update README and guides"
```

### فایل‌های Infrastructure

```python
دسته: infrastructure-docker
فایل‌ها:
  - Dockerfile
  - docker-compose.yml
نوع کامیت: chore(docker)
پیام: "update Docker configuration"

دسته: infrastructure-cicd
فایل‌ها:
  - .github/workflows/test.yml
  - .github/workflows/deploy.yml
نوع کامیت: chore(cicd)
پیام: "update CI/CD pipeline"
```

---

## Conventional Commits

تمام پیام‌های کامیت از فرمت **Conventional Commits** پیروی می‌کنند:

### فرمت:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### انواع (Types):

- `feat`: ویژگی جدید
- `fix`: رفع باگ
- `docs`: تغییرات مستندات
- `test`: اضافه کردن تست‌ها
- `refactor`: بازسازی کد
- `chore`: کارهای نگهداری
- `perf`: بهبود عملکرد
- `ci`: تغییرات CI/CD

### محدوده‌ها (Scopes):

- `ai`: هوش مصنوعی
- `git`: یکپارچه‌سازی Git
- `devops`: اتوماسیون DevOps
- `database`: پایگاه داده
- `api`: API
- `core`: هسته فریمورک
- `tests`: تست‌ها
- `docs`: مستندات
- `config`: تنظیمات

### مثال‌ها:

```
✅ خوب:
feat(ai): add intelligent team generation
fix(database): resolve connection pool leak
docs(readme): update installation instructions
test(git): add commit validation tests

❌ بد:
Added new feature
Fixed bug
Update docs
```

---

## استانداردهای TEAM_PROMPT.md

تمام کامیت‌ها این استانداردها را رعایت می‌کنند:

### 1. فقط انگلیسی

```python
✅ خوب: feat(ai): add team generation
❌ بد: feat(ai): اضافه کردن تیم
```

### 2. Type Hints

```python
# قبل از کامیت، بررسی می‌شود:
✅ def process_data(items: List[str]) -> Dict[str, Any]:
❌ def process_data(items):  # بدون type hints
```

### 3. Docstrings

```python
# قبل از کامیت، بررسی می‌شود:
✅ def calculate_total(items: List[float]) -> float:
    """Calculate total sum of items."""
    return sum(items)

❌ def calculate_total(items: List[float]) -> float:
    return sum(items)  # بدون docstring
```

### 4. بدون Secrets

```python
# قبل از کامیت، بررسی می‌شود:
❌ password = "my_secret_123"  # هاردکد شده!
✅ password = os.getenv("PASSWORD")  # از متغیر محیط
```

### 5. Test Coverage ≥ 95%

```python
# قبل از کامیت، تست‌ها اجرا می‌شوند:
pytest --cov=gravity_framework --cov-report=term
# Coverage باید ≥ 95% باشد
```

---

## Pre-Commit Checks

قبل از هر کامیت، این بررسی‌ها انجام می‌شود:

```python
بررسی‌های Pre-commit:
├── ✅ Black formatting (قالب‌بندی کد)
├── ✅ isort (مرتب‌سازی imports)
├── ✅ mypy (بررسی type hints)
├── ✅ pytest (اجرای تست‌ها)
├── ✅ coverage (پوشش تست ≥ 95%)
├── ✅ bandit (بررسی امنیتی)
└── ✅ secrets (تشخیص hardcoded secrets)
```

اگر هر کدام fail شود:
1. سیستم **سعی می‌کند خودکار رفع کند**
2. اگر نتوانست → کامیت **لغو** می‌شود
3. شما مشکل را **رفع می‌کنید**
4. دوباره **کامیت می‌کنید**

---

## Auto-Fix

سیستم می‌تواند خودکار این مشکلات را رفع کند:

### 1. قالب‌بندی کد

```python
# قبل:
def  calculate(x,y)  :
    return x+y

# بعد (Black):
def calculate(x, y):
    return x + y
```

### 2. مرتب‌سازی Imports

```python
# قبل:
from pathlib import Path
import os
import sys
from typing import List

# بعد (isort):
import os
import sys
from pathlib import Path
from typing import List
```

### 3. اضافه کردن Type Hints

```python
# قبل:
def process_data(items):
    return [x * 2 for x in items]

# بعد (AI):
def process_data(items: List[int]) -> List[int]:
    return [x * 2 for x in items]
```

### 4. تولید Docstrings

```python
# قبل:
def calculate_total(items: List[float]) -> float:
    return sum(items)

# بعد (AI):
def calculate_total(items: List[float]) -> float:
    """
    Calculate total sum of items.
    
    Args:
        items: List of float values
        
    Returns:
        Sum of all items
    """
    return sum(items)
```

---

## استفاده از CLI

```bash
# تحلیل تغییرات
$ gravity commit analyze

# ساخت کامیت‌های منظم
$ gravity commit organize

# کامیت و پوش هوشمند
$ gravity commit push

# بررسی کامیت خودکار
$ gravity commit check

# اجبار به کامیت
$ gravity commit force
```

---

## API Reference

### `analyze_commits()`

تحلیل فایل‌های تغییر یافته.

```python
framework = GravityFramework()
analysis = framework.analyze_commits()

# خروجی:
{
    'groups': {
        'features-git': ['file1.py', 'file2.py'],
        'tests': ['test_file.py']
    },
    'summary': '...',
    'recommendations': [...]
}
```

### `organize_and_commit()`

ساخت کامیت‌های منظم.

```python
result = framework.organize_and_commit(
    auto_generate_messages=True,  # استفاده از AI
    push=False                     # بدون پوش
)

# خروجی:
{
    'success': True,
    'total_commits': 3,
    'commits': [...],
    'failed_commits': []
}
```

### `smart_commit_push()`

Workflow کامل (یک دستور).

```python
result = framework.smart_commit_push()

# خروجی:
{
    'success': True,
    'analysis': {...},
    'commits': {...},
    'push': {...},
    'summary': '...'
}
```

### `check_auto_commit()`

بررسی آستانه 100 فایل.

```python
result = framework.check_auto_commit()

if result:
    # کامیت خودکار انجام شد
    print(result['summary'])
else:
    # هنوز به آستانه نرسیده
    print("Not yet")
```

---

## مثال‌های پیشرفته

### مثال 1: Workflow سفارشی

```python
from gravity_framework import GravityFramework

framework = GravityFramework()

# 1. تحلیل
analysis = framework.analyze_commits()

# 2. فقط feature files را کامیت کن
for rec in analysis['recommendations']:
    if rec['category'].startswith('features-'):
        # کامیت این دسته
        result = framework.git.smart_commit(
            message=rec['suggested_message'],
            files=rec['files']
        )
        print(f"Committed: {rec['category']}")
```

### مثال 2: کامیت با تأیید دستی

```python
framework = GravityFramework()

# تحلیل
analysis = framework.analyze_commits()

# نمایش توصیه‌ها
for i, rec in enumerate(analysis['recommendations'], 1):
    print(f"\n{i}. {rec['suggested_message']}")
    print(f"   Files: {len(rec['files'])}")
    
    # تأیید کاربر
    confirm = input("   Commit this? (y/n): ")
    
    if confirm.lower() == 'y':
        result = framework.git.smart_commit(
            message=rec['suggested_message'],
            files=rec['files']
        )
        print("   ✅ Committed")
```

### مثال 3: کامیت با Batch Size

```python
framework = GravityFramework()

# کامیت هر 10 فایل
result = framework.organize_and_commit(batch_size=10)

# هر دسته حداکثر 10 فایل دارد
```

---

## بهترین روش‌ها

### 1. Commit Often

```python
# ❌ بد: صدها فایل یکجا
# ... 200 فایل تغییر ...
framework.smart_commit_push()

# ✅ خوب: کامیت منظم
# ... 10 فایل تغییر ...
framework.smart_commit_push()
# ... 15 فایل دیگر ...
framework.smart_commit_push()
```

### 2. استفاده از Auto-Commit

```python
# هر 100 فایل، خودکار کامیت و پوش
framework.check_auto_commit()
```

### 3. Validate قبل از Commit

```python
# اول استانداردها را بررسی کن
validation = framework.validate_standards()

if not validation['valid']:
    # رفع خودکار
    framework.auto_fix_standards()

# سپس کامیت
framework.smart_commit_push()
```

### 4. پیام‌های معنادار

```python
# ✅ خوب: توضیح واضح
feat(ai): add intelligent team generation with IQ 180+ experts

# ❌ بد: نامفهوم
update files
```

---

## عیب‌یابی

### مشکل: کامیت fail می‌شود

```python
# بررسی کنید چه چیزی fail شده
result = framework.organize_and_commit()

for failed in result['failed_commits']:
    print(f"Failed: {failed['category']}")
    print(f"Error: {failed['error']}")
    print(f"Checks: {failed['checks']}")
```

### مشکل: Git integration فعال نیست

```python
framework = GravityFramework()

if framework.commit_manager is None:
    print("Not a Git repository!")
    # راه حل: git init کنید
```

### مشکل: AI پیام خوبی تولید نمی‌کند

```python
# استفاده از پیام‌های پیشنهادی بدون AI
result = framework.organize_and_commit(
    auto_generate_messages=False  # بدون AI
)
```

---

## خلاصه

سیستم مدیریت هوشمند کامیت:

✅ **خودکار** - دسته‌بندی و کامیت خودکار  
✅ **هوشمند** - تولید پیام با AI  
✅ **منظم** - کامیت‌های منطقی و تمیز  
✅ **استاندارد** - رعایت TEAM_PROMPT.md  
✅ **ساده** - یک دستور برای همه چیز!  

**یک دستور:**

```python
framework.smart_commit_push()
# ✅ تمام! همه چیز کامیت و پوش شد!
```

---

## مسئول

**Dr. Chen Wei**
- نقش: CLI & Developer Experience Designer
- تخصص: Git workflow automation
- تجربه: 18 سال
- IQ: 191

**مسئولیت‌ها:**
- طراحی Git workflow
- اتوماسیون کامیت‌ها
- تجربه توسعه‌دهنده
- CLI design
