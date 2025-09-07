"""
🌍 Site Builder REST API - Global Edition
Advanced RESTful API for website extraction and building
API پیشرفته برای استخراج و ساخت وب‌سایت
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import asyncio
import aiohttp
import time
from typing import Dict, List, Optional, Any
import logging
from concurrent.futures import ThreadPoolExecutor
import yaml
import requests
from urllib.parse import urlparse, urljoin
import hashlib
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class GlobalSiteBuilderAPI(APIView):
    """
    🌍 Global Site Builder API
    Advanced API endpoints for worldwide usage
    """
    
    permission_classes = [AllowAny]  # For demo, in production use proper auth
    
    def __init__(self):
        self.supported_languages = ['en', 'fa', 'ar', 'es', 'fr', 'de', 'zh', 'ja', 'ko', 'ru', 'pt', 'it']
        self.supported_frameworks = ['bootstrap', 'tailwind', 'bulma', 'foundation', 'materialize', 'semantic', 'chakra', 'antd']
        self.rate_limits = {}
        self.max_requests_per_minute = 60
    
    def check_rate_limit(self, client_ip: str) -> bool:
        """Check rate limiting for API requests"""
        current_time = time.time()
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = []
        
        # Remove old requests (older than 1 minute)
        self.rate_limits[client_ip] = [
            req_time for req_time in self.rate_limits[client_ip] 
            if current_time - req_time < 60
        ]
        
        if len(self.rate_limits[client_ip]) >= self.max_requests_per_minute:
            return False
        
        self.rate_limits[client_ip].append(current_time)
        return True
    
    def get_client_ip(self, request) -> str:
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def validate_url(self, url: str) -> bool:
        """Validate URL format and accessibility"""
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return False
            
            # Check if URL is accessible
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code < 400
        except:
            return False
    
    def detect_language(self, html_content: str) -> str:
        """Detect website language"""
        lang_indicators = {
            'fa': ['فارسی', 'persian', 'fa-ir', 'lang="fa"'],
            'ar': ['العربية', 'arabic', 'ar-sa', 'lang="ar"'],
            'en': ['english', 'en-us', 'lang="en"'],
            'es': ['español', 'spanish', 'es-es', 'lang="es"'],
            'fr': ['français', 'french', 'fr-fr', 'lang="fr"'],
            'de': ['deutsch', 'german', 'de-de', 'lang="de"'],
            'zh': ['中文', 'chinese', 'zh-cn', 'lang="zh"'],
            'ja': ['日本語', 'japanese', 'ja-jp', 'lang="ja"'],
            'ko': ['한국어', 'korean', 'ko-kr', 'lang="ko"'],
            'ru': ['русский', 'russian', 'ru-ru', 'lang="ru"'],
            'pt': ['português', 'portuguese', 'pt-br', 'lang="pt"'],
            'it': ['italiano', 'italian', 'it-it', 'lang="it"']
        }
        
        html_lower = html_content.lower()
        for lang, indicators in lang_indicators.items():
            if any(indicator in html_lower for indicator in indicators):
                return lang
        return 'en'  # Default to English
    
    def analyze_seo(self, html_content: str) -> Dict[str, Any]:
        """Analyze SEO elements"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        seo_data = {
            'title': soup.find('title').get_text() if soup.find('title') else '',
            'meta_description': '',
            'meta_keywords': '',
            'h1_count': len(soup.find_all('h1')),
            'h2_count': len(soup.find_all('h2')),
            'images_without_alt': 0,
            'internal_links': 0,
            'external_links': 0,
            'seo_score': 0
        }
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            seo_data['meta_description'] = meta_desc.get('content', '')
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            seo_data['meta_keywords'] = meta_keywords.get('content', '')
        
        # Images without alt
        images = soup.find_all('img')
        seo_data['images_without_alt'] = len([img for img in images if not img.get('alt')])
        
        # Links analysis
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href.startswith('http'):
                seo_data['external_links'] += 1
            else:
                seo_data['internal_links'] += 1
        
        # Calculate SEO score
        score = 0
        if seo_data['title']: score += 20
        if seo_data['meta_description']: score += 20
        if seo_data['h1_count'] == 1: score += 20
        if seo_data['h2_count'] > 0: score += 10
        if seo_data['images_without_alt'] == 0: score += 15
        if seo_data['internal_links'] > 0: score += 15
        
        seo_data['seo_score'] = min(score, 100)
        return seo_data
    
    def extract_assets(self, html_content: str, base_url: str) -> Dict[str, List[str]]:
        """Extract and categorize assets"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        assets = {
            'css': [],
            'js': [],
            'images': [],
            'fonts': [],
            'videos': [],
            'other': []
        }
        
        # CSS files
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                assets['css'].append(urljoin(base_url, href))
        
        # JavaScript files
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                assets['js'].append(urljoin(base_url, src))
        
        # Images
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                assets['images'].append(urljoin(base_url, src))
        
        # Fonts
        for link in soup.find_all('link', rel='preload'):
            href = link.get('href')
            if href and any(ext in href.lower() for ext in ['.woff', '.woff2', '.ttf', '.otf']):
                assets['fonts'].append(urljoin(base_url, href))
        
        # Videos
        for video in soup.find_all('video', src=True):
            src = video.get('src')
            if src:
                assets['videos'].append(urljoin(base_url, src))
        
        return assets

@api_view(['POST'])
@permission_classes([AllowAny])
def extract_website(request):
    """
    🌍 Extract website template with advanced analysis
    استخراج قالب وب‌سایت با تحلیل پیشرفته
    """
    api = GlobalSiteBuilderAPI()
    client_ip = api.get_client_ip(request)
    
    # Rate limiting
    if not api.check_rate_limit(client_ip):
        return Response({
            'error': 'Rate limit exceeded. Please try again later.',
            'code': 'RATE_LIMIT_EXCEEDED'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    try:
        data = json.loads(request.body)
        url = data.get('url')
        
        if not url:
            return Response({
                'error': 'URL is required',
                'code': 'MISSING_URL'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate URL
        if not api.validate_url(url):
            return Response({
                'error': 'Invalid or inaccessible URL',
                'code': 'INVALID_URL'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract website content
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'SiteBuilder/1.0 (Global Edition)'
        })
        
        if response.status_code != 200:
            return Response({
                'error': f'Failed to fetch website. Status: {response.status_code}',
                'code': 'FETCH_FAILED'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        html_content = response.text
        
        # Advanced analysis
        analysis = {
            'url': url,
            'timestamp': time.time(),
            'language': api.detect_language(html_content),
            'seo': api.analyze_seo(html_content),
            'assets': api.extract_assets(html_content, url),
            'performance': {
                'content_size': len(html_content),
                'load_time': response.elapsed.total_seconds(),
                'status_code': response.status_code
            },
            'metadata': {
                'title': '',
                'description': '',
                'keywords': '',
                'viewport': '',
                'robots': ''
            }
        }
        
        # Extract metadata
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title_tag = soup.find('title')
        if title_tag:
            analysis['metadata']['title'] = title_tag.get_text()
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            analysis['metadata']['description'] = meta_desc.get('content', '')
        
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            analysis['metadata']['keywords'] = meta_keywords.get('content', '')
        
        meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
        if meta_viewport:
            analysis['metadata']['viewport'] = meta_viewport.get('content', '')
        
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        if meta_robots:
            analysis['metadata']['robots'] = meta_robots.get('content', '')
        
        return Response({
            'success': True,
            'data': analysis,
            'message': 'Website extracted successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        return Response({
            'error': 'Internal server error during extraction',
            'code': 'EXTRACTION_ERROR',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_supported_languages(request):
    """Get list of supported languages"""
    api = GlobalSiteBuilderAPI()
    return Response({
        'languages': api.supported_languages,
        'count': len(api.supported_languages)
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_supported_frameworks(request):
    """Get list of supported frameworks"""
    api = GlobalSiteBuilderAPI()
    return Response({
        'frameworks': api.supported_frameworks,
        'count': len(api.supported_frameworks)
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_performance(request):
    """
    🚀 Analyze website performance
    تحلیل عملکرد وب‌سایت
    """
    api = GlobalSiteBuilderAPI()
    client_ip = api.get_client_ip(request)
    
    if not api.check_rate_limit(client_ip):
        return Response({
            'error': 'Rate limit exceeded',
            'code': 'RATE_LIMIT_EXCEEDED'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    try:
        data = json.loads(request.body)
        url = data.get('url')
        
        if not url or not api.validate_url(url):
            return Response({
                'error': 'Invalid URL',
                'code': 'INVALID_URL'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Performance analysis
        start_time = time.time()
        response = requests.get(url, timeout=30)
        load_time = time.time() - start_time
        
        performance_data = {
            'url': url,
            'load_time': round(load_time, 2),
            'status_code': response.status_code,
            'content_size': len(response.content),
            'headers': dict(response.headers),
            'performance_score': api.calculate_performance_score(load_time, len(response.content)),
            'recommendations': []
        }
        
        # Generate recommendations
        if load_time > 3:
            performance_data['recommendations'].append('Consider optimizing images and reducing file sizes')
        if len(response.content) > 1000000:  # 1MB
            performance_data['recommendations'].append('Content size is large, consider compression')
        if response.status_code != 200:
            performance_data['recommendations'].append('Fix HTTP status code issues')
        
        return Response({
            'success': True,
            'data': performance_data
        })
        
    except Exception as e:
        logger.error(f"Performance analysis error: {str(e)}")
        return Response({
            'error': 'Performance analysis failed',
            'code': 'ANALYSIS_ERROR'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': time.time(),
        'services': {
            'api': 'operational',
            'extraction': 'operational',
            'analysis': 'operational'
        }
    })
