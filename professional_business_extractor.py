#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏢 استخراج کامل سایت‌های حرفه‌ای برای پلتفرم کسب‌وکار
مخصوص قالب‌ها، سیستم‌های مدیریت، حسابداری و نقشه‌ها
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from datetime import datetime

class ProfessionalBusinessExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.base_output_dir = Path("extraction_module/extracted_sites/extracted_sites")
        self.base_output_dir.mkdir(parents=True, exist_ok=True)

    def extract_business_site(self, url, name, category):
        """استخراج سایت با تحلیل کسب‌وکاری"""
        print(f"🏢 شروع استخراج: {name}")
        print(f"🔗 URL: {url}")
        print(f"📂 دسته: {category}")
        
        output_path = self.base_output_dir / name
        output_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # دریافت HTML
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            html_content = response.text
            
            # ذخیره HTML
            with open(output_path / "index.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # پارس کردن
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # تحلیل کسب‌وکاری
            business_analysis = self._analyze_business_features(soup, url)
            
            # متادیتا کامل
            metadata = {
                "basic_info": {
                    "url": url,
                    "name": name,
                    "category": category,
                    "title": soup.title.string if soup.title else "",
                    "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "size": len(html_content)
                },
                "business_features": business_analysis,
                "seo_analysis": self._analyze_seo(soup),
                "technical_analysis": self._analyze_technical(soup),
                "ui_ux_analysis": self._analyze_ui_ux(soup),
                "extraction_status": "success"
            }
            
            # ذخیره متادیتا
            with open(output_path / "metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            # تولید README
            self._generate_business_readme(output_path, metadata)
            
            print(f"✅ استخراج موفق: {name}")
            return True
            
        except Exception as e:
            print(f"❌ خطا در استخراج {name}: {e}")
            error_metadata = {
                "url": url,
                "name": name,
                "category": category,
                "error": str(e),
                "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "extraction_status": "failed"
            }
            
            with open(output_path / "error.json", 'w', encoding='utf-8') as f:
                json.dump(error_metadata, f, ensure_ascii=False, indent=2)
            
            return False

    def _analyze_business_features(self, soup, url):
        """تحلیل ویژگی‌های کسب‌وکاری"""
        features = {
            "business_type": self._detect_business_type(soup, url),
            "key_features": [],
            "business_services": [],
            "target_audience": self._detect_target_audience(soup),
            "business_size": self._estimate_business_size(soup),
            "industry_vertical": self._detect_industry(soup, url)
        }
        
        # تشخیص ویژگی‌های کلیدی
        if self._has_ecommerce(soup):
            features["key_features"].append("E-commerce")
            features["business_services"].append("فروش آنلاین")
        
        if self._has_booking(soup):
            features["key_features"].append("Booking System")
            features["business_services"].append("رزرو آنلاین")
        
        if self._has_payment(soup):
            features["key_features"].append("Payment Gateway")
            features["business_services"].append("درگاه پرداخت")
        
        if self._has_map(soup):
            features["key_features"].append("Map Integration")
            features["business_services"].append("نقشه و موقعیت")
        
        if self._has_crm(soup):
            features["key_features"].append("CRM Features")
            features["business_services"].append("مدیریت مشتری")
        
        if self._has_inventory(soup):
            features["key_features"].append("Inventory Management")
            features["business_services"].append("مدیریت موجودی")
        
        if self._has_accounting(soup):
            features["key_features"].append("Accounting System")
            features["business_services"].append("سیستم حسابداری")
        
        return features

    def _detect_business_type(self, soup, url):
        """تشخیص نوع کسب‌وکار"""
        text = soup.get_text().lower()
        url_lower = url.lower()
        
        business_keywords = {
            "restaurant": ["restaurant", "food", "menu", "dining", "cafe"],
            "retail": ["shop", "store", "buy", "product", "cart"],
            "service": ["service", "appointment", "booking", "consultation"],
            "healthcare": ["health", "medical", "doctor", "clinic", "hospital"],
            "beauty": ["beauty", "salon", "spa", "hair", "makeup"],
            "education": ["education", "school", "course", "training", "learn"],
            "finance": ["finance", "bank", "payment", "accounting", "invoice"],
            "real_estate": ["property", "real estate", "house", "apartment"],
            "automotive": ["car", "auto", "vehicle", "repair", "garage"],
            "technology": ["tech", "software", "app", "digital", "it"]
        }
        
        for biz_type, keywords in business_keywords.items():
            if any(keyword in text or keyword in url_lower for keyword in keywords):
                return biz_type
        
        return "general"

    def _detect_target_audience(self, soup):
        """تشخیص مخاطب هدف"""
        text = soup.get_text().lower()
        
        if any(word in text for word in ["enterprise", "corporation", "business", "company"]):
            return "B2B"
        elif any(word in text for word in ["government", "public", "municipal"]):
            return "B2G"
        else:
            return "B2C"

    def _estimate_business_size(self, soup):
        """تخمین اندازه کسب‌وکار"""
        text = soup.get_text().lower()
        
        if any(word in text for word in ["enterprise", "corporation", "global", "international"]):
            return "large"
        elif any(word in text for word in ["medium", "regional", "multi-location"]):
            return "medium"
        elif any(word in text for word in ["small", "local", "family", "startup"]):
            return "small"
        else:
            return "micro"

    def _detect_industry(self, soup, url):
        """تشخیص صنعت"""
        text = soup.get_text().lower()
        url_lower = url.lower()
        
        industries = {
            "technology": ["tech", "software", "digital", "ai", "cloud"],
            "healthcare": ["health", "medical", "care", "wellness"],
            "finance": ["finance", "bank", "invest", "money", "payment"],
            "retail": ["retail", "shop", "store", "commerce"],
            "food": ["food", "restaurant", "cafe", "dining"],
            "education": ["education", "school", "university", "training"],
            "real_estate": ["property", "real estate", "construction"],
            "automotive": ["auto", "car", "vehicle", "transport"],
            "beauty": ["beauty", "salon", "cosmetic", "spa"],
            "manufacturing": ["manufacturing", "production", "factory"]
        }
        
        for industry, keywords in industries.items():
            if any(keyword in text or keyword in url_lower for keyword in keywords):
                return industry
        
        return "general"

    def _has_ecommerce(self, soup):
        """بررسی وجود فروشگاه آنلاین"""
        indicators = ["add to cart", "buy now", "checkout", "shopping cart", "price", "$"]
        text = soup.get_text().lower()
        return any(indicator in text for indicator in indicators)

    def _has_booking(self, soup):
        """بررسی سیستم رزرو"""
        indicators = ["book", "appointment", "reserve", "schedule", "availability"]
        text = soup.get_text().lower()
        return any(indicator in text for indicator in indicators)

    def _has_payment(self, soup):
        """بررسی درگاه پرداخت"""
        indicators = ["payment", "pay", "checkout", "credit card", "paypal", "stripe"]
        text = soup.get_text().lower()
        return any(indicator in text for indicator in indicators)

    def _has_map(self, soup):
        """بررسی نقشه"""
        return bool(soup.find_all(['iframe', 'div'], attrs={'src': lambda x: x and 'maps' in x}) or
                   soup.find_all(attrs={'class': lambda x: x and 'map' in str(x).lower()}))

    def _has_crm(self, soup):
        """بررسی CRM"""
        indicators = ["crm", "customer management", "lead", "contact management"]
        text = soup.get_text().lower()
        return any(indicator in text for indicator in indicators)

    def _has_inventory(self, soup):
        """بررسی مدیریت موجودی"""
        indicators = ["inventory", "stock", "warehouse", "product management"]
        text = soup.get_text().lower()
        return any(indicator in text for indicator in indicators)

    def _has_accounting(self, soup):
        """بررسی سیستم حسابداری"""
        indicators = ["accounting", "invoice", "billing", "financial", "bookkeeping"]
        text = soup.get_text().lower()
        return any(indicator in text for indicator in indicators)

    def _analyze_seo(self, soup):
        """تحلیل SEO"""
        return {
            "meta_description": self._get_meta_content(soup, "description"),
            "meta_keywords": self._get_meta_content(soup, "keywords"),
            "og_title": self._get_meta_property(soup, "og:title"),
            "og_description": self._get_meta_property(soup, "og:description"),
            "h1_count": len(soup.find_all('h1')),
            "h2_count": len(soup.find_all('h2')),
            "img_alt_missing": len([img for img in soup.find_all('img') if not img.get('alt')])
        }

    def _analyze_technical(self, soup):
        """تحلیل فنی"""
        return {
            "has_responsive": bool(soup.find('meta', attrs={'name': 'viewport'})),
            "css_files": len(soup.find_all('link', attrs={'rel': 'stylesheet'})),
            "js_files": len(soup.find_all('script', attrs={'src': True})),
            "external_links": len([a for a in soup.find_all('a', href=True) if 'http' in a['href']]),
            "forms": len(soup.find_all('form')),
            "has_ssl": True  # اگر درخواست موفق بود، احتمالاً SSL دارد
        }

    def _analyze_ui_ux(self, soup):
        """تحلیل UI/UX"""
        return {
            "navigation_menus": len(soup.find_all(['nav', 'ul', 'ol'])),
            "buttons": len(soup.find_all(['button', 'input'], attrs={'type': 'submit'})),
            "images": len(soup.find_all('img')),
            "videos": len(soup.find_all(['video', 'iframe'])),
            "contact_forms": len([form for form in soup.find_all('form') 
                                if any(field in str(form).lower() for field in ['email', 'contact', 'message'])])
        }

    def _get_meta_content(self, soup, name):
        """دریافت محتوای meta tag"""
        meta = soup.find('meta', attrs={'name': name})
        return meta.get('content', '') if meta else ''

    def _get_meta_property(self, soup, property_name):
        """دریافت محتوای meta property"""
        meta = soup.find('meta', attrs={'property': property_name})
        return meta.get('content', '') if meta else ''

    def _generate_business_readme(self, output_path, metadata):
        """تولید README برای هر سایت"""
        basic = metadata['basic_info']
        business = metadata['business_features']
        
        readme_content = f"""# {basic['name']}

## 📊 اطلاعات کلی
- **URL:** {basic['url']}
- **دسته:** {basic['category']}
- **تاریخ استخراج:** {basic['extracted_at']}
- **اندازه:** {basic['size']:,} بایت

## 🏢 تحلیل کسب‌وکاری
- **نوع کسب‌وکار:** {business['business_type']}
- **اندازه:** {business['business_size']}
- **صنعت:** {business['industry_vertical']}
- **مخاطب:** {business['target_audience']}

## ⭐ ویژگی‌های کلیدی
{chr(10).join(f"- {feature}" for feature in business['key_features'])}

## 🔧 خدمات کسب‌وکاری
{chr(10).join(f"- {service}" for service in business['business_services'])}

## 🎯 کاربرد برای قالب
این سایت برای {business['business_type']} مناسب است و می‌تواند الهام‌بخش قالب‌های:
- کسب‌وکارهای {business['business_size']}
- صنعت {business['industry_vertical']}
- مخاطبان {business['target_audience']}

---
*استخراج شده توسط Professional Business Extractor*
"""
        
        with open(output_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)

def main():
    """استخراج سایت‌های حرفه‌ای کسب‌وکار"""
    extractor = ProfessionalBusinessExtractor()
    
    # سایت‌های قالب کسب‌وکار
    template_sites = [
        # قالب‌های کسب‌وکار کوچک
        ("https://themeforest.net", "themeforest_templates", "business_templates"),
        ("https://templatemonster.com", "templatemonster", "business_templates"),
        ("https://colorlib.com", "colorlib_templates", "business_templates"),
        
        # سیستم‌های مدیریت کسب‌وکار
        ("https://freshbooks.com", "freshbooks_accounting", "accounting_software"),
        ("https://quickbooks.intuit.com", "quickbooks", "accounting_software"),
        ("https://www.zoho.com", "zoho_business", "business_management"),
        ("https://monday.com", "monday_project", "project_management"),
        
        # سیستم‌های فروش و CRM
        ("https://shopify.com", "shopify_ecommerce", "ecommerce_platform"),
        ("https://woocommerce.com", "woocommerce", "ecommerce_platform"),
        ("https://salesforce.com", "salesforce_crm", "crm_system"),
        ("https://hubspot.com", "hubspot_crm", "crm_system"),
        
        # سیستم‌های نقشه و موقعیت
        ("https://foursquare.com", "foursquare_business", "location_services"),
        ("https://business.google.com", "google_business", "business_listing"),
        ("https://www.yelp.com/biz", "yelp_business", "business_directory"),
        
        # رستوران و غذا
        ("https://www.opentable.com", "opentable_restaurant", "restaurant_booking"),
        ("https://www.ubereats.com", "ubereats", "food_delivery"),
        ("https://www.doordash.com", "doordash", "food_delivery"),
        
        # زیبایی و سلامت
        ("https://www.vagaro.com", "vagaro_salon", "salon_booking"),
        ("https://www.booksy.com", "booksy_beauty", "beauty_booking"),
        ("https://www.fresha.com", "fresha_wellness", "wellness_booking"),
        
        # خرده‌فروشی
        ("https://square.com", "square_retail", "retail_pos"),
        ("https://www.lightspeedhq.com", "lightspeed_retail", "retail_management"),
        ("https://www.shopkeep.com", "shopkeep", "small_business_pos"),
        
        # پزشکی
        ("https://www.practicefusion.com", "practice_fusion", "medical_practice"),
        ("https://www.athenahealth.com", "athena_health", "healthcare_management"),
        ("https://www.doximity.com", "doximity_medical", "medical_network"),
        
        # آموزش
        ("https://www.teachable.com", "teachable_education", "online_education"),
        ("https://www.udemy.com", "udemy_courses", "online_learning"),
        ("https://www.coursera.org", "coursera", "online_education"),
    ]
    
    print("🚀 شروع استخراج سایت‌های حرفه‌ای کسب‌وکار...")
    print(f"📊 تعداد سایت‌ها: {len(template_sites)}")
    
    success_count = 0
    total_sites = len(template_sites)
    
    for i, (url, name, category) in enumerate(template_sites, 1):
        print(f"\n[{i}/{total_sites}] 🎯 {name}")
        if extractor.extract_business_site(url, name, category):
            success_count += 1
        
        if i < total_sites:
            print("⏳ انتظار 3 ثانیه...")
            time.sleep(3)
    
    # گزارش نهایی
    print(f"\n🎉 استخراج کامل شد!")
    print(f"✅ موفق: {success_count}/{total_sites}")
    print(f"📁 فایل‌ها در: extraction_module/extracted_sites/extracted_sites/")
    
    # ذخیره گزارش
    report = {
        "extraction_type": "Professional Business Sites",
        "total_sites": total_sites,
        "successful": success_count,
        "failed": total_sites - success_count,
        "success_rate": f"{(success_count/total_sites)*100:.1f}%",
        "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categories": {
            "business_templates": 3,
            "accounting_software": 3,
            "business_management": 2,
            "ecommerce_platform": 3,
            "crm_system": 2,
            "location_services": 3,
            "restaurant_booking": 3,
            "beauty_booking": 3,
            "retail_management": 3,
            "medical_practice": 3,
            "online_education": 3
        }
    }
    
    with open("extraction_module/professional_business_extraction_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📊 گزارش ذخیره شد: professional_business_extraction_report.json")

if __name__ == "__main__":
    main()