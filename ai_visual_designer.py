#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 AI Visual Designer - تولید خودکار طراحی با هوش مصنوعی
قابلیت‌های پیشرفته:
- تولید طراحی بر اساس توضیحات متنی
- پیش‌بینی ترندهای طراحی
- تطبیق خودکار با برند
- تولید پالت رنگی هوشمند
"""

import os
import json
import requests
import base64
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import openai
from PIL import Image, ImageDraw, ImageFont
import io
import colorsys

class AIVisualDesigner:
    """طراح بصری هوش مصنوعی"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.openai_api_key = self.config.get('openai_api_key')
        self.design_trends = self._load_design_trends()
        self.color_palettes = self._load_color_palettes()
        
    def _load_design_trends(self) -> Dict:
        """بارگذاری ترندهای طراحی"""
        return {
            "2024": {
                "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
                "fonts": ["Inter", "Poppins", "Roboto", "Montserrat"],
                "layouts": ["minimalist", "grid", "asymmetric", "card-based"],
                "effects": ["glassmorphism", "neumorphism", "gradients", "shadows"]
            },
            "persian": {
                "colors": ["#2C3E50", "#E74C3C", "#F39C12", "#27AE60", "#8E44AD"],
                "fonts": ["Vazir", "Samim", "Shabnam", "IRANSans"],
                "layouts": ["traditional", "modern", "minimalist", "ornate"],
                "effects": ["persian_patterns", "calligraphy", "geometric", "floral"]
            }
        }
    
    def _load_color_palettes(self) -> Dict:
        """بارگذاری پالت‌های رنگی"""
        return {
            "business": {
                "primary": "#2563EB",
                "secondary": "#64748B", 
                "accent": "#F59E0B",
                "background": "#F8FAFC",
                "text": "#1E293B"
            },
            "creative": {
                "primary": "#EC4899",
                "secondary": "#8B5CF6",
                "accent": "#06B6D4", 
                "background": "#FEF3C7",
                "text": "#374151"
            },
            "minimal": {
                "primary": "#000000",
                "secondary": "#6B7280",
                "accent": "#EF4444",
                "background": "#FFFFFF",
                "text": "#111827"
            },
            "persian": {
                "primary": "#2C3E50",
                "secondary": "#E74C3C",
                "accent": "#F39C12",
                "background": "#FDF2E9",
                "text": "#2C3E50"
            }
        }
    
    async def generate_design_from_description(self, description: str, business_type: str = "general") -> Dict:
        """
        تولید طراحی بر اساس توضیحات متنی
        
        Args:
            description: توضیحات طراحی مورد نظر
            business_type: نوع کسب‌وکار
            
        Returns:
            طراحی تولید شده
        """
        print(f"🎨 تولید طراحی برای: {description}")
        
        # تحلیل توضیحات با AI
        design_analysis = await self._analyze_design_description(description, business_type)
        
        # تولید پالت رنگی
        color_palette = self._generate_color_palette(design_analysis)
        
        # انتخاب فونت‌ها
        fonts = self._select_fonts(design_analysis)
        
        # تولید لایوت
        layout = self._generate_layout(design_analysis)
        
        # تولید کامپوننت‌ها
        components = self._generate_components(design_analysis)
        
        # تولید CSS
        css_styles = self._generate_css_styles(color_palette, fonts, layout, components)
        
        return {
            "design_analysis": design_analysis,
            "color_palette": color_palette,
            "fonts": fonts,
            "layout": layout,
            "components": components,
            "css_styles": css_styles,
            "preview_url": await self._generate_preview(design_analysis, css_styles),
            "created_at": datetime.now().isoformat()
        }
    
    async def _analyze_design_description(self, description: str, business_type: str) -> Dict:
        """تحلیل توضیحات طراحی با AI"""
        try:
            if not self.openai_api_key:
                return self._fallback_analysis(description, business_type)
            
            openai.api_key = self.openai_api_key
            
            prompt = f"""
            تحلیل طراحی وب‌سایت بر اساس توضیحات زیر:
            
            توضیحات: {description}
            نوع کسب‌وکار: {business_type}
            
            لطفاً تحلیل کنید:
            1. سبک طراحی (minimalist, modern, traditional, creative)
            2. رنگ‌های مناسب (3-5 رنگ)
            3. نوع فونت (sans-serif, serif, display)
            4. لایوت (grid, flexbox, asymmetric)
            5. کامپوننت‌های مورد نیاز
            6. احساس کلی (professional, friendly, creative, luxury)
            
            پاسخ را به صورت JSON ارائه دهید.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            analysis_text = response.choices[0].message.content
            return json.loads(analysis_text)
            
        except Exception as e:
            print(f"خطا در تحلیل AI: {e}")
            return self._fallback_analysis(description, business_type)
    
    def _fallback_analysis(self, description: str, business_type: str) -> Dict:
        """تحلیل جایگزین بدون AI"""
        # تحلیل ساده بر اساس کلمات کلیدی
        description_lower = description.lower()
        
        style = "modern"
        if any(word in description_lower for word in ["کلاسیک", "سنتی", "classic", "traditional"]):
            style = "traditional"
        elif any(word in description_lower for word in ["خلاق", "رنگی", "creative", "colorful"]):
            style = "creative"
        elif any(word in description_lower for word in ["ساده", "مینیمال", "minimal", "simple"]):
            style = "minimalist"
        
        return {
            "style": style,
            "business_type": business_type,
            "mood": "professional",
            "layout_type": "grid",
            "color_scheme": "business" if business_type in ["business", "corporate"] else "creative"
        }
    
    def _generate_color_palette(self, analysis: Dict) -> Dict:
        """تولید پالت رنگی هوشمند"""
        color_scheme = analysis.get("color_scheme", "business")
        base_palette = self.color_palettes.get(color_scheme, self.color_palettes["business"])
        
        # تولید رنگ‌های اضافی
        additional_colors = self._generate_additional_colors(base_palette["primary"])
        
        return {
            **base_palette,
            "additional": additional_colors,
            "gradients": self._generate_gradients(base_palette),
            "shades": self._generate_color_shades(base_palette["primary"])
        }
    
    def _generate_additional_colors(self, primary_color: str) -> List[str]:
        """تولید رنگ‌های اضافی بر اساس رنگ اصلی"""
        # تبدیل hex به RGB
        hex_color = primary_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # تبدیل به HSV
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        additional_colors = []
        for i in range(5):
            # تغییر hue برای تولید رنگ‌های مکمل
            new_h = (h + i * 0.2) % 1.0
            new_r, new_g, new_b = colorsys.hsv_to_rgb(new_h, s, v)
            hex_color = f"#{int(new_r*255):02x}{int(new_g*255):02x}{int(new_b*255):02x}"
            additional_colors.append(hex_color)
        
        return additional_colors
    
    def _generate_gradients(self, palette: Dict) -> List[str]:
        """تولید گرادیان‌ها"""
        gradients = []
        colors = [palette["primary"], palette["secondary"], palette["accent"]]
        
        for i in range(len(colors)):
            for j in range(i+1, len(colors)):
                gradient = f"linear-gradient(135deg, {colors[i]}, {colors[j]})"
                gradients.append(gradient)
        
        return gradients
    
    def _generate_color_shades(self, color: str) -> Dict:
        """تولید سایه‌های مختلف رنگ"""
        hex_color = color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        shades = {}
        for i, shade_name in enumerate(["50", "100", "200", "300", "400", "500", "600", "700", "800", "900"]):
            # محاسبه سایه
            factor = (i + 1) * 0.1
            new_r = int(r * (1 - factor) + 255 * factor)
            new_g = int(g * (1 - factor) + 255 * factor)
            new_b = int(b * (1 - factor) + 255 * factor)
            
            shades[shade_name] = f"#{new_r:02x}{new_g:02x}{new_b:02x}"
        
        return shades
    
    def _select_fonts(self, analysis: Dict) -> Dict:
        """انتخاب فونت‌های مناسب"""
        style = analysis.get("style", "modern")
        business_type = analysis.get("business_type", "general")
        
        if business_type == "persian" or "فارسی" in str(analysis):
            font_family = "Vazir"
            fallback_fonts = ["Samim", "Shabnam", "IRANSans", "Tahoma"]
        else:
            if style == "traditional":
                font_family = "Georgia"
                fallback_fonts = ["Times New Roman", "serif"]
            elif style == "creative":
                font_family = "Poppins"
                fallback_fonts = ["Inter", "Roboto", "sans-serif"]
            else:
                font_family = "Inter"
                fallback_fonts = ["Roboto", "Arial", "sans-serif"]
        
        return {
            "primary": font_family,
            "fallback": fallback_fonts,
            "headings": font_family,
            "body": font_family,
            "display": font_family
        }
    
    def _generate_layout(self, analysis: Dict) -> Dict:
        """تولید لایوت"""
        layout_type = analysis.get("layout_type", "grid")
        style = analysis.get("style", "modern")
        
        layouts = {
            "grid": {
                "type": "CSS Grid",
                "columns": 12,
                "gap": "24px",
                "container_max_width": "1200px",
                "responsive_breakpoints": {
                    "mobile": "768px",
                    "tablet": "1024px",
                    "desktop": "1200px"
                }
            },
            "flexbox": {
                "type": "Flexbox",
                "direction": "row",
                "wrap": "wrap",
                "justify_content": "space-between",
                "align_items": "center"
            },
            "asymmetric": {
                "type": "Asymmetric Grid",
                "columns": [2, 1, 3],
                "gap": "32px",
                "container_max_width": "1400px"
            }
        }
        
        return layouts.get(layout_type, layouts["grid"])
    
    def _generate_components(self, analysis: Dict) -> List[Dict]:
        """تولید کامپوننت‌های مورد نیاز"""
        business_type = analysis.get("business_type", "general")
        style = analysis.get("style", "modern")
        
        base_components = [
            {
                "type": "header",
                "name": "هدر سایت",
                "elements": ["logo", "navigation", "cta_button"],
                "style": style
            },
            {
                "type": "hero",
                "name": "بخش اصلی",
                "elements": ["title", "subtitle", "image", "cta_button"],
                "style": style
            },
            {
                "type": "footer",
                "name": "فوتر",
                "elements": ["links", "social_media", "contact_info"],
                "style": style
            }
        ]
        
        # اضافه کردن کامپوننت‌های خاص بر اساس نوع کسب‌وکار
        if business_type in ["restaurant", "food"]:
            base_components.extend([
                {
                    "type": "menu",
                    "name": "منوی غذا",
                    "elements": ["menu_items", "prices", "images"],
                    "style": style
                },
                {
                    "type": "gallery",
                    "name": "گالری تصاویر",
                    "elements": ["image_grid", "lightbox"],
                    "style": style
                }
            ])
        elif business_type in ["ecommerce", "shop"]:
            base_components.extend([
                {
                    "type": "product_grid",
                    "name": "شبکه محصولات",
                    "elements": ["product_cards", "filters", "pagination"],
                    "style": style
                },
                {
                    "type": "cart",
                    "name": "سبد خرید",
                    "elements": ["cart_items", "checkout_button"],
                    "style": style
                }
            ])
        
        return base_components
    
    def _generate_css_styles(self, color_palette: Dict, fonts: Dict, layout: Dict, components: List[Dict]) -> str:
        """تولید CSS استایل‌ها"""
        css = f"""
/* 🎨 AI Generated Styles */
:root {{
    /* رنگ‌های اصلی */
    --primary-color: {color_palette['primary']};
    --secondary-color: {color_palette['secondary']};
    --accent-color: {color_palette['accent']};
    --background-color: {color_palette['background']};
    --text-color: {color_palette['text']};
    
    /* فونت‌ها */
    --font-primary: '{fonts['primary']}', {', '.join(fonts['fallback'])};
    --font-heading: '{fonts['headings']}', {', '.join(fonts['fallback'])};
    
    /* لایوت */
    --container-max-width: {layout.get('container_max_width', '1200px')};
    --grid-gap: {layout.get('gap', '24px')};
}}

/* استایل‌های پایه */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--font-primary);
    background-color: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
}}

.container {{
    max-width: var(--container-max-width);
    margin: 0 auto;
    padding: 0 20px;
}}

/* کامپوننت‌ها */
"""
        
        # اضافه کردن استایل‌های کامپوننت‌ها
        for component in components:
            css += self._generate_component_css(component, color_palette)
        
        return css
    
    def _generate_component_css(self, component: Dict, color_palette: Dict) -> str:
        """تولید CSS برای کامپوننت"""
        component_type = component["type"]
        style = component.get("style", "modern")
        
        if component_type == "header":
            return f"""
.header {{
    background: {color_palette['primary']};
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

.nav {{
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
"""
        elif component_type == "hero":
            return f"""
.hero {{
    background: linear-gradient(135deg, {color_palette['primary']}, {color_palette['secondary']});
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
    background: {color_palette['accent']};
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
"""
        
        return ""
    
    async def _generate_preview(self, analysis: Dict, css_styles: str) -> str:
        """تولید پیش‌نمایش طراحی"""
        # این بخش می‌تواند یک تصویر پیش‌نمایش تولید کند
        # یا یک URL برای پیش‌نمایش زنده برگرداند
        return f"preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    def get_design_trends(self, year: str = "2024") -> Dict:
        """دریافت ترندهای طراحی"""
        return self.design_trends.get(year, self.design_trends["2024"])
    
    def suggest_improvements(self, current_design: Dict) -> List[str]:
        """پیشنهاد بهبودهای طراحی"""
        suggestions = []
        
        # تحلیل رنگ‌ها
        if len(current_design.get("colors", [])) < 3:
            suggestions.append("اضافه کردن رنگ‌های بیشتر برای تنوع بصری")
        
        # تحلیل فونت‌ها
        if not current_design.get("fonts"):
            suggestions.append("انتخاب فونت‌های مناسب برای خوانایی بهتر")
        
        # تحلیل لایوت
        if not current_design.get("responsive"):
            suggestions.append("بهینه‌سازی برای موبایل و تبلت")
        
        return suggestions

# مثال استفاده
if __name__ == "__main__":
    designer = AIVisualDesigner()
    
    # تست تولید طراحی
    description = "یک وب‌سایت مدرن برای رستوران ایرانی با رنگ‌های گرم و فونت‌های فارسی"
    result = designer.generate_design_from_description(description, "restaurant")
    
    print("🎨 طراحی تولید شده:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
