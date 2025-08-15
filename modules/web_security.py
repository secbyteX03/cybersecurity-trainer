"""
Web Security Module - Teaches web application security concepts.
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

class WebSecurityModule:
    def __init__(self):
        self.name = "web_security"
        self.commands = {
            "sqlmap": "Test for SQL injection vulnerabilities",
            "nikto": "Web server scanner",
            "dirb": "Web content scanner",
            "whatweb": "Website technology identifier",
            "wpscan": "WordPress vulnerability scanner",
            "nmap -sV --script=http-*": "Nmap HTTP vulnerability scanning",
            "burpsuite": "Web application security testing tool",
            "zap": "OWASP ZAP proxy for security testing",
            "testssl": "Test SSL/TLS vulnerabilities",
            "wafw00f": "Web Application Firewall detector"
        }
        self.completed_commands = set()

    def run(self):
        """Run the web security module."""
        console.print(Panel.fit(
            "🔒 [bold blue]Web Security Module[/bold blue] 🔒\n"
            "Learn about web application security testing tools and techniques.",
            style="blue"
        ))
        
        console.print("\n[bold]Available web security tools:[/]")
        for i, (cmd, desc) in enumerate(self.commands.items(), 1):
            status = "[green]✓[/] " if cmd in self.completed_commands else "  "
            console.print(f"{i:>2}. {status}{cmd:<30} - {desc}")
        
        console.print("\nEnter a command to learn more about it, or 'back' to return.")
        
        while True:
            choice = Prompt.ask("\n> ").strip().lower()
            
            if choice == 'back':
                return len(self.completed_commands)
                
            if choice.isdigit() and 1 <= int(choice) <= len(self.commands):
                cmd = list(self.commands.keys())[int(choice) - 1]
                self._show_command_help(cmd)
                self.completed_commands.add(cmd)
            elif choice in self.commands:
                self._show_command_help(choice)
                self.completed_commands.add(choice)
            else:
                console.print("[yellow]Invalid choice. Try again or type 'back'.[/]")
    
    def _show_command_help(self, command: str) -> None:
        """Show detailed help for a web security command."""
        help_texts = {
            "sqlmap": (
                "[bold]sqlmap[/] - Automatic SQL injection and database takeover tool\n\n"
                "Example usage:\n"
                "  sqlmap -u "http://example.com/page.php?id=1" --dbs\n"
                "  sqlmap -u "http://example.com/login.php" --forms --crawl=2"
            ),
            "nikto": (
                "[bold]nikto[/] - Web server scanner\n\n"
                "Example usage:\n"
                "  nikto -h http://example.com\n"
                "  nikto -h http://example.com -p 80,443 -Tuning x 6"
            ),
            "dirb": (
                "[bold]dirb[/] - Web Content Scanner\n\n"
                "Example usage:\n"
                "  dirb http://example.com/ wordlists/common.txt\n"
                "  dirb https://example.com/ -r -z 100"
            ),
            "whatweb": (
                "[bold]whatweb[/] - Website technology identifier\n\n"
                "Example usage:\n"
                "  whatweb example.com\n"
                "  whatweb -a 3 -v https://example.com"
            ),
            "wpscan": (
                "[bold]wpscan[/] - WordPress vulnerability scanner\n\n"
                "Example usage:\n"
                "  wpscan --url example.com --enumerate vp,vt,tt,cb,dbe,u1-100\n"
                "  wpscan --url example.com --passwords passwords.txt --usernames users.txt"
            )
        }
        
        console.print(Panel.fit(
            help_texts.get(command, "No detailed help available for this command."),
            title=f"Command: {command}",
            style="blue"
        ))
        
        if command in ["sqlmap", "wpscan"]:
            console.print("\n[red]WARNING:[/] This is a powerful tool. Only use on systems you own or have permission to test.")
        
        console.print("\n[dim]Press Enter to continue...[/]")
        input()
        
        # Mark as completed
        self.completed_commands.add(command)
