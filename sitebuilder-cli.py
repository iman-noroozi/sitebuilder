#!/usr/bin/env python3
"""
🚀 Site Builder CLI Tool - Global Edition
Advanced command-line tool for website extraction, analysis, and building
ابزار خط فرمان پیشرفته برای استخراج، تحلیل و ساخت سایت
"""

import argparse
import sys
import os
import json
import subprocess
import time
import requests
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
from concurrent.futures import ThreadPoolExecutor
import yaml

class SiteBuilderCLI:
    def __init__(self):
        self.version = "1.0.0"
        self.description = "Advanced Website Builder - Global Edition"
        self.supported_languages = ['en', 'fa', 'ar', 'es', 'fr', 'de', 'zh', 'ja', 'ko']
        self.supported_frameworks = ['bootstrap', 'tailwind', 'bulma', 'foundation', 'materialize', 'semantic']
        self.setup_logging()
    
    def setup_logging(self):
        """Setup advanced logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sitebuilder.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_robots_txt(self, url: str) -> bool:
        """Check robots.txt compliance"""
        try:
            robots_url = f"{url.rstrip('/')}/robots.txt"
            response = requests.get(robots_url, timeout=10)
            if response.status_code == 200:
                robots_content = response.text.lower()
                if 'disallow: /' in robots_content:
                    self.logger.warning(f"robots.txt disallows scraping for {url}")
                    return False
            return True
        except Exception as e:
            self.logger.warning(f"Could not check robots.txt: {e}")
            return True
    
    def detect_framework(self, html_content: str) -> str:
        """Detect CSS framework used"""
        frameworks = {
            'bootstrap': ['bootstrap', 'btn-', 'container', 'row', 'col-'],
            'tailwind': ['tailwind', 'tw-', 'bg-', 'text-', 'p-', 'm-'],
            'bulma': ['bulma', 'button', 'section', 'container', 'columns'],
            'foundation': ['foundation', 'button', 'row', 'column', 'grid-'],
            'materialize': ['materialize', 'btn', 'card', 'row', 'col'],
            'semantic': ['semantic', 'ui', 'button', 'segment', 'grid']
        }
        
        html_lower = html_content.lower()
        for framework, keywords in frameworks.items():
            if any(keyword in html_lower for keyword in keywords):
                return framework
        return 'custom'
    
    def analyze_performance(self, url: str) -> Dict[str, Any]:
        """Analyze website performance"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=30)
            load_time = time.time() - start_time
            
            return {
                'load_time': round(load_time, 2),
                'status_code': response.status_code,
                'content_length': len(response.content),
                'headers': dict(response.headers),
                'performance_score': self.calculate_performance_score(load_time, len(response.content))
            }
        except Exception as e:
            self.logger.error(f"Performance analysis failed: {e}")
            return {}
    
    def calculate_performance_score(self, load_time: float, content_size: int) -> int:
        """Calculate performance score (0-100)"""
        time_score = max(0, 100 - (load_time * 20))  # Penalty for slow loading
        size_score = max(0, 100 - (content_size / 10000))  # Penalty for large content
        return int((time_score + size_score) / 2)
    
    def extract(self, url, output_path, options=None):
        """استخراج قالب از URL"""
        print(f"🔍 شروع استخراج از: {url}")
        print(f"📁 مسیر خروجی: {output_path}")
        
        try:
            # اجرای Node.js extractor
            extractor_path = Path(__file__).parent / "extractor" / "puppeteer.js"
            
            if not extractor_path.exists():
                print("❌ فایل extractor یافت نشد!")
                return False
            
            cmd = [
                "node", 
                str(extractor_path),
                url,
                output_path
            ]
            
            if options and options.get('headless'):
                cmd.append('--headless')
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ استخراج با موفقیت انجام شد!")
                return True
            else:
                print(f"❌ خطا در استخراج: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ خطا: {e}")
            return False
    
    def analyze(self, input_path):
        """تحلیل قالب استخراج شده"""
        print(f"📊 تحلیل قالب در: {input_path}")
        
        try:
            input_path = Path(input_path)
            
            if not input_path.exists():
                print("❌ مسیر ورودی وجود ندارد!")
                return False
            
            # بررسی فایل‌های موجود
            files = {
                'html': input_path / 'index.html',
                'css': input_path / 'styles.css',
                'js': input_path / 'scripts.js',
                'metadata': input_path / 'metadata.json'
            }
            
            analysis = {
                'path': str(input_path),
                'files': {},
                'stats': {}
            }
            
            for file_type, file_path in files.items():
                if file_path.exists():
                    size = file_path.stat().st_size
                    analysis['files'][file_type] = {
                        'exists': True,
                        'size': size,
                        'size_kb': round(size / 1024, 2)
                    }
                else:
                    analysis['files'][file_type] = {'exists': False}
            
            # خواندن metadata اگر موجود باشد
            if files['metadata'].exists():
                with open(files['metadata'], 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    analysis['metadata'] = metadata
            
            # نمایش نتایج
            print("\n📋 نتایج تحلیل:")
            print(f"📁 مسیر: {analysis['path']}")
            
            for file_type, info in analysis['files'].items():
                if info['exists']:
                    print(f"✅ {file_type.upper()}: {info['size_kb']} KB")
                else:
                    print(f"❌ {file_type.upper()}: موجود نیست")
            
            if 'metadata' in analysis:
                meta = analysis['metadata']
                print(f"\n📊 آمار:")
                print(f"  - عنوان: {meta.get('title', 'نامشخص')}")
                print(f"  - URL: {meta.get('url', 'نامشخص')}")
                print(f"  - تاریخ استخراج: {meta.get('extractedAt', 'نامشخص')}")
                print(f"  - تعداد استایل‌ها: {meta.get('styles', 0)}")
                print(f"  - تعداد اسکریپت‌ها: {meta.get('scripts', 0)}")
                print(f"  - تعداد تصاویر: {meta.get('images', 0)}")
                print(f"  - تعداد فونت‌ها: {meta.get('fonts', 0)}")
            
            return True
            
        except Exception as e:
            print(f"❌ خطا در تحلیل: {e}")
            return False
    
    def build(self, input_path, output_path, options=None):
        """ساخت سایت از قالب"""
        print(f"🏗️ ساخت سایت از: {input_path}")
        print(f"📁 مسیر خروجی: {output_path}")
        
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)
            
            if not input_path.exists():
                print("❌ مسیر ورودی وجود ندارد!")
                return False
            
            # ایجاد دایرکتوری خروجی
            output_path.mkdir(parents=True, exist_ok=True)
            
            # کپی فایل‌های اصلی
            files_to_copy = ['index.html', 'styles.css', 'scripts.js']
            
            for file_name in files_to_copy:
                src_file = input_path / file_name
                dst_file = output_path / file_name
                
                if src_file.exists():
                    import shutil
                    shutil.copy2(src_file, dst_file)
                    print(f"✅ کپی شد: {file_name}")
                else:
                    print(f"⚠️ فایل یافت نشد: {file_name}")
            
            # کپی تصاویر و فونت‌ها
            for asset_dir in ['images', 'fonts']:
                src_assets = input_path / asset_dir
                dst_assets = output_path / asset_dir
                
                if src_assets.exists():
                    import shutil
                    shutil.copytree(src_assets, dst_assets, dirs_exist_ok=True)
                    print(f"✅ کپی شد: {asset_dir}/")
            
            # ایجاد فایل‌های اضافی
            self._create_additional_files(output_path, options)
            
            print("✅ ساخت سایت کامل شد!")
            return True
            
        except Exception as e:
            print(f"❌ خطا در ساخت: {e}")
            return False
    
    def _create_additional_files(self, output_path, options=None):
        """ایجاد فایل‌های اضافی"""
        # robots.txt
        robots_content = """User-agent: *
Allow: /
Sitemap: /sitemap.xml
"""
        with open(output_path / 'robots.txt', 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        # sitemap.xml
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>/</loc>
        <lastmod>2024-01-01</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""
        with open(output_path / 'sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print("✅ فایل‌های اضافی ایجاد شدند")

def main():
    parser = argparse.ArgumentParser(
        description="🚀 Site Builder CLI - ابزار استخراج و ساخت سایت",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
مثال‌ها:
  sitebuilder-cli extract https://example.com ./output
  sitebuilder-cli analyze ./output
  sitebuilder-cli build ./output ./final_site
  sitebuilder-cli extract https://example.com ./output --headless
        """
    )
    
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    
    subparsers = parser.add_subparsers(dest='command', help='دستورات موجود')
    
    # دستور extract
    extract_parser = subparsers.add_parser('extract', help='استخراج قالب از URL')
    extract_parser.add_argument('url', help='URL سایت برای استخراج')
    extract_parser.add_argument('output', help='مسیر خروجی')
    extract_parser.add_argument('--headless', action='store_true', help='اجرای بدون نمایش مرورگر')
    
    # دستور analyze
    analyze_parser = subparsers.add_parser('analyze', help='تحلیل قالب استخراج شده')
    analyze_parser.add_argument('input', help='مسیر قالب استخراج شده')
    
    # دستور build
    build_parser = subparsers.add_parser('build', help='ساخت سایت از قالب')
    build_parser.add_argument('input', help='مسیر قالب ورودی')
    build_parser.add_argument('output', help='مسیر خروجی نهایی')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = SiteBuilderCLI()
    
    if args.command == 'extract':
        options = {'headless': args.headless} if hasattr(args, 'headless') else None
        success = cli.extract(args.url, args.output, options)
    elif args.command == 'analyze':
        success = cli.analyze(args.input)
    elif args.command == 'build':
        success = cli.build(args.input, args.output)
    else:
        print("❌ دستور نامعتبر!")
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
