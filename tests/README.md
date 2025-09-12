# 🧪 تست‌های PEY Builder

این پوشه شامل تمام تست‌های جامع و حرفه‌ای برای پروژه PEY Builder است.

## 📁 ساختار فایل‌ها

### 🐍 تست‌های Python
- `test_simple.py` - تست‌های ساده برای اطمینان از کارکرد
- `test_basic.py` - تست‌های پایه و عملکرد اصلی
- `test_extractor.py` - تست‌های استخراج قالب‌ها
- `test_advanced_features.py` - تست‌های ویژگی‌های پیشرفته
- `test_security.py` - تست‌های امنیتی جامع
- `test_performance.py` - تست‌های عملکرد و بهینه‌سازی

### 🟢 تست‌های Node.js
- `test_simple.test.js` - تست‌های ساده Jest
- `test_node_comprehensive.js` - تست‌های جامع Node.js
- `setup.js` - تنظیمات اولیه Jest

### ⚙️ فایل‌های پیکربندی
- `jest.config.js` - تنظیمات Jest
- `setup.js` - تنظیمات اولیه تست‌ها

## 🚀 اجرای تست‌ها

### تست‌های Python
```bash
# اجرای تمام تست‌های Python
python -m pytest tests/ -v

# اجرای تست‌های خاص
python -m pytest tests/test_simple.py -v
python -m pytest tests/test_advanced_features.py -v
python -m pytest tests/test_security.py -v
python -m pytest tests/test_performance.py -v

# اجرای با پوشش کد
python -m pytest tests/ --cov=. --cov-report=html
```

### تست‌های Node.js
```bash
# اجرای تمام تست‌های Jest
npm test

# اجرای تست‌های جامع
npm run test:comprehensive

# اجرای تمام تست‌ها
npm run test:all

# اجرای با پوشش کد
npm run test:coverage
```

## 📊 انواع تست‌ها

### 🧪 تست‌های واحد (Unit Tests)
- تست‌های عملکردهای جداگانه
- تست‌های کلاس‌ها و متدها
- تست‌های validation و error handling

### 🔒 تست‌های امنیتی (Security Tests)
- تست‌های SQL Injection
- تست‌های XSS Prevention
- تست‌های Path Traversal
- تست‌های Authentication
- تست‌های Rate Limiting

### ⚡ تست‌های عملکرد (Performance Tests)
- تست‌های حافظه و CPU
- تست‌های I/O و شبکه
- تست‌های همزمانی
- تست‌های دیتابیس
- تست‌های کش

### 🎯 تست‌های یکپارچگی (Integration Tests)
- تست‌های API
- تست‌های دیتابیس
- تست‌های فایل سیستم
- تست‌های شبکه

## 🔧 تنظیمات CI/CD

تست‌ها به صورت خودکار در GitHub Actions اجرا می‌شوند:

- **Python Tests**: Python 3.9 و 3.11
- **Node.js Tests**: Node.js 18 و 20
- **Security Tests**: Bandit, Safety, Semgrep
- **Performance Tests**: Memory, CPU, I/O monitoring

## 📈 گزارش‌گیری

### پوشش کد (Code Coverage)
- حداقل 70% پوشش کد برای تمام فایل‌ها
- گزارش HTML برای بررسی جزئیات
- گزارش JSON برای CI/CD

### گزارش‌های امنیتی
- گزارش Bandit برای Python
- گزارش Safety برای وابستگی‌ها
- گزارش Semgrep برای کد

## 🛠️ توسعه تست‌ها

### اضافه کردن تست جدید
1. فایل تست را در پوشه مناسب ایجاد کنید
2. نام فایل را با `test_` شروع کنید
3. کلاس‌های تست را از `unittest.TestCase` ارث برید
4. متدهای تست را با `test_` شروع کنید

### بهترین روش‌ها
- هر تست باید مستقل باشد
- از mock objects استفاده کنید
- تست‌ها باید سریع اجرا شوند
- نام‌های توصیفی انتخاب کنید
- کامنت‌های مناسب اضافه کنید

## 🐛 عیب‌یابی

### مشکلات رایج
- **Import Error**: مسیرهای Python را بررسی کنید
- **Timeout**: timeout تست‌ها را افزایش دهید
- **Memory Error**: حافظه سیستم را بررسی کنید
- **Network Error**: اتصال اینترنت را بررسی کنید

### لاگ‌ها
- لاگ‌های تست در `coverage/` ذخیره می‌شوند
- گزارش‌های HTML در `coverage/html/` موجود است
- لاگ‌های CI/CD در GitHub Actions قابل مشاهده است

## 📞 پشتیبانی

برای سوالات و مشکلات:
- GitHub Issues: [ایجاد Issue](https://github.com/iman-noroozi/sitebuilder/issues)
- Email: info@peysunweb.ir
- Website: [peyai.ir](https://peyai.ir)

---

**توسعه یافته با ❤️ توسط تیم PEY Builder**
