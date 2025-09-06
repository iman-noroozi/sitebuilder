#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏢 کاتالوگ کامل خدمات کسب‌وکاری
همه خدماتی که می‌تونیم به کسب‌وکارهای کوچک ایرانی ارائه بدیم
"""

import json
from datetime import datetime

# کاتالوگ کامل خدمات کسب‌وکاری
COMPLETE_SERVICES_CATALOG = {
    "website_infrastructure": {
        "title": "🚀 راه‌اندازی سایت و زیرساخت فروش",
        "icon": "🚀",
        "services": {
            "website_design": {
                "title": "طراحی سایت اختصاصی",
                "description": "طراحی سایت با ظاهر منحصربه‌فرد برای کسب‌وکار شما",
                "features": [
                    "طراحی ریسپانسیو (موبایل + دسکتاپ)",
                    "ظاهر اختصاصی مطابق برند",
                    "بهینه‌سازی سرعت بارگذاری",
                    "سئوی پیشرفته"
                ],
                "iranian_tools": ["ایران‌هاست", "آسیاتک", "پارس‌پک"],
                "international_tools": ["WordPress", "Elementor", "Webflow"],
                "price_range": "2,000,000 - 10,000,000 تومان",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "1-4 هفته"
            },
            "website_builder": {
                "title": "سایت‌ساز حرفه‌ای",
                "description": "پلتفرم سایت‌ساز با ادیتور کشیدنی GrapesJS",
                "features": [
                    "ادیتور بصری کشیدنی",
                    "قالب‌های آماده فارسی",
                    "پشتیبانی RTL کامل",
                    "بلوک‌های فارسی آماده"
                ],
                "iranian_tools": ["پلتفرم اختصاصی ما"],
                "international_tools": ["GrapesJS", "Bootstrap", "Tailwind"],
                "price_range": "500,000 - 2,000,000 تومان",
                "target_businesses": ["کسب‌وکارهای کوچک", "استارتاپ‌ها"],
                "implementation_time": "1-7 روز"
            },
            "ecommerce_setup": {
                "title": "راه‌اندازی فروشگاه آنلاین",
                "description": "سیستم کامل فروش آنلاین با تمام امکانات",
                "features": [
                    "سبد خرید پیشرفته",
                    "مدیریت محصولات",
                    "سیستم تخفیف و کوپن",
                    "پنل مدیریت کامل"
                ],
                "iranian_tools": ["ایدکالا", "دیجی‌استایل"],
                "international_tools": ["Shopify", "WooCommerce", "Magento"],
                "price_range": "3,000,000 - 15,000,000 تومان",
                "target_businesses": ["فروشگاه‌ها", "برندها", "تولیدکنندگان"],
                "implementation_time": "2-6 هفته"
            },
            "hosting_domain": {
                "title": "هاستینگ و دامنه",
                "description": "سرویس هاستینگ سریع و پایدار با دامنه",
                "features": [
                    "SSL رایگان",
                    "پشتیبان‌گیری خودکار",
                    "CDN ایرانی",
                    "پشتیبانی 24/7"
                ],
                "iranian_tools": ["ایران‌هاست", "آسیاتک", "پارس‌پک"],
                "international_tools": ["Cloudflare", "AWS", "DigitalOcean"],
                "price_range": "300,000 - 1,500,000 تومان سالانه",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "1-3 روز"
            }
        }
    },
    
    "payment_systems": {
        "title": "💳 سیستم‌های پرداخت حرفه‌ای",
        "icon": "💳",
        "services": {
            "payment_gateway_integration": {
                "title": "اتصال درگاه پرداخت",
                "description": "اتصال به بهترین درگاه‌های پرداخت ایرانی",
                "features": [
                    "پشتیبانی همه کارت‌های ایرانی",
                    "تراکنش امن با رمزنگاری",
                    "گزارش‌گیری تفصیلی",
                    "پیگیری خودکار پرداخت‌ها"
                ],
                "iranian_tools": ["زرین‌پال", "آیدی‌پی", "پارسیان", "پاسارگاد", "ملت"],
                "international_tools": ["Stripe", "PayPal", "Square"],
                "price_range": "500,000 - 1,500,000 تومان + کمیسیون",
                "target_businesses": ["فروشگاه آنلاین", "خدمات", "رستوران"],
                "implementation_time": "3-7 روز"
            },
            "multi_payment_gateway": {
                "title": "چندین درگاه پرداخت",
                "description": "امکان پرداخت از چندین درگاه برای اطمینان بیشتر",
                "features": [
                    "انتخاب خودکار درگاه بهینه",
                    "پشتیبان در صورت خرابی یک درگاه",
                    "بهترین نرخ کمیسیون",
                    "گزارش مقایسه‌ای درگاه‌ها"
                ],
                "iranian_tools": ["زرین‌پال + آیدی‌پی", "پارسیان + ملت"],
                "international_tools": ["Stripe + PayPal"],
                "price_range": "800,000 - 2,000,000 تومان",
                "target_businesses": ["فروشگاه‌های بزرگ", "استارتاپ‌ها"],
                "implementation_time": "1-2 هفته"
            },
            "installment_payment": {
                "title": "پرداخت اقساطی",
                "description": "امکان خرید اقساطی برای مشتریان",
                "features": [
                    "اقساط 3، 6، 12 ماهه",
                    "محاسبه خودکار اقساط",
                    "بررسی اعتبار مشتری",
                    "پیگیری اقساط"
                ],
                "iranian_tools": ["تپسی‌پی", "فن‌آوا"],
                "international_tools": ["Klarna", "Afterpay"],
                "price_range": "1,000,000 - 3,000,000 تومان",
                "target_businesses": ["فروشگاه‌های لوازم خانگی", "مد و پوشاک"],
                "implementation_time": "2-3 هفته"
            }
        }
    },
    
    "sms_communication": {
        "title": "📲 ارسال پیامک خودکار",
        "icon": "📲",
        "services": {
            "automated_sms": {
                "title": "پیامک خودکار فروش",
                "description": "ارسال پیامک در مراحل مختلف خرید و فروش",
                "features": [
                    "تأیید خرید و پرداخت",
                    "آپدیت وضعیت سفارش",
                    "یادآوری سبد خرید رهاشده",
                    "پیگیری رضایت مشتری"
                ],
                "iranian_tools": ["کاوه‌نگار", "مگفا", "آی‌پی‌پنل", "SMS.ir"],
                "international_tools": ["Twilio", "SendGrid"],
                "price_range": "300,000 - 800,000 تومان + هزینه پیامک",
                "target_businesses": ["فروشگاه آنلاین", "خدمات"],
                "implementation_time": "3-5 روز"
            },
            "marketing_sms": {
                "title": "پیامک بازاریابی",
                "description": "کمپین‌های پیامکی برای افزایش فروش",
                "features": [
                    "پیامک تولد و مناسبت‌ها",
                    "اطلاع‌رسانی تخفیف‌ها",
                    "معرفی محصولات جدید",
                    "پیامک وفاداری مشتری"
                ],
                "iranian_tools": ["کاوه‌نگار", "مگفا"],
                "international_tools": ["Mailchimp SMS", "Klaviyo"],
                "price_range": "500,000 - 1,200,000 تومان ماهانه",
                "target_businesses": ["فروشگاه", "رستوران", "زیبایی"],
                "implementation_time": "1 هفته"
            },
            "otp_verification": {
                "title": "تأیید هویت با OTP",
                "description": "احراز هویت مشتریان با کد یکبار مصرف",
                "features": [
                    "کد تأیید ثبت‌نام",
                    "تأیید شماره موبایل",
                    "ورود امن به حساب",
                    "تأیید تراکنش‌های مهم"
                ],
                "iranian_tools": ["کاوه‌نگار", "آی‌پی‌پنل"],
                "international_tools": ["Twilio Verify", "Firebase Auth"],
                "price_range": "200,000 - 600,000 تومان",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "2-3 روز"
            }
        }
    },
    
    "accounting_financial": {
        "title": "🧮 حسابداری و مدیریت مالی",
        "icon": "🧮",
        "services": {
            "accounting_integration": {
                "title": "اتصال نرم‌افزار حسابداری",
                "description": "ادغام کامل با سیستم‌های حسابداری ایرانی",
                "features": [
                    "ثبت خودکار فروش",
                    "صدور فاکتور رسمی",
                    "محاسبه مالیات",
                    "گزارش‌های مالی"
                ],
                "iranian_tools": ["سپیدار", "حسابفا", "هدهد"],
                "international_tools": ["QuickBooks", "Xero"],
                "price_range": "800,000 - 2,500,000 تومان",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "1-2 هفته"
            },
            "invoice_system": {
                "title": "سیستم فاکتور هوشمند",
                "description": "صدور خودکار فاکتور با طراحی حرفه‌ای",
                "features": [
                    "فاکتور رسمی و غیررسمی",
                    "طراحی اختصاصی فاکتور",
                    "ارسال خودکار به مشتری",
                    "پیگیری پرداخت فاکتور"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["FreshBooks", "Zoho Invoice"],
                "price_range": "500,000 - 1,500,000 تومان",
                "target_businesses": ["خدمات", "فروشگاه"],
                "implementation_time": "1 هفته"
            },
            "expense_management": {
                "title": "مدیریت هزینه‌ها",
                "description": "کنترل و بودجه‌بندی هزینه‌های کسب‌وکار",
                "features": [
                    "ثبت هزینه‌ها با عکس فیش",
                    "دسته‌بندی هزینه‌ها",
                    "تنظیم بودجه ماهانه",
                    "هشدار تجاوز از بودجه"
                ],
                "iranian_tools": ["حسابفا", "هزینه‌یاب"],
                "international_tools": ["Expensify", "Receipt Bank"],
                "price_range": "300,000 - 900,000 تومان",
                "target_businesses": ["کسب‌وکارهای کوچک"],
                "implementation_time": "3-5 روز"
            },
            "commission_system": {
                "title": "مدیریت پورسانت",
                "description": "محاسبه و پرداخت خودکار پورسانت",
                "features": [
                    "تعریف درصد پورسانت",
                    "محاسبه خودکار",
                    "گزارش فروشنده",
                    "پرداخت دوره‌ای"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["Commission Junction"],
                "price_range": "600,000 - 1,800,000 تومان",
                "target_businesses": ["فروش", "بازاریابی"],
                "implementation_time": "1-2 هفته"
            }
        }
    },
    
    "crm_customer": {
        "title": "👥 مدیریت ارتباط با مشتری",
        "icon": "👥",
        "services": {
            "crm_integration": {
                "title": "سیستم CRM کامل",
                "description": "مدیریت حرفه‌ای روابط با مشتریان",
                "features": [
                    "پروفایل کامل مشتری",
                    "تاریخچه خریدها",
                    "پیگیری تعاملات",
                    "اتوماسیون فروش"
                ],
                "iranian_tools": ["CRM ایرانی اختصاصی"],
                "international_tools": ["HubSpot", "Salesforce", "Zoho CRM"],
                "price_range": "1,000,000 - 3,000,000 تومان",
                "target_businesses": ["فروش", "خدمات", "B2B"],
                "implementation_time": "2-3 هفته"
            },
            "customer_loyalty": {
                "title": "سیستم وفاداری مشتری",
                "description": "امتیازدهی و پاداش برای مشتریان وفادار",
                "features": [
                    "امتیاز برای هر خرید",
                    "سطح‌بندی مشتریان",
                    "تخفیف‌های ویژه",
                    "هدایای تولد"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["LoyaltyLion", "Yotpo"],
                "price_range": "800,000 - 2,000,000 تومان",
                "target_businesses": ["فروشگاه", "رستوران", "زیبایی"],
                "implementation_time": "1-2 هفته"
            },
            "customer_support": {
                "title": "سیستم پشتیبانی مشتری",
                "description": "پلتفرم جامع پشتیبانی و خدمات پس از فروش",
                "features": [
                    "تیکت‌ها و درخواست‌ها",
                    "چت آنلاین",
                    "پایگاه دانش",
                    "نظرسنجی رضایت"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["Zendesk", "Freshdesk", "Intercom"],
                "price_range": "600,000 - 1,800,000 تومان",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "1-2 هفته"
            }
        }
    },
    
    "booking_scheduling": {
        "title": "🗓 سیستم رزرو و نوبت‌دهی",
        "icon": "🗓",
        "services": {
            "online_booking": {
                "title": "رزرو آنلاین حرفه‌ای",
                "description": "سیستم رزرو وقت برای خدمات",
                "features": [
                    "تقویم آنلاین",
                    "انتخاب زمان توسط مشتری",
                    "تأیید خودکار یا دستی",
                    "یادآوری پیامکی"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["Calendly", "Acuity", "Booksy"],
                "price_range": "500,000 - 1,500,000 تومان",
                "target_businesses": ["آرایشگاه", "مطب", "آموزشگاه"],
                "implementation_time": "1 هفته"
            },
            "queue_management": {
                "title": "مدیریت صف دیجیتال",
                "description": "سیستم نوبت‌دهی هوشمند بدون انتظار",
                "features": [
                    "شماره نوبت دیجیتال",
                    "تخمین زمان انتظار",
                    "اطلاع‌رسانی نزدیک شدن نوبت",
                    "آمار صف و انتظار"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["Q-nomy", "Qminder"],
                "price_range": "800,000 - 2,200,000 تومان",
                "target_businesses": ["بانک", "درمانگاه", "ادارات"],
                "implementation_time": "2 هفته"
            },
            "resource_booking": {
                "title": "رزرو منابع و تسهیلات",
                "description": "مدیریت رزرو اتاق‌ها، تجهیزات و منابع",
                "features": [
                    "رزرو اتاق جلسه",
                    "رزرو تجهیزات",
                    "محدودیت زمانی",
                    "تأیید مدیر"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["Robin", "Joan"],
                "price_range": "1,000,000 - 2,500,000 تومان",
                "target_businesses": ["شرکت‌ها", "مراکز آموزشی"],
                "implementation_time": "2-3 هفته"
            }
        }
    },
    
    "inventory_management": {
        "title": "📦 مدیریت موجودی و انبار",
        "icon": "📦",
        "services": {
            "inventory_tracking": {
                "title": "ردیابی موجودی هوشمند",
                "description": "کنترل دقیق موجودی و انبار",
                "features": [
                    "ثبت ورود و خروج کالا",
                    "هشدار موجودی کم",
                    "بارکد و QR کد",
                    "گزارش‌های انبار"
                ],
                "iranian_tools": ["انبارداری ایرانی"],
                "international_tools": ["Zoho Inventory", "TradeGecko"],
                "price_range": "700,000 - 2,000,000 تومان",
                "target_businesses": ["فروشگاه", "انبار", "تولید"],
                "implementation_time": "1-2 هفته"
            },
            "supply_chain": {
                "title": "مدیریت زنجیره تأمین",
                "description": "کنترل کامل از تأمین‌کننده تا مشتری",
                "features": [
                    "مدیریت تأمین‌کنندگان",
                    "سفارش خودکار کالا",
                    "پیش‌بینی تقاضا",
                    "بهینه‌سازی هزینه"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["SAP", "Oracle SCM"],
                "price_range": "2,000,000 - 5,000,000 تومان",
                "target_businesses": ["تولید", "توزیع", "فروشگاه‌های زنجیره‌ای"],
                "implementation_time": "3-6 هفته"
            },
            "warehouse_management": {
                "title": "سیستم مدیریت انبار",
                "description": "بهینه‌سازی عملیات انبارداری",
                "features": [
                    "نقشه انبار دیجیتال",
                    "بهینه‌سازی مسیر چیدمان",
                    "مدیریت بسته‌بندی",
                    "گزارش عملکرد انبار"
                ],
                "iranian_tools": ["WMS ایرانی"],
                "international_tools": ["Manhattan WMS", "JDA"],
                "price_range": "1,500,000 - 4,000,000 تومان",
                "target_businesses": ["انبارهای بزرگ", "مراکز توزیع"],
                "implementation_time": "4-8 هفته"
            }
        }
    },
    
    "pos_sales": {
        "title": "🧾 سیستم فروش و صندوق",
        "icon": "🧾",
        "services": {
            "pos_system": {
                "title": "سیستم POS کامل",
                "description": "صندوق فروش دیجیتال با تمام امکانات",
                "features": [
                    "فروش سریع با بارکد",
                    "مدیریت کالا و قیمت",
                    "چاپ فاکتور",
                    "گزارش فروش لحظه‌ای"
                ],
                "iranian_tools": ["POS ایرانی اختصاصی"],
                "international_tools": ["Square", "Shopify POS", "Lightspeed"],
                "price_range": "1,000,000 - 3,000,000 تومان + سخت‌افزار",
                "target_businesses": ["فروشگاه", "رستوران", "کافه"],
                "implementation_time": "1-2 هفته"
            },
            "mobile_pos": {
                "title": "POS موبایل",
                "description": "فروش در هر نقطه با موبایل یا تبلت",
                "features": [
                    "فروش با موبایل",
                    "کارت‌خوان بلوتوثی",
                    "همگام‌سازی با انبار",
                    "گزارش آنلاین"
                ],
                "iranian_tools": ["اپلیکیشن اختصاصی"],
                "international_tools": ["Square Reader", "SumUp"],
                "price_range": "500,000 - 1,500,000 تومان",
                "target_businesses": ["فروش سیار", "نمایشگاه", "دست‌فروش"],
                "implementation_time": "5-10 روز"
            },
            "restaurant_pos": {
                "title": "POS رستوران",
                "description": "سیستم فروش مخصوص رستوران و کافه",
                "features": [
                    "سفارش‌گیری از میز",
                    "مدیریت میزها",
                    "انتقال به آشپزخانه",
                    "محاسبه انعام"
                ],
                "iranian_tools": ["رستوران POS ایرانی"],
                "international_tools": ["Toast", "Revel", "TouchBistro"],
                "price_range": "1,500,000 - 4,000,000 تومان",
                "target_businesses": ["رستوران", "کافه", "فست‌فود"],
                "implementation_time": "2-3 هفته"
            }
        }
    },
    
    "delivery_tracking": {
        "title": "🚚 ردیابی و مدیریت تحویل",
        "icon": "🚚",
        "services": {
            "order_tracking": {
                "title": "ردیابی سفارش",
                "description": "پیگیری کامل مراحل تحویل سفارش",
                "features": [
                    "ردیابی لحظه‌ای",
                    "اطلاع‌رسانی مراحل",
                    "لینک ردیابی برای مشتری",
                    "تخمین زمان تحویل"
                ],
                "iranian_tools": ["پست ایران", "تیپاکس", "باربری‌ها"],
                "international_tools": ["AfterShip", "Route", "ShipStation"],
                "price_range": "300,000 - 1,000,000 تومان",
                "target_businesses": ["فروشگاه آنلاین"],
                "implementation_time": "1 هفته"
            },
            "delivery_management": {
                "title": "مدیریت پیک و تحویل",
                "description": "سیستم کامل مدیریت پیک‌ها و تحویل",
                "features": [
                    "مدیریت پیک‌ها",
                    "بهینه‌سازی مسیر",
                    "محاسبه هزینه ارسال",
                    "رضایت‌سنجی تحویل"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["Onfleet", "GetSwift"],
                "price_range": "1,000,000 - 3,000,000 تومان",
                "target_businesses": ["رستوران", "داروخانه", "سوپرمارکت"],
                "implementation_time": "2-4 هفته"
            },
            "shipping_integration": {
                "title": "اتصال شرکت‌های حمل",
                "description": "ادغام با شرکت‌های حمل‌ونقل",
                "features": [
                    "اتصال پست ایران",
                    "ادغام با تیپاکس",
                    "باربری‌های محلی",
                    "مقایسه نرخ حمل"
                ],
                "iranian_tools": ["پست ایران API", "تیپاکس API"],
                "international_tools": ["FedEx", "DHL", "UPS"],
                "price_range": "500,000 - 1,500,000 تومان",
                "target_businesses": ["فروشگاه آنلاین"],
                "implementation_time": "1-2 هفته"
            }
        }
    },
    
    "analytics_reporting": {
        "title": "📊 تحلیل و داشبورد هوشمند",
        "icon": "📊",
        "services": {
            "business_dashboard": {
                "title": "داشبورد مدیریتی",
                "description": "نمای کلی از عملکرد کسب‌وکار",
                "features": [
                    "KPI های کلیدی",
                    "نمودارهای تعاملی",
                    "گزارش‌های خودکار",
                    "هشدارهای هوشمند"
                ],
                "iranian_tools": ["داشبورد اختصاصی"],
                "international_tools": ["Google Analytics", "Tableau", "Power BI"],
                "price_range": "800,000 - 2,500,000 تومان",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "1-3 هفته"
            },
            "sales_analytics": {
                "title": "تحلیل فروش",
                "description": "آنالیز عمیق عملکرد فروش و بازاریابی",
                "features": [
                    "ترند فروش",
                    "تحلیل مشتری",
                    "محصولات پرفروش",
                    "پیش‌بینی فروش"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["Salesforce Analytics", "HubSpot"],
                "price_range": "600,000 - 1,800,000 تومان",
                "target_businesses": ["فروش", "بازاریابی"],
                "implementation_time": "2 هفته"
            },
            "financial_reporting": {
                "title": "گزارش‌گیری مالی",
                "description": "گزارش‌های مالی و حسابداری خودکار",
                "features": [
                    "سود و زیان",
                    "ترازنامه",
                    "جریان نقدی",
                    "نسبت‌های مالی"
                ],
                "iranian_tools": ["حسابفا", "سپیدار"],
                "international_tools": ["QuickBooks", "Xero"],
                "price_range": "500,000 - 1,500,000 تومان",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "1-2 هفته"
            }
        }
    },
    
    "marketing_automation": {
        "title": "🎯 بازاریابی و اتوماسیون",
        "icon": "🎯",
        "services": {
            "email_marketing": {
                "title": "ایمیل مارکتینگ",
                "description": "کمپین‌های ایمیلی خودکار",
                "features": [
                    "خبرنامه",
                    "ایمیل خودکار",
                    "آنالیز نتایج",
                    "A/B تست"
                ],
                "iranian_tools": ["ایمیل سرویس ایرانی"],
                "international_tools": ["Mailchimp", "ConvertKit", "AWeber"],
                "price_range": "400,000 - 1,200,000 تومان ماهانه",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "1 هفته"
            },
            "social_media_management": {
                "title": "مدیریت شبکه‌های اجتماعی",
                "description": "اتوماسیون و مدیریت شبکه‌های اجتماعی",
                "features": [
                    "زمان‌بندی پست‌ها",
                    "تحلیل عملکرد",
                    "پاسخ خودکار",
                    "مانیتورینگ برند"
                ],
                "iranian_tools": ["ابزار اختصاصی"],
                "international_tools": ["Hootsuite", "Buffer", "Sprout Social"],
                "price_range": "500,000 - 1,500,000 تومان ماهانه",
                "target_businesses": ["برند", "فروشگاه", "خدمات"],
                "implementation_time": "1-2 هفته"
            },
            "lead_generation": {
                "title": "تولید مشتری بالقوه",
                "description": "سیستم جذب و تربیت مشتری بالقوه",
                "features": [
                    "فرم‌های جذب",
                    "مگنت سرب",
                    "اتوماسیون تربیت",
                    "امتیازدهی مشتری"
                ],
                "iranian_tools": ["سیستم اختصاصی"],
                "international_tools": ["HubSpot", "Pardot", "Marketo"],
                "price_range": "800,000 - 2,500,000 تومان",
                "target_businesses": ["B2B", "خدمات", "مشاوره"],
                "implementation_time": "2-3 هفته"
            }
        }
    },
    
    "advanced_features": {
        "title": "🚀 ویژگی‌های پیشرفته",
        "icon": "🚀",
        "services": {
            "chatbot_ai": {
                "title": "ربات گفتگوی هوشمند",
                "description": "پاسخگوی خودکار مشتریان با هوش مصنوعی",
                "features": [
                    "پاسخ 24/7",
                    "تشخیص زبان طبیعی",
                    "انتقال به انسان",
                    "یادگیری خودکار"
                ],
                "iranian_tools": ["چت‌بات اختصاصی"],
                "international_tools": ["Intercom", "Drift", "Zendesk Chat"],
                "price_range": "1,000,000 - 3,000,000 تومان",
                "target_businesses": ["فروشگاه آنلاین", "خدمات"],
                "implementation_time": "2-4 هفته"
            },
            "mobile_app": {
                "title": "اپلیکیشن موبایل",
                "description": "اپ اختصاصی برای کسب‌وکار شما",
                "features": [
                    "اپ اندروید و iOS",
                    "نوتیفیکیشن",
                    "خرید درون‌برنامه‌ای",
                    "حساب کاربری"
                ],
                "iranian_tools": ["توسعه اختصاصی"],
                "international_tools": ["React Native", "Flutter"],
                "price_range": "5,000,000 - 20,000,000 تومان",
                "target_businesses": ["برندهای بزرگ", "فروشگاه‌های زنجیره‌ای"],
                "implementation_time": "2-6 ماه"
            },
            "api_integration": {
                "title": "ادغام سیستم‌های خارجی",
                "description": "اتصال به سیستم‌ها و سرویس‌های خارجی",
                "features": [
                    "API سفارشی",
                    "ادغام ERP",
                    "اتصال به انبار",
                    "همگام‌سازی داده"
                ],
                "iranian_tools": ["توسعه اختصاصی"],
                "international_tools": ["Zapier", "Microsoft Flow"],
                "price_range": "2,000,000 - 8,000,000 تومان",
                "target_businesses": ["شرکت‌های بزرگ"],
                "implementation_time": "4-12 هفته"
            },
            "pwa_development": {
                "title": "Progressive Web App",
                "description": "تبدیل سایت به اپلیکیشن وب پیشرفته",
                "features": [
                    "کار آفلاین",
                    "نصب روی موبایل",
                    "نوتیفیکیشن وب",
                    "سرعت بالا"
                ],
                "iranian_tools": ["توسعه اختصاصی"],
                "international_tools": ["PWA Builder", "Workbox"],
                "price_range": "1,500,000 - 4,000,000 تومان",
                "target_businesses": ["فروشگاه آنلاین", "خدمات"],
                "implementation_time": "3-6 هفته"
            }
        }
    },
    
    "security_maintenance": {
        "title": "🔒 امنیت و نگهداری",
        "icon": "🔒",
        "services": {
            "security_ssl": {
                "title": "امنیت و SSL",
                "description": "محافظت کامل سایت و اطلاعات مشتریان",
                "features": [
                    "گواهی SSL",
                    "فایروال",
                    "محافظت از DDoS",
                    "بکاپ روزانه"
                ],
                "iranian_tools": ["CDN ایرانی", "آسیاتک"],
                "international_tools": ["Cloudflare", "Let's Encrypt"],
                "price_range": "200,000 - 800,000 تومان سالانه",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "1-2 روز"
            },
            "backup_recovery": {
                "title": "پشتیبان‌گیری و بازیابی",
                "description": "محافظت از داده‌ها و بازیابی سریع",
                "features": [
                    "بکاپ خودکار",
                    "ذخیره ابری",
                    "بازیابی سریع",
                    "تست بازیابی"
                ],
                "iranian_tools": ["ذخیره ابری ایرانی"],
                "international_tools": ["AWS Backup", "Google Drive"],
                "price_range": "150,000 - 500,000 تومان ماهانه",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "2-3 روز"
            },
            "maintenance_support": {
                "title": "نگهداری و پشتیبانی",
                "description": "نگهداری مداوم و پشتیبانی فنی",
                "features": [
                    "آپدیت مداوم",
                    "رفع باگ",
                    "پشتیبانی 24/7",
                    "مانیتورینگ سایت"
                ],
                "iranian_tools": ["تیم پشتیبانی اختصاصی"],
                "international_tools": ["تیم بین‌المللی"],
                "price_range": "300,000 - 1,000,000 تومان ماهانه",
                "target_businesses": ["همه کسب‌وکارها"],
                "implementation_time": "فوری"
            }
        }
    }
}

def generate_services_summary():
    """تولید خلاصه خدمات"""
    total_services = 0
    categories = len(COMPLETE_SERVICES_CATALOG)
    
    by_implementation_time = {"1 هفته": 0, "2 هفته": 0, "بیشتر از 1 ماه": 0}
    by_target_business = {}
    by_price_range = {"تا 1 میلیون": 0, "1-3 میلیون": 0, "بیش از 3 میلیون": 0}
    
    for category_data in COMPLETE_SERVICES_CATALOG.values():
        for service_data in category_data["services"].values():
            total_services += 1
            
            # تحلیل زمان پیاده‌سازی
            impl_time = service_data["implementation_time"]
            if "روز" in impl_time or ("1" in impl_time and "هفته" in impl_time):
                by_implementation_time["1 هفته"] += 1
            elif "2" in impl_time and "هفته" in impl_time:
                by_implementation_time["2 هفته"] += 1
            else:
                by_implementation_time["بیشتر از 1 ماه"] += 1
            
            # تحلیل کسب‌وکارهای هدف
            for business in service_data["target_businesses"]:
                by_target_business[business] = by_target_business.get(business, 0) + 1
            
            # تحلیل قیمت
            price = service_data["price_range"]
            if "1,000,000" not in price or price.startswith("300,000") or price.startswith("500,000"):
                by_price_range["تا 1 میلیون"] += 1
            elif "3,000,000" not in price or "2,000,000" in price:
                by_price_range["1-3 میلیون"] += 1
            else:
                by_price_range["بیش از 3 میلیون"] += 1
    
    return {
        "total_categories": categories,
        "total_services": total_services,
        "by_implementation_time": by_implementation_time,
        "by_target_business": by_target_business,
        "by_price_range": by_price_range,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    """ایجاد فایل‌های کاتالوگ خدمات کامل"""
    
    # ذخیره کاتالوگ کامل
    with open("complete_services_catalog.json", 'w', encoding='utf-8') as f:
        json.dump(COMPLETE_SERVICES_CATALOG, f, ensure_ascii=False, indent=2)
    
    # تولید خلاصه
    summary = generate_services_summary()
    
    # ذخیره خلاصه
    with open("complete_services_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # تولید راهنمای کامل خدمات
    guide_content = f"""# 🏢 راهنمای کامل خدمات کسب‌وکاری

## 📊 خلاصه آمار
- **تعداد دسته‌ها:** {summary['total_categories']} دسته
- **تعداد خدمات:** {summary['total_services']} خدمت کامل

### زمان پیاده‌سازی:
- **سریع (تا 1 هفته):** {summary['by_implementation_time']['1 هفته']} خدمت
- **متوسط (2 هفته):** {summary['by_implementation_time']['2 هفته']} خدمت  
- **طولانی (بیشتر از 1 ماه):** {summary['by_implementation_time']['بیشتر از 1 ماه']} خدمت

### محدوده قیمت:
- **اقتصادی (تا 1 میلیون):** {summary['by_price_range']['تا 1 میلیون']} خدمت
- **متوسط (1-3 میلیون):** {summary['by_price_range']['1-3 میلیون']} خدمت
- **پریمیوم (بیش از 3 میلیون):** {summary['by_price_range']['بیش از 3 میلیون']} خدمت

## 🎯 بسته‌های خدماتی پیشنهادی

### 📦 بسته مبتدی (3-5 میلیون تومان)
✅ طراحی سایت اختصاصی  
✅ اتصال درگاه پرداخت  
✅ پیامک خودکار  
✅ سیستم رزرو ساده  
✅ SSL و امنیت پایه  

**مناسب برای:** نانوایی، آرایشگاه، مطب، خدمات محلی

### 📦 بسته حرفه‌ای (8-15 میلیون تومان)
✅ فروشگاه آنلاین کامل  
✅ سیستم CRM  
✅ حسابداری متصل  
✅ موجودی و انبار  
✅ POS سیستم  
✅ تحلیل و گزارش  

**مناسب برای:** فروشگاه، رستوران، برند کوچک

### 📦 بسته پیشرفته (20-50 میلیون تومان)
✅ همه خدمات بسته حرفه‌ای  
✅ اپلیکیشن موبایل  
✅ چت‌بات هوشمند  
✅ اتوماسیون بازاریابی  
✅ ادغام سیستم‌های خارجی  
✅ پشتیبانی اختصاصی  

**مناسب برای:** شرکت‌ها، برندهای بزرگ، زنجیره‌ها

## 🚀 خدمات ویژه ایرانی

### 💳 **درگاه‌های پرداخت ایرانی:**
- زرین‌پال (محبوب‌ترین)
- آیدی‌پی (مدرن)  
- بانک‌های پارسیان، پاسارگاد، ملت

### 📱 **پیامک ایرانی:**
- کاوه‌نگار (پرطرفدار)
- مگفا، آی‌پی‌پنل، SMS.ir

### 🧮 **حسابداری ایرانی:**
- سپیدار (محبوب‌ترین)
- حسابفا (آنلاین)
- هدهد (ساده)

## 💡 مشاوره رایگان

قبل از شروع، **مشاوره رایگان** دریافت کنید:
- تحلیل نیازهای کسب‌وکار
- پیشنهاد بهترین ابزارها  
- برآورد هزینه و زمان
- نقشه راه پیاده‌سازی

---

## 📞 راه‌های ارتباط

**تلفن:** 021-xxxxxxxx  
**واتساپ:** 09xxxxxxxxx  
**ایمیل:** info@company.com  
**آدرس:** تهران، خیابان...

---

*تولید شده در {summary['generated_at']}*
"""
    
    with open("COMPLETE_SERVICES_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("🎉 کاتالوگ خدمات کامل شد!")
    print(f"📊 {summary['total_services']} خدمت در {summary['total_categories']} دسته")
    print("📁 فایل‌ها:")
    print("  - complete_services_catalog.json")
    print("  - complete_services_summary.json") 
    print("  - COMPLETE_SERVICES_GUIDE.md")

if __name__ == "__main__":
    main()