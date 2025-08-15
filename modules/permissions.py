"""
Permissions Module - File permissions and security
"""
import os
import stat
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

class PermissionsModule:
    def __init__(self):
        self.commands_completed = 0
        self.total_commands = 7

    def simulate_ls_permissions(self, args=""):
        """Simulate ls -l output with focus on permissions"""
        if "-l" in args:
            return """
            total 24
            -rw-r--r-- 1 user user  1234 Jun 15 10:30 public.txt
            -rwxr-xr-x 1 user user  5678 Jun 15 10:31 script.sh
            -rwx------ 1 root root  9101 Jun 15 10:32 secret.txt
            drwxr-xr-x 2 user user  4096 Jun 15 10:33 documents/
            -rwsr-xr-x 1 root root 12345 Jun 15 10:34 suid_program
            """
        else:
            return "public.txt  script.sh  secret.txt  documents/  suid_program"

    def simulate_chmod_result(self, perms, filename):
        """Simulate result of chmod command"""
        if not perms or not filename:
            return "Usage: chmod [permissions] [file]"
            
        try:
            # Parse octal permissions
            if perms.startswith('0'):
                perms = perms[1:]
            mode = int(perms, 8)
            
            # Convert to symbolic representation
            perms_str = ""
            for who in ["USR", "GRP", "OTH"]:
                for what in ["R", "W", "X"]:
                    perms_str += what if mode & 0o400 else "-"
                    mode <<= 1
            
            # Reconstruct the mode for display
            mode_str = f"0o{int(perms, 8):03o}"
            
            return f"Changed permissions of '{filename}' to {mode_str} ({perms_str})"
            
        except ValueError:
            return f"chmod: invalid mode: '{perms}'"

    def simulate_find_permissions(self, args=""):
        """Simulate find command for permission-based searches"""
        if "-perm" in args:
            if "400" in args:
                return "/home/user/secret_key"
            elif "777" in args:
                return "/tmp/insecure_dir\n/var/tmp/unsafe_file"
        elif "-type f -perm -4000" in args:  # SUID files
            return "/usr/bin/passwd\n/usr/bin/sudo"
        elif "-type d -perm -1000" in args:  # Sticky bit directories
            return "/tmp\n/var/tmp"
        return ""

    def explain_permissions(self):
        """Explain Linux permission system"""
        console.print("\n[bold]Linux Permission System:[/bold]")
        
        # Permission types
        table = Table(title="Permission Types")
        table.add_column("Symbol", style="cyan")
        table.add_column("Meaning")
        table.add_row("r", "Read permission")
        table.add_row("w", "Write permission")
        table.add_row("x", "Execute permission")
        table.add_row("s", "Set User/Group ID")
        table.add_row("t", "Sticky bit")
        console.print(table)
        
        # Numeric permissions
        console.print("\n[bold]Numeric Permissions (Octal):[/bold]")
        num_table = Table(title="Permission Values")
        num_table.add_column("Permission", style="cyan")
        num_table.add_column("Value")
        num_table.add_row("Read (r)", "4")
        num_table.add_row("Write (w)", "2")
        num_table.add_row("Execute (x)", "1")
        console.print(num_table)
        
        # Common permission examples
        console.print("\n[bold]Common Permission Examples:[/bold]")
        examples = [
            ("-rw------- (600)", "Only the owner can read/write"),
            ("-rw-r--r-- (644)", "Owner can read/write, others can only read"),
            ("-rwxr-xr-x (755)", "Owner has full access, others can read/execute"),
            ("-rwsr-xr-x (4755)", "SUID - Runs with owner's privileges"),
            ("drwxrwxrwt (1777)", "Sticky bit on directory - Only owner can delete files")
        ]
        
        for perm, desc in examples:
            console.print(f"• {perm}: {desc}")

    def run_permissions_lesson(self, cmd, explanation, security_context, example):
        """Run permissions lesson"""
        console.print(f"\n[bold]Command:[/bold] {cmd}")
        console.print(f"[bold]Purpose:[/bold] {explanation}")
        console.print("\n[bold]Security Context:[/bold]")
        console.print(security_context)
        
        if example:
            console.print(f"\n[bold]Example:[/bold] {example}")
        
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
            if cmd == "ls -l":
                console.print(self.simulate_ls_permissions(user_input))
            elif cmd.startswith("chmod"):
                parts = user_input.split()
                if len(parts) >= 3:
                    perms = parts[1]
                    filename = parts[2]
                    console.print(self.simulate_chmod_result(perms, filename))
                else:
                    console.print("Usage: chmod [permissions] [file]")
            elif cmd.startswith("find"):
                console.print(self.simulate_find_permissions(user_input))
            else:
                console.print("Command output simulation not implemented yet.")
            
            self.commands_completed += 1
            console.print(f"\n[green]✓ Command executed! ({self.commands_completed}/{self.total_commands} completed)[/]")
            break

    def show_security_checklist(self):
        """Show permission security checklist"""
        checklist = [
            "🔒 Check for world-writable files and directories",
            "🔒 Look for files with SUID/SGID bits set",
            "🔒 Verify sensitive files have strict permissions (600 or 400)",
            "🔒 Ensure directories don't have dangerous permissions (e.g., 777)",
            "🔒 Check for files owned by root but writable by others",
            "🔒 Look for hidden files and directories (names starting with '.')",
            "🔒 Verify configuration files have appropriate permissions"
        ]
        
        console.print("\n[bold]Permission Security Checklist:[/bold]")
        for item in checklist:
            console.print(f"• {item}")

    def run(self):
        """Run the permissions module"""
        console.print(Panel.fit("🔐 [bold]Module 4: File Permissions[/bold]", 
                             subtitle="Master Linux file permissions and security"))
        
        # Explain permissions first
        self.explain_permissions()
        
        lessons = [
            {
                "cmd": "ls -l",
                "explanation": "List files with detailed information including permissions",
                "security": "First step in permission auditing.\n"
                           "- Look for unusual permissions\n"
                           "- Identify files owned by root or other users",
                "example": "-l /etc/passwd"
            },
            {
                "cmd": "chmod",
                "explanation": "Change file mode bits (permissions)",
                "security": "Critical for security hardening.\n"
                           "- Restrict sensitive files\n"
                           "- Set appropriate permissions on scripts",
                "example": "755 script.sh"
            },
            {
                "cmd": "find",
                "explanation": "Search for files with specific permissions",
                "security": "Essential for security audits.\n"
                           "- Find world-writable files\n"
                           "- Locate SUID/SGID files",
                "example": "/ -type f -perm -4000 2>/dev/null"
            }
        ]
        
        for lesson in lessons:
            self.run_permissions_lesson(
                lesson["cmd"],
                lesson["explanation"],
                lesson["security"],
                lesson.get("example", "")
            )
        
        self.show_security_checklist()
        
        console.print("\n[bold green]🎉 Module 4 Complete![/]")
        console.print("You've learned essential file permission commands for cybersecurity.")
        
        return self.commands_completed
