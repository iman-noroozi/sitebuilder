# 📝 Changelog

تمام تغییرات مهم این پروژه در این فایل مستند شده است.

فرمت این فایل بر اساس [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) است و این پروژه از [Semantic Versioning](https://semver.org/spec/v2.0.0.html) پیروی می‌کند.

## [0.1.0] - 2024-01-01

### 🎉 اولین انتشار

#### ✨ ویژگی‌های جدید
- **استخراج‌کننده قالب**: ابزار کامل استخراج HTML، CSS، JavaScript، تصاویر و فونت‌ها
- **CLI Tool**: ابزار خط فرمان با سه دستور اصلی (extract, analyze, build)
- **ویرایشگر بصری**: رابط کاربری drag & drop با GrapesJS
- **پشتیبانی فارسی**: رابط کاربری کاملاً فارسی با RTL
- **Docker Support**: پشتیبانی کامل Docker و Docker Compose
- **CI/CD Pipeline**: GitHub Actions برای تست و build خودکار

#### 🔧 بهبودها
- **امنیت**: تنظیمات امنیتی production-ready
- **مستندات**: README کامل و راهنماهای نصب
- **تست‌ها**: تست‌های پایه Python و JavaScript
- **ساختار**: معماری ماژولار و تمیز

#### 📦 فایل‌های اضافه شده
- `sitebuilder-cli.py` - ابزار خط فرمان
- `setup.py` - فایل نصب pip
- `SCRAPING_POLICY.md` - سیاست حقوقی استخراج
- `demo.html` - دمو زنده
- `frontend/rtl-components.html` - کامپوننت‌های RTL فارسی
- `tests/test_basic.py` - تست‌های Python
- `tests/test_basic.test.js` - تست‌های JavaScript
- `.github/workflows/ci.yml` - GitHub Actions workflow

#### 🐛 رفع باگ‌ها
- رفع خطاهای CI/CD pipeline
- بهبود error handling در extractor
- رفع مشکلات Docker build

#### 📚 مستندات
- README کامل با راهنمای نصب
- راهنمای استفاده از CLI
- سیاست حقوقی استخراج
- راهنمای مشارکت

#### 🔒 امنیت
- تنظیمات environment variables
- امنیت production-ready
- بررسی وابستگی‌های ناامن
- احترام به robots.txt

---

## [Unreleased]

### 🚀 برنامه‌های آینده
- انتشار در PyPI
- دمو آنلاین
- کامپوننت‌های بیشتر
- پشتیبانی از CMS ها
- API RESTful
- پنل مدیریت وب

---

## 📋 انواع تغییرات

- **✨ ویژگی جدید**: قابلیت جدید اضافه شده
- **🔧 بهبود**: بهبود در قابلیت موجود
- **🐛 رفع باگ**: رفع مشکل
- **📚 مستندات**: تغییر در مستندات
- **🔒 امنیت**: بهبود امنیت
- **📦 فایل**: اضافه/حذف فایل
- **🚀 انتشار**: انتشار جدید
