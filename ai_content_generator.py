#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Content Generator - Advanced Content Creation System
Generates intelligent content in multiple languages with SEO optimization
"""

import json
import re
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import requests
import openai
from googletrans import Translator
import langdetect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

@dataclass
class ContentRequest:
    """Content generation request structure"""
    business_type: str
    language: str = "fa"  # fa, en, ar, etc.
    content_type: str = "homepage"  # homepage, about, services, contact
    tone: str = "professional"  # professional, casual, friendly, formal
    length: str = "medium"  # short, medium, long
    keywords: List[str] = None
    target_audience: str = "general"
    industry: str = "general"

@dataclass
class GeneratedContent:
    """Generated content structure"""
    title: str
    content: str
    meta_description: str
    keywords: List[str]
    seo_score: int
    readability_score: int
    language: str
    word_count: int
    created_at: datetime

class AIContentGenerator:
    """Advanced AI Content Generator with multilingual support"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.translator = Translator()
        self.content_templates = self._load_content_templates()
        self.seo_keywords = self._load_seo_keywords()
        self.industry_templates = self._load_industry_templates()
        
        if openai_api_key:
            openai.api_key = openai_api_key
    
    def _load_content_templates(self) -> Dict:
        """Load content templates for different business types"""
        return {
            "restaurant": {
                "fa": {
                    "homepage": {
                        "title": "رستوران {name} - بهترین طعم‌های {cuisine}",
                        "content": "به رستوران {name} خوش آمدید. ما با {years} سال تجربه، بهترین {cuisine} را با مواد اولیه تازه و دستور پخت اصیل ارائه می‌دهیم.",
                        "meta": "رستوران {name} - {cuisine} اصیل با {years} سال تجربه. رزرو آنلاین، تحویل سریع، طعم بی‌نظیر."
                    }
                },
                "en": {
                    "homepage": {
                        "title": "{name} Restaurant - Best {cuisine} Flavors",
                        "content": "Welcome to {name} Restaurant. With {years} years of experience, we serve the best {cuisine} with fresh ingredients and authentic recipes.",
                        "meta": "{name} Restaurant - Authentic {cuisine} with {years} years experience. Online booking, fast delivery, amazing taste."
                    }
                }
            },
            "ecommerce": {
                "fa": {
                    "homepage": {
                        "title": "فروشگاه آنلاین {name} - بهترین محصولات {category}",
                        "content": "فروشگاه آنلاین {name} با {products_count}+ محصول باکیفیت در دسته‌بندی {category}. ارسال رایگان، ضمانت کیفیت، پشتیبانی 24/7.",
                        "meta": "فروشگاه آنلاین {name} - {category} باکیفیت، ارسال رایگان، ضمانت کیفیت. خرید آنلاین آسان و امن."
                    }
                },
                "en": {
                    "homepage": {
                        "title": "{name} Online Store - Best {category} Products",
                        "content": "{name} Online Store offers {products_count}+ quality products in {category} category. Free shipping, quality guarantee, 24/7 support.",
                        "meta": "{name} Online Store - Quality {category}, free shipping, quality guarantee. Easy and secure online shopping."
                    }
                }
            },
            "consulting": {
                "fa": {
                    "homepage": {
                        "title": "مشاوره {service} - {name}",
                        "content": "شرکت مشاوره {name} با تیم متخصص و {years} سال تجربه، خدمات {service} را با بالاترین کیفیت ارائه می‌دهد.",
                        "meta": "مشاوره {service} - {name} با {years} سال تجربه. تیم متخصص، خدمات باکیفیت، مشاوره رایگان."
                    }
                },
                "en": {
                    "homepage": {
                        "title": "{service} Consulting - {name}",
                        "content": "{name} Consulting Company with expert team and {years} years experience provides {service} services with highest quality.",
                        "meta": "{service} Consulting - {name} with {years} years experience. Expert team, quality services, free consultation."
                    }
                }
            }
        }
    
    def _load_seo_keywords(self) -> Dict:
        """Load SEO keywords for different industries"""
        return {
            "restaurant": {
                "fa": ["رستوران", "غذا", "طعم", "رزرو", "تحویل", "کیفیت", "اصیل"],
                "en": ["restaurant", "food", "taste", "booking", "delivery", "quality", "authentic"]
            },
            "ecommerce": {
                "fa": ["فروشگاه", "خرید", "محصول", "ارسال", "قیمت", "کیفیت", "ضمانت"],
                "en": ["store", "buy", "product", "shipping", "price", "quality", "guarantee"]
            },
            "consulting": {
                "fa": ["مشاوره", "خدمات", "متخصص", "تجربه", "کیفیت", "راهنمایی"],
                "en": ["consulting", "services", "expert", "experience", "quality", "guidance"]
            }
        }
    
    def _load_industry_templates(self) -> Dict:
        """Load industry-specific templates"""
        return {
            "technology": {
                "fa": "فناوری و نوآوری",
                "en": "Technology and Innovation"
            },
            "healthcare": {
                "fa": "بهداشت و درمان",
                "en": "Healthcare and Medical"
            },
            "education": {
                "fa": "آموزش و پرورش",
                "en": "Education and Training"
            },
            "finance": {
                "fa": "مالی و بانکداری",
                "en": "Finance and Banking"
            }
        }
    
    def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate intelligent content based on request"""
        try:
            # Detect language if not specified
            if not request.language:
                request.language = self._detect_language(request.business_type)
            
            # Get base template
            template = self._get_template(request)
            
            # Generate content using AI or templates
            if self.openai_api_key and request.language in ["en", "fa"]:
                content = self._generate_with_ai(request, template)
            else:
                content = self._generate_with_template(request, template)
            
            # Optimize for SEO
            seo_optimized = self._optimize_seo(content, request)
            
            # Calculate scores
            seo_score = self._calculate_seo_score(seo_optimized, request)
            readability_score = self._calculate_readability_score(seo_optimized)
            
            return GeneratedContent(
                title=seo_optimized["title"],
                content=seo_optimized["content"],
                meta_description=seo_optimized["meta_description"],
                keywords=seo_optimized["keywords"],
                seo_score=seo_score,
                readability_score=readability_score,
                language=request.language,
                word_count=len(seo_optimized["content"].split()),
                created_at=datetime.now()
            )
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return self._generate_fallback_content(request)
    
    def _detect_language(self, text: str) -> str:
        """Detect language of input text"""
        try:
            detected = langdetect.detect(text)
            return detected
        except:
            return "en"
    
    def _get_template(self, request: ContentRequest) -> Dict:
        """Get appropriate template for request"""
        business_type = request.business_type.lower()
        language = request.language
        
        if business_type in self.content_templates:
            if language in self.content_templates[business_type]:
                return self.content_templates[business_type][language]
        
        # Fallback to general template
        return self._get_general_template(language)
    
    def _get_general_template(self, language: str) -> Dict:
        """Get general template for any language"""
        if language == "fa":
            return {
                "homepage": {
                    "title": "شرکت {name} - خدمات {service}",
                    "content": "به {name} خوش آمدید. ما خدمات {service} را با بالاترین کیفیت ارائه می‌دهیم.",
                    "meta": "شرکت {name} - خدمات {service} باکیفیت. تیم متخصص، تجربه بالا."
                }
            }
        else:
            return {
                "homepage": {
                    "title": "{name} Company - {service} Services",
                    "content": "Welcome to {name}. We provide {service} services with highest quality.",
                    "meta": "{name} Company - Quality {service} services. Expert team, high experience."
                }
            }
    
    def _generate_with_ai(self, request: ContentRequest, template: Dict) -> Dict:
        """Generate content using OpenAI API"""
        try:
            prompt = self._create_ai_prompt(request, template)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert content writer and SEO specialist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_content = response.choices[0].message.content
            
            return {
                "title": self._extract_title(ai_content),
                "content": ai_content,
                "meta_description": self._extract_meta_description(ai_content),
                "keywords": self._extract_keywords(ai_content, request)
            }
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_with_template(request, template)
    
    def _create_ai_prompt(self, request: ContentRequest, template: Dict) -> str:
        """Create AI prompt for content generation"""
        language_name = "Persian" if request.language == "fa" else "English"
        
        prompt = f"""
        Write a {request.content_type} page content in {language_name} for a {request.business_type} business.
        
        Requirements:
        - Language: {language_name}
        - Tone: {request.tone}
        - Length: {request.length}
        - Target Audience: {request.target_audience}
        - Industry: {request.industry}
        
        Include:
        1. Compelling title
        2. Engaging content
        3. SEO-optimized meta description
        4. Relevant keywords
        
        Make it professional, engaging, and SEO-friendly.
        """
        
        if request.keywords:
            prompt += f"\nKeywords to include: {', '.join(request.keywords)}"
        
        return prompt
    
    def _generate_with_template(self, request: ContentRequest, template: Dict) -> Dict:
        """Generate content using templates"""
        content_type = request.content_type
        
        if content_type in template:
            base_template = template[content_type]
            
            # Replace placeholders
            title = base_template["title"].format(
                name=request.business_type.title(),
                service=request.industry,
                cuisine="ایرانی" if request.language == "fa" else "Persian",
                years="10",
                products_count="1000",
                category=request.industry
            )
            
            content = base_template["content"].format(
                name=request.business_type.title(),
                service=request.industry,
                cuisine="ایرانی" if request.language == "fa" else "Persian",
                years="10",
                products_count="1000",
                category=request.industry
            )
            
            meta_description = base_template["meta"].format(
                name=request.business_type.title(),
                service=request.industry,
                cuisine="ایرانی" if request.language == "fa" else "Persian",
                years="10",
                products_count="1000",
                category=request.industry
            )
            
            return {
                "title": title,
                "content": content,
                "meta_description": meta_description,
                "keywords": self._get_industry_keywords(request.business_type, request.language)
            }
        
        return self._generate_fallback_content(request)
    
    def _get_industry_keywords(self, business_type: str, language: str) -> List[str]:
        """Get industry-specific keywords"""
        if business_type in self.seo_keywords:
            if language in self.seo_keywords[business_type]:
                return self.seo_keywords[business_type][language]
        
        # Fallback keywords
        if language == "fa":
            return ["خدمات", "کیفیت", "تجربه", "متخصص"]
        else:
            return ["services", "quality", "experience", "expert"]
    
    def _optimize_seo(self, content: Dict, request: ContentRequest) -> Dict:
        """Optimize content for SEO"""
        optimized = content.copy()
        
        # Add keywords to title
        if request.keywords:
            keywords_str = " | ".join(request.keywords[:3])
            optimized["title"] += f" | {keywords_str}"
        
        # Optimize meta description length
        if len(optimized["meta_description"]) > 160:
            optimized["meta_description"] = optimized["meta_description"][:157] + "..."
        
        # Add keywords to content
        if request.keywords:
            for keyword in request.keywords[:5]:
                if keyword.lower() not in optimized["content"].lower():
                    optimized["content"] += f" {keyword}."
        
        return optimized
    
    def _calculate_seo_score(self, content: Dict, request: ContentRequest) -> int:
        """Calculate SEO score for content"""
        score = 0
        
        # Title length (50-60 characters optimal)
        title_len = len(content["title"])
        if 50 <= title_len <= 60:
            score += 20
        elif 40 <= title_len <= 70:
            score += 15
        
        # Meta description length (150-160 characters optimal)
        meta_len = len(content["meta_description"])
        if 150 <= meta_len <= 160:
            score += 20
        elif 140 <= meta_len <= 170:
            score += 15
        
        # Keyword density
        content_lower = content["content"].lower()
        keyword_count = sum(content_lower.count(keyword.lower()) for keyword in request.keywords or [])
        if keyword_count > 0:
            score += min(20, keyword_count * 2)
        
        # Content length
        word_count = len(content["content"].split())
        if 300 <= word_count <= 800:
            score += 20
        elif 200 <= word_count <= 1000:
            score += 15
        
        # Language-specific optimizations
        if request.language == "fa":
            # Check for Persian-specific SEO elements
            if "شرکت" in content["content"] or "خدمات" in content["content"]:
                score += 10
        else:
            # Check for English-specific SEO elements
            if any(word in content["content"].lower() for word in ["services", "company", "quality"]):
                score += 10
        
        return min(100, score)
    
    def _calculate_readability_score(self, content: Dict) -> int:
        """Calculate readability score"""
        try:
            text = content["content"]
            words = word_tokenize(text)
            sentences = re.split(r'[.!?]+', text)
            
            if len(sentences) == 0 or len(words) == 0:
                return 50
            
            avg_words_per_sentence = len(words) / len(sentences)
            
            # Simple readability calculation
            if avg_words_per_sentence <= 15:
                score = 90
            elif avg_words_per_sentence <= 20:
                score = 80
            elif avg_words_per_sentence <= 25:
                score = 70
            else:
                score = 60
            
            return score
            
        except Exception:
            return 50
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content"""
        lines = content.split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) < 100:
                return line.strip()
        return "Generated Title"
    
    def _extract_meta_description(self, content: str) -> str:
        """Extract meta description from content"""
        # Take first 150 characters
        return content[:150] + "..." if len(content) > 150 else content
    
    def _extract_keywords(self, content: str, request: ContentRequest) -> List[str]:
        """Extract keywords from content"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = {}
        
        for word in words:
            if len(word) > 3:  # Only words longer than 3 characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top 5 most frequent words
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _generate_fallback_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate fallback content when other methods fail"""
        if request.language == "fa":
            title = f"شرکت {request.business_type.title()}"
            content = f"به {request.business_type.title()} خوش آمدید. ما خدمات باکیفیت ارائه می‌دهیم."
            meta = f"شرکت {request.business_type.title()} - خدمات باکیفیت"
        else:
            title = f"{request.business_type.title()} Company"
            content = f"Welcome to {request.business_type.title()}. We provide quality services."
            meta = f"{request.business_type.title()} Company - Quality Services"
        
        return GeneratedContent(
            title=title,
            content=content,
            meta_description=meta,
            keywords=["services", "quality"],
            seo_score=60,
            readability_score=70,
            language=request.language,
            word_count=len(content.split()),
            created_at=datetime.now()
        )
    
    def translate_content(self, content: GeneratedContent, target_language: str) -> GeneratedContent:
        """Translate generated content to another language"""
        try:
            translated_title = self.translator.translate(content.title, dest=target_language).text
            translated_content = self.translator.translate(content.content, dest=target_language).text
            translated_meta = self.translator.translate(content.meta_description, dest=target_language).text
            
            return GeneratedContent(
                title=translated_title,
                content=translated_content,
                meta_description=translated_meta,
                keywords=content.keywords,  # Keep original keywords
                seo_score=content.seo_score,
                readability_score=content.readability_score,
                language=target_language,
                word_count=len(translated_content.split()),
                created_at=datetime.now()
            )
            
        except Exception as e:
            print(f"Translation failed: {e}")
            return content
    
    def get_content_suggestions(self, business_type: str, language: str = "fa") -> List[Dict]:
        """Get content suggestions for a business type"""
        suggestions = []
        
        content_types = ["homepage", "about", "services", "contact", "blog"]
        
        for content_type in content_types:
            suggestion = {
                "type": content_type,
                "title": f"{content_type.title()} Page",
                "description": f"Generate {content_type} content for {business_type}",
                "keywords": self._get_industry_keywords(business_type, language),
                "estimated_words": random.randint(200, 800)
            }
            suggestions.append(suggestion)
        
        return suggestions

# Example usage and testing
if __name__ == "__main__":
    # Initialize the AI Content Generator
    generator = AIContentGenerator()
    
    # Example 1: Restaurant content in Persian
    restaurant_request = ContentRequest(
        business_type="restaurant",
        language="fa",
        content_type="homepage",
        tone="friendly",
        length="medium",
        keywords=["رستوران", "غذا", "طعم"],
        target_audience="families",
        industry="food"
    )
    
    restaurant_content = generator.generate_content(restaurant_request)
    print("🍽️ Restaurant Content (Persian):")
    print(f"Title: {restaurant_content.title}")
    print(f"Content: {restaurant_content.content}")
    print(f"SEO Score: {restaurant_content.seo_score}")
    print(f"Readability Score: {restaurant_content.readability_score}")
    print()
    
    # Example 2: E-commerce content in English
    ecommerce_request = ContentRequest(
        business_type="ecommerce",
        language="en",
        content_type="homepage",
        tone="professional",
        length="long",
        keywords=["store", "products", "quality"],
        target_audience="shoppers",
        industry="retail"
    )
    
    ecommerce_content = generator.generate_content(ecommerce_request)
    print("🛒 E-commerce Content (English):")
    print(f"Title: {ecommerce_content.title}")
    print(f"Content: {ecommerce_content.content}")
    print(f"SEO Score: {ecommerce_content.seo_score}")
    print(f"Readability Score: {ecommerce_content.readability_score}")
    print()
    
    # Example 3: Get content suggestions
    suggestions = generator.get_content_suggestions("consulting", "fa")
    print("💡 Content Suggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion['title']}: {suggestion['description']}")
