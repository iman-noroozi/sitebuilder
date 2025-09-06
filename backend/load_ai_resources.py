#!/usr/bin/env python
"""
اسکریپت بارگذاری منابع هوش مصنوعی از template_extractor
"""
import os
import sys
import django
import json
from pathlib import Path

# تنظیم Django
sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from sitebuilder_app.models import AIResource

def load_ai_resources():
    """بارگذاری منابع هوش مصنوعی"""
    base_path = Path(__file__).resolve().parent.parent.parent.parent.parent
    
    # منابع مختلف هوش مصنوعی
    resources_data = [
        {
            'name': 'Hugging Face Models',
            'description': 'مدل‌های هوش مصنوعی از Hugging Face برای پردازش زبان طبیعی',
            'resource_type': 'model',
            'source_url': 'https://huggingface.co/models',
            'local_path': str(base_path / 'template_extractor' / 'extracted_data' / 'huggingface_models.json'),
            'is_offline_available': True,
            'tags': ['nlp', 'machine-learning', 'transformer', 'huggingface'],
            'metadata': {
                'provider': 'Hugging Face',
                'category': 'Natural Language Processing',
                'update_frequency': 'daily'
            }
        },
        {
            'name': 'OpenAI APIs',
            'description': 'API های OpenAI برای دسترسی به مدل‌های پیشرفته هوش مصنوعی',
            'resource_type': 'api',
            'source_url': 'https://platform.openai.com/docs',
            'local_path': str(base_path / 'template_extractor' / 'extracted_data' / 'openai_apis.json'),
            'is_offline_available': False,
            'tags': ['openai', 'gpt', 'api', 'ai'],
            'metadata': {
                'provider': 'OpenAI',
                'category': 'Language Models',
                'requires_api_key': True
            }
        },
        {
            'name': 'Google AI Services',
            'description': 'سرویس‌های هوش مصنوعی گوگل شامل Vision، Speech و Language',
            'resource_type': 'service',
            'source_url': 'https://ai.google.dev/',
            'local_path': str(base_path / 'template_extractor' / 'extracted_data' / 'google_ai_services.json'),
            'is_offline_available': False,
            'tags': ['google', 'vision', 'speech', 'language'],
            'metadata': {
                'provider': 'Google',
                'category': 'AI Services',
                'requires_api_key': True
            }
        },
        {
            'name': 'Kaggle Datasets',
            'description': 'مجموعه‌داده‌های متنوع برای آموزش مدل‌های هوش مصنوعی',
            'resource_type': 'dataset',
            'source_url': 'https://www.kaggle.com/datasets',
            'local_path': str(base_path / 'template_extractor' / 'extracted_data' / 'kaggle_datasets.json'),
            'is_offline_available': True,
            'tags': ['dataset', 'machine-learning', 'kaggle', 'training'],
            'metadata': {
                'provider': 'Kaggle',
                'category': 'Datasets',
                'license': 'various'
            }
        },
        {
            'name': 'AWS Open Data',
            'description': 'داده‌های باز آمازون برای تحقیقات و توسعه هوش مصنوعی',
            'resource_type': 'dataset',
            'source_url': 'https://registry.opendata.aws/',
            'local_path': str(base_path / 'template_extractor' / 'extracted_data' / 'aws_open_data.json'),
            'is_offline_available': True,
            'tags': ['aws', 'open-data', 'cloud', 'dataset'],
            'metadata': {
                'provider': 'Amazon Web Services',
                'category': 'Open Data',
                'cost': 'free'
            }
        },
        {
            'name': 'Wikipedia Dumps',
            'description': 'داده‌های ویکی‌پدیا برای آموزش مدل‌های زبانی',
            'resource_type': 'dataset',
            'source_url': 'https://dumps.wikimedia.org/',
            'local_path': str(base_path / 'template_extractor' / 'extracted_data' / 'wikipedia_dumps.json'),
            'is_offline_available': True,
            'tags': ['wikipedia', 'text', 'knowledge', 'nlp'],
            'metadata': {
                'provider': 'Wikimedia Foundation',
                'category': 'Text Data',
                'license': 'Creative Commons'
            }
        },
        {
            'name': 'Project Gutenberg Books',
            'description': 'کتاب‌های رایگان برای آموزش مدل‌های پردازش متن',
            'resource_type': 'dataset',
            'source_url': 'https://www.gutenberg.org/',
            'local_path': str(base_path / 'template_extractor' / 'extracted_data' / 'project_gutenberg.json'),
            'is_offline_available': True,
            'tags': ['books', 'literature', 'text', 'gutenberg'],
            'metadata': {
                'provider': 'Project Gutenberg',
                'category': 'Literature',
                'license': 'Public Domain'
            }
        },
        {
            'name': 'Business Services Catalog',
            'description': 'کاتالوگ کامل خدمات کسب و کار برای هوش مصنوعی',
            'resource_type': 'dataset',
            'source_url': '',
            'local_path': str(base_path / 'template_extractor' / 'business_data' / 'business_services_complete.json'),
            'is_offline_available': True,
            'tags': ['business', 'services', 'catalog', 'marketplace'],
            'metadata': {
                'provider': 'PeysunWeb',
                'category': 'Business Intelligence',
                'update_frequency': 'weekly'
            }
        },
        {
            'name': 'Developer Resources',
            'description': 'منابع توسعه‌دهندگان و ابزارهای برنامه‌نویسی',
            'resource_type': 'tool',
            'source_url': '',
            'local_path': str(base_path / 'template_extractor' / 'business_data' / 'developer_resources.json'),
            'is_offline_available': True,
            'tags': ['developer', 'tools', 'programming', 'resources'],
            'metadata': {
                'provider': 'PeysunWeb',
                'category': 'Development Tools',
                'update_frequency': 'monthly'
            }
        },
        {
            'name': 'Verification APIs Marketplace',
            'description': 'بازار API های تایید و احراز هویت',
            'resource_type': 'api',
            'source_url': '',
            'local_path': str(base_path / 'template_extractor' / 'business_data' / 'verification_apis_marketplace.json'),
            'is_offline_available': True,
            'tags': ['verification', 'api', 'authentication', 'security'],
            'metadata': {
                'provider': 'PeysunWeb',
                'category': 'Security & Verification',
                'update_frequency': 'weekly'
            }
        }
    ]
    
    for resource_data in resources_data:
        # بررسی وجود فایل محلی
        local_path = Path(resource_data['local_path'])
        if local_path.exists():
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    resource_data['file_size'] = local_path.stat().st_size
                    resource_data['metadata']['data_count'] = len(data) if isinstance(data, list) else 1
            except Exception as e:
                print(f"خطا در خواندن فایل {local_path}: {e}")
                resource_data['file_size'] = 0
        else:
            resource_data['file_size'] = 0
            print(f"فایل {local_path} وجود ندارد.")
        
        # ایجاد یا بروزرسانی منبع
        resource, created = AIResource.objects.get_or_create(
            name=resource_data['name'],
            defaults=resource_data
        )
        
        if created:
            print(f"منبع '{resource_data['name']}' ایجاد شد.")
        else:
            # بروزرسانی اطلاعات موجود
            for key, value in resource_data.items():
                if key != 'name':
                    setattr(resource, key, value)
            resource.save()
            print(f"منبع '{resource_data['name']}' بروزرسانی شد.")

def main():
    """تابع اصلی"""
    print("شروع بارگذاری منابع هوش مصنوعی...")
    
    load_ai_resources()
    
    print("بارگذاری منابع هوش مصنوعی تکمیل شد!")
    
    # نمایش آمار
    total_resources = AIResource.objects.count()
    offline_resources = AIResource.objects.filter(is_offline_available=True).count()
    print(f"\nآمار:")
    print(f"- تعداد کل منابع: {total_resources}")
    print(f"- منابع آفلاین: {offline_resources}")
    print(f"- منابع آنلاین: {total_resources - offline_resources}")

if __name__ == '__main__':
    main()
