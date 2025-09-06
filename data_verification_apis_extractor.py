#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 استخراج API های استعلام و تایید هویت
همه سرویس‌های ممکن برای استعلام کد ملی، آدرس، موبایل و...
"""

import json
from datetime import datetime

# سرویس‌های استعلام و تایید هویت ایرانی
IRANIAN_VERIFICATION_APIS = {
    "national_id_verification": {
        "category": "تایید هویت",
        "services": {
            "sabte_ahval": {
                "name": "سازمان ثبت احوال",
                "url": "https://www.sabteahval.ir",
                "description": "استعلام اصالت کد ملی و مشخصات فردی",
                "apis": [
                    "تایید کد ملی",
                    "استعلام نام و نام خانوادگی",
                    "تاریخ تولد",
                    "محل تولد",
                    "وضعیت حیات"
                ],
                "cost": "500 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "1-3 ثانیه"
            },
            "postal_company": {
                "name": "شرکت ملی پست ایران",
                "url": "https://www.post.ir",
                "description": "تایید آدرس و کد پستی",
                "apis": [
                    "تایید کد پستی",
                    "استعلام آدرس کامل",
                    "تعیین موقعیت جغرافیایی",
                    "تایید وجود آدرس"
                ],
                "cost": "300 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "متوسط",
                "response_time": "2-5 ثانیه"
            },
            "telecommunications": {
                "name": "سازمان تنظیم مقررات ارتباطات",
                "url": "https://www.cra.ir",
                "description": "تایید شماره همراه و اپراتور",
                "apis": [
                    "تایید شماره همراه",
                    "تشخیص اپراتور",
                    "وضعیت فعال/غیرفعال",
                    "نوع خط (دائمی/اعتباری)"
                ],
                "cost": "200 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "1-2 ثانیه"
            }
        }
    },
    
    "business_verification": {
        "category": "تایید کسب‌وکار",
        "services": {
            "tax_affairs": {
                "name": "سازمان امور مالیاتی",
                "url": "https://www.intamedia.ir",
                "description": "استعلام شناسه ملی و وضعیت مالیاتی",
                "apis": [
                    "تایید شناسه ملی شرکت",
                    "وضعیت مالیاتی",
                    "نام شرکت",
                    "آدرس ثبتی",
                    "وضعیت فعالیت"
                ],
                "cost": "800 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "3-6 ثانیه"
            },
            "company_registration": {
                "name": "سازمان ثبت شرکت‌ها",
                "url": "https://www.sabteahval.ir",
                "description": "استعلام اطلاعات ثبتی شرکت",
                "apis": [
                    "شماره ثبت شرکت",
                    "نوع شرکت",
                    "سرمایه شرکت",
                    "تاریخ ثبت",
                    "مدیران شرکت"
                ],
                "cost": "1000 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "5-10 ثانیه"
            },
            "chamber_commerce": {
                "name": "اتاق بازرگانی ایران",
                "url": "https://www.iccima.ir",
                "description": "تایید عضویت در اتاق بازرگانی",
                "apis": [
                    "شماره عضویت",
                    "نوع فعالیت",
                    "درجه اعتبار",
                    "تاریخ عضویت",
                    "وضعیت فعال/غیرفعال"
                ],
                "cost": "600 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "متوسط",
                "response_time": "3-8 ثانیه"
            }
        }
    },
    
    "financial_verification": {
        "category": "تایید مالی",
        "services": {
            "banking_system": {
                "name": "سیستم بانکی کشور",
                "url": "https://www.cbi.ir",
                "description": "تایید حساب بانکی و شماره کارت",
                "apis": [
                    "تایید شماره حساب",
                    "نام صاحب حساب",
                    "نام بانک",
                    "وضعیت حساب",
                    "تایید شماره کارت"
                ],
                "cost": "400 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "2-4 ثانیه"
            },
            "insurance_verification": {
                "name": "سازمان تامین اجتماعی",
                "url": "https://www.tamin.ir",
                "description": "تایید سابقه بیمه و وضعیت بیمه",
                "apis": [
                    "شماره بیمه",
                    "سابقه بیمه",
                    "وضعیت اشتغال",
                    "نام کارفرما",
                    "میزان حقوق"
                ],
                "cost": "600 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "متوسط",
                "response_time": "5-12 ثانیه"
            }
        }
    },
    
    "property_verification": {
        "category": "تایید املاک",
        "services": {
            "property_registration": {
                "name": "سازمان ثبت اسناد و املاک",
                "url": "https://www.sabt.ir",
                "description": "استعلام اطلاعات ملکی",
                "apis": [
                    "مالکیت ملک",
                    "مساحت ملک",
                    "نوع کاربری",
                    "آدرس دقیق",
                    "وضعیت رهن/فروش"
                ],
                "cost": "1200 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "10-20 ثانیه"
            },
            "municipality": {
                "name": "شهرداری‌های کشور",
                "url": "https://www.tehran.ir",
                "description": "استعلام پروانه ساختمان و مجوزها",
                "apis": [
                    "پروانه ساختمان",
                    "پایان کار",
                    "عوارض شهرداری",
                    "آدرس ملک",
                    "مجوزهای شهرداری"
                ],
                "cost": "400 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "متوسط",
                "response_time": "3-10 ثانیه"
            }
        }
    }
}

# سرویس‌های بین‌المللی
INTERNATIONAL_VERIFICATION_APIS = {
    "global_services": {
        "category": "سرویس‌های جهانی",
        "services": {
            "trulioo": {
                "name": "Trulioo Global Identity",
                "url": "https://www.trulioo.com",
                "description": "تایید هویت جهانی",
                "apis": [
                    "Document Verification",
                    "Address Verification", 
                    "Phone Verification",
                    "Email Verification",
                    "Age Verification"
                ],
                "cost": "$0.75 - $3.00 per query",
                "iranian_compatibility": "محدود",
                "reliability": "بالا",
                "response_time": "1-3 seconds"
            },
            "jumio": {
                "name": "Jumio Identity Verification",
                "url": "https://www.jumio.com",
                "description": "تایید هویت با سند شناسایی",
                "apis": [
                    "ID Document Verification",
                    "Selfie Verification",
                    "Liveness Detection",
                    "Age Verification",
                    "Address Verification"
                ],
                "cost": "$1.50 - $4.00 per verification",
                "iranian_compatibility": "محدود",
                "reliability": "بالا",
                "response_time": "2-5 seconds"
            },
            "twilio_verify": {
                "name": "Twilio Verify API",
                "url": "https://www.twilio.com/verify",
                "description": "تایید شماره تلفن با OTP",
                "apis": [
                    "SMS Verification",
                    "Voice Verification",
                    "Email Verification",
                    "Push Notification Verify",
                    "TOTP Verification"
                ],
                "cost": "$0.05 - $0.15 per verification",
                "iranian_compatibility": "متوسط",
                "reliability": "بالا",
                "response_time": "1-2 seconds"
            }
        }
    },
    
    "data_enrichment": {
        "category": "غنی‌سازی داده",
        "services": {
            "clearbit": {
                "name": "Clearbit Enrichment API",
                "url": "https://clearbit.com",
                "description": "غنی‌سازی اطلاعات شرکت و شخص",
                "apis": [
                    "Person Enrichment",
                    "Company Enrichment",
                    "Email Finder",
                    "Logo API",
                    "Autocomplete"
                ],
                "cost": "$0.20 - $1.00 per enrichment",
                "iranian_compatibility": "کم",
                "reliability": "بالا",
                "response_time": "1-3 seconds"
            },
            "fullcontact": {
                "name": "FullContact Identity API",
                "url": "https://www.fullcontact.com",
                "description": "حل هویت و غنی‌سازی مخاطب",
                "apis": [
                    "Person Enrich",
                    "Company Enrich", 
                    "Email Verification",
                    "Social Media Profiles",
                    "Contact Resolution"
                ],
                "cost": "$0.30 - $2.00 per request",
                "iranian_compatibility": "کم",
                "reliability": "بالا",
                "response_time": "2-4 seconds"
            }
        }
    }
}

# سرویس‌های ایرانی اختصاصی
SPECIALIZED_IRANIAN_APIS = {
    "government_services": {
        "category": "خدمات دولتی",
        "services": {
            "egov_portal": {
                "name": "دروازه ملی خدمات الکترونیک دولت",
                "url": "https://www.iran.gov.ir",
                "description": "دسترسی به خدمات دولتی",
                "apis": [
                    "استعلام وضعیت نظام وظیفه",
                    "گواهی عدم سوء پیشینه",
                    "استعلام مدارک تحصیلی",
                    "وضعیت گذرنامه",
                    "استعلام جرائم رانندگی"
                ],
                "cost": "200-1000 تومان بر حسب نوع استعلام",
                "iranian_compatibility": "100%",
                "reliability": "متوسط",
                "response_time": "5-30 ثانیه"
            },
            "police_services": {
                "name": "نیروی انتظامی جمهوری اسلامی ایران",
                "url": "https://www.police.ir",
                "description": "استعلامات انتظامی",
                "apis": [
                    "استعلام پلاک خودرو",
                    "وضعیت گواهینامه",
                    "جرائم رانندگی",
                    "استعلام سرقتی بودن خودرو",
                    "وضعیت بیمه شخص ثالث"
                ],
                "cost": "300-800 تومان بر حسب نوع استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "3-10 ثانیه"
            }
        }
    },
    
    "education_verification": {
        "category": "تایید تحصیلات",
        "services": {
            "education_ministry": {
                "name": "وزارت آموزش و پرورش",
                "url": "https://www.medu.ir",
                "description": "تایید مدارک تحصیلی",
                "apis": [
                    "تایید دیپلم",
                    "کارنامه دبیرستان",
                    "رتبه کنکور",
                    "معدل کل",
                    "رشته تحصیلی"
                ],
                "cost": "500 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "5-15 ثانیه"
            },
            "university_verification": {
                "name": "وزارت علوم، تحقیقات و فناوری",
                "url": "https://www.msrt.ir",
                "description": "تایید مدارک دانشگاهی",
                "apis": [
                    "تایید مدرک دانشگاهی",
                    "نام دانشگاه",
                    "رشته تحصیلی",
                    "سال فارغ‌التحصیلی",
                    "معدل کل"
                ],
                "cost": "800 تومان به ازای هر استعلام",
                "iranian_compatibility": "100%",
                "reliability": "بالا",
                "response_time": "10-25 ثانیه"
            }
        }
    }
}

def generate_verification_marketplace():
    """تولید مارکت‌پلیس سرویس‌های تایید هویت"""
    
    marketplace = {
        "iranian_apis": IRANIAN_VERIFICATION_APIS,
        "international_apis": INTERNATIONAL_VERIFICATION_APIS,
        "specialized_apis": SPECIALIZED_IRANIAN_APIS,
        "total_services": 0,
        "pricing_models": {
            "pay_per_use": "پرداخت بر اساس استفاده",
            "monthly_subscription": "اشتراک ماهانه",
            "annual_package": "بسته سالانه با تخفیف"
        },
        "integration_methods": {
            "rest_api": "REST API",
            "webhook": "Webhook",
            "batch_processing": "پردازش انبوه",
            "real_time": "بلادرنگ"
        }
    }
    
    # محاسبه تعداد کل سرویس‌ها
    for category in [IRANIAN_VERIFICATION_APIS, INTERNATIONAL_VERIFICATION_APIS, SPECIALIZED_IRANIAN_APIS]:
        for main_cat in category.values():
            marketplace["total_services"] += len(main_cat["services"])
    
    return marketplace

def main():
    """ایجاد فایل‌های سرویس‌های تایید هویت"""
    
    marketplace = generate_verification_marketplace()
    
    # ذخیره مارکت‌پلیس کامل
    with open("verification_apis_marketplace.json", 'w', encoding='utf-8') as f:
        json.dump(marketplace, f, ensure_ascii=False, indent=2)
    
    # تولید راهنمای کامل
    guide_content = f"""# 🔍 مارکت‌پلیس API های استعلام و تایید هویت

## 📊 خلاصه آمار
- **تعداد کل سرویس‌ها:** {marketplace['total_services']} سرویس
- **سرویس‌های ایرانی:** {len(IRANIAN_VERIFICATION_APIS)} دسته
- **سرویس‌های بین‌المللی:** {len(INTERNATIONAL_VERIFICATION_APIS)} دسته
- **سرویس‌های تخصصی:** {len(SPECIALIZED_IRANIAN_APIS)} دسته

## 🇮🇷 سرویس‌های ایرانی (100% سازگار)

"""
    
    # اضافه کردن سرویس‌های ایرانی
    for category_id, category_data in IRANIAN_VERIFICATION_APIS.items():
        guide_content += f"### {category_data['category']}\n\n"
        
        for service_id, service_data in category_data['services'].items():
            guide_content += f"#### {service_data['name']}\n"
            guide_content += f"**وب‌سایت:** {service_data['url']}\n"
            guide_content += f"**توضیحات:** {service_data['description']}\n\n"
            guide_content += "**API های موجود:**\n"
            for api in service_data['apis']:
                guide_content += f"- {api}\n"
            guide_content += f"\n**هزینه:** {service_data['cost']}\n"
            guide_content += f"**قابلیت اطمینان:** {service_data['reliability']}\n"
            guide_content += f"**زمان پاسخ:** {service_data['response_time']}\n\n"
            guide_content += "---\n\n"
    
    # اضافه کردن سرویس‌های بین‌المللی
    guide_content += "## 🌍 سرویس‌های بین‌المللی\n\n"
    
    for category_id, category_data in INTERNATIONAL_VERIFICATION_APIS.items():
        guide_content += f"### {category_data['category']}\n\n"
        
        for service_id, service_data in category_data['services'].items():
            guide_content += f"#### {service_data['name']}\n"
            guide_content += f"**وب‌سایت:** {service_data['url']}\n"
            guide_content += f"**توضیحات:** {service_data['description']}\n\n"
            guide_content += "**API های موجود:**\n"
            for api in service_data['apis']:
                guide_content += f"- {api}\n"
            guide_content += f"\n**هزینه:** {service_data['cost']}\n"
            guide_content += f"**سازگاری با ایران:** {service_data['iranian_compatibility']}\n"
            guide_content += f"**قابلیت اطمینان:** {service_data['reliability']}\n"
            guide_content += f"**زمان پاسخ:** {service_data['response_time']}\n\n"
            guide_content += "---\n\n"
    
    # اضافه کردن سرویس‌های تخصصی
    guide_content += "## 🎯 سرویس‌های تخصصی ایرانی\n\n"
    
    for category_id, category_data in SPECIALIZED_IRANIAN_APIS.items():
        guide_content += f"### {category_data['category']}\n\n"
        
        for service_id, service_data in category_data['services'].items():
            guide_content += f"#### {service_data['name']}\n"
            guide_content += f"**وب‌سایت:** {service_data['url']}\n"
            guide_content += f"**توضیحات:** {service_data['description']}\n\n"
            guide_content += "**API های موجود:**\n"
            for api in service_data['apis']:
                guide_content += f"- {api}\n"
            guide_content += f"\n**هزینه:** {service_data['cost']}\n"
            guide_content += f"**قابلیت اطمینان:** {service_data['reliability']}\n"
            guide_content += f"**زمان پاسخ:** {service_data['response_time']}\n\n"
            guide_content += "---\n\n"
    
    guide_content += f"""
## 💰 مدل‌های قیمت‌گذاری

### 🔸 پرداخت بر اساس استفاده
- هزینه فقط برای استعلامات انجام شده
- مناسب کسب‌وکارهای کوچک
- بدون هزینه ثابت ماهانه

### 🔸 اشتراک ماهانه
- تعداد محدود استعلام رایگان
- هزینه کمتر برای استفاده بالا
- پشتیبانی اولویت‌دار

### 🔸 بسته سالانه
- تا 40% تخفیف نسبت به ماهانه
- استعلامات نامحدود
- پشتیبانی اختصاصی

## 🔧 روش‌های ادغام

### REST API
- ساده‌ترین روش ادغام
- پشتیبانی از JSON/XML
- مستندات کامل

### Webhook
- اطلاع‌رسانی خودکار
- مناسب برای پردازش‌های طولانی
- کاهش زمان انتظار

### پردازش انبوه
- آپلود فایل Excel/CSV
- پردازش هزاران رکورد
- خروجی گزارش تفصیلی

### بلادرنگ
- پاسخ فوری
- مناسب برای فرم‌های آنلاین
- تجربه کاربری بهتر

---

## 📞 پشتیبانی فنی

**ایمیل:** api-support@company.com  
**تلفن:** 021-xxxxxxxx  
**مستندات:** https://docs.company.com  
**تست API:** https://sandbox.company.com  

---

*تولید شده در {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    with open("VERIFICATION_APIS_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("🎉 مارکت‌پلیس API های تایید هویت آماده شد!")
    print(f"🔍 {marketplace['total_services']} سرویس استعلام و تایید")
    print("📁 فایل‌ها:")
    print("  - verification_apis_marketplace.json")
    print("  - VERIFICATION_APIS_GUIDE.md")
    print("\n🇮🇷 سرویس‌های ایرانی شامل:")
    print("  ✅ تایید کد ملی و مشخصات")
    print("  ✅ استعلام آدرس و کد پستی") 
    print("  ✅ تایید شماره همراه و اپراتور")
    print("  ✅ استعلام شرکت‌ها و کسب‌وکارها")
    print("  ✅ تایید حساب بانکی")
    print("  ✅ استعلام املاک و دارایی")
    print("  ✅ تایید مدارک تحصیلی")
    print("  ✅ استعلامات دولتی و انتظامی")

if __name__ == "__main__":
    main()