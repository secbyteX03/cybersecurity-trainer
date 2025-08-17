"""
Badges and Leaderboard module for the Cybersecurity Trainer.

This module handles the tracking of user progress, awarding badges based on achievements,
and maintaining a local leaderboard of user scores and accomplishments.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Tuple, Union
import json
import os
from collections import defaultdict
import time

from rich.console import Console
from rich.table import Table, Column
from rich.box import ROUNDED
from rich.panel import Panel
from rich.text import Text
from rich.progress import track

# Constants
DEFAULT_PROFILES_DIR = ".profiles"
SCOREBOARD_FILE = "scoreboard.json"

@dataclass
class Badge:
    """
    Represents an achievement badge that can be earned by users.
    
    Attributes:
        id: Unique identifier for the badge
        name: Display name of the badge
        description: Description of how to earn the badge
        icon: Emoji or symbol to represent the badge
        criteria: Dictionary of criteria needed to earn the badge
        category: Category of the badge (e.g., 'challenges', 'modules', 'streak')
        points: Number of points awarded for earning this badge
    """
    id: str
    name: str
    description: str
    icon: str = "⭐"
    criteria: Dict[str, Any] = field(default_factory=dict)
    category: str = "general"
    points: int = 10
    
    def is_earned(self, user_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check if the user has earned this badge based on their data.
        
        Args:
            user_data: Dictionary containing user's progress data
            
        Returns:
            Tuple of (is_earned, messages) where messages contains details about
            which criteria were met or not met
        """
        messages = []
        
        # Special case: badge already earned
        if self.id in user_data.get('badges_earned', set()):
            return True, [f"Badge '{self.name}' already earned"]
            
        # Check each criterion
        for key, required_value in self.criteria.items():
            user_value = user_data.get(key, 0)
            
            # Handle nested criteria (e.g., challenges.completed > 5)
            if isinstance(required_value, dict):
                for op, value in required_value.items():
                    if op == ">" and not (user_value > value):
                        messages.append(f"{key} ({user_value}) is not greater than {value}")
                        return False, messages
                    elif op == ">=" and not (user_value >= value):
                        messages.append(f"{key} ({user_value}) is less than {value}")
                        return False, messages
                    elif op == "<" and not (user_value < value):
                        messages.append(f"{key} ({user_value}) is not less than {value}")
                        return False, messages
                    elif op == "<=" and not (user_value <= value):
                        messages.append(f"{key} ({user_value}) is greater than {value}")
                        return False, messages
                    elif op == "==" and user_value != value:
                        messages.append(f"{key} ({user_value}) is not equal to {value}")
                        return False, messages
                    elif op == "!=" and user_value == value:
                        messages.append(f"{key} ({user_value}) is equal to {value}")
                        return False, messages
                    elif op == "contains" and value not in user_value:
                        messages.append(f"{key} does not contain {value}")
                        return False, messages
                    messages.append(f"✓ {key} {op} {value} (has {user_value})")
            # Simple equality check
            elif user_value != required_value:
                messages.append(f"{key} is {user_value}, expected {required_value}")
                return False, messages
            else:
                messages.append(f"✓ {key} == {required_value}")
                
        return True, messages

class BadgeManager:
    """
    Manages the collection of available badges and handles badge-related operations.
    
    This class is responsible for:
    - Loading and managing the collection of available badges
    - Checking user progress against badge criteria
    - Awarding badges when criteria are met
    - Providing badge information and statistics
    """
    
    def __init__(self):
        """Initialize the BadgeManager and load available badges."""
        self.badges: Dict[str, Badge] = {}
        self._load_default_badges()
    
    def _load_default_badges(self):
        """Load the default set of badges with their criteria."""
        self.badges = {
            # Challenge Completion Badges
            "first_challenge": Badge(
                id="first_challenge",
                name="First Step",
                description="Complete your first challenge",
                icon="🎯",
                category="challenges",
                points=10,
                criteria={"challenges.completed": {">": 0}}
            ),
            "challenge_master": Badge(
                id="challenge_master",
                name="Challenge Master",
                description="Complete 10 challenges",
                icon="🏆",
                category="challenges",
                points=50,
                criteria={"challenges.completed": {">=": 10}}
            ),
            "perfect_score": Badge(
                id="perfect_score",
                name="Perfect Score",
                description="Get a perfect score on a challenge",
                icon="💯",
                category="challenges",
                points=25,
                criteria={"challenges.perfect_scores": {">": 0}}
            ),
            
            # Module Completion Badges
            "module_explorer": Badge(
                id="module_explorer",
                name="Module Explorer",
                description="Complete all challenges in a module",
                icon="🔍",
                category="modules",
                points=30,
                criteria={"modules.completed": {">": 0}}
            ),
            "jack_of_all_trades": Badge(
                id="jack_of_all_trades",
                name="Jack of All Trades",
                description="Complete at least one challenge in every module",
                icon="🎭",
                category="modules",
                points=75,
                criteria={"modules.touched_count": {">=": 5}}  # Assuming 5+ modules
            ),
            
            # Streak Badges
            "streak_3_days": Badge(
                id="streak_3_days",
                name="Three Day Streak",
                description="Maintain a 3-day learning streak",
                icon="🔥",
                category="streak",
                points=15,
                criteria={"streak.current": {">=": 3}}
            ),
            "streak_7_days": Badge(
                id="streak_7_days",
                name="One Week Streak",
                description="Maintain a 7-day learning streak",
                icon="🚀",
                category="streak",
                points=35,
                criteria={"streak.current": {">=": 7}}
            ),
            
            # Special Achievement Badges
            "early_bird": Badge(
                id="early_bird",
                name="Early Bird",
                description="Complete a challenge before 9 AM",
                icon="🌅",
                category="special",
                points=20,
                criteria={"has_early_bird_achievement": True}
            ),
            "night_owl": Badge(
                id="night_owl",
                name="Night Owl",
                description="Complete a challenge after 10 PM",
                icon="🦉",
                category="special",
                points=20,
                criteria={"has_night_owl_achievement": True}
            ),
            "weekend_warrior": Badge(
                id="weekend_warrior",
                name="Weekend Warrior",
                description="Complete a challenge on both weekend days",
                icon="🏋️",
                category="special",
                points=30,
                criteria={"has_weekend_warrior_achievement": True}
            )
        }
    
    def get_badge(self, badge_id: str) -> Optional[Badge]:
        """
        Retrieve a badge by its ID.
        
        Args:
            badge_id: The ID of the badge to retrieve
            
        Returns:
            The Badge object if found, None otherwise
        """
        return self.badges.get(badge_id)
    
    def get_all_badges(self) -> List[Badge]:
        """
        Get a list of all available badges.
        
        Returns:
            List of all Badge objects
        """
        return list(self.badges.values())
    
    def get_badges_by_category(self, category: str) -> List[Badge]:
        """
        Get all badges in a specific category.
        
        Args:
            category: The category to filter by (e.g., 'challenges', 'streak')
            
        Returns:
            List of Badge objects in the specified category
        """
        return [badge for badge in self.badges.values() if badge.category == category]
    
    def check_badge_progress(self, badge_id: str, user_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check if a user has earned a specific badge based on their progress.
        
        Args:
            badge_id: The ID of the badge to check
            user_data: Dictionary containing the user's progress data
            
        Returns:
            Tuple of (is_earned, messages) indicating if the badge was earned and any relevant messages
        """
        badge = self.get_badge(badge_id)
        if not badge:
            return False, [f"Badge with ID '{badge_id}' not found"]
        
        return badge.is_earned(user_data)
    
    def get_earned_badges(self, user_data: Dict[str, Any]) -> List[Badge]:
        """
        Get a list of all badges that the user has earned.
        
        Args:
            user_data: Dictionary containing the user's progress data
            
        Returns:
            List of Badge objects that the user has earned
        """
        earned_badges = []
        for badge in self.badges.values():
            is_earned, _ = badge.is_earned(user_data)
            if is_earned:
                earned_badges.append(badge)
        return earned_badges
    
    def get_potential_badges(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get a list of badges the user is close to earning.
        
        Args:
            user_data: Dictionary containing the user's progress data
            
        Returns:
            List of dictionaries containing badge and progress information
        """
        potential = []
        for badge in self.badges.values():
            is_earned, _ = badge.is_earned(user_data)
            if not is_earned:
                # Check if user is making progress toward this badge
                progress = self._calculate_badge_progress(badge, user_data)
                if progress > 0:
                    potential.append({
                        'badge': badge,
                        'progress': progress,
                        'next_steps': self._get_next_steps(badge, user_data)
                    })
        
        # Sort by progress (descending)
        return sorted(potential, key=lambda x: x['progress'], reverse=True)
    
    def _calculate_badge_progress(self, badge: Badge, user_data: Dict[str, Any]) -> float:
        """
        Calculate the user's progress toward earning a badge.
        
        Args:
            badge: The badge to check progress for
            user_data: Dictionary containing the user's progress data
            
        Returns:
            A float between 0 and 1 representing the progress (0% to 100%)
        """
        if not badge.criteria:
            return 0.0
        
        total_criteria = len(badge.criteria)
        met_criteria = 0
        
        for key, required_value in badge.criteria.items():
            user_value = user_data.get(key, 0)
            
            if isinstance(required_value, dict):
                # Handle comparison operators
                for op, value in required_value.items():
                    try:
                        if op == ">" and user_value > value:
                            met_criteria += 1
                        elif op == ">=" and user_value >= value:
                            met_criteria += 1
                        elif op == "<" and user_value < value:
                            met_criteria += 1
                        elif op == "<=" and user_value <= value:
                            met_criteria += 1
                        elif op == "==" and user_value == value:
                            met_criteria += 1
                        elif op == "!=" and user_value != value:
                            met_criteria += 1
                        elif op == "contains" and value in user_value:
                            met_criteria += 1
                    except (TypeError, ValueError):
                        # Skip invalid comparisons
                        continue
            elif user_value == required_value:
                met_criteria += 1
        
        return met_criteria / total_criteria if total_criteria > 0 else 0.0
    
    def _get_next_steps(self, badge: Badge, user_data: Dict[str, Any]) -> List[str]:
        """
        Get a list of next steps to earn a badge.
        
        Args:
            badge: The badge to get next steps for
            user_data: Dictionary containing the user's progress data
            
        Returns:
            List of strings describing what the user needs to do to earn the badge
        """
        next_steps = []
        
        for key, required_value in badge.criteria.items():
            user_value = user_data.get(key, 0)
            
            if isinstance(required_value, dict):
                for op, value in required_value.items():
                    if op == ">" and user_value <= value:
                        next_steps.append(f"Increase {key} to more than {value} (current: {user_value})")
                    elif op == ">=" and user_value < value:
                        next_steps.append(f"Increase {key} to at least {value} (current: {user_value})")
                    elif op == "<" and user_value >= value:
                        next_steps.append(f"Decrease {key} to less than {value} (current: {user_value})")
                    elif op == "<=" and user_value > value:
                        next_steps.append(f"Decrease {key} to at most {value} (current: {user_value})")
                    elif op == "==" and user_value != value:
                        next_steps.append(f"Set {key} to exactly {value} (current: {user_value})")
                    elif op == "!=" and user_value == value:
                        next_steps.append(f"Change {key} from {value}")
                    elif op == "contains" and value not in user_value:
                        next_steps.append(f"Ensure {key} contains {value}")
            elif user_value != required_value:
                next_steps.append(f"Set {key} to {required_value} (current: {user_value})")
        
        return next_steps
    
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
            with open(self.scoreboard_file, 'r+') as f:
                try:
                    scoreboard = json.load(f)
                except json.JSONDecodeError:
                    scoreboard = {"users": {}}
                
                # Initialize users dictionary if it doesn't exist
                if "users" not in scoreboard:
                    scoreboard["users"] = {}
                
                # Initialize user if not exists
                if username not in scoreboard["users"]:
                    scoreboard["users"][username] = {
                        "challenges.completed": 0,
                        "challenges.perfect_scores": 0,
                        "modules.completed": 0,
                        "modules.touched_count": 0,
                        "streak.current": 0,
                        "total_score": 0,
                        "last_activity": "",
                        "badges": []
                    }
                
                # Update stats
                for key, value in stats.items():
                    if key in scoreboard["users"][username]:
                        if isinstance(value, (int, float)) and key != "last_activity":
                            scoreboard["users"][username][key] += value
                        else:
                            scoreboard["users"][username][key] = value
                
                # Update last activity if not set in stats
                if "last_activity" not in stats:
                    scoreboard["users"][username]["last_activity"] = datetime.now(timezone.utc).isoformat()
                
                # Update badges
                user_data = scoreboard["users"][username].copy()
                badges_earned = set(user_data.get("badges", []))
                
                # Check for new badges
                new_badges = []
                for badge in self.badge_manager.get_all_badges():
                    is_earned, _ = badge.is_earned(user_data)
                    if is_earned and badge.id not in badges_earned:
                        new_badges.append(badge.id)
                
                # Update user's badges (convert set to list for JSON serialization)
                if new_badges:
                    user_data["badges"] = list(set(user_data.get("badges", []) + new_badges))
                    scoreboard["users"][username].update(user_data)
                
                # Save updated scoreboard
                f.seek(0)
                json.dump(scoreboard, f, indent=2)
                f.truncate()
                
                return True
                
        except Exception as e:
            print(f"Error updating scoreboard: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get the top users from the leaderboard."""
        try:
            with open(self.scoreboard_file, 'r') as f:
                try:
                    scoreboard = json.load(f)
                except json.JSONDecodeError:
                    return []
            
            # Sort users by total_score (descending)
            users = scoreboard.get("users", {})
            sorted_users = sorted(
                users.items(),
                key=lambda x: x[1].get("total_score", 0),
                reverse=True
            )
            
            # Format results
            result = []
            for i, (username, data) in enumerate(sorted_users, 1):
                if limit > 0 and len(result) >= limit:
                    break
                    
                result.append({
                    "rank": i,
                    "username": username,
                    "score": data.get("total_score", 0),
                    "challenges": data.get("challenges.completed", 0),
                    "badges": len(data.get("badges", [])),
                    "last_activity": data.get("last_activity", "Never")
                })
            
            return result
            
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def display_leaderboard(self, limit: int = 10):
        """Display the leaderboard in a formatted table."""
        leaderboard = self.get_leaderboard(limit)
        
        if not leaderboard:
            print("No leaderboard data available yet.")
            return
        
        console = Console()
        table = Table(
            title="🏆 Leaderboard", 
            show_header=True, 
            header_style="bold magenta",
            box=ROUNDED,
            expand=True
        )
        
        # Add columns
        table.add_column("Rank", style="cyan", justify="center")
        table.add_column("Username", style="green")
        table.add_column("Score", justify="right", style="yellow")
        table.add_column("Challenges", justify="right")
        table.add_column("Badges", justify="right")
        table.add_column("Last Active", justify="center")
        
        # Add rows
        for entry in leaderboard:
            last_active = entry.get("last_activity", "Never")
            if last_active != "Never":
                try:
                    last_active = datetime.fromisoformat(last_active.replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")
                except (ValueError, AttributeError):
                    pass  # Keep original value if parsing fails
                
            table.add_row(
                f"[bold]{entry['rank']}.",
                f"[bold]{entry['username']}",
                f"[bold yellow]{entry['score']:,}",
                str(entry['challenges']),
                f"[cyan]{entry['badges']}",
                str(last_active)
            )
        
        console.print(table)
    
    def get_user_stats(self, username: str) -> Optional[Dict]:
        """Get detailed statistics for a specific user."""
        try:
            with open(self.scoreboard_file, 'r') as f:
                try:
                    scoreboard = json.load(f)
                except json.JSONDecodeError:
                    return None
            
            return scoreboard.get("users", {}).get(username)
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return None
    
    def get_user_rank(self, username: str) -> Optional[int]:
        """Get the current rank of a user."""
        leaderboard = self.get_leaderboard(0)  # 0 means no limit
        for entry in leaderboard:
            if entry["username"] == username:
                return entry["rank"]
        return None
    
    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """Get recent activities across all users."""
        try:
            with open(self.scoreboard_file, 'r') as f:
                try:
                    scoreboard = json.load(f)
                except json.JSONDecodeError:
                    return []
            
            activities = []
            for username, data in scoreboard.get("users", {}).items():
                if "last_activity" in data and data["last_activity"]:
                    try:
                        timestamp = datetime.fromisoformat(data["last_activity"].replace('Z', '+00:00')).timestamp()
                        activities.append({
                            "username": username,
                            "activity": data["last_activity"],
                            "timestamp": timestamp
                        })
                    except (ValueError, AttributeError):
                        continue  # Skip invalid timestamps
            
            # Sort by timestamp (newest first) and limit results
            activities.sort(key=lambda x: x["timestamp"], reverse=True)
            return activities[:limit]
            
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return []
    
    def award_badges(self, username: str) -> List[Badge]:
        """Award any new badges the user has earned."""
        try:
            with open(self.scoreboard_file, 'r+') as f:
                try:
                    scoreboard = json.load(f)
                except json.JSONDecodeError:
                    return []
                
                if "users" not in scoreboard or username not in scoreboard["users"]:
                    return []
                
                user_data = scoreboard["users"][username].copy()
                user_data["badges_earned"] = set(user_data.get("badges", []))
                
                # Check for new badges
                new_badges = []
                for badge in self.badge_manager.get_all_badges():
                    is_earned, _ = badge.is_earned(user_data)
                    if is_earned and badge.id not in user_data["badges_earned"]:
                        new_badges.append(badge)
                        user_data["badges"].append(badge.id)
                
                # Update user data if new badges were awarded
                if new_badges:
                    scoreboard["users"][username] = user_data
                    f.seek(0)
                    json.dump(scoreboard, f, indent=2)
                    f.truncate()
                
                return new_badges
                
        except Exception as e:
            print(f"Error awarding badges: {e}")
            return []
    
    def get_badge_progress(self, username: str) -> List[Dict]:
        """Get progress for all badges for a user."""
        user_data = self.get_user_stats(username)
        if not user_data:
            return []
        
        badges_progress = []
        user_data["badges_earned"] = set(user_data.get("badges", []))
        
        for badge in self.badge_manager.get_all_badges():
            is_earned, messages = badge.is_earned(user_data)
            progress = self.badge_manager._calculate_badge_progress(badge, user_data)
            next_steps = self.badge_manager._get_next_steps(badge, user_data)
            
            badges_progress.append({
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon,
                "earned": is_earned,
                "progress": progress,
                "next_steps": next_steps
            })
        
        return badges_progress

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
