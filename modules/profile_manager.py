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
    
    def update_progress(self, module: str, value: Any) -> None:
        """Update progress for a module.
        
        Args:
            module: Module name (e.g., 'basics', 'networking')
            value: Progress value (e.g., score, list of completed items)
        """
        if not self.current_profile:
            raise RuntimeError("No profile is currently loaded")
            
        if module == 'challenge' and isinstance(value, list):
            # For challenges, we append to the completed list
            completed = set(self.current_profile['progress']['challenges_completed'])
            completed.update(value)
            self.current_profile['progress']['challenges_completed'] = list(completed)
        elif module == 'lesson' and isinstance(value, dict):
            # For lessons, we update the lessons_completed dict
            lesson_id = value.get('id')
            if lesson_id:
                self.current_profile['progress']['lessons_completed'][lesson_id] = {
                    'completed_at': datetime.now().isoformat(),
                    'score': value.get('score', 0)
                }
        elif module in self.current_profile['progress']:
            # For modules with numeric progress
            self.current_profile['progress'][module] = value
            
        self._save_profile(self.current_profile)
    
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
