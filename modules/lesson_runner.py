"""
Lesson Runner Module

Handles the execution of guided lessons, including loading lessons from JSON files,
managing progress, and providing an interactive learning experience.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

class LessonRunner:
    """Handles the execution of guided lessons."""
    
    def __init__(self, console: Optional[Console] = None):
        """Initialize the LessonRunner.
        
        Args:
            console: Optional Rich Console instance for output
        """
        self.console = console or Console()
        self.lessons_dir = Path("data/lessons")
        self.progress_file = Path(".progress/lesson_progress.json")
        self.current_lesson = None
        self.current_step = 0
        self.progress = self._load_progress()
        
    def _load_lesson(self, lesson_id: str) -> Dict:
        """Load a lesson from a JSON file.
        
        Args:
            lesson_id: ID of the lesson to load
            
        Returns:
            Dict containing the lesson data
            
        Raises:
            FileNotFoundError: If the lesson file doesn't exist
            json.JSONDecodeError: If the lesson file is invalid JSON
        """
        lesson_file = self.lessons_dir / f"{lesson_id}.json"
        with open(lesson_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_progress(self) -> Dict:
        """Load the user's lesson progress.
        
        Returns:
            Dict containing the user's progress
        """
        if not self.progress_file.exists():
            return {}
            
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_progress(self):
        """Save the user's lesson progress to disk."""
        # Ensure the .progress directory exists
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_available_lessons(self) -> List[Dict[str, str]]:
        """Get a list of available lessons.
        
        Returns:
            List of dicts containing lesson metadata
        """
        if not self.lessons_dir.exists():
            return []
            
        lessons = []
        for file in self.lessons_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lesson_data = json.load(f)
                    lessons.append({
                        'id': file.stem,
                        'title': lesson_data.get('title', 'Untitled Lesson'),
                        'description': lesson_data.get('description', '')
                    })
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
                
        return lessons
    
    def start_lesson(self, lesson_id: str):
        """Start a new lesson.
        
        Args:
            lesson_id: ID of the lesson to start
        """
        try:
            self.current_lesson = self._load_lesson(lesson_id)
            self.current_step = 0
            
            # Initialize progress if this is the first time
            if lesson_id not in self.progress:
                self.progress[lesson_id] = {
                    'completed_steps': [],
                    'completed': False,
                    'current_step': 0
                }
            
            self._show_current_step()
            
        except FileNotFoundError:
            self.console.print(f"[red]Error:[/red] Lesson '{lesson_id}' not found.")
            return
        except json.JSONDecodeError:
            self.console.print(f"[red]Error:[/red] Invalid lesson file for '{lesson_id}'.")
            return
    
    def _show_current_step(self):
        """Display the current step of the current lesson."""
        if not self.current_lesson or not self.current_lesson['lessons']:
            self.console.print("[yellow]No lesson is currently loaded.[/yellow]")
            return
            
        step = self.current_lesson['lessons'][self.current_step]
        
        # Clear the console for a cleaner look
        self.console.clear()
        
        # Show lesson title and progress
        progress = f"[cyan]Step {self.current_step + 1} of {len(self.current_lesson['lessons'])}[/cyan]"
        title = f"[bold]{self.current_lesson['title']} - {step['title']}[/bold] {progress}"
        self.console.print(Panel(title, style="blue"))
        
        # Show the lesson content with markdown support
        self.console.print(Markdown(step['content']))
        
        # Show available commands
        self.console.print("\n[dim]Commands: next, prev, exit, help[/dim]")
    
    def process_command(self, command: str) -> bool:
        """Process a user command.
        
        Args:
            command: The command entered by the user
            
        Returns:
            bool: True if the lesson should continue, False if it should end
        """
        if not self.current_lesson:
            self.console.print("[yellow]No active lesson. Start a lesson first.[/yellow]")
            return True
            
        command = command.strip().lower()
        
        if command == 'exit':
            return False
            
        if command == 'help':
            self._show_help()
            return True
            
        if command == 'next':
            return self._next_step()
            
        if command == 'prev':
            return self._prev_step()
            
        # Check if this is a command the lesson expects
        current_step = self.current_lesson['lessons'][self.current_step]
        if 'command' in current_step and command == current_step['command']:
            self.console.print(f"[green]✓ {current_step.get('success_message', 'Correct!')}[/green]")
            
            # Mark this step as completed if not already
            lesson_id = self.current_lesson['module']
            if self.current_step not in self.progress[lesson_id]['completed_steps']:
                self.progress[lesson_id]['completed_steps'].append(self.current_step)
                self._save_progress()
                
            # If this was the last step, mark the lesson as complete
            if self.current_step == len(self.current_lesson['lessons']) - 1:
                self.progress[lesson_id]['completed'] = True
                self._save_progress()
                
            return self._next_step()
            
        # If we get here, the command wasn't recognized
        self.console.print("[yellow]Command not recognized. Type 'help' for available commands.[/yellow]")
        return True
    
    def _next_step(self) -> bool:
        """Advance to the next step in the lesson.
        
        Returns:
            bool: True if there are more steps, False if the lesson is complete
        """
        if self.current_step < len(self.current_lesson['lessons']) - 1:
            self.current_step += 1
            self._show_current_step()
            return True
        else:
            self.console.print("[green]🎉 Lesson complete![/green]")
            return False
    
    def _prev_step(self) -> bool:
        """Go back to the previous step in the lesson.
        
        Returns:
            bool: True (always continues the lesson)
        """
        if self.current_step > 0:
            self.current_step -= 1
            self._show_current_step()
        else:
            self.console.print("[yellow]This is the first step.[/yellow]")
        return True
    
    def _show_help(self):
        """Display help information."""
        help_text = """
        [bold]Available Commands:[/bold]
        
        [cyan]next[/cyan]      - Go to the next step
        [cyan]prev[/cyan]      - Go to the previous step
        [cyan]exit[/cyan]      - Exit the current lesson
        [cyan]help[/cyan]      - Show this help message
        
        Follow the instructions in each step to complete the lesson.
        Type commands exactly as shown to proceed.
        """
        self.console.print(Panel(Markdown(help_text), title="Help", border_style="blue"))


def run_lesson_interactive(lesson_id: str, console: Optional[Console] = None):
    """Run a lesson in interactive mode.
    
    Args:
        lesson_id: ID of the lesson to run
        console: Optional Rich Console instance for output
    """
    runner = LessonRunner(console)
    runner.start_lesson(lesson_id)
    
    while True:
        try:
            command = input("\n> ").strip()
            if not runner.process_command(command):
                break
        except KeyboardInterrupt:
            print("\nExiting lesson...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            break


if __name__ == "__main__":
    # Example usage
    console = Console()
    console.print("[bold]Available Lessons:[/bold]")
    
    runner = LessonRunner(console)
    lessons = runner.get_available_lessons()
    
    if not lessons:
        console.print("[yellow]No lessons found.[/yellow]")
    else:
        for i, lesson in enumerate(lessons, 1):
            console.print(f"{i}. [cyan]{lesson['title']}[/cyan] - {lesson['description']}")
        
        try:
            choice = int(input("\nSelect a lesson number: ")) - 1
            if 0 <= choice < len(lessons):
                run_lesson_interactive(lessons[choice]['id'], console)
            else:
                console.print("[red]Invalid selection.[/red]")
        except ValueError:
            console.print("[red]Please enter a number.[/red]")
