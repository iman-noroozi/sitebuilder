import json
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
from pathlib import Path

class TemplateParser:
    def __init__(self):
        self.supported_frameworks = ['bootstrap', 'tailwind', 'bulma', 'foundation']
        self.component_patterns = {
            'navbar': ['nav', '.navbar', '.navigation', '.header-menu'],
            'hero': ['.hero', '.jumbotron', '.banner', '.intro'],
            'card': ['.card', '.product', '.service', '.feature'],
            'footer': ['footer', '.footer', '.site-footer'],
            'sidebar': ['.sidebar', '.aside', '.widget-area'],
            'gallery': ['.gallery', '.portfolio', '.grid'],
            'form': ['form', '.contact-form', '.subscribe'],
            'testimonial': ['.testimonial', '.review', '.quote']
        }
    
    def parse_template(self, template_path):
        """تجزیه و تحلیل قالب استخراج شده"""
        print(f"شروع تجزیه قالب: {template_path}")
        
        # خواندن فایل JSON قالب
        template_file = os.path.join(template_path, 'template.json')
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"فایل قالب یافت نشد: {template_file}")
        
        with open(template_file, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        html_content = template_data.get('html', '')
        css_content = template_data.get('styles', '')
        
        # تجزیه HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        analysis = {
            'metadata': template_data.get('metadata', {}),
            'framework': self._detect_framework(html_content, css_content),
            'components': self._extract_components(soup),
            'layout_structure': self._analyze_layout(soup),
            'colors': self._extract_colors(css_content),
            'fonts': self._extract_fonts(css_content),
            'images': self._extract_images(soup),
            'responsive_breakpoints': self._find_breakpoints(css_content),
            'javascript_features': self._analyze_js_features(html_content)
        }
        
        # ذخیره تجزیه و تحلیل
        analysis_file = os.path.join(template_path, 'analysis.json')
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"تجزیه و تحلیل در {analysis_file} ذخیره شد")
        return analysis
    
    def _detect_framework(self, html, css):
        """تشخیص فریمورک CSS استفاده شده"""
        frameworks_found = []
        
        # Bootstrap
        if 'bootstrap' in html.lower() or 'btn btn-' in html or 'container-fluid' in html:
            frameworks_found.append('bootstrap')
        
        # Tailwind CSS
        if 'tailwindcss' in html.lower() or re.search(r'\b(bg-\w+|text-\w+|p-\d+|m-\d+)\b', html):
            frameworks_found.append('tailwind')
        
        # Bulma
        if 'bulma' in html.lower() or 'is-primary' in html or 'column' in html:
            frameworks_found.append('bulma')
        
        # Foundation
        if 'foundation' in html.lower() or 'grid-x' in html:
            frameworks_found.append('foundation')
        
        return frameworks_found
    
    def _extract_components(self, soup):
        """استخراج کامپوننت‌های قابل تشخیص"""
        components = {}
        
        for component_name, selectors in self.component_patterns.items():
            found_elements = []
            
            for selector in selectors:
                if selector.startswith('.'):
                    elements = soup.find_all(class_=selector[1:])
                elif selector.startswith('#'):
                    elements = soup.find_all(id=selector[1:])
                else:
                    elements = soup.find_all(selector)
                
                for element in elements:
                    found_elements.append({
                        'tag': element.name,
                        'classes': element.get('class', []),
                        'id': element.get('id'),
                        'html': str(element)[:500] + '...' if len(str(element)) > 500 else str(element)
                    })
            
            if found_elements:
                components[component_name] = found_elements
        
        return components
    
    def _analyze_layout(self, soup):
        """تحلیل ساختار لی‌اوت"""
        layout = {
            'has_header': bool(soup.find(['header', 'nav']) or soup.find(class_=re.compile(r'header|nav'))),
            'has_footer': bool(soup.find('footer') or soup.find(class_=re.compile(r'footer'))),
            'has_sidebar': bool(soup.find(class_=re.compile(r'sidebar|aside'))),
            'main_sections': len(soup.find_all(['section', 'main', 'article'])),
            'grid_system': self._detect_grid_system(soup)
        }
        
        return layout
    
    def _detect_grid_system(self, soup):
        """تشخیص سیستم Grid استفاده شده"""
        html_str = str(soup)
        
        if 'display: grid' in html_str or 'grid-template' in html_str:
            return 'css-grid'
        elif 'display: flex' in html_str or 'flex-' in html_str:
            return 'flexbox'
        elif 'col-' in html_str:
            return 'bootstrap-grid'
        elif re.search(r'grid-cols-\d+', html_str):
            return 'tailwind-grid'
        else:
            return 'unknown'
    
    def _extract_colors(self, css):
        """استخراج پالت رنگی"""
        color_patterns = [
            r'#[0-9a-fA-F]{6}',  # Hex colors
            r'#[0-9a-fA-F]{3}',   # Short hex colors
            r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)',  # RGB
            r'rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)',  # RGBA
            r'hsl\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*\)',  # HSL
        ]
        
        colors = set()
        for pattern in color_patterns:
            matches = re.findall(pattern, css)
            colors.update(matches)
        
        return list(colors)
    
    def _extract_fonts(self, css):
        """استخراج فونت‌های استفاده شده"""
        font_pattern = r'font-family\s*:\s*([^;]+)'
        fonts = re.findall(font_pattern, css, re.IGNORECASE)
        
        cleaned_fonts = []
        for font in fonts:
            font = font.strip().replace('"', '').replace("'", '')
            if font not in cleaned_fonts:
                cleaned_fonts.append(font)
        
        return cleaned_fonts
    
    def _extract_images(self, soup):
        """استخراج تصاویر و منابع مدیا"""
        images = []
        
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src'),
                'alt': img.get('alt'),
                'class': img.get('class'),
                'width': img.get('width'),
                'height': img.get('height')
            })
        
        return images
    
    def _find_breakpoints(self, css):
        """یافتن نقاط شکست واکنش‌گرا"""
        breakpoint_pattern = r'@media[^{]+\((?:max-width|min-width):\s*(\d+px)\)'
        breakpoints = re.findall(breakpoint_pattern, css)
        
        unique_breakpoints = list(set(breakpoints))
        unique_breakpoints.sort(key=lambda x: int(x.replace('px', '')))
        
        return unique_breakpoints
    
    def _analyze_js_features(self, html):
        """تحلیل ویژگی‌های JavaScript"""
        features = {
            'has_jquery': 'jquery' in html.lower(),
            'has_bootstrap_js': 'bootstrap' in html.lower() and '.js' in html.lower(),
            'has_custom_js': bool(re.search(r'<script[^>]*>.*?</script>', html, re.DOTALL)),
            'interactive_elements': len(re.findall(r'onclick|onchange|onsubmit', html, re.IGNORECASE))
        }
        
        return features
    
    def generate_editable_structure(self, analysis, output_path):
        """تولید ساختار قابل ویرایش برای ادیتور"""
        editable_structure = {
            'template_id': analysis['metadata'].get('url', 'unknown'),
            'title': analysis['metadata'].get('title', 'Untitled Template'),
            'framework': analysis.get('framework', []),
            'blocks': [],
            'global_styles': {
                'colors': analysis.get('colors', []),
                'fonts': analysis.get('fonts', []),
                'breakpoints': analysis.get('responsive_breakpoints', [])
            }
        }
        
        # تبدیل کامپوننت‌ها به بلاک‌های قابل ویرایش
        for component_type, components in analysis.get('components', {}).items():
            for i, component in enumerate(components):
                block = {
                    'id': f"{component_type}_{i}",
                    'type': component_type,
                    'name': f"{component_type.title()} {i+1}",
                    'html': component['html'],
                    'classes': component['classes'],
                    'editable': True,
                    'draggable': True
                }
                editable_structure['blocks'].append(block)
        
        # ذخیره ساختار قابل ویرایش
        output_file = os.path.join(output_path, 'editable_structure.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(editable_structure, f, indent=2, ensure_ascii=False)
        
        print(f"ساختار قابل ویرایش در {output_file} ذخیره شد")
        return editable_structure

# استفاده
if __name__ == "__main__":
    parser = TemplateParser()
    
    # مثال استفاده
    template_path = "./extracted_templates/template_1"
    if os.path.exists(template_path):
        analysis = parser.parse_template(template_path)
        parser.generate_editable_structure(analysis, template_path)
        print("تجزیه و تحلیل کامل شد!")
    else:
        print(f"مسیر قالب یافت نشد: {template_path}")
