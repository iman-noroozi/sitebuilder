#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monetization System - Multiple revenue streams for global platform
Features that generate revenue while providing value to users
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
import hashlib
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RevenueStream(Enum):
    """Types of revenue streams"""
    SUBSCRIPTION = "subscription"
    MARKETPLACE = "marketplace"
    PREMIUM_FEATURES = "premium_features"
    AFFILIATE = "affiliate"
    ADVERTISING = "advertising"
    CONSULTING = "consulting"
    WHITELABEL = "whitelabel"
    API_ACCESS = "api_access"
    CUSTOM_DEVELOPMENT = "custom_development"
    TRAINING = "training"

class SubscriptionTier(Enum):
    """Subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    VIP = "vip"

@dataclass
class Subscription:
    """Subscription data"""
    user_id: str
    tier: SubscriptionTier
    start_date: datetime
    end_date: datetime
    price: float
    currency: str
    features: List[str]
    is_active: bool = True

@dataclass
class MarketplaceItem:
    """Marketplace item"""
    id: str
    seller_id: str
    name: str
    description: str
    price: float
    currency: str
    category: str
    tags: List[str]
    downloads: int = 0
    rating: float = 0.0
    revenue_share: float = 0.3  # 30% to platform

class MonetizationSystem:
    """Comprehensive monetization system for global platform"""
    
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {}
        self.marketplace_items: Dict[str, MarketplaceItem] = {}
        self.revenue_tracking: Dict[str, List[Dict]] = {}
        self.affiliate_programs: Dict[str, Dict] = {}
        self.advertising_spaces: Dict[str, Dict] = {}
        
        # Initialize monetization features
        self._initialize_subscription_tiers()
        self._initialize_marketplace_categories()
        self._initialize_affiliate_programs()
        
        logger.info("Monetization System initialized")
    
    def _initialize_subscription_tiers(self):
        """Initialize subscription tiers and pricing"""
        self.subscription_tiers = {
            SubscriptionTier.FREE: {
                "name": "Free",
                "price": 0.0,
                "currency": "USD",
                "features": [
                    "Basic website builder",
                    "5 AI content generations per month",
                    "Basic templates",
                    "Community support",
                    "1 project"
                ],
                "limits": {
                    "websites": 1,
                    "ai_content": 5,
                    "collaborators": 1,
                    "storage": "100MB"
                }
            },
            SubscriptionTier.BASIC: {
                "name": "Basic",
                "price": 9.99,
                "currency": "USD",
                "features": [
                    "Advanced website builder",
                    "50 AI content generations per month",
                    "Premium templates",
                    "Email support",
                    "5 projects",
                    "Basic analytics"
                ],
                "limits": {
                    "websites": 5,
                    "ai_content": 50,
                    "collaborators": 3,
                    "storage": "1GB"
                }
            },
            SubscriptionTier.PRO: {
                "name": "Pro",
                "price": 29.99,
                "currency": "USD",
                "features": [
                    "Professional website builder",
                    "Unlimited AI content",
                    "All templates",
                    "Priority support",
                    "Unlimited projects",
                    "Advanced analytics",
                    "Voice commands",
                    "Real-time collaboration",
                    "Custom domains"
                ],
                "limits": {
                    "websites": -1,  # Unlimited
                    "ai_content": -1,
                    "collaborators": 10,
                    "storage": "10GB"
                }
            },
            SubscriptionTier.ENTERPRISE: {
                "name": "Enterprise",
                "price": 99.99,
                "currency": "USD",
                "features": [
                    "Enterprise website builder",
                    "Unlimited everything",
                    "White-label options",
                    "Dedicated support",
                    "Custom integrations",
                    "Advanced security",
                    "API access",
                    "Custom training",
                    "Revenue sharing"
                ],
                "limits": {
                    "websites": -1,
                    "ai_content": -1,
                    "collaborators": -1,
                    "storage": "100GB"
                }
            },
            SubscriptionTier.VIP: {
                "name": "VIP",
                "price": 299.99,
                "currency": "USD",
                "features": [
                    "VIP website builder",
                    "Personal AI assistant",
                    "Exclusive templates",
                    "24/7 phone support",
                    "Custom development",
                    "Revenue sharing (50%)",
                    "Early access features",
                    "Personal consultant",
                    "Global marketplace access"
                ],
                "limits": {
                    "websites": -1,
                    "ai_content": -1,
                    "collaborators": -1,
                    "storage": "1TB"
                }
            }
        }
    
    def _initialize_marketplace_categories(self):
        """Initialize marketplace categories"""
        self.marketplace_categories = {
            "templates": {
                "name": "Website Templates",
                "description": "Professional website templates",
                "revenue_share": 0.3,
                "popular_tags": ["modern", "responsive", "business", "portfolio"]
            },
            "components": {
                "name": "UI Components",
                "description": "Reusable UI components",
                "revenue_share": 0.25,
                "popular_tags": ["button", "form", "navigation", "card"]
            },
            "ai_content": {
                "name": "AI Content Packs",
                "description": "AI-generated content libraries",
                "revenue_share": 0.4,
                "popular_tags": ["copywriting", "seo", "marketing", "blog"]
            },
            "plugins": {
                "name": "Plugins & Extensions",
                "description": "Functionality extensions",
                "revenue_share": 0.35,
                "popular_tags": ["analytics", "seo", "social", "ecommerce"]
            },
            "themes": {
                "name": "Themes & Styles",
                "description": "Visual themes and styles",
                "revenue_share": 0.3,
                "popular_tags": ["dark", "light", "colorful", "minimal"]
            },
            "tutorials": {
                "name": "Tutorials & Courses",
                "description": "Educational content",
                "revenue_share": 0.5,
                "popular_tags": ["beginner", "advanced", "video", "guide"]
            }
        }
    
    def _initialize_affiliate_programs(self):
        """Initialize affiliate programs"""
        self.affiliate_programs = {
            "referral": {
                "name": "Referral Program",
                "commission_rate": 0.3,  # 30% of first payment
                "cookie_duration": 30,  # days
                "minimum_payout": 50.0,
                "payout_methods": ["paypal", "bank_transfer", "crypto"]
            },
            "content_creator": {
                "name": "Content Creator Program",
                "commission_rate": 0.25,
                "cookie_duration": 60,
                "minimum_payout": 100.0,
                "requirements": ["youtube_channel", "blog", "social_media"]
            },
            "developer": {
                "name": "Developer Partner Program",
                "commission_rate": 0.4,
                "cookie_duration": 90,
                "minimum_payout": 200.0,
                "requirements": ["technical_skills", "portfolio", "github"]
            },
            "enterprise": {
                "name": "Enterprise Partner Program",
                "commission_rate": 0.5,
                "cookie_duration": 180,
                "minimum_payout": 1000.0,
                "requirements": ["enterprise_network", "sales_team", "certification"]
            }
        }
    
    # 1. Subscription Management
    def create_subscription(self, user_id: str, tier: SubscriptionTier, duration_months: int = 1) -> Dict:
        """Create new subscription"""
        tier_info = self.subscription_tiers[tier]
        
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_months * 30)
        
        subscription = Subscription(
            user_id=user_id,
            tier=tier,
            start_date=start_date,
            end_date=end_date,
            price=tier_info["price"] * duration_months,
            currency=tier_info["currency"],
            features=tier_info["features"]
        )
        
        self.subscriptions[user_id] = subscription
        
        # Track revenue
        self._track_revenue(RevenueStream.SUBSCRIPTION, subscription.price, {
            "user_id": user_id,
            "tier": tier.value,
            "duration_months": duration_months
        })
        
        return {
            "subscription_id": user_id,
            "tier": tier.value,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "price": subscription.price,
            "currency": subscription.currency,
            "features": subscription.features
        }
    
    def get_subscription_info(self, user_id: str) -> Dict:
        """Get user subscription information"""
        if user_id not in self.subscriptions:
            return {"tier": "free", "features": self.subscription_tiers[SubscriptionTier.FREE]["features"]}
        
        subscription = self.subscriptions[user_id]
        return {
            "tier": subscription.tier.value,
            "features": subscription.features,
            "is_active": subscription.is_active,
            "end_date": subscription.end_date.isoformat(),
            "days_remaining": (subscription.end_date - datetime.now()).days
        }
    
    def upgrade_subscription(self, user_id: str, new_tier: SubscriptionTier) -> Dict:
        """Upgrade user subscription"""
        current_sub = self.subscriptions.get(user_id)
        
        if current_sub:
            # Calculate prorated amount
            remaining_days = (current_sub.end_date - datetime.now()).days
            if remaining_days > 0:
                current_tier_info = self.subscription_tiers[current_sub.tier]
                new_tier_info = self.subscription_tiers[new_tier]
                
                # Calculate upgrade cost
                upgrade_cost = (new_tier_info["price"] - current_tier_info["price"]) * (remaining_days / 30)
                
                # Update subscription
                current_sub.tier = new_tier
                current_sub.features = new_tier_info["features"]
                
                # Track revenue
                self._track_revenue(RevenueStream.SUBSCRIPTION, upgrade_cost, {
                    "user_id": user_id,
                    "upgrade_from": current_sub.tier.value,
                    "upgrade_to": new_tier.value
                })
                
                return {
                    "upgraded": True,
                    "new_tier": new_tier.value,
                    "upgrade_cost": upgrade_cost,
                    "new_features": new_tier_info["features"]
                }
        
        return {"error": "No active subscription found"}
    
    # 2. Marketplace System
    def list_marketplace_item(self, seller_id: str, item_data: Dict) -> Dict:
        """List item in marketplace"""
        item_id = str(uuid.uuid4())
        
        item = MarketplaceItem(
            id=item_id,
            seller_id=seller_id,
            name=item_data["name"],
            description=item_data["description"],
            price=item_data["price"],
            currency=item_data.get("currency", "USD"),
            category=item_data["category"],
            tags=item_data.get("tags", [])
        )
        
        self.marketplace_items[item_id] = item
        
        return {
            "item_id": item_id,
            "marketplace_url": f"https://sitebuilder.com/marketplace/{item_id}",
            "item": item
        }
    
    def purchase_marketplace_item(self, buyer_id: str, item_id: str) -> Dict:
        """Purchase marketplace item"""
        if item_id not in self.marketplace_items:
            return {"error": "Item not found"}
        
        item = self.marketplace_items[item_id]
        
        # Calculate revenue split
        platform_revenue = item.price * item.revenue_share
        seller_revenue = item.price * (1 - item.revenue_share)
        
        # Update item stats
        item.downloads += 1
        
        # Track revenue
        self._track_revenue(RevenueStream.MARKETPLACE, platform_revenue, {
            "item_id": item_id,
            "seller_id": item.seller_id,
            "buyer_id": buyer_id,
            "item_price": item.price
        })
        
        return {
            "purchase_id": str(uuid.uuid4()),
            "item": item,
            "platform_revenue": platform_revenue,
            "seller_revenue": seller_revenue,
            "download_url": f"https://sitebuilder.com/download/{item_id}"
        }
    
    def get_marketplace_items(self, category: str = None, limit: int = 20) -> List[Dict]:
        """Get marketplace items"""
        items = list(self.marketplace_items.values())
        
        if category:
            items = [item for item in items if item.category == category]
        
        # Sort by popularity (downloads * rating)
        items.sort(key=lambda x: x.downloads * x.rating, reverse=True)
        
        return [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "currency": item.currency,
                "category": item.category,
                "tags": item.tags,
                "downloads": item.downloads,
                "rating": item.rating,
                "seller_id": item.seller_id
            }
            for item in items[:limit]
        ]
    
    # 3. Affiliate Program
    def join_affiliate_program(self, user_id: str, program_type: str) -> Dict:
        """Join affiliate program"""
        if program_type not in self.affiliate_programs:
            return {"error": "Program not found"}
        
        program = self.affiliate_programs[program_type]
        affiliate_id = str(uuid.uuid4())
        
        return {
            "affiliate_id": affiliate_id,
            "program": program_type,
            "commission_rate": program["commission_rate"],
            "affiliate_link": f"https://sitebuilder.com/ref/{affiliate_id}",
            "dashboard_url": f"https://sitebuilder.com/affiliate/{affiliate_id}",
            "requirements": program.get("requirements", [])
        }
    
    def track_affiliate_conversion(self, affiliate_id: str, user_id: str, amount: float) -> Dict:
        """Track affiliate conversion"""
        # Find affiliate program
        program_type = None
        for prog_type, program in self.affiliate_programs.items():
            if affiliate_id in program.get("affiliates", []):
                program_type = prog_type
                break
        
        if not program_type:
            return {"error": "Invalid affiliate ID"}
        
        program = self.affiliate_programs[program_type]
        commission = amount * program["commission_rate"]
        
        # Track revenue
        self._track_revenue(RevenueStream.AFFILIATE, commission, {
            "affiliate_id": affiliate_id,
            "user_id": user_id,
            "conversion_amount": amount,
            "commission": commission
        })
        
        return {
            "conversion_tracked": True,
            "commission": commission,
            "payout_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
    
    # 4. Premium Features
    def unlock_premium_feature(self, user_id: str, feature_name: str) -> Dict:
        """Unlock premium feature"""
        premium_features = {
            "ai_content_pro": {
                "name": "AI Content Pro",
                "price": 19.99,
                "description": "Advanced AI content generation with custom models"
            },
            "voice_commands_pro": {
                "name": "Voice Commands Pro",
                "price": 14.99,
                "description": "Advanced voice recognition and commands"
            },
            "collaboration_pro": {
                "name": "Collaboration Pro",
                "price": 24.99,
                "description": "Advanced real-time collaboration features"
            },
            "security_pro": {
                "name": "Security Pro",
                "price": 29.99,
                "description": "Advanced security and compliance features"
            },
            "analytics_pro": {
                "name": "Analytics Pro",
                "price": 9.99,
                "description": "Advanced analytics and reporting"
            }
        }
        
        if feature_name not in premium_features:
            return {"error": "Feature not found"}
        
        feature = premium_features[feature_name]
        
        # Track revenue
        self._track_revenue(RevenueStream.PREMIUM_FEATURES, feature["price"], {
            "user_id": user_id,
            "feature": feature_name
        })
        
        return {
            "feature_unlocked": True,
            "feature_name": feature["name"],
            "price": feature["price"],
            "description": feature["description"],
            "unlock_date": datetime.now().isoformat()
        }
    
    # 5. API Access
    def create_api_access(self, user_id: str, plan: str) -> Dict:
        """Create API access for user"""
        api_plans = {
            "basic": {
                "name": "API Basic",
                "price": 49.99,
                "requests_per_month": 10000,
                "features": ["REST API", "Basic endpoints", "Documentation"]
            },
            "pro": {
                "name": "API Pro",
                "price": 149.99,
                "requests_per_month": 100000,
                "features": ["REST API", "All endpoints", "Webhooks", "Priority support"]
            },
            "enterprise": {
                "name": "API Enterprise",
                "price": 499.99,
                "requests_per_month": -1,  # Unlimited
                "features": ["REST API", "All endpoints", "Webhooks", "Dedicated support", "Custom endpoints"]
            }
        }
        
        if plan not in api_plans:
            return {"error": "API plan not found"}
        
        api_plan = api_plans[plan]
        api_key = self._generate_api_key(user_id)
        
        # Track revenue
        self._track_revenue(RevenueStream.API_ACCESS, api_plan["price"], {
            "user_id": user_id,
            "plan": plan
        })
        
        return {
            "api_key": api_key,
            "plan": plan,
            "plan_details": api_plan,
            "activation_date": datetime.now().isoformat()
        }
    
    def _generate_api_key(self, user_id: str) -> str:
        """Generate API key"""
        return hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()
    
    # 6. White-label Solutions
    def create_whitelabel_solution(self, client_id: str, solution_data: Dict) -> Dict:
        """Create white-label solution"""
        solution_id = str(uuid.uuid4())
        
        # Calculate pricing based on features
        base_price = 999.99
        feature_prices = {
            "custom_branding": 299.99,
            "custom_domain": 199.99,
            "custom_features": 499.99,
            "dedicated_support": 399.99,
            "custom_integrations": 799.99
        }
        
        total_price = base_price
        for feature in solution_data.get("features", []):
            total_price += feature_prices.get(feature, 0)
        
        # Track revenue
        self._track_revenue(RevenueStream.WHITELABEL, total_price, {
            "client_id": client_id,
            "solution_id": solution_id,
            "features": solution_data.get("features", [])
        })
        
        return {
            "solution_id": solution_id,
            "client_id": client_id,
            "total_price": total_price,
            "features": solution_data.get("features", []),
            "delivery_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "support_duration": "12 months"
        }
    
    # 7. Training and Consulting
    def book_training_session(self, user_id: str, training_type: str) -> Dict:
        """Book training session"""
        training_types = {
            "basic": {
                "name": "Basic Training",
                "price": 99.99,
                "duration": "2 hours",
                "topics": ["Website building basics", "AI content", "Templates"]
            },
            "advanced": {
                "name": "Advanced Training",
                "price": 199.99,
                "duration": "4 hours",
                "topics": ["Advanced features", "Custom development", "API usage"]
            },
            "enterprise": {
                "name": "Enterprise Training",
                "price": 499.99,
                "duration": "8 hours",
                "topics": ["Team collaboration", "Security", "Scalability"]
            }
        }
        
        if training_type not in training_types:
            return {"error": "Training type not found"}
        
        training = training_types[training_type]
        
        # Track revenue
        self._track_revenue(RevenueStream.TRAINING, training["price"], {
            "user_id": user_id,
            "training_type": training_type
        })
        
        return {
            "session_id": str(uuid.uuid4()),
            "training_type": training_type,
            "training_details": training,
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "instructor": "Expert Trainer"
        }
    
    def book_consulting_session(self, user_id: str, consulting_type: str) -> Dict:
        """Book consulting session"""
        consulting_types = {
            "strategy": {
                "name": "Strategy Consulting",
                "price": 299.99,
                "duration": "2 hours",
                "focus": "Business strategy and planning"
            },
            "technical": {
                "name": "Technical Consulting",
                "price": 399.99,
                "duration": "3 hours",
                "focus": "Technical implementation and optimization"
            },
            "marketing": {
                "name": "Marketing Consulting",
                "price": 249.99,
                "duration": "2 hours",
                "focus": "Digital marketing and SEO"
            }
        }
        
        if consulting_type not in consulting_types:
            return {"error": "Consulting type not found"}
        
        consulting = consulting_types[consulting_type]
        
        # Track revenue
        self._track_revenue(RevenueStream.CONSULTING, consulting["price"], {
            "user_id": user_id,
            "consulting_type": consulting_type
        })
        
        return {
            "session_id": str(uuid.uuid4()),
            "consulting_type": consulting_type,
            "consulting_details": consulting,
            "scheduled_date": (datetime.now() + timedelta(days=3)).isoformat(),
            "consultant": "Senior Consultant"
        }
    
    # 8. Revenue Tracking
    def _track_revenue(self, stream: RevenueStream, amount: float, metadata: Dict):
        """Track revenue from different streams"""
        revenue_entry = {
            "id": str(uuid.uuid4()),
            "stream": stream.value,
            "amount": amount,
            "currency": "USD",
            "timestamp": datetime.now(),
            "metadata": metadata
        }
        
        if stream.value not in self.revenue_tracking:
            self.revenue_tracking[stream.value] = []
        
        self.revenue_tracking[stream.value].append(revenue_entry)
    
    def get_revenue_analytics(self, days: int = 30) -> Dict:
        """Get revenue analytics"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        total_revenue = 0
        revenue_by_stream = {}
        revenue_by_day = {}
        
        for stream, entries in self.revenue_tracking.items():
            stream_revenue = 0
            for entry in entries:
                if entry["timestamp"] > cutoff_date:
                    stream_revenue += entry["amount"]
                    total_revenue += entry["amount"]
                    
                    # Group by day
                    day = entry["timestamp"].strftime("%Y-%m-%d")
                    if day not in revenue_by_day:
                        revenue_by_day[day] = 0
                    revenue_by_day[day] += entry["amount"]
            
            revenue_by_stream[stream] = stream_revenue
        
        return {
            "period_days": days,
            "total_revenue": total_revenue,
            "revenue_by_stream": revenue_by_stream,
            "revenue_by_day": revenue_by_day,
            "top_revenue_stream": max(revenue_by_stream.items(), key=lambda x: x[1])[0] if revenue_by_stream else None
        }
    
    def get_platform_metrics(self) -> Dict:
        """Get platform business metrics"""
        total_subscriptions = len(self.subscriptions)
        active_subscriptions = len([s for s in self.subscriptions.values() if s.is_active])
        
        total_marketplace_items = len(self.marketplace_items)
        total_marketplace_revenue = sum(
            sum(entry["amount"] for entry in entries)
            for entries in self.revenue_tracking.get("marketplace", [])
        )
        
        return {
            "total_subscriptions": total_subscriptions,
            "active_subscriptions": active_subscriptions,
            "subscription_revenue": sum(
                sum(entry["amount"] for entry in entries)
                for entries in self.revenue_tracking.get("subscription", [])
            ),
            "marketplace_items": total_marketplace_items,
            "marketplace_revenue": total_marketplace_revenue,
            "affiliate_programs": len(self.affiliate_programs),
            "revenue_streams": len(self.revenue_tracking),
            "total_revenue": sum(
                sum(entry["amount"] for entries in self.revenue_tracking.values() for entry in entries)
            )
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize monetization system
    monetization = MonetizationSystem()
    
    # Test subscription creation
    print("💳 Testing Subscription System...")
    subscription = monetization.create_subscription("user123", SubscriptionTier.PRO, 1)
    print(f"✅ Created subscription: {subscription['tier']} - ${subscription['price']}")
    
    # Test marketplace
    print("\n🛒 Testing Marketplace...")
    item = monetization.list_marketplace_item("seller123", {
        "name": "AI Portfolio Template",
        "description": "Modern portfolio template with AI integration",
        "price": 29.99,
        "category": "templates",
        "tags": ["portfolio", "AI", "modern"]
    })
    print(f"✅ Listed item: {item['item'].name} - ${item['item'].price}")
    
    purchase = monetization.purchase_marketplace_item("buyer123", item["item_id"])
    print(f"✅ Purchased item: Platform revenue ${purchase['platform_revenue']}")
    
    # Test premium features
    print("\n⭐ Testing Premium Features...")
    feature = monetization.unlock_premium_feature("user123", "ai_content_pro")
    print(f"✅ Unlocked feature: {feature['feature_name']} - ${feature['price']}")
    
    # Test API access
    print("\n🔌 Testing API Access...")
    api_access = monetization.create_api_access("user123", "pro")
    print(f"✅ Created API access: {api_access['plan']} - ${api_access['plan_details']['price']}")
    
    # Test training
    print("\n🎓 Testing Training...")
    training = monetization.book_training_session("user123", "advanced")
    print(f"✅ Booked training: {training['training_details']['name']} - ${training['training_details']['price']}")
    
    # Test revenue analytics
    print("\n📊 Testing Revenue Analytics...")
    analytics = monetization.get_revenue_analytics(30)
    print(f"✅ Total revenue (30 days): ${analytics['total_revenue']}")
    print(f"✅ Revenue by stream: {analytics['revenue_by_stream']}")
    
    # Test platform metrics
    print("\n📈 Testing Platform Metrics...")
    metrics = monetization.get_platform_metrics()
    print(f"✅ Active subscriptions: {metrics['active_subscriptions']}")
    print(f"✅ Total revenue: ${metrics['total_revenue']}")
    
    print("\n🎉 All monetization tests completed successfully!")
