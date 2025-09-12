#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏪 Agent Marketplace - بازار Agent های هوشمند
قابلیت‌های پیشرفته:
- فروش و خرید Agent ها
- سیستم امتیازدهی و نظرات
- دسته‌بندی و جستجوی پیشرفته
- سیستم لایسنس و اشتراک
- Analytics و گزارش‌گیری
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging
import uuid
import hashlib
from pathlib import Path

class AgentCategory(Enum):
    """دسته‌بندی Agent ها"""
    AUTOMATION = "automation"
    AI_ASSISTANT = "ai_assistant"
    DATA_PROCESSING = "data_processing"
    COMMUNICATION = "communication"
    ECOMMERCE = "ecommerce"
    MARKETING = "marketing"
    CUSTOMER_SERVICE = "customer_service"
    ANALYTICS = "analytics"
    INTEGRATION = "integration"
    CUSTOM = "custom"

class LicenseType(Enum):
    """انواع لایسنس"""
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"

class AgentStatus(Enum):
    """وضعیت Agent"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"

@dataclass
class AgentMetadata:
    """اطلاعات Agent"""
    id: str
    name: str
    description: str
    category: AgentCategory
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    author: str = ""
    author_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: AgentStatus = AgentStatus.DRAFT
    license_type: LicenseType = LicenseType.FREE
    price: float = 0.0
    currency: str = "USD"
    downloads: int = 0
    rating: float = 0.0
    reviews_count: int = 0
    thumbnail_url: str = ""
    demo_url: str = ""
    documentation_url: str = ""
    source_code_url: str = ""
    requirements: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    screenshots: List[str] = field(default_factory=list)
    workflow_data: Dict = field(default_factory=dict)

@dataclass
class Review:
    """نظر کاربر"""
    id: str
    agent_id: str
    user_id: str
    user_name: str
    rating: int  # 1-5
    title: str
    comment: str
    created_at: datetime = field(default_factory=datetime.now)
    helpful_count: int = 0
    verified_purchase: bool = False

@dataclass
class Purchase:
    """خرید Agent"""
    id: str
    agent_id: str
    user_id: str
    user_name: str
    price: float
    currency: str
    license_type: LicenseType
    purchase_date: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    status: str = "completed"

class AgentMarketplace:
    """بازار Agent های هوشمند"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.agents = {}
        self.reviews = {}
        self.purchases = {}
        self.users = {}
        self.categories = {}
        
        # تنظیم logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # مسیرهای فایل
        self.data_dir = Path("marketplace_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # فایل‌های داده
        self.agents_file = self.data_dir / "agents.json"
        self.reviews_file = self.data_dir / "reviews.json"
        self.purchases_file = self.data_dir / "purchases.json"
        self.users_file = self.data_dir / "users.json"
        
        # بارگذاری داده‌ها
        self._load_data()
        
        # Agent های پیش‌تعریف شده
        self._create_sample_agents()
    
    def _load_data(self):
        """بارگذاری داده‌ها از فایل"""
        # بارگذاری Agent ها
        if self.agents_file.exists():
            with open(self.agents_file, "r", encoding="utf-8") as f:
                agents_data = json.load(f)
                for agent_id, agent_data in agents_data.items():
                    self.agents[agent_id] = AgentMetadata(**agent_data)
        
        # بارگذاری نظرات
        if self.reviews_file.exists():
            with open(self.reviews_file, "r", encoding="utf-8") as f:
                reviews_data = json.load(f)
                for review_id, review_data in reviews_data.items():
                    self.reviews[review_id] = Review(**review_data)
        
        # بارگذاری خریدها
        if self.purchases_file.exists():
            with open(self.purchases_file, "r", encoding="utf-8") as f:
                purchases_data = json.load(f)
                for purchase_id, purchase_data in purchases_data.items():
                    self.purchases[purchase_id] = Purchase(**purchase_data)
    
    def _save_data(self):
        """ذخیره داده‌ها در فایل"""
        # ذخیره Agent ها
        agents_data = {}
        for agent_id, agent in self.agents.items():
            agents_data[agent_id] = {
                "id": agent.id,
                "name": agent.name,
                "description": agent.description,
                "category": agent.category.value,
                "tags": agent.tags,
                "version": agent.version,
                "author": agent.author,
                "author_id": agent.author_id,
                "created_at": agent.created_at.isoformat(),
                "updated_at": agent.updated_at.isoformat(),
                "status": agent.status.value,
                "license_type": agent.license_type.value,
                "price": agent.price,
                "currency": agent.currency,
                "downloads": agent.downloads,
                "rating": agent.rating,
                "reviews_count": agent.reviews_count,
                "thumbnail_url": agent.thumbnail_url,
                "demo_url": agent.demo_url,
                "documentation_url": agent.documentation_url,
                "source_code_url": agent.source_code_url,
                "requirements": agent.requirements,
                "features": agent.features,
                "screenshots": agent.screenshots,
                "workflow_data": agent.workflow_data
            }
        
        with open(self.agents_file, "w", encoding="utf-8") as f:
            json.dump(agents_data, f, ensure_ascii=False, indent=2)
        
        # ذخیره نظرات
        reviews_data = {}
        for review_id, review in self.reviews.items():
            reviews_data[review_id] = {
                "id": review.id,
                "agent_id": review.agent_id,
                "user_id": review.user_id,
                "user_name": review.user_name,
                "rating": review.rating,
                "title": review.title,
                "comment": review.comment,
                "created_at": review.created_at.isoformat(),
                "helpful_count": review.helpful_count,
                "verified_purchase": review.verified_purchase
            }
        
        with open(self.reviews_file, "w", encoding="utf-8") as f:
            json.dump(reviews_data, f, ensure_ascii=False, indent=2)
        
        # ذخیره خریدها
        purchases_data = {}
        for purchase_id, purchase in self.purchases.items():
            purchases_data[purchase_id] = {
                "id": purchase.id,
                "agent_id": purchase.agent_id,
                "user_id": purchase.user_id,
                "user_name": purchase.user_name,
                "price": purchase.price,
                "currency": purchase.currency,
                "license_type": purchase.license_type.value,
                "purchase_date": purchase.purchase_date.isoformat(),
                "expires_at": purchase.expires_at.isoformat() if purchase.expires_at else None,
                "status": purchase.status
            }
        
        with open(self.purchases_file, "w", encoding="utf-8") as f:
            json.dump(purchases_data, f, ensure_ascii=False, indent=2)
    
    def _create_sample_agents(self):
        """ایجاد Agent های نمونه"""
        if self.agents:  # اگر قبلاً Agent هایی وجود دارد، نمونه ایجاد نکن
            return
        
        sample_agents = [
            {
                "name": "🤖 Customer Service Bot",
                "description": "ربات پاسخگویی خودکار به مشتریان با قابلیت‌های پیشرفته AI",
                "category": AgentCategory.CUSTOMER_SERVICE,
                "tags": ["customer-service", "ai", "automation", "chatbot"],
                "author": "پیسان وب",
                "price": 29.99,
                "license_type": LicenseType.PREMIUM,
                "features": [
                    "پاسخگویی 24/7",
                    "پشتیبانی چندزبانه",
                    "ادغام با CRM",
                    "تحلیل احساسات"
                ],
                "workflow_data": {
                    "nodes": [
                        {"id": "input1", "type": "input", "config": {"type": "text"}},
                        {"id": "ai1", "type": "processing", "config": {"type": "gpt"}},
                        {"id": "output1", "type": "output", "config": {"type": "text"}}
                    ]
                }
            },
            {
                "name": "📊 Social Media Manager",
                "description": "مدیریت خودکار شبکه‌های اجتماعی با برنامه‌ریزی و انتشار محتوا",
                "category": AgentCategory.MARKETING,
                "tags": ["social-media", "marketing", "automation", "content"],
                "author": "پیسان وب",
                "price": 49.99,
                "license_type": LicenseType.PREMIUM,
                "features": [
                    "انتشار خودکار",
                    "تحلیل عملکرد",
                    "پاسخگویی به کامنت‌ها",
                    "برنامه‌ریزی محتوا"
                ]
            },
            {
                "name": "🛒 E-commerce Assistant",
                "description": "دستیار فروش آنلاین با قابلیت‌های پیشرفته مدیریت محصولات",
                "category": AgentCategory.ECOMMERCE,
                "tags": ["ecommerce", "sales", "inventory", "automation"],
                "author": "پیسان وب",
                "price": 79.99,
                "license_type": LicenseType.ENTERPRISE,
                "features": [
                    "مدیریت موجودی",
                    "پیش‌بینی فروش",
                    "بهینه‌سازی قیمت",
                    "تحلیل مشتریان"
                ]
            },
            {
                "name": "📧 Email Marketing Automation",
                "description": "سیستم بازاریابی ایمیلی خودکار با قابلیت‌های شخصی‌سازی",
                "category": AgentCategory.MARKETING,
                "tags": ["email", "marketing", "automation", "personalization"],
                "author": "پیسان وب",
                "price": 39.99,
                "license_type": LicenseType.PREMIUM,
                "features": [
                    "شخصی‌سازی ایمیل‌ها",
                    "برنامه‌ریزی ارسال",
                    "تحلیل بازگشایی",
                    "A/B Testing"
                ]
            },
            {
                "name": "🔍 Data Analytics Agent",
                "description": "تحلیلگر داده‌های پیشرفته با قابلیت‌های گزارش‌گیری",
                "category": AgentCategory.ANALYTICS,
                "tags": ["analytics", "data", "reporting", "insights"],
                "author": "پیسان وب",
                "price": 99.99,
                "license_type": LicenseType.ENTERPRISE,
                "features": [
                    "تحلیل داده‌های پیچیده",
                    "گزارش‌گیری خودکار",
                    "پیش‌بینی روندها",
                    "داشبورد تعاملی"
                ]
            },
            {
                "name": "🌐 API Integration Hub",
                "description": "مرکز یکپارچه‌سازی API های مختلف با قابلیت‌های پیشرفته",
                "category": AgentCategory.INTEGRATION,
                "tags": ["api", "integration", "automation", "webhook"],
                "author": "پیسان وب",
                "price": 59.99,
                "license_type": LicenseType.PREMIUM,
                "features": [
                    "اتصال به 100+ API",
                    "تبدیل داده‌ها",
                    "مدیریت خطاها",
                    "مانیتورینگ Real-time"
                ]
            }
        ]
        
        for agent_data in sample_agents:
            agent_id = str(uuid.uuid4())
            agent = AgentMetadata(
                id=agent_id,
                name=agent_data["name"],
                description=agent_data["description"],
                category=agent_data["category"],
                tags=agent_data["tags"],
                author=agent_data["author"],
                author_id="peysanweb",
                price=agent_data["price"],
                license_type=agent_data["license_type"],
                features=agent_data["features"],
                workflow_data=agent_data.get("workflow_data", {}),
                status=AgentStatus.PUBLISHED,
                downloads=0,
                rating=4.5,
                reviews_count=0
            )
            self.agents[agent_id] = agent
        
        self._save_data()
    
    def publish_agent(self, agent_data: Dict, author_id: str) -> str:
        """
        انتشار Agent جدید
        
        Args:
            agent_data: داده‌های Agent
            author_id: شناسه نویسنده
            
        Returns:
            شناسه Agent
        """
        agent_id = str(uuid.uuid4())
        
        agent = AgentMetadata(
            id=agent_id,
            name=agent_data["name"],
            description=agent_data["description"],
            category=AgentCategory(agent_data["category"]),
            tags=agent_data.get("tags", []),
            author=agent_data.get("author", ""),
            author_id=author_id,
            price=agent_data.get("price", 0.0),
            license_type=LicenseType(agent_data.get("license_type", "free")),
            features=agent_data.get("features", []),
            workflow_data=agent_data.get("workflow_data", {}),
            status=AgentStatus.PUBLISHED,
            thumbnail_url=agent_data.get("thumbnail_url", ""),
            demo_url=agent_data.get("demo_url", ""),
            documentation_url=agent_data.get("documentation_url", ""),
            source_code_url=agent_data.get("source_code_url", ""),
            requirements=agent_data.get("requirements", [])
        )
        
        self.agents[agent_id] = agent
        self._save_data()
        
        self.logger.info(f"Agent published: {agent_id}")
        return agent_id
    
    def update_agent(self, agent_id: str, updates: Dict, author_id: str) -> bool:
        """
        به‌روزرسانی Agent
        
        Args:
            agent_id: شناسه Agent
            updates: تغییرات
            author_id: شناسه نویسنده
            
        Returns:
            موفقیت به‌روزرسانی
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        
        # بررسی مجوز ویرایش
        if agent.author_id != author_id:
            return False
        
        # اعمال تغییرات
        for key, value in updates.items():
            if hasattr(agent, key):
                if key in ["category", "license_type", "status"]:
                    setattr(agent, key, type(getattr(agent, key))(value))
                else:
                    setattr(agent, key, value)
        
        agent.updated_at = datetime.now()
        self._save_data()
        
        return True
    
    def delete_agent(self, agent_id: str, author_id: str) -> bool:
        """
        حذف Agent
        
        Args:
            agent_id: شناسه Agent
            author_id: شناسه نویسنده
            
        Returns:
            موفقیت حذف
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        
        # بررسی مجوز حذف
        if agent.author_id != author_id:
            return False
        
        # حذف Agent
        del self.agents[agent_id]
        
        # حذف نظرات مرتبط
        reviews_to_delete = [rid for rid, review in self.reviews.items() if review.agent_id == agent_id]
        for rid in reviews_to_delete:
            del self.reviews[rid]
        
        self._save_data()
        return True
    
    def search_agents(self, query: str = "", category: str = "", 
                     price_min: float = 0, price_max: float = float('inf'),
                     rating_min: float = 0, tags: List[str] = None) -> List[Dict]:
        """
        جستجوی Agent ها
        
        Args:
            query: عبارت جستجو
            category: دسته‌بندی
            price_min: حداقل قیمت
            price_max: حداکثر قیمت
            rating_min: حداقل امتیاز
            tags: تگ‌ها
            
        Returns:
            لیست Agent های یافت شده
        """
        results = []
        
        for agent in self.agents.values():
            if agent.status != AgentStatus.PUBLISHED:
                continue
            
            # فیلتر دسته‌بندی
            if category and agent.category.value != category:
                continue
            
            # فیلتر قیمت
            if agent.price < price_min or agent.price > price_max:
                continue
            
            # فیلتر امتیاز
            if agent.rating < rating_min:
                continue
            
            # فیلتر تگ‌ها
            if tags and not any(tag in agent.tags for tag in tags):
                continue
            
            # فیلتر جستجو
            if query:
                query_lower = query.lower()
                if not (query_lower in agent.name.lower() or 
                       query_lower in agent.description.lower() or
                       any(query_lower in tag.lower() for tag in agent.tags)):
                    continue
            
            results.append({
                "id": agent.id,
                "name": agent.name,
                "description": agent.description,
                "category": agent.category.value,
                "tags": agent.tags,
                "author": agent.author,
                "price": agent.price,
                "currency": agent.currency,
                "license_type": agent.license_type.value,
                "rating": agent.rating,
                "reviews_count": agent.reviews_count,
                "downloads": agent.downloads,
                "thumbnail_url": agent.thumbnail_url,
                "demo_url": agent.demo_url,
                "created_at": agent.created_at.isoformat(),
                "updated_at": agent.updated_at.isoformat()
            })
        
        # مرتب‌سازی بر اساس محبوبیت
        results.sort(key=lambda x: (x["rating"], x["downloads"]), reverse=True)
        
        return results
    
    def get_agent_details(self, agent_id: str) -> Optional[Dict]:
        """دریافت جزئیات Agent"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        
        # دریافت نظرات
        agent_reviews = [r for r in self.reviews.values() if r.agent_id == agent_id]
        
        return {
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "category": agent.category.value,
            "tags": agent.tags,
            "version": agent.version,
            "author": agent.author,
            "author_id": agent.author_id,
            "created_at": agent.created_at.isoformat(),
            "updated_at": agent.updated_at.isoformat(),
            "status": agent.status.value,
            "license_type": agent.license_type.value,
            "price": agent.price,
            "currency": agent.currency,
            "downloads": agent.downloads,
            "rating": agent.rating,
            "reviews_count": agent.reviews_count,
            "thumbnail_url": agent.thumbnail_url,
            "demo_url": agent.demo_url,
            "documentation_url": agent.documentation_url,
            "source_code_url": agent.source_code_url,
            "requirements": agent.requirements,
            "features": agent.features,
            "screenshots": agent.screenshots,
            "reviews": [
                {
                    "id": review.id,
                    "user_name": review.user_name,
                    "rating": review.rating,
                    "title": review.title,
                    "comment": review.comment,
                    "created_at": review.created_at.isoformat(),
                    "helpful_count": review.helpful_count,
                    "verified_purchase": review.verified_purchase
                }
                for review in agent_reviews
            ]
        }
    
    def add_review(self, agent_id: str, user_id: str, user_name: str, 
                   rating: int, title: str, comment: str) -> str:
        """
        اضافه کردن نظر
        
        Args:
            agent_id: شناسه Agent
            user_id: شناسه کاربر
            user_name: نام کاربر
            rating: امتیاز (1-5)
            title: عنوان نظر
            comment: متن نظر
            
        Returns:
            شناسه نظر
        """
        if agent_id not in self.agents:
            raise ValueError("Agent not found")
        
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        review_id = str(uuid.uuid4())
        
        # بررسی خرید قبلی
        verified_purchase = any(
            p.agent_id == agent_id and p.user_id == user_id and p.status == "completed"
            for p in self.purchases.values()
        )
        
        review = Review(
            id=review_id,
            agent_id=agent_id,
            user_id=user_id,
            user_name=user_name,
            rating=rating,
            title=title,
            comment=comment,
            verified_purchase=verified_purchase
        )
        
        self.reviews[review_id] = review
        
        # به‌روزرسانی امتیاز Agent
        self._update_agent_rating(agent_id)
        
        self._save_data()
        return review_id
    
    def _update_agent_rating(self, agent_id: str):
        """به‌روزرسانی امتیاز Agent"""
        agent_reviews = [r for r in self.reviews.values() if r.agent_id == agent_id]
        
        if agent_reviews:
            total_rating = sum(r.rating for r in agent_reviews)
            avg_rating = total_rating / len(agent_reviews)
            
            agent = self.agents[agent_id]
            agent.rating = round(avg_rating, 1)
            agent.reviews_count = len(agent_reviews)
    
    def purchase_agent(self, agent_id: str, user_id: str, user_name: str, 
                      license_type: str = "premium") -> str:
        """
        خرید Agent
        
        Args:
            agent_id: شناسه Agent
            user_id: شناسه کاربر
            user_name: نام کاربر
            license_type: نوع لایسنس
            
        Returns:
            شناسه خرید
        """
        if agent_id not in self.agents:
            raise ValueError("Agent not found")
        
        agent = self.agents[agent_id]
        
        # محاسبه قیمت
        price = agent.price
        if agent.license_type == LicenseType.FREE:
            price = 0.0
        
        purchase_id = str(uuid.uuid4())
        
        # محاسبه تاریخ انقضا
        expires_at = None
        if license_type == "premium":
            expires_at = datetime.now() + timedelta(days=365)
        elif license_type == "enterprise":
            expires_at = datetime.now() + timedelta(days=365 * 2)
        
        purchase = Purchase(
            id=purchase_id,
            agent_id=agent_id,
            user_id=user_id,
            user_name=user_name,
            price=price,
            currency=agent.currency,
            license_type=LicenseType(license_type),
            expires_at=expires_at
        )
        
        self.purchases[purchase_id] = purchase
        
        # افزایش تعداد دانلود
        agent.downloads += 1
        
        self._save_data()
        return purchase_id
    
    def get_user_purchases(self, user_id: str) -> List[Dict]:
        """دریافت خریدهای کاربر"""
        user_purchases = [p for p in self.purchases.values() if p.user_id == user_id]
        
        return [
            {
                "id": purchase.id,
                "agent_id": purchase.agent_id,
                "agent_name": self.agents[purchase.agent_id].name if purchase.agent_id in self.agents else "Unknown",
                "price": purchase.price,
                "currency": purchase.currency,
                "license_type": purchase.license_type.value,
                "purchase_date": purchase.purchase_date.isoformat(),
                "expires_at": purchase.expires_at.isoformat() if purchase.expires_at else None,
                "status": purchase.status
            }
            for purchase in user_purchases
        ]
    
    def get_marketplace_stats(self) -> Dict:
        """دریافت آمار بازار"""
        total_agents = len(self.agents)
        published_agents = len([a for a in self.agents.values() if a.status == AgentStatus.PUBLISHED])
        total_reviews = len(self.reviews)
        total_purchases = len(self.purchases)
        total_revenue = sum(p.price for p in self.purchases.values() if p.status == "completed")
        
        # آمار بر اساس دسته‌بندی
        category_stats = {}
        for agent in self.agents.values():
            category = agent.category.value
            if category not in category_stats:
                category_stats[category] = {"count": 0, "revenue": 0}
            category_stats[category]["count"] += 1
            
            # محاسبه درآمد
            agent_purchases = [p for p in self.purchases.values() if p.agent_id == agent.id]
            category_stats[category]["revenue"] += sum(p.price for p in agent_purchases)
        
        # محبوب‌ترین Agent ها
        top_agents = sorted(
            self.agents.values(),
            key=lambda x: (x.downloads, x.rating),
            reverse=True
        )[:10]
        
        return {
            "total_agents": total_agents,
            "published_agents": published_agents,
            "total_reviews": total_reviews,
            "total_purchases": total_purchases,
            "total_revenue": total_revenue,
            "category_stats": category_stats,
            "top_agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "downloads": agent.downloads,
                    "rating": agent.rating,
                    "price": agent.price
                }
                for agent in top_agents
            ]
        }
    
    def get_agent_categories(self) -> List[Dict]:
        """دریافت دسته‌بندی‌ها"""
        categories = []
        for category in AgentCategory:
            agents_in_category = [a for a in self.agents.values() if a.category == category and a.status == AgentStatus.PUBLISHED]
            categories.append({
                "value": category.value,
                "name": category.value.replace("_", " ").title(),
                "count": len(agents_in_category),
                "description": self._get_category_description(category)
            })
        
        return categories
    
    def _get_category_description(self, category: AgentCategory) -> str:
        """دریافت توضیحات دسته‌بندی"""
        descriptions = {
            AgentCategory.AUTOMATION: "Agent های خودکارسازی فرآیندها",
            AgentCategory.AI_ASSISTANT: "دستیاران هوشمند AI",
            AgentCategory.DATA_PROCESSING: "پردازش و تحلیل داده‌ها",
            AgentCategory.COMMUNICATION: "ابزارهای ارتباطی و پیام‌رسانی",
            AgentCategory.ECOMMERCE: "ابزارهای تجارت الکترونیک",
            AgentCategory.MARKETING: "ابزارهای بازاریابی و تبلیغات",
            AgentCategory.CUSTOMER_SERVICE: "خدمات مشتریان و پشتیبانی",
            AgentCategory.ANALYTICS: "تحلیل و گزارش‌گیری",
            AgentCategory.INTEGRATION: "یکپارچه‌سازی و اتصال سیستم‌ها",
            AgentCategory.CUSTOM: "Agent های سفارشی"
        }
        return descriptions.get(category, "دسته‌بندی عمومی")

# مثال استفاده
if __name__ == "__main__":
    marketplace = AgentMarketplace()
    
    # جستجوی Agent ها
    results = marketplace.search_agents(query="customer service", category="customer_service")
    print(f"Found {len(results)} agents")
    
    # دریافت جزئیات Agent
    if results:
        agent_details = marketplace.get_agent_details(results[0]["id"])
        print(f"Agent: {agent_details['name']}")
        print(f"Rating: {agent_details['rating']}")
        print(f"Price: ${agent_details['price']}")
    
    # آمار بازار
    stats = marketplace.get_marketplace_stats()
    print(f"Total agents: {stats['total_agents']}")
    print(f"Total revenue: ${stats['total_revenue']}")
    
    # دسته‌بندی‌ها
    categories = marketplace.get_agent_categories()
    for category in categories:
        print(f"{category['name']}: {category['count']} agents")
