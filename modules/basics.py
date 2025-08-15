"""
Linux Basics Module - Essential Linux commands for cybersecurity
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

class BasicsModule:
    def __init__(self):
        self.commands_completed = 0
        self.total_commands = 10

    def simulate_ls(self, args=""):
        """Simulate ls command output"""
        if "-l" in args:
            return """
            total 24
            drwxr-xr-x 2 user user 4096 Jan 10 10:00 Desktop
            drwxr-xr-x 2 user user 4096 Jan 10 10:00 Documents
            drwxr-xr-x 2 user user 4096 Jan 10 10:00 Downloads
            -rw-r--r-- 1 user user   42 Jan 10 10:00 notes.txt
            -rwxr-xr-x 1 user user 1234 Jan 10 10:00 script.sh
            """
        else:
            return "Desktop  Documents  Downloads  notes.txt  script.sh"

    def simulate_find(self, args=""):
        """Simulate find command output"""
        if "-name" in args and "*.txt" in args:
            return "./notes.txt\n./Documents/secret.txt\n./Downloads/receipt.txt"
        elif "-type f -perm /u=x" in args:
            return "./script.sh\n./bin/custom_tool"
        return ".\n./Desktop\n./Documents\n./Downloads\n./notes.txt\n./script.sh"

    def simulate_grep(self, args=""):
        """Simulate grep command output"""
        if "password" in args and "-r" in args:
            return """
            ./config.ini:password=supersecret
            ./backup/old_config.ini:password=oldpassword
            """
        elif "TODO" in args:
            return "script.sh:# TODO: Remove debug output before production"
        return "No matches found"

    def explain_command(self, cmd, description, security_context):
        """Display command explanation"""
        console.print(f"\n[bold]Command:[/bold] {cmd}")
        console.print(f"[bold]Purpose:[/bold] {description}")
        console.print("\n[bold]Security Context:[/bold]")
        console.print(security_context)

    def run_command_lesson(self, cmd, explanation, security_context, example_args=""):
        """Run an interactive command lesson"""
        self.explain_command(cmd, explanation, security_context)
        
        if example_args:
            console.print(f"\n[bold]Example:[/bold] {cmd} {example_args}")
        
        while True:
            user_input = Prompt.ask(
                f"\n[bold]Try '{cmd} [options]' (or 'next' to continue)",
                default=""
            )
            
            if user_input.lower() == 'next':
                break
                
            if not user_input.startswith(cmd.split()[0]):
                console.print("[yellow]Try using the command we're learning![/]")
                continue
                
            # Simulate command output
            if cmd.startswith("ls"):
                console.print(self.simulate_ls(user_input))
            elif cmd.startswith("find"):
                console.print(self.simulate_find(user_input))
            elif cmd.startswith("grep"):
                console.print(self.simulate_grep(user_input))
            else:
                console.print("Command output simulation not implemented yet.")
            
            self.commands_completed += 1
            console.print(f"\n[green]✓ Command executed! ({self.commands_completed}/{self.total_commands} completed)[/]")
            break

    def run(self):
        """Run the basics module"""
        console.print(Panel.fit("🔍 [bold]Module 1: Linux Basics[/bold]", 
                             subtitle="Master essential commands for system navigation"))
        
        lessons = [
            {
                "cmd": "ls",
                "explanation": "List directory contents",
                "security": "Understanding directory structure is crucial for finding sensitive files.\n"
                           "- Look for unusual files or directories\n"
                           "- Check file permissions (use 'ls -l' for details)",
                "example": "-l"
            },
            {
                "cmd": "find",
                "explanation": "Search for files in a directory hierarchy",
                "security": "Powerful for finding sensitive files. Common in security audits.\n"
                           "- Find files with sensitive permissions\n"
                           "- Locate configuration files with passwords",
                "example": "/ -type f -name '*.conf' -exec grep -l 'password' {} \\;"
            },
            {
                "cmd": "grep",
                "explanation": "Search text using patterns",
                "security": "Essential for log analysis and finding sensitive data.\n"
                           "- Search for passwords in config files\n"
                           "- Analyze logs for suspicious activity",
                "example": "-r 'password' /etc/"
            }
        ]
        
        for lesson in lessons:
            self.run_command_lesson(
                lesson["cmd"],
                lesson["explanation"],
                lesson["security"],
                lesson.get("example", "")
            )
        
        console.print("\n[bold green]🎉 Module 1 Complete![/]")
        console.print("You've learned essential Linux commands that are the foundation of cybersecurity work.")
        
        return self.commands_completed
