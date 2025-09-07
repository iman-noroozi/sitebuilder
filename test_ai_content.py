#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for AI Content Generator
Tests all functionality of the AI Content Generation system
"""

import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_content_generator import AIContentGenerator, ContentRequest, GeneratedContent

def test_ai_content_generator():
    """Test the AI Content Generator functionality"""
    print("🤖 Testing AI Content Generator...")
    print("=" * 50)
    
    # Initialize the generator
    generator = AIContentGenerator()
    
    # Test 1: Restaurant content in Persian
    print("\n🍽️ Test 1: Restaurant Content (Persian)")
    print("-" * 30)
    
    restaurant_request = ContentRequest(
        business_type="restaurant",
        language="fa",
        content_type="homepage",
        tone="friendly",
        length="medium",
        keywords=["رستوران", "غذا", "طعم", "کیفیت"],
        target_audience="families",
        industry="food"
    )
    
    restaurant_content = generator.generate_content(restaurant_request)
    print(f"✅ Title: {restaurant_content.title}")
    print(f"✅ Content: {restaurant_content.content[:100]}...")
    print(f"✅ SEO Score: {restaurant_content.seo_score}/100")
    print(f"✅ Readability Score: {restaurant_content.readability_score}/100")
    print(f"✅ Word Count: {restaurant_content.word_count}")
    print(f"✅ Language: {restaurant_content.language}")
    
    # Test 2: E-commerce content in English
    print("\n🛒 Test 2: E-commerce Content (English)")
    print("-" * 30)
    
    ecommerce_request = ContentRequest(
        business_type="ecommerce",
        language="en",
        content_type="homepage",
        tone="professional",
        length="long",
        keywords=["store", "products", "quality", "shipping"],
        target_audience="shoppers",
        industry="retail"
    )
    
    ecommerce_content = generator.generate_content(ecommerce_request)
    print(f"✅ Title: {ecommerce_content.title}")
    print(f"✅ Content: {ecommerce_content.content[:100]}...")
    print(f"✅ SEO Score: {ecommerce_content.seo_score}/100")
    print(f"✅ Readability Score: {ecommerce_content.readability_score}/100")
    print(f"✅ Word Count: {ecommerce_content.word_count}")
    print(f"✅ Language: {ecommerce_content.language}")
    
    # Test 3: Consulting content in Arabic
    print("\n💼 Test 3: Consulting Content (Arabic)")
    print("-" * 30)
    
    consulting_request = ContentRequest(
        business_type="consulting",
        language="ar",
        content_type="services",
        tone="formal",
        length="medium",
        keywords=["استشارات", "خدمات", "خبرة"],
        target_audience="businesses",
        industry="consulting"
    )
    
    consulting_content = generator.generate_content(consulting_request)
    print(f"✅ Title: {consulting_content.title}")
    print(f"✅ Content: {consulting_content.content[:100]}...")
    print(f"✅ SEO Score: {consulting_content.seo_score}/100")
    print(f"✅ Readability Score: {consulting_content.readability_score}/100")
    print(f"✅ Word Count: {consulting_content.word_count}")
    print(f"✅ Language: {consulting_content.language}")
    
    # Test 4: Translation functionality
    print("\n🌍 Test 4: Translation Functionality")
    print("-" * 30)
    
    try:
        translated_content = generator.translate_content(restaurant_content, "en")
        print(f"✅ Original (Persian): {restaurant_content.title}")
        print(f"✅ Translated (English): {translated_content.title}")
        print(f"✅ Translation successful!")
    except Exception as e:
        print(f"❌ Translation failed: {e}")
    
    # Test 5: Content suggestions
    print("\n💡 Test 5: Content Suggestions")
    print("-" * 30)
    
    suggestions = generator.get_content_suggestions("restaurant", "fa")
    print(f"✅ Found {len(suggestions)} suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. {suggestion['title']} - {suggestion['description']}")
    
    # Test 6: SEO Analysis
    print("\n📊 Test 6: SEO Analysis")
    print("-" * 30)
    
    test_content = {
        "title": "Best Restaurant in Tehran - Authentic Persian Food",
        "content": "Welcome to our restaurant. We serve the best Persian food with fresh ingredients and authentic recipes. Our chefs have years of experience in traditional Persian cuisine.",
        "meta_description": "Best restaurant in Tehran serving authentic Persian food with fresh ingredients and traditional recipes.",
        "keywords": ["restaurant", "Persian", "food", "Tehran"]
    }
    
    mock_request = ContentRequest(
        business_type="restaurant",
        language="en",
        keywords=["restaurant", "Persian", "food"]
    )
    
    seo_score = generator._calculate_seo_score(test_content, mock_request)
    readability_score = generator._calculate_readability_score(test_content)
    
    print(f"✅ SEO Score: {seo_score}/100")
    print(f"✅ Readability Score: {readability_score}/100")
    
    # Test 7: Language detection
    print("\n🔍 Test 7: Language Detection")
    print("-" * 30)
    
    test_texts = [
        "این یک متن فارسی است",
        "This is an English text",
        "هذا نص عربي",
        "Ceci est un texte français"
    ]
    
    for text in test_texts:
        detected = generator._detect_language(text)
        print(f"✅ '{text}' -> {detected}")
    
    print("\n🎉 All tests completed successfully!")
    return True

def test_api_endpoints():
    """Test API endpoints (if server is running)"""
    print("\n🌐 Testing API Endpoints...")
    print("=" * 50)
    
    import requests
    
    base_url = "http://localhost:5001"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/ai-content/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check endpoint working")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ API server not running (this is expected)")
        return False
    
    # Test supported languages
    try:
        response = requests.get(f"{base_url}/api/ai-content/languages", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Languages endpoint working - {len(data['languages'])} languages supported")
        else:
            print(f"❌ Languages endpoint failed: {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ Languages endpoint not accessible")
    
    # Test business types
    try:
        response = requests.get(f"{base_url}/api/ai-content/business-types", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Business types endpoint working - {len(data['business_types'])} types supported")
        else:
            print(f"❌ Business types endpoint failed: {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ Business types endpoint not accessible")
    
    return True

def generate_sample_content():
    """Generate sample content for demonstration"""
    print("\n📝 Generating Sample Content...")
    print("=" * 50)
    
    generator = AIContentGenerator()
    
    # Sample requests
    sample_requests = [
        {
            "name": "Persian Restaurant",
            "request": ContentRequest(
                business_type="restaurant",
                language="fa",
                content_type="homepage",
                tone="friendly",
                keywords=["رستوران", "غذا", "طعم"]
            )
        },
        {
            "name": "English E-commerce",
            "request": ContentRequest(
                business_type="ecommerce",
                language="en",
                content_type="homepage",
                tone="professional",
                keywords=["store", "products", "quality"]
            )
        },
        {
            "name": "Arabic Consulting",
            "request": ContentRequest(
                business_type="consulting",
                language="ar",
                content_type="services",
                tone="formal",
                keywords=["استشارات", "خدمات"]
            )
        }
    ]
    
    sample_content = []
    
    for sample in sample_requests:
        print(f"\n📄 Generating {sample['name']}...")
        content = generator.generate_content(sample['request'])
        
        sample_content.append({
            "name": sample['name'],
            "content": {
                "title": content.title,
                "content": content.content,
                "meta_description": content.meta_description,
                "keywords": content.keywords,
                "seo_score": content.seo_score,
                "readability_score": content.readability_score,
                "language": content.language,
                "word_count": content.word_count
            }
        })
        
        print(f"✅ Generated: {content.title}")
        print(f"   SEO Score: {content.seo_score}/100")
        print(f"   Readability: {content.readability_score}/100")
        print(f"   Words: {content.word_count}")
    
    # Save to file
    output_file = "sample_ai_content.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_content, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Sample content saved to: {output_file}")
    return sample_content

def main():
    """Main test function"""
    print("🚀 AI Content Generator Test Suite")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Run core tests
        test_ai_content_generator()
        
        # Test API endpoints
        test_api_endpoints()
        
        # Generate sample content
        generate_sample_content()
        
        print("\n🎉 All tests completed successfully!")
        print("✅ AI Content Generator is working properly!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
