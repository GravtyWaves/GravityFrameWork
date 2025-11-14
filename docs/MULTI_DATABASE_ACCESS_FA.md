# دسترسی چندگانه به دیتابیس و یادگیری
## Multi-Database Access & Learning

> **فریمورک Gravity به همه دیتابیس‌های میکروسرویس‌ها متصل می‌شود و از داده‌ها یاد می‌گیرد!**

---

## 📚 فهرست مطالب

1. [معرفی](#معرفی)
2. [قابلیت‌های کلیدی](#قابلیتهای-کلیدی)
3. [استفاده سریع](#استفاده-سریع)
4. [مثال‌های کامل](#مثالهای-کامل)
5. [یادگیری از داده](#یادگیری-از-داده)
6. [API Reference](#api-reference)

---

## معرفی

یکی از **قدرتمندترین** ویژگی‌های Gravity Framework:

**دسترسی یکپارچه به همه دیتابیس‌های میکروسرویس‌ها**

### چرا مهم است؟

در یک سیستم microservice، داده‌ها پراکنده هستند:
- سرویس `auth` دیتابیس خودش را دارد
- سرویس `order` دیتابیس خودش
- سرویس `product` دیتابیس خودش
- ...

**Gravity Framework همه آنها را به هم متصل می‌کند! 🔗**

---

## قابلیت‌های کلیدی

### 1️⃣ دسترسی یکپارچه

```python
# به همه دیتابیس‌ها همزمان دسترسی داشته باشید
count = await framework.register_service_databases()
# ✅ 15 دیتابیس ثبت شد!
```

### 2️⃣ جستجو در همه دیتابیس‌ها

```python
# یک جستجو در همه سرویس‌ها
results = await framework.search_all_databases('admin@example.com')
# می‌گردد در auth, user, order, و...
```

### 3️⃣ یادگیری هوشمند

```python
# سیستم از داده‌ها یاد می‌گیرد
insights = await framework.learn_from_database_data()
# الگوها، روابط، پیشنهادات
```

### 4️⃣ پاسخ به سوالات

```python
# سوال بپرسید، AI جواب می‌دهد
answer = await framework.answer_with_data(
    "چند کاربر فعال داریم?"
)
```

---

## استفاده سریع

### مرحله 1: ثبت دیتابیس‌ها

```python
from gravity_framework import GravityFramework
import asyncio

async def main():
    framework = GravityFramework()
    
    # کشف و نصب سرویس‌ها
    services = framework.discover_services()
    await framework.install()
    
    # ثبت همه دیتابیس‌ها
    count = await framework.register_service_databases()
    print(f"✅ {count} دیتابیس ثبت شد")

asyncio.run(main())
```

### مرحله 2: Query کردن

```python
# Query سرویس خاص
users = await framework.query_service_database(
    'auth-service',
    'SELECT * FROM users WHERE active = true'
)

print(f"کاربران فعال: {len(users)}")
```

### مرحله 3: یادگیری

```python
# یادگیری از داده‌ها
insights = await framework.learn_from_database_data()

print("Schemas:", insights['schemas'].keys())
print("Patterns:", insights['patterns'])
print("Recommendations:", insights['recommendations'])
```

---

## مثال‌های کامل

### مثال 1: جستجو در همه سرویس‌ها

```python
import asyncio
from gravity_framework import GravityFramework

async def search_example():
    framework = GravityFramework()
    await framework.register_service_databases()
    
    # جستجو
    results = await framework.search_all_databases('premium')
    
    print("🔍 نتایج جستجو:")
    for service, matches in results.items():
        if matches:
            print(f"\n{service}:")
            for match in matches:
                print(f"  {match['table']}: {match['count']} نتیجه")

asyncio.run(search_example())
```

**خروجی:**
```
🔍 نتایج جستجو:

auth-service:
  users: 5 نتیجه
  subscriptions: 12 نتیجه

order-service:
  orders: 8 نتیجه
  products: 3 نتیجه
```

### مثال 2: Federated Query

```python
async def federated_example():
    framework = GravityFramework()
    await framework.register_service_databases()
    
    # Query جدول users در همه سرویس‌ها
    all_users = await framework.federated_query(
        'users',
        where='active = true',
        limit=50
    )
    
    print(f"👥 {len(all_users)} کاربر یافت شد:")
    for user in all_users:
        source = user.pop('_source_service')
        print(f"  {user['email']} (از {source})")

asyncio.run(federated_example())
```

**خروجی:**
```
👥 127 کاربر یافت شد:
  admin@example.com (از auth-service)
  user@example.com (از auth-service)
  customer@store.com (از order-service)
  ...
```

### مثال 3: Aggregation

```python
async def aggregate_example():
    framework = GravityFramework()
    await framework.register_service_databases()
    
    # شمارش کاربران
    result = await framework.aggregate_data('users', 'COUNT(*)')
    
    print(f"📊 تعداد کاربران:")
    print(f"  کل: {result['total']}")
    print(f"\n  به تفکیک سرویس:")
    for service, count in result['by_service'].items():
        print(f"    {service}: {count}")
    
    # مجموع فروش
    result = await framework.aggregate_data('orders', 'SUM(total)')
    print(f"\n💰 مجموع فروش:")
    print(f"  کل: ${result['total']:,.2f}")

asyncio.run(aggregate_example())
```

**خروجی:**
```
📊 تعداد کاربران:
  کل: 1,247

  به تفکیک سرویس:
    auth-service: 823
    user-service: 424

💰 مجموع فروش:
  کل: $52,489.50
```

### مثال 4: یادگیری از داده

```python
async def learning_example():
    framework = GravityFramework()
    await framework.register_service_databases()
    
    # یادگیری کامل
    insights = await framework.learn_from_database_data()
    
    print("🧠 یادگیری از داده‌ها:\n")
    
    # Schemas
    print("Schemas کشف شده:")
    for service, schema in insights['schemas'].items():
        if 'error' not in schema:
            tables = schema.get('tables', {})
            print(f"  {service}: {len(tables)} جدول")
    
    # Patterns
    print("\nPatterns پیدا شده:")
    for service, patterns in insights['data_patterns'].items():
        print(f"  {service}:")
        for table, info in patterns['tables'].items():
            print(f"    {table}:")
            print(f"      Columns: {info['column_count']}")
            print(f"      Timestamps: {info['has_timestamps']}")
    
    # Relationships
    print("\nRelationships:")
    total_rels = sum(
        len(rels) 
        for rels in insights['relationships'].values()
    )
    print(f"  {total_rels} رابطه پیدا شد")
    
    # Recommendations
    print("\n💡 پیشنهادات:")
    for rec in insights['recommendations']:
        print(f"  {rec}")

asyncio.run(learning_example())
```

**خروجی:**
```
🧠 یادگیری از داده‌ها:

Schemas کشف شده:
  auth-service: 5 جدول
  user-service: 3 جدول
  order-service: 8 جدول

Patterns پیدا شده:
  auth-service:
    users:
      Columns: 8
      Timestamps: True
    sessions:
      Columns: 5
      Timestamps: True

Relationships:
  25 رابطه پیدا شد

💡 پیشنهادات:
  📊 Found 3 common tables across services
  ⏰ order-service.carts missing timestamps
  🔗 Detected 25 relationships
```

### مثال 5: پاسخ به سوالات

```python
async def qa_example():
    framework = GravityFramework()
    await framework.register_service_databases()
    
    questions = [
        "چند کاربر فعال داریم؟",
        "آخرین سفارش‌ها چه بودند؟",
        "کاربران admin کیانند؟"
    ]
    
    for question in questions:
        print(f"\n❓ {question}")
        
        answer = await framework.answer_with_data(question)
        
        print(f"✅ جواب:")
        print(f"  سرویس‌های جستجو شده: {answer['total_services']}")
        print(f"  نتایج: {len(answer['search_results'])}")
        
        for service, results in answer['search_results'].items():
            if results:
                for result in results[:2]:
                    print(f"    {service}.{result['table']}: {result['count']}")

asyncio.run(qa_example())
```

---

## یادگیری از داده

### الگوهایی که سیستم یاد می‌گیرد:

#### 1️⃣ Schema Patterns
```python
{
    'users': {
        'column_count': 8,
        'has_timestamps': True,
        'has_id': True,
        'nullable_columns': 3
    }
}
```

#### 2️⃣ Common Structures
```python
{
    'users': ['auth-service', 'user-service'],
    'orders': ['order-service', 'payment-service']
}
# جداول مشترک در چند سرویس
```

#### 3️⃣ Relationships
```python
[
    {
        'table': 'user_roles',
        'column': 'user_id',
        'references': 'users'
    },
    {
        'table': 'orders',
        'column': 'user_id',
        'references': 'users'
    }
]
```

#### 4️⃣ Recommendations
```python
[
    "📊 Found 3 common tables - consider standardizing",
    "⏰ sessions table missing timestamps",
    "🔗 Detected 15 relationships - add constraints"
]
```

---

## API Reference

### `register_service_databases()`

ثبت همه دیتابیس‌های سرویس‌ها:

```python
count = await framework.register_service_databases()
# Returns: تعداد دیتابیس‌های ثبت شده
```

### `query_service_database(service, sql, params)`

Query سرویس خاص:

```python
users = await framework.query_service_database(
    'auth-service',
    'SELECT * FROM users WHERE active = :active',
    {'active': True}
)
```

### `search_all_databases(term)`

جستجو در همه دیتابیس‌ها:

```python
results = await framework.search_all_databases('admin@example.com')
```

### `get_all_database_stats()`

آمار همه دیتابیس‌ها:

```python
stats = await framework.get_all_database_stats()
# {
#   'auth-service': {
#     'table_count': 5,
#     'total_rows': 1247,
#     'tables': {...}
#   }
# }
```

### `learn_from_database_data()`

یادگیری از داده‌ها:

```python
insights = await framework.learn_from_database_data()
# {
#   'schemas': {...},
#   'patterns': {...},
#   'relationships': {...},
#   'recommendations': [...]
# }
```

### `answer_with_data(question)`

پاسخ به سوال با استفاده از داده:

```python
answer = await framework.answer_with_data("چند کاربر داریم؟")
```

### `federated_query(table, where, limit)`

Query جدول در همه سرویس‌ها:

```python
all_users = await framework.federated_query(
    'users',
    where='active = true',
    limit=100
)
```

### `aggregate_data(table, func)`

Aggregation روی داده‌ها:

```python
result = await framework.aggregate_data('users', 'COUNT(*)')
# {
#   'total': 1247,
#   'by_service': {
#     'auth-service': 823,
#     'user-service': 424
#   }
# }
```

---

## موارد استفاده

### 1️⃣ Analytics

```python
# تحلیل کاربران
total = await framework.aggregate_data('users', 'COUNT(*)')
active = await framework.federated_query('users', 'active = true')

print(f"کل: {total['total']}")
print(f"فعال: {len(active)}")
```

### 2️⃣ Reporting

```python
# گزارش فروش
revenue = await framework.aggregate_data('orders', 'SUM(total)')
orders = await framework.aggregate_data('orders', 'COUNT(*)')

print(f"فروش: ${revenue['total']:,.2f}")
print(f"تعداد سفارش: {orders['total']}")
```

### 3️⃣ Search

```python
# جستجو کاربر
results = await framework.search_all_databases('user@example.com')

for service, matches in results.items():
    print(f"{service}: {len(matches)} نتیجه")
```

### 4️⃣ Troubleshooting

```python
# پیدا کردن خطا
error_logs = await framework.query_service_database(
    'order-service',
    'SELECT * FROM logs WHERE level = :level',
    {'level': 'ERROR'}
)
```

### 5️⃣ Learning

```python
# یادگیری و بهبود
insights = await framework.learn_from_database_data()

for rec in insights['recommendations']:
    print(f"💡 {rec}")
    # اصلاحات را انجام دهید
```

---

## مزایا

✅ **دسترسی یکپارچه** - یک API برای همه دیتابیس‌ها  
✅ **یادگیری هوشمند** - AI از داده‌ها یاد می‌گیرد  
✅ **جستجوی سریع** - پیدا کردن داده در هر جا  
✅ **Aggregation** - ترکیب داده از چند سرویس  
✅ **پاسخگویی** - جواب سوالات کاربران  
✅ **پیشنهادات** - بهبود معماری دیتابیس  

---

## نتیجه‌گیری

با Gravity Framework:

1. **به همه دیتابیس‌ها دسترسی دارید** 🔗
2. **در همه جا جستجو کنید** 🔍
3. **از داده‌ها یاد بگیرید** 🧠
4. **به سوالات پاسخ دهید** 💬
5. **پیشنهادات هوشمند دریافت کنید** 💡

**شروع کنید!** 🚀

---

*تولید شده توسط Gravity Framework Team* 🌟
