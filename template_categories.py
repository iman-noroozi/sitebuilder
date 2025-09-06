#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📂 دسته‌بندی قالب‌ها بر اساس نوع کسب‌وکار
"""

import json
from pathlib import Path

# دسته‌بندی کامل قالب‌ها
TEMPLATE_CATEGORIES = {
    "portfolio_creative": {
        "title": "نمونه‌کار و خلاقیت",
        "description": "قالب‌های مناسب برای طراحان، عکاسان و هنرمندان",
        "templates": [
            "dribbble_com",
            "behance_net", 
            "awwwards_com",
            "onepagelove_com",
            "uidesigndaily_com"
        ],
        "features": ["گالری تصاویر", "انیمیشن‌های نرم", "طراحی مینیمال"],
        "suitable_for": ["طراحان گرافیک", "عکاسان", "هنرمندان", "آژانس‌های تبلیغاتی"],
        "colors": ["dark", "minimal", "creative"]
    },
    
    "business_corporate": {
        "title": "کسب‌وکار و شرکتی",
        "description": "قالب‌های حرفه‌ای برای شرکت‌ها و کسب‌وکارها",
        "templates": [
            "getbootstrap_com",
            "tailwindcss_com",
            "chakra_ui_com"
        ],
        "features": ["فرم تماس", "بخش درباره ما", "صفحه خدمات"],
        "suitable_for": ["شرکت‌های تجاری", "استارتاپ‌ها", "موسسات", "کنسرن‌ها"],
        "colors": ["blue", "professional", "clean"]
    },
    
    "ecommerce_shop": {
        "title": "فروشگاه و تجارت الکترونیک",
        "description": "قالب‌های مناسب برای فروشگاه‌های آنلاین",
        "templates": [
            "shopify_templates",
            "woocommerce_themes"
        ],
        "features": ["سبد خرید", "صفحه محصول", "فیلتر جستجو"],
        "suitable_for": ["فروشگاه‌های آنلاین", "برندها", "تولیدکنندگان"],
        "colors": ["orange", "green", "trust"]
    },
    
    "blog_magazine": {
        "title": "بلاگ و مجله",
        "description": "قالب‌های مناسب برای وبلاگ‌ها و مجلات آنلاین",
        "templates": [
            "medium_inspired",
            "news_templates"
        ],
        "features": ["سیستم مقالات", "دسته‌بندی", "جستجو"],
        "suitable_for": ["بلاگرها", "نویسندگان", "مجلات آنلاین"],
        "colors": ["clean", "readable", "modern"]
    },
    
    "landing_page": {
        "title": "صفحه فرود",
        "description": "قالب‌های تک‌صفحه‌ای برای کمپین‌ها",
        "templates": [
            "landingfolio_com",
            "onepagelove_com"
        ],
        "features": ["CTA قوی", "فرم ثبت‌نام", "شمارنده"],
        "suitable_for": ["کمپین‌های تبلیغاتی", "محصولات جدید", "رویدادها"],
        "colors": ["conversion", "bright", "action"]
    },
    
    "restaurant_food": {
        "title": "رستوران و غذا",
        "description": "قالب‌های مخصوص رستوران‌ها و کافه‌ها",
        "templates": [
            "restaurant_themes"
        ],
        "features": ["منوی غذا", "رزرو آنلاین", "گالری غذا"],
        "suitable_for": ["رستوران‌ها", "کافه‌ها", "فست‌فودها"],
        "colors": ["warm", "appetizing", "cozy"]
    },
    
    "health_medical": {
        "title": "پزشکی و سلامت",
        "description": "قالب‌های مناسب برای حوزه پزشکی",
        "templates": [
            "medical_templates"
        ],
        "features": ["نوبت‌دهی آنلاین", "معرفی پزشکان", "مقالات پزشکی"],
        "suitable_for": ["کلینیک‌ها", "بیمارستان‌ها", "دندانپزشکان"],
        "colors": ["blue", "clean", "trustworthy"]
    },
    
    "education_learning": {
        "title": "آموزش و یادگیری",
        "description": "قالب‌های آموزشی و دانشگاهی",
        "templates": [
            "education_themes"
        ],
        "features": ["دوره‌های آنلاین", "تقویم کلاس‌ها", "پروفایل اساتید"],
        "suitable_for": ["مدارس", "دانشگاه‌ها", "مراکز آموزشی"],
        "colors": ["green", "knowledge", "inspiring"]
    },
    
    "technology_saas": {
        "title": "تکنولوژی و نرم‌افزار",
        "description": "قالب‌های مناسب برای شرکت‌های فناوری",
        "templates": [
            "mui_com",
            "ant_design",
            "mantine_dev"
        ],
        "features": ["داشبورد کاربری", "API documentation", "پنل مدیریت"],
        "suitable_for": ["استارتاپ‌های فناوری", "شرکت‌های نرم‌افزاری", "سرویس‌های SaaS"],
        "colors": ["tech", "modern", "innovative"]
    },
    
    "real_estate": {
        "title": "املاک و مستغلات",
        "description": "قالب‌های مخصوص آژانس‌های املاک",
        "templates": [
            "real_estate_themes"
        ],
        "features": ["جستجوی ملک", "نقشه", "فیلتر قیمت"],
        "suitable_for": ["آژانس‌های املاک", "سازندگان", "مشاوران املاک"],
        "colors": ["professional", "luxurious", "trustworthy"]
    }
}

def generate_category_file():
    """تولید فایل دسته‌بندی"""
    output_path = Path("extraction_module/template_categories.json")
    
    # اضافه کردن اطلاعات کلی
    category_data = {
        "metadata": {
            "title": "دسته‌بندی قالب‌های سایت‌ساز",
            "description": "دسته‌بندی کامل قالب‌ها بر اساس نوع کسب‌وکار",
            "total_categories": len(TEMPLATE_CATEGORIES),
            "created_at": "2024",
            "language": "fa"
        },
        "categories": TEMPLATE_CATEGORIES
    }
    
    # ذخیره فایل
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(category_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ فایل دسته‌بندی ایجاد شد: {output_path}")
    return output_path

def create_template_guide():
    """ایجاد راهنمای انتخاب قالب"""
    guide_content = """# 🎯 راهنمای انتخاب قالب مناسب

## سوالات کلیدی برای انتخاب قالب:

### 1️⃣ نوع کسب‌وکار شما چیست؟
- **خلاقیت و هنر**: Portfolio Creative
- **شرکت و تجارت**: Business Corporate  
- **فروشگاه**: E-commerce Shop
- **آموزش**: Education Learning
- **پزشکی**: Health Medical
- **رستوران**: Restaurant Food
- **املاک**: Real Estate
- **تکنولوژی**: Technology SaaS

### 2️⃣ هدف اصلی سایت چیست؟
- **نمایش نمونه‌کار**: قالب‌های Portfolio
- **فروش محصول**: قالب‌های E-commerce
- **جذب مشتری**: قالب‌های Landing Page
- **اطلاع‌رسانی**: قالب‌های Blog/Magazine

### 3️⃣ مخاطب هدف شما کیست؟
- **جوانان**: طراحی مدرن و رنگارنگ
- **حرفه‌ای**: طراحی کلاسیک و محتشم
- **خانواده‌ها**: طراحی گرم و صمیمی

### 4️⃣ ویژگی‌های مورد نیاز:
- فرم تماس ✅
- گالری تصاویر ✅  
- فروشگاه آنلاین ✅
- بلاگ ✅
- چندزبانه ✅

## 🎨 راهنمای رنگ‌ها:

- **آبی**: اعتماد، حرفه‌ای (پزشکی، تجاری)
- **سبز**: رشد، طبیعت (آموزش، محیط‌زیست)
- **نارنجی**: انرژی، خلاقیت (هنری، ورزشی)
- **قرمز**: قدرت، عجله (فروش، اورژانسی)
- **خاکستری**: مدرن، مینیمال (تکنولوژی)

## 🚀 نکات بهینه‌سازی:

1. **سرعت بارگذاری**: قالب‌های سبک انتخاب کنید
2. **واکنش‌گرایی**: حتماً Mobile-Friendly باشد
3. **SEO**: متادیتا و ساختار مناسب داشته باشد
4. **قابلیت سفارشی‌سازی**: آسان ویرایش شود

*برای مشاوره در انتخاب قالب، با تیم پشتیبانی تماس بگیرید.*
"""
    
    guide_path = Path("extraction_module/TEMPLATE_SELECTION_GUIDE.md")
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ راهنمای انتخاب قالب ایجاد شد: {guide_path}")

if __name__ == "__main__":
    print("📂 ایجاد سیستم دسته‌بندی قالب‌ها...")
    
    # تولید فایل‌ها
    generate_category_file()
    create_template_guide()
    
    print("\n🎉 سیستم دسته‌بندی آماده شد!")
    print("📁 فایل‌ها:")
    print("  - template_categories.json")
    print("  - TEMPLATE_SELECTION_GUIDE.md")