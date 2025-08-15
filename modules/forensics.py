"""
Digital Forensics Module - File investigation and analysis
"""
import os
import hashlib
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

class ForensicsModule:
    def __init__(self):
        self.commands_completed = 0
        self.total_commands = 6

    def simulate_file_command(self, filename=""):
        """Simulate file command output"""
        if not filename:
            return "Usage: file [filename]"
            
        if "suspicious" in filename:
            return f"{filename}: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked"
        elif filename.endswith(".pdf"):
            return f"{filename}: PDF document, version 1.7"
        elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
            return f"{filename}: JPEG image data, EXIF standard"
        else:
            return f"{filename}: ASCII text"

    def simulate_strings(self, filename=""):
        """Simulate strings command output"""
        if not filename:
            return "Usage: strings [filename]"
            
        if "suspicious" in filename:
            return """
            /lib64/ld-linux-x86-64.so.2
            libc.so.6
            __libc_start_main
            GLIBC_2.2.5
            /tmp/.X11-unix
            /bin/sh
            /tmp/.X0-lock
            /dev/tty
            /dev/urandom
            /dev/null
            /bin/csh -i
            /bin/sh
            /bin/bash
            """
        else:
            return "No printable strings found in the file."

    def simulate_hexdump(self, filename=""):
        """Simulate hexdump command output"""
        if not filename:
            return "Usage: hexdump [filename]"
            
        if "suspicious" in filename:
            return """
            0000000 457f 464c 0102 0001 0000 0000 0000 0000
            0000010 0003 003e 0001 0000 0100 0000 0000 0000
            0000020 0040 0000 0000 0000 0000 0000 0000 0000
            0000030 0000 0000 0040 0038 0009 0040 001d 001c
            0000040 0006 0000 0005 0000 0040 0000 0000 0000
            """
        else:
            return "0000000 4865 6c6c 6f20 576f 726c 6421 0a"

    def simulate_hash(self, filename="", algo="md5"):
        """Simulate hash calculation"""
        if not filename:
            return f"Usage: {algo}sum [filename]"
            
        hashes = {
            "md5": "d41d8cd98f00b204e9800998ecf8427e",
            "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
        
        return f"{hashes.get(algo, hashes['md5'])}  {filename}"

    def simulate_stat(self, filename=""):
        """Simulate stat command output"""
        if not filename:
            return "Usage: stat [filename]"
            
        now = int(time.time())
        return f"""
          File: {filename}
          Size: 1024       	Blocks: 8          IO Block: 4096   regular file
        Device: 801h/2049d	Inode: 12345678    Links: 1
        Access: (0644/-rw-r--r--)  Uid: ( 1000/   user)   Gid: ( 1000/   user)
        Access: {datetime.fromtimestamp(now-3600).strftime('%Y-%m-%d %H:%M:%S')} +0000
        Modify: {datetime.fromtimestamp(now-7200).strftime('%Y-%m-%d %H:%M:%S')} +0000
        Change: {datetime.fromtimestamp(now-10800).strftime('%Y-%m-%d %H:%M:%S')} +0000
         Birth: {datetime.fromtimestamp(now-86400).strftime('%Y-%m-%d %H:%M:%S')} +0000
        """

    def run_forensics_lesson(self, cmd, explanation, security_context, example):
        """Run forensics lesson"""
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
            if cmd.startswith("file"):
                filename = user_input.split()[1] if len(user_input.split()) > 1 else ""
                console.print(self.simulate_file_command(filename))
            elif cmd.startswith("strings"):
                filename = user_input.split()[1] if len(user_input.split()) > 1 else ""
                console.print(self.simulate_strings(filename))
            elif cmd.startswith("hexdump"):
                filename = user_input.split()[1] if len(user_input.split()) > 1 else ""
                console.print(self.simulate_hexdump(filename))
            elif cmd.startswith(('md5sum', 'sha1sum', 'sha256sum')):
                filename = user_input.split()[1] if len(user_input.split()) > 1 else ""
                algo = cmd.replace('sum', '')
                console.print(self.simulate_hash(filename, algo))
            elif cmd.startswith("stat"):
                filename = user_input.split()[1] if len(user_input.split()) > 1 else ""
                console.print(self.simulate_stat(filename))
            else:
                console.print("Command output simulation not implemented yet.")
            
            self.commands_completed += 1
            console.print(f"\n[green]✓ Command executed! ({self.commands_completed}/{self.total_commands} completed)[/]")
            break

    def show_forensics_workflow(self):
        """Show typical forensics workflow"""
        workflow = [
            "1. Document the system state (running processes, network connections)",
            "2. Create a forensic image of the disk (using dd or similar tools)",
            "3. Calculate hash values of important files for integrity checking",
            "4. Analyze file metadata (timestamps, permissions, etc.)",
            "5. Search for suspicious files or patterns",
            "6. Recover deleted files if necessary",
            "7. Document all findings with timestamps"
        ]
        
        console.print("\n[bold]Typical Digital Forensics Workflow:[/bold]")
        for step in workflow:
            console.print(f"• {step}")

    def run(self):
        """Run the forensics module"""
        console.print(Panel.fit("🔍 [bold]Module 3: Digital Forensics[/bold]", 
                             subtitle="Master file investigation and analysis"))
        
        lessons = [
            {
                "cmd": "file",
                "explanation": "Determine file type",
                "security": "Helps identify file types even when extensions are changed.\n"
                           "- Detect disguised executable files\n"
                           "- Identify potentially malicious files",
                "example": "suspicious_file"
            },
            {
                "cmd": "strings",
                "explanation": "Display printable strings in a file",
                "security": "Useful for finding hidden text or URLs.\n"
                           "- Reveal hardcoded credentials\n"
                           "- Find suspicious URLs or IPs",
                "example": "suspicious_binary"
            },
            {
                "cmd": "hexdump",
                "explanation": "Display file contents in hexadecimal",
                "security": "Low-level file analysis.\n"
                           "- Analyze file headers\n"
                           "- Identify file signatures",
                "example": "-C suspicious_file"
            },
            {
                "cmd": "md5sum",
                "explanation": "Calculate MD5 hash of a file",
                "security": "Used for file integrity checking.\n"
                           "- Verify file authenticity\n"
                           "- Detect file modifications",
                "example": "important_document.pdf"
            },
            {
                "cmd": "stat",
                "explanation": "Display file status",
                "security": "Reveals file metadata including timestamps.\n"
                           "- Check for timestamp anomalies\n"
                           "- Verify file permissions",
                "example": "suspicious_file"
            }
        ]
        
        for lesson in lessons:
            self.run_forensics_lesson(
                lesson["cmd"],
                lesson["explanation"],
                lesson["security"],
                lesson.get("example", "")
            )
        
        self.show_forensics_workflow()
        
        console.print("\n[bold green]🎉 Module 3 Complete![/]")
        console.print("You've learned essential digital forensics commands for cybersecurity.")
        
        return self.commands_completed
