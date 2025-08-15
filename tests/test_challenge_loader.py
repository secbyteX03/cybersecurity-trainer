"""
Tests for the ChallengeLoader class.
"""
import os
import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, mock_open

from modules.challenge_loader import ChallengeLoader

def test_load_challenges():
    """Test loading challenges from YAML files."""
    # Create a temporary directory with a test challenge
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test challenge file
        test_challenge = {
            'id': 'test_challenge',
            'title': 'Test Challenge',
            'description': 'A test challenge',
            'difficulty': 'easy',
            'points': 50,
            'prerequisites': {'basics': 3},
            'solution': {
                'commands': ['echo "test"']
            },
            'hints': ['First hint', 'Second hint']
        }
        
        challenge_path = Path(temp_dir) / "test_challenge.yaml"
        with open(challenge_path, 'w') as f:
            yaml.dump(test_challenge, f)
        
        # Test loading
        loader = ChallengeLoader(temp_dir)
        assert 'test_challenge' in loader.challenges
        assert loader.challenges['test_challenge']['title'] == 'Test Challenge'

def test_get_available_challenges():
    """Test filtering available challenges based on user progress."""
    # Create a loader with mock challenges
    loader = ChallengeLoader()
    loader.challenges = {
        'easy_challenge': {
            'id': 'easy_challenge',
            'prerequisites': {'basics': 2},
            'title': 'Easy Challenge'
        },
        'medium_challenge': {
            'id': 'medium_challenge',
            'prerequisites': {'basics': 5, 'networking': 3},
            'title': 'Medium Challenge'
        },
        'hard_challenge': {
            'id': 'hard_challenge',
            'prerequisites': {'basworking': 10},
            'title': 'Hard Challenge'
        }
    }
    
    # Test with different user progress levels
    user_progress_1 = {'basics': 3, 'networking': 1}
    available_1 = loader.get_available_challenges(user_progress_1)
    assert len(available_1) == 1
    assert available_1[0]['id'] == 'easy_challenge'
    
    user_progress_2 = {'basics': 5, 'networking': 3}
    available_2 = loader.get_available_challenges(user_progress_2)
    assert len(available_2) == 2
    assert 'easy_challenge' in [c['id'] for c in available_2]
    assert 'medium_challenge' in [c['id'] for c in available_2]

def test_validate_solution():
    """Test solution validation."""
    loader = ChallengeLoader()
    loader.challenges = {
        'test_challenge': {
            'id': 'test_challenge',
            'solution': {
                'commands': ['echo "test"', 'ls -la']
            }
        }
    }
    
    # Test with correct commands
    result = loader.validate_solution('test_challenge', ['echo "test"', 'ls -la'])
    assert result['success'] is True
    
    # Test with missing commands
    result = loader.validate_solution('test_challenge', ['echo "test"'])
    assert result['success'] is False
    assert 'ls -la' in result['hint']
    
    # Test with extra commands
    result = loader.validate_solution('test_challenge', ['echo "test"', 'ls -la', 'extra'])
    assert result['success'] is True  # Extra commands are allowed
    
    # Test with non-existent challenge
    result = loader.validate_solution('no_such_challenge', [])
    assert result['success'] is False
    assert 'not found' in result['message']
