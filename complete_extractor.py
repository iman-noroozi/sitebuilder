"""
🏗️ ابزار استخراج کامل سایت با Python
نسخه مستقل بدون نیاز به Node.js

استفاده:
python complete_extractor.py <URL> [OUTPUT_PATH]

مثال:
python complete_extractor.py https://example.com ./extracted_site
"""

import requests
from bs4 import BeautifulSoup
import os
import json
import re
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time
from datetime import datetime
import shutil
import zipfile

class CompleteSiteExtractor:
    def __init__(self, options=None):
        self.options = options or {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # گزینه‌های پیش‌فرض
        self.download_images = self.options.get('download_images', True)
        self.download_css = self.options.get('download_css', True) 
        self.download_js = self.options.get('download_js', True)
        self.clean_html = self.options.get('clean_html', True)
        self.timeout = self.options.get('timeout', 30)
        
    def extract_complete_site(self, url, output_path):
        """استخراج کامل سایت"""
        print(f"🔍 شروع استخراج کامل سایت از: {url}")
        
        # ایجاد پوشه خروجی
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # ایجاد پوشه‌های فرعی
        assets_path = output_path / 'assets'
        images_path = assets_path / 'images'
        css_path = assets_path / 'css'
        js_path = assets_path / 'js'
        
        for path in [assets_path, images_path, css_path, js_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        try:
            # دریافت HTML اصلی
            print("📄 دریافت HTML...")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # تجزیه URL پایه
            base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
            
            # استخراج و دانلود CSS
            css_files = []
            if self.download_css:
                css_files = self._extract_and_download_css(soup, base_url, css_path)
            
            # استخراج و دانلود JavaScript
            js_files = []
            if self.download_js:
                js_files = self._extract_and_download_js(soup, base_url, js_path)
            
            # استخراج و دانلود تصاویر
            image_files = []
            if self.download_images:
                image_files = self._extract_and_download_images(soup, base_url, images_path)
            
            # تمیز کردن و بروزرسانی HTML
            if self.clean_html:
                html_content = self._clean_html(html_content)
            
            # بروزرسانی مسیرها در HTML
            html_content = self._update_html_paths(html_content, css_files, js_files, image_files)
            
            # استخراج متادیتا
            metadata = self._extract_metadata(soup, url)
            
            # ذخیره فایل‌ها
            self._save_files(output_path, html_content, metadata, css_files, js_files, image_files)
            
            print(f"✅ استخراج کامل شد!")
            print(f"📊 آمار:")
            print(f"   - CSS: {len(css_files)} فایل")
            print(f"   - JavaScript: {len(js_files)} فایل") 
            print(f"   - تصاویر: {len(image_files)} فایل")
            print(f"📁 خروجی: {output_path}")
            
            return {
                'success': True,
                'output_path': str(output_path),
                'stats': {
                    'css_files': len(css_files),
                    'js_files': len(js_files), 
                    'images': len(image_files)
                }
            }
            
        except Exception as e:
            print(f"❌ خطا: {e}")
            return {'success': False, 'error': str(e)}
    
    def _extract_and_download_css(self, soup, base_url, css_path):
        """استخراج و دانلود فایل‌های CSS"""
        print("🎨 استخراج CSS...")
        css_files = []
        
        # CSS فایل‌های خارجی
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                css_url = urljoin(base_url, href)
                filename = self._get_filename_from_url(css_url, 'css')
                
                if self._download_file(css_url, css_path / filename):
                    css_files.append(filename)
                    link['href'] = f'./assets/css/{filename}'
        
        # CSS inline
        inline_css = []
        for style in soup.find_all('style'):
            if style.string:
                inline_css.append(style.string)
        
        if inline_css:
            inline_filename = 'inline_styles.css'
            with open(css_path / inline_filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(inline_css))
            css_files.append(inline_filename)
        
        return css_files
    
    def _extract_and_download_js(self, soup, base_url, js_path):
        """استخراج و دانلود فایل‌های JavaScript"""
        print("⚡ استخراج JavaScript...")
        js_files = []
        
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src and not src.startswith('data:'):
                js_url = urljoin(base_url, src)
                filename = self._get_filename_from_url(js_url, 'js')
                
                if self._download_file(js_url, js_path / filename):
                    js_files.append(filename)
                    script['src'] = f'./assets/js/{filename}'
        
        return js_files
    
    def _extract_and_download_images(self, soup, base_url, images_path):
        """استخراج و دانلود تصاویر"""
        print("🖼️ استخراج تصاویر...")
        image_files = []
        
        # تصاویر img
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src and not src.startswith('data:'):
                img_url = urljoin(base_url, src)
                filename = self._get_filename_from_url(img_url, 'jpg')
                
                if self._download_file(img_url, images_path / filename):
                    image_files.append(filename)
                    img['src'] = f'./assets/images/{filename}'
        
        # تصاویر background در CSS
        # این بخش می‌تواند پیچیده‌تر باشد و نیاز به پردازش CSS دارد
        
        return image_files
    
    def _download_file(self, url, file_path):
        """دانلود فایل"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ دانلود شد: {file_path.name}")
            return True
            
        except Exception as e:
            print(f"❌ خطا در دانلود {url}: {e}")
            return False
    
    def _get_filename_from_url(self, url, default_ext):
        """استخراج نام فایل از URL"""
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        if not filename or '.' not in filename:
            filename = f"file_{hash(url) % 10000}.{default_ext}"
        
        # تمیز کردن نام فایل
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return filename
    
    def _clean_html(self, html):
        """تمیز کردن HTML"""
        # حذف کامنت‌ها
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # حذف اسکریپت‌های تحلیلی
        html = re.sub(r'<script[^>]*google-analytics[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<script[^>]*gtag[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # تمیز کردن فضاهای اضافی
        html = re.sub(r'\s+', ' ', html)
        
        return html.strip()
    
    def _update_html_paths(self, html, css_files, js_files, image_files):
        """بروزرسانی مسیرها در HTML"""
        # این تابع مسیرهای نسبی را به مسیرهای محلی تبدیل می‌کند
        # پیاده‌سازی کامل نیاز به regex پیچیده‌تری دارد
        return html
    
    def _extract_metadata(self, soup, url):
        """استخراج متادیتا"""
        metadata = {
            'url': url,
            'extracted_at': datetime.now().isoformat(),
            'title': '',
            'description': '',
            'keywords': '',
            'og': {}
        }
        
        # عنوان
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()
        
        # توضیحات
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            metadata['description'] = desc_tag.get('content', '')
        
        # کلمات کلیدی
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag:
            metadata['keywords'] = keywords_tag.get('content', '')
        
        # Open Graph
        og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
        for tag in og_tags:
            prop = tag.get('property', '').replace('og:', '')
            content = tag.get('content', '')
            if prop and content:
                metadata['og'][prop] = content
        
        return metadata
    
    def _save_files(self, output_path, html_content, metadata, css_files, js_files, image_files):
        """ذخیره فایل‌ها"""
        
        # ذخیره HTML
        with open(output_path / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # ذخیره متادیتا
        with open(output_path / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # ایجاد README
        readme_content = f"""# سایت استخراج شده

## اطلاعات
- **URL منبع:** {metadata['url']}
- **عنوان:** {metadata['title']}
- **تاریخ استخراج:** {metadata['extracted_at']}

## فایل‌ها
- `index.html` - صفحه اصلی
- `metadata.json` - اطلاعات سایت
- `assets/` - فایل‌های جانبی
  - `css/` - فایل‌های استایل ({len(css_files)} فایل)
  - `js/` - فایل‌های اسکریپت ({len(js_files)} فایل)
  - `images/` - تصاویر ({len(image_files)} فایل)

## نحوه استفاده
فایل `index.html` را در مرورگر باز کنید.
"""
        
        with open(output_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def create_zip(self, folder_path, zip_name=None):
        """ایجاد فایل ZIP"""
        folder_path = Path(folder_path)
        
        if not zip_name:
            zip_name = f"{folder_path.name}.zip"
        
        zip_path = folder_path.parent / zip_name
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(folder_path)
                    zipf.write(file_path, arcname)
        
        print(f"📦 فایل ZIP ایجاد شد: {zip_path}")
        return str(zip_path)


def main():
    """تابع اصلی"""
    import sys
    
    if len(sys.argv) < 2:
        print("""
🏗️ ابزار استخراج کامل سایت

استفاده:
    python complete_extractor.py <URL> [OUTPUT_PATH] [OPTIONS]

مثال‌ها:
    python complete_extractor.py https://example.com
    python complete_extractor.py https://example.com ./my_site
    
گزینه‌ها:
    --no-images     عدم دانلود تصاویر
    --no-css        عدم دانلود CSS
    --no-js         عدم دانلود JavaScript
    --zip           ایجاد فایل ZIP
        """)
        return
    
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else f"./extracted_{int(time.time())}"
    
    # تجزیه گزینه‌ها
    options = {
        'download_images': '--no-images' not in sys.argv,
        'download_css': '--no-css' not in sys.argv,
        'download_js': '--no-js' not in sys.argv,
        'clean_html': True,
        'timeout': 30
    }
    
    # ایجاد extractor
    extractor = CompleteSiteExtractor(options)
    
    # استخراج
    result = extractor.extract_complete_site(url, output_path)
    
    if result['success']:
        # ایجاد ZIP در صورت درخواست
        if '--zip' in sys.argv:
            extractor.create_zip(result['output_path'])
        
        print(f"\n🎉 استخراج با موفقیت تمام شد!")
        print(f"📁 مسیر خروجی: {result['output_path']}")
    else:
        print(f"\n❌ استخراج ناموفق: {result['error']}")


if __name__ == "__main__":
    main()
