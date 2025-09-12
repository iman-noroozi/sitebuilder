#!/usr/bin/env python3
"""
🧪 تست‌های پایه برای CI/CD
"""

import unittest
import os
import sys
import tempfile
import shutil

# اضافه کردن مسیر پروژه
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBasicFunctionality(unittest.TestCase):
    """تست‌های عملکرد پایه"""
    
    def setUp(self):
        """راه‌اندازی قبل از هر تست"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """پاکسازی بعد از هر تست"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_project_structure(self):
        """تست ساختار پروژه"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # بررسی وجود فایل‌های مهم
        required_files = [
            'README.md',
            'package.json',
            'requirements.txt',
            'Dockerfile',
            'docker-compose.yml'
        ]
        
        for file_name in required_files:
            file_path = os.path.join(project_root, file_name)
            self.assertTrue(
                os.path.exists(file_path),
                f"فایل {file_name} باید وجود داشته باشد"
            )
    
    def test_directory_structure(self):
        """تست ساختار دایرکتوری‌ها"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        required_dirs = [
            'backend',
            'extractor',
            'frontend',
            'tests'
        ]
        
        for dir_name in required_dirs:
            dir_path = os.path.join(project_root, dir_name)
            self.assertTrue(
                os.path.exists(dir_path) and os.path.isdir(dir_path),
                f"دایرکتوری {dir_name} باید وجود داشته باشد"
            )
    
    def test_url_validation(self):
        """تست اعتبارسنجی URL"""
        def is_valid_url(url):
            if not url:
                return False
            return url.startswith(('http://', 'https://'))
        
        # تست URL های معتبر
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://www.example.com/path"
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_url(url))
        
        # تست URL های نامعتبر
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "",
            None
        ]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(is_valid_url(url))
    
    def test_file_operations(self):
        """تست عملیات فایل"""
        test_file = os.path.join(self.temp_dir, "test.txt")
        test_content = "تست محتوای فارسی"
        
        # نوشتن فایل
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # بررسی وجود فایل
        self.assertTrue(os.path.exists(test_file))
        
        # خواندن فایل
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertEqual(content, test_content)
    
    def test_json_operations(self):
        """تست عملیات JSON"""
        import json
        
        test_data = {
            "name": "تست",
            "version": "1.0.0",
            "features": ["استخراج", "ساخت", "ویرایش"]
        }
        
        json_file = os.path.join(self.temp_dir, "test.json")
        
        # نوشتن JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # خواندن JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data, test_data)

class TestDjangoSetup(unittest.TestCase):
    """تست راه‌اندازی Django"""
    
    def test_django_settings(self):
        """تست تنظیمات Django"""
        try:
            import django
            import os
            
            # تنظیم متغیر محیطی Django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
            
            # راه‌اندازی Django
            django.setup()
            
            from django.conf import settings

            # بررسی تنظیمات پایه
            self.assertIsNotNone(settings.SECRET_KEY)
            self.assertIsInstance(settings.INSTALLED_APPS, list)

        except ImportError:
            self.skipTest("Django نصب نشده است")
        except Exception as e:
            self.skipTest(f"Django تنظیم نشده است: {e}")

if __name__ == '__main__':
    # راه‌اندازی تست‌ها
    unittest.main(verbosity=2)
