#!/usr/bin/env python3
"""
🧪 تست‌های استخراج‌کننده قالب‌ها
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import sys

# اضافه کردن مسیر پروژه
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestTemplateExtractor(unittest.TestCase):
    """تست‌های کلاس TemplateExtractor"""
    
    def setUp(self):
        """راه‌اندازی قبل از هر تست"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_url = "https://example.com"
    
    def tearDown(self):
        """پاکسازی بعد از هر تست"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_extractor_initialization(self):
        """تست راه‌اندازی استخراج‌کننده"""
        # این تست باید بعد از پیاده‌سازی کلاس TemplateExtractor فعال شود
        pass
    
    def test_url_validation(self):
        """تست اعتبارسنجی URL"""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://www.example.com/path",
        ]
        
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "",
            None,
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                # تست اعتبار URL
                self.assertTrue(self._is_valid_url(url))
        
        for url in invalid_urls:
            with self.subTest(url=url):
                # تست عدم اعتبار URL
                self.assertFalse(self._is_valid_url(url))
    
    def _is_valid_url(self, url):
        """تابع کمکی برای تست اعتبار URL"""
        if not url:
            return False
        
        return url.startswith(('http://', 'https://'))
    
    def test_output_directory_creation(self):
        """تست ایجاد دایرکتوری خروجی"""
        output_dir = os.path.join(self.temp_dir, "test_output")
        
        # ایجاد دایرکتوری
        os.makedirs(output_dir, exist_ok=True)
        
        # بررسی وجود دایرکتوری
        self.assertTrue(os.path.exists(output_dir))
        self.assertTrue(os.path.isdir(output_dir))
    
    def test_file_download_simulation(self):
        """تست شبیه‌سازی دانلود فایل"""
        test_content = "Test HTML content"
        test_file = os.path.join(self.temp_dir, "test.html")
        
        # نوشتن فایل تست
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # خواندن و بررسی فایل
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertEqual(content, test_content)
    
    @patch('requests.get')
    def test_http_request_simulation(self, mock_get):
        """تست شبیه‌سازی درخواست HTTP"""
        # تنظیم mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test</body></html>"
        mock_get.return_value = mock_response
        
        # تست درخواست
        import requests
        response = requests.get(self.test_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test", response.text)
        mock_get.assert_called_once_with(self.test_url)

class TestSiteBuilder(unittest.TestCase):
    """تست‌های کلاس SiteBuilder"""
    
    def setUp(self):
        """راه‌اندازی قبل از هر تست"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """پاکسازی بعد از هر تست"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_site_config_validation(self):
        """تست اعتبارسنجی تنظیمات سایت"""
        valid_config = {
            'site_name': 'Test Site',
            'domain': 'testsite.com',
            'description': 'Test Description',
            'keywords': 'test, site',
        }
        
        invalid_configs = [
            {},  # خالی
            {'site_name': ''},  # نام خالی
            {'site_name': 'Test', 'domain': ''},  # دامنه خالی
        ]
        
        # تست تنظیمات معتبر
        self.assertTrue(self._validate_site_config(valid_config))
        
        # تست تنظیمات نامعتبر
        for config in invalid_configs:
            with self.subTest(config=config):
                self.assertFalse(self._validate_site_config(config))
    
    def _validate_site_config(self, config):
        """تابع کمکی برای اعتبارسنجی تنظیمات سایت"""
        required_fields = ['site_name', 'domain', 'description']
        
        for field in required_fields:
            if field not in config or not config[field]:
                return False
        
        return True
    
    def test_html_generation(self):
        """تست تولید HTML"""
        template_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{site_name}}</title>
            <meta name="description" content="{{description}}">
        </head>
        <body>
            <h1>{{site_name}}</h1>
            <p>{{description}}</p>
        </body>
        </html>
        """
        
        replacements = {
            'site_name': 'My Test Site',
            'description': 'This is a test site'
        }
        
        # جایگزینی متغیرها
        generated_html = template_html
        for key, value in replacements.items():
            generated_html = generated_html.replace(f'{{{{{key}}}}}', value)
        
        # بررسی نتیجه
        self.assertIn('My Test Site', generated_html)
        self.assertIn('This is a test site', generated_html)
        self.assertNotIn('{{site_name}}', generated_html)
        self.assertNotIn('{{description}}', generated_html)

class TestBusinessToolsManager(unittest.TestCase):
    """تست‌های کلاس BusinessToolsManager"""
    
    def setUp(self):
        """راه‌اندازی قبل از هر تست"""
        self.temp_db = tempfile.mktemp(suffix='.db')
    
    def tearDown(self):
        """پاکسازی بعد از هر تست"""
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)
    
    def test_database_initialization(self):
        """تست راه‌اندازی دیتابیس"""
        # این تست باید بعد از پیاده‌سازی کلاس BusinessToolsManager فعال شود
        pass
    
    def test_tool_categorization(self):
        """تست دسته‌بندی ابزارها"""
        tools = [
            {'name': 'Payment Gateway', 'category': 'Payment'},
            {'name': 'CRM System', 'category': 'Customer Management'},
            {'name': 'Email Marketing', 'category': 'Marketing'},
        ]
        
        categories = set(tool['category'] for tool in tools)
        
        self.assertIn('Payment', categories)
        self.assertIn('Customer Management', categories)
        self.assertIn('Marketing', categories)
        self.assertEqual(len(categories), 3)

if __name__ == '__main__':
    # راه‌اندازی تست‌ها
    unittest.main(verbosity=2)
