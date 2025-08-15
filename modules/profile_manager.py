"""
Profile Manager Module

Handles user profile creation, loading, and progress tracking.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from .badges import leaderboard, badge_manager

console = Console()

class ProfileManager:
    """Manages user profiles and tracks progress."""
    
    def __init__(self, profiles_dir: str = ".profiles"):
        """Initialize the profile manager.
        
        Args:
            profiles_dir: Directory to store profile data
        """
        self.profiles_dir = Path(profiles_dir)
        self.current_profile: Optional[Dict[str, Any]] = None
        self.profiles_dir.mkdir(exist_ok=True, parents=True)
        
    def list_profiles(self) -> List[str]:
        """List all available profiles.
        
        Returns:
            List of profile names
        """
        return [f.stem for f in self.profiles_dir.glob("*.json")]
    
    def profile_exists(self, username: str) -> bool:
        """Check if a profile exists.
        
        Args:
            username: Name of the profile to check
            
        Returns:
            bool: True if the profile exists, False otherwise
        """
        return (self.profiles_dir / f"{username}.json").exists()
    
    def create_profile(self, username: str) -> Dict[str, Any]:
        """Create a new user profile.
        
        Args:
            username: Name for the new profile
            
        Returns:
            The created profile data
        """
        if not username.strip():
            raise ValueError("Username cannot be empty")
            
        if self.profile_exists(username):
            raise ValueError(f"Profile '{username}' already exists")
            
        profile = {
            "username": username,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
            "login_streak": 0,
            "last_login_date": None,
            "progress": {
                "basics": 0,
                "networking": 0,
                "forensics": 0,
                "permissions": 0,
                "challenges_completed": [],
                "lessons_completed": {}
            },
            "achievements": [],
            "preferences": {
                "theme": "default",
                "notifications": True
            }
        }
        
        self._save_profile(profile)
        return profile
    
    def load_profile(self, username: str) -> Dict[str, Any]:
        """Load a user profile.
        
        Args:
            username: Name of the profile to load
            
        Returns:
            The loaded profile data
        """
        profile_path = self.profiles_dir / f"{username}.json"
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile '{username}' not found")
            
        with open(profile_path, 'r') as f:
            profile = json.load(f)
            
        # Update last login and check streak
        now = datetime.now()
        last_login = datetime.fromisoformat(profile['last_login'])
        profile['last_login'] = now.isoformat()
        
        # Check if we need to update the streak
        if profile['last_login_date']:
            last_login_date = datetime.fromisoformat(profile['last_login_date']).date()
            today = now.date()
            yesterday = today - timedelta(days=1)
            
            if last_login_date == yesterday:
                # Consecutive day login
                profile['login_streak'] += 1
            elif last_login_date < yesterday:
                # Broken streak
                profile['login_streak'] = 1
            # else: same day, don't update streak
        else:
            # First login
            profile['login_streak'] = 1
            
        profile['last_login_date'] = now.date().isoformat()
        
        self._save_profile(profile)
        self.current_profile = profile
        return profile
    
    def update_progress(self, module: str, challenge: str, score: int = 10) -> bool:
        """Update the user's progress with a completed challenge.
        
        Args:
            module: The module name
            challenge: The challenge name
            score: Points to award for completion
            
        Returns:
            bool: True if progress was updated, False otherwise
        """
        if not self.current_profile:
            return False
            
        try:
            # Update completed challenges
            if "completed_challenges" not in self.current_profile:
                self.current_profile["completed_challenges"] = {}
                
            challenge_key = f"{module}:{challenge}"
            if challenge_key not in self.current_profile["completed_challenges"]:
                self.current_profile["completed_challenges"][challenge_key] = {
                    "completed_at": datetime.now().isoformat(),
                    "score": score
                }
                
                # Update module progress
                if "module_progress" not in self.current_profile:
                    self.current_profile["module_progress"] = {}
                    
                if module not in self.current_profile["module_progress"]:
                    self.current_profile["module_progress"][module] = {"completed": 0, "total": 0}
                    
                self.current_profile["module_progress"][module]["completed"] += 1
                
                # Update total score and challenge count
                self.current_profile["total_score"] = self.current_profile.get("total_score", 0) + score
                self.current_profile["challenges_completed"] = self.current_profile.get("challenges_completed", 0) + 1
                
                # Check for module completion
                module_completed = all(
                    progress["completed"] >= progress.get("total", 1) 
                    for progress in self.current_profile["module_progress"].values()
                )
                
                if module_completed:
                    self.current_profile["modules_completed"] = len(self.current_profile["module_progress"])
                
                # Update last activity
                self.current_profile["last_activity"] = datetime.now().isoformat()
                
                # Update streak
                self._update_streak()
                
                # Update leaderboard
                self._update_leaderboard()
                
                # Save the updated profile
                self.save_profile()
                return True
                
        except Exception as e:
            console.print(f"[red]Error updating progress: {e}[/red]")
            
        return False
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of the current profile's progress.
        
        Returns:
            Dictionary with progress summary
        """
        if not self.current_profile:
            return {}
            
        progress = self.current_profile['progress'].copy()
        progress['login_streak'] = self.current_profile['login_streak']
        progress['total_lessons'] = len(progress.get('lessons_completed', {}))
        progress['total_challenges'] = len(progress.get('challenges_completed', []))
        
        return progress
    
    def show_profile_summary(self) -> None:
        """Display a summary of the current profile's progress."""
        if not self.current_profile:
            console.print("[red]No profile is currently loaded[/red]")
            return
            
        progress = self.get_progress_summary()
        
        table = Table(title=f"Progress for {self.current_profile['username']}")
        table.add_column("Module", style="cyan")
        table.add_column("Progress", justify="right")
        
        # Add module progress
        table.add_row("Linux Basics", f"{progress['basics']}/10")
        table.add_row("Networking", f"{progress['networking']}/8")
        table.add_row("Digital Forensics", f"{progress['forensics']}/6")
        table.add_row("Permissions", f"{progress['permissions']}/7")
        table.add_row("Challenges Completed", str(progress['total_challenges']))
        table.add_row("Lessons Completed", str(progress['total_lessons']))
        table.add_row("Login Streak", f"{progress['login_streak']} days")
        
        console.print(table)
    
    def show_profile(self):
        """Display the current user's profile information with badges and stats."""
        if not self.current_profile:
            console.print("[yellow]No profile loaded.[/yellow]")
            return
            
        # Basic profile info
        profile_table = Table(show_header=False, box=None)
        profile_table.add_column("", style="cyan", width=20)
        profile_table.add_column("", style="")
        
        profile_table.add_row("Username", f"[bold]{self.current_profile.get('username', 'Unknown User')}[/bold]")
        profile_table.add_row("Total Score", f"[green]{self.current_profile.get('total_score', 0)}[/green]")
        profile_table.add_row("Challenges", f"{self.current_profile.get('challenges_completed', 0)} completed")
        profile_table.add_row("Current Streak", f"{self.current_profile.get('current_streak', 0)} days")
        profile_table.add_row("Longest Streak", f"{self.current_profile.get('longest_streak', 0)} days")
        
        # Show modules progress if any
        if "module_progress" in self.current_profile and self.current_profile["module_progress"]:
            modules = []
            for mod, prog in self.current_profile["module_progress"].items():
                completed = prog.get("completed", 0)
                total = prog.get("total", 1)
                progress = f"{completed}/{total}"
                modules.append(f"• {mod}: {progress}")
            
            profile_table.add_row("\nModules", "\n".join(modules))
        
        console.print(Panel(profile_table, title="[bold]Profile[/bold]"))
        
        # Show badges
        if hasattr(badge_manager, 'display_badges'):
            badge_manager.display_badges(self.current_profile)
            
        # Show leaderboard position
        leaderboard_stats = leaderboard.get_leaderboard(100)  # Get a large enough number to find current user
        user_rank = next(
            (entry["rank"] for entry in leaderboard_stats 
             if entry["username"] == self.current_profile.get("username")), 
            None
        )
        
        if user_rank:
            console.print(f"\n[bold]Leaderboard Rank:[/bold] #{user_rank}")
        
        console.print("\n[dim]Last active:[/dim]", 
                     self.current_profile.get("last_activity", "Never"))
    
    def _update_streak(self) -> None:
        """Update the user's login streak."""
        if not self.current_profile:
            return
            
        today = datetime.now().date()
        last_login_str = self.current_profile.get("last_login")
        
        if not last_login_str:
            # First login
            self.current_profile["current_streak"] = 1
            self.current_profile["longest_streak"] = 1
        else:
            last_login = datetime.fromisoformat(last_login_str).date()
            days_since = (today - last_login).days
            
            if days_since == 0:
                # Already logged in today
                return
            elif days_since == 1:
                # Consecutive day
                self.current_profile["current_streak"] = self.current_profile.get("current_streak", 0) + 1
            else:
                # Broken streak
                self.current_profile["current_streak"] = 1
            
            # Update longest streak if needed
            if self.current_profile["current_streak"] > self.current_profile.get("longest_streak", 0):
                self.current_profile["longest_streak"] = self.current_profile["current_streak"]
        
        # Update last login
        self.current_profile["last_login"] = today.isoformat()
    
    def _update_leaderboard(self) -> None:
        """Update the leaderboard with the current profile's stats."""
        if not self.current_profile or "username" not in self.current_profile:
            return
            
        stats = {
            "challenges_completed": self.current_profile.get("challenges_completed", 0),
            "total_score": self.current_profile.get("total_score", 0),
            "last_activity": datetime.now().isoformat(),
            "badges": [badge.id for badge in badge_manager.get_earned_badges(self.current_profile)]
        }
        
        leaderboard.update_score(self.current_profile["username"], stats)
    
    def save_profile(self) -> bool:
        """Save the current profile to disk.
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        if not self.current_profile or "username" not in self.current_profile:
            return False
            
        try:
            # Ensure all directories exist
            self.profiles_dir.mkdir(exist_ok=True, parents=True)
            
            # Save profile
            profile_file = self.profiles_dir / f"{self.current_profile['username']}.json"
            with open(profile_file, 'w') as f:
                json.dump(self.current_profile, f, indent=2)
                
            return True
        except Exception as e:
            console.print(f"[red]Error saving profile: {e}[/red]")
            return False
    
    def _save_profile(self, profile: Dict[str, Any]) -> None:
        """Save profile data to disk.
        
        Args:
            profile: Profile data to save
        """
        profile_path = self.profiles_dir / f"{profile['username']}.json"
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2)


def select_or_create_profile() -> Optional[Dict[str, Any]]:
    """Interactive function to select or create a profile.
    
    Returns:
        The selected/created profile data, or None if cancelled
    """
    manager = ProfileManager()
    
    while True:
        profiles = manager.list_profiles()
        
        console.print("\n[bold]PROFILES[/bold]")
        for i, profile in enumerate(profiles, 1):
            console.print(f"{i}. {profile}")
        
        console.print("\nOptions:")
        console.print("  [bold]new[/bold] - Create a new profile")
        console.print("  [bold]exit[/bold] - Exit the trainer")
        
        choice = Prompt.ask("\nSelect a profile or enter a command", default="1" if profiles else "new")
        
        if choice.lower() == 'new':
            while True:
                username = Prompt.ask("Enter a username (or 'back' to cancel)")
                if username.lower() == 'back':
                    break
                try:
                    profile = manager.create_profile(username)
                    console.print(f"\n[green]Profile '{username}' created successfully![/green]")
                    return manager.load_profile(username)
                except (ValueError, OSError) as e:
                    console.print(f"[red]Error: {e}[/red]")
        elif choice.lower() == 'exit':
            return None
        elif choice.isdigit() and 1 <= int(choice) <= len(profiles):
            username = profiles[int(choice) - 1]
            try:
                return manager.load_profile(username)
            except Exception as e:
                console.print(f"[red]Error loading profile: {e}[/red]")
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")


if __name__ == "__main__":
    # Test the profile manager
    profile = select_or_create_profile()
    if profile:
        manager = ProfileManager()
        manager.current_profile = profile
        manager.show_profile_summary()
