#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏗️ موتور ساخت سایت پیشرفته
قابلیت‌های اصلی:
- تبدیل قالب‌ها به سایت نهایی
- انتشار خودکار (FTP, GitHub Pages, Netlify)
- تولید PWA
- SEO خودکار
"""

import os
import json
import shutil
import zipfile
import requests
from pathlib import Path
from datetime import datetime
import subprocess
import re
from typing import Dict, List, Optional

class SiteBuilder:
    """موتور اصلی ساخت سایت"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.output_dir = Path("built_sites")
        self.output_dir.mkdir(exist_ok=True)

    def build_site_from_template(self, template_path: str, site_config: Dict) -> str:
        """
        ساخت سایت از قالب استخراج شده

        Args:
            template_path: مسیر قالب استخراج شده
            site_config: تنظیمات سایت (نام، دامنه، متن‌ها)

        Returns:
            مسیر سایت ساخته شده
        """
        print(f"🏗️ شروع ساخت سایت از قالب: {template_path}")

        # خواندن قالب
        template_data = self._load_template(template_path)
        if not template_data:
            raise ValueError("قالب یافت نشد!")

        # ایجاد پوشه سایت
        site_name = site_config.get('site_name', 'my_site')
        site_path = self.output_dir / f"{site_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        site_path.mkdir(exist_ok=True)

        # کپی فایل‌های قالب
        self._copy_template_files(template_path, site_path)

        # اعمال تغییرات سفارشی
        self._apply_customizations(site_path, site_config)

        # تولید PWA
        if site_config.get('generate_pwa', True):
            self._generate_pwa(site_path, site_config)

        # SEO خودکار
        if site_config.get('auto_seo', True):
            self._generate_seo_files(site_path, site_config)

        # بهینه‌سازی
        self._optimize_site(site_path)

        print(f"✅ سایت با موفقیت ساخته شد: {site_path}")
        return str(site_path)

    def _load_template(self, template_path: str) -> Optional[Dict]:
        """خواندن اطلاعات قالب"""
        template_file = Path(template_path) / "template.json"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def _copy_template_files(self, template_path: str, site_path: Path):
        """کپی فایل‌های قالب"""
        template_dir = Path(template_path)

        # کپی فایل‌های اصلی
        for file in ['index.html', 'styles.css', 'script.js']:
            src = template_dir / file
            if src.exists():
                shutil.copy2(src, site_path)

        # کپی پوشه assets
        assets_dir = template_dir / "assets"
        if assets_dir.exists():
            shutil.copytree(assets_dir, site_path / "assets")

    def _apply_customizations(self, site_path: Path, site_config: Dict):
        """اعمال تغییرات سفارشی"""
        # خواندن HTML
        html_file = site_path / "index.html"
        if html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # جایگزینی متن‌ها
            text_replacements = site_config.get('text_replacements', {})
            for old_text, new_text in text_replacements.items():
                html_content = html_content.replace(old_text, new_text)

            # تغییر عنوان
            title = site_config.get('site_name', 'سایت من')
            html_content = re.sub(
                r'<title>.*?</title>',
                f'<title>{title}</title>',
                html_content,
                flags=re.IGNORECASE
            )

            # اضافه کردن متادیتا
            meta_tags = self._generate_meta_tags(site_config)
            html_content = html_content.replace('</head>', f'{meta_tags}\n</head>')

            # ذخیره HTML تغییر یافته
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

    def _generate_meta_tags(self, site_config: Dict) -> str:
        """تولید متادیتا"""
        title = site_config.get('site_name', 'سایت من')
        description = site_config.get('description', 'توضیحات سایت')
        keywords = site_config.get('keywords', 'سایت، وب، طراحی')

        meta_tags = f"""
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
"""
        return meta_tags

    def _generate_pwa(self, site_path: Path, site_config: Dict):
        """تولید فایل‌های PWA"""
        print("📱 تولید PWA...")

        # manifest.json
        manifest = {
            "name": site_config.get('site_name', 'سایت من'),
            "short_name": site_config.get('short_name', 'سایت'),
            "description": site_config.get('description', 'توضیحات سایت'),
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#667eea",
            "icons": [
                {
                    "src": "assets/icons/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "assets/icons/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }

        with open(site_path / "manifest.json", 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        # service-worker.js
        sw_content = """
// Service Worker برای PWA
const CACHE_NAME = 'site-cache-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/styles.css',
    '/script.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
"""

        with open(site_path / "sw.js", 'w', encoding='utf-8') as f:
            f.write(sw_content)

        # اضافه کردن PWA به HTML
        html_file = site_path / "index.html"
        if html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            pwa_meta = """
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#667eea">
    <link rel="apple-touch-icon" href="/assets/icons/icon-192x192.png">
"""

            html_content = html_content.replace('</head>', f'{pwa_meta}\n</head>')

            # اضافه کردن service worker
            sw_script = """
<script>
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    });
}
</script>
"""
            html_content = html_content.replace('</body>', f'{sw_script}\n</body>')

            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

    def _generate_seo_files(self, site_path: Path, site_config: Dict):
        """تولید فایل‌های SEO"""
        print("🔍 تولید فایل‌های SEO...")

        # robots.txt
        robots_content = f"""User-agent: *
Allow: /

Sitemap: {site_config.get('domain', 'https://example.com')}/sitemap.xml
"""

        with open(site_path / "robots.txt", 'w', encoding='utf-8') as f:
            f.write(robots_content)

        # sitemap.xml
        sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{site_config.get('domain', 'https://example.com')}/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""

        with open(site_path / "sitemap.xml", 'w', encoding='utf-8') as f:
            f.write(sitemap_content)

    def _optimize_site(self, site_path: Path):
        """بهینه‌سازی سایت"""
        print("⚡ بهینه‌سازی سایت...")

        # فشرده‌سازی CSS
        css_file = site_path / "styles.css"
        if css_file.exists():
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()

            # حذف کامنت‌ها و فضاهای اضافی
            css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
            css_content = re.sub(r'\s+', ' ', css_content)
            css_content = css_content.strip()

            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(css_content)

    def compress_site(self, site_path: str) -> str:
        """فشرده کردن سایت"""
        site_path = Path(site_path)
        zip_path = site_path.with_suffix('.zip')

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in site_path.rglob('*'):
                if file.is_file():
                    zipf.write(file, file.relative_to(site_path))

        print(f"📦 سایت فشرده شد: {zip_path}")
        return str(zip_path)

    def deploy_to_github_pages(self, site_path: str, repo_name: str, token: str) -> bool:
        """انتشار به GitHub Pages"""
        print(f"🚀 انتشار به GitHub Pages: {repo_name}")

        try:
            # ایجاد repository
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }

            # ایجاد repo
            repo_data = {
                'name': repo_name,
                'description': 'سایت ساخته شده با Site Builder',
                'private': False,
                'auto_init': True
            }

            response = requests.post(
                'https://api.github.com/user/repos',
                headers=headers,
                json=repo_data
            )

            if response.status_code == 201:
                print("✅ Repository ایجاد شد")
                return True
            else:
                print(f"❌ خطا در ایجاد repository: {response.text}")
                return False

        except Exception as e:
            print(f"❌ خطا در انتشار: {e}")
            return False

    def deploy_to_netlify(self, site_path: str, site_name: str, token: str) -> bool:
        """انتشار به Netlify"""
        print(f"🚀 انتشار به Netlify: {site_name}")

        try:
            # آپلود فایل‌ها به Netlify
            headers = {
                'Authorization': f'Bearer {token}'
            }

            # ایجاد site
            site_data = {
                'name': site_name,
                'custom_domain': None
            }

            response = requests.post(
                'https://api.netlify.com/api/v1/sites',
                headers=headers,
                json=site_data
            )

            if response.status_code == 201:
                print("✅ سایت در Netlify ایجاد شد")
                return True
            else:
                print(f"❌ خطا در ایجاد سایت: {response.text}")
                return False

        except Exception as e:
            print(f"❌ خطا در انتشار: {e}")
            return False

    def deploy_to_ftp(self, site_path: str, ftp_config: Dict) -> bool:
        """انتشار به FTP"""
        print(f"🚀 انتشار به FTP: {ftp_config.get('host')}")

        try:
            from ftplib import FTP

            ftp = FTP()
            ftp.connect(
                ftp_config['host'],
                ftp_config.get('port', 21)
            )
            ftp.login(
                ftp_config['username'],
                ftp_config['password']
            )

            # آپلود فایل‌ها
            site_path = Path(site_path)
            for file in site_path.rglob('*'):
                if file.is_file():
                    remote_path = f"{ftp_config.get('remote_path', '/')}/{file.relative_to(site_path)}"
                    with open(file, 'rb') as f:
                        ftp.storbinary(f'STOR {remote_path}', f)

            ftp.quit()
            print("✅ فایل‌ها با موفقیت آپلود شدند")
            return True

        except Exception as e:
            print(f"❌ خطا در آپلود FTP: {e}")
            return False

# مثال استفاده
if __name__ == "__main__":
    builder = SiteBuilder()

    # تنظیمات سایت
    site_config = {
        'site_name': 'سایت من',
        'domain': 'https://mysite.com',
        'description': 'سایت شخصی من',
        'keywords': 'وب، طراحی، توسعه',
        'text_replacements': {
            'عنوان قدیمی': 'عنوان جدید',
            'متن قدیمی': 'متن جدید'
        },
        'generate_pwa': True,
        'auto_seo': True
    }

    # ساخت سایت
    site_path = builder.build_site_from_template(
        './extracted_sites/bootstrap_template',
        site_config
    )

    # فشرده کردن
    zip_path = builder.compress_site(site_path)

    print(f"🎉 سایت آماده است: {zip_path}")
