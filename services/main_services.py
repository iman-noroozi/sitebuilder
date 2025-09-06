# 🎯 فایل اصلی همه خدمات
import json
from services.web_services import WEB_SERVICES
from services.payment_services import PAYMENT_SERVICES
from services.bot_services import BOT_SERVICES
from services.marketing_services import MARKETING_SERVICES
from services.ecommerce_services import ECOMMERCE_SERVICES

def create_unified_services():
    """ایجاد ساختار واحد همه خدمات"""
    
    unified_services = {
        "platform_info": {
            "name": "🌟 پلتفرم واحد همه خدمات",
            "description": "تمامی خدمات در یک مکان مرتب و سازماندهی شده",
            "version": "4.0 UNIFIED",
            "last_updated": "2024-12-19 15:30:00",
            "total_sections": 5,
            "total_services": 20
        },
        "service_sections": [
            {
                "section_id": "web_design",
                "section_name": "🌐 خدمات وب و طراحی",
                "description": "طراحی و توسعه وب حرفه‌ای",
                "icon": "🌐",
                "services": WEB_SERVICES
            },
            {
                "section_id": "payment_financial",
                "section_name": "💳 خدمات پرداخت و مالی",
                "description": "راه‌حل‌های پرداخت و مدیریت مالی",
                "icon": "💳",
                "services": PAYMENT_SERVICES
            },
            {
                "section_id": "bot_development",
                "section_name": "🤖 خدمات ربات‌سازی و اتوماسیون",
                "description": "ساخت ربات‌های هوشمند برای همه پلتفرم‌ها",
                "icon": "🤖",
                "services": BOT_SERVICES
            },
            {
                "section_id": "marketing",
                "section_name": "📈 خدمات بازاریابی و تبلیغات",
                "description": "ابزارهای بازاریابی هوشمند",
                "icon": "📈",
                "services": MARKETING_SERVICES
            },
            {
                "section_id": "ecommerce",
                "section_name": "🛍 خدمات فروشگاه و موجودی",
                "description": "راه‌حل‌های کامل تجارت الکترونیک",
                "icon": "🛍",
                "services": ECOMMERCE_SERVICES
            }
        ],
        "statistics": {
            "total_sections": 5,
            "total_services": 20,
            "setup_time_range": "فوری تا 12 هفته",
            "coverage": "همه صنایع و نیازها"
        }
    }
    
    return unified_services

def save_services_to_json():
    """ذخیره خدمات در فایل JSON"""
    services = create_unified_services()
    
    with open('all_services_unified.json', 'w', encoding='utf-8') as f:
        json.dump(services, f, ensure_ascii=False, indent=2)
    
    print("✅ فایل JSON با موفقیت ایجاد شد!")
    print(f"📊 تعداد بخش‌ها: {services['statistics']['total_sections']}")
    print(f"🎯 کل خدمات: {services['statistics']['total_services']}")

if __name__ == "__main__":
    save_services_to_json() 