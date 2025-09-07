#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Export System - World-class output generation
Export websites in multiple formats with advanced features
"""

import json
import os
import zipfile
import base64
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, BinaryIO
from dataclasses import dataclass
from enum import Enum
import logging
import subprocess
import tempfile
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExportFormat(Enum):
    """Export formats"""
    HTML = "html"
    CSS = "css"
    JS = "js"
    ZIP = "zip"
    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    WEBP = "webp"
    MP4 = "mp4"
    GIF = "gif"
    JSON = "json"
    XML = "xml"
    DOCX = "docx"
    PPTX = "pptx"
    XLSX = "xlsx"

class ExportQuality(Enum):
    """Export quality levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"

@dataclass
class ExportOptions:
    """Export options"""
    format: ExportFormat
    quality: ExportQuality
    include_assets: bool = True
    minify: bool = True
    optimize_images: bool = True
    include_source_maps: bool = False
    watermark: bool = False
    custom_css: Optional[str] = None
    custom_js: Optional[str] = None

class AdvancedExportSystem:
    """World-class export system for multiple formats"""
    
    def __init__(self):
        self.export_templates: Dict[str, str] = {}
        self.export_presets: Dict[str, ExportOptions] = {}
        self.optimization_settings: Dict[str, Any] = {}
        
        # Initialize export system
        self._initialize_export_templates()
        self._initialize_export_presets()
        self._initialize_optimization_settings()
        
        logger.info("Advanced Export System initialized")
    
    def _initialize_export_templates(self):
        """Initialize export templates"""
        self.export_templates = {
            "responsive_html": """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <meta name="description" content="{{description}}">
    <meta name="keywords" content="{{keywords}}">
    <meta name="author" content="{{author}}">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{{title}}">
    <meta property="og:description" content="{{description}}">
    <meta property="og:image" content="{{og_image}}">
    <meta property="og:url" content="{{url}}">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{title}}">
    <meta name="twitter:description" content="{{description}}">
    <meta name="twitter:image" content="{{twitter_image}}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{{favicon}}">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="{{css_file}}">
    {{custom_css}}
    
    <!-- Preload Critical Resources -->
    <link rel="preload" href="{{critical_css}}" as="style">
    <link rel="preload" href="{{critical_font}}" as="font" type="font/woff2" crossorigin>
    
    <!-- Performance Optimizations -->
    <link rel="dns-prefetch" href="//fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Analytics -->
    {{analytics_code}}
</head>
<body>
    {{content}}
    
    <!-- Scripts -->
    <script src="{{js_file}}"></script>
    {{custom_js}}
    
    <!-- Performance Monitoring -->
    <script>
        // Performance monitoring
        window.addEventListener('load', function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart);
        });
    </script>
</body>
</html>
            """,
            "pwa_manifest": """
{
    "name": "{{app_name}}",
    "short_name": "{{short_name}}",
    "description": "{{description}}",
    "start_url": "/",
    "display": "standalone",
    "background_color": "{{bg_color}}",
    "theme_color": "{{theme_color}}",
    "orientation": "portrait-primary",
    "icons": [
        {
            "src": "{{icon_192}}",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "{{icon_512}}",
            "sizes": "512x512",
            "type": "image/png"
        }
    ],
    "categories": ["{{categories}}"],
    "lang": "fa",
    "dir": "rtl"
}
            """,
            "service_worker": """
// Service Worker for PWA
const CACHE_NAME = '{{cache_name}}';
const urlsToCache = [
    '/',
    '{{css_file}}',
    '{{js_file}}',
    '{{manifest_file}}'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});
            """
        }
    
    def _initialize_export_presets(self):
        """Initialize export presets"""
        self.export_presets = {
            "production": ExportOptions(
                format=ExportFormat.HTML,
                quality=ExportQuality.ULTRA,
                include_assets=True,
                minify=True,
                optimize_images=True,
                include_source_maps=False,
                watermark=False
            ),
            "development": ExportOptions(
                format=ExportFormat.HTML,
                quality=ExportQuality.MEDIUM,
                include_assets=True,
                minify=False,
                optimize_images=False,
                include_source_maps=True,
                watermark=True
            ),
            "presentation": ExportOptions(
                format=ExportFormat.PDF,
                quality=ExportQuality.HIGH,
                include_assets=True,
                minify=True,
                optimize_images=True,
                watermark=True
            ),
            "archive": ExportOptions(
                format=ExportFormat.ZIP,
                quality=ExportQuality.HIGH,
                include_assets=True,
                minify=True,
                optimize_images=True
            )
        }
    
    def _initialize_optimization_settings(self):
        """Initialize optimization settings"""
        self.optimization_settings = {
            "image_quality": {
                "low": 60,
                "medium": 80,
                "high": 90,
                "ultra": 95
            },
            "compression_level": {
                "low": 1,
                "medium": 6,
                "high": 9,
                "ultra": 9
            },
            "minification": {
                "html": True,
                "css": True,
                "js": True,
                "json": True
            }
        }
    
    # 1. HTML Export
    def export_html(self, content: str, options: ExportOptions, metadata: Dict = None) -> str:
        """Export as HTML with advanced features"""
        if metadata is None:
            metadata = {}
        
        # Prepare template data
        template_data = {
            "title": metadata.get("title", "My Website"),
            "description": metadata.get("description", "A beautiful website created with Site Builder"),
            "keywords": metadata.get("keywords", "website, design, modern"),
            "author": metadata.get("author", "Site Builder"),
            "og_image": metadata.get("og_image", ""),
            "twitter_image": metadata.get("twitter_image", ""),
            "url": metadata.get("url", ""),
            "favicon": metadata.get("favicon", ""),
            "css_file": "styles.css",
            "js_file": "script.js",
            "critical_css": "critical.css",
            "critical_font": "fonts.woff2",
            "analytics_code": self._generate_analytics_code(metadata.get("analytics", {})),
            "content": content,
            "custom_css": options.custom_css or "",
            "custom_js": options.custom_js or ""
        }
        
        # Generate HTML
        html_template = self.export_templates["responsive_html"]
        html_content = self._replace_template_vars(html_template, template_data)
        
        # Minify if requested
        if options.minify:
            html_content = self._minify_html(html_content)
        
        return html_content
    
    # 2. CSS Export
    def export_css(self, styles: Dict, options: ExportOptions) -> str:
        """Export as optimized CSS"""
        css_content = []
        
        # Add CSS variables
        css_content.append(self._generate_css_variables(styles.get("variables", {})))
        
        # Add base styles
        css_content.append(self._generate_base_styles())
        
        # Add component styles
        for component, style in styles.get("components", {}).items():
            css_content.append(self._generate_component_css(component, style))
        
        # Add responsive styles
        css_content.append(self._generate_responsive_css(styles.get("responsive", {})))
        
        # Add animations
        css_content.append(self._generate_animations_css(styles.get("animations", {})))
        
        # Combine all CSS
        full_css = "\n".join(css_content)
        
        # Minify if requested
        if options.minify:
            full_css = self._minify_css(full_css)
        
        return full_css
    
    # 3. JavaScript Export
    def export_js(self, scripts: Dict, options: ExportOptions) -> str:
        """Export as optimized JavaScript"""
        js_content = []
        
        # Add utility functions
        js_content.append(self._generate_utility_functions())
        
        # Add component scripts
        for component, script in scripts.get("components", {}).items():
            js_content.append(self._generate_component_js(component, script))
        
        # Add event handlers
        js_content.append(self._generate_event_handlers(scripts.get("events", {})))
        
        # Add performance optimizations
        js_content.append(self._generate_performance_js())
        
        # Combine all JavaScript
        full_js = "\n".join(js_content)
        
        # Minify if requested
        if options.minify:
            full_js = self._minify_js(full_js)
        
        return full_js
    
    # 4. ZIP Archive Export
    def export_zip(self, files: Dict[str, str], options: ExportOptions) -> bytes:
        """Export as ZIP archive"""
        zip_buffer = tempfile.NamedTemporaryFile()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, 
                           compresslevel=self.optimization_settings["compression_level"][options.quality.value]) as zip_file:
            
            for file_path, file_content in files.items():
                # Optimize content based on file type
                if file_path.endswith(('.html', '.css', '.js')):
                    if options.minify:
                        if file_path.endswith('.html'):
                            file_content = self._minify_html(file_content)
                        elif file_path.endswith('.css'):
                            file_content = self._minify_css(file_content)
                        elif file_path.endswith('.js'):
                            file_content = self._minify_js(file_content)
                
                zip_file.writestr(file_path, file_content)
        
        zip_buffer.seek(0)
        return zip_buffer.read()
    
    # 5. PDF Export
    def export_pdf(self, html_content: str, options: ExportOptions, metadata: Dict = None) -> bytes:
        """Export as PDF"""
        try:
            # Use weasyprint for PDF generation
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
            
            # Create HTML document
            html_doc = HTML(string=html_content)
            
            # Add CSS for PDF
            pdf_css = CSS(string=self._generate_pdf_css())
            
            # Generate PDF
            pdf_bytes = html_doc.write_pdf(stylesheets=[pdf_css])
            
            return pdf_bytes
            
        except ImportError:
            logger.warning("WeasyPrint not available, using fallback PDF generation")
            return self._fallback_pdf_generation(html_content)
    
    # 6. Image Export
    def export_image(self, html_content: str, options: ExportOptions, 
                    format: str = "png", width: int = 1920, height: int = 1080) -> bytes:
        """Export as image"""
        try:
            # Use playwright for image generation
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={'width': width, 'height': height})
                page.set_content(html_content)
                
                # Wait for content to load
                page.wait_for_load_state('networkidle')
                
                # Take screenshot
                image_bytes = page.screenshot(type=format, full_page=True)
                
                browser.close()
                
                return image_bytes
                
        except ImportError:
            logger.warning("Playwright not available, using fallback image generation")
            return self._fallback_image_generation(html_content, format, width, height)
    
    # 7. PWA Export
    def export_pwa(self, content: str, options: ExportOptions, metadata: Dict = None) -> Dict[str, str]:
        """Export as Progressive Web App"""
        if metadata is None:
            metadata = {}
        
        pwa_files = {}
        
        # Generate manifest
        manifest_data = {
            "app_name": metadata.get("title", "My PWA"),
            "short_name": metadata.get("short_name", "MyApp"),
            "description": metadata.get("description", "A Progressive Web App"),
            "bg_color": metadata.get("bg_color", "#ffffff"),
            "theme_color": metadata.get("theme_color", "#667eea"),
            "icon_192": "icon-192.png",
            "icon_512": "icon-512.png",
            "categories": "productivity,utilities",
            "cache_name": f"pwa-cache-{int(time.time())}",
            "css_file": "styles.css",
            "js_file": "script.js",
            "manifest_file": "manifest.json"
        }
        
        manifest_content = self._replace_template_vars(
            self.export_templates["pwa_manifest"], manifest_data
        )
        pwa_files["manifest.json"] = manifest_content
        
        # Generate service worker
        sw_content = self._replace_template_vars(
            self.export_templates["service_worker"], manifest_data
        )
        pwa_files["sw.js"] = sw_content
        
        # Generate HTML with PWA features
        pwa_html = self.export_html(content, options, metadata)
        pwa_files["index.html"] = pwa_html
        
        return pwa_files
    
    # 8. Static Site Generator
    def export_static_site(self, pages: Dict[str, str], options: ExportOptions, 
                          metadata: Dict = None) -> Dict[str, str]:
        """Export as static site"""
        if metadata is None:
            metadata = {}
        
        static_files = {}
        
        # Generate each page
        for page_path, page_content in pages.items():
            page_metadata = {**metadata, "title": f"{metadata.get('title', 'Site')} - {page_path}"}
            html_content = self.export_html(page_content, options, page_metadata)
            static_files[page_path] = html_content
        
        # Generate sitemap
        sitemap = self._generate_sitemap(pages.keys(), metadata.get("base_url", ""))
        static_files["sitemap.xml"] = sitemap
        
        # Generate robots.txt
        robots = self._generate_robots_txt(metadata.get("base_url", ""))
        static_files["robots.txt"] = robots
        
        return static_files
    
    # 9. Advanced Optimization
    def optimize_export(self, content: str, format: str, options: ExportOptions) -> str:
        """Apply advanced optimizations"""
        optimized_content = content
        
        if format == "html":
            # Remove unused CSS
            optimized_content = self._remove_unused_css(optimized_content)
            
            # Optimize images
            if options.optimize_images:
                optimized_content = self._optimize_images(optimized_content, options.quality)
            
            # Add performance hints
            optimized_content = self._add_performance_hints(optimized_content)
        
        elif format == "css":
            # Remove unused selectors
            optimized_content = self._remove_unused_selectors(optimized_content)
            
            # Optimize colors
            optimized_content = self._optimize_colors(optimized_content)
        
        elif format == "js":
            # Tree shaking
            optimized_content = self._tree_shake_js(optimized_content)
            
            # Dead code elimination
            optimized_content = self._eliminate_dead_code(optimized_content)
        
        return optimized_content
    
    # 10. Export Analytics
    def generate_export_report(self, export_data: Dict) -> Dict:
        """Generate export analytics report"""
        report = {
            "export_time": datetime.now().isoformat(),
            "total_files": len(export_data.get("files", {})),
            "total_size": sum(len(content) for content in export_data.get("files", {}).values()),
            "formats": list(set(file.split('.')[-1] for file in export_data.get("files", {}).keys())),
            "optimization_applied": export_data.get("optimization", {}),
            "performance_score": self._calculate_performance_score(export_data),
            "accessibility_score": self._calculate_accessibility_score(export_data),
            "seo_score": self._calculate_seo_score(export_data)
        }
        
        return report
    
    # Helper methods
    def _replace_template_vars(self, template: str, data: Dict) -> str:
        """Replace template variables"""
        for key, value in data.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template
    
    def _minify_html(self, html: str) -> str:
        """Minify HTML"""
        # Simple HTML minification
        import re
        html = re.sub(r'\s+', ' ', html)
        html = re.sub(r'>\s+<', '><', html)
        return html.strip()
    
    def _minify_css(self, css: str) -> str:
        """Minify CSS"""
        import re
        css = re.sub(r'\s+', ' ', css)
        css = re.sub(r';\s*}', '}', css)
        css = re.sub(r'{\s*', '{', css)
        css = re.sub(r';\s*', ';', css)
        return css.strip()
    
    def _minify_js(self, js: str) -> str:
        """Minify JavaScript"""
        import re
        js = re.sub(r'\s+', ' ', js)
        js = re.sub(r';\s*}', '}', js)
        js = re.sub(r'{\s*', '{', js)
        return js.strip()
    
    def _generate_analytics_code(self, analytics_config: Dict) -> str:
        """Generate analytics code"""
        if not analytics_config:
            return ""
        
        code = ""
        if analytics_config.get("google_analytics"):
            code += f"""
            <!-- Google Analytics -->
            <script async src="https://www.googletagmanager.com/gtag/js?id={analytics_config['google_analytics']}"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){{dataLayer.push(arguments);}}
                gtag('js', new Date());
                gtag('config', '{analytics_config['google_analytics']}');
            </script>
            """
        
        return code
    
    def _generate_css_variables(self, variables: Dict) -> str:
        """Generate CSS variables"""
        css_vars = [":root {"]
        for key, value in variables.items():
            css_vars.append(f"  --{key}: {value};")
        css_vars.append("}")
        return "\n".join(css_vars)
    
    def _generate_base_styles(self) -> str:
        """Generate base styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        img {
            max-width: 100%;
            height: auto;
        }
        """
    
    def _generate_component_css(self, component: str, style: Dict) -> str:
        """Generate component CSS"""
        return f".{component} {{ {style} }}"
    
    def _generate_responsive_css(self, responsive: Dict) -> str:
        """Generate responsive CSS"""
        css = []
        for breakpoint, styles in responsive.items():
            css.append(f"@media (max-width: {breakpoint}px) {{ {styles} }}")
        return "\n".join(css)
    
    def _generate_animations_css(self, animations: Dict) -> str:
        """Generate animations CSS"""
        css = []
        for name, animation in animations.items():
            css.append(f"@keyframes {name} {{ {animation} }}")
        return "\n".join(css)
    
    def _generate_utility_functions(self) -> str:
        """Generate utility functions"""
        return """
        // Utility functions
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
        
        function throttle(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }
        """
    
    def _generate_component_js(self, component: str, script: str) -> str:
        """Generate component JavaScript"""
        return f"// {component}\n{script}"
    
    def _generate_event_handlers(self, events: Dict) -> str:
        """Generate event handlers"""
        handlers = []
        for event, handler in events.items():
            handlers.append(f"document.addEventListener('{event}', {handler});")
        return "\n".join(handlers)
    
    def _generate_performance_js(self) -> str:
        """Generate performance monitoring JavaScript"""
        return """
        // Performance monitoring
        window.addEventListener('load', function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart);
            
            // Report to analytics
            if (typeof gtag !== 'undefined') {
                gtag('event', 'page_load_time', {
                    'value': Math.round(perfData.loadEventEnd - perfData.loadEventStart)
                });
            }
        });
        """
    
    def _generate_pdf_css(self) -> str:
        """Generate CSS for PDF export"""
        return """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-size: 12pt;
            line-height: 1.4;
        }
        
        h1 { font-size: 18pt; }
        h2 { font-size: 16pt; }
        h3 { font-size: 14pt; }
        
        .page-break {
            page-break-before: always;
        }
        """
    
    def _generate_sitemap(self, pages: List[str], base_url: str) -> str:
        """Generate XML sitemap"""
        sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
        sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        
        for page in pages:
            sitemap.append(f'  <url>')
            sitemap.append(f'    <loc>{base_url}/{page}</loc>')
            sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
            sitemap.append(f'    <changefreq>weekly</changefreq>')
            sitemap.append(f'    <priority>0.8</priority>')
            sitemap.append(f'  </url>')
        
        sitemap.append('</urlset>')
        return '\n'.join(sitemap)
    
    def _generate_robots_txt(self, base_url: str) -> str:
        """Generate robots.txt"""
        return f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
        """
    
    def _calculate_performance_score(self, export_data: Dict) -> int:
        """Calculate performance score"""
        # Simple performance scoring
        files = export_data.get("files", {})
        total_size = sum(len(content) for content in files.values())
        
        if total_size < 100000:  # < 100KB
            return 100
        elif total_size < 500000:  # < 500KB
            return 80
        elif total_size < 1000000:  # < 1MB
            return 60
        else:
            return 40
    
    def _calculate_accessibility_score(self, export_data: Dict) -> int:
        """Calculate accessibility score"""
        # Simple accessibility scoring
        html_content = ""
        for file_path, content in export_data.get("files", {}).items():
            if file_path.endswith('.html'):
                html_content += content
        
        score = 100
        
        # Check for alt attributes
        if 'alt=' not in html_content:
            score -= 20
        
        # Check for semantic HTML
        if '<header>' not in html_content and '<nav>' not in html_content:
            score -= 15
        
        # Check for ARIA labels
        if 'aria-label' not in html_content:
            score -= 10
        
        return max(0, score)
    
    def _calculate_seo_score(self, export_data: Dict) -> int:
        """Calculate SEO score"""
        # Simple SEO scoring
        html_content = ""
        for file_path, content in export_data.get("files", {}).items():
            if file_path.endswith('.html'):
                html_content += content
        
        score = 100
        
        # Check for title tag
        if '<title>' not in html_content:
            score -= 25
        
        # Check for meta description
        if 'meta name="description"' not in html_content:
            score -= 20
        
        # Check for heading structure
        if '<h1>' not in html_content:
            score -= 15
        
        # Check for alt attributes
        if 'alt=' not in html_content:
            score -= 10
        
        return max(0, score)
    
    def _fallback_pdf_generation(self, html_content: str) -> bytes:
        """Fallback PDF generation"""
        # Simple fallback - return HTML as text
        return html_content.encode('utf-8')
    
    def _fallback_image_generation(self, html_content: str, format: str, width: int, height: int) -> bytes:
        """Fallback image generation"""
        # Simple fallback - return HTML as text
        return html_content.encode('utf-8')

# Example usage and testing
if __name__ == "__main__":
    # Initialize export system
    export_system = AdvancedExportSystem()
    
    print("📤 Advanced Export System Demo")
    print("=" * 50)
    
    # Test HTML export
    print("\n1. Testing HTML export...")
    html_content = export_system.export_html(
        "<h1>Hello World</h1><p>This is a test page.</p>",
        export_system.export_presets["production"],
        {"title": "Test Page", "description": "A test page"}
    )
    print(f"✅ HTML exported: {len(html_content)} characters")
    
    # Test CSS export
    print("\n2. Testing CSS export...")
    css_content = export_system.export_css(
        {
            "variables": {"primary-color": "#667eea", "secondary-color": "#764ba2"},
            "components": {"button": "background: var(--primary-color); color: white;"},
            "responsive": {"768": ".button { font-size: 14px; }"},
            "animations": {"fadeIn": "from { opacity: 0; } to { opacity: 1; }"}
        },
        export_system.export_presets["production"]
    )
    print(f"✅ CSS exported: {len(css_content)} characters")
    
    # Test JavaScript export
    print("\n3. Testing JavaScript export...")
    js_content = export_system.export_js(
        {
            "components": {"button": "console.log('Button clicked');"},
            "events": {"click": "function(e) { console.log('Click event'); }"}
        },
        export_system.export_presets["production"]
    )
    print(f"✅ JavaScript exported: {len(js_content)} characters")
    
    # Test PWA export
    print("\n4. Testing PWA export...")
    pwa_files = export_system.export_pwa(
        "<h1>PWA Test</h1>",
        export_system.export_presets["production"],
        {"title": "PWA App", "short_name": "PWA"}
    )
    print(f"✅ PWA exported: {len(pwa_files)} files")
    
    # Test static site export
    print("\n5. Testing static site export...")
    static_files = export_system.export_static_site(
        {
            "index.html": "<h1>Home</h1>",
            "about.html": "<h1>About</h1>",
            "contact.html": "<h1>Contact</h1>"
        },
        export_system.export_presets["production"],
        {"title": "My Site", "base_url": "https://mysite.com"}
    )
    print(f"✅ Static site exported: {len(static_files)} files")
    
    # Test export report
    print("\n6. Testing export report...")
    export_data = {
        "files": {"index.html": html_content, "styles.css": css_content},
        "optimization": {"minified": True, "compressed": True}
    }
    report = export_system.generate_export_report(export_data)
    print(f"✅ Export report generated:")
    print(f"   Performance Score: {report['performance_score']}")
    print(f"   Accessibility Score: {report['accessibility_score']}")
    print(f"   SEO Score: {report['seo_score']}")
    
    print("\n🎉 Advanced Export System Demo completed!")
    print("=" * 50)
