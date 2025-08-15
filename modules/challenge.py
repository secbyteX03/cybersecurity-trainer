"""
Challenge Module - Hands-on cybersecurity scenarios
"""
import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

class ChallengeModule:
    def __init__(self, user_progress):
        self.user_progress = user_progress
        self.completed_challenges = []

    def check_prerequisites(self):
        """Check if user has completed enough basic modules"""
        required = {
            'basics': 5,  # At least 5/10 commands completed
            'networking': 3,
            'forensics': 2,
            'permissions': 2
        }
        
        for module, min_score in required.items():
            if self.user_progress.get(module, 0) < min_score:
                console.print(f"[red]You need to complete more of the {module} module first![/]")
                console.print(f"Required: {min_score} commands, Completed: {self.user_progress.get(module, 0)}")
                return False
        return True

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
