"""
Tests for the lesson_runner module.
"""

import json
import os
import shutil
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from modules.lesson_runner import LessonRunner, run_lesson_interactive

# Test data
SAMPLE_LESSON = {
    "module": "test_lesson",
    "title": "Test Lesson",
    "description": "A test lesson",
    "lessons": [
        {
            "id": "step1",
            "title": "First Step",
            "content": "This is the first step.",
            "expected_input": "next"
        },
        {
            "id": "step2",
            "title": "Second Step",
            "content": "Run the command: echo hello",
            "command": "echo hello",
            "success_message": "Great job!"
        },
        {
            "id": "step3",
            "title": "Final Step",
            "content": "This is the final step.",
            "is_completion": True
        }
    ]
}


@pytest.fixture
def setup_lesson_files():
    """Set up test files and clean up after tests."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    lessons_dir = Path(temp_dir) / "data" / "lessons"
    lessons_dir.mkdir(parents=True)
    
    # Create a sample lesson file
    lesson_file = lessons_dir / "test_lesson.json"
    with open(lesson_file, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_LESSON, f)
    
    # Create a progress directory
    progress_dir = Path(temp_dir) / ".progress"
    progress_dir.mkdir()
    
    # Set environment variables for the test
    original_cwd = os.getcwd()
    os.chdir(temp_dir)
    
    yield temp_dir, lessons_dir, progress_dir
    
    # Clean up
    os.chdir(original_cwd)
    shutil.rmtree(temp_dir)


def test_lesson_runner_initialization(setup_lesson_files):
    """Test that LessonRunner initializes correctly."""
    temp_dir, _, _ = setup_lesson_files
    
    runner = LessonRunner()
    
    assert runner.lessons_dir == Path(temp_dir) / "data" / "lessons"
    assert runner.progress_file == Path(temp_dir) / ".progress" / "lesson_progress.json"
    assert runner.progress == {}


def test_load_lesson(setup_lesson_files):
    """Test loading a lesson from a file."""
    runner = LessonRunner()
    lesson = runner._load_lesson("test_lesson")
    
    assert lesson["module"] == "test_lesson"
    assert len(lesson["lessons"]) == 3
    assert lesson["lessons"][0]["id"] == "step1"


def test_save_and_load_progress(setup_lesson_files):
    """Test saving and loading progress."""
    runner = LessonRunner()
    
    # Initial progress should be empty
    assert runner.progress == {}
    
    # Add some progress
    runner.progress = {"test_lesson": {"completed_steps": [0, 1], "completed": False}}
    runner._save_progress()
    
    # Create a new runner to test loading
    new_runner = LessonRunner()
    assert new_runner.progress == {"test_lesson": {"completed_steps": [0, 1], "completed": False}}


def test_get_available_lessons(setup_lesson_files):
    """Test getting a list of available lessons."""
    runner = LessonRunner()
    lessons = runner.get_available_lessons()
    
    assert len(lessons) == 1
    assert lessons[0]["id"] == "test_lesson"
    assert lessons[0]["title"] == "Test Lesson"


def test_start_lesson(setup_lesson_files):
    """Test starting a lesson."""
    runner = LessonRunner()
    
    # Mock the console to capture output
    mock_console = MagicMock()
    runner.console = mock_console
    
    runner.start_lesson("test_lesson")
    
    # Check that the lesson was loaded correctly
    assert runner.current_lesson["module"] == "test_lesson"
    assert runner.current_step == 0
    
    # Check that progress was initialized
    assert "test_lesson" in runner.progress
    assert runner.progress["test_lesson"]["completed_steps"] == []
    assert not runner.progress["test_lesson"]["completed"]
    
    # Check that the first step was shown
    assert mock_console.print.called


def test_process_command_next(setup_lesson_files):
    """Test the 'next' command."""
    runner = LessonRunner()
    runner.start_lesson("test_lesson")
    
    # Process 'next' command
    should_continue = runner.process_command("next")
    
    assert should_continue is True
    assert runner.current_step == 1  # Should have advanced to the next step


def test_process_command_prev(setup_lesson_files):
    """Test the 'prev' command."""
    runner = LessonRunner()
    runner.start_lesson("test_lesson")
    runner.current_step = 1  # Move to second step
    
    # Process 'prev' command
    should_continue = runner.process_command("prev")
    
    assert should_continue is True
    assert runner.current_step == 0  # Should have gone back to the first step


def test_process_command_exit(setup_lesson_files):
    """Test the 'exit' command."""
    runner = LessonRunner()
    runner.start_lesson("test_lesson")
    
    # Process 'exit' command
    should_continue = runner.process_command("exit")
    
    assert should_continue is False  # Should signal to stop the lesson


def test_process_command_help(setup_lesson_files):
    """Test the 'help' command."""
    runner = LessonRunner()
    runner.start_lesson("test_lesson")
    
    # Mock the help method
    with patch.object(runner, '_show_help') as mock_help:
        should_continue = runner.process_command("help")
        
        assert should_continue is True
        mock_help.assert_called_once()


def test_process_command_lesson_command(setup_lesson_files):
    """Test processing a command that's part of the lesson."""
    runner = LessonRunner()
    runner.start_lesson("test_lesson")
    
    # Move to the second step which expects 'echo hello'
    runner.current_step = 1
    
    # Process the expected command
    should_continue = runner.process_command("echo hello")
    
    assert should_continue is True
    assert runner.current_step == 2  # Should have advanced to the next step
    assert 1 in runner.progress["test_lesson"]["completed_steps"]  # Step should be marked as completed


def test_run_lesson_interactive(setup_lesson_files):
    """Test the interactive lesson runner."""
    # Mock input to simulate user interaction
    with patch('builtins.input', side_effect=["next", "echo hello", "exit"]):
        # Mock the console to capture output
        mock_console = MagicMock()
        
        # Run the interactive lesson
        run_lesson_interactive("test_lesson", mock_console)
        
        # Check that the lesson was run
        assert mock_console.print.called
        
        # Check that the first step was shown
        # This is a bit fragile but verifies the lesson ran
        assert any("First Step" in str(call) for call in mock_console.print.call_args_list)
