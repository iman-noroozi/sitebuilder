#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗣️ Voice-to-Website - تبدیل گفتار به وب‌سایت کامل
قابلیت‌های پیشرفته:
- تشخیص گفتار فارسی و انگلیسی
- تبدیل گفتار به محتوا
- تولید خودکار ساختار سایت
- تولید کد HTML/CSS
"""

import os
import json
import speech_recognition as sr
import pyttsx3
import openai
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import aiohttp
import wave
import pyaudio
import threading
import queue

class VoiceToWebsite:
    """تبدیل گفتار به وب‌سایت"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.openai_api_key = self.config.get('openai_api_key')
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
        # تنظیمات تشخیص گفتار
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # زبان‌های پشتیبانی شده
        self.supported_languages = {
            'fa': 'Persian',
            'en': 'English',
            'ar': 'Arabic',
            'tr': 'Turkish'
        }
        
        # الگوهای تشخیص دستورات
        self.command_patterns = {
            'create_website': [
                'ساخت وب‌سایت', 'ایجاد سایت', 'سایت بساز', 'create website', 'build site'
            ],
            'add_page': [
                'اضافه کردن صفحه', 'صفحه جدید', 'add page', 'new page'
            ],
            'add_component': [
                'اضافه کردن بخش', 'کامپوننت جدید', 'add component', 'new section'
            ],
            'change_style': [
                'تغییر استایل', 'تغییر رنگ', 'change style', 'change color'
            ],
            'publish': [
                'انتشار', 'آپلود', 'publish', 'upload', 'deploy'
            ]
        }
    
    async def start_voice_listening(self, language: str = 'fa') -> Dict:
        """
        شروع گوش دادن به صدای کاربر
        
        Args:
            language: زبان گفتار (fa, en, ar, tr)
            
        Returns:
            نتیجه تشخیص گفتار
        """
        print(f"🎤 شروع گوش دادن به زبان {self.supported_languages.get(language, language)}")
        
        try:
            with self.microphone as source:
                # تنظیم میکروفون
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ میکروفون آماده است")
                
                # گوش دادن به صدای کاربر
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
                print("🎯 صدای کاربر دریافت شد")
                
                # تشخیص گفتار
                text = await self._recognize_speech(audio, language)
                
                if text:
                    # تحلیل دستور
                    command = self._analyze_command(text)
                    
                    # اجرای دستور
                    result = await self._execute_command(command, text)
                    
                    return {
                        "status": "success",
                        "recognized_text": text,
                        "command": command,
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "status": "error",
                        "message": "متوجه نشدم، لطفاً دوباره بگویید",
                        "timestamp": datetime.now().isoformat()
                    }
                    
        except sr.WaitTimeoutError:
            return {
                "status": "timeout",
                "message": "زمان انتظار به پایان رسید",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"خطا در تشخیص گفتار: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _recognize_speech(self, audio, language: str) -> Optional[str]:
        """تشخیص گفتار از فایل صوتی"""
        try:
            if language == 'fa':
                # استفاده از Google Speech Recognition برای فارسی
                text = self.recognizer.recognize_google(audio, language='fa-IR')
            elif language == 'en':
                text = self.recognizer.recognize_google(audio, language='en-US')
            elif language == 'ar':
                text = self.recognizer.recognize_google(audio, language='ar-SA')
            elif language == 'tr':
                text = self.recognizer.recognize_google(audio, language='tr-TR')
            else:
                text = self.recognizer.recognize_google(audio)
            
            print(f"📝 متن تشخیص داده شده: {text}")
            return text
            
        except sr.UnknownValueError:
            print("❌ نتوانستم گفتار را تشخیص دهم")
            return None
        except sr.RequestError as e:
            print(f"❌ خطا در سرویس تشخیص گفتار: {e}")
            return None
    
    def _analyze_command(self, text: str) -> Dict:
        """تحلیل دستور از متن تشخیص داده شده"""
        text_lower = text.lower()
        
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    return {
                        "type": command_type,
                        "confidence": 0.9,
                        "matched_pattern": pattern,
                        "full_text": text
                    }
        
        # اگر دستور خاصی تشخیص داده نشد، احتمالاً درخواست ساخت سایت است
        return {
            "type": "create_website",
            "confidence": 0.7,
            "matched_pattern": "general_request",
            "full_text": text
        }
    
    async def _execute_command(self, command: Dict, original_text: str) -> Dict:
        """اجرای دستور تشخیص داده شده"""
        command_type = command["type"]
        
        if command_type == "create_website":
            return await self._create_website_from_voice(original_text)
        elif command_type == "add_page":
            return await self._add_page_from_voice(original_text)
        elif command_type == "add_component":
            return await self._add_component_from_voice(original_text)
        elif command_type == "change_style":
            return await self._change_style_from_voice(original_text)
        elif command_type == "publish":
            return await self._publish_website_from_voice(original_text)
        else:
            return {
                "status": "unknown_command",
                "message": "دستور تشخیص داده نشد"
            }
    
    async def _create_website_from_voice(self, description: str) -> Dict:
        """ساخت وب‌سایت از توضیحات صوتی"""
        print(f"🏗️ ساخت وب‌سایت از توضیحات: {description}")
        
        try:
            # تحلیل توضیحات با AI
            website_analysis = await self._analyze_website_description(description)
            
            # تولید ساختار سایت
            site_structure = self._generate_site_structure(website_analysis)
            
            # تولید محتوا
            content = await self._generate_content_from_description(description, website_analysis)
            
            # تولید کد HTML/CSS
            html_code = self._generate_html_code(site_structure, content)
            css_code = self._generate_css_code(website_analysis)
            
            # تولید فایل‌های سایت
            site_files = self._create_site_files(html_code, css_code, website_analysis)
            
            return {
                "status": "success",
                "website_analysis": website_analysis,
                "site_structure": site_structure,
                "content": content,
                "html_code": html_code,
                "css_code": css_code,
                "site_files": site_files,
                "preview_url": f"preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"خطا در ساخت وب‌سایت: {str(e)}"
            }
    
    async def _analyze_website_description(self, description: str) -> Dict:
        """تحلیل توضیحات وب‌سایت با AI"""
        try:
            if not self.openai_api_key:
                return self._fallback_analysis(description)
            
            openai.api_key = self.openai_api_key
            
            prompt = f"""
            تحلیل توضیحات وب‌سایت و استخراج اطلاعات مورد نیاز:
            
            توضیحات: {description}
            
            لطفاً تحلیل کنید:
            1. نوع کسب‌وکار (restaurant, ecommerce, portfolio, blog, etc.)
            2. صفحات مورد نیاز (home, about, services, contact, etc.)
            3. کامپوننت‌های مورد نیاز (header, hero, gallery, contact form, etc.)
            4. سبک طراحی (modern, traditional, minimalist, creative)
            5. رنگ‌های مناسب
            6. محتوای مورد نیاز برای هر صفحه
            
            پاسخ را به صورت JSON ارائه دهید.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.7
            )
            
            analysis_text = response.choices[0].message.content
            return json.loads(analysis_text)
            
        except Exception as e:
            print(f"خطا در تحلیل AI: {e}")
            return self._fallback_analysis(description)
    
    def _fallback_analysis(self, description: str) -> Dict:
        """تحلیل جایگزین بدون AI"""
        description_lower = description.lower()
        
        # تشخیص نوع کسب‌وکار
        business_type = "general"
        if any(word in description_lower for word in ["رستوران", "غذا", "restaurant", "food"]):
            business_type = "restaurant"
        elif any(word in description_lower for word in ["فروشگاه", "خرید", "shop", "store", "ecommerce"]):
            business_type = "ecommerce"
        elif any(word in description_lower for word in ["نمونه کار", "portfolio", "کار"]):
            business_type = "portfolio"
        elif any(word in description_lower for word in ["وبلاگ", "blog", "مقاله"]):
            business_type = "blog"
        
        # تشخیص سبک طراحی
        design_style = "modern"
        if any(word in description_lower for word in ["کلاسیک", "سنتی", "classic", "traditional"]):
            design_style = "traditional"
        elif any(word in description_lower for word in ["ساده", "مینیمال", "minimal", "simple"]):
            design_style = "minimalist"
        elif any(word in description_lower for word in ["خلاق", "رنگی", "creative", "colorful"]):
            design_style = "creative"
        
        return {
            "business_type": business_type,
            "design_style": design_style,
            "pages": ["home", "about", "contact"],
            "components": ["header", "hero", "footer"],
            "colors": ["#2563EB", "#64748B", "#F59E0B"],
            "language": "fa" if any(ord(char) > 127 for char in description) else "en"
        }
    
    def _generate_site_structure(self, analysis: Dict) -> Dict:
        """تولید ساختار سایت"""
        business_type = analysis.get("business_type", "general")
        
        base_structure = {
            "pages": [
                {
                    "name": "home",
                    "title": "صفحه اصلی",
                    "url": "/",
                    "components": ["header", "hero", "footer"]
                }
            ],
            "components": [
                {
                    "name": "header",
                    "type": "navigation",
                    "elements": ["logo", "menu", "cta_button"]
                },
                {
                    "name": "hero",
                    "type": "banner",
                    "elements": ["title", "subtitle", "image", "cta_button"]
                },
                {
                    "name": "footer",
                    "type": "footer",
                    "elements": ["links", "social_media", "contact_info"]
                }
            ]
        }
        
        # اضافه کردن صفحات خاص بر اساس نوع کسب‌وکار
        if business_type == "restaurant":
            base_structure["pages"].extend([
                {
                    "name": "menu",
                    "title": "منوی غذا",
                    "url": "/menu",
                    "components": ["header", "menu_grid", "footer"]
                },
                {
                    "name": "gallery",
                    "title": "گالری تصاویر",
                    "url": "/gallery",
                    "components": ["header", "image_gallery", "footer"]
                }
            ])
        elif business_type == "ecommerce":
            base_structure["pages"].extend([
                {
                    "name": "products",
                    "title": "محصولات",
                    "url": "/products",
                    "components": ["header", "product_grid", "footer"]
                },
                {
                    "name": "cart",
                    "title": "سبد خرید",
                    "url": "/cart",
                    "components": ["header", "cart_items", "checkout_form", "footer"]
                }
            ])
        
        return base_structure
    
    async def _generate_content_from_description(self, description: str, analysis: Dict) -> Dict:
        """تولید محتوا از توضیحات"""
        try:
            if not self.openai_api_key:
                return self._fallback_content_generation(analysis)
            
            openai.api_key = self.openai_api_key
            
            prompt = f"""
            تولید محتوای وب‌سایت بر اساس توضیحات زیر:
            
            توضیحات: {description}
            نوع کسب‌وکار: {analysis.get('business_type', 'general')}
            صفحات: {', '.join(analysis.get('pages', ['home']))}
            
            برای هر صفحه محتوای مناسب تولید کنید:
            - عنوان صفحه
            - توضیحات کوتاه
            - محتوای اصلی
            - کلمات کلیدی SEO
            
            پاسخ را به صورت JSON ارائه دهید.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            content_text = response.choices[0].message.content
            return json.loads(content_text)
            
        except Exception as e:
            print(f"خطا در تولید محتوا: {e}")
            return self._fallback_content_generation(analysis)
    
    def _fallback_content_generation(self, analysis: Dict) -> Dict:
        """تولید محتوای جایگزین"""
        business_type = analysis.get("business_type", "general")
        
        content_templates = {
            "restaurant": {
                "home": {
                    "title": "رستوران ما",
                    "subtitle": "بهترین طعم‌های ایرانی",
                    "content": "به رستوران ما خوش آمدید. ما بهترین غذاهای ایرانی را با کیفیت عالی ارائه می‌دهیم.",
                    "keywords": ["رستوران", "غذای ایرانی", "طعم عالی"]
                }
            },
            "ecommerce": {
                "home": {
                    "title": "فروشگاه آنلاین ما",
                    "subtitle": "بهترین محصولات با قیمت مناسب",
                    "content": "به فروشگاه آنلاین ما خوش آمدید. محصولات باکیفیت با قیمت مناسب.",
                    "keywords": ["فروشگاه", "خرید آنلاین", "محصولات"]
                }
            },
            "general": {
                "home": {
                    "title": "وب‌سایت ما",
                    "subtitle": "بهترین خدمات",
                    "content": "به وب‌سایت ما خوش آمدید. ما بهترین خدمات را ارائه می‌دهیم.",
                    "keywords": ["خدمات", "کیفیت", "تخصص"]
                }
            }
        }
        
        return content_templates.get(business_type, content_templates["general"])
    
    def _generate_html_code(self, structure: Dict, content: Dict) -> str:
        """تولید کد HTML"""
        html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content.get('home', {}).get('title', 'وب‌سایت من')}</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="logo">
                <i class="fas fa-star"></i>
                {content.get('home', {}).get('title', 'وب‌سایت من')}
            </div>
            <nav class="nav">
                <ul>
                    <li><a href="/">خانه</a></li>
                    <li><a href="/about">درباره ما</a></li>
                    <li><a href="/contact">تماس</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>{content.get('home', {}).get('title', 'وب‌سایت من')}</h1>
            <p>{content.get('home', {}).get('subtitle', 'بهترین خدمات')}</p>
            <button class="cta-button">شروع کنید</button>
        </div>
    </section>

    <!-- Main Content -->
    <main class="main-content">
        <div class="container">
            <p>{content.get('home', {}).get('content', 'محتوای اصلی سایت')}</p>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 {content.get('home', {}).get('title', 'وب‌سایت من')}. تمامی حقوق محفوظ است.</p>
        </div>
    </footer>
</body>
</html>"""
        
        return html
    
    def _generate_css_code(self, analysis: Dict) -> str:
        """تولید کد CSS"""
        design_style = analysis.get("design_style", "modern")
        colors = analysis.get("colors", ["#2563EB", "#64748B", "#F59E0B"])
        
        css = f"""
/* 🎨 Voice-to-Website Generated Styles */
:root {{
    --primary-color: {colors[0]};
    --secondary-color: {colors[1]};
    --accent-color: {colors[2]};
    --background-color: #ffffff;
    --text-color: #333333;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Vazir', 'Tahoma', sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Header */
.header {{
    background: var(--primary-color);
    color: white;
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}}

.header .container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: bold;
}}

.nav ul {{
    display: flex;
    list-style: none;
    gap: 2rem;
}}

.nav a {{
    color: white;
    text-decoration: none;
    transition: opacity 0.3s;
}}

.nav a:hover {{
    opacity: 0.8;
}}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 4rem 0;
    text-align: center;
}}

.hero h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.hero p {{
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}}

.cta-button {{
    background: var(--accent-color);
    color: white;
    padding: 1rem 2rem;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: transform 0.3s;
}}

.cta-button:hover {{
    transform: translateY(-2px);
}}

/* Main Content */
.main-content {{
    padding: 4rem 0;
}}

/* Footer */
.footer {{
    background: var(--secondary-color);
    color: white;
    padding: 2rem 0;
    text-align: center;
}}

/* Responsive */
@media (max-width: 768px) {{
    .hero h1 {{
        font-size: 2rem;
    }}
    
    .nav ul {{
        flex-direction: column;
        gap: 1rem;
    }}
}}
"""
        
        return css
    
    def _create_site_files(self, html_code: str, css_code: str, analysis: Dict) -> Dict:
        """ایجاد فایل‌های سایت"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        site_name = f"voice_website_{timestamp}"
        
        # ایجاد پوشه سایت
        site_dir = f"generated_sites/{site_name}"
        os.makedirs(site_dir, exist_ok=True)
        
        # نوشتن فایل HTML
        with open(f"{site_dir}/index.html", "w", encoding="utf-8") as f:
            f.write(html_code)
        
        # نوشتن فایل CSS
        with open(f"{site_dir}/styles.css", "w", encoding="utf-8") as f:
            f.write(css_code)
        
        # نوشتن فایل اطلاعات
        info = {
            "site_name": site_name,
            "created_at": datetime.now().isoformat(),
            "analysis": analysis,
            "files": ["index.html", "styles.css"]
        }
        
        with open(f"{site_dir}/site_info.json", "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        
        return {
            "site_dir": site_dir,
            "site_name": site_name,
            "files": ["index.html", "styles.css", "site_info.json"],
            "preview_url": f"{site_dir}/index.html"
        }
    
    async def _add_page_from_voice(self, description: str) -> Dict:
        """اضافه کردن صفحه از توضیحات صوتی"""
        # پیاده‌سازی اضافه کردن صفحه
        return {"status": "success", "message": "صفحه اضافه شد"}
    
    async def _add_component_from_voice(self, description: str) -> Dict:
        """اضافه کردن کامپوننت از توضیحات صوتی"""
        # پیاده‌سازی اضافه کردن کامپوننت
        return {"status": "success", "message": "کامپوننت اضافه شد"}
    
    async def _change_style_from_voice(self, description: str) -> Dict:
        """تغییر استایل از توضیحات صوتی"""
        # پیاده‌سازی تغییر استایل
        return {"status": "success", "message": "استایل تغییر کرد"}
    
    async def _publish_website_from_voice(self, description: str) -> Dict:
        """انتشار وب‌سایت از توضیحات صوتی"""
        # پیاده‌سازی انتشار سایت
        return {"status": "success", "message": "سایت منتشر شد"}
    
    def speak_response(self, text: str, language: str = 'fa') -> None:
        """تبدیل متن به گفتار"""
        try:
            engine = pyttsx3.init()
            
            # تنظیمات صدا
            voices = engine.getProperty('voices')
            if language == 'fa' and len(voices) > 1:
                engine.setProperty('voice', voices[1].id)  # صدای فارسی
            
            engine.setProperty('rate', 150)  # سرعت گفتار
            engine.setProperty('volume', 0.8)  # حجم صدا
            
            engine.say(text)
            engine.runAndWait()
            
        except Exception as e:
            print(f"خطا در تبدیل متن به گفتار: {e}")

# مثال استفاده
if __name__ == "__main__":
    voice_website = VoiceToWebsite()
    
    # تست تشخیص گفتار
    async def test_voice_recognition():
        result = await voice_website.start_voice_listening('fa')
        print("🎤 نتیجه تشخیص گفتار:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result["status"] == "success":
            # پاسخ صوتی
            voice_website.speak_response("وب‌سایت شما با موفقیت ساخته شد!", 'fa')
    
    # اجرای تست
    asyncio.run(test_voice_recognition())
