#!/usr/bin/env python
"""
اسکریپت بارگذاری قالب‌ها از پوشه templates_library به دیتابیس
"""
import os
import sys
import django
from pathlib import Path

# تنظیم Django
sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from sitebuilder_app.models import TemplateCategory, SiteTemplate
from django.contrib.auth.models import User

def create_categories():
    """ایجاد دسته‌بندی‌های قالب"""
    categories_data = [
        {
            'name': 'کسب و کار',
            'name_en': 'Business',
            'description': 'قالب‌های مربوط به کسب و کار و شرکت‌ها',
            'icon': 'fas fa-briefcase',
            'color': '#007bff'
        },
        {
            'name': 'فروشگاه آنلاین',
            'name_en': 'E-commerce',
            'description': 'قالب‌های فروشگاه آنلاین و تجارت الکترونیک',
            'icon': 'fas fa-shopping-cart',
            'color': '#28a745'
        },
        {
            'name': 'رستوران و غذا',
            'name_en': 'Restaurant & Food',
            'description': 'قالب‌های رستوران، کافه و خدمات غذایی',
            'icon': 'fas fa-utensils',
            'color': '#ffc107'
        },
        {
            'name': 'سلامت و پزشکی',
            'name_en': 'Health & Medical',
            'description': 'قالب‌های پزشکی، درمانگاه و سلامت',
            'icon': 'fas fa-heartbeat',
            'color': '#dc3545'
        },
        {
            'name': 'آموزش',
            'name_en': 'Education',
            'description': 'قالب‌های آموزشی، مدرسه و دانشگاه',
            'icon': 'fas fa-graduation-cap',
            'color': '#17a2b8'
        },
        {
            'name': 'سفر و گردشگری',
            'name_en': 'Travel & Tourism',
            'description': 'قالب‌های آژانس مسافرتی و گردشگری',
            'icon': 'fas fa-plane',
            'color': '#6f42c1'
        },
        {
            'name': 'رویداد و هنر',
            'name_en': 'Events & Arts',
            'description': 'قالب‌های رویدادها، هنر و فرهنگ',
            'icon': 'fas fa-calendar-alt',
            'color': '#fd7e14'
        },
        {
            'name': 'خودرو',
            'name_en': 'Automotive',
            'description': 'قالب‌های فروشگاه خودرو و خدمات خودرویی',
            'icon': 'fas fa-car',
            'color': '#6c757d'
        },
        {
            'name': 'زیبایی و مد',
            'name_en': 'Beauty & Fashion',
            'description': 'قالب‌های آرایشگاه، مد و زیبایی',
            'icon': 'fas fa-cut',
            'color': '#e83e8c'
        },
        {
            'name': 'ساخت و ساز',
            'name_en': 'Construction',
            'description': 'قالب‌های شرکت‌های ساختمانی و عمرانی',
            'icon': 'fas fa-hammer',
            'color': '#20c997'
        },
        {
            'name': 'کشاورزی',
            'name_en': 'Agriculture',
            'description': 'قالب‌های کشاورزی و محصولات کشاورزی',
            'icon': 'fas fa-seedling',
            'color': '#28a745'
        },
        {
            'name': 'صنایع دستی',
            'name_en': 'Handicrafts',
            'description': 'قالب‌های صنایع دستی و هنرهای سنتی',
            'icon': 'fas fa-palette',
            'color': '#fd7e14'
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = TemplateCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories[cat_data['name_en'].lower()] = category
        if created:
            print(f"دسته‌بندی '{cat_data['name']}' ایجاد شد.")
        else:
            print(f"دسته‌بندی '{cat_data['name']}' از قبل وجود دارد.")
    
    return categories

def load_templates_from_directory(base_path, categories):
    """بارگذاری قالب‌ها از پوشه"""
    templates_path = Path(base_path) / 'templates_library' / 'site_templates'
    
    if not templates_path.exists():
        print(f"مسیر {templates_path} وجود ندارد!")
        return
    
    # نگاشت نام پوشه‌ها به دسته‌بندی‌ها
    folder_to_category = {
        'business': 'business',
        'ecommerce': 'e-commerce',
        'restaurant': 'restaurant & food',
        'food-beverage': 'restaurant & food',
        'medical': 'health & medical',
        'health-wellness': 'health & medical',
        'education': 'education',
        'travel': 'travel & tourism',
        'events-arts': 'events & arts',
        'automotive': 'automotive',
        'beauty-fashion': 'beauty & fashion',
        'construction': 'construction',
        'agriculture': 'agriculture',
        'handicrafts': 'handicrafts',
        'retail': 'business',
        'retail-shopping': 'e-commerce',
        'user-dashboard': 'business',
        'template-manager': 'business',
        'image-manager': 'business',
        'assets': 'business'
    }
    
    for folder in templates_path.iterdir():
        if folder.is_dir() and folder.name != '__pycache__':
            category_name = folder_to_category.get(folder.name, 'business')
            category = categories.get(category_name)
            
            if not category:
                print(f"دسته‌بندی برای '{folder.name}' پیدا نشد. از 'business' استفاده می‌کنم.")
                category = categories.get('business')
            
            # بررسی فایل‌های HTML در پوشه
            html_files = list(folder.glob('*.html'))
            
            for html_file in html_files:
                template_name = html_file.stem.replace('_', ' ').title()
                
                # خواندن محتوای HTML
                try:
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(html_file, 'r', encoding='latin-1') as f:
                            html_content = f.read()
                    except:
                        print(f"خطا در خواندن فایل {html_file}")
                        continue
                
                # ایجاد قالب
                template, created = SiteTemplate.objects.get_or_create(
                    name=template_name,
                    category=category,
                    defaults={
                        'description': f'قالب {template_name} برای {category.name}',
                        'html_content': html_content,
                        'status': 'active',
                        'is_free': True,
                        'tags': [folder.name, category.name_en.lower()],
                        'metadata': {
                            'source_folder': folder.name,
                            'file_path': str(html_file),
                            'file_size': html_file.stat().st_size
                        }
                    }
                )
                
                if created:
                    print(f"قالب '{template_name}' در دسته '{category.name}' ایجاد شد.")
                else:
                    print(f"قالب '{template_name}' از قبل وجود دارد.")

def main():
    """تابع اصلی"""
    print("شروع بارگذاری قالب‌ها...")
    
    # ایجاد دسته‌بندی‌ها
    categories = create_categories()
    
    # بارگذاری قالب‌ها
    base_path = Path(__file__).resolve().parent.parent.parent.parent.parent
    load_templates_from_directory(base_path, categories)
    
    print("بارگذاری قالب‌ها تکمیل شد!")
    
    # نمایش آمار
    total_templates = SiteTemplate.objects.count()
    total_categories = TemplateCategory.objects.count()
    print(f"\nآمار:")
    print(f"- تعداد قالب‌ها: {total_templates}")
    print(f"- تعداد دسته‌بندی‌ها: {total_categories}")

if __name__ == '__main__':
    main()
