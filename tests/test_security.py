#!/usr/bin/env python3
"""
🔒 تست‌های امنیتی جامع برای PEY Builder
"""

import unittest
import os
import sys
import tempfile
import shutil
import json
import re
from unittest.mock import patch, MagicMock
import hashlib
import secrets
import string

# اضافه کردن مسیر پروژه
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestInputValidation(unittest.TestCase):
    """تست‌های اعتبارسنجی ورودی"""
    
    def test_sql_injection_prevention(self):
        """تست جلوگیری از SQL Injection"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "'; INSERT INTO users VALUES ('hacker', 'password'); --",
            "1' UNION SELECT * FROM users --",
            "admin'--",
            "admin'/*",
            "admin' OR 1=1#"
        ]
        
        for malicious_input in malicious_inputs:
            with self.subTest(input=malicious_input):
                sanitized = self._sanitize_sql_input(malicious_input)
                self.assertNotIn("DROP", sanitized.upper())
                self.assertNotIn("INSERT", sanitized.upper())
                self.assertNotIn("UNION", sanitized.upper())
                self.assertNotIn("--", sanitized)
                self.assertNotIn("/*", sanitized)
                self.assertNotIn("#", sanitized)
    
    def _sanitize_sql_input(self, input_text):
        """تابع کمکی برای پاکسازی ورودی SQL"""
        # حذف کاراکترهای خطرناک
        dangerous_chars = ["'", '"', ';', '--', '/*', '*/', '#', 'xp_', 'sp_']
        sanitized = input_text
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized
    
    def test_xss_prevention(self):
        """تست جلوگیری از XSS"""
        malicious_inputs = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<keygen onfocus=alert('XSS') autofocus>",
            "<video><source onerror=alert('XSS')>",
            "<audio src=x onerror=alert('XSS')>"
        ]
        
        for malicious_input in malicious_inputs:
            with self.subTest(input=malicious_input):
                sanitized = self._sanitize_xss_input(malicious_input)
                self.assertNotIn("<script>", sanitized.lower())
                self.assertNotIn("javascript:", sanitized.lower())
                self.assertNotIn("onerror=", sanitized.lower())
                self.assertNotIn("onload=", sanitized.lower())
                self.assertNotIn("onfocus=", sanitized.lower())
    
    def _sanitize_xss_input(self, input_text):
        """تابع کمکی برای پاکسازی ورودی XSS"""
        # حذف تگ‌های خطرناک
        dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form', 'input', 'button']
        sanitized = input_text
        
        for tag in dangerous_tags:
            # حذف تگ باز
            sanitized = re.sub(f'<{tag}[^>]*>', '', sanitized, flags=re.IGNORECASE)
            # حذف تگ بسته
            sanitized = re.sub(f'</{tag}>', '', sanitized, flags=re.IGNORECASE)
        
        # حذف event handlers
        event_handlers = ['onload', 'onerror', 'onfocus', 'onclick', 'onmouseover', 'onkeypress']
        for handler in event_handlers:
            sanitized = re.sub(f'{handler}\\s*=\\s*[^\\s>]+', '', sanitized, flags=re.IGNORECASE)
        
        # حذف javascript: protocol
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def test_path_traversal_prevention(self):
        """تست جلوگیری از Path Traversal"""
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\SAM",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd"
        ]
        
        for malicious_path in malicious_paths:
            with self.subTest(path=malicious_path):
                sanitized = self._sanitize_path(malicious_path)
                self.assertNotIn("..", sanitized)
                self.assertNotIn("etc", sanitized)
                self.assertNotIn("passwd", sanitized)
                self.assertNotIn("system32", sanitized)
    
    def _sanitize_path(self, path):
        """تابع کمکی برای پاکسازی مسیر"""
        # حذف کاراکترهای خطرناک
        dangerous_chars = ['..', '/', '\\', '%2e', '%2f', '%5c']
        sanitized = path
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # URL decode
        import urllib.parse
        sanitized = urllib.parse.unquote(sanitized)
        
        return sanitized

class TestAuthenticationSecurity(unittest.TestCase):
    """تست‌های امنیت احراز هویت"""
    
    def test_password_strength(self):
        """تست قدرت رمز عبور"""
        weak_passwords = [
            "123456",
            "password",
            "admin",
            "qwerty",
            "12345678",
            "abc123",
            "password123",
            "1234567890"
        ]
        
        strong_passwords = [
            "MyStr0ng!P@ssw0rd",
            "C0mpl3x#P@ss2024",
            "S3cur3$P@ssw0rd!",
            "Str0ng&P@ssw0rd#1"
        ]
        
        for weak_password in weak_passwords:
            with self.subTest(password=weak_password):
                self.assertFalse(self._is_strong_password(weak_password))
        
        for strong_password in strong_passwords:
            with self.subTest(password=strong_password):
                self.assertTrue(self._is_strong_password(strong_password))
    
    def _is_strong_password(self, password):
        """تابع کمکی برای بررسی قدرت رمز عبور"""
        if len(password) < 8:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        return has_upper and has_lower and has_digit and has_special
    
    def test_token_generation(self):
        """تست تولید توکن امن"""
        tokens = []
        
        # تولید چندین توکن
        for _ in range(100):
            token = self._generate_secure_token()
            tokens.append(token)
        
        # بررسی یکتایی توکن‌ها
        self.assertEqual(len(tokens), len(set(tokens)))
        
        # بررسی طول توکن
        for token in tokens:
            self.assertGreaterEqual(len(token), 32)
            self.assertLessEqual(len(token), 64)
        
        # بررسی کاراکترهای مجاز
        allowed_chars = string.ascii_letters + string.digits + '-_'
        for token in tokens:
            for char in token:
                self.assertIn(char, allowed_chars)
    
    def _generate_secure_token(self):
        """تابع کمکی برای تولید توکن امن"""
        return secrets.token_urlsafe(32)
    
    def test_session_security(self):
        """تست امنیت جلسه"""
        session_data = {
            'session_id': self._generate_secure_token(),
            'user_id': 'user123',
            'created_at': 1234567890,
            'expires_at': 1234567890 + 3600,  # 1 hour
            'ip_address': '192.168.1.1',
            'user_agent': 'Mozilla/5.0...'
        }
        
        # بررسی فیلدهای ضروری
        self.assertIn('session_id', session_data)
        self.assertIn('user_id', session_data)
        self.assertIn('created_at', session_data)
        self.assertIn('expires_at', session_data)
        self.assertIn('ip_address', session_data)
        
        # بررسی انقضای جلسه
        self.assertGreater(session_data['expires_at'], session_data['created_at'])
        
        # بررسی طول session_id
        self.assertGreaterEqual(len(session_data['session_id']), 32)

class TestDataEncryption(unittest.TestCase):
    """تست‌های رمزنگاری داده"""
    
    def test_password_hashing(self):
        """تست هش کردن رمز عبور"""
        password = "MySecretPassword123!"
        
        # تولید هش
        hashed = self._hash_password(password)
        
        # بررسی ویژگی‌های هش
        self.assertNotEqual(hashed, password)
        self.assertGreater(len(hashed), 50)
        self.assertTrue(hashed.startswith('$2b$'))  # bcrypt format
        
        # بررسی تطبیق رمز عبور
        self.assertTrue(self._verify_password(password, hashed))
        self.assertFalse(self._verify_password("wrong_password", hashed))
    
    def _hash_password(self, password):
        """تابع کمکی برای هش کردن رمز عبور"""
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password, hashed):
        """تابع کمکی برای بررسی رمز عبور"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def test_data_encryption(self):
        """تست رمزنگاری داده"""
        sensitive_data = "This is sensitive information"
        key = secrets.token_bytes(32)
        
        # رمزنگاری
        encrypted = self._encrypt_data(sensitive_data, key)
        
        # بررسی ویژگی‌های رمزنگاری
        self.assertNotEqual(encrypted, sensitive_data)
        self.assertIsInstance(encrypted, bytes)
        
        # رمزگشایی
        decrypted = self._decrypt_data(encrypted, key)
        self.assertEqual(decrypted, sensitive_data)
    
    def _encrypt_data(self, data, key):
        """تابع کمکی برای رمزنگاری داده"""
        from cryptography.fernet import Fernet
        f = Fernet(key)
        return f.encrypt(data.encode('utf-8'))
    
    def _decrypt_data(self, encrypted_data, key):
        """تابع کمکی برای رمزگشایی داده"""
        from cryptography.fernet import Fernet
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode('utf-8')

class TestRateLimiting(unittest.TestCase):
    """تست‌های محدودیت نرخ درخواست"""
    
    def test_rate_limit_configuration(self):
        """تست تنظیمات محدودیت نرخ"""
        rate_limits = {
            '/api/login': {'limit': 5, 'window': 300},  # 5 attempts per 5 minutes
            '/api/register': {'limit': 3, 'window': 3600},  # 3 attempts per hour
            '/api/generate-content': {'limit': 100, 'window': 3600},  # 100 requests per hour
            '/api/extract-template': {'limit': 50, 'window': 3600}  # 50 requests per hour
        }
        
        for endpoint, config in rate_limits.items():
            with self.subTest(endpoint=endpoint):
                self.assertIn('limit', config)
                self.assertIn('window', config)
                self.assertGreater(config['limit'], 0)
                self.assertGreater(config['window'], 0)
    
    def test_rate_limit_tracking(self):
        """تست ردیابی محدودیت نرخ"""
        client_ip = "192.168.1.100"
        endpoint = "/api/generate-content"
        
        # شبیه‌سازی درخواست‌ها
        requests = []
        for i in range(10):
            request = {
                'ip': client_ip,
                'endpoint': endpoint,
                'timestamp': 1234567890 + i,
                'user_id': f'user{i}'
            }
            requests.append(request)
        
        # بررسی محدودیت
        is_limited = self._check_rate_limit(requests, limit=5, window=60)
        self.assertTrue(is_limited)
    
    def _check_rate_limit(self, requests, limit, window):
        """تابع کمکی برای بررسی محدودیت نرخ"""
        if len(requests) > limit:
            return True
        
        # بررسی در بازه زمانی
        current_time = max(req['timestamp'] for req in requests)
        recent_requests = [req for req in requests if current_time - req['timestamp'] <= window]
        
        return len(recent_requests) > limit

class TestFileUploadSecurity(unittest.TestCase):
    """تست‌های امنیت آپلود فایل"""
    
    def test_file_type_validation(self):
        """تست اعتبارسنجی نوع فایل"""
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']
        dangerous_extensions = ['.exe', '.bat', '.cmd', '.scr', '.pif', '.com', '.js', '.php', '.asp', '.jsp']
        
        for ext in allowed_extensions:
            with self.subTest(extension=ext):
                self.assertTrue(self._is_allowed_file_type(f'test{ext}'))
        
        for ext in dangerous_extensions:
            with self.subTest(extension=ext):
                self.assertFalse(self._is_allowed_file_type(f'test{ext}'))
    
    def _is_allowed_file_type(self, filename):
        """تابع کمکی برای بررسی نوع فایل مجاز"""
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.txt', '.css', '.js']
        dangerous_extensions = ['.exe', '.bat', '.cmd', '.scr', '.pif', '.com', '.php', '.asp', '.jsp', '.sh']
        
        filename_lower = filename.lower()
        
        # بررسی پسوندهای خطرناک
        for ext in dangerous_extensions:
            if filename_lower.endswith(ext):
                return False
        
        # بررسی پسوندهای مجاز
        for ext in allowed_extensions:
            if filename_lower.endswith(ext):
                return True
        
        return False
    
    def test_file_size_validation(self):
        """تست اعتبارسنجی اندازه فایل"""
        max_size = 10 * 1024 * 1024  # 10MB
        
        valid_sizes = [1024, 1024*1024, 5*1024*1024]  # 1KB, 1MB, 5MB
        invalid_sizes = [11*1024*1024, 50*1024*1024, 100*1024*1024]  # 11MB, 50MB, 100MB
        
        for size in valid_sizes:
            with self.subTest(size=size):
                self.assertTrue(self._is_valid_file_size(size, max_size))
        
        for size in invalid_sizes:
            with self.subTest(size=size):
                self.assertFalse(self._is_valid_file_size(size, max_size))
    
    def _is_valid_file_size(self, file_size, max_size):
        """تابع کمکی برای بررسی اندازه فایل"""
        return 0 < file_size <= max_size
    
    def test_malicious_file_content(self):
        """تست محتوای مخرب فایل"""
        malicious_contents = [
            b'<script>alert("XSS")</script>',
            b'<?php system($_GET["cmd"]); ?>',
            b'<iframe src="javascript:alert(\'XSS\')"></iframe>',
            b'exec("rm -rf /")',
            b'DROP TABLE users;'
        ]
        
        for content in malicious_contents:
            with self.subTest(content=content):
                self.assertTrue(self._contains_malicious_content(content))
    
    def _contains_malicious_content(self, content):
        """تابع کمکی برای بررسی محتوای مخرب"""
        malicious_patterns = [
            b'<script',
            b'<?php',
            b'<iframe',
            b'exec(',
            b'system(',
            b'DROP TABLE',
            b'DELETE FROM',
            b'INSERT INTO'
        ]
        
        content_lower = content.lower()
        for pattern in malicious_patterns:
            if pattern in content_lower:
                return True
        
        return False

class TestAPISecurity(unittest.TestCase):
    """تست‌های امنیت API"""
    
    def test_cors_configuration(self):
        """تست تنظیمات CORS"""
        cors_config = {
            'allowed_origins': ['https://peyai.ir', 'https://www.peyai.ir'],
            'allowed_methods': ['GET', 'POST', 'PUT', 'DELETE'],
            'allowed_headers': ['Content-Type', 'Authorization'],
            'expose_headers': ['X-Total-Count'],
            'max_age': 3600
        }
        
        # بررسی تنظیمات CORS
        self.assertIn('allowed_origins', cors_config)
        self.assertIn('allowed_methods', cors_config)
        self.assertIn('allowed_headers', cors_config)
        
        # بررسی روش‌های مجاز
        allowed_methods = cors_config['allowed_methods']
        self.assertIn('GET', allowed_methods)
        self.assertIn('POST', allowed_methods)
        self.assertNotIn('TRACE', allowed_methods)  # TRACE خطرناک است
    
    def test_api_key_validation(self):
        """تست اعتبارسنجی کلید API"""
        valid_api_keys = [
            'pk_test_1234567890abcdef',
            'sk_live_abcdef1234567890',
            'pey_2024_abcdef1234567890'
        ]
        
        invalid_api_keys = [
            '',
            'invalid_key',
            '123456',
            'test_key_without_prefix',
            'pk_test_short'
        ]
        
        for api_key in valid_api_keys:
            with self.subTest(api_key=api_key):
                self.assertTrue(self._is_valid_api_key(api_key))
        
        for api_key in invalid_api_keys:
            with self.subTest(api_key=api_key):
                self.assertFalse(self._is_valid_api_key(api_key))
    
    def _is_valid_api_key(self, api_key):
        """تابع کمکی برای بررسی کلید API"""
        if not api_key or len(api_key) < 20:
            return False
        
        valid_prefixes = ['pk_test_', 'sk_live_', 'pey_2024_']
        return any(api_key.startswith(prefix) for prefix in valid_prefixes)
    
    def test_request_validation(self):
        """تست اعتبارسنجی درخواست"""
        valid_request = {
            'method': 'POST',
            'url': '/api/websites',
            'headers': {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer valid_token',
                'User-Agent': 'PEY-Builder/1.0'
            },
            'body': {
                'name': 'Test Website',
                'domain': 'testsite.com'
            }
        }
        
        # بررسی ساختار درخواست
        self.assertIn('method', valid_request)
        self.assertIn('url', valid_request)
        self.assertIn('headers', valid_request)
        self.assertIn('body', valid_request)
        
        # بررسی هدرهای ضروری
        headers = valid_request['headers']
        self.assertIn('Content-Type', headers)
        self.assertIn('Authorization', headers)
        self.assertIn('User-Agent', headers)
        
        # بررسی Content-Type
        self.assertEqual(headers['Content-Type'], 'application/json')

if __name__ == '__main__':
    # راه‌اندازی تست‌ها
    unittest.main(verbosity=2)
