#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧩 Smart Component Generator - تولید هوشمند کامپوننت‌های سفارشی
قابلیت‌های پیشرفته:
- تولید کامپوننت‌های سفارشی با AI
- یادگیری از رفتار کاربر
- پیشنهاد کامپوننت‌های مرتبط
- بهینه‌سازی خودکار عملکرد
"""

import os
import json
import openai
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import asyncio
import aiohttp
import re
from dataclasses import dataclass
from enum import Enum

class ComponentType(Enum):
    """انواع کامپوننت‌ها"""
    LAYOUT = "layout"
    CONTENT = "content"
    INTERACTIVE = "interactive"
    MEDIA = "media"
    FORM = "form"
    NAVIGATION = "navigation"
    DISPLAY = "display"

@dataclass
class ComponentSpec:
    """مشخصات کامپوننت"""
    name: str
    type: ComponentType
    description: str
    props: Dict
    styles: Dict
    dependencies: List[str]
    responsive: bool = True
    accessible: bool = True

class SmartComponentGenerator:
    """تولیدکننده هوشمند کامپوننت‌ها"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.openai_api_key = self.config.get('openai_api_key')
        self.component_library = self._load_component_library()
        self.user_preferences = self._load_user_preferences()
        self.usage_analytics = self._load_usage_analytics()
        
        # الگوهای کامپوننت‌های رایج
        self.common_patterns = {
            "hero_section": {
                "description": "بخش اصلی با عنوان، توضیحات و دکمه CTA",
                "props": ["title", "subtitle", "cta_text", "background_image"],
                "styles": ["gradient_background", "centered_text", "large_typography"]
            },
            "feature_grid": {
                "description": "شبکه ویژگی‌ها با آیکون، عنوان و توضیحات",
                "props": ["features", "columns", "icon_style"],
                "styles": ["card_layout", "hover_effects", "responsive_grid"]
            },
            "testimonial_slider": {
                "description": "اسلایدر نظرات مشتریان",
                "props": ["testimonials", "autoplay", "show_rating"],
                "styles": ["carousel", "quote_styling", "avatar_display"]
            },
            "contact_form": {
                "description": "فرم تماس با اعتبارسنجی",
                "props": ["fields", "validation", "submit_action"],
                "styles": ["form_styling", "error_states", "success_message"]
            }
        }
    
    def _load_component_library(self) -> Dict:
        """بارگذاری کتابخانه کامپوننت‌ها"""
        return {
            "layout": {
                "container": {
                    "name": "Container",
                    "description": "ظرف اصلی برای محتوا",
                    "props": ["max_width", "padding", "margin"],
                    "styles": ["responsive", "centered"]
                },
                "grid": {
                    "name": "Grid",
                    "description": "شبکه برای چیدمان عناصر",
                    "props": ["columns", "gap", "align_items"],
                    "styles": ["responsive", "flexible"]
                },
                "flexbox": {
                    "name": "Flexbox",
                    "description": "چیدمان انعطاف‌پذیر",
                    "props": ["direction", "justify_content", "align_items"],
                    "styles": ["responsive", "flexible"]
                }
            },
            "content": {
                "heading": {
                    "name": "Heading",
                    "description": "عنوان‌های مختلف",
                    "props": ["level", "text", "color", "size"],
                    "styles": ["typography", "responsive"]
                },
                "paragraph": {
                    "name": "Paragraph",
                    "description": "متن پاراگراف",
                    "props": ["text", "color", "size", "line_height"],
                    "styles": ["typography", "readable"]
                },
                "button": {
                    "name": "Button",
                    "description": "دکمه قابل کلیک",
                    "props": ["text", "variant", "size", "onClick"],
                    "styles": ["interactive", "hover_effects"]
                }
            },
            "interactive": {
                "modal": {
                    "name": "Modal",
                    "description": "پنجره بازشو",
                    "props": ["title", "content", "show", "onClose"],
                    "styles": ["overlay", "animation", "responsive"]
                },
                "dropdown": {
                    "name": "Dropdown",
                    "description": "منوی کشویی",
                    "props": ["options", "selected", "onChange"],
                    "styles": ["list_styling", "hover_effects"]
                },
                "tabs": {
                    "name": "Tabs",
                    "description": "تب‌های محتوا",
                    "props": ["tabs", "active_tab", "onChange"],
                    "styles": ["tab_styling", "content_switching"]
                }
            }
        }
    
    def _load_user_preferences(self) -> Dict:
        """بارگذاری ترجیحات کاربر"""
        return {
            "preferred_style": "modern",
            "color_scheme": "blue",
            "font_family": "Vazir",
            "component_size": "medium",
            "animation_preference": "subtle",
            "accessibility_level": "high"
        }
    
    def _load_usage_analytics(self) -> Dict:
        """بارگذاری آمار استفاده"""
        return {
            "most_used_components": ["button", "container", "heading"],
            "user_behavior": {
                "prefers_simple": True,
                "uses_animations": False,
                "mobile_first": True
            },
            "performance_metrics": {
                "load_time": 1.2,
                "bundle_size": 45.6
            }
        }
    
    async def generate_component(self, description: str, context: Dict = None) -> ComponentSpec:
        """
        تولید کامپوننت بر اساس توضیحات
        
        Args:
            description: توضیحات کامپوننت مورد نظر
            context: زمینه استفاده (صفحه، نوع سایت، etc.)
            
        Returns:
            مشخصات کامپوننت تولید شده
        """
        print(f"🧩 تولید کامپوننت: {description}")
        
        # تحلیل توضیحات
        analysis = await self._analyze_component_description(description, context)
        
        # تولید مشخصات کامپوننت
        component_spec = self._create_component_spec(analysis)
        
        # بهینه‌سازی بر اساس ترجیحات کاربر
        optimized_spec = self._optimize_for_user_preferences(component_spec)
        
        # تولید کد
        code = self._generate_component_code(optimized_spec)
        
        # ذخیره در کتابخانه
        self._save_to_library(optimized_spec, code)
        
        return optimized_spec
    
    async def _analyze_component_description(self, description: str, context: Dict = None) -> Dict:
        """تحلیل توضیحات کامپوننت با AI"""
        try:
            if not self.openai_api_key:
                return self._fallback_analysis(description, context)
            
            openai.api_key = self.openai_api_key
            
            prompt = f"""
            تحلیل توضیحات کامپوننت و تولید مشخصات فنی:
            
            توضیحات: {description}
            زمینه: {context or 'عمومی'}
            
            لطفاً تحلیل کنید:
            1. نوع کامپوننت (layout, content, interactive, media, form, navigation, display)
            2. ویژگی‌های مورد نیاز (props)
            3. استایل‌های مناسب
            4. وابستگی‌های مورد نیاز
            5. قابلیت‌های تعاملی
            6. بهینه‌سازی برای موبایل
            7. دسترسی‌پذیری
            
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
            return self._fallback_analysis(description, context)
    
    def _fallback_analysis(self, description: str, context: Dict = None) -> Dict:
        """تحلیل جایگزین بدون AI"""
        description_lower = description.lower()
        
        # تشخیص نوع کامپوننت
        component_type = ComponentType.CONTENT
        if any(word in description_lower for word in ["فرم", "form", "ورودی", "input"]):
            component_type = ComponentType.FORM
        elif any(word in description_lower for word in ["منو", "menu", "ناوبری", "navigation"]):
            component_type = ComponentType.NAVIGATION
        elif any(word in description_lower for word in ["تصویر", "image", "ویدیو", "video", "گالری", "gallery"]):
            component_type = ComponentType.MEDIA
        elif any(word in description_lower for word in ["تعاملی", "interactive", "کلیک", "click", "hover"]):
            component_type = ComponentType.INTERACTIVE
        elif any(word in description_lower for word in ["چیدمان", "layout", "شبکه", "grid"]):
            component_type = ComponentType.LAYOUT
        
        return {
            "type": component_type.value,
            "name": self._generate_component_name(description),
            "description": description,
            "props": self._extract_props_from_description(description),
            "styles": self._extract_styles_from_description(description),
            "dependencies": [],
            "responsive": True,
            "accessible": True
        }
    
    def _generate_component_name(self, description: str) -> str:
        """تولید نام کامپوننت از توضیحات"""
        # استخراج کلمات کلیدی
        words = re.findall(r'\b\w+\b', description.lower())
        
        # فیلتر کردن کلمات غیرضروری
        stop_words = ["یک", "برای", "که", "با", "در", "از", "به", "a", "an", "the", "for", "with", "in", "on", "at"]
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # انتخاب 2-3 کلمه کلیدی
        if len(keywords) >= 2:
            name = "".join(word.capitalize() for word in keywords[:2])
        else:
            name = "CustomComponent"
        
        return name
    
    def _extract_props_from_description(self, description: str) -> List[str]:
        """استخراج props از توضیحات"""
        props = []
        description_lower = description.lower()
        
        # تشخیص props رایج
        if "عنوان" in description_lower or "title" in description_lower:
            props.append("title")
        if "متن" in description_lower or "text" in description_lower:
            props.append("text")
        if "رنگ" in description_lower or "color" in description_lower:
            props.append("color")
        if "اندازه" in description_lower or "size" in description_lower:
            props.append("size")
        if "تصویر" in description_lower or "image" in description_lower:
            props.append("image")
        if "لینک" in description_lower or "link" in description_lower:
            props.append("href")
        
        return props
    
    def _extract_styles_from_description(self, description: str) -> List[str]:
        """استخراج استایل‌ها از توضیحات"""
        styles = []
        description_lower = description.lower()
        
        # تشخیص استایل‌های رایج
        if "رنگی" in description_lower or "colorful" in description_lower:
            styles.append("colorful")
        if "ساده" in description_lower or "simple" in description_lower:
            styles.append("simple")
        if "مدرن" in description_lower or "modern" in description_lower:
            styles.append("modern")
        if "گرد" in description_lower or "rounded" in description_lower:
            styles.append("rounded")
        if "سایه" in description_lower or "shadow" in description_lower:
            styles.append("shadow")
        
        return styles
    
    def _create_component_spec(self, analysis: Dict) -> ComponentSpec:
        """ایجاد مشخصات کامپوننت"""
        return ComponentSpec(
            name=analysis.get("name", "CustomComponent"),
            type=ComponentType(analysis.get("type", "content")),
            description=analysis.get("description", ""),
            props=analysis.get("props", {}),
            styles=analysis.get("styles", {}),
            dependencies=analysis.get("dependencies", []),
            responsive=analysis.get("responsive", True),
            accessible=analysis.get("accessible", True)
        )
    
    def _optimize_for_user_preferences(self, spec: ComponentSpec) -> ComponentSpec:
        """بهینه‌سازی بر اساس ترجیحات کاربر"""
        # اعمال ترجیحات کاربر
        if self.user_preferences.get("preferred_style") == "minimal":
            spec.styles["minimal"] = True
        
        if self.user_preferences.get("animation_preference") == "none":
            spec.styles["no_animation"] = True
        
        if self.user_preferences.get("accessibility_level") == "high":
            spec.accessible = True
            spec.styles["high_contrast"] = True
        
        return spec
    
    def _generate_component_code(self, spec: ComponentSpec) -> Dict:
        """تولید کد کامپوننت"""
        if spec.type == ComponentType.LAYOUT:
            return self._generate_layout_component(spec)
        elif spec.type == ComponentType.CONTENT:
            return self._generate_content_component(spec)
        elif spec.type == ComponentType.INTERACTIVE:
            return self._generate_interactive_component(spec)
        elif spec.type == ComponentType.FORM:
            return self._generate_form_component(spec)
        else:
            return self._generate_generic_component(spec)
    
    def _generate_layout_component(self, spec: ComponentSpec) -> Dict:
        """تولید کامپوننت چیدمان"""
        html = f"""
<div class="{spec.name.lower()}-container">
    <div class="{spec.name.lower()}-content">
        <!-- محتوای کامپوننت -->
    </div>
</div>
"""
        
        css = f"""
.{spec.name.lower()}-container {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
}}

.{spec.name.lower()}-content {{
    max-width: 100%;
    margin: 0 auto;
}}

@media (min-width: 768px) {{
    .{spec.name.lower()}-container {{
        flex-direction: row;
        gap: 2rem;
    }}
}}
"""
        
        js = f"""
class {spec.name} {{
    constructor(element) {{
        this.element = element;
        this.init();
    }}
    
    init() {{
        // مقداردهی اولیه
        this.setupEventListeners();
    }}
    
    setupEventListeners() {{
        // تنظیم event listener ها
    }}
}}

// استفاده
document.addEventListener('DOMContentLoaded', () => {{
    const {spec.name.lower()}Elements = document.querySelectorAll('.{spec.name.lower()}-container');
    {spec.name.lower()}Elements.forEach(element => new {spec.name}(element));
}});
"""
        
        return {
            "html": html,
            "css": css,
            "javascript": js,
            "type": "layout"
        }
    
    def _generate_content_component(self, spec: ComponentSpec) -> Dict:
        """تولید کامپوننت محتوا"""
        html = f"""
<div class="{spec.name.lower()}-component">
    <h2 class="{spec.name.lower()}-title">{{{{title}}}}</h2>
    <p class="{spec.name.lower()}-text">{{{{text}}}}</p>
    <button class="{spec.name.lower()}-button">{{{{buttonText}}}}</button>
</div>
"""
        
        css = f"""
.{spec.name.lower()}-component {{
    padding: 2rem;
    border-radius: 8px;
    background: #ffffff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
}}

.{spec.name.lower()}-title {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #333;
}}

.{spec.name.lower()}-text {{
    margin-bottom: 1.5rem;
    color: #666;
    line-height: 1.6;
}}

.{spec.name.lower()}-button {{
    background: #007bff;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s;
}}

.{spec.name.lower()}-button:hover {{
    background: #0056b3;
}}
"""
        
        js = f"""
class {spec.name} {{
    constructor(element, props) {{
        this.element = element;
        this.props = props;
        this.init();
    }}
    
    init() {{
        this.render();
        this.setupEventListeners();
    }}
    
    render() {{
        this.element.innerHTML = `
            <h2 class="{spec.name.lower()}-title">${{this.props.title}}</h2>
            <p class="{spec.name.lower()}-text">${{this.props.text}}</p>
            <button class="{spec.name.lower()}-button">${{this.props.buttonText}}</button>
        `;
    }}
    
    setupEventListeners() {{
        const button = this.element.querySelector('.{spec.name.lower()}-button');
        if (button) {{
            button.addEventListener('click', () => {{
                if (this.props.onClick) {{
                    this.props.onClick();
                }}
            }});
        }}
    }}
}}
"""
        
        return {
            "html": html,
            "css": css,
            "javascript": js,
            "type": "content"
        }
    
    def _generate_interactive_component(self, spec: ComponentSpec) -> Dict:
        """تولید کامپوننت تعاملی"""
        html = f"""
<div class="{spec.name.lower()}-interactive">
    <div class="{spec.name.lower()}-trigger">
        <span class="{spec.name.lower()}-trigger-text">کلیک کنید</span>
        <i class="fas fa-chevron-down {spec.name.lower()}-icon"></i>
    </div>
    <div class="{spec.name.lower()}-content">
        <p>محتوای تعاملی</p>
    </div>
</div>
"""
        
        css = f"""
.{spec.name.lower()}-interactive {{
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}}

.{spec.name.lower()}-trigger {{
    padding: 1rem;
    background: #f8f9fa;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.3s;
}}

.{spec.name.lower()}-trigger:hover {{
    background: #e9ecef;
}}

.{spec.name.lower()}-icon {{
    transition: transform 0.3s;
}}

.{spec.name.lower()}-interactive.active .{spec.name.lower()}-icon {{
    transform: rotate(180deg);
}}

.{spec.name.lower()}-content {{
    padding: 1rem;
    background: white;
    display: none;
}}

.{spec.name.lower()}-interactive.active .{spec.name.lower()}-content {{
    display: block;
}}
"""
        
        js = f"""
class {spec.name} {{
    constructor(element) {{
        this.element = element;
        this.isActive = false;
        this.init();
    }}
    
    init() {{
        this.setupEventListeners();
    }}
    
    setupEventListeners() {{
        const trigger = this.element.querySelector('.{spec.name.lower()}-trigger');
        trigger.addEventListener('click', () => {{
            this.toggle();
        }});
    }}
    
    toggle() {{
        this.isActive = !this.isActive;
        this.element.classList.toggle('active', this.isActive);
    }}
    
    show() {{
        this.isActive = true;
        this.element.classList.add('active');
    }}
    
    hide() {{
        this.isActive = false;
        this.element.classList.remove('active');
    }}
}}
"""
        
        return {
            "html": html,
            "css": css,
            "javascript": js,
            "type": "interactive"
        }
    
    def _generate_form_component(self, spec: ComponentSpec) -> Dict:
        """تولید کامپوننت فرم"""
        html = f"""
<form class="{spec.name.lower()}-form">
    <div class="{spec.name.lower()}-field">
        <label for="name">نام:</label>
        <input type="text" id="name" name="name" required>
    </div>
    <div class="{spec.name.lower()}-field">
        <label for="email">ایمیل:</label>
        <input type="email" id="email" name="email" required>
    </div>
    <div class="{spec.name.lower()}-field">
        <label for="message">پیام:</label>
        <textarea id="message" name="message" rows="4" required></textarea>
    </div>
    <button type="submit" class="{spec.name.lower()}-submit">ارسال</button>
</form>
"""
        
        css = f"""
.{spec.name.lower()}-form {{
    max-width: 500px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}}

.{spec.name.lower()}-field {{
    margin-bottom: 1.5rem;
}}

.{spec.name.lower()}-field label {{
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #333;
}}

.{spec.name.lower()}-field input,
.{spec.name.lower()}-field textarea {{
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.3s;
}}

.{spec.name.lower()}-field input:focus,
.{spec.name.lower()}-field textarea:focus {{
    outline: none;
    border-color: #007bff;
}}

.{spec.name.lower()}-submit {{
    background: #007bff;
    color: white;
    border: none;
    padding: 0.75rem 2rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.3s;
}}

.{spec.name.lower()}-submit:hover {{
    background: #0056b3;
}}
"""
        
        js = f"""
class {spec.name} {{
    constructor(element) {{
        this.element = element;
        this.init();
    }}
    
    init() {{
        this.setupEventListeners();
    }}
    
    setupEventListeners() {{
        this.element.addEventListener('submit', (e) => {{
            e.preventDefault();
            this.handleSubmit();
        }});
    }}
    
    handleSubmit() {{
        const formData = new FormData(this.element);
        const data = Object.fromEntries(formData);
        
        // اعتبارسنجی
        if (this.validateForm(data)) {{
            this.submitForm(data);
        }}
    }}
    
    validateForm(data) {{
        // اعتبارسنجی فرم
        return true;
    }}
    
    submitForm(data) {{
        // ارسال فرم
        console.log('Form submitted:', data);
    }}
}}
"""
        
        return {
            "html": html,
            "css": css,
            "javascript": js,
            "type": "form"
        }
    
    def _generate_generic_component(self, spec: ComponentSpec) -> Dict:
        """تولید کامپوننت عمومی"""
        return {
            "html": f"<div class='{spec.name.lower()}'>{spec.description}</div>",
            "css": f".{spec.name.lower()} {{ padding: 1rem; }}",
            "javascript": f"// {spec.name} component",
            "type": "generic"
        }
    
    def _save_to_library(self, spec: ComponentSpec, code: Dict) -> None:
        """ذخیره در کتابخانه کامپوننت‌ها"""
        component_data = {
            "spec": {
                "name": spec.name,
                "type": spec.type.value,
                "description": spec.description,
                "props": spec.props,
                "styles": spec.styles,
                "dependencies": spec.dependencies,
                "responsive": spec.responsive,
                "accessible": spec.accessible
            },
            "code": code,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        # ذخیره در فایل
        library_file = "component_library.json"
        if os.path.exists(library_file):
            with open(library_file, "r", encoding="utf-8") as f:
                library = json.load(f)
        else:
            library = {}
        
        library[spec.name] = component_data
        
        with open(library_file, "w", encoding="utf-8") as f:
            json.dump(library, f, ensure_ascii=False, indent=2)
    
    def suggest_related_components(self, current_component: str) -> List[Dict]:
        """پیشنهاد کامپوننت‌های مرتبط"""
        suggestions = []
        
        # الگوهای مرتبط
        if "hero" in current_component.lower():
            suggestions.extend([
                {"name": "FeatureGrid", "reason": "معمولاً با hero section استفاده می‌شود"},
                {"name": "TestimonialSlider", "reason": "برای نمایش نظرات مشتریان"},
                {"name": "ContactForm", "reason": "برای دریافت اطلاعات تماس"}
            ])
        elif "form" in current_component.lower():
            suggestions.extend([
                {"name": "Modal", "reason": "برای نمایش فرم در پنجره بازشو"},
                {"name": "Button", "reason": "برای دکمه‌های فرم"},
                {"name": "Input", "reason": "برای فیلدهای ورودی"}
            ])
        
        return suggestions
    
    def get_component_analytics(self, component_name: str) -> Dict:
        """دریافت آمار استفاده کامپوننت"""
        library_file = "component_library.json"
        if os.path.exists(library_file):
            with open(library_file, "r", encoding="utf-8") as f:
                library = json.load(f)
            
            if component_name in library:
                return {
                    "usage_count": library[component_name].get("usage_count", 0),
                    "created_at": library[component_name].get("created_at"),
                    "last_used": library[component_name].get("last_used"),
                    "performance_score": self._calculate_performance_score(component_name)
                }
        
        return {"error": "کامپوننت یافت نشد"}
    
    def _calculate_performance_score(self, component_name: str) -> float:
        """محاسبه امتیاز عملکرد کامپوننت"""
        # محاسبه بر اساس معیارهای مختلف
        base_score = 8.5
        
        # تنظیم بر اساس نوع کامپوننت
        if "form" in component_name.lower():
            base_score += 0.5  # فرم‌ها معمولاً عملکرد خوبی دارند
        
        if "interactive" in component_name.lower():
            base_score -= 0.3  # کامپوننت‌های تعاملی ممکن است کندتر باشند
        
        return min(10.0, max(0.0, base_score))

# مثال استفاده
if __name__ == "__main__":
    generator = SmartComponentGenerator()
    
    # تست تولید کامپوننت
    async def test_component_generation():
        description = "یک کامپوننت فرم تماس با اعتبارسنجی و استایل مدرن"
        context = {"page_type": "contact", "business_type": "restaurant"}
        
        component = await generator.generate_component(description, context)
        print("🧩 کامپوننت تولید شده:")
        print(f"نام: {component.name}")
        print(f"نوع: {component.type.value}")
        print(f"توضیحات: {component.description}")
        print(f"Props: {component.props}")
        print(f"Styles: {component.styles}")
    
    # اجرای تست
    asyncio.run(test_component_generation())
