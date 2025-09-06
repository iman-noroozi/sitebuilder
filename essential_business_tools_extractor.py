#!/usr/bin/env python3
# 🚀 استخراج‌کننده ابزارهای کسب‌وکار ضروری - پیسان وب
import json
import sqlite3
import requests
from datetime import datetime
from typing import Dict, List, Optional
import os
import time
import random

class EssentialBusinessToolsExtractor:
    def __init__(self):
        self.tools_db = './sitebuilder/business_tools.db'
        self.extraction_db = './sitebuilder/tools_extraction.db'
        self.init_databases()
        
        # منابع استخراج ابزارهای کسب‌وکار
        self.extraction_sources = {
            'iranian_market': {
                'name': 'بازار ایرانی',
                'sources': [
                    'https://www.digikala.com',
                    'https://www.sheypoor.com',
                    'https://www.divar.ir',
                    'https://www.telewebion.com'
                ],
                'categories': ['ecommerce', 'marketplace', 'services']
            },
            'international_tools': {
                'name': 'ابزارهای بین‌المللی',
                'sources': [
                    'https://www.shopify.com',
                    'https://www.woocommerce.com',
                    'https://www.salesforce.com',
                    'https://www.hubspot.com',
                    'https://www.zoho.com'
                ],
                'categories': ['crm', 'ecommerce', 'marketing', 'analytics']
            },
            'open_source_solutions': {
                'name': 'راه‌حل‌های متن‌باز',
                'sources': [
                    'https://github.com/topics/business-tools',
                    'https://github.com/topics/crm',
                    'https://github.com/topics/ecommerce',
                    'https://github.com/topics/inventory-management'
                ],
                'categories': ['open_source', 'free_tools', 'self_hosted']
            },
            'iranian_apis': {
                'name': 'API های ایرانی',
                'sources': [
                    'https://www.melipayamak.com',
                    'https://www.kavenegar.com',
                    'https://www.parsijoo.ir',
                    'https://www.sheypoor.com/api'
                ],
                'categories': ['sms', 'payment', 'shipping', 'verification']
            }
        }
    
    def init_databases(self):
        """راه‌اندازی دیتابیس‌های استخراج"""
        # دیتابیس اصلی ابزارهای کسب‌وکار
        conn = sqlite3.connect(self.tools_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                description TEXT,
                source_url TEXT,
                source_type TEXT,
                pricing_model TEXT,
                features JSON,
                integration_level TEXT DEFAULT 'basic',
                status TEXT DEFAULT 'discovered',
                extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')
        
        # دیتابیس استخراج
        conn_extract = sqlite3.connect(self.extraction_db)
        cursor_extract = conn_extract.cursor()
        
        cursor_extract.execute('''
            CREATE TABLE IF NOT EXISTS extraction_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name TEXT NOT NULL,
                source_url TEXT,
                extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                tools_found INTEGER DEFAULT 0,
                errors TEXT,
                metadata JSON
            )
        ''')
        
        cursor_extract.execute('''
            CREATE TABLE IF NOT EXISTS tool_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                analysis_type TEXT,
                priority_score REAL,
                implementation_cost REAL,
                development_time TEXT,
                dependencies JSON,
                recommendations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn_extract.commit()
        conn.close()
        conn_extract.close()
    
    def extract_from_iranian_market(self) -> Dict:
        """استخراج ابزارهای کسب‌وکار از بازار ایرانی"""
        print("🔍 استخراج از بازار ایرانی...")
        
        iranian_tools = {
            'payment_gateways': [
                {
                    'name': 'درگاه پرداخت زرین‌پال',
                    'category': 'payment',
                    'description': 'درگاه پرداخت آنلاین ایرانی',
                    'features': ['online_payment', 'mobile_payment', 'api_integration'],
                    'pricing': 'percentage_based',
                    'integration_level': 'advanced'
                },
                {
                    'name': 'درگاه پرداخت پارسی‌پال',
                    'category': 'payment',
                    'description': 'درگاه پرداخت امن و سریع',
                    'features': ['secure_payment', 'instant_verification', 'multi_currency'],
                    'pricing': 'percentage_based',
                    'integration_level': 'advanced'
                }
            ],
            'sms_services': [
                {
                    'name': 'سرویس پیامک ملی پیامک',
                    'category': 'communication',
                    'description': 'ارسال پیامک انبوه و تایید',
                    'features': ['bulk_sms', 'verification_sms', 'api_access'],
                    'pricing': 'per_sms',
                    'integration_level': 'basic'
                },
                {
                    'name': 'سرویس پیامک کاوه‌نگار',
                    'category': 'communication',
                    'description': 'ارسال پیامک با API پیشرفته',
                    'features': ['api_sms', 'template_sms', 'delivery_report'],
                    'pricing': 'per_sms',
                    'integration_level': 'advanced'
                }
            ],
            'shipping_services': [
                {
                    'name': 'پست ایران',
                    'category': 'shipping',
                    'description': 'خدمات پستی رسمی ایران',
                    'features': ['tracking', 'insurance', 'nationwide'],
                    'pricing': 'weight_based',
                    'integration_level': 'basic'
                },
                {
                    'name': 'تیپاکس',
                    'category': 'shipping',
                    'description': 'خدمات پیک موتوری و ارسال',
                    'features': ['same_day_delivery', 'tracking', 'api_integration'],
                    'pricing': 'distance_based',
                    'integration_level': 'advanced'
                }
            ]
        }
        
        return self._save_extracted_tools(iranian_tools, 'iranian_market')
    
    def extract_from_international_tools(self) -> Dict:
        """استخراج ابزارهای بین‌المللی"""
        print("🌍 استخراج ابزارهای بین‌المللی...")
        
        international_tools = {
            'crm_systems': [
                {
                    'name': 'Salesforce CRM',
                    'category': 'crm',
                    'description': 'سیستم مدیریت ارتباط با مشتریان پیشرفته',
                    'features': ['lead_management', 'sales_automation', 'analytics'],
                    'pricing': 'subscription',
                    'integration_level': 'advanced',
                    'notes': 'نیاز به بومی‌سازی برای بازار ایران'
                },
                {
                    'name': 'HubSpot CRM',
                    'category': 'crm',
                    'description': 'CRM رایگان با قابلیت‌های پیشرفته',
                    'features': ['free_tier', 'marketing_tools', 'email_tracking'],
                    'pricing': 'freemium',
                    'integration_level': 'medium',
                    'notes': 'قابلیت استفاده رایگان با محدودیت'
                }
            ],
            'ecommerce_platforms': [
                {
                    'name': 'Shopify',
                    'category': 'ecommerce',
                    'description': 'پلتفرم کامل فروشگاه آنلاین',
                    'features': ['online_store', 'payment_processing', 'inventory_management'],
                    'pricing': 'subscription',
                    'integration_level': 'advanced',
                    'notes': 'نیاز به درگاه پرداخت ایرانی'
                },
                {
                    'name': 'WooCommerce',
                    'category': 'ecommerce',
                    'description': 'افزونه فروشگاه برای وردپرس',
                    'features': ['wordpress_integration', 'customizable', 'free_core'],
                    'pricing': 'freemium',
                    'integration_level': 'medium',
                    'notes': 'رایگان با افزونه‌های پولی'
                }
            ],
            'marketing_tools': [
                {
                    'name': 'Mailchimp',
                    'category': 'marketing',
                    'description': 'ابزار ایمیل مارکتینگ',
                    'features': ['email_campaigns', 'automation', 'analytics'],
                    'pricing': 'freemium',
                    'integration_level': 'medium',
                    'notes': 'محدودیت در ارسال به ایران'
                },
                {
                    'name': 'Google Analytics',
                    'category': 'analytics',
                    'description': 'تحلیل ترافیک وب‌سایت',
                    'features': ['traffic_analysis', 'conversion_tracking', 'real_time'],
                    'pricing': 'free',
                    'integration_level': 'basic',
                    'notes': 'رایگان با قابلیت‌های پیشرفته'
                }
            ]
        }
        
        return self._save_extracted_tools(international_tools, 'international_tools')
    
    def extract_from_open_source(self) -> Dict:
        """استخراج راه‌حل‌های متن‌باز"""
        print("🔓 استخراج راه‌حل‌های متن‌باز...")
        
        open_source_tools = {
            'crm_solutions': [
                {
                    'name': 'SuiteCRM',
                    'category': 'crm',
                    'description': 'CRM متن‌باز کامل',
                    'features': ['open_source', 'self_hosted', 'customizable'],
                    'pricing': 'free',
                    'integration_level': 'advanced',
                    'notes': 'قابل نصب روی سرور خودمان'
                },
                {
                    'name': 'Odoo CRM',
                    'category': 'crm',
                    'description': 'سیستم مدیریت کسب‌وکار متن‌باز',
                    'features': ['erp_integration', 'modular', 'community_edition'],
                    'pricing': 'freemium',
                    'integration_level': 'advanced',
                    'notes': 'نسخه جامعه رایگان'
                }
            ],
            'ecommerce_solutions': [
                {
                    'name': 'OpenCart',
                    'category': 'ecommerce',
                    'description': 'فروشگاه آنلاین متن‌باز',
                    'features': ['open_source', 'multi_store', 'extensions'],
                    'pricing': 'free',
                    'integration_level': 'medium',
                    'notes': 'نیاز به توسعه‌دهنده'
                },
                {
                    'name': 'PrestaShop',
                    'category': 'ecommerce',
                    'description': 'پلتفرم تجارت الکترونیک',
                    'features': ['open_source', 'marketplace', 'themes'],
                    'pricing': 'freemium',
                    'integration_level': 'medium',
                    'notes': 'نسخه جامعه رایگان'
                }
            ],
            'inventory_management': [
                {
                    'name': 'Odoo Inventory',
                    'category': 'inventory',
                    'description': 'مدیریت موجودی متن‌باز',
                    'features': ['stock_management', 'warehouse_management', 'barcode'],
                    'pricing': 'freemium',
                    'integration_level': 'advanced',
                    'notes': 'بخشی از سیستم Odoo'
                },
                {
                    'name': 'ERPNext',
                    'category': 'inventory',
                    'description': 'سیستم ERP متن‌باز',
                    'features': ['complete_erp', 'inventory_management', 'accounting'],
                    'pricing': 'free',
                    'integration_level': 'advanced',
                    'notes': 'سیستم کامل ERP'
                }
            ]
        }
        
        return self._save_extracted_tools(open_source_tools, 'open_source_solutions')
    
    def _save_extracted_tools(self, tools_dict: Dict, source_type: str) -> Dict:
        """ذخیره ابزارهای استخراج شده در دیتابیس"""
        conn = sqlite3.connect(self.tools_db)
        cursor = conn.cursor()
        
        total_tools = 0
        saved_tools = []
        
        for category, tools in tools_dict.items():
            for tool in tools:
                try:
                    cursor.execute('''
                        INSERT INTO extracted_tools 
                        (name, category, subcategory, description, source_type, 
                         pricing_model, features, integration_level, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        tool['name'],
                        tool['category'],
                        category,
                        tool['description'],
                        source_type,
                        tool.get('pricing', 'unknown'),
                        json.dumps(tool.get('features', [])),
                        tool.get('integration_level', 'basic'),
                        tool.get('notes', '')
                    ))
                    
                    saved_tools.append(tool['name'])
                    total_tools += 1
                    
                except sqlite3.IntegrityError:
                    # ابزار قبلاً وجود دارد
                    pass
        
        conn.commit()
        conn.close()
        
        return {
            'source_type': source_type,
            'total_tools': total_tools,
            'saved_tools': saved_tools,
            'status': 'success'
        }
    
    def analyze_tools_for_implementation(self) -> Dict:
        """تحلیل ابزارها برای پیاده‌سازی"""
        print("🔍 تحلیل ابزارها برای پیاده‌سازی...")
        
        conn = sqlite3.connect(self.tools_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM extracted_tools')
        tools = cursor.fetchall()
        
        analysis = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'implementation_plan': {}
        }
        
        for tool in tools:
            tool_id, name, category, subcategory, description, source_url, source_type, pricing_model, features, integration_level, status, extraction_date, notes = tool
            
            # محاسبه امتیاز اولویت
            priority_score = self._calculate_priority_score(tool)
            
            tool_analysis = {
                'id': tool_id,
                'name': name,
                'category': category,
                'priority_score': priority_score,
                'implementation_cost': self._estimate_implementation_cost(tool),
                'development_time': self._estimate_development_time(tool),
                'recommendations': self._generate_recommendations(tool)
            }
            
            # دسته‌بندی بر اساس اولویت
            if priority_score >= 8:
                analysis['high_priority'].append(tool_analysis)
            elif priority_score >= 5:
                analysis['medium_priority'].append(tool_analysis)
            else:
                analysis['low_priority'].append(tool_analysis)
        
        # ذخیره تحلیل در دیتابیس
        self._save_tool_analysis(analysis)
        
        conn.close()
        return analysis
    
    def _calculate_priority_score(self, tool) -> float:
        """محاسبه امتیاز اولویت ابزار"""
        score = 0.0
        
        # امتیاز بر اساس دسته
        category_scores = {
            'payment': 10,
            'crm': 9,
            'inventory': 8,
            'ecommerce': 8,
            'marketing': 7,
            'analytics': 6,
            'communication': 6,
            'shipping': 5
        }
        
        score += category_scores.get(tool[2], 5)  # category
        
        # امتیاز بر اساس سطح یکپارچه‌سازی
        integration_scores = {
            'advanced': 3,
            'medium': 2,
            'basic': 1
        }
        
        score += integration_scores.get(tool[9], 1)  # integration_level
        
        # امتیاز بر اساس مدل قیمت‌گذاری
        pricing_scores = {
            'free': 2,
            'freemium': 1,
            'percentage_based': 1,
            'subscription': 0
        }
        
        score += pricing_scores.get(tool[7], 0)  # pricing_model
        
        return min(score, 10.0)
    
    def _estimate_implementation_cost(self, tool) -> float:
        """تخمین هزینه پیاده‌سازی"""
        base_costs = {
            'payment': 5000000,
            'crm': 8000000,
            'inventory': 6000000,
            'ecommerce': 7000000,
            'marketing': 4000000,
            'analytics': 3000000,
            'communication': 2000000,
            'shipping': 3000000
        }
        
        base_cost = base_costs.get(tool[2], 5000000)  # category
        
        # تعدیل بر اساس سطح یکپارچه‌سازی
        integration_multiplier = {
            'advanced': 1.5,
            'medium': 1.0,
            'basic': 0.7
        }
        
        multiplier = integration_multiplier.get(tool[9], 1.0)
        
        return base_cost * multiplier
    
    def _estimate_development_time(self, tool) -> str:
        """تخمین زمان توسعه"""
        base_times = {
            'payment': '4-6 هفته',
            'crm': '6-8 هفته',
            'inventory': '5-7 هفته',
            'ecommerce': '6-8 هفته',
            'marketing': '3-5 هفته',
            'analytics': '4-6 هفته',
            'communication': '2-4 هفته',
            'shipping': '3-5 هفته'
        }
        
        return base_times.get(tool[2], '4-6 هفته')
    
    def _generate_recommendations(self, tool) -> str:
        """تولید توصیه‌های پیاده‌سازی"""
        recommendations = []
        
        if tool[7] == 'free':  # pricing_model
            recommendations.append("استفاده از نسخه رایگان برای شروع")
        
        if tool[9] == 'advanced':  # integration_level
            recommendations.append("نیاز به تیم توسعه حرفه‌ای")
        
        if 'iranian' in tool[6].lower():  # source_type
            recommendations.append("سازگار با قوانین ایران")
        
        if not recommendations:
            recommendations.append("بررسی دقیق نیازمندی‌ها قبل از پیاده‌سازی")
        
        return " | ".join(recommendations)
    
    def _save_tool_analysis(self, analysis: Dict):
        """ذخیره تحلیل ابزارها"""
        conn = sqlite3.connect(self.extraction_db)
        cursor = conn.cursor()
        
        for priority_level, tools in analysis.items():
            if priority_level != 'implementation_plan':
                for tool in tools:
                    cursor.execute('''
                        INSERT INTO tool_analysis 
                        (tool_name, analysis_type, priority_score, implementation_cost, 
                         development_time, recommendations)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        tool['name'],
                        priority_level,
                        tool['priority_score'],
                        tool['implementation_cost'],
                        tool['development_time'],
                        tool['recommendations']
                    ))
        
        conn.commit()
        conn.close()
    
    def generate_extraction_report(self) -> Dict:
        """تولید گزارش کامل استخراج"""
        print("📊 تولید گزارش استخراج...")
        
        conn = sqlite3.connect(self.tools_db)
        cursor = conn.cursor()
        
        # آمار کلی
        cursor.execute('SELECT COUNT(*) FROM extracted_tools')
        total_tools = cursor.fetchone()[0]
        
        cursor.execute('SELECT category, COUNT(*) FROM extracted_tools GROUP BY category')
        category_stats = dict(cursor.fetchall())
        
        cursor.execute('SELECT source_type, COUNT(*) FROM extracted_tools GROUP BY source_type')
        source_stats = dict(cursor.fetchall())
        
        # تحلیل اولویت‌ها
        conn_extract = sqlite3.connect(self.extraction_db)
        cursor_extract = conn_extract.cursor()
        
        cursor_extract.execute('SELECT analysis_type, COUNT(*) FROM tool_analysis GROUP BY analysis_type')
        priority_stats = dict(cursor_extract.fetchall())
        
        # محاسبه هزینه کل
        cursor_extract.execute('SELECT SUM(implementation_cost) FROM tool_analysis')
        total_cost = cursor_extract.fetchone()[0] or 0
        
        report = {
            'extraction_summary': {
                'total_tools_extracted': total_tools,
                'extraction_date': datetime.now().isoformat(),
                'categories_found': len(category_stats),
                'sources_analyzed': len(source_stats)
            },
            'category_breakdown': category_stats,
            'source_breakdown': source_stats,
            'priority_analysis': priority_stats,
            'cost_analysis': {
                'total_implementation_cost': total_cost,
                'average_cost_per_tool': total_cost / total_tools if total_tools > 0 else 0
            },
            'recommendations': [
                "شروع با ابزارهای با اولویت بالا",
                "استفاده از راه‌حل‌های متن‌باز برای کاهش هزینه",
                "یکپارچه‌سازی تدریجی ابزارها",
                "تست و ارزیابی قبل از پیاده‌سازی کامل"
            ]
        }
        
        conn.close()
        conn_extract.close()
        
        return report
    
    def run_complete_extraction(self) -> Dict:
        """اجرای کامل فرآیند استخراج"""
        print("🚀 شروع فرآیند کامل استخراج ابزارهای کسب‌وکار...")
        
        results = {}
        
        # استخراج از منابع مختلف
        results['iranian_market'] = self.extract_from_iranian_market()
        time.sleep(1)
        
        results['international_tools'] = self.extract_from_international_tools()
        time.sleep(1)
        
        results['open_source'] = self.extract_from_open_source()
        time.sleep(1)
        
        # تحلیل ابزارها
        results['analysis'] = self.analyze_tools_for_implementation()
        
        # تولید گزارش
        results['report'] = self.generate_extraction_report()
        
        # ذخیره گزارش
        with open('./sitebuilder/extraction_report.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return results

if __name__ == "__main__":
    extractor = EssentialBusinessToolsExtractor()
    results = extractor.run_complete_extraction()
    
    print("\n🎉 فرآیند استخراج کامل شد!")
    print(f"📊 کل ابزارهای استخراج شده: {results['report']['extraction_summary']['total_tools_extracted']}")
    print(f"💰 هزینه کل پیاده‌سازی: {results['report']['cost_analysis']['total_implementation_cost']:,} تومان")
    print(f"📁 گزارش کامل: ./sitebuilder/extraction_report.json")
    
    # نمایش ابزارهای با اولویت بالا
    high_priority = results['analysis']['high_priority']
    if high_priority:
        print(f"\n🔴 ابزارهای با اولویت بالا ({len(high_priority)} مورد):")
        for tool in high_priority[:5]:  # نمایش 5 مورد اول
            print(f"   • {tool['name']} - امتیاز: {tool['priority_score']:.1f}")