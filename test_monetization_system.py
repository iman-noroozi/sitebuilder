#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for Monetization System
Comprehensive testing for all monetization functionality
"""

import unittest
import json
import time
from datetime import datetime, timedelta
from monetization_system import MonetizationSystem, RevenueStream, SubscriptionTier, Subscription, MarketplaceItem

class TestMonetizationSystem(unittest.TestCase):
    """Test cases for Monetization System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.monetization = MonetizationSystem()
        self.test_user_id = "test_user_123"
        self.test_seller_id = "seller_123"
        self.test_buyer_id = "buyer_123"
    
    def test_subscription_creation(self):
        """Test subscription creation"""
        subscription = self.monetization.create_subscription(
            self.test_user_id, SubscriptionTier.PRO, 1
        )
        
        self.assertEqual(subscription["subscription_id"], self.test_user_id)
        self.assertEqual(subscription["tier"], "pro")
        self.assertEqual(subscription["price"], 29.99)
        self.assertEqual(subscription["currency"], "USD")
        self.assertIn("start_date", subscription)
        self.assertIn("end_date", subscription)
        self.assertIsInstance(subscription["features"], list)
    
    def test_subscription_info(self):
        """Test subscription information retrieval"""
        # Test with no subscription (should return free tier)
        info = self.monetization.get_subscription_info("non_existent_user")
        self.assertEqual(info["tier"], "free")
        self.assertIsInstance(info["features"], list)
        
        # Test with active subscription
        self.monetization.create_subscription(self.test_user_id, SubscriptionTier.BASIC, 1)
        info = self.monetization.get_subscription_info(self.test_user_id)
        self.assertEqual(info["tier"], "basic")
        self.assertTrue(info["is_active"])
        self.assertIn("end_date", info)
        self.assertIn("days_remaining", info)
    
    def test_subscription_upgrade(self):
        """Test subscription upgrade"""
        # Create basic subscription first
        self.monetization.create_subscription(self.test_user_id, SubscriptionTier.BASIC, 1)
        
        # Upgrade to pro
        upgrade_result = self.monetization.upgrade_subscription(
            self.test_user_id, SubscriptionTier.PRO
        )
        
        self.assertTrue(upgrade_result["upgraded"])
        self.assertEqual(upgrade_result["new_tier"], "pro")
        self.assertIn("upgrade_cost", upgrade_result)
        self.assertIn("new_features", upgrade_result)
    
    def test_marketplace_listing(self):
        """Test marketplace item listing"""
        item_data = {
            "name": "Test Template",
            "description": "A test template for testing",
            "price": 29.99,
            "category": "templates",
            "tags": ["test", "template", "demo"]
        }
        
        result = self.monetization.list_marketplace_item(self.test_seller_id, item_data)
        
        self.assertIn("item_id", result)
        self.assertIn("marketplace_url", result)
        self.assertIn("item", result)
        self.assertEqual(result["item"].name, item_data["name"])
        self.assertEqual(result["item"].price, item_data["price"])
    
    def test_marketplace_purchase(self):
        """Test marketplace item purchase"""
        # First list an item
        item_data = {
            "name": "Test Template",
            "description": "A test template for testing",
            "price": 29.99,
            "category": "templates",
            "tags": ["test", "template", "demo"]
        }
        
        list_result = self.monetization.list_marketplace_item(self.test_seller_id, item_data)
        item_id = list_result["item_id"]
        
        # Purchase the item
        purchase_result = self.monetization.purchase_marketplace_item(self.test_buyer_id, item_id)
        
        self.assertIn("purchase_id", purchase_result)
        self.assertIn("item", purchase_result)
        self.assertIn("platform_revenue", purchase_result)
        self.assertIn("seller_revenue", purchase_result)
        self.assertIn("download_url", purchase_result)
        
        # Check revenue split
        expected_platform_revenue = 29.99 * 0.3  # 30% to platform
        expected_seller_revenue = 29.99 * 0.7    # 70% to seller
        self.assertEqual(purchase_result["platform_revenue"], expected_platform_revenue)
        self.assertEqual(purchase_result["seller_revenue"], expected_seller_revenue)
    
    def test_marketplace_items_retrieval(self):
        """Test marketplace items retrieval"""
        # List some items first
        items_data = [
            {
                "name": "Template 1",
                "description": "First template",
                "price": 19.99,
                "category": "templates",
                "tags": ["template1"]
            },
            {
                "name": "Component 1",
                "description": "First component",
                "price": 9.99,
                "category": "components",
                "tags": ["component1"]
            }
        ]
        
        for item_data in items_data:
            self.monetization.list_marketplace_item(self.test_seller_id, item_data)
        
        # Get all items
        all_items = self.monetization.get_marketplace_items()
        self.assertIsInstance(all_items, list)
        self.assertGreaterEqual(len(all_items), 2)
        
        # Get items by category
        template_items = self.monetization.get_marketplace_items("templates")
        self.assertIsInstance(template_items, list)
        
        # Test limit parameter
        limited_items = self.monetization.get_marketplace_items(limit=1)
        self.assertEqual(len(limited_items), 1)
    
    def test_affiliate_program_joining(self):
        """Test affiliate program joining"""
        result = self.monetization.join_affiliate_program(self.test_user_id, "referral")
        
        self.assertIn("affiliate_id", result)
        self.assertEqual(result["program"], "referral")
        self.assertIn("commission_rate", result)
        self.assertIn("affiliate_link", result)
        self.assertIn("dashboard_url", result)
        self.assertIn("requirements", result)
    
    def test_affiliate_conversion_tracking(self):
        """Test affiliate conversion tracking"""
        # Join affiliate program first
        join_result = self.monetization.join_affiliate_program(self.test_user_id, "referral")
        affiliate_id = join_result["affiliate_id"]
        
        # Track conversion
        conversion_result = self.monetization.track_affiliate_conversion(
            affiliate_id, self.test_buyer_id, 100.0
        )
        
        self.assertTrue(conversion_result["conversion_tracked"])
        self.assertIn("commission", conversion_result)
        self.assertIn("payout_date", conversion_result)
        
        # Check commission calculation (30% for referral program)
        expected_commission = 100.0 * 0.3
        self.assertEqual(conversion_result["commission"], expected_commission)
    
    def test_premium_feature_unlock(self):
        """Test premium feature unlocking"""
        result = self.monetization.unlock_premium_feature(self.test_user_id, "ai_content_pro")
        
        self.assertTrue(result["feature_unlocked"])
        self.assertEqual(result["feature_name"], "AI Content Pro")
        self.assertEqual(result["price"], 19.99)
        self.assertIn("description", result)
        self.assertIn("unlock_date", result)
    
    def test_api_access_creation(self):
        """Test API access creation"""
        result = self.monetization.create_api_access(self.test_user_id, "pro")
        
        self.assertIn("api_key", result)
        self.assertEqual(result["plan"], "pro")
        self.assertIn("plan_details", result)
        self.assertIn("activation_date", result)
        
        # Check plan details
        plan_details = result["plan_details"]
        self.assertEqual(plan_details["name"], "API Pro")
        self.assertEqual(plan_details["price"], 149.99)
        self.assertEqual(plan_details["requests_per_month"], 100000)
        self.assertIsInstance(plan_details["features"], list)
    
    def test_whitelabel_solution_creation(self):
        """Test white-label solution creation"""
        solution_data = {
            "features": ["custom_branding", "custom_domain", "dedicated_support"]
        }
        
        result = self.monetization.create_whitelabel_solution(self.test_user_id, solution_data)
        
        self.assertIn("solution_id", result)
        self.assertEqual(result["client_id"], self.test_user_id)
        self.assertIn("total_price", result)
        self.assertIn("features", result)
        self.assertIn("delivery_date", result)
        self.assertIn("support_duration", result)
        
        # Check pricing calculation
        base_price = 999.99
        feature_prices = 299.99 + 199.99 + 399.99  # custom_branding + custom_domain + dedicated_support
        expected_total = base_price + feature_prices
        self.assertEqual(result["total_price"], expected_total)
    
    def test_training_session_booking(self):
        """Test training session booking"""
        result = self.monetization.book_training_session(self.test_user_id, "advanced")
        
        self.assertIn("session_id", result)
        self.assertEqual(result["training_type"], "advanced")
        self.assertIn("training_details", result)
        self.assertIn("scheduled_date", result)
        self.assertIn("instructor", result)
        
        # Check training details
        training_details = result["training_details"]
        self.assertEqual(training_details["name"], "Advanced Training")
        self.assertEqual(training_details["price"], 199.99)
        self.assertEqual(training_details["duration"], "4 hours")
        self.assertIsInstance(training_details["topics"], list)
    
    def test_consulting_session_booking(self):
        """Test consulting session booking"""
        result = self.monetization.book_consulting_session(self.test_user_id, "strategy")
        
        self.assertIn("session_id", result)
        self.assertEqual(result["consulting_type"], "strategy")
        self.assertIn("consulting_details", result)
        self.assertIn("scheduled_date", result)
        self.assertIn("consultant", result)
        
        # Check consulting details
        consulting_details = result["consulting_details"]
        self.assertEqual(consulting_details["name"], "Strategy Consulting")
        self.assertEqual(consulting_details["price"], 299.99)
        self.assertEqual(consulting_details["duration"], "2 hours")
        self.assertIn("focus", consulting_details)
    
    def test_revenue_tracking(self):
        """Test revenue tracking"""
        # Generate some revenue
        self.monetization.create_subscription(self.test_user_id, SubscriptionTier.PRO, 1)
        self.monetization.unlock_premium_feature(self.test_user_id, "ai_content_pro")
        
        # Check revenue tracking
        subscription_revenue = self.monetization.revenue_tracking.get("subscription", [])
        premium_revenue = self.monetization.revenue_tracking.get("premium_features", [])
        
        self.assertGreater(len(subscription_revenue), 0)
        self.assertGreater(len(premium_revenue), 0)
        
        # Check revenue entry structure
        revenue_entry = subscription_revenue[0]
        self.assertIn("id", revenue_entry)
        self.assertIn("stream", revenue_entry)
        self.assertIn("amount", revenue_entry)
        self.assertIn("currency", revenue_entry)
        self.assertIn("timestamp", revenue_entry)
        self.assertIn("metadata", revenue_entry)
    
    def test_revenue_analytics(self):
        """Test revenue analytics"""
        # Generate some revenue first
        self.monetization.create_subscription(self.test_user_id, SubscriptionTier.PRO, 1)
        self.monetization.unlock_premium_feature(self.test_user_id, "ai_content_pro")
        
        analytics = self.monetization.get_revenue_analytics(30)
        
        self.assertIn("period_days", analytics)
        self.assertIn("total_revenue", analytics)
        self.assertIn("revenue_by_stream", analytics)
        self.assertIn("revenue_by_day", analytics)
        self.assertIn("top_revenue_stream", analytics)
        
        self.assertGreater(analytics["total_revenue"], 0)
        self.assertIsInstance(analytics["revenue_by_stream"], dict)
        self.assertIsInstance(analytics["revenue_by_day"], dict)
    
    def test_platform_metrics(self):
        """Test platform metrics"""
        # Generate some data first
        self.monetization.create_subscription(self.test_user_id, SubscriptionTier.PRO, 1)
        self.monetization.list_marketplace_item(self.test_seller_id, {
            "name": "Test Item",
            "description": "Test",
            "price": 29.99,
            "category": "templates"
        })
        
        metrics = self.monetization.get_platform_metrics()
        
        self.assertIn("total_subscriptions", metrics)
        self.assertIn("active_subscriptions", metrics)
        self.assertIn("subscription_revenue", metrics)
        self.assertIn("marketplace_items", metrics)
        self.assertIn("marketplace_revenue", metrics)
        self.assertIn("affiliate_programs", metrics)
        self.assertIn("revenue_streams", metrics)
        self.assertIn("total_revenue", metrics)
        
        self.assertGreater(metrics["total_subscriptions"], 0)
        self.assertGreater(metrics["active_subscriptions"], 0)
        self.assertGreater(metrics["marketplace_items"], 0)
    
    def test_subscription_tiers_initialization(self):
        """Test subscription tiers initialization"""
        tiers = self.monetization.subscription_tiers
        
        # Check all tiers exist
        expected_tiers = [SubscriptionTier.FREE, SubscriptionTier.BASIC, 
                         SubscriptionTier.PRO, SubscriptionTier.ENTERPRISE, SubscriptionTier.VIP]
        
        for tier in expected_tiers:
            self.assertIn(tier, tiers)
            tier_info = tiers[tier]
            self.assertIn("name", tier_info)
            self.assertIn("price", tier_info)
            self.assertIn("currency", tier_info)
            self.assertIn("features", tier_info)
            self.assertIn("limits", tier_info)
    
    def test_marketplace_categories_initialization(self):
        """Test marketplace categories initialization"""
        categories = self.monetization.marketplace_categories
        
        expected_categories = ["templates", "components", "ai_content", 
                              "plugins", "themes", "tutorials"]
        
        for category in expected_categories:
            self.assertIn(category, categories)
            category_info = categories[category]
            self.assertIn("name", category_info)
            self.assertIn("description", category_info)
            self.assertIn("revenue_share", category_info)
            self.assertIn("popular_tags", category_info)
    
    def test_affiliate_programs_initialization(self):
        """Test affiliate programs initialization"""
        programs = self.monetization.affiliate_programs
        
        expected_programs = ["referral", "content_creator", "developer", "enterprise"]
        
        for program in expected_programs:
            self.assertIn(program, programs)
            program_info = programs[program]
            self.assertIn("name", program_info)
            self.assertIn("commission_rate", program_info)
            self.assertIn("cookie_duration", program_info)
            self.assertIn("minimum_payout", program_info)
            self.assertIn("payout_methods", program_info)
    
    def test_api_key_generation(self):
        """Test API key generation"""
        key1 = self.monetization._generate_api_key("user1")
        key2 = self.monetization._generate_api_key("user2")
        
        self.assertIsInstance(key1, str)
        self.assertIsInstance(key2, str)
        self.assertNotEqual(key1, key2)
        self.assertEqual(len(key1), 64)  # SHA256 hex length
        self.assertEqual(len(key2), 64)
    
    def test_invalid_operations(self):
        """Test invalid operations"""
        # Test invalid marketplace item
        invalid_purchase = self.monetization.purchase_marketplace_item(
            self.test_buyer_id, "invalid_item_id"
        )
        self.assertIn("error", invalid_purchase)
        
        # Test invalid affiliate program
        invalid_affiliate = self.monetization.join_affiliate_program(
            self.test_user_id, "invalid_program"
        )
        self.assertIn("error", invalid_affiliate)
        
        # Test invalid premium feature
        invalid_feature = self.monetization.unlock_premium_feature(
            self.test_user_id, "invalid_feature"
        )
        self.assertIn("error", invalid_feature)
        
        # Test invalid API plan
        invalid_api = self.monetization.create_api_access(
            self.test_user_id, "invalid_plan"
        )
        self.assertIn("error", invalid_api)
        
        # Test invalid training type
        invalid_training = self.monetization.book_training_session(
            self.test_user_id, "invalid_training"
        )
        self.assertIn("error", invalid_training)
        
        # Test invalid consulting type
        invalid_consulting = self.monetization.book_consulting_session(
            self.test_user_id, "invalid_consulting"
        )
        self.assertIn("error", invalid_consulting)
    
    def test_subscription_upgrade_edge_cases(self):
        """Test subscription upgrade edge cases"""
        # Test upgrade without existing subscription
        no_sub_upgrade = self.monetization.upgrade_subscription(
            "non_existent_user", SubscriptionTier.PRO
        )
        self.assertIn("error", no_sub_upgrade)
    
    def test_affiliate_conversion_edge_cases(self):
        """Test affiliate conversion edge cases"""
        # Test invalid affiliate ID
        invalid_conversion = self.monetization.track_affiliate_conversion(
            "invalid_affiliate_id", self.test_buyer_id, 100.0
        )
        self.assertIn("error", invalid_conversion)

def run_monetization_demo():
    """Run a comprehensive demo of monetization system"""
    print("💰 Monetization System Demo")
    print("=" * 50)
    
    # Initialize system
    monetization = MonetizationSystem()
    
    # Subscription demo
    print("\n1. Subscription System...")
    subscription = monetization.create_subscription("demo_user", SubscriptionTier.PRO, 1)
    print(f"✅ Created subscription: {subscription['tier']} - ${subscription['price']}")
    
    subscription_info = monetization.get_subscription_info("demo_user")
    print(f"✅ Subscription info: {subscription_info['tier']} - {subscription_info['days_remaining']} days remaining")
    
    # Marketplace demo
    print("\n2. Marketplace System...")
    item = monetization.list_marketplace_item("demo_seller", {
        "name": "Demo Template",
        "description": "A demo template for testing",
        "price": 29.99,
        "category": "templates",
        "tags": ["demo", "template", "test"]
    })
    print(f"✅ Listed item: {item['item'].name} - ${item['item'].price}")
    
    purchase = monetization.purchase_marketplace_item("demo_buyer", item["item_id"])
    print(f"✅ Purchased item: Platform revenue ${purchase['platform_revenue']:.2f}")
    
    # Affiliate program demo
    print("\n3. Affiliate Program...")
    affiliate = monetization.join_affiliate_program("demo_user", "referral")
    print(f"✅ Joined affiliate program: {affiliate['program']} - {affiliate['commission_rate']*100}% commission")
    
    conversion = monetization.track_affiliate_conversion(affiliate["affiliate_id"], "new_user", 100.0)
    print(f"✅ Tracked conversion: ${conversion['commission']:.2f} commission")
    
    # Premium features demo
    print("\n4. Premium Features...")
    feature = monetization.unlock_premium_feature("demo_user", "ai_content_pro")
    print(f"✅ Unlocked feature: {feature['feature_name']} - ${feature['price']}")
    
    # API access demo
    print("\n5. API Access...")
    api_access = monetization.create_api_access("demo_user", "pro")
    print(f"✅ Created API access: {api_access['plan']} - ${api_access['plan_details']['price']}")
    
    # Training demo
    print("\n6. Training Services...")
    training = monetization.book_training_session("demo_user", "advanced")
    print(f"✅ Booked training: {training['training_details']['name']} - ${training['training_details']['price']}")
    
    # Consulting demo
    print("\n7. Consulting Services...")
    consulting = monetization.book_consulting_session("demo_user", "strategy")
    print(f"✅ Booked consulting: {consulting['consulting_details']['name']} - ${consulting['consulting_details']['price']}")
    
    # White-label demo
    print("\n8. White-label Solutions...")
    whitelabel = monetization.create_whitelabel_solution("demo_client", {
        "features": ["custom_branding", "custom_domain"]
    })
    print(f"✅ Created white-label solution: ${whitelabel['total_price']:.2f}")
    
    # Revenue analytics demo
    print("\n9. Revenue Analytics...")
    analytics = monetization.get_revenue_analytics(30)
    print(f"✅ Total revenue (30 days): ${analytics['total_revenue']:.2f}")
    print(f"✅ Revenue by stream: {analytics['revenue_by_stream']}")
    
    # Platform metrics demo
    print("\n10. Platform Metrics...")
    metrics = monetization.get_platform_metrics()
    print(f"✅ Active subscriptions: {metrics['active_subscriptions']}")
    print(f"✅ Marketplace items: {metrics['marketplace_items']}")
    print(f"✅ Total revenue: ${metrics['total_revenue']:.2f}")
    
    print("\n🎉 Monetization Demo completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    # Run tests
    print("🧪 Running Monetization System Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "="*60 + "\n")
    
    # Run demo
    run_monetization_demo()
