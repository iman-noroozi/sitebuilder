#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Viral Features System - Features that make users want to share and use globally
Features designed to go viral and attract users worldwide
"""

import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
import hashlib
import qrcode
from io import BytesIO
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ViralFeatureType(Enum):
    """Types of viral features"""
    CHALLENGE = "challenge"
    GAMIFICATION = "gamification"
    SOCIAL_SHARING = "social_sharing"
    ACHIEVEMENT = "achievement"
    LEADERBOARD = "leaderboard"
    REFERRAL = "referral"
    CONTEST = "contest"
    TEMPLATE_SHARING = "template_sharing"
    COLLABORATION_INVITE = "collaboration_invite"
    AI_SHOWCASE = "ai_showcase"

@dataclass
class ViralEvent:
    """Viral event data"""
    id: str
    type: ViralFeatureType
    user_id: str
    timestamp: datetime
    data: Dict
    share_count: int = 0
    engagement_score: float = 0.0

class ViralFeaturesSystem:
    """System for creating viral features that attract global users"""
    
    def __init__(self):
        self.viral_events: List[ViralEvent] = []
        self.user_achievements: Dict[str, List[str]] = {}
        self.leaderboards: Dict[str, List[Dict]] = {}
        self.challenges: Dict[str, Dict] = {}
        self.referral_codes: Dict[str, str] = {}
        
        # Initialize viral features
        self._initialize_viral_features()
        
        logger.info("Viral Features System initialized")
    
    def _initialize_viral_features(self):
        """Initialize viral features and challenges"""
        # Daily challenges
        self.challenges = {
            "daily_website": {
                "title": "Daily Website Challenge",
                "description": "Create a website in under 5 minutes",
                "reward": "Expert Builder Badge",
                "difficulty": "easy",
                "time_limit": 300,  # 5 minutes
                "participants": 0
            },
            "ai_master": {
                "title": "AI Content Master",
                "description": "Generate 10 AI-powered content pieces",
                "reward": "AI Wizard Badge",
                "difficulty": "medium",
                "time_limit": 3600,  # 1 hour
                "participants": 0
            },
            "global_collaborator": {
                "title": "Global Collaborator",
                "description": "Collaborate with users from 5 different countries",
                "reward": "World Citizen Badge",
                "difficulty": "hard",
                "time_limit": 86400,  # 24 hours
                "participants": 0
            },
            "voice_commander": {
                "title": "Voice Commander",
                "description": "Build a website using only voice commands",
                "reward": "Voice Master Badge",
                "difficulty": "medium",
                "time_limit": 1800,  # 30 minutes
                "participants": 0
            },
            "security_guardian": {
                "title": "Security Guardian",
                "description": "Implement advanced security features",
                "reward": "Security Expert Badge",
                "difficulty": "hard",
                "time_limit": 7200,  # 2 hours
                "participants": 0
            }
        }
        
        # Initialize leaderboards
        self.leaderboards = {
            "weekly_builders": [],
            "ai_content_creators": [],
            "global_collaborators": [],
            "voice_commanders": [],
            "security_experts": []
        }
    
    # 1. Gamification System
    def create_user_profile(self, user_id: str, username: str) -> Dict:
        """Create gamified user profile"""
        profile = {
            "user_id": user_id,
            "username": username,
            "level": 1,
            "experience": 0,
            "badges": [],
            "achievements": [],
            "streak_days": 0,
            "total_websites": 0,
            "total_collaborations": 0,
            "total_ai_content": 0,
            "total_voice_commands": 0,
            "referral_count": 0,
            "global_rank": 0,
            "created_at": datetime.now(),
            "last_active": datetime.now()
        }
        
        # Generate unique referral code
        profile["referral_code"] = self._generate_referral_code(user_id)
        
        return profile
    
    def award_experience(self, user_id: str, action: str, points: int = 10):
        """Award experience points for actions"""
        # Different actions give different points
        action_points = {
            "create_website": 50,
            "use_ai_content": 25,
            "voice_command": 15,
            "collaborate": 30,
            "share_template": 20,
            "complete_challenge": 100,
            "refer_friend": 75,
            "daily_login": 10,
            "security_setup": 40
        }
        
        points = action_points.get(action, points)
        
        # Log viral event
        self._log_viral_event(ViralFeatureType.GAMIFICATION, user_id, {
            "action": action,
            "points_awarded": points,
            "timestamp": datetime.now()
        })
        
        return points
    
    def check_level_up(self, user_id: str, current_exp: int) -> Dict:
        """Check if user should level up"""
        level = (current_exp // 1000) + 1
        next_level_exp = level * 1000
        
        if current_exp >= next_level_exp:
            return {
                "leveled_up": True,
                "new_level": level,
                "reward": f"Level {level} Unlocked!",
                "new_features": self._get_level_rewards(level)
            }
        
        return {"leveled_up": False}
    
    def _get_level_rewards(self, level: int) -> List[str]:
        """Get rewards for reaching a level"""
        rewards = {
            2: ["Advanced Templates", "Custom Themes"],
            3: ["AI Content Pro", "Voice Commands Pro"],
            4: ["Real-time Collaboration", "Advanced Security"],
            5: ["Global Marketplace", "Premium Support"],
            10: ["VIP Status", "Early Access Features"],
            20: ["Ambassador Program", "Revenue Sharing"]
        }
        return rewards.get(level, [])
    
    # 2. Achievement System
    def check_achievements(self, user_id: str, user_stats: Dict) -> List[str]:
        """Check and award achievements"""
        new_achievements = []
        
        achievements = {
            "first_website": {"condition": user_stats.get("total_websites", 0) >= 1, "title": "First Website"},
            "website_master": {"condition": user_stats.get("total_websites", 0) >= 10, "title": "Website Master"},
            "ai_explorer": {"condition": user_stats.get("total_ai_content", 0) >= 5, "title": "AI Explorer"},
            "voice_pioneer": {"condition": user_stats.get("total_voice_commands", 0) >= 20, "title": "Voice Pioneer"},
            "global_citizen": {"condition": user_stats.get("total_collaborations", 0) >= 5, "title": "Global Citizen"},
            "streak_master": {"condition": user_stats.get("streak_days", 0) >= 7, "title": "Streak Master"},
            "referral_king": {"condition": user_stats.get("referral_count", 0) >= 10, "title": "Referral King"},
            "security_expert": {"condition": user_stats.get("security_setups", 0) >= 3, "title": "Security Expert"},
            "template_creator": {"condition": user_stats.get("templates_shared", 0) >= 5, "title": "Template Creator"},
            "collaboration_champion": {"condition": user_stats.get("total_collaborations", 0) >= 20, "title": "Collaboration Champion"}
        }
        
        for achievement_id, achievement in achievements.items():
            if achievement["condition"] and achievement_id not in user_stats.get("achievements", []):
                new_achievements.append(achievement_id)
                self._log_viral_event(ViralFeatureType.ACHIEVEMENT, user_id, {
                    "achievement": achievement_id,
                    "title": achievement["title"]
                })
        
        return new_achievements
    
    # 3. Daily Challenges
    def get_daily_challenges(self) -> List[Dict]:
        """Get daily challenges"""
        return list(self.challenges.values())
    
    def start_challenge(self, user_id: str, challenge_id: str) -> Dict:
        """Start a challenge"""
        if challenge_id not in self.challenges:
            return {"error": "Challenge not found"}
        
        challenge = self.challenges[challenge_id]
        challenge["participants"] += 1
        
        return {
            "challenge_id": challenge_id,
            "title": challenge["title"],
            "description": challenge["description"],
            "time_limit": challenge["time_limit"],
            "started_at": datetime.now(),
            "participants": challenge["participants"]
        }
    
    def complete_challenge(self, user_id: str, challenge_id: str) -> Dict:
        """Complete a challenge"""
        if challenge_id not in self.challenges:
            return {"error": "Challenge not found"}
        
        challenge = self.challenges[challenge_id]
        
        # Award points and badge
        points = self.award_experience(user_id, "complete_challenge", 100)
        
        return {
            "completed": True,
            "challenge": challenge["title"],
            "reward": challenge["reward"],
            "points_awarded": points,
            "badge_unlocked": True
        }
    
    # 4. Leaderboards
    def update_leaderboard(self, leaderboard_type: str, user_id: str, score: int, metadata: Dict = None):
        """Update leaderboard"""
        if leaderboard_type not in self.leaderboards:
            self.leaderboards[leaderboard_type] = []
        
        # Find existing entry
        existing_index = None
        for i, entry in enumerate(self.leaderboards[leaderboard_type]):
            if entry["user_id"] == user_id:
                existing_index = i
                break
        
        entry = {
            "user_id": user_id,
            "score": score,
            "rank": 0,
            "updated_at": datetime.now(),
            "metadata": metadata or {}
        }
        
        if existing_index is not None:
            self.leaderboards[leaderboard_type][existing_index] = entry
        else:
            self.leaderboards[leaderboard_type].append(entry)
        
        # Sort by score
        self.leaderboards[leaderboard_type].sort(key=lambda x: x["score"], reverse=True)
        
        # Update ranks
        for i, entry in enumerate(self.leaderboards[leaderboard_type]):
            entry["rank"] = i + 1
        
        # Log viral event
        self._log_viral_event(ViralFeatureType.LEADERBOARD, user_id, {
            "leaderboard": leaderboard_type,
            "score": score,
            "rank": entry["rank"]
        })
    
    def get_leaderboard(self, leaderboard_type: str, limit: int = 10) -> List[Dict]:
        """Get leaderboard"""
        if leaderboard_type not in self.leaderboards:
            return []
        
        return self.leaderboards[leaderboard_type][:limit]
    
    # 5. Referral System
    def _generate_referral_code(self, user_id: str) -> str:
        """Generate unique referral code"""
        # Create a short, memorable code
        hash_obj = hashlib.md5(user_id.encode())
        code = hash_obj.hexdigest()[:8].upper()
        self.referral_codes[code] = user_id
        return code
    
    def process_referral(self, referral_code: str, new_user_id: str) -> Dict:
        """Process referral"""
        if referral_code not in self.referral_codes:
            return {"error": "Invalid referral code"}
        
        referrer_id = self.referral_codes[referral_code]
        
        # Award points to both users
        self.award_experience(referrer_id, "refer_friend", 75)
        self.award_experience(new_user_id, "referred_signup", 25)
        
        # Log viral event
        self._log_viral_event(ViralFeatureType.REFERRAL, referrer_id, {
            "referred_user": new_user_id,
            "referral_code": referral_code
        })
        
        return {
            "success": True,
            "referrer_id": referrer_id,
            "points_awarded": 75
        }
    
    # 6. Social Sharing Features
    def generate_shareable_content(self, user_id: str, content_type: str, content_data: Dict) -> Dict:
        """Generate shareable content for social media"""
        share_templates = {
            "website_created": {
                "text": "🚀 Just created an amazing website using AI! Check it out: {url}",
                "hashtags": ["#WebsiteBuilder", "#AI", "#WebDesign", "#Tech"],
                "image_template": "website_showcase"
            },
            "ai_content": {
                "text": "🤖 Generated incredible content with AI! This is the future: {preview}",
                "hashtags": ["#AIContent", "#ContentCreation", "#AI", "#Innovation"],
                "image_template": "ai_content_showcase"
            },
            "voice_commands": {
                "text": "🎤 Built a website using only voice commands! Mind = blown 🤯",
                "hashtags": ["#VoiceCommands", "#WebDesign", "#Innovation", "#Tech"],
                "image_template": "voice_showcase"
            },
            "collaboration": {
                "text": "👥 Collaborating globally in real-time! This is how the future works: {url}",
                "hashtags": ["#Collaboration", "#Global", "#RealTime", "#Innovation"],
                "image_template": "collaboration_showcase"
            },
            "achievement": {
                "text": "🏆 Just unlocked the {achievement} achievement! Level {level} here I come!",
                "hashtags": ["#Achievement", "#Gaming", "#Progress", "#Success"],
                "image_template": "achievement_showcase"
            }
        }
        
        template = share_templates.get(content_type, share_templates["website_created"])
        
        # Generate shareable content
        shareable_content = {
            "text": template["text"].format(**content_data),
            "hashtags": template["hashtags"],
            "image_template": template["image_template"],
            "share_url": f"https://sitebuilder.com/share/{self._generate_share_id()}",
            "qr_code": self._generate_qr_code(f"https://sitebuilder.com/share/{self._generate_share_id()}")
        }
        
        # Log viral event
        self._log_viral_event(ViralFeatureType.SOCIAL_SHARING, user_id, {
            "content_type": content_type,
            "share_url": shareable_content["share_url"]
        })
        
        return shareable_content
    
    def _generate_share_id(self) -> str:
        """Generate unique share ID"""
        return hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:12]
    
    def _generate_qr_code(self, url: str) -> str:
        """Generate QR code for sharing"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    # 7. Template Sharing
    def share_template(self, user_id: str, template_data: Dict) -> Dict:
        """Share template globally"""
        share_id = self._generate_share_id()
        
        shared_template = {
            "id": share_id,
            "user_id": user_id,
            "template_data": template_data,
            "share_count": 0,
            "download_count": 0,
            "rating": 0.0,
            "tags": template_data.get("tags", []),
            "category": template_data.get("category", "general"),
            "created_at": datetime.now(),
            "is_featured": False
        }
        
        # Log viral event
        self._log_viral_event(ViralFeatureType.TEMPLATE_SHARING, user_id, {
            "template_id": share_id,
            "template_name": template_data.get("name", "Untitled")
        })
        
        return {
            "share_id": share_id,
            "share_url": f"https://sitebuilder.com/template/{share_id}",
            "template": shared_template
        }
    
    def get_trending_templates(self, limit: int = 10) -> List[Dict]:
        """Get trending templates"""
        # Mock trending templates
        trending = [
            {
                "id": "trending_1",
                "name": "AI-Powered Portfolio",
                "category": "portfolio",
                "downloads": 1250,
                "rating": 4.8,
                "tags": ["AI", "Portfolio", "Modern"],
                "preview_url": "https://example.com/preview1.jpg"
            },
            {
                "id": "trending_2",
                "name": "Voice-Controlled E-commerce",
                "category": "ecommerce",
                "downloads": 980,
                "rating": 4.7,
                "tags": ["Voice", "E-commerce", "Innovation"],
                "preview_url": "https://example.com/preview2.jpg"
            }
        ]
        
        return trending[:limit]
    
    # 8. Global Collaboration Invites
    def send_collaboration_invite(self, user_id: str, invite_data: Dict) -> Dict:
        """Send global collaboration invite"""
        invite_id = self._generate_share_id()
        
        invite = {
            "id": invite_id,
            "from_user": user_id,
            "project_name": invite_data.get("project_name", "Untitled Project"),
            "invite_message": invite_data.get("message", "Join me in building something amazing!"),
            "languages": invite_data.get("languages", ["en"]),
            "skills_needed": invite_data.get("skills", []),
            "expires_at": datetime.now() + timedelta(days=7),
            "accepted_count": 0,
            "max_collaborators": invite_data.get("max_collaborators", 5)
        }
        
        # Log viral event
        self._log_viral_event(ViralFeatureType.COLLABORATION_INVITE, user_id, {
            "invite_id": invite_id,
            "project_name": invite["project_name"]
        })
        
        return {
            "invite_id": invite_id,
            "invite_url": f"https://sitebuilder.com/collaborate/{invite_id}",
            "invite": invite
        }
    
    # 9. AI Showcase
    def showcase_ai_feature(self, user_id: str, feature_type: str, result_data: Dict) -> Dict:
        """Showcase AI feature results"""
        showcase_id = self._generate_share_id()
        
        showcase = {
            "id": showcase_id,
            "user_id": user_id,
            "feature_type": feature_type,
            "result_data": result_data,
            "impressions": 0,
            "likes": 0,
            "shares": 0,
            "created_at": datetime.now()
        }
        
        # Log viral event
        self._log_viral_event(ViralFeatureType.AI_SHOWCASE, user_id, {
            "showcase_id": showcase_id,
            "feature_type": feature_type
        })
        
        return {
            "showcase_id": showcase_id,
            "showcase_url": f"https://sitebuilder.com/showcase/{showcase_id}",
            "showcase": showcase
        }
    
    # 10. Viral Event Logging
    def _log_viral_event(self, event_type: ViralFeatureType, user_id: str, data: Dict):
        """Log viral event"""
        event = ViralEvent(
            id=self._generate_share_id(),
            type=event_type,
            user_id=user_id,
            timestamp=datetime.now(),
            data=data
        )
        
        self.viral_events.append(event)
        
        # Keep only last 1000 events
        if len(self.viral_events) > 1000:
            self.viral_events = self.viral_events[-1000:]
    
    def get_viral_analytics(self, days: int = 7) -> Dict:
        """Get viral analytics"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_events = [e for e in self.viral_events if e.timestamp > cutoff_date]
        
        # Group by type
        events_by_type = {}
        for event in recent_events:
            event_type = event.type.value
            if event_type not in events_by_type:
                events_by_type[event_type] = 0
            events_by_type[event_type] += 1
        
        # Calculate engagement score
        total_events = len(recent_events)
        unique_users = len(set(e.user_id for e in recent_events))
        engagement_score = (total_events / unique_users) if unique_users > 0 else 0
        
        return {
            "period_days": days,
            "total_events": total_events,
            "unique_users": unique_users,
            "engagement_score": engagement_score,
            "events_by_type": events_by_type,
            "top_viral_features": sorted(events_by_type.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def get_global_stats(self) -> Dict:
        """Get global platform statistics"""
        return {
            "total_users": len(set(e.user_id for e in self.viral_events)),
            "total_websites_created": sum(1 for e in self.viral_events if e.data.get("action") == "create_website"),
            "total_ai_content_generated": sum(1 for e in self.viral_events if e.data.get("action") == "use_ai_content"),
            "total_voice_commands": sum(1 for e in self.viral_events if e.data.get("action") == "voice_command"),
            "total_collaborations": sum(1 for e in self.viral_events if e.data.get("action") == "collaborate"),
            "total_templates_shared": sum(1 for e in self.viral_events if e.type == ViralFeatureType.TEMPLATE_SHARING),
            "total_referrals": sum(1 for e in self.viral_events if e.type == ViralFeatureType.REFERRAL),
            "active_challenges": len([c for c in self.challenges.values() if c["participants"] > 0]),
            "leaderboard_entries": sum(len(lb) for lb in self.leaderboards.values())
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize viral features system
    viral_system = ViralFeaturesSystem()
    
    # Test user profile creation
    print("🎮 Testing Gamification System...")
    profile = viral_system.create_user_profile("user123", "TestUser")
    print(f"✅ Created profile: {profile['username']} (Level {profile['level']})")
    print(f"✅ Referral code: {profile['referral_code']}")
    
    # Test experience awarding
    points = viral_system.award_experience("user123", "create_website", 50)
    print(f"✅ Awarded {points} points for creating website")
    
    # Test achievements
    user_stats = {"total_websites": 1, "total_ai_content": 0, "total_voice_commands": 0}
    achievements = viral_system.check_achievements("user123", user_stats)
    print(f"✅ New achievements: {achievements}")
    
    # Test challenges
    print("\n🏆 Testing Challenges...")
    challenges = viral_system.get_daily_challenges()
    print(f"✅ Available challenges: {len(challenges)}")
    
    challenge_result = viral_system.start_challenge("user123", "daily_website")
    print(f"✅ Started challenge: {challenge_result['title']}")
    
    # Test leaderboards
    print("\n🏅 Testing Leaderboards...")
    viral_system.update_leaderboard("weekly_builders", "user123", 150, {"websites": 3})
    leaderboard = viral_system.get_leaderboard("weekly_builders", 5)
    print(f"✅ Leaderboard entries: {len(leaderboard)}")
    
    # Test social sharing
    print("\n📱 Testing Social Sharing...")
    share_content = viral_system.generate_shareable_content("user123", "website_created", {
        "url": "https://example.com/website"
    })
    print(f"✅ Generated shareable content: {share_content['text'][:50]}...")
    
    # Test template sharing
    print("\n📄 Testing Template Sharing...")
    template_share = viral_system.share_template("user123", {
        "name": "AI Portfolio Template",
        "category": "portfolio",
        "tags": ["AI", "Portfolio", "Modern"]
    })
    print(f"✅ Shared template: {template_share['share_id']}")
    
    # Test viral analytics
    print("\n📊 Testing Viral Analytics...")
    analytics = viral_system.get_viral_analytics(7)
    print(f"✅ Viral analytics: {analytics['total_events']} events, {analytics['unique_users']} users")
    
    # Test global stats
    print("\n🌍 Testing Global Stats...")
    global_stats = viral_system.get_global_stats()
    print(f"✅ Global stats: {global_stats['total_users']} users, {global_stats['total_websites_created']} websites")
    
    print("\n🎉 All viral features tests completed successfully!")
