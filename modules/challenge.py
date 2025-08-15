"""
Challenge Module - Hands-on cybersecurity scenarios with auto-grader and hints
"""
import os
import time
from typing import List, Dict, Any
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.markdown import Markdown

from .challenge_loader import ChallengeLoader

console = Console()

class ChallengeModule:
    def __init__(self, user_progress):
        """Initialize the Challenge Module with user progress tracking."""
        self.user_progress = user_progress
        self.completed_challenges = user_progress.get('challenges_completed', [])
        self.hints_used = {}
        self.challenge_loader = ChallengeLoader()
        self.current_challenge = None

    def _display_challenge_info(self, challenge: Dict) -> None:
        """Display challenge information and description."""
        console.print(Panel.fit(
            f"[bold]{challenge['title']}[/bold]\n"
            f"Difficulty: {challenge.get('difficulty', 'medium')} | "
            f"Points: {challenge.get('points', 50)}",
            style="blue"
        ))
        
        console.print(Markdown(challenge['description']))
        console.print("\n[bold]Your task:[/] " + challenge.get('task', 'Complete the challenge'))
    
    def _show_hint(self, challenge: Dict, hint_level: int) -> None:
        """Show a hint for the current challenge."""
        hints = challenge.get('hints', [])
        if not hints:
            console.print("[yellow]No hints available for this challenge.[/]")
            return
            
        hint_level = min(hint_level, len(hints) - 1)
        console.print(f"\n[bold]Hint ({hint_level + 1}/{len(hints)}):[/] " + hints[hint_level])
        
        # Track hints used
        if challenge['id'] not in self.hints_used:
            self.hints_used[challenge['id']] = []
        if hint_level not in self.hints_used[challenge['id']]:
            self.hints_used[challenge['id']].append(hint_level)
    
    def _run_challenge_commands(self) -> List[str]:
        """Run the challenge and collect user commands."""
        console.print("\n[bold]Enter your commands (one per line, 'submit' when done):[/]")
        commands = []
        
        while True:
            try:
                cmd = Prompt.ask("\n> ").strip()
                if not cmd:
                    continue
                    
                if cmd.lower() == 'submit':
                    if not commands:
                        console.print("[yellow]No commands entered. Type 'exit' to quit.[/]")
                        continue
                    return commands
                    
                if cmd.lower() == 'exit':
                    if Confirm.ask("\nAre you sure you want to quit this challenge?"):
                        return None
                    continue
                    
                commands.append(cmd)
                
            except KeyboardInterrupt:
                if Confirm.ask("\nAre you sure you want to quit this challenge?"):
                    return None
    
    def run_challenge(self, challenge_id: str) -> bool:
        """Run a specific challenge with auto-grader and hints."""
        challenge = self.challenge_loader.get_challenge(challenge_id)
        if not challenge:
            console.print(f"[red]Challenge '{challenge_id}' not found.[/]")
            return False
            
        self.current_challenge = challenge
        console.clear()
        
        # Display challenge info
        self._display_challenge_info(challenge)
        
        hint_level = -1  # Start with no hint
        
        while True:
            # Show available commands
            console.print("\n[bold]Available commands:[/]")
            console.print("- Type your command and press Enter")
            console.print("- 'hint' - Get a hint")
            console.print("- 'submit' - Submit your solution")
            console.print("- 'exit' - Quit the challenge")
            
            # Run the challenge
            commands = self._run_challenge_commands()
            if commands is None:  # User chose to exit
                return False
                
            # Validate solution
            result = self.challenge_loader.validate_solution(challenge_id, commands)
            
            if result['success']:
                self._on_challenge_complete(challenge, result)
                return True
            else:
                console.print(f"\n[red]{result['message']}[/]")
                if 'hint' in result:
                    console.print(f"[yellow]Hint: {result['hint']}[/]")
                
                # Offer another hint
                if Confirm.ask("\nWould you like to see a hint?"):
                    hint_level = min(hint_level + 1, 2)  # Max 3 hints (0, 1, 2)
                    self._show_hint(challenge, hint_level)
    
    def _on_challenge_complete(self, challenge: Dict, result: Dict) -> None:
        """Handle challenge completion."""
        console.print("\n" + "=" * 60)
        console.print("[bold green]🎉 Challenge Completed! 🎉[/]")
        console.print(f"[bold]Points earned:[/] {result.get('points', 0)}")
        
        # Show success message
        if 'success_message' in challenge:
            console.print("\n" + challenge['success_message'])
        
        # Update completed challenges
        if challenge['id'] not in self.completed_challenges:
            self.completed_challenges.append(challenge['id'])
            
        # Show resources for further learning
        if 'resources' in challenge and challenge['resources']:
            console.print("\n[bold]Learn more:[/]")
            for resource in challenge['resources']:
                console.print(f"- {resource}")
    
    def list_available_challenges(self) -> List[Dict]:
        """List all challenges the user can attempt."""
        return self.challenge_loader.get_available_challenges(self.user_progress)
        
    def _display_challenge_list(self) -> None:
        """Display available challenges in a formatted table."""
        challenges = self.list_available_challenges()
        
        if not challenges:
            console.print("\n[yellow]No challenges available. Complete more modules to unlock challenges![/]")
            return []
            
        table = Table(title="Available Challenges", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Challenge", style="green")
        table.add_column("Difficulty", style="yellow")
        table.add_column("Points", style="blue")
        table.add_column("Status", style="cyan")
        
        for i, challenge in enumerate(challenges, 1):
            status = "[green]✓ Completed[/]" if challenge['id'] in self.completed_challenges else "[yellow]Not Started[/]"
            table.add_row(
                str(i),
                challenge['title'],
                challenge.get('difficulty', 'medium').title(),
                str(challenge.get('points', 50)),
                status
            )
            
        console.print()
        console.print(table)
        return challenges
        
    def run(self) -> List[str]:
        """Run the challenges interface."""
        console.print("\n[bold]Cybersecurity Challenges[/bold]")
        console.print("Test your skills with real-world scenarios!\n")
        
        while True:
            challenges = self._display_challenge_list()
            if not challenges:
                return self.completed_challenges
                
            console.print("\n[bold]Options:[/]")
            console.print("- Enter a challenge number to start")
            console.print("- 'exit' to return to main menu")
            
            choice = Prompt.ask("\nSelect an option").strip().lower()
            
            if choice == 'exit':
                return self.completed_challenges
                
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(challenges):
                    self.run_challenge(challenges[idx]['id'])
                    # Update user progress after completing a challenge
                    if hasattr(self, 'on_progress_update'):
                        self.on_progress_update('challenges_completed', self.completed_challenges)
                else:
                    console.print("[red]Invalid challenge number.[/]")
            except ValueError:
                console.print("[red]Please enter a number or 'exit'.[/]")

    def run_challenge_1(self):
        """Challenge 1: Suspicious Log Analysis"""
        if 1 in self.completed_challenges:
            console.print("\n[green]✓ Challenge 1 already completed![/]")
            return True
            
        console.print(Panel.fit("🔍 [bold]Challenge 1: Suspicious Log Analysis[/bold]"))
        console.print("""
        You are a security analyst investigating a potential breach.
        A suspicious log file has been found in /var/log/auth.log
        
        Your task is to analyze the log and find evidence of unauthorized access.
        """)
        
        # Simulated log file
        log_entries = [
            "Aug 15 08:30:01 server sshd[1234]: Accepted password for admin from 192.168.1.100",
            "Aug 15 08:30:05 server sudo:     admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/bash",
            "Aug 15 08:31:22 server sshd[1235]: Failed password for root from 192.168.1.101",
            "Aug 15 08:31:24 server sshd[1236]: Failed password for root from 192.168.1.101",
            "Aug 15 08:31:26 server sshd[1237]: Accepted password for root from 192.168.1.101",
            "Aug 15 08:32:15 server sudo:     root : TTY=pts/1 ; PWD=/root ; USER=root ; COMMAND=/usr/bin/apt update",
            "Aug 15 08:32:30 server sudo:     root : TTY=pts/1 ; PWD=/root ; USER=root ; COMMAND=/usr/bin/apt install nmap"
        ]
        
        console.print("\n[bold]Log Entries:[/bold]")
        for entry in log_entries:
            console.print(f"• {entry}")
            time.sleep(0.5)
        
        console.print("\n[bold]Questions:[/bold]")
        questions = [
            ("1. How many failed login attempts were there for the root account?", "2"),
            ("2. From which IP address did the successful root login occur?", "192.168.1.101"),
            ("3. What tool was installed after the root login?", "nmap")
        ]
        
        score = 0
        for question, answer in questions:
            user_ans = Prompt.ask(question)
            if user_ans.strip().lower() == answer.lower():
                console.print("[green]✓ Correct![/]")
                score += 1
            else:
                console.print(f"[red]✗ Incorrect! The answer was: {answer}[/]")
        
        if score >= 2:
            self.completed_challenges.append(1)
            console.print("\n[bold green]🎉 Challenge 1 Completed![/]")
            return True
        else:
            console.print("\n[red]❌ Try again! Review the log entries carefully.[/]")
            return False

    def run_challenge_2(self):
        """Challenge 2: Network Intrusion Detection"""
        if 2 in self.completed_challenges:
            console.print("\n[green]✓ Challenge 2 already completed![/]")
            return True
            
        console.print(Panel.fit("🌐 [bold]Challenge 2: Network Intrusion Detection[/bold]"))
        console.print("""
        Your network monitoring system has detected suspicious traffic.
        Analyze the following network capture and answer the questions.
        """)
        
        # Simulated network capture
        captures = [
            "10.0.0.5 -> 192.168.1.100 TCP 80 [SYN] Seq=0",
            "192.168.1.100 -> 10.0.0.5 TCP 80 [SYN, ACK] Seq=0 Ack=1",
            "10.0.0.5 -> 192.168.1.100 TCP 80 [ACK] Seq=1 Ack=1",
            "10.0.0.5 -> 192.168.1.100 HTTP GET /wp-login.php",
            "10.0.0.5 -> 192.168.1.100 HTTP POST /wp-login.php (login attempt: admin/password)",
            "10.0.0.5 -> 192.168.1.100 HTTP POST /wp-login.php (login attempt: admin/admin123)",
            "10.0.0.5 -> 192.168.1.100 HTTP POST /wp-login.php (login attempt: admin/welcome123)",
            "10.0.0.5 -> 192.168.1.100 HTTP GET /wp-admin/install.php"
        ]
        
        console.print("\n[bold]Network Capture:[/bold]")
        for capture in captures:
            console.print(f"• {capture}")
            time.sleep(0.3)
        
        console.print("\n[bold]Questions:[/bold]")
        questions = [
            ("1. What type of attack is being attempted?", "brute force")
        ]
        
        score = 0
        for question, answer in questions:
            user_ans = Prompt.ask(question)
            if answer.lower() in user_ans.lower():
                console.print("[green]✓ Correct![/]")
                score += 1
            else:
                console.print(f"[red]✗ Incorrect! The answer was: {answer}[/]")
        
        if score >= 1:
            self.completed_challenges.append(2)
            console.print("\n[bold green]🎉 Challenge 2 Completed![/]")
            return True
        else:
            console.print("\n[red]❌ Try again! Look for patterns in the traffic.[/]")
            return False

    def run_challenge_3(self):
        """Challenge 3: File Permissions Audit"""
        if 3 in self.completed_challenges:
            console.print("\n[green]✓ Challenge 3 already completed![/]")
            return True
            
        console.print(Panel.fit("🔐 [bold]Challenge 3: File Permissions Audit[/bold]"))
        console.print("""
        You've been asked to audit file permissions on a Linux server.
        Find and fix the following security issues:
        
        1. World-writable files in /etc
        2. SUID/SGID files that shouldn't have those bits set
        3. Sensitive files with incorrect permissions
        """)
        
        console.print("\n[bold]Simulated Environment:[/bold]")
        console.print("""
        /etc/passwd -rw-r--r-- root:root
        /etc/shadow -rw-r----- root:shadow
        /tmp/script.sh -rwxrwxrwx root:root (SUID)
        /home/user/backup -rwxrwxrwx user:user
        """)
        
        questions = [
            ("1. What command would you use to find world-writable files in /etc?", "find /etc -type f -perm -o+w"),
            ("2. What's the recommended permission for /etc/shadow? (octal)", "640"),
            ("3. How would you remove the SUID bit from /tmp/script.sh?", "chmod u-s /tmp/script.sh")
        ]
        
        score = 0
        for question, answer in questions:
            user_ans = Prompt.ask(question)
            if answer.lower() in user_ans.lower():
                console.print("[green]✓ Correct![/]")
                score += 1
            else:
                console.print(f"[red]✗ Incorrect! The answer was: {answer}[/]")
        
        if score >= 2:
            self.completed_challenges.append(3)
            console.print("\n[bold green]🎉 Challenge 3 Completed![/]")
            return True
        else:
            console.print("\n[red]❌ Try again! Review file permissions and related commands.[/]")
            return False

    def run(self):
        """Run the challenge module"""
        if not self.check_prerequisites():
            console.print("\n[red]Please complete the required modules before attempting challenges.[/]")
            return 0
            
        console.print(Panel.fit("🏆 [bold]Challenge Mode[/bold]", 
                             subtitle="Test your skills with real-world scenarios"))
        
        challenges = [
            ("1", "Suspicious Log Analysis", self.run_challenge_1),
            ("2", "Network Intrusion Detection", self.run_challenge_2),
            ("3", "File Permissions Audit", self.run_challenge_3)
        ]
        
        while True:
            console.print("\n[bold]Available Challenges:[/bold]")
            for num, name, _ in challenges:
                status = "[green]✓[/]" if int(num) in self.completed_challenges else "[red]◌[/]"
                console.print(f"{num}. {name} {status}")
            
            console.print("\n0. Return to main menu")
            
            choice = Prompt.ask("\nSelect a challenge (0-3)", choices=[str(i) for i in range(4)])
            
            if choice == "0":
                break
                
            for num, name, func in challenges:
                if choice == num:
                    console.clear()
                    console.print(Panel.fit(f"🏁 [bold]Starting: {name}[/bold]"))
                    func()
                    input("\nPress Enter to continue...")
                    break
        
        return len(self.completed_challenges)
