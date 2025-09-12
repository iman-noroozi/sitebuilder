#!/usr/bin/env python3
"""
📝 Smart Content & SEO Generator - سازنده محتوا و SEO هوشمند PEY Builder
"""

import json
import re
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentType(Enum):
    """انواع محتوا"""
    BLOG_POST = "blog_post"
    PRODUCT_DESCRIPTION = "product_description"
    LANDING_PAGE = "landing_page"
    ABOUT_PAGE = "about_page"
    FAQ = "faq"
    NEWS_ARTICLE = "news_article"

class SEOTarget(Enum):
    """اهداف SEO"""
    LOCAL_SEO = "local_seo"
    ECOMMERCE_SEO = "ecommerce_seo"
    CONTENT_MARKETING = "content_marketing"
    TECHNICAL_SEO = "technical_seo"

@dataclass
class KeywordData:
    """داده‌های کلیدواژه"""
    keyword: str
    search_volume: int
    difficulty: float
    cpc: float
    competition: str
    related_keywords: List[str]

@dataclass
class ContentStructure:
    """ساختار محتوا"""
    title: str
    meta_description: str
    headings: List[str]
    paragraphs: List[str]
    keywords: List[str]
    internal_links: List[str]
    external_links: List[str]
    images: List[str]
    seo_score: float

@dataclass
class CompetitorAnalysis:
    """تحلیل رقبا"""
    domain: str
    title: str
    meta_description: str
    headings: List[str]
    keywords: List[str]
    content_length: int
    backlinks: int
    domain_authority: float

class SmartContentSEOGenerator:
    """سازنده محتوا و SEO هوشمند"""
    
    def __init__(self):
        self.keyword_database = self._load_keyword_database()
        self.content_templates = self._load_content_templates()
        self.seo_rules = self._load_seo_rules()
        self.competitor_data = self._load_competitor_data()
        
        logger.info("📝 Smart Content & SEO Generator initialized")
    
    def _load_keyword_database(self) -> Dict[str, KeywordData]:
        """بارگذاری دیتابیس کلیدواژه‌ها"""
        return {
            "فروشگاه آنلاین": KeywordData(
                keyword="فروشگاه آنلاین",
                search_volume=12000,
                difficulty=0.7,
                cpc=2.5,
                competition="high",
                related_keywords=["خرید آنلاین", "فروشگاه اینترنتی", "سایت فروشگاهی"]
            ),
            "طراحی سایت": KeywordData(
                keyword="طراحی سایت",
                search_volume=8500,
                difficulty=0.6,
                cpc=3.2,
                competition="medium",
                related_keywords=["ساخت سایت", "طراحی وب", "سایت ساز"]
            ),
            "هوش مصنوعی": KeywordData(
                keyword="هوش مصنوعی",
                search_volume=15000,
                difficulty=0.8,
                cpc=4.1,
                competition="high",
                related_keywords=["AI", "یادگیری ماشین", "ربات هوشمند"]
            )
        }
    
    def _load_content_templates(self) -> Dict[ContentType, Dict]:
        """بارگذاری قالب‌های محتوا"""
        return {
            ContentType.BLOG_POST: {
                "structure": ["عنوان جذاب", "مقدمه", "محتوای اصلی", "نتیجه‌گیری"],
                "word_count": 1500,
                "headings": ["H1", "H2", "H3"],
                "seo_focus": "informational"
            },
            ContentType.PRODUCT_DESCRIPTION: {
                "structure": ["عنوان محصول", "ویژگی‌ها", "مزایا", "نحوه استفاده"],
                "word_count": 300,
                "headings": ["H1", "H2"],
                "seo_focus": "commercial"
            },
            ContentType.LANDING_PAGE: {
                "structure": ["عنوان اصلی", "مزایا", "شواهد اجتماعی", "دعوت به عمل"],
                "word_count": 800,
                "headings": ["H1", "H2", "H3"],
                "seo_focus": "conversion"
            }
        }
    
    def _load_seo_rules(self) -> Dict:
        """بارگذاری قوانین SEO"""
        return {
            "title_length": {"min": 30, "max": 60},
            "meta_description_length": {"min": 120, "max": 160},
            "heading_structure": ["H1", "H2", "H3", "H4"],
            "keyword_density": {"min": 0.5, "max": 2.0},
            "content_length": {"min": 300, "max": 2000},
            "image_alt_text": True,
            "internal_linking": True,
            "external_linking": True
        }
    
    def _load_competitor_data(self) -> List[CompetitorAnalysis]:
        """بارگذاری داده‌های رقبا"""
        return [
            CompetitorAnalysis(
                domain="example1.com",
                title="بهترین فروشگاه آنلاین",
                meta_description="فروشگاه آنلاین با بهترین قیمت‌ها و کیفیت",
                headings=["محصولات", "خدمات", "تماس با ما"],
                keywords=["فروشگاه", "آنلاین", "خرید"],
                content_length=1200,
                backlinks=500,
                domain_authority=65
            ),
            CompetitorAnalysis(
                domain="example2.com",
                title="طراحی سایت حرفه‌ای",
                meta_description="طراحی سایت مدرن و حرفه‌ای برای کسب‌وکار شما",
                headings=["خدمات طراحی", "نمونه کارها", "قیمت‌ها"],
                keywords=["طراحی", "سایت", "حرفه‌ای"],
                content_length=800,
                backlinks=300,
                domain_authority=55
            )
        ]
    
    def generate_content(self, topic: str, content_type: ContentType, 
                        target_keywords: List[str], target_audience: str = "عمومی") -> ContentStructure:
        """تولید محتوا"""
        logger.info(f"📝 Generating {content_type.value} content for topic: {topic}")
        
        # تحلیل کلیدواژه‌ها
        keyword_analysis = self._analyze_keywords(target_keywords)
        
        # تولید عنوان
        title = self._generate_title(topic, keyword_analysis, content_type)
        
        # تولید meta description
        meta_description = self._generate_meta_description(topic, keyword_analysis)
        
        # تولید headings
        headings = self._generate_headings(topic, content_type, keyword_analysis)
        
        # تولید paragraphs
        paragraphs = self._generate_paragraphs(topic, content_type, keyword_analysis, target_audience)
        
        # تولید لینک‌ها
        internal_links = self._generate_internal_links(topic, keyword_analysis)
        external_links = self._generate_external_links(topic, keyword_analysis)
        
        # تولید تصاویر
        images = self._generate_image_suggestions(topic, content_type)
        
        # محاسبه امتیاز SEO
        seo_score = self._calculate_seo_score(title, meta_description, headings, paragraphs, target_keywords)
        
        content = ContentStructure(
            title=title,
            meta_description=meta_description,
            headings=headings,
            paragraphs=paragraphs,
            keywords=target_keywords,
            internal_links=internal_links,
            external_links=external_links,
            images=images,
            seo_score=seo_score
        )
        
        logger.info(f"✅ Content generated with SEO score: {seo_score:.2f}")
        return content
    
    def _analyze_keywords(self, keywords: List[str]) -> Dict[str, KeywordData]:
        """تحلیل کلیدواژه‌ها"""
        analysis = {}
        
        for keyword in keywords:
            if keyword in self.keyword_database:
                analysis[keyword] = self.keyword_database[keyword]
            else:
                # شبیه‌سازی داده‌های کلیدواژه جدید
                analysis[keyword] = KeywordData(
                    keyword=keyword,
                    search_volume=random.randint(1000, 10000),
                    difficulty=random.uniform(0.3, 0.9),
                    cpc=random.uniform(1.0, 5.0),
                    competition="medium",
                    related_keywords=self._generate_related_keywords(keyword)
                )
        
        return analysis
    
    def _generate_title(self, topic: str, keyword_analysis: Dict, content_type: ContentType) -> str:
        """تولید عنوان"""
        primary_keyword = list(keyword_analysis.keys())[0] if keyword_analysis else topic
        
        templates = {
            ContentType.BLOG_POST: [
                f"راهنمای کامل {primary_keyword} در سال 2024",
                f"همه چیز درباره {primary_keyword} که باید بدانید",
                f"نکات طلایی برای {primary_keyword}"
            ],
            ContentType.PRODUCT_DESCRIPTION: [
                f"خرید {primary_keyword} با بهترین قیمت",
                f"{primary_keyword} - کیفیت تضمینی",
                f"بهترین {primary_keyword} موجود در بازار"
            ],
            ContentType.LANDING_PAGE: [
                f"راه‌حل {primary_keyword} برای کسب‌وکار شما",
                f"تخصص ما در {primary_keyword}",
                f"خدمات {primary_keyword} با کیفیت بالا"
            ]
        }
        
        title_options = templates.get(content_type, [f"راهنمای {primary_keyword}"])
        selected_title = title_options[0]  # در نسخه کامل، انتخاب هوشمندانه
        
        # بررسی طول عنوان
        if len(selected_title) > self.seo_rules["title_length"]["max"]:
            selected_title = selected_title[:self.seo_rules["title_length"]["max"]-3] + "..."
        
        return selected_title
    
    def _generate_meta_description(self, topic: str, keyword_analysis: Dict) -> str:
        """تولید meta description"""
        primary_keyword = list(keyword_analysis.keys())[0] if keyword_analysis else topic
        
        description = f"راهنمای جامع {primary_keyword} با نکات کاربردی و تخصصی. "
        description += f"یادگیری {primary_keyword} به صورت کامل و حرفه‌ای. "
        description += "مشاوره رایگان و پشتیبانی 24/7."
        
        # بررسی طول meta description
        if len(description) > self.seo_rules["meta_description_length"]["max"]:
            description = description[:self.seo_rules["meta_description_length"]["max"]-3] + "..."
        
        return description
    
    def _generate_headings(self, topic: str, content_type: ContentType, keyword_analysis: Dict) -> List[str]:
        """تولید headings"""
        template = self.content_templates[content_type]
        headings = []
        
        # H1
        headings.append(f"راهنمای کامل {topic}")
        
        # H2 headings
        if content_type == ContentType.BLOG_POST:
            headings.extend([
                "مقدمه‌ای بر موضوع",
                "نکات مهم و کاربردی",
                "راه‌حل‌های پیشنهادی",
                "نتیجه‌گیری"
            ])
        elif content_type == ContentType.PRODUCT_DESCRIPTION:
            headings.extend([
                "ویژگی‌های محصول",
                "مزایای استفاده",
                "نحوه استفاده",
                "سوالات متداول"
            ])
        elif content_type == ContentType.LANDING_PAGE:
            headings.extend([
                "خدمات ما",
                "مزایای رقابتی",
                "شواهد اجتماعی",
                "تماس با ما"
            ])
        
        return headings
    
    def _generate_paragraphs(self, topic: str, content_type: ContentType, 
                           keyword_analysis: Dict, target_audience: str) -> List[str]:
        """تولید paragraphs"""
        paragraphs = []
        
        # مقدمه
        intro = f"در این مقاله به بررسی جامع {topic} می‌پردازیم. "
        intro += f"این موضوع برای {target_audience} بسیار مهم و کاربردی است. "
        intro += "با مطالعه این راهنما، اطلاعات کاملی در این زمینه کسب خواهید کرد."
        paragraphs.append(intro)
        
        # محتوای اصلی
        if content_type == ContentType.BLOG_POST:
            paragraphs.extend([
                f"موضوع {topic} یکی از مهم‌ترین مباحث در حوزه تکنولوژی است. "
                "در این بخش به بررسی جزئیات و نکات مهم می‌پردازیم.",
                
                "برای درک بهتر این موضوع، باید به چند نکته کلیدی توجه کنید. "
                "این نکات به شما کمک می‌کند تا بهترین نتیجه را بگیرید.",
                
                "در ادامه، راه‌حل‌های عملی و کاربردی ارائه می‌دهیم که "
                "می‌توانید به راحتی از آن‌ها استفاده کنید."
            ])
        elif content_type == ContentType.PRODUCT_DESCRIPTION:
            paragraphs.extend([
                f"محصول {topic} با کیفیت بالا و قیمت مناسب عرضه می‌شود. "
                "این محصول تمام نیازهای شما را برآورده می‌کند.",
                
                "ویژگی‌های منحصر به فرد این محصول آن را از سایر محصولات مشابه متمایز می‌کند. "
                "کیفیت ساخت و مواد اولیه درجه یک تضمین شده است.",
                
                "برای استفاده از این محصول، کافی است دستورالعمل‌های ساده را دنبال کنید. "
                "پشتیبانی کامل و مشاوره رایگان در اختیار شما قرار دارد."
            ])
        
        # نتیجه‌گیری
        conclusion = f"در پایان، {topic} موضوعی است که نیاز به توجه و دقت دارد. "
        conclusion += "با رعایت نکات ارائه شده، می‌توانید بهترین نتیجه را کسب کنید. "
        conclusion += "برای اطلاعات بیشتر با ما تماس بگیرید."
        paragraphs.append(conclusion)
        
        return paragraphs
    
    def _generate_internal_links(self, topic: str, keyword_analysis: Dict) -> List[str]:
        """تولید لینک‌های داخلی"""
        internal_links = [
            f"/blog/{topic.replace(' ', '-')}-guide",
            f"/services/{topic.replace(' ', '-')}",
            f"/about-{topic.replace(' ', '-')}",
            "/contact",
            "/faq"
        ]
        return internal_links
    
    def _generate_external_links(self, topic: str, keyword_analysis: Dict) -> List[str]:
        """تولید لینک‌های خارجی"""
        external_links = [
            "https://example.com/authority-site",
            "https://research.com/study",
            "https://industry.com/standards"
        ]
        return external_links
    
    def _generate_image_suggestions(self, topic: str, content_type: ContentType) -> List[str]:
        """تولید پیشنهادات تصاویر"""
        images = [
            f"{topic}-main-image.jpg",
            f"{topic}-infographic.png",
            f"{topic}-diagram.svg"
        ]
        return images
    
    def _calculate_seo_score(self, title: str, meta_description: str, 
                           headings: List[str], paragraphs: List[str], keywords: List[str]) -> float:
        """محاسبه امتیاز SEO"""
        score = 0.0
        
        # بررسی عنوان
        if self.seo_rules["title_length"]["min"] <= len(title) <= self.seo_rules["title_length"]["max"]:
            score += 20
        
        # بررسی meta description
        if self.seo_rules["meta_description_length"]["min"] <= len(meta_description) <= self.seo_rules["meta_description_length"]["max"]:
            score += 20
        
        # بررسی headings
        if len(headings) >= 3:
            score += 15
        
        # بررسی طول محتوا
        total_content = " ".join(paragraphs)
        if self.seo_rules["content_length"]["min"] <= len(total_content) <= self.seo_rules["content_length"]["max"]:
            score += 20
        
        # بررسی تراکم کلیدواژه
        keyword_density = self._calculate_keyword_density(total_content, keywords)
        if self.seo_rules["keyword_density"]["min"] <= keyword_density <= self.seo_rules["keyword_density"]["max"]:
            score += 15
        
        # بررسی ساختار
        if self._check_content_structure(headings, paragraphs):
            score += 10
        
        return min(score, 100.0)
    
    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> float:
        """محاسبه تراکم کلیدواژه"""
        total_words = len(content.split())
        keyword_count = 0
        
        for keyword in keywords:
            keyword_count += content.lower().count(keyword.lower())
        
        return (keyword_count / total_words) * 100 if total_words > 0 else 0
    
    def _check_content_structure(self, headings: List[str], paragraphs: List[str]) -> bool:
        """بررسی ساختار محتوا"""
        return len(headings) > 0 and len(paragraphs) > 0
    
    def _generate_related_keywords(self, keyword: str) -> List[str]:
        """تولید کلیدواژه‌های مرتبط"""
        related = [
            f"{keyword} چیست",
            f"راهنمای {keyword}",
            f"نکات {keyword}",
            f"بهترین {keyword}"
        ]
        return related
    
    def analyze_competitors(self, topic: str) -> List[CompetitorAnalysis]:
        """تحلیل رقبا"""
        logger.info(f"🔍 Analyzing competitors for topic: {topic}")
        
        # فیلتر کردن رقبا بر اساس موضوع
        relevant_competitors = [
            competitor for competitor in self.competitor_data
            if any(keyword in competitor.title.lower() or keyword in competitor.meta_description.lower()
                   for keyword in topic.lower().split())
        ]
        
        # مرتب‌سازی بر اساس domain authority
        relevant_competitors.sort(key=lambda x: x.domain_authority, reverse=True)
        
        return relevant_competitors[:5]  # بازگشت 5 رقیب برتر
    
    def generate_seo_recommendations(self, content: ContentStructure, 
                                   competitors: List[CompetitorAnalysis]) -> List[str]:
        """تولید توصیه‌های SEO"""
        recommendations = []
        
        # بررسی عنوان
        if len(content.title) < self.seo_rules["title_length"]["min"]:
            recommendations.append("عنوان را طولانی‌تر کنید تا حداقل 30 کاراکتر باشد")
        elif len(content.title) > self.seo_rules["title_length"]["max"]:
            recommendations.append("عنوان را کوتاه‌تر کنید تا حداکثر 60 کاراکتر باشد")
        
        # بررسی meta description
        if len(content.meta_description) < self.seo_rules["meta_description_length"]["min"]:
            recommendations.append("Meta description را طولانی‌تر کنید")
        
        # بررسی headings
        if len(content.headings) < 3:
            recommendations.append("تعداد headings را افزایش دهید")
        
        # بررسی لینک‌ها
        if len(content.internal_links) < 3:
            recommendations.append("لینک‌های داخلی بیشتری اضافه کنید")
        
        if len(content.external_links) < 2:
            recommendations.append("لینک‌های خارجی معتبر اضافه کنید")
        
        # مقایسه با رقبا
        if competitors:
            best_competitor = competitors[0]
            if len(content.title) < len(best_competitor.title):
                recommendations.append(f"عنوان را مانند رقیب برتر ({best_competitor.domain}) بهبود دهید")
        
        return recommendations
    
    def optimize_images(self, images: List[str], topic: str) -> List[Dict[str, str]]:
        """بهینه‌سازی تصاویر"""
        optimized_images = []
        
        for image in images:
            optimized = {
                "original": image,
                "alt_text": f"تصویر {topic} - توضیحات کامل",
                "title": f"عنوان تصویر {topic}",
                "compressed": f"compressed_{image}",
                "webp": f"{image.split('.')[0]}.webp",
                "responsive": f"responsive_{image}"
            }
            optimized_images.append(optimized)
        
        return optimized_images

# مثال استفاده
if __name__ == "__main__":
    # ایجاد generator
    generator = SmartContentSEOGenerator()
    
    # تولید محتوا
    content = generator.generate_content(
        topic="طراحی سایت",
        content_type=ContentType.BLOG_POST,
        target_keywords=["طراحی سایت", "ساخت وب‌سایت", "طراحی وب"],
        target_audience="صاحبان کسب‌وکار"
    )
    
    print("📝 Generated Content:")
    print(f"Title: {content.title}")
    print(f"Meta Description: {content.meta_description}")
    print(f"SEO Score: {content.seo_score:.2f}")
    print(f"Headings: {len(content.headings)}")
    print(f"Paragraphs: {len(content.paragraphs)}")
    
    # تحلیل رقبا
    competitors = generator.analyze_competitors("طراحی سایت")
    print(f"\n🔍 Competitors Analysis: {len(competitors)} competitors found")
    
    # تولید توصیه‌ها
    recommendations = generator.generate_seo_recommendations(content, competitors)
    print(f"\n💡 SEO Recommendations:")
    for rec in recommendations:
        print(f"- {rec}")
    
    # بهینه‌سازی تصاویر
    optimized_images = generator.optimize_images(content.images, "طراحی سایت")
    print(f"\n🖼️ Optimized Images: {len(optimized_images)} images")
