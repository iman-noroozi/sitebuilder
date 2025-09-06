# 🚀 راهنمای کامل نصب و استفاده - سایت بیلدر

## 📋 فهرست مطالب
- [نصب و راه‌اندازی](#نصب-و-راهاندازی)
- [استفاده از استخراج‌کننده](#استفاده-از-استخراجکننده)
- [استفاده از ویرایشگر](#استفاده-از-ویرایشگر)
- [ساخت سایت نهایی](#ساخت-سایت-نهایی)
- [انتشار خودکار](#انتشار-خودکار)
- [عیب‌یابی](#عیبیابی)

---

## 🛠️ نصب و راه‌اندازی

### پیش‌نیازها
- **Node.js** (نسخه 16 یا بالاتر)
- **Python** (نسخه 3.8 یا بالاتر)
- **Git** (برای کلون کردن پروژه)

### مرحله 1: کلون کردن پروژه
```bash
git clone https://github.com/yourusername/sitebuilder.git
cd sitebuilder
```

### مرحله 2: نصب وابستگی‌های Node.js
```bash
npm install
```

### مرحله 3: نصب وابستگی‌های Python
```bash
pip install -r requirements.txt
```

### مرحله 4: نصب spaCy (برای NLP)
```bash
pip install spacy
python -m spacy download xx_ent_wiki_sm
```

### مرحله 5: تست نصب
```bash
# تست استخراج‌کننده
node test/test.js

# تست ویرایشگر
python -m http.server 8000
# سپس در مرورگر: http://localhost:8000/editor/
```

---

## 🔍 استفاده از استخراج‌کننده

### استخراج تک سایت
```javascript
const TemplateExtractor = require('./extractor/puppeteer.js');

const extractor = new TemplateExtractor({
    headless: false,           // مشاهده فرآیند
    downloadAssets: true,      // دانلود فایل‌ها
    extractImages: true,       // دانلود تصاویر
    extractFonts: true,        // دانلود فونت‌ها
    timeout: 45000            // تایم‌اوت (میلی‌ثانیه)
});

// استخراج سایت
extractor.extractTemplate('https://example.com', './output')
    .then(() => console.log('✅ استخراج کامل شد'))
    .catch(err => console.error('❌ خطا:', err));
```

### استخراج چند سایت همزمان
```javascript
const urls = [
    'https://site1.com',
    'https://site2.com',
    'https://site3.com'
];

extractor.extractMultiplePages(urls, './outputs')
    .then(results => {
        console.log('✅ همه سایت‌ها استخراج شدند');
        console.log('نتایج:', results);
    });
```

### از خط فرمان
```bash
# استخراج تک سایت
node extractor/puppeteer.js https://example.com ./output

# تست ابزار
node test/test.js single https://getbootstrap.com
node test/test.js multi
```

---

## 🎨 استفاده از ویرایشگر

### راه‌اندازی ویرایشگر
1. فایل `editor/index.html` را در مرورگر باز کنید
2. یا از سرور محلی استفاده کنید:
```bash
python -m http.server 8000
# سپس: http://localhost:8000/editor/
```

### کامپوننت‌های فارسی موجود
- **هدر فارسی** - منوی ناوبری کامل
- **بخش قهرمان** - Hero section با دکمه CTA
- **بخش خدمات** - کارت‌های خدمات با آیکون
- **فرم تماس** - فرم تماس کامل
- **فوتر فارسی** - فوتر با اطلاعات تماس

### نحوه استفاده
1. کامپوننت مورد نظر را از پنل سمت چپ انتخاب کنید
2. روی کامپوننت کلیک کنید تا به صفحه اضافه شود
3. کامپوننت را در صفحه جابجا کنید
4. روی کامپوننت کلیک کنید تا ویرایش کنید
5. از پنل سمت راست استایل‌ها را تغییر دهید

### ذخیره و بارگذاری
- **ذخیره قالب**: روی دکمه "ذخیره قالب" کلیک کنید
- **بارگذاری قالب**: روی دکمه "بارگذاری قالب" کلیک کنید
- **انتشار سایت**: روی دکمه "انتشار سایت" کلیک کنید

---

## 🏗️ ساخت سایت نهایی

### استفاده از موتور ساخت
```python
from builder_core.build_engine import SiteBuilder

builder = SiteBuilder()

# تنظیمات سایت
site_config = {
    'site_name': 'سایت من',
    'domain': 'https://mysite.com',
    'description': 'سایت شخصی من',
    'keywords': 'وب، طراحی، توسعه',
    'text_replacements': {
        'عنوان قدیمی': 'عنوان جدید',
        'متن قدیمی': 'متن جدید'
    },
    'generate_pwa': True,      # تولید PWA
    'auto_seo': True          # SEO خودکار
}

# ساخت سایت
site_path = builder.build_site_from_template(
    './extracted_sites/bootstrap_template',
    site_config
)

# فشرده کردن برای دانلود
zip_path = builder.compress_site(site_path)
print(f"سایت آماده: {zip_path}")
```

### ویژگی‌های خودکار
- ✅ **PWA** - Progressive Web App
- ✅ **SEO** - بهینه‌سازی موتور جستجو
- ✅ **Responsive** - واکنش‌گرا
- ✅ **Optimized** - بهینه‌سازی شده
- ✅ **Compressed** - فشرده شده

---

## 🚀 انتشار خودکار

### انتشار به GitHub Pages
```python
# نیاز به GitHub Token
github_config = {
    'repo_name': 'my-website',
    'token': 'your_github_token_here'
}

success = builder.deploy_to_github_pages(
    site_path,
    github_config['repo_name'],
    github_config['token']
)
```

### انتشار به Netlify
```python
# نیاز به Netlify Token
netlify_config = {
    'site_name': 'my-website',
    'token': 'your_netlify_token_here'
}

success = builder.deploy_to_netlify(
    site_path,
    netlify_config['site_name'],
    netlify_config['token']
)
```

### انتشار به FTP
```python
ftp_config = {
    'host': 'ftp.example.com',
    'username': 'your_username',
    'password': 'your_password',
    'remote_path': '/public_html/',
    'port': 21
}

success = builder.deploy_to_ftp(site_path, ftp_config)
```

---

## 🔧 عیب‌یابی

### مشکلات رایج

#### 1. خطای "Navigation timeout"
```javascript
// افزایش timeout
const extractor = new TemplateExtractor({ 
    timeout: 60000  // 60 ثانیه
});
```

#### 2. مشکل در دانلود تصاویر
```javascript
// بررسی مسیرهای نسبی
const baseURL = new URL(url).origin;
const fullImageUrl = imgUrl.startsWith('http') 
    ? imgUrl 
    : new URL(imgUrl, baseURL).href;
```

#### 3. خطای CORS در مرورگر
```javascript
// غیرفعال کردن web security
const extractor = new TemplateExtractor({
    puppeteerArgs: ['--disable-web-security']
});
```

#### 4. مشکل در ویرایشگر
- مرورگر را refresh کنید
- کش مرورگر را پاک کنید
- از مرورگر Chrome استفاده کنید

#### 5. خطای Python
```bash
# نصب مجدد وابستگی‌ها
pip install --upgrade -r requirements.txt

# بررسی نسخه Python
python --version  # باید 3.8+ باشد
```

### لاگ‌ها و دیباگ
```bash
# مشاهده لاگ‌های استخراج
tail -f extraction.log

# تست عملکرد
node test/test.js debug

# بررسی فایل‌های تولید شده
ls -la extracted_sites/
ls -la built_sites/
```

---

## 📊 آمار و عملکرد

### سرعت استخراج
- **سایت کوچک**: 15-30 ثانیه
- **سایت متوسط**: 30-60 ثانیه  
- **سایت بزرگ**: 60-120 ثانیه

### حجم فایل‌ها
- **قالب کوچک**: 1-5MB
- **قالب متوسط**: 5-15MB
- **قالب بزرگ**: 15-50MB

### قابلیت‌های پشتیبانی شده
- ✅ HTML5 کامل
- ✅ CSS3 + Flexbox/Grid
- ✅ JavaScript ES6+
- ✅ تصاویر (PNG, JPG, SVG, WebP)
- ✅ فونت‌ها (WOFF, WOFF2, TTF)
- ✅ ویدیو و صوت
- ✅ فایل‌های PDF

---

## 🎯 مثال‌های عملی

### مثال 1: ساخت سایت شخصی
```python
site_config = {
    'site_name': 'احمد محمدی - توسعه‌دهنده وب',
    'domain': 'https://ahmad-mohammadi.ir',
    'description': 'توسعه‌دهنده وب و طراح UI/UX',
    'text_replacements': {
        'John Doe': 'احمد محمدی',
        'Web Developer': 'توسعه‌دهنده وب',
        'john@example.com': 'ahmad@example.com'
    }
}
```

### مثال 2: ساخت سایت شرکتی
```python
site_config = {
    'site_name': 'شرکت فناوری پیشرو',
    'domain': 'https://pishro-tech.com',
    'description': 'شرکت پیشرو در زمینه توسعه نرم‌افزار',
    'text_replacements': {
        'Company Name': 'شرکت فناوری پیشرو',
        'info@company.com': 'info@pishro-tech.com'
    }
}
```

### مثال 3: ساخت فروشگاه آنلاین
```python
site_config = {
    'site_name': 'فروشگاه آنلاین',
    'domain': 'https://shop.example.com',
    'description': 'فروشگاه آنلاین با بهترین قیمت‌ها',
    'generate_pwa': True,
    'auto_seo': True
}
```

---

## 📞 پشتیبانی

### منابع کمک
- 📖 [مستندات کامل](https://github.com/yourusername/sitebuilder/docs)
- 🐛 [گزارش باگ](https://github.com/yourusername/sitebuilder/issues)
- 💬 [سوالات](https://github.com/yourusername/sitebuilder/discussions)
- 📧 [ایمیل پشتیبانی](mailto:support@example.com)

### جامعه کاربران
- 📱 [تلگرام](https://t.me/sitebuilder_ir)
- 🐦 [توییتر](https://twitter.com/sitebuilder_ir)
- 📘 [اینستاگرام](https://instagram.com/sitebuilder_ir)

---

**ساخته شده با ❤️ برای جامعه توسعه‌دهندگان ایرانی**

*آخرین بروزرسانی: 2024* 