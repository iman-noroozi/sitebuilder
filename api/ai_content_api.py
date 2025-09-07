#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Content API - RESTful API for AI Content Generation
Provides endpoints for intelligent content creation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from typing import Dict, List
import logging

# Import our AI Content Generator
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_content_generator import AIContentGenerator, ContentRequest, GeneratedContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize AI Content Generator
ai_generator = AIContentGenerator(
    openai_api_key=os.getenv('OPENAI_API_KEY')
)

@app.route('/api/ai-content/generate', methods=['POST'])
def generate_content():
    """Generate AI content based on request parameters"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['business_type', 'language']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400
        
        # Create content request
        content_request = ContentRequest(
            business_type=data['business_type'],
            language=data.get('language', 'fa'),
            content_type=data.get('content_type', 'homepage'),
            tone=data.get('tone', 'professional'),
            length=data.get('length', 'medium'),
            keywords=data.get('keywords', []),
            target_audience=data.get('target_audience', 'general'),
            industry=data.get('industry', 'general')
        )
        
        # Generate content
        generated_content = ai_generator.generate_content(content_request)
        
        # Convert to JSON-serializable format
        response_data = {
            'title': generated_content.title,
            'content': generated_content.content,
            'meta_description': generated_content.meta_description,
            'keywords': generated_content.keywords,
            'seo_score': generated_content.seo_score,
            'readability_score': generated_content.readability_score,
            'language': generated_content.language,
            'word_count': generated_content.word_count,
            'created_at': generated_content.created_at.isoformat(),
            'status': 'success'
        }
        
        logger.info(f"Generated content for {data['business_type']} in {data['language']}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/ai-content/translate', methods=['POST'])
def translate_content():
    """Translate existing content to another language"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content', 'target_language']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400
        
        # Create GeneratedContent object from input
        original_content = GeneratedContent(
            title=data['content'].get('title', ''),
            content=data['content'].get('content', ''),
            meta_description=data['content'].get('meta_description', ''),
            keywords=data['content'].get('keywords', []),
            seo_score=data['content'].get('seo_score', 0),
            readability_score=data['content'].get('readability_score', 0),
            language=data['content'].get('language', 'en'),
            word_count=data['content'].get('word_count', 0),
            created_at=datetime.now()
        )
        
        # Translate content
        translated_content = ai_generator.translate_content(
            original_content, 
            data['target_language']
        )
        
        # Convert to JSON-serializable format
        response_data = {
            'title': translated_content.title,
            'content': translated_content.content,
            'meta_description': translated_content.meta_description,
            'keywords': translated_content.keywords,
            'seo_score': translated_content.seo_score,
            'readability_score': translated_content.readability_score,
            'language': translated_content.language,
            'word_count': translated_content.word_count,
            'created_at': translated_content.created_at.isoformat(),
            'status': 'success'
        }
        
        logger.info(f"Translated content to {data['target_language']}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error translating content: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/ai-content/suggestions', methods=['GET'])
def get_content_suggestions():
    """Get content suggestions for a business type"""
    try:
        business_type = request.args.get('business_type', 'general')
        language = request.args.get('language', 'fa')
        
        suggestions = ai_generator.get_content_suggestions(business_type, language)
        
        return jsonify({
            'suggestions': suggestions,
            'business_type': business_type,
            'language': language,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/ai-content/batch-generate', methods=['POST'])
def batch_generate_content():
    """Generate multiple content pieces in batch"""
    try:
        data = request.get_json()
        
        if 'requests' not in data:
            return jsonify({
                'error': 'Missing required field: requests',
                'status': 'error'
            }), 400
        
        results = []
        
        for req_data in data['requests']:
            try:
                # Create content request
                content_request = ContentRequest(
                    business_type=req_data['business_type'],
                    language=req_data.get('language', 'fa'),
                    content_type=req_data.get('content_type', 'homepage'),
                    tone=req_data.get('tone', 'professional'),
                    length=req_data.get('length', 'medium'),
                    keywords=req_data.get('keywords', []),
                    target_audience=req_data.get('target_audience', 'general'),
                    industry=req_data.get('industry', 'general')
                )
                
                # Generate content
                generated_content = ai_generator.generate_content(content_request)
                
                # Add to results
                results.append({
                    'title': generated_content.title,
                    'content': generated_content.content,
                    'meta_description': generated_content.meta_description,
                    'keywords': generated_content.keywords,
                    'seo_score': generated_content.seo_score,
                    'readability_score': generated_content.readability_score,
                    'language': generated_content.language,
                    'word_count': generated_content.word_count,
                    'created_at': generated_content.created_at.isoformat(),
                    'request_id': req_data.get('id', ''),
                    'status': 'success'
                })
                
            except Exception as e:
                results.append({
                    'error': str(e),
                    'request_id': req_data.get('id', ''),
                    'status': 'error'
                })
        
        return jsonify({
            'results': results,
            'total_requests': len(data['requests']),
            'successful': len([r for r in results if r.get('status') == 'success']),
            'failed': len([r for r in results if r.get('status') == 'error']),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error in batch generation: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/ai-content/analyze', methods=['POST'])
def analyze_content():
    """Analyze existing content for SEO and readability"""
    try:
        data = request.get_json()
        
        if 'content' not in data:
            return jsonify({
                'error': 'Missing required field: content',
                'status': 'error'
            }), 400
        
        content_text = data['content']
        language = data.get('language', 'fa')
        keywords = data.get('keywords', [])
        
        # Create a mock request for analysis
        mock_request = ContentRequest(
            business_type=data.get('business_type', 'general'),
            language=language,
            keywords=keywords
        )
        
        # Create mock content for analysis
        mock_content = {
            'title': data.get('title', ''),
            'content': content_text,
            'meta_description': data.get('meta_description', ''),
            'keywords': keywords
        }
        
        # Calculate scores
        seo_score = ai_generator._calculate_seo_score(mock_content, mock_request)
        readability_score = ai_generator._calculate_readability_score(mock_content)
        
        # Extract keywords
        extracted_keywords = ai_generator._extract_keywords(content_text, mock_request)
        
        return jsonify({
            'seo_score': seo_score,
            'readability_score': readability_score,
            'word_count': len(content_text.split()),
            'extracted_keywords': extracted_keywords,
            'suggestions': {
                'seo_improvements': _get_seo_suggestions(seo_score),
                'readability_improvements': _get_readability_suggestions(readability_score)
            },
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error analyzing content: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

def _get_seo_suggestions(score: int) -> List[str]:
    """Get SEO improvement suggestions based on score"""
    suggestions = []
    
    if score < 60:
        suggestions.extend([
            "Add more relevant keywords to your content",
            "Optimize your title length (50-60 characters)",
            "Improve your meta description (150-160 characters)",
            "Add more content (300-800 words recommended)"
        ])
    elif score < 80:
        suggestions.extend([
            "Fine-tune your keyword density",
            "Add internal links to related content",
            "Include alt text for images"
        ])
    else:
        suggestions.append("Great SEO optimization! Keep up the good work.")
    
    return suggestions

def _get_readability_suggestions(score: int) -> List[str]:
    """Get readability improvement suggestions based on score"""
    suggestions = []
    
    if score < 60:
        suggestions.extend([
            "Use shorter sentences (15 words or less)",
            "Break up long paragraphs",
            "Use simpler words and phrases",
            "Add bullet points and subheadings"
        ])
    elif score < 80:
        suggestions.extend([
            "Consider using more active voice",
            "Add transitional phrases between paragraphs"
        ])
    else:
        suggestions.append("Excellent readability! Your content is easy to read.")
    
    return suggestions

@app.route('/api/ai-content/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Content Generator',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/ai-content/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    languages = [
        {'code': 'fa', 'name': 'Persian', 'native_name': 'فارسی'},
        {'code': 'en', 'name': 'English', 'native_name': 'English'},
        {'code': 'ar', 'name': 'Arabic', 'native_name': 'العربية'},
        {'code': 'fr', 'name': 'French', 'native_name': 'Français'},
        {'code': 'de', 'name': 'German', 'native_name': 'Deutsch'},
        {'code': 'es', 'name': 'Spanish', 'native_name': 'Español'},
        {'code': 'it', 'name': 'Italian', 'native_name': 'Italiano'},
        {'code': 'pt', 'name': 'Portuguese', 'native_name': 'Português'},
        {'code': 'ru', 'name': 'Russian', 'native_name': 'Русский'},
        {'code': 'zh', 'name': 'Chinese', 'native_name': '中文'},
        {'code': 'ja', 'name': 'Japanese', 'native_name': '日本語'},
        {'code': 'ko', 'name': 'Korean', 'native_name': '한국어'}
    ]
    
    return jsonify({
        'languages': languages,
        'total': len(languages),
        'status': 'success'
    })

@app.route('/api/ai-content/business-types', methods=['GET'])
def get_business_types():
    """Get list of supported business types"""
    business_types = [
        {'id': 'restaurant', 'name': 'Restaurant', 'name_fa': 'رستوران'},
        {'id': 'ecommerce', 'name': 'E-commerce', 'name_fa': 'فروشگاه آنلاین'},
        {'id': 'consulting', 'name': 'Consulting', 'name_fa': 'مشاوره'},
        {'id': 'healthcare', 'name': 'Healthcare', 'name_fa': 'بهداشت و درمان'},
        {'id': 'education', 'name': 'Education', 'name_fa': 'آموزش'},
        {'id': 'technology', 'name': 'Technology', 'name_fa': 'فناوری'},
        {'id': 'finance', 'name': 'Finance', 'name_fa': 'مالی'},
        {'id': 'real_estate', 'name': 'Real Estate', 'name_fa': 'املاک'},
        {'id': 'legal', 'name': 'Legal Services', 'name_fa': 'خدمات حقوقی'},
        {'id': 'marketing', 'name': 'Marketing', 'name_fa': 'بازاریابی'},
        {'id': 'travel', 'name': 'Travel & Tourism', 'name_fa': 'سفر و گردشگری'},
        {'id': 'fitness', 'name': 'Fitness & Wellness', 'name_fa': 'تناسب اندام'},
        {'id': 'beauty', 'name': 'Beauty & Spa', 'name_fa': 'زیبایی و اسپا'},
        {'id': 'automotive', 'name': 'Automotive', 'name_fa': 'خودرو'},
        {'id': 'home_services', 'name': 'Home Services', 'name_fa': 'خدمات منزل'}
    ]
    
    return jsonify({
        'business_types': business_types,
        'total': len(business_types),
        'status': 'success'
    })

if __name__ == '__main__':
    # Run the API server
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting AI Content API on port {port}")
    print(f"📝 Available endpoints:")
    print(f"   POST /api/ai-content/generate - Generate AI content")
    print(f"   POST /api/ai-content/translate - Translate content")
    print(f"   GET  /api/ai-content/suggestions - Get content suggestions")
    print(f"   POST /api/ai-content/batch-generate - Batch content generation")
    print(f"   POST /api/ai-content/analyze - Analyze content")
    print(f"   GET  /api/ai-content/health - Health check")
    print(f"   GET  /api/ai-content/languages - Supported languages")
    print(f"   GET  /api/ai-content/business-types - Business types")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
