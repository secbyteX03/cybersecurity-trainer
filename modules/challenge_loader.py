"""
Challenge Loader - Loads and manages cybersecurity challenges from YAML files.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any

class ChallengeLoader:
    def __init__(self, challenges_dir: str = "data/challenges"):
        """Initialize the challenge loader with the directory containing challenge YAML files."""
        self.challenges_dir = Path(challenges_dir)
        self.challenges: Dict[str, Dict] = {}
        self._load_challenges()
    
    def _load_challenges(self) -> None:
        """Load all challenge definitions from YAML files."""
        if not self.challenges_dir.exists():
            return
            
        for yaml_file in self.challenges_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    challenge = yaml.safe_load(f)
                    if 'id' in challenge:
                        self.challenges[challenge['id']] = challenge
            except Exception as e:
                print(f"Error loading challenge {yaml_file}: {e}")
    
    def get_challenge(self, challenge_id: str) -> Optional[Dict]:
        """Get a specific challenge by ID."""
        return self.challenges.get(challenge_id)
    
    def get_available_challenges(self, user_progress: Dict[str, int]) -> List[Dict]:
        """Get all challenges that the user can attempt based on their progress."""
        available = []
        
        for challenge in self.challenges.values():
            can_attempt = True
            
            # Check prerequisites
            for module, min_score in challenge.get('prerequisites', {}).items():
                if user_progress.get(module, 0) < min_score:
                    can_attempt = False
                    break
            
            if can_attempt:
                available.append(challenge)
        
        return available
    
    def validate_solution(self, challenge_id: str, commands: List[str]) -> Dict[str, Any]:
        """
        Validate if the provided commands solve the challenge.
        Returns a dictionary with validation results.
        """
        challenge = self.get_challenge(challenge_id)
        if not challenge:
            return {
                'success': False,
                'message': 'Challenge not found',
                'hint': None
            }
        
        solution_commands = set(cmd.strip().lower() for cmd in challenge['solution']['commands'])
        user_commands = set(cmd.strip().lower() for cmd in commands)
        
        # Check if all required commands were used
        missing_commands = solution_commands - user_commands
        
        if missing_commands:
            return {
                'success': False,
                'message': 'Not all required commands were used',
                'hint': f'Try using these commands: {", ".join(missing_commands)}',
                'missing_commands': list(missing_commands)
            }
        
        return {
            'success': True,
            'message': 'Challenge completed successfully!',
            'points': challenge.get('points', 0)
        }
