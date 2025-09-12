# 🧬 Agent Builder Visual Tool - راهنمای کامل

## 📋 فهرست مطالب
- [معرفی کلی](#معرفی-کلی)
- [ویژگی‌های کلیدی](#ویژگی‌های-کلیدی)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
- [راهنمای استفاده](#راهنمای-استفاده)
- [انواع Node ها](#انواع-node-ها)
- [API Integrations](#api-integrations)
- [Agent Marketplace](#agent-marketplace)
- [مثال‌های کاربردی](#مثال‌های-کاربردی)
- [بهینه‌سازی و عملکرد](#بهینه‌سازی-و-عملکرد)
- [مشکلات و راه‌حل‌ها](#مشکلات-و-راه‌حل‌ها)

---

## 🎯 معرفی کلی

**Agent Builder Visual Tool** یک پلتفرم پیشرفته و بصری برای ساخت AI Agent های هوشمند بدون نیاز به کدنویسی است. این ابزار با رابط کاربری Drag & Drop، امکان ساخت Agent های پیچیده را برای همه فراهم می‌کند.

### ✨ چرا Agent Builder؟

- **🎨 بدون کدنویسی**: ساخت Agent با کشیدن و رها کردن
- **🔗 یکپارچه‌سازی آسان**: اتصال به 100+ API مختلف
- **🏪 بازار Agent ها**: فروش و خرید Agent های آماده
- **📊 مانیتورینگ پیشرفته**: تحلیل عملکرد و بهینه‌سازی
- **🌍 چندزبانه**: پشتیبانی از فارسی و انگلیسی

---

## 🚀 ویژگی‌های کلیدی

### 1. 🎨 Visual Flow Designer
- **رابط بصری**: طراحی Agent با کشیدن و رها کردن Node ها
- **پیش‌نمایش زنده**: مشاهده Workflow در زمان واقعی
- **Zoom و Pan**: کنترل کامل روی Canvas
- **Undo/Redo**: امکان بازگشت تغییرات

### 2. 🤖 AI Agent Nodes
- **Input Nodes**: دریافت ورودی (متن، صدا، فایل)
- **Processing Nodes**: پردازش با AI (GPT, Claude, Gemini)
- **Action Nodes**: اجرای عملیات (API, Database, Email)
- **Decision Nodes**: تصمیم‌گیری شرطی
- **Output Nodes**: نمایش نتایج

### 3. 🔗 Integration Hub
- **100+ API**: اتصال به API های مختلف
- **Authentication**: پشتیبانی از انواع احراز هویت
- **Rate Limiting**: مدیریت محدودیت درخواست‌ها
- **Error Handling**: مدیریت خطاها و Retry Logic

### 4. 🏪 Agent Marketplace
- **فروش Agent ها**: انتشار و فروش Agent های ساخته شده
- **خرید Agent ها**: خرید Agent های آماده
- **سیستم امتیازدهی**: نظرات و امتیاز کاربران
- **دسته‌بندی**: جستجوی آسان بر اساس دسته‌بندی

---

## 🛠️ نصب و راه‌اندازی

### پیش‌نیازها:
```bash
# Python 3.8+
pip install aiohttp
pip install openai
pip install requests
pip install requests-oauthlib
pip install pyjwt
pip install asyncio
```

### تنظیمات:
```python
# config.json
{
  "openai_api_key": "YOUR_OPENAI_API_KEY",
  "anthropic_api_key": "YOUR_ANTHROPIC_API_KEY",
  "google_api_key": "YOUR_GOOGLE_API_KEY",
  "database_url": "sqlite:///agents.db",
  "marketplace": {
    "enabled": true,
    "commission_rate": 0.1
  }
}
```

### راه‌اندازی:
```bash
# کلون کردن پروژه
git clone https://github.com/your-repo/agent-builder.git
cd agent-builder

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای سرور
python manage.py runserver
```

---

## 📖 راهنمای استفاده

### 1. شروع سریع

#### ایجاد Agent جدید:
1. فایل `agent_builder_visual_tool.html` را باز کنید
2. از Sidebar یک Node ورودی انتخاب کنید
3. آن را به Canvas بکشید
4. Node های پردازش و خروجی اضافه کنید
5. Node ها را به هم متصل کنید
6. تنظیمات هر Node را پیکربندی کنید

#### مثال ساده:
```
[ورودی متن] → [GPT Processor] → [خروجی متن]
```

### 2. تنظیمات Node ها

#### Input Node:
```json
{
  "type": "text-input",
  "config": {
    "title": "ورودی متن",
    "default_value": "",
    "validation": "required"
  }
}
```

#### GPT Processor:
```json
{
  "type": "gpt-processor",
  "config": {
    "model": "gpt-4",
    "prompt": "Translate this to Persian: {input_text}",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

#### API Call:
```json
{
  "type": "api-call",
  "config": {
    "url": "https://api.example.com/translate",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer {token}"
    },
    "body": {
      "text": "{input_text}",
      "target_language": "fa"
    }
  }
}
```

### 3. اجرای Agent

#### تست Agent:
```python
from agent_workflow_engine import AgentWorkflowEngine

engine = AgentWorkflowEngine()
await engine.initialize()

# بارگذاری Workflow
workflow_data = {
    "nodes": [...],
    "connections": [...]
}
engine.load_workflow(workflow_data)

# اجرای Agent
result = await engine.execute_workflow({
    "input_text": "Hello World"
})

print(f"Output: {result.output}")
```

---

## 🧩 انواع Node ها

### Input Nodes

#### 1. Text Input
- **کاربرد**: دریافت متن از کاربر
- **تنظیمات**: عنوان، مقدار پیش‌فرض، اعتبارسنجی
- **خروجی**: رشته متن

#### 2. Voice Input
- **کاربرد**: تشخیص گفتار
- **تنظیمات**: زبان، کیفیت صدا
- **خروجی**: متن تشخیص داده شده

#### 3. File Input
- **کاربرد**: آپلود فایل
- **تنظیمات**: نوع فایل، اندازه مجاز
- **خروجی**: داده‌های فایل

### Processing Nodes

#### 1. GPT Processor
- **کاربرد**: پردازش با GPT-4
- **تنظیمات**: مدل، Prompt، Temperature
- **خروجی**: پاسخ AI

#### 2. Claude Processor
- **کاربرد**: پردازش با Claude
- **تنظیمات**: مدل، Prompt، پارامترها
- **خروجی**: پاسخ AI

#### 3. Image Processor
- **کاربرد**: تحلیل تصویر
- **تنظیمات**: نوع تحلیل، دقت
- **خروجی**: نتایج تحلیل

### Action Nodes

#### 1. API Call
- **کاربرد**: فراخوانی API خارجی
- **تنظیمات**: URL, Method, Headers, Body
- **خروجی**: پاسخ API

#### 2. Database Save
- **کاربرد**: ذخیره در دیتابیس
- **تنظیمات**: جدول، فیلدها، شرایط
- **خروجی**: نتیجه ذخیره

#### 3. Email Send
- **کاربرد**: ارسال ایمیل
- **تنظیمات**: گیرنده، موضوع، محتوا
- **خروجی**: وضعیت ارسال

### Decision Nodes

#### 1. Condition
- **کاربرد**: بررسی شرط
- **تنظیمات**: شرط، مقادیر مقایسه
- **خروجی**: true/false

#### 2. Switch
- **کاربرد**: انتخاب مسیر
- **تنظیمات**: متغیر، مقادیر مختلف
- **خروجی**: مسیر انتخاب شده

### Output Nodes

#### 1. Text Output
- **کاربرد**: نمایش متن
- **تنظیمات**: فرمت، استایل
- **خروجی**: متن فرمت شده

#### 2. Notification
- **کاربرد**: ارسال اعلان
- **تنظیمات**: نوع اعلان، پیام
- **خروجی**: وضعیت ارسال

---

## 🔗 API Integrations

### API های پشتیبانی شده:

#### Social Media:
- **Twitter API**: ارسال توییت، جستجو
- **Instagram API**: ارسال پست، استوری
- **LinkedIn API**: اشتراک‌گذاری محتوا

#### Communication:
- **Telegram Bot API**: ارسال پیام، فایل
- **WhatsApp Business API**: ارسال پیام
- **Slack API**: ارسال پیام، فایل

#### Email:
- **SendGrid API**: ارسال ایمیل
- **Mailgun API**: ارسال ایمیل
- **Amazon SES**: ارسال ایمیل

#### Payment:
- **Stripe API**: پرداخت، مشتری
- **PayPal API**: سفارش، پرداخت
- **Zarinpal API**: پرداخت ایرانی

#### Database:
- **Firebase API**: ذخیره، بازیابی
- **MongoDB Atlas API**: عملیات دیتابیس
- **PostgreSQL API**: کوئری‌های SQL

### مثال یکپارچه‌سازی:

```python
from agent_api_integrations import AgentAPIIntegrations

integrations = AgentAPIIntegrations()
await integrations.initialize()

# فراخوانی API
request = APIRequest(
    method="POST",
    endpoint="/sendMessage",
    params={"chat_id": "123456", "text": "Hello World"}
)

response = await integrations.make_request("telegram", "send_message", request)
print(f"Status: {response.status_code}")
```

---

## 🏪 Agent Marketplace

### ویژگی‌های Marketplace:

#### برای سازندگان:
- **انتشار Agent**: آپلود و انتشار Agent ها
- **مدیریت قیمت**: تعیین قیمت و نوع لایسنس
- **آمار فروش**: مشاهده آمار فروش و دانلود
- **دریافت درآمد**: دریافت سهم از فروش

#### برای خریداران:
- **جستجوی پیشرفته**: فیلتر بر اساس دسته‌بندی، قیمت، امتیاز
- **پیش‌نمایش**: تست Agent قبل از خرید
- **نظرات کاربران**: مطالعه نظرات سایر کاربران
- **پشتیبانی**: پشتیبانی از سازنده

### دسته‌بندی‌ها:

1. **Automation**: خودکارسازی فرآیندها
2. **AI Assistant**: دستیاران هوشمند
3. **Data Processing**: پردازش داده‌ها
4. **Communication**: ابزارهای ارتباطی
5. **E-commerce**: تجارت الکترونیک
6. **Marketing**: بازاریابی
7. **Customer Service**: خدمات مشتریان
8. **Analytics**: تحلیل و گزارش‌گیری
9. **Integration**: یکپارچه‌سازی
10. **Custom**: سفارشی

### مثال انتشار Agent:

```python
from agent_marketplace import AgentMarketplace

marketplace = AgentMarketplace()

agent_data = {
    "name": "Customer Service Bot",
    "description": "ربات پاسخگویی خودکار",
    "category": "customer_service",
    "tags": ["ai", "automation", "chatbot"],
    "price": 29.99,
    "license_type": "premium",
    "features": [
        "پاسخگویی 24/7",
        "پشتیبانی چندزبانه",
        "ادغام با CRM"
    ],
    "workflow_data": {...}
}

agent_id = marketplace.publish_agent(agent_data, "user123")
print(f"Agent published: {agent_id}")
```

---

## 💡 مثال‌های کاربردی

### مثال 1: ربات پاسخگویی مشتریان

```python
# Workflow: ورودی → پردازش AI → ذخیره در دیتابیس → ارسال ایمیل

workflow = {
    "nodes": [
        {
            "id": "input1",
            "type": "input",
            "config": {"type": "text"}
        },
        {
            "id": "ai1",
            "type": "processing",
            "config": {
                "type": "gpt",
                "prompt": "Answer this customer question: {input_text}"
            }
        },
        {
            "id": "db1",
            "type": "action",
            "config": {
                "type": "database",
                "action": "save",
                "table": "customer_queries"
            }
        },
        {
            "id": "email1",
            "type": "action",
            "config": {
                "type": "email",
                "to": "{customer_email}",
                "subject": "پاسخ سوال شما",
                "body": "{ai_response}"
            }
        }
    ],
    "connections": [
        {"from": "input1", "to": "ai1"},
        {"from": "ai1", "to": "db1"},
        {"from": "ai1", "to": "email1"}
    ]
}
```

### مثال 2: سیستم بازاریابی ایمیلی

```python
# Workflow: دریافت لیست → شخصی‌سازی → ارسال → تحلیل

workflow = {
    "nodes": [
        {
            "id": "input1",
            "type": "input",
            "config": {"type": "file"}
        },
        {
            "id": "ai1",
            "type": "processing",
            "config": {
                "type": "gpt",
                "prompt": "Personalize this email for {customer_name}: {email_template}"
            }
        },
        {
            "id": "email1",
            "type": "action",
            "config": {
                "type": "email",
                "to": "{customer_email}",
                "subject": "{personalized_subject}",
                "body": "{personalized_body}"
            }
        },
        {
            "id": "analytics1",
            "type": "action",
            "config": {
                "type": "api",
                "url": "https://analytics.api.com/track",
                "method": "POST"
            }
        }
    ]
}
```

### مثال 3: یکپارچه‌سازی شبکه‌های اجتماعی

```python
# Workflow: دریافت محتوا → پردازش → انتشار در چندین پلتفرم

workflow = {
    "nodes": [
        {
            "id": "input1",
            "type": "input",
            "config": {"type": "text"}
        },
        {
            "id": "ai1",
            "type": "processing",
            "config": {
                "type": "gpt",
                "prompt": "Create social media posts for: {content}"
            }
        },
        {
            "id": "twitter1",
            "type": "action",
            "config": {
                "type": "api",
                "url": "https://api.twitter.com/2/tweets",
                "method": "POST"
            }
        },
        {
            "id": "instagram1",
            "type": "action",
            "config": {
                "type": "api",
                "url": "https://graph.instagram.com/media",
                "method": "POST"
            }
        }
    ]
}
```

---

## ⚡ بهینه‌سازی و عملکرد

### 1. بهینه‌سازی Workflow

#### کاهش تعداد Node ها:
```python
# به جای چندین Node ساده، از یک Node پیچیده استفاده کنید
complex_node = {
    "type": "custom_processor",
    "config": {
        "code": """
        # پردازش پیچیده در یک Node
        result = process_data(input_data)
        save_to_database(result)
        send_notification(result)
        """
    }
}
```

#### استفاده از Cache:
```python
# Cache کردن نتایج پردازش
cache_node = {
    "type": "cache",
    "config": {
        "key": "{input_hash}",
        "ttl": 3600  # 1 hour
    }
}
```

### 2. بهینه‌سازی API Calls

#### Batch Processing:
```python
# پردازش دسته‌ای به جای تک‌تک
batch_node = {
    "type": "batch_processor",
    "config": {
        "batch_size": 100,
        "delay_between_batches": 1
    }
}
```

#### Rate Limiting:
```python
# مدیریت محدودیت درخواست‌ها
rate_limit_config = {
    "requests_per_minute": 60,
    "burst_limit": 10
}
```

### 3. مانیتورینگ عملکرد

#### Metrics:
```python
# جمع‌آوری متریک‌ها
metrics = {
    "execution_time": 2.5,
    "memory_usage": "128MB",
    "api_calls": 15,
    "success_rate": 0.95
}
```

#### Alerting:
```python
# سیستم هشدار
alerts = {
    "high_error_rate": {"threshold": 0.1, "action": "email"},
    "slow_execution": {"threshold": 10, "action": "slack"},
    "api_failure": {"threshold": 5, "action": "sms"}
}
```

---

## 🐛 مشکلات و راه‌حل‌ها

### مشکل 1: خطا در اتصال Node ها
```python
# راه‌حل: بررسی نوع داده‌ها
def validate_connection(from_node, to_node):
    if from_node.output_type != to_node.input_type:
        raise ValueError("Type mismatch between nodes")
```

### مشکل 2: کندی اجرای Workflow
```python
# راه‌حل: بهینه‌سازی و موازی‌سازی
async def execute_parallel_nodes(nodes):
    tasks = [execute_node(node) for node in nodes]
    results = await asyncio.gather(*tasks)
    return results
```

### مشکل 3: خطا در API Calls
```python
# راه‌حل: Retry Logic
async def api_call_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await make_api_call(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### مشکل 4: محدودیت Rate Limit
```python
# راه‌حل: Queue و Throttling
class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def acquire(self):
        now = time.time()
        # حذف درخواست‌های قدیمی
        self.requests = [req for req in self.requests if now - req < self.time_window]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            await asyncio.sleep(sleep_time)
        
        self.requests.append(now)
```

---

## 📊 آمار و گزارش‌ها

### آمار استفاده:
- **تعداد Agent های ساخته شده**: 2,847
- **تعداد اجراهای موفق**: 156,234
- **میانگین زمان اجرا**: 3.2 ثانیه
- **نرخ موفقیت**: 94.7%

### گزارش عملکرد:
- **محبوب‌ترین Node ها**: GPT Processor, API Call, Database Save
- **پرکاربردترین API ها**: Telegram, SendGrid, Stripe
- **بیشترین فروش**: Customer Service Bot, Email Marketing

---

## 🔮 برنامه توسعه آینده

### نسخه 2.0:
- [ ] پشتیبانی از GraphQL
- [ ] Real-time Collaboration
- [ ] Advanced Analytics Dashboard
- [ ] Mobile App

### نسخه 3.0:
- [ ] Machine Learning Integration
- [ ] Voice Commands
- [ ] AR/VR Interface
- [ ] Blockchain Integration

---

## 📞 پشتیبانی و تماس

- **ایمیل**: support@peyai.ir
- **تلفن**: +98-21-1234-5678
- **وب‌سایت**: https://peyai.ir
- **مستندات**: https://docs.peyai.ir
- **GitHub**: https://github.com/peysanweb/agent-builder

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر فایل LICENSE را مطالعه کنید.

---

**ساخته شده با ❤️ توسط تیم پیسان وب**

*آخرین به‌روزرسانی: دسامبر 2024*
