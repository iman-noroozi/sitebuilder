#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏢 کاتالوگ کامل خدمات کسب‌وکاری
تمام خدماتی که می‌تونیم به کسب‌وکارهای کوچک ارائه بدیم
"""

import json
from datetime import datetime

# کاتالوگ کامل خدمات
BUSINESS_SERVICES_CATALOG = {
    "digital_presence": {
        "title": "🌐 حضور دیجیتال",
        "icon": "🌐",
        "services": {
            "website_builder": {
                "title": "ساخت سایت حرفه‌ای",
                "description": "طراحی و ساخت سایت با ادیتور کشیدنی",
                "features": ["ادیتور GrapesJS", "قالب‌های آماده", "طراحی ریسپانسیو", "سئوی خودکار"],
                "price_range": "500,000 - 2,000,000 تومان",
                "implementation": "موجود",
                "priority": "بالا"
            },
            "domain_hosting": {
                "title": "دامنه و هاستینگ",
                "description": "ثبت دامنه و ارائه هاستینگ سریع",
                "features": ["دامنه .ir", "SSL رایگان", "پشتیبان‌گیری", "CDN ایرانی"],
                "price_range": "200,000 - 500,000 تومان سالانه",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "seo_optimization": {
                "title": "بهینه‌سازی سئو",
                "description": "رتبه‌بندی بهتر در گوگل",
                "features": ["کلمات کلیدی", "محتوای بهینه", "sitemap", "robots.txt"],
                "price_range": "300,000 - 800,000 تومان",
                "implementation": "موجود",
                "priority": "متوسط"
            },
            "social_media": {
                "title": "مدیریت شبکه‌های اجتماعی",
                "description": "اتوماسیون پست‌ها و تعامل",
                "features": ["اتوپست", "آنالیز", "پاسخ خودکار", "کمپین"],
                "price_range": "400,000 - 1,000,000 تومان ماهانه",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            }
        }
    },
    
    "e_commerce": {
        "title": "🛒 فروش آنلاین",
        "icon": "🛒",
        "services": {
            "online_store": {
                "title": "فروشگاه آنلاین",
                "description": "فروش محصولات و خدمات",
                "features": ["کاتالوگ محصولات", "سبد خرید", "مدیریت سفارش", "تخفیف و کوپن"],
                "price_range": "800,000 - 3,000,000 تومان",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "inventory_management": {
                "title": "مدیریت موجودی",
                "description": "کنترل انبار و موجودی",
                "features": ["ورود/خروج کالا", "هشدار موجودی", "گزارش‌گیری", "بارکد"],
                "price_range": "600,000 - 1,500,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "بالا"
            },
            "marketplace_integration": {
                "title": "اتصال به مارکت‌پلیس‌ها",
                "description": "فروش در دیجی‌کالا، بامیلو و...",
                "features": ["sync محصولات", "مدیریت سفارش", "قیمت‌گذاری", "گزارش فروش"],
                "price_range": "500,000 - 1,200,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            }
        }
    },
    
    "financial_management": {
        "title": "💰 مدیریت مالی",
        "icon": "💰",
        "services": {
            "accounting_system": {
                "title": "سیستم حسابداری",
                "description": "حسابداری کامل طبق استاندارد",
                "features": ["دفتر روزنامه", "ترازنامه", "سود و زیان", "مالیات"],
                "price_range": "700,000 - 2,000,000 تومان",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "invoice_system": {
                "title": "سیستم فاکتور",
                "description": "صدور فاکتور رسمی و غیررسمی",
                "features": ["فاکتور رسمی", "فاکتور پیش‌فرم", "مالیات", "تخفیف"],
                "price_range": "400,000 - 1,000,000 تومان",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "payment_gateway": {
                "title": "درگاه پرداخت",
                "description": "پرداخت آنلاین امن",
                "features": ["پارسیان", "پاسارگاد", "ملت", "واسط پرداخت"],
                "price_range": "0.5% - 2% کارمزد",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "expense_tracking": {
                "title": "مدیریت هزینه‌ها",
                "description": "ثبت و کنترل هزینه‌های کسب‌وکار",
                "features": ["ثبت هزینه", "دسته‌بندی", "گزارش ماهانه", "بودجه‌بندی"],
                "price_range": "300,000 - 700,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            },
            "commission_management": {
                "title": "مدیریت پورسانت",
                "description": "محاسبه و پرداخت پورسانت",
                "features": ["درصد پورسانت", "پرداخت خودکار", "گزارش فروشنده", "سطح‌بندی"],
                "price_range": "500,000 - 1,200,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            }
        }
    },
    
    "communication": {
        "title": "📱 ارتباطات",
        "icon": "📱",
        "services": {
            "sms_service": {
                "title": "سرویس پیامک",
                "description": "ارسال پیامک انبوه و تبلیغاتی",
                "features": ["پیامک تبلیغاتی", "OTP", "پیامک سفارش", "پنل کاربری"],
                "price_range": "50 - 200 تومان هر پیامک",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "whatsapp_business": {
                "title": "واتساپ بیزنس",
                "description": "پیام‌رسانی تجاری واتساپ",
                "features": ["API واتساپ", "چت‌بات", "کاتالوگ", "پیام خودکار"],
                "price_range": "0.05 - 0.1 دلار هر پیام",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            },
            "email_marketing": {
                "title": "ایمیل مارکتینگ",
                "description": "کمپین‌های ایمیلی",
                "features": ["خبرنامه", "ایمیل خودکار", "آنالیز", "قالب آماده"],
                "price_range": "200,000 - 600,000 تومان ماهانه",
                "implementation": "نیاز به توسعه",
                "priority": "پایین"
            },
            "crm_system": {
                "title": "مدیریت مشتری (CRM)",
                "description": "پیگیری و مدیریت مشتریان",
                "features": ["پروفایل مشتری", "تاریخچه خرید", "یادآوری", "پیگیری"],
                "price_range": "600,000 - 1,800,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            }
        }
    },
    
    "booking_reservation": {
        "title": "📅 رزرو و نوبت‌دهی",
        "icon": "📅",
        "services": {
            "appointment_booking": {
                "title": "سیستم رزرو نوبت",
                "description": "رزرو آنلاین برای خدمات",
                "features": ["تقویم آنلاین", "تأیید خودکار", "یادآوری SMS", "کنسلی"],
                "price_range": "500,000 - 1,500,000 تومان",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "resource_management": {
                "title": "مدیریت منابع",
                "description": "مدیریت اتاق، میز، تجهیزات",
                "features": ["رزرو منابع", "تقویم منابع", "تداخل زمانی", "گزارش استفاده"],
                "price_range": "700,000 - 2,000,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            },
            "queue_management": {
                "title": "مدیریت صف",
                "description": "سیستم نوبت‌دهی دیجیتال",
                "features": ["شماره نوبت", "تخمین زمان", "اطلاع‌رسانی", "آمار انتظار"],
                "price_range": "800,000 - 2,500,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            }
        }
    },
    
    "analytics_reporting": {
        "title": "📊 آنالیز و گزارش",
        "icon": "📊",
        "services": {
            "business_intelligence": {
                "title": "هوش تجاری",
                "description": "آنالیز داده‌ها و گزارش‌های مدیریتی",
                "features": ["داشبورد", "نمودارها", "KPI", "پیش‌بینی"],
                "price_range": "800,000 - 2,500,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            },
            "sales_analytics": {
                "title": "آنالیز فروش",
                "description": "تحلیل عملکرد فروش",
                "features": ["ترند فروش", "محصولات پرفروش", "فصلی‌بودن", "مقایسه"],
                "price_range": "500,000 - 1,200,000 تومان",
                "implementation": "آماده توسعه",
                "priority": "متوسط"
            },
            "customer_analytics": {
                "title": "آنالیز مشتری",
                "description": "رفتار و الگوی خرید مشتریان",
                "features": ["RFM Analysis", "CLV", "Churn", "Segmentation"],
                "price_range": "600,000 - 1,500,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "پایین"
            }
        }
    },
    
    "location_services": {
        "title": "🗺️ خدمات مکانی",
        "icon": "🗺️",
        "services": {
            "google_business": {
                "title": "ثبت در گوگل مپ",
                "description": "ثبت و بهینه‌سازی کسب‌وکار در گوگل",
                "features": ["تأیید کسب‌وکار", "عکس و ویدیو", "نظرات", "پست‌ها"],
                "price_range": "300,000 - 800,000 تومان",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "delivery_system": {
                "title": "سیستم تحویل",
                "description": "مدیریت سفارش و تحویل",
                "features": ["پیک آنلاین", "ردیابی", "محاسبه هزینه", "زمان‌بندی"],
                "price_range": "1,000,000 - 3,000,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            },
            "location_marketing": {
                "title": "مارکتینگ مکانی",
                "description": "تبلیغات بر اساس موقعیت",
                "features": ["تبلیغ محلی", "جئوفنسینگ", "مشتریان اطراف", "رقابت محلی"],
                "price_range": "400,000 - 1,000,000 تومان ماهانه",
                "implementation": "نیاز به توسعه",
                "priority": "پایین"
            }
        }
    },
    
    "automation": {
        "title": "🤖 اتوماسیون",
        "icon": "🤖",
        "services": {
            "workflow_automation": {
                "title": "اتوماسیون فرآیندها",
                "description": "خودکارسازی کارهای تکراری",
                "features": ["Workflow Designer", "شرایط", "اعمال خودکار", "گزارش"],
                "price_range": "800,000 - 2,000,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            },
            "chatbot": {
                "title": "ربات گفتگو",
                "description": "پاسخ خودکار به سؤالات",
                "features": ["AI پاسخگو", "سؤالات متداول", "انتقال به انسان", "آموزش"],
                "price_range": "600,000 - 1,500,000 تومان",
                "implementation": "آماده توسعه",
                "priority": "متوسط"
            },
            "automated_marketing": {
                "title": "مارکتینگ خودکار",
                "description": "کمپین‌های خودکار",
                "features": ["ایمیل خودکار", "پیامک برنامه‌ای", "پیگیری مشتری", "cross-sell"],
                "price_range": "700,000 - 1,800,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "پایین"
            }
        }
    },
    
    "security_compliance": {
        "title": "🔒 امنیت و قانونی",
        "icon": "🔒",
        "services": {
            "ssl_security": {
                "title": "گواهی امنیت SSL",
                "description": "رمزنگاری و امنیت سایت",
                "features": ["SSL Certificate", "HTTPs", "امنیت داده", "تأیید هویت"],
                "price_range": "200,000 - 500,000 تومان سالانه",
                "implementation": "موجود",
                "priority": "بالا"
            },
            "backup_system": {
                "title": "پشتیبان‌گیری",
                "description": "بکاپ خودکار اطلاعات",
                "features": ["بکاپ روزانه", "بازیابی", "ذخیره ابری", "نسخه‌بندی"],
                "price_range": "150,000 - 400,000 تومان ماهانه",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "gdpr_compliance": {
                "title": "قوانین حریم خصوصی",
                "description": "تطبیق با قوانین داده",
                "features": ["رضایت کاربر", "حذف داده", "گزارش نقض", "سیاست حریم"],
                "price_range": "300,000 - 700,000 تومان",
                "implementation": "نیاز به توسعه",
                "priority": "متوسط"
            }
        }
    },
    
    "training_support": {
        "title": "🎓 آموزش و پشتیبانی",
        "icon": "🎓",
        "services": {
            "staff_training": {
                "title": "آموزش کارکنان",
                "description": "آموزش استفاده از سیستم",
                "features": ["ویدیوهای آموزشی", "وبینار", "آموزش حضوری", "گواهینامه"],
                "price_range": "200,000 - 800,000 تومان",
                "implementation": "آماده توسعه",
                "priority": "متوسط"
            },
            "technical_support": {
                "title": "پشتیبانی فنی",
                "description": "پشتیبانی 24/7",
                "features": ["تیکت", "چت آنلاین", "تماس تلفنی", "راه‌حل از راه دور"],
                "price_range": "100,000 - 500,000 تومان ماهانه",
                "implementation": "آماده توسعه",
                "priority": "بالا"
            },
            "business_consulting": {
                "title": "مشاوره کسب‌وکار",
                "description": "مشاوره رشد و بهبود",
                "features": ["تحلیل کسب‌وکار", "استراتژی", "بهینه‌سازی", "راهکار"],
                "price_range": "500,000 - 2,000,000 تومان",
                "implementation": "آماده ارائه",
                "priority": "متوسط"
            }
        }
    }
}

def generate_services_summary():
    """تولید خلاصه خدمات"""
    total_services = 0
    categories = len(BUSINESS_SERVICES_CATALOG)
    
    by_priority = {"بالا": 0, "متوسط": 0, "پایین": 0}
    by_implementation = {"موجود": 0, "آماده توسعه": 0, "نیاز به توسعه": 0, "آماده ارائه": 0}
    
    for category_data in BUSINESS_SERVICES_CATALOG.values():
        for service_data in category_data["services"].values():
            total_services += 1
            by_priority[service_data["priority"]] += 1
            by_implementation[service_data["implementation"]] += 1
    
    return {
        "total_categories": categories,
        "total_services": total_services,
        "by_priority": by_priority,
        "by_implementation": by_implementation,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    """ایجاد فایل‌های کاتالوگ خدمات"""
    
    # ذخیره کاتالوگ کامل
    with open("business_services_complete.json", 'w', encoding='utf-8') as f:
        json.dump(BUSINESS_SERVICES_CATALOG, f, ensure_ascii=False, indent=2)
    
    # تولید خلاصه
    summary = generate_services_summary()
    
    # ذخیره خلاصه
    with open("business_services_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # تولید راهنمای انتخاب خدمات
    guide_content = f"""# 🏢 راهنمای انتخاب خدمات کسب‌وکاری

## 📊 خلاصه آمار
- **تعداد دسته‌ها:** {summary['total_categories']} دسته
- **تعداد خدمات:** {summary['total_services']} خدمت

### اولویت خدمات:
- **بالا:** {summary['by_priority']['بالا']} خدمت
- **متوسط:** {summary['by_priority']['متوسط']} خدمت  
- **پایین:** {summary['by_priority']['پایین']} خدمت

### وضعیت توسعه:
- **موجود:** {summary['by_implementation']['موجود']} خدمت
- **آماده توسعه:** {summary['by_implementation']['آماده توسعه']} خدمت
- **نیاز به توسعه:** {summary['by_implementation']['نیاز به توسعه']} خدمت
- **آماده ارائه:** {summary['by_implementation']['آماده ارائه']} خدمت

## 🎯 پیشنهاد مراحل توسعه

### مرحله اول (خدمات پایه):
"""
    
    # اضافه کردن پیشنهادات بر اساس اولویت
    for category_key, category_data in BUSINESS_SERVICES_CATALOG.items():
        guide_content += f"\n### {category_data['title']}\n"
        
        high_priority = []
        medium_priority = []
        
        for service_key, service_data in category_data["services"].items():
            if service_data["priority"] == "بالا":
                high_priority.append(f"- **{service_data['title']}** - {service_data['description']}")
            elif service_data["priority"] == "متوسط":
                medium_priority.append(f"- **{service_data['title']}** - {service_data['description']}")
        
        if high_priority:
            guide_content += "#### اولویت بالا:\n" + "\n".join(high_priority) + "\n"
        if medium_priority:
            guide_content += "#### اولویت متوسط:\n" + "\n".join(medium_priority) + "\n"
    
    guide_content += f"""
---
*تولید شده در {summary['generated_at']}*
"""
    
    with open("BUSINESS_SERVICES_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("🎉 کاتالوگ خدمات کامل شد!")
    print(f"📊 {summary['total_services']} خدمت در {summary['total_categories']} دسته")
    print("📁 فایل‌ها:")
    print("  - business_services_complete.json")
    print("  - business_services_summary.json") 
    print("  - BUSINESS_SERVICES_GUIDE.md")

if __name__ == "__main__":
    main()