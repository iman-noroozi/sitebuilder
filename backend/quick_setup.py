#!/usr/bin/env python3
"""
Quick Django Setup & Test Script
راه‌اندازی سریع Django برای تست Frontend
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def setup_django():
    """راه‌اندازی Django"""
    print("🚀 راه‌اندازی Django...")
    
    # تنظیم مسیر
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    try:
        django.setup()
        print("✅ Django راه‌اندازی شد")
        return True
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی Django: {e}")
        return False

def run_migrations():
    """اجرای migrations"""
    print("📊 اجرای migrations...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations اجرا شد")
        return True
    except Exception as e:
        print(f"❌ خطا در migrations: {e}")
        return False

def create_superuser():
    """ایجاد superuser"""
    print("👤 ایجاد superuser...")
    
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            print("✅ Superuser ایجاد شد (admin/admin)")
        else:
            print("ℹ️ Superuser از قبل موجود است")
        return True
    except Exception as e:
        print(f"❌ خطا در ایجاد superuser: {e}")
        return False

def create_sample_data():
    """ایجاد داده‌های نمونه"""
    print("📝 ایجاد داده‌های نمونه...")
    
    try:
        from django.contrib.auth.models import User
        from sitebuilder_app.models import ExtractedTemplate, GeneratedSite
        
        # کاربر نمونه
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass')
            user.save()
        
        # قالب‌های نمونه
        templates_data = [
            {
                'title': 'Bootstrap Carousel',
                'url': 'https://getbootstrap.com/docs/5.3/examples/carousel/',
                'status': 'completed',
                'metadata': {
                    'title': 'Bootstrap Carousel Example',
                    'files': {'scripts': 2, 'images': 1, 'fonts': 0}
                }
            },
            {
                'title': 'Example Domain',
                'url': 'https://example.com',
                'status': 'completed',
                'metadata': {
                    'title': 'IANA-managed Reserved Domains',
                    'files': {'scripts': 2, 'images': 1, 'fonts': 6}
                }
            }
        ]
        
        for template_data in templates_data:
            template, created = ExtractedTemplate.objects.get_or_create(
                url=template_data['url'],
                defaults={
                    'user': user,
                    'title': template_data['title'],
                    'status': template_data['status'],
                    'metadata': template_data['metadata']
                }
            )
            if created:
                print(f"✅ قالب ایجاد شد: {template.title}")
        
        # سایت نمونه
        site_data = {
            'name': 'سایت نمونه',
            'domain': 'example.local',
            'description': 'یک سایت نمونه برای تست'
        }
        
        if templates := ExtractedTemplate.objects.filter(status='completed').first():
            site, created = GeneratedSite.objects.get_or_create(
                domain=site_data['domain'],
                defaults={
                    'user': user,
                    'template': templates,
                    'name': site_data['name'],
                    'description': site_data['description']
                }
            )
            if created:
                print(f"✅ سایت ایجاد شد: {site.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در ایجاد داده‌های نمونه: {e}")
        return False

def test_api_endpoints():
    """تست API endpoints"""
    print("🧪 تست API endpoints...")
    
    try:
        from django.test import Client
        from django.contrib.auth.models import User
        
        client = Client()
        
        # تست بدون احراز هویت
        response = client.get('/sitebuilder/api/templates/')
        print(f"Templates API (بدون احراز): {response.status_code}")
        
        # تست با احراز هویت
        user = User.objects.get(username='admin')
        client.force_login(user)
        
        response = client.get('/sitebuilder/api/templates/')
        print(f"Templates API (با احراز): {response.status_code}")
        
        response = client.get('/sitebuilder/api/sites/')
        print(f"Sites API: {response.status_code}")
        
        response = client.get('/sitebuilder/api/jobs/')
        print(f"Jobs API: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست API: {e}")
        return False

def run_server():
    """اجرای Django server"""
    print("🌐 اجرای Django server...")
    print("📍 Server در آدرس http://localhost:8000 اجرا خواهد شد")
    print("📍 Admin panel: http://localhost:8000/admin (admin/admin)")
    print("📍 API: http://localhost:8000/sitebuilder/api/")
    print("🔄 برای متوقف کردن: Ctrl+C")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\n👋 سرور متوقف شد")

def main():
    """اجرای اصلی"""
    print("=" * 50)
    print("🏗️  SiteBuilder Django Setup")
    print("=" * 50)
    
    # مراحل راه‌اندازی
    steps = [
        ("راه‌اندازی Django", setup_django),
        ("اجرای Migrations", run_migrations),
        ("ایجاد Superuser", create_superuser),
        ("ایجاد داده‌های نمونه", create_sample_data),
        ("تست API Endpoints", test_api_endpoints),
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if step_func():
            success_count += 1
        else:
            break
    
    print(f"\n📊 {success_count}/{len(steps)} مرحله با موفقیت انجام شد")
    
    if success_count == len(steps):
        print("\n🎉 همه چیز آماده است!")
        
        # پرسیدن برای اجرای سرور
        response = input("\n❓ آیا می‌خواهید سرور را اجرا کنید؟ (y/n): ")
        if response.lower() in ['y', 'yes', 'بله', '1']:
            run_server()
    else:
        print("\n⚠️ برخی مراحل ناموفق بودند. لطفاً خطاها را بررسی کنید.")

if __name__ == '__main__':
    main()
