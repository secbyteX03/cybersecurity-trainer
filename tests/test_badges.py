"""Tests for the badges and leaderboard functionality."""
import os
import json
import tempfile
import shutil
from pathlib import Path
import pytest
from datetime import datetime, timedelta

from modules.badges import Badge, BadgeManager, Leaderboard
from modules.profile_manager import ProfileManager

# Test data
TEST_USER = "test_user"
TEST_MODULE = "test_module"
TEST_CHALLENGE = "test_challenge"

@pytest.fixture
def temp_profiles_dir():
    """Create a temporary profiles directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def badge_manager():
    """Create a BadgeManager instance for testing."""
    return BadgeManager()

@pytest.fixture
def leaderboard(temp_profiles_dir):
    """Create a Leaderboard instance with a temporary profiles directory."""
    return Leaderboard(profiles_dir=temp_profiles_dir)

@pytest.fixture
def profile_manager(temp_profiles_dir):
    """Create a ProfileManager instance with a temporary profiles directory."""
    return ProfileManager(profiles_dir=temp_profiles_dir)

def test_badge_creation():
    """Test creating a badge with criteria."""
    badge = Badge(
        id="test_badge",
        name="Test Badge",
        description="A test badge",
        icon="⭐",
        criteria={"challenges_completed": {">": 5}}
    )
    
    assert badge.id == "test_badge"
    assert badge.name == "Test Badge"
    assert badge.description == "A test badge"
    assert badge.icon == "⭐"
    assert badge.criteria == {"challenges_completed": {">": 5}}

def test_badge_earned(badge_manager):
    """Test if a badge is earned based on user data."""
    # Test with a badge that requires > 5 challenges completed
    badge = Badge(
        id="test_badge",
        name="Test Badge",
        description="Complete 5 challenges",
        criteria={"challenges_completed": {">": 5}}
    )
    
    # User with 3 challenges (should not earn)
    assert not badge.is_earned({"challenges_completed": 3})
    
    # User with 6 challenges (should earn)
    assert badge.is_earned({"challenges_completed": 6})

def test_leaderboard_update(leaderboard):
    """Test updating the leaderboard with user scores."""
    # Initial update
    leaderboard.update_score("user1", {"challenges_completed": 5, "total_score": 50})
    
    # Check leaderboard
    leaderboard_data = leaderboard.get_leaderboard()
    assert len(leaderboard_data) == 1
    assert leaderboard_data[0]["username"] == "user1"
    assert leaderboard_data[0]["challenges"] == 5
    assert leaderboard_data[0]["score"] == 50
    
    # Add another user
    leaderboard.update_score("user2", {"challenges_completed": 3, "total_score": 30})
    
    # Check sorting (user1 should be first)
    leaderboard_data = leaderboard.get_leaderboard()
    assert len(leaderboard_data) == 2
    assert leaderboard_data[0]["username"] == "user1"
    assert leaderboard_data[1]["username"] == "user2"

def test_profile_progress(profile_manager, leaderboard):
    """Test profile progress updates and leaderboard integration."""
    # Create a test profile
    profile_manager.create_profile(TEST_USER)
    
    # Initial state
    assert profile_manager.current_profile["username"] == TEST_USER
    assert profile_manager.current_profile.get("challenges_completed", 0) == 0
    assert profile_manager.current_profile.get("total_score", 0) == 0
    
    # Complete a challenge
    assert profile_manager.update_progress(TEST_MODULE, TEST_CHALLENGE, 10)
    
    # Check profile was updated
    assert profile_manager.current_profile["challenges_completed"] == 1
    assert profile_manager.current_profile["total_score"] == 10
    assert f"{TEST_MODULE}:{TEST_CHALLENGE}" in profile_manager.current_profile["completed_challenges"]
    
    # Check leaderboard was updated
    leaderboard_data = leaderboard.get_leaderboard()
    assert len(leaderboard_data) == 1
    assert leaderboard_data[0]["username"] == TEST_USER
    assert leaderboard_data[0]["challenges"] == 1
    assert leaderboard_data[0]["score"] == 10

def test_streak_calculation(profile_manager):
    """Test streak calculation logic."""
    # Create a test profile
    profile_manager.create_profile(TEST_USER)
    
    # Initial state
    assert "current_streak" not in profile_manager.current_profile
    
    # First login - should set initial streak
    profile_manager._update_streak()
    assert profile_manager.current_profile["current_streak"] == 1
    assert profile_manager.current_profile["longest_streak"] == 1
    
    # Same day login - should not change
    profile_manager._update_streak()
    assert profile_manager.current_profile["current_streak"] == 1
    
    # Simulate next day login
    yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
    profile_manager.current_profile["last_login"] = yesterday
    profile_manager._update_streak()
    assert profile_manager.current_profile["current_streak"] == 2
    assert profile_manager.current_profile["longest_streak"] == 2
    
    # Simulate broken streak
    three_days_ago = (datetime.now() - timedelta(days=3)).date().isoformat()
    profile_manager.current_profile["last_login"] = three_days_ago
    profile_manager._update_streak()
    assert profile_manager.current_profile["current_streak"] == 1
    assert profile_manager.current_profile["longest_streak"] == 2

def test_badge_awarding(profile_manager, badge_manager):
    """Test that badges are awarded based on progress."""
    # Create a test profile
    profile_manager.create_profile(TEST_USER)
    
    # Initial state - should have no badges
    earned_badges = badge_manager.get_earned_badges(profile_manager.current_profile)
    assert len(earned_badges) == 0
    
    # Complete first challenge - should earn first_steps badge
    profile_manager.update_progress("test_module", "challenge1")
    
    # Get updated profile data
    profile_data = profile_manager.current_profile
    
    # Check that first_steps badge is earned
    earned_badges = badge_manager.get_earned_badges(profile_data)
    assert any(badge.id == "first_steps" for badge in earned_badges)
    
    # Complete 4 more challenges to total 5 - should earn quick_learner badge
    for i in range(2, 7):
        profile_manager.update_progress("test_module", f"challenge{i}")
    
    profile_data = profile_manager.current_profile
    earned_badges = badge_manager.get_earned_badges(profile_data)
    assert any(badge.id == "quick_learner" for badge in earned_badges)
