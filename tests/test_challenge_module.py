"""
Tests for the ChallengeModule class.
"""
import pytest
from unittest.mock import patch, MagicMock
from modules.challenge import ChallengeModule
from modules.challenge_loader import ChallengeLoader

def test_challenge_module_initialization():
    """Test ChallengeModule initialization."""
    user_progress = {'basics': 5, 'networking': 3}
    challenge_module = ChallengeModule(user_progress)
    
    assert challenge_module.user_progress == user_progress
    assert challenge_module.completed_challenges == []
    assert challenge_module.hints_used == {}
    assert isinstance(challenge_module.challenge_loader, ChallengeLoader)

def test_display_challenge_info(capsys):
    """Test displaying challenge information."""
    challenge_module = ChallengeModule({})
    test_challenge = {
        'title': 'Test Challenge',
        'description': 'A test challenge',
        'difficulty': 'easy',
        'points': 50,
        'task': 'Complete the task'
    }
    
    challenge_module._display_challenge_info(test_challenge)
    captured = capsys.readouterr()
    
    assert 'Test Challenge' in captured.out
    assert 'easy' in captured.out
    assert '50' in captured.out
    assert 'Complete the task' in captured.out

@patch('modules.challenge.console')
def test_show_hint(mock_console):
    """Test showing hints."""
    challenge_module = ChallengeModule({})
    test_challenge = {
        'id': 'test_challenge',
        'hints': ['First hint', 'Second hint', 'Third hint']
    }
    
    # Test first hint
    challenge_module._show_hint(test_challenge, 0)
    mock_console.print.assert_called_with('\n[bold]Hint (1/3):[/] First hint')
    assert 'test_challenge' in challenge_module.hints_used
    assert 0 in challenge_module.hints_used['test_challenge']
    
    # Test second hint
    challenge_module._show_hint(test_challenge, 1)
    mock_console.print.assert_called_with('\n[bold]Hint (2/3):[/] Second hint')
    assert 1 in challenge_module.hints_used['test_challenge']
    
    # Test hint level out of bounds
    mock_console.reset_mock()
    challenge_module._show_hint(test_challenge, 5)
    mock_console.print.assert_called_with('\n[bold]Hint (3/3):[/] Third hint')

def test_validate_solution():
    """Test solution validation through the challenge module."""
    challenge_module = ChallengeModule({})
    challenge_module.challenge_loader = MagicMock()
    
    # Mock the loader's validate_solution
    challenge_module.challenge_loader.validate_solution.return_value = {
        'success': True,
        'message': 'Success!',
        'points': 50
    }
    
    # Test with a valid challenge ID
    result = challenge_module.challenge_loader.validate_solution('test_challenge', ['command'])
    assert result['success'] is True
    challenge_module.challenge_loader.validate_solution.assert_called_once_with(
        'test_challenge', ['command']
    )

def test_on_challenge_complete(capsys):
    """Test challenge completion handling."""
    challenge_module = ChallengeModule({})
    test_challenge = {
        'id': 'test_challenge',
        'success_message': 'Great job!',
        'resources': ['Resource 1', 'Resource 2']
    }
    
    challenge_module._on_challenge_complete(test_challenge, {'points': 50})
    captured = capsys.readouterr()
    
    assert '🎉 Challenge Completed!' in captured.out
    assert '50' in captured.out
    assert 'Great job!' in captured.out
    assert 'Resource 1' in captured.out
    assert 'Resource 2' in captured.out
    assert 'test_challenge' in challenge_module.completed_challenges

@patch('modules.challenge.console')
@patch('modules.challenge.Prompt.ask')
def test_run_challenge_commands(mock_ask, mock_console):
    """Test command input handling."""
    challenge_module = ChallengeModule({})
    
    # Test normal command input
    mock_ask.side_effect = ['command1', 'command2', 'submit']
    result = challenge_module._run_challenge_commands()
    assert result == ['command1', 'command2']
    
    # Test empty command
    mock_ask.side_effect = ['', 'command', 'submit']
    result = challenge_module._run_challenge_commands()
    assert result == ['command']
    
    # Test exit
    mock_ask.side_effect = ['command', 'exit']
    mock_console.print = MagicMock()
    with patch('builtins.input', return_value='y'):
        result = challenge_module._run_challenge_commands()
    assert result is None
