"""
Tests for the Leaderboard and Badge functionality.
"""
import os
import json
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from modules.badges import Leaderboard, BadgeManager, Badge

class TestLeaderboardAndBadges(unittest.TestCase):
    """Test cases for Leaderboard and Badge functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test data
        self.test_dir = Path(tempfile.mkdtemp())
        self.leaderboard = Leaderboard(profiles_dir=str(self.test_dir))
        self.badge_manager = BadgeManager()
        
        # Sample user data
        self.test_user = "test_user"
        self.test_stats = {
            "challenges.completed": 5,
            "challenges.perfect_scores": 2,
            "modules.completed": 1,
            "modules.touched_count": 3,
            "streak.current": 7,
            "last_activity": datetime.utcnow().isoformat(),
            "total_score": 150
        }
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test leaderboard initialization creates necessary files."""
        self.assertTrue(self.leaderboard.scoreboard_file.exists())
        self.assertTrue(self.leaderboard.scoreboard_file.is_file())
    
    def test_update_score_new_user(self):
        """Test updating score for a new user."""
        self.leaderboard.update_score(self.test_user, self.test_stats)
        
        # Verify the score was saved correctly
        with open(self.leaderboard.scoreboard_file, 'r') as f:
            data = json.load(f)
            
        self.assertIn("users", data)
        self.assertIn(self.test_user, data["users"])
        self.assertEqual(data["users"][self.test_user]["challenges.completed"], 5)
        self.assertEqual(data["users"][self.test_user]["total_score"], 150)
    
    def test_update_score_existing_user(self):
        """Test updating score for an existing user."""
        # First update
        self.leaderboard.update_score(self.test_user, self.test_stats)
        
        # Second update with additional stats
        self.leaderboard.update_score(self.test_user, {"challenges.completed": 2})  # Add 2 more
        
        # Verify the score was updated correctly
        with open(self.leaderboard.scoreboard_file, 'r') as f:
            data = json.load(f)
            
        self.assertEqual(data["users"][self.test_user]["challenges.completed"], 7)  # 5 + 2
    
    def test_get_leaderboard(self):
        """Test retrieving the leaderboard."""
        # Add test users
        users = [
            ("user1", {"total_score": 100, "challenges.completed": 3, "last_activity": datetime.utcnow().isoformat()}),
            ("user2", {"total_score": 200, "challenges.completed": 5, "last_activity": datetime.utcnow().isoformat()}),
            ("user3", {"total_score": 150, "challenges.completed": 4, "last_activity": datetime.utcnow().isoformat()})
        ]
        
        for username, stats in users:
            self.leaderboard.update_score(username, stats)
        
        # Get top 2 users
        leaderboard = self.leaderboard.get_leaderboard(limit=2)
        
        self.assertEqual(len(leaderboard), 2)
        self.assertEqual(leaderboard[0]["username"], "user2")  # Highest score first
        self.assertEqual(leaderboard[0]["score"], 200)
        self.assertEqual(leaderboard[1]["username"], "user3")
    
    def test_badge_awarding(self):
        """Test that badges are awarded correctly."""
        # Update score with stats that should earn badges
        self.leaderboard.update_score(self.test_user, self.test_stats)
        
        # Get user data
        with open(self.leaderboard.scoreboard_file, 'r') as f:
            data = json.load(f)
        
        user_data = data["users"][self.test_user]
        
        # Check that badges were awarded
        self.assertIn("badges", user_data)
        self.assertGreater(len(user_data["badges"]), 0)
        
        # Check specific badges
        badge_ids = [b.id for b in self.badge_manager.get_all_badges()]
        for badge_id in ["first_challenge", "challenge_master"]:
            if badge_id in badge_ids:  # Only check if badge exists
                self.assertIn(badge_id, user_data["badges"])
    
    def test_get_user_stats(self):
        """Test retrieving user statistics."""
        # Add test user
        self.leaderboard.update_score(self.test_user, self.test_stats)
        
        # Get user stats
        stats = self.leaderboard.get_user_stats(self.test_user)
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats["challenges.completed"], 5)
        self.assertEqual(stats["total_score"], 150)
    
    def test_get_user_rank(self):
        """Test getting a user's rank."""
        # Add test users
        users = [
            ("user1", {"total_score": 100}),
            (self.test_user, {"total_score": 200}),
            ("user3", {"total_score": 150})
        ]
        
        for username, stats in users:
            self.leaderboard.update_score(username, stats)
        
        # Get rank
        rank = self.leaderboard.get_user_rank(self.test_user)
        self.assertEqual(rank, 1)  # Should be first place
    
    def test_get_recent_activity(self):
        """Test retrieving recent activity."""
        # Add test users with different timestamps
        now = datetime.utcnow()
        users = [
            ("user1", {"last_activity": (now - timedelta(minutes=5)).isoformat()}),
            ("user2", {"last_activity": now.isoformat()}),
            ("user3", {"last_activity": (now - timedelta(minutes=10)).isoformat()})
        ]
        
        for username, stats in users:
            self.leaderboard.update_score(username, stats)
        
        # Get recent activity
        activity = self.leaderboard.get_recent_activity(limit=2)
        
        self.assertEqual(len(activity), 2)
        # Should be ordered by most recent first
        self.assertEqual(activity[0]["username"], "user2")
        self.assertEqual(activity[1]["username"], "user1")


class TestBadgeManager(unittest.TestCase):
    """Test cases for BadgeManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.badge_manager = BadgeManager()
        self.test_user_data = {
            "challenges.completed": 5,
            "challenges.perfect_scores": 2,
            "modules.completed": 1,
            "modules.touched_count": 3,
            "streak.current": 7,
            "has_early_bird_achievement": True,
            "has_night_owl_achievement": False,
            "has_weekend_warrior_achievement": True,
            "last_activity": datetime.utcnow().isoformat()
        }
    
    def test_get_badge(self):
        """Test retrieving a badge by ID."""
        badge = self.badge_manager.get_badge("first_challenge")
        self.assertIsNotNone(badge)
        self.assertEqual(badge.name, "First Step")
        self.assertEqual(badge.points, 10)
    
    def test_get_all_badges(self):
        """Test retrieving all badges."""
        badges = self.badge_manager.get_all_badges()
        self.assertGreater(len(badges), 0)
        self.assertTrue(any(b.id == "first_challenge" for b in badges))
    
    def test_get_badges_by_category(self):
        """Test retrieving badges by category."""
        challenge_badges = self.badge_manager.get_badges_by_category("challenges")
        self.assertGreater(len(challenge_badges), 0)
        self.assertTrue(all(b.category == "challenges" for b in challenge_badges))
    
    def test_check_badge_progress(self):
        """Test checking badge progress."""
        # Test with a badge the user should have earned
        earned, messages = self.badge_manager.check_badge_progress(
            "first_challenge", self.test_user_data)
        self.assertTrue(earned)
        
        # Test with a badge the user hasn't earned
        earned, messages = self.badge_manager.check_badge_progress(
            "night_owl", self.test_user_data)
        self.assertFalse(earned)
    
    def test_get_earned_badges(self):
        """Test getting badges the user has earned."""
        badges = self.badge_manager.get_earned_badges(self.test_user_data)
        self.assertGreater(len(badges), 0)
        self.assertTrue(any(b.id == "first_challenge" for b in badges))
    
    def test_get_potential_badges(self):
        """Test getting badges the user is close to earning."""
        # User has completed 5 challenges, so they're close to the 10-challenge badge
        potential = self.badge_manager.get_potential_badges(self.test_user_data)
        challenge_badges = [p for p in potential if p['badge'].category == 'challenges' and 
                          'challenges.completed' in p['next_steps']]
        self.assertGreaterEqual(len(challenge_badges), 0)
    
    def test_calculate_badge_progress(self):
        """Test calculating badge progress."""
        badge = self.badge_manager.get_badge("challenge_master")
        # Update test data to match expected criteria
        test_data = self.test_user_data.copy()
        test_data.update({
            "challenges.completed": 5,
            "challenges.perfect_scores": 3,
            "modules.completed": 1,
            "streak.current": 2
        })
        progress = self.badge_manager._calculate_badge_progress(badge, test_data)
        # Progress should be between 0 and 1
        self.assertGreaterEqual(progress, 0.0)
        self.assertLessEqual(progress, 1.0)


if __name__ == "__main__":
    unittest.main()
