#!/usr/bin/env python3
"""
🏗️ Site Builder - مدیریت پروژه
سیستم کامل سایت‌سازی و استخراج قالب‌ها
"""

import os
import sys
import django
from pathlib import Path

def setup_django():
    """راه‌اندازی Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()

def main():
    """تابع اصلی"""
    if len(sys.argv) < 2:
        print("""
🏗️ Site Builder - سیستم مدیریت پروژه

دستورات موجود:
  python manage.py runserver     - راه‌اندازی سرور توسعه
  python manage.py migrate       - اجرای migrations
  python manage.py collectstatic - جمع‌آوری فایل‌های استاتیک
  python manage.py extract       - استخراج قالب‌ها
  python manage.py build         - ساخت سایت
  python manage.py test          - اجرای تست‌ها
  python manage.py setup         - راه‌اندازی اولیه
        """)
        return
    
    command = sys.argv[1]
    
    if command == 'runserver':
        setup_django()
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    
    elif command == 'migrate':
        setup_django()
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
    
    elif command == 'collectstatic':
        setup_django()
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    elif command == 'extract':
        from extractor.puppeteer import TemplateExtractor
        if len(sys.argv) < 4:
            print("استفاده: python manage.py extract <URL> <output_dir>")
            return
        url = sys.argv[2]
        output_dir = sys.argv[3]
        extractor = TemplateExtractor()
        extractor.extract_template(url, output_dir)
    
    elif command == 'build':
        from builder_core.build_engine import SiteBuilder
        if len(sys.argv) < 4:
            print("استفاده: python manage.py build <template_dir> <output_dir>")
            return
        template_dir = sys.argv[2]
        output_dir = sys.argv[3]
        builder = SiteBuilder()
        builder.build_site_from_template(template_dir, output_dir)
    
    elif command == 'test':
        setup_django()
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'test'])
    
    elif command == 'setup':
        print("🚀 راه‌اندازی اولیه Site Builder...")
        setup_django()
        
        # ایجاد دیتابیس
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        
        # ایجاد superuser
        print("👤 ایجاد کاربر مدیر...")
        execute_from_command_line(['manage.py', 'createsuperuser'])
        
        # جمع‌آوری فایل‌های استاتیک
        print("📦 جمع‌آوری فایل‌های استاتیک...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("✅ راه‌اندازی کامل شد!")
        print("🌐 برای شروع: python manage.py runserver")
    
    else:
        print(f"❌ دستور نامشخص: {command}")

if __name__ == '__main__':
    main()
