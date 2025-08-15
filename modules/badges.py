"""
Badges module for the Cybersecurity Trainer.
Defines badges that users can earn by completing challenges.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os

@dataclass
class Badge:
    """Represents an achievement badge that can be earned by users."""
    id: str
    name: str
    description: str
    icon: str = "⭐"
    criteria: Dict = field(default_factory=dict)
    
    def is_earned(self, user_data: Dict) -> bool:
        """Check if the user has earned this badge based on their data."""
        # Check each criterion
        for key, required_value in self.criteria.items():
            user_value = user_data.get(key, 0)
            if isinstance(required_value, dict):
                # Handle nested criteria (e.g., challenges.completed > 5)
                for op, value in required_value.items():
                    if op == ">" and user_value <= value:
                        return False
                    elif op == "<" and user_value >= value:
                        return False
                    elif op == "==" and user_value != value:
                        return False
            elif user_value != required_value:
                return False
        return True

class BadgeManager:
    """Manages available badges and user badge progress."""
    
    def __init__(self):
        self.badges: Dict[str, Badge] = {}
        self.load_default_badges()
    
    def load_default_badges(self):
        """Load the default set of badges."""
        self.badges = {
            "first_steps": Badge(
                id="first_steps",
                name="First Steps",
                description="Complete your first challenge",
                icon="👣",
                criteria={"challenges_completed": {">": 0}}
            ),
            "quick_learner": Badge(
                id="quick_learner",
                name="Quick Learner",
                description="Complete 5 challenges",
                icon="🚀",
                criteria={"challenges_completed": {">": 4}}
            ),
            "module_master": Badge(
                id="module_master",
                name="Module Master",
                description="Complete all challenges in a module",
                icon="🎓",
                criteria={"modules_completed": {">": 0}}
            ),
            "security_expert": Badge(
                id="security_expert",
                name="Security Expert",
                description="Complete all challenges in all modules",
                icon="🏆",
                criteria={"modules_completed_all": True}
            ),
            "streak_7": Badge(
                id="streak_7",
                name="7-Day Streak",
                description="Use the trainer for 7 consecutive days",
                icon="🔥",
                criteria={"streak_days": {">=": 7}}
            )
        }
    
    def get_earned_badges(self, user_data: Dict) -> List[Badge]:
        """Return a list of badges the user has earned."""
        return [badge for badge in self.badges.values() if badge.is_earned(user_data)]
    
    def get_unearned_badges(self, user_data: Dict) -> List[Badge]:
        """Return a list of badges the user hasn't earned yet."""
        return [badge for badge in self.badges.values() if not badge.is_earned(user_data)]
    
    def display_badges(self, user_data: Dict):
        """Display the user's badges in a formatted table."""
        console = Console()
        earned_badges = self.get_earned_badges(user_data)
        unearned_badges = self.get_unearned_badges(user_data)
        
        # Display earned badges
        if earned_badges:
            table = Table(title="Your Badges", show_header=True, header_style="bold magenta")
            table.add_column("Badge", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Description")
            
            for badge in earned_badges:
                table.add_row(badge.icon, badge.name, badge.description)
            
            console.print(Panel(table, title="[bold]Earned Badges[/bold]"))
        
        # Display unearned badges (grayed out)
        if unearned_badges:
            table = Table(title="Available Badges", show_header=True, header_style="bold")
            table.add_column("Badge", style="dim")
            table.add_column("Name", style="dim")
            table.add_column("Description", style="dim")
            
            for badge in unearned_badges:
                table.add_row("🔒", f"[dim]{badge.name}", f"[dim]{badge.description}")
            
            console.print(Panel(table, title="[dim]Available Badges (locked)"))

class Leaderboard:
    """Manages and displays the leaderboard."""
    
    def __init__(self, profiles_dir: str = ".profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.scoreboard_file = self.profiles_dir / "scoreboard.json"
        self.badge_manager = BadgeManager()
        
        # Ensure profiles directory exists
        self.profiles_dir.mkdir(exist_ok=True)
        
        # Initialize scoreboard if it doesn't exist
        if not self.scoreboard_file.exists():
            self._init_scoreboard()
    
    def _init_scoreboard(self):
        """Initialize an empty scoreboard."""
        with open(self.scoreboard_file, 'w') as f:
            json.dump({"users": {}}, f, indent=2)
    
    def update_score(self, username: str, stats: Dict):
        """Update a user's score in the leaderboard."""
        try:
            # Load existing scoreboard
            with open(self.scoreboard_file, 'r') as f:
                scoreboard = json.load(f)
            
            # Update user's stats
            if "users" not in scoreboard:
                scoreboard["users"] = {}
            
            # Initialize user if not exists
            if username not in scoreboard["users"]:
                scoreboard["users"][username] = {
                    "challenges_completed": 0,
                    "modules_completed": 0,
                    "total_score": 0,
                    "last_activity": "",
                    "badges": []
                }
            
            # Update stats
            for key, value in stats.items():
                if key in scoreboard["users"][username]:
                    if isinstance(value, (int, float)):
                        scoreboard["users"][username][key] += value
                    else:
                        scoreboard["users"][username][key] = value
            
            # Update badges
            user_data = scoreboard["users"][username]
            earned_badges = self.badge_manager.get_earned_badges(user_data)
            user_data["badges"] = list(set([badge.id for badge in earned_badges]))
            
            # Save updated scoreboard
            with open(self.scoreboard_file, 'w') as f:
                json.dump(scoreboard, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error updating scoreboard: {e}")
            return False
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get the top users from the leaderboard."""
        try:
            with open(self.scoreboard_file, 'r') as f:
                scoreboard = json.load(f)
            
            # Sort users by total_score (descending)
            users = scoreboard.get("users", {})
            sorted_users = sorted(
                users.items(),
                key=lambda x: x[1].get("total_score", 0),
                reverse=True
            )
            
            # Format results
            result = []
            for i, (username, data) in enumerate(sorted_users[:limit], 1):
                result.append({
                    "rank": i,
                    "username": username,
                    "score": data.get("total_score", 0),
                    "challenges": data.get("challenges_completed", 0),
                    "badges": len(data.get("badges", [])),
                    "last_activity": data.get("last_activity", "Never")
                })
            
            return result
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []
    
    def display_leaderboard(self, limit: int = 10):
        """Display the leaderboard in a formatted table."""
        leaderboard = self.get_leaderboard(limit)
        
        if not leaderboard:
            print("No leaderboard data available yet.")
            return
        
        console = Console()
        table = Table(title="🏆 Leaderboard", show_header=True, header_style="bold magenta")
        
        # Add columns
        table.add_column("Rank", style="cyan")
        table.add_column("Username", style="green")
        table.add_column("Score", justify="right")
        table.add_column("Challenges", justify="right")
        table.add_column("Badges", justify="right")
        table.add_column("Last Active")
        
        # Add rows
        for entry in leaderboard:
            table.add_row(
                str(entry["rank"]),
                entry["username"],
                str(entry["score"]),
                str(entry["challenges"]),
                str(entry["badges"]),
                entry["last_activity"]
            )
        
        console.print(table)

# Global instance
badge_manager = BadgeManager()
leaderboard = Leaderboard()

if __name__ == "__main__":
    # Example usage
    test_user = "test_user"
    leaderboard.update_score(test_user, {"challenges_completed": 1, "total_score": 10})
    leaderboard.display_leaderboard()
    
    # Display badges for the test user
    badge_manager.display_badges({"challenges_completed": 1, "total_score": 10})
