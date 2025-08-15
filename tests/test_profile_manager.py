""
Tests for the profile_manager module.
"""

import json
import os
import shutil
import tempfile
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from modules.profile_manager import ProfileManager, select_or_create_profile


def test_profile_manager_initialization():
    """Test that ProfileManager initializes correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ProfileManager(profiles_dir=temp_dir)
        assert manager.profiles_dir == Path(temp_dir)
        assert manager.current_profile is None
        assert os.path.exists(temp_dir)


def test_create_and_load_profile():
    """Test creating and loading a profile."""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ProfileManager(profiles_dir=temp_dir)
        
        # Test creating a new profile
        profile = manager.create_profile("testuser")
        assert profile["username"] == "testuser"
        assert profile["login_streak"] == 0
        
        # Test loading the profile
        loaded_profile = manager.load_profile("testuser")
        assert loaded_profile["username"] == "testuser"
        assert loaded_profile["login_streak"] == 1  # Should be 1 after first login
        
        # Test profile exists
        assert manager.profile_exists("testuser") is True
        assert manager.profile_exists("nonexistent") is False


def test_list_profiles():
    """Test listing available profiles."""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ProfileManager(profiles_dir=temp_dir)
        
        # Create some test profiles
        manager.create_profile("user1")
        manager.create_profile("user2")
        
        # Test listing profiles
        profiles = manager.list_profiles()
        assert set(profiles) == {"user1", "user2"}


def test_login_streak():
    """Test login streak tracking."""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ProfileManager(profiles_dir=temp_dir)
        
        # Create a profile and log in
        manager.create_profile("testuser")
        profile = manager.load_profile("testuser")
        assert profile["login_streak"] == 1
        
        # Log in again on the same day - streak should stay the same
        profile = manager.load_profile("testuser")
        assert profile["login_streak"] == 1


def test_update_progress():
    """Test updating profile progress."""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ProfileManager(profiles_dir=temp_dir)
        manager.create_profile("testuser")
        manager.load_profile("testuser")
        
        # Update module progress
        manager.update_progress("basics", 5)
        assert manager.current_profile["progress"]["basics"] == 5
        
        # Update challenges
        manager.update_progress("challenge", ["challenge1"])
        assert "challenge1" in manager.current_profile["progress"]["challenges_completed"]
        
        # Update lessons
        manager.update_progress("lesson", {"id": "linux_basics", "score": 100})
        assert "linux_basics" in manager.current_profile["progress"]["lessons_completed"]


def test_get_progress_summary():
    """Test getting a progress summary."""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ProfileManager(profiles_dir=temp_dir)
        manager.create_profile("testuser")
        manager.load_profile("testuser")
        
        # Set up some progress
        manager.update_progress("basics", 5)
        manager.update_progress("challenge", ["challenge1"])
        manager.update_progress("lesson", {"id": "linux_basics", "score": 100})
        
        # Get summary
        summary = manager.get_progress_summary()
        assert summary["basics"] == 5
        assert "challenge1" in summary["challenges_completed"]
        assert summary["total_lessons"] == 1
        assert summary["login_streak"] == 1


@patch("modules.profile_manager.console")
def test_select_or_create_profile_new(mock_console):
    """Test creating a new profile through the interactive function."""
    # Mock user input
    with patch("modules.profile_manager.Prompt.ask", side_effect=["new", "testuser"]) as mock_prompt:
        with tempfile.TemporaryDirectory() as temp_dir:
            profile = select_or_create_profile()
            
            # Verify the profile was created
            assert profile["username"] == "testuser"
            assert os.path.exists(os.path.join(temp_dir, "testuser.json"))


@patch("modules.profile_manager.console")
def test_select_or_create_profile_existing(mock_console):
    """Test selecting an existing profile through the interactive function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test profile
        manager = ProfileManager(profiles_dir=temp_dir)
        manager.create_profile("testuser")
        
        # Mock user input to select the existing profile
        with patch("modules.profile_manager.Prompt.ask", side_effect=["1", "exit"]):
            profile = select_or_create_profile()
            assert profile["username"] == "testuser"


def test_show_profile_summary(capsys):
    """Test displaying the profile summary."""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ProfileManager(profiles_dir=temp_dir)
        manager.create_profile("testuser")
        manager.load_profile("testuser")
        
        # Set up some progress
        manager.update_progress("basics", 5)
        
        # Show the summary
        manager.show_profile_summary()
        
        # Capture the output and verify it contains expected text
        captured = capsys.readouterr()
        assert "testuser" in captured.out
        assert "Linux Basics" in captured.out
        assert "5/10" in captured.out
