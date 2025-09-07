#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for Viral Features System
Comprehensive testing for all viral features functionality
"""

import unittest
import json
import time
from datetime import datetime, timedelta
from viral_features import ViralFeaturesSystem, ViralFeatureType, ViralEvent

class TestViralFeaturesSystem(unittest.TestCase):
    """Test cases for Viral Features System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.viral_system = ViralFeaturesSystem()
        self.test_user_id = "test_user_123"
        self.test_username = "TestUser"
    
    def test_user_profile_creation(self):
        """Test user profile creation"""
        profile = self.viral_system.create_user_profile(self.test_user_id, self.test_username)
        
        self.assertEqual(profile["user_id"], self.test_user_id)
        self.assertEqual(profile["username"], self.test_username)
        self.assertEqual(profile["level"], 1)
        self.assertEqual(profile["experience"], 0)
        self.assertIsInstance(profile["referral_code"], str)
        self.assertEqual(len(profile["referral_code"]), 8)
    
    def test_experience_awarding(self):
        """Test experience point awarding"""
        # Test different actions
        actions = ["create_website", "use_ai_content", "voice_command", "collaborate"]
        expected_points = [50, 25, 15, 30]
        
        for action, expected in zip(actions, expected_points):
            points = self.viral_system.award_experience(self.test_user_id, action)
            self.assertEqual(points, expected)
    
    def test_level_up_system(self):
        """Test level up system"""
        # Test level up calculation
        level_up_info = self.viral_system.check_level_up(self.test_user_id, 1500)
        self.assertTrue(level_up_info["leveled_up"])
        self.assertEqual(level_up_info["new_level"], 2)
        
        # Test no level up
        no_level_up = self.viral_system.check_level_up(self.test_user_id, 500)
        self.assertFalse(no_level_up["leveled_up"])
    
    def test_achievement_system(self):
        """Test achievement system"""
        # Test achievements with different user stats
        user_stats = {
            "total_websites": 1,
            "total_ai_content": 5,
            "total_voice_commands": 20,
            "total_collaborations": 5,
            "streak_days": 7,
            "referral_count": 10,
            "security_setups": 3,
            "templates_shared": 5
        }
        
        achievements = self.viral_system.check_achievements(self.test_user_id, user_stats)
        self.assertIsInstance(achievements, list)
        self.assertGreater(len(achievements), 0)
    
    def test_daily_challenges(self):
        """Test daily challenges"""
        challenges = self.viral_system.get_daily_challenges()
        self.assertIsInstance(challenges, list)
        self.assertGreater(len(challenges), 0)
        
        # Test challenge structure
        challenge = challenges[0]
        self.assertIn("title", challenge)
        self.assertIn("description", challenge)
        self.assertIn("reward", challenge)
        self.assertIn("difficulty", challenge)
        self.assertIn("time_limit", challenge)
    
    def test_challenge_start_and_complete(self):
        """Test challenge start and completion"""
        # Start a challenge
        challenge_result = self.viral_system.start_challenge(self.test_user_id, "daily_website")
        self.assertIn("challenge_id", challenge_result)
        self.assertIn("title", challenge_result)
        self.assertIn("time_limit", challenge_result)
        
        # Complete the challenge
        complete_result = self.viral_system.complete_challenge(self.test_user_id, "daily_website")
        self.assertTrue(complete_result["completed"])
        self.assertIn("reward", complete_result)
        self.assertIn("points_awarded", complete_result)
    
    def test_leaderboard_system(self):
        """Test leaderboard system"""
        # Update leaderboard
        self.viral_system.update_leaderboard("weekly_builders", self.test_user_id, 150, {"websites": 3})
        
        # Get leaderboard
        leaderboard = self.viral_system.get_leaderboard("weekly_builders", 5)
        self.assertIsInstance(leaderboard, list)
        
        if leaderboard:
            entry = leaderboard[0]
            self.assertIn("user_id", entry)
            self.assertIn("score", entry)
            self.assertIn("rank", entry)
    
    def test_referral_system(self):
        """Test referral system"""
        # Create user profile to get referral code
        profile = self.viral_system.create_user_profile(self.test_user_id, self.test_username)
        referral_code = profile["referral_code"]
        
        # Process referral
        new_user_id = "new_user_456"
        referral_result = self.viral_system.process_referral(referral_code, new_user_id)
        
        self.assertTrue(referral_result["success"])
        self.assertEqual(referral_result["referrer_id"], self.test_user_id)
        self.assertEqual(referral_result["points_awarded"], 75)
    
    def test_social_sharing(self):
        """Test social sharing features"""
        content_data = {
            "url": "https://example.com/website",
            "preview": "Amazing website created with AI!"
        }
        
        shareable_content = self.viral_system.generate_shareable_content(
            self.test_user_id, "website_created", content_data
        )
        
        self.assertIn("text", shareable_content)
        self.assertIn("hashtags", shareable_content)
        self.assertIn("share_url", shareable_content)
        self.assertIn("qr_code", shareable_content)
        self.assertIn("https://sitebuilder.com/share/", shareable_content["share_url"])
    
    def test_template_sharing(self):
        """Test template sharing"""
        template_data = {
            "name": "AI Portfolio Template",
            "category": "portfolio",
            "tags": ["AI", "Portfolio", "Modern"]
        }
        
        share_result = self.viral_system.share_template(self.test_user_id, template_data)
        
        self.assertIn("share_id", share_result)
        self.assertIn("share_url", share_result)
        self.assertIn("template", share_result)
        self.assertIn("https://sitebuilder.com/template/", share_result["share_url"])
    
    def test_collaboration_invites(self):
        """Test collaboration invites"""
        invite_data = {
            "project_name": "Global Website Project",
            "message": "Join me in building something amazing!",
            "languages": ["en", "fa", "ar"],
            "skills": ["design", "development", "content"],
            "max_collaborators": 5
        }
        
        invite_result = self.viral_system.send_collaboration_invite(self.test_user_id, invite_data)
        
        self.assertIn("invite_id", invite_result)
        self.assertIn("invite_url", invite_result)
        self.assertIn("invite", invite_result)
        self.assertIn("https://sitebuilder.com/collaborate/", invite_result["invite_url"])
    
    def test_ai_showcase(self):
        """Test AI showcase features"""
        result_data = {
            "content_type": "blog_post",
            "quality_score": 95,
            "language": "fa",
            "word_count": 500
        }
        
        showcase_result = self.viral_system.showcase_ai_feature(
            self.test_user_id, "ai_content", result_data
        )
        
        self.assertIn("showcase_id", showcase_result)
        self.assertIn("showcase_url", showcase_result)
        self.assertIn("showcase", showcase_result)
        self.assertIn("https://sitebuilder.com/showcase/", showcase_result["showcase_url"])
    
    def test_trending_templates(self):
        """Test trending templates"""
        trending = self.viral_system.get_trending_templates(5)
        
        self.assertIsInstance(trending, list)
        self.assertLessEqual(len(trending), 5)
        
        if trending:
            template = trending[0]
            self.assertIn("id", template)
            self.assertIn("name", template)
            self.assertIn("category", template)
            self.assertIn("downloads", template)
            self.assertIn("rating", template)
    
    def test_viral_analytics(self):
        """Test viral analytics"""
        # Generate some viral events first
        self.viral_system.award_experience(self.test_user_id, "create_website")
        self.viral_system.award_experience(self.test_user_id, "use_ai_content")
        
        analytics = self.viral_system.get_viral_analytics(7)
        
        self.assertIn("period_days", analytics)
        self.assertIn("total_events", analytics)
        self.assertIn("unique_users", analytics)
        self.assertIn("engagement_score", analytics)
        self.assertIn("events_by_type", analytics)
        self.assertIn("top_viral_features", analytics)
    
    def test_global_stats(self):
        """Test global platform statistics"""
        # Generate some events
        self.viral_system.award_experience(self.test_user_id, "create_website")
        self.viral_system.award_experience(self.test_user_id, "use_ai_content")
        
        stats = self.viral_system.get_global_stats()
        
        self.assertIn("total_users", stats)
        self.assertIn("total_websites_created", stats)
        self.assertIn("total_ai_content_generated", stats)
        self.assertIn("total_voice_commands", stats)
        self.assertIn("total_collaborations", stats)
        self.assertIn("total_templates_shared", stats)
        self.assertIn("total_referrals", stats)
        self.assertIn("active_challenges", stats)
        self.assertIn("leaderboard_entries", stats)
    
    def test_viral_event_logging(self):
        """Test viral event logging"""
        initial_count = len(self.viral_system.viral_events)
        
        # Generate some events
        self.viral_system.award_experience(self.test_user_id, "create_website")
        self.viral_system.award_experience(self.test_user_id, "use_ai_content")
        
        final_count = len(self.viral_system.viral_events)
        self.assertGreater(final_count, initial_count)
    
    def test_referral_code_generation(self):
        """Test referral code generation"""
        code1 = self.viral_system._generate_referral_code("user1")
        code2 = self.viral_system._generate_referral_code("user2")
        
        self.assertEqual(len(code1), 8)
        self.assertEqual(len(code2), 8)
        self.assertNotEqual(code1, code2)
        self.assertTrue(code1.isupper())
        self.assertTrue(code2.isupper())
    
    def test_share_id_generation(self):
        """Test share ID generation"""
        share_id1 = self.viral_system._generate_share_id()
        share_id2 = self.viral_system._generate_share_id()
        
        self.assertEqual(len(share_id1), 12)
        self.assertEqual(len(share_id2), 12)
        self.assertNotEqual(share_id1, share_id2)
    
    def test_qr_code_generation(self):
        """Test QR code generation"""
        test_url = "https://sitebuilder.com/test"
        qr_code = self.viral_system._generate_qr_code(test_url)
        
        self.assertIsInstance(qr_code, str)
        self.assertTrue(qr_code.startswith("data:image/png;base64,"))
        self.assertGreater(len(qr_code), 100)  # Base64 should be substantial
    
    def test_level_rewards(self):
        """Test level rewards system"""
        # Test different levels
        level_2_rewards = self.viral_system._get_level_rewards(2)
        level_5_rewards = self.viral_system._get_level_rewards(5)
        level_20_rewards = self.viral_system._get_level_rewards(20)
        
        self.assertIsInstance(level_2_rewards, list)
        self.assertIsInstance(level_5_rewards, list)
        self.assertIsInstance(level_20_rewards, list)
        
        # Test non-existent level
        no_rewards = self.viral_system._get_level_rewards(100)
        self.assertEqual(no_rewards, [])
    
    def test_challenge_validation(self):
        """Test challenge validation"""
        # Test invalid challenge
        invalid_result = self.viral_system.start_challenge(self.test_user_id, "invalid_challenge")
        self.assertIn("error", invalid_result)
        
        # Test invalid completion
        invalid_complete = self.viral_system.complete_challenge(self.test_user_id, "invalid_challenge")
        self.assertIn("error", invalid_complete)
    
    def test_invalid_referral(self):
        """Test invalid referral processing"""
        invalid_result = self.viral_system.process_referral("INVALID", "new_user")
        self.assertIn("error", invalid_result)
    
    def test_leaderboard_edge_cases(self):
        """Test leaderboard edge cases"""
        # Test non-existent leaderboard
        empty_leaderboard = self.viral_system.get_leaderboard("non_existent", 5)
        self.assertEqual(empty_leaderboard, [])
        
        # Test limit parameter
        self.viral_system.update_leaderboard("test_lb", "user1", 100)
        self.viral_system.update_leaderboard("test_lb", "user2", 200)
        self.viral_system.update_leaderboard("test_lb", "user3", 300)
        
        limited_leaderboard = self.viral_system.get_leaderboard("test_lb", 2)
        self.assertEqual(len(limited_leaderboard), 2)
    
    def test_analytics_edge_cases(self):
        """Test analytics edge cases"""
        # Test with no events
        empty_analytics = self.viral_system.get_viral_analytics(1)
        self.assertEqual(empty_analytics["total_events"], 0)
        self.assertEqual(empty_analytics["unique_users"], 0)
        self.assertEqual(empty_analytics["engagement_score"], 0)
    
    def test_global_stats_edge_cases(self):
        """Test global stats edge cases"""
        # Test with no events
        empty_stats = self.viral_system.get_global_stats()
        self.assertEqual(empty_stats["total_users"], 0)
        self.assertEqual(empty_stats["total_websites_created"], 0)

def run_viral_features_demo():
    """Run a comprehensive demo of viral features"""
    print("🚀 Viral Features System Demo")
    print("=" * 50)
    
    # Initialize system
    viral_system = ViralFeaturesSystem()
    
    # Create user profile
    print("\n1. Creating user profile...")
    profile = viral_system.create_user_profile("demo_user", "DemoUser")
    print(f"✅ Created profile: {profile['username']} (Level {profile['level']})")
    print(f"✅ Referral code: {profile['referral_code']}")
    
    # Award experience
    print("\n2. Awarding experience points...")
    actions = ["create_website", "use_ai_content", "voice_command", "collaborate"]
    total_exp = 0
    for action in actions:
        points = viral_system.award_experience("demo_user", action)
        total_exp += points
        print(f"✅ {action}: +{points} points")
    
    print(f"✅ Total experience: {total_exp}")
    
    # Check level up
    print("\n3. Checking level up...")
    level_up = viral_system.check_level_up("demo_user", total_exp)
    if level_up["leveled_up"]:
        print(f"🎉 Level up! New level: {level_up['new_level']}")
        print(f"🎁 Rewards: {level_up['new_features']}")
    else:
        print("📈 Keep going to level up!")
    
    # Check achievements
    print("\n4. Checking achievements...")
    user_stats = {
        "total_websites": 1,
        "total_ai_content": 5,
        "total_voice_commands": 20,
        "total_collaborations": 5,
        "streak_days": 7,
        "referral_count": 10
    }
    achievements = viral_system.check_achievements("demo_user", user_stats)
    print(f"✅ New achievements: {len(achievements)}")
    for achievement in achievements:
        print(f"   🏆 {achievement}")
    
    # Daily challenges
    print("\n5. Daily challenges...")
    challenges = viral_system.get_daily_challenges()
    print(f"✅ Available challenges: {len(challenges)}")
    for challenge in challenges[:3]:  # Show first 3
        print(f"   🏆 {challenge['title']} - {challenge['reward']}")
    
    # Start and complete a challenge
    print("\n6. Starting challenge...")
    challenge_result = viral_system.start_challenge("demo_user", "daily_website")
    print(f"✅ Started: {challenge_result['title']}")
    
    complete_result = viral_system.complete_challenge("demo_user", "daily_website")
    print(f"✅ Completed: {complete_result['reward']} (+{complete_result['points_awarded']} points)")
    
    # Leaderboard
    print("\n7. Leaderboard system...")
    viral_system.update_leaderboard("weekly_builders", "demo_user", 150, {"websites": 3})
    leaderboard = viral_system.get_leaderboard("weekly_builders", 3)
    print(f"✅ Leaderboard entries: {len(leaderboard)}")
    
    # Social sharing
    print("\n8. Social sharing...")
    share_content = viral_system.generate_shareable_content("demo_user", "website_created", {
        "url": "https://demo.com/website"
    })
    print(f"✅ Generated shareable content: {share_content['text'][:50]}...")
    print(f"✅ Share URL: {share_content['share_url']}")
    
    # Template sharing
    print("\n9. Template sharing...")
    template_share = viral_system.share_template("demo_user", {
        "name": "Demo Template",
        "category": "portfolio",
        "tags": ["demo", "portfolio", "modern"]
    })
    print(f"✅ Shared template: {template_share['share_id']}")
    
    # Referral system
    print("\n10. Referral system...")
    referral_result = viral_system.process_referral(profile['referral_code'], "new_user_456")
    print(f"✅ Referral processed: +{referral_result['points_awarded']} points")
    
    # Viral analytics
    print("\n11. Viral analytics...")
    analytics = viral_system.get_viral_analytics(7)
    print(f"✅ Total events: {analytics['total_events']}")
    print(f"✅ Unique users: {analytics['unique_users']}")
    print(f"✅ Engagement score: {analytics['engagement_score']:.2f}")
    
    # Global stats
    print("\n12. Global platform stats...")
    global_stats = viral_system.get_global_stats()
    print(f"✅ Total users: {global_stats['total_users']}")
    print(f"✅ Websites created: {global_stats['total_websites_created']}")
    print(f"✅ AI content generated: {global_stats['total_ai_content_generated']}")
    print(f"✅ Active challenges: {global_stats['active_challenges']}")
    
    print("\n🎉 Viral Features Demo completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    # Run tests
    print("🧪 Running Viral Features Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "="*60 + "\n")
    
    # Run demo
    run_viral_features_demo()
