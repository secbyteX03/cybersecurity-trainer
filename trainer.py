
"""
Cybersecurity Command Trainer - Main Entry Point
A safe, educational CLI tool for learning cybersecurity commands
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import print as rprint
from modules import basics, networking, forensics, permissions, challenge

console = Console()

class CyberSecTrainer:
    def __init__(self):
        self.console = console
        self.user_progress = {
            'basics': 0,
            'networking': 0, 
            'forensics': 0,
            'permissions': 0,
            'challenges_completed': []
        }

    def show_banner(self):
        banner = """
+--------------------------------------------------+
|           CYBERSECURITY COMMAND TRAINER          |
|                                                  |
|           Learn cybersecurity commands safely!   |
|              No real system changes made.        |
+--------------------------------------------------+
        """
        console.print(banner, style="bold blue")

    def show_main_menu(self):
        console.print("\n=== CYBERSECURITY COMMAND TRAINER ===\n", style="bold blue")
        console.print("MAIN MENU\n", style="bold underline")
        
        menu_items = [
            ("1", "Linux Basics", f"Progress: {self.user_progress['basics']}/10"),
            ("2", "Networking", f"Progress: {self.user_progress['networking']}/8"),
            ("3", "Digital Forensics", f"Progress: {self.user_progress['forensics']}/6"),
            ("4", "Permissions", f"Progress: {self.user_progress['permissions']}/7"),
            ("5", "Challenges", f"Completed: {len(self.user_progress['challenges_completed'])}/5"),
            ("6", "Help", "Command reference and tips"),
            ("0", "Exit", "Quit the trainer")
        ]
        
        for num, title, desc in menu_items:
            console.print(f"[{num}] {title}", style="bold")
            console.print(f"   {desc}\n", style="dim")

    def show_help(self):
        console.print("\n=== HOW TO USE THIS TRAINER ===\n", style="bold green")
        console.print("This is a SAFE learning environment - no real system changes are made!")
        console.print("All outputs are simulated for educational purposes")
        console.print("Commands are explained with context and security implications")
        console.print("Progress through modules to unlock challenges")
        console.print("Type 'back' at any prompt to return to main menu\n")
        
        console.print("TIPS:", style="bold")
        console.print("- Read command explanations carefully")
        console.print("- Try to understand WHY each command is useful in cybersecurity")
        console.print("- Practice the commands in a real Linux VM after learning here")
        console.print("- Complete basic modules before attempting challenges\n")

    def run(self):
        self.show_banner()
        
        while True:
            console.print("\n" + "="*60)
            self.show_main_menu()
            
            choice = Prompt.ask("\nSelect a training module (1-6, 0 to exit)", choices=["1", "2", "3", "4", "5", "6", "0"])
            
            if choice == "0":
                console.print("\nGoodbye! Happy learning and stay secure!", style="bold green")
                break
            elif choice == "1":
                basics_trainer = basics.BasicsModule()
                self.user_progress['basics'] = basics_trainer.run()
            elif choice == "2":
                net_trainer = networking.NetworkingModule()
                self.user_progress['networking'] = net_trainer.run()
            elif choice == "3":
                forensics_trainer = forensics.ForensicsModule()
                self.user_progress['forensics'] = forensics_trainer.run()
            elif choice == "4":
                perms_trainer = permissions.PermissionsModule()
                self.user_progress['permissions'] = perms_trainer.run()
            elif choice == "5":
                challenge_trainer = challenge.ChallengeModule(self.user_progress)
                completed = challenge_trainer.run()
                self.user_progress['challenges_completed'].extend(completed)
            elif choice == "6":
                self.show_help()

if __name__ == "__main__":
    try:
        trainer = CyberSecTrainer()
        trainer.run()
    except KeyboardInterrupt:
        console.print("\nExiting trainer. Happy learning!", style="bold yellow")
    except Exception as e:
        console.print(f"\nERROR: {e}", style="bold red")
        console.print("Please check your Python environment and try again.")

# modules/__init__.py
"""
Cybersecurity Trainer Modules
"""

# modules/basics.py
"""
Linux Basics Module - Essential commands for cybersecurity
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
import time
import random

console = Console()

class BasicsModule:
    def __init__(self):
        self.commands_completed = 0
        self.total_commands = 10
        
    def simulate_ls(self, args=""):
        """Simulate ls command output"""
        if "-la" in args or "-al" in args:
            return """total 48
drwxr-xr-x  5 user user 4096 Dec 15 10:30 .
drwxr-xr-x 20 user user 4096 Dec 15 09:15 ..
-rw-------  1 user user  156 Dec 14 16:22 .bash_history
-rw-r--r--  1 user user  220 Dec 10 11:30 .bash_logout
-rw-r--r--  1 user user 3771 Dec 10 11:30 .bashrc
drwxr-xr-x  2 user user 4096 Dec 15 08:45 Documents
-rw-r--r--  1 user user  807 Dec 10 11:30 .profile
-rw-r--r--  1 user user 1024 Dec 15 10:30 suspicious.log
drwxr-xr-x  2 user user 4096 Dec 14 20:15 scripts
drwx------  2 user user 4096 Dec 15 09:00 .ssh"""
        elif "-l" in args:
            return """-rw-r--r--  1 user user  220 Dec 10 11:30 .bash_logout
-rw-r--r--  1 user user 3771 Dec 10 11:30 .bashrc
drwxr-xr-x  2 user user 4096 Dec 15 08:45 Documents
-rw-r--r--  1 user user  807 Dec 10 11:30 .profile
-rw-r--r--  1 user user 1024 Dec 15 10:30 suspicious.log
drwxr-xr-x  2 user user 4096 Dec 14 20:15 scripts"""
        else:
            return "Documents  scripts  suspicious.log"

    def simulate_find(self, args=""):
        """Simulate find command output"""
        if "*.log" in args:
            return """/home/user/suspicious.log
/var/log/auth.log
/var/log/syslog
/var/log/apache2/access.log
/var/log/apache2/error.log"""
        elif "-name" in args and "config" in args:
            return """/etc/ssh/ssh_config
/etc/apache2/apache2.conf
/home/user/.bashrc
/etc/mysql/my.cnf"""
        else:
            return """/home/user/Documents
/home/user/scripts
/home/user/suspicious.log"""

    def simulate_grep(self, args=""):
        """Simulate grep command output"""
        if "error" in args.lower():
            return """[2024-12-15 10:15:32] ERROR: Failed login attempt from 192.168.1.100
[2024-12-15 10:16:45] ERROR: Invalid password for user admin
[2024-12-15 10:18:22] ERROR: Connection refused on port 22"""
        elif "failed" in args.lower():
            return """Dec 15 08:30:15 server sshd[1234]: Failed password for root from 192.168.1.50
Dec 15 08:30:20 server sshd[1235]: Failed password for admin from 192.168.1.50
Dec 15 08:30:25 server sshd[1236]: Failed password for root from 192.168.1.50"""
        else:
            return "pattern found in multiple lines..."

    def explain_command(self, cmd, description, security_context):
        """Display command explanation"""
        panel = Panel.fit(f"""
🔧 Command: {cmd}
📖 Description: {description}
🛡️ Security Context: {security_context}
        """, title="Command Explanation", border_style="blue")
        console.print(panel)

    def run_command_lesson(self, cmd, explanation, security_context, example_args=""):
        """Run an interactive command lesson"""
        console.print(f"\n📝 Learning: [bold cyan]{cmd}[/bold cyan]")
        self.explain_command(cmd, explanation, security_context)
        
        console.print(f"\n💻 Let's try it! Type: [bold green]{cmd} {example_args}[/bold green]")
        
        while True:
            user_input = Prompt.ask("$ ").strip()
            
            if user_input.lower() == "back":
                return False
                
            if user_input.startswith(cmd.split()[0]):
                # Simulate command execution
                console.print("🔄 Executing (simulated)...", style="dim")
                time.sleep(0.5)
                
                if cmd.startswith("ls"):
                    output = self.simulate_ls(user_input)
                elif cmd.startswith("find"):
                    output = self.simulate_find(user_input)
                elif cmd.startswith("grep"):
                    output = self.simulate_grep(user_input)
                else:
                    output = f"Simulated output for: {user_input}"
                
                console.print(output, style="dim white")
                console.print("[SUCCESS] Command executed successfully.", style="bold green")
                
                return True
            else:
                console.print(f"[ERROR] Try typing: {cmd} {example_args}", style="bold red")

    def run(self):
        console.print("\n[LINUX BASICS MODULE]", style="bold blue")
        console.print("Learn essential Linux commands used in cybersecurity")
        
        lessons = [
            ("ls -la", "List files with detailed information including hidden files", 
             "Essential for discovering hidden malware, config files, and understanding file permissions", "-la"),
            ("pwd", "Print working directory - shows current location", 
             "Important for maintaining situational awareness during investigations", ""),
            ("cd /var/log", "Change directory to navigate the filesystem", 
             "Navigate to log directories to investigate security events", "/var/log"),
            ("find / -name '*.log'", "Find files by name pattern across the system", 
             "Locate log files, config files, or suspicious files during incident response", "/ -name '*.log'"),
            ("grep -i 'error' /var/log/syslog", "Search for text patterns in files", 
             "Essential for log analysis and finding indicators of compromise", "-i 'error' suspicious.log"),
            ("cat suspicious.log", "Display file contents", 
             "Quick way to view file contents during forensic analysis", "suspicious.log"),
            ("head -10 /var/log/auth.log", "Show first 10 lines of a file", 
             "Preview large log files without opening the entire file", "-10 suspicious.log"),
            ("tail -f /var/log/syslog", "Show last lines of file and follow changes", 
             "Monitor log files in real-time for security events", "-f suspicious.log"),
            ("wc -l /var/log/auth.log", "Count lines, words, or characters in files", 
             "Get quick statistics about log file size and activity", "-l suspicious.log"),
            ("history", "Show command history", 
             "Review commands executed by users during forensic investigations", "")
        ]
        
        completed = 0
        for i, (cmd, desc, security, args) in enumerate(lessons, 1):
            console.print(f"\n{'='*50}")
            console.print(f"📚 Lesson {i}/{len(lessons)}")
            
            if self.run_command_lesson(cmd, desc, security, args):
                completed += 1
                console.print(f"✅ Lesson {i} completed! ({completed}/{len(lessons)})", style="bold green")
            else:
                console.print("↩️ Returning to main menu", style="yellow")
                break
                
            if i < len(lessons):
                continue_prompt = Prompt.ask("\nContinue to next lesson?", choices=["y", "n", "back"], default="y")
                if continue_prompt in ["n", "back"]:
                    break
        
        if completed == len(lessons):
            console.print("\n*** CONGRATULATIONS! ***", style="bold green")
            console.print("You've completed the Linux Basics module!")
            console.print("You're ready for more advanced modules!")
        
        return completed

# modules/networking.py
"""
Networking Module - Network analysis and security commands
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import time
import random

console = Console()

class NetworkingModule:
    def __init__(self):
        self.commands_completed = 0
        self.total_commands = 8

    def simulate_ping(self, target=""):
        """Simulate ping command output"""
        return f"""PING {target} (192.168.1.1): 56 data bytes
64 bytes from 192.168.1.1: icmp_seq=0 ttl=64 time=1.234 ms
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=1.456 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=1.123 ms
^C
--- {target} ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 1.123/1.271/1.456/0.140 ms"""

    def simulate_netstat(self, args=""):
        """Simulate netstat command output"""
        if "-tuln" in args:
            return """Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN     
udp        0      0 0.0.0.0:53              0.0.0.0:*                          
udp        0      0 0.0.0.0:68              0.0.0.0:*               """
        else:
            return """Active Internet connections
Proto Local Address    Foreign Address   State
tcp   192.168.1.10:80  192.168.1.50:5432  ESTABLISHED
tcp   192.168.1.10:22  192.168.1.100:4455 ESTABLISHED"""

    def simulate_nmap(self, target=""):
        """Simulate nmap scan output"""
        return f"""Starting Nmap scan on {target}...

Nmap scan report for {target}
Host is up (0.0012s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3306/tcp open  mysql

Nmap done: 1 IP address scanned in 2.34 seconds"""

    def simulate_ss(self, args=""):
        """Simulate ss command output"""
        return """State      Local Address:Port               Peer Address:Port              
LISTEN     0.0.0.0:22                    0.0.0.0:*                  
LISTEN     127.0.0.1:3306                0.0.0.0:*                  
LISTEN     0.0.0.0:80                    0.0.0.0:*                  
ESTAB      192.168.1.10:22               192.168.1.100:4455"""

    def run_networking_lesson(self, cmd, explanation, security_context, example):
        """Run interactive networking lesson"""
        console.print(f"\n🌐 Learning: [bold cyan]{cmd}[/bold cyan]")
        
        panel = Panel.fit(f"""
🔧 Command: {cmd}
📖 Description: {explanation}
🛡️ Security Use: {security_context}
💡 Example: {example}
        """, title="Network Command", border_style="cyan")
        console.print(panel)
        
        console.print(f"\n💻 Try it: [bold green]{example}[/bold green]")
        
        while True:
            user_input = Prompt.ask("$ ").strip()
            
            if user_input.lower() == "back":
                return False
                
            # Check if user input starts with the command
            cmd_base = cmd.split()[0]
            if user_input.startswith(cmd_base):
                console.print("🔄 Scanning/Connecting (simulated)...", style="dim")
                time.sleep(1)
                
                # Simulate appropriate output
                if cmd_base == "ping":
                    target = user_input.split()[-1] if len(user_input.split()) > 1 else "example.com"
                    output = self.simulate_ping(target)
                elif cmd_base == "netstat":
                    output = self.simulate_netstat(user_input)
                elif cmd_base == "nmap":
                    target = user_input.split()[-1] if len(user_input.split()) > 1 else "192.168.1.1"
                    output = self.simulate_nmap(target)
                elif cmd_base == "ss":
                    output = self.simulate_ss(user_input)
                elif cmd_base == "traceroute":
                    output = """traceroute to google.com (8.8.8.8), 30 hops max, 60 byte packets
 1  router.local (192.168.1.1)  1.234 ms  1.456 ms  1.123 ms
 2  10.0.0.1 (10.0.0.1)  15.234 ms  12.456 ms  14.123 ms
 3  * * *
 4  8.8.8.8 (8.8.8.8)  45.234 ms  42.456 ms  44.123 ms"""
                else:
                    output = f"Simulated output for: {user_input}"
                
                console.print(output, style="dim white")
                console.print("✅ Command executed successfully!", style="bold green")
                return True
            else:
                console.print(f"❌ Try: {example}", style="bold red")

    def show_network_security_tips(self):
        """Show important networking security tips"""
        tips_table = Table(title="🔒 Network Security Tips", show_header=True)
        tips_table.add_column("Command", style="cyan")
        tips_table.add_column("Security Tip", style="green")
        
        tips = [
            ("ping", "Test connectivity but be aware it can reveal your location"),
            ("netstat", "Monitor for unexpected listening ports (backdoors)"),
            ("nmap", "ONLY scan networks you own - unauthorized scanning is illegal"),
            ("ss", "Modern replacement for netstat with better performance"),
            ("traceroute", "Reveals network path - useful for troubleshooting"),
            ("tcpdump", "Capture network traffic for analysis (requires root)"),
            ("wireshark", "GUI tool for detailed packet analysis"),
            ("iftop", "Monitor network usage by host in real-time")
        ]
        
        for cmd, tip in tips:
            tips_table.add_row(cmd, tip)
            
        console.print(tips_table)

    def run(self):
        console.print("\n🌐 [bold cyan]NETWORKING MODULE[/bold cyan] 🌐")
        console.print("Learn network analysis commands for cybersecurity")
        
        # Show security warning first
        warning = Panel.fit("""
⚠️  IMPORTANT LEGAL WARNING ⚠️

• ONLY scan networks and systems you own or have explicit permission to test
• Unauthorized network scanning can be illegal in many jurisdictions
• These simulations are for educational purposes only
• Always follow responsible disclosure if you find vulnerabilities
• Use these skills ethically and legally
        """, title="🚨 Ethical Usage", border_style="red")
        console.print(warning)
        
        acknowledge = Prompt.ask("\nDo you understand and agree to use these tools ethically?", choices=["yes", "no"])
        if acknowledge.lower() != "yes":
            console.print("Training cancelled. Please only use these tools ethically.", style="red")
            return 0
        
        lessons = [
            ("ping", "Send ICMP packets to test network connectivity", 
             "Test if hosts are online, measure latency, basic network troubleshooting", "ping -c 3 google.com"),
            ("netstat -tuln", "Display network connections and listening ports", 
             "Identify suspicious connections, find backdoors, monitor network activity", "netstat -tuln"),
            ("ss -tuln", "Modern alternative to netstat for socket information", 
             "Faster than netstat, better for real-time monitoring", "ss -tuln"),
            ("nmap -sS 192.168.1.1", "Network mapper - scan for open ports and services", 
             "Discover services, identify vulnerabilities, network reconnaissance", "nmap -sS 127.0.0.1"),
            ("traceroute google.com", "Trace the network path to a destination", 
             "Identify network bottlenecks, routing issues, network topology", "traceroute google.com"),
            ("iftop", "Display bandwidth usage by host in real-time", 
             "Monitor for data exfiltration, identify network abuse", "iftop"),
            ("tcpdump -i eth0", "Capture and analyze network packets", 
             "Deep packet inspection, protocol analysis, incident response", "tcpdump -i any -c 5"),
            ("whois example.com", "Query domain registration information", 
             "OSINT gathering, identify domain owners, investigate suspicious domains", "whois example.com")
        ]
        
        completed = 0
        for i, (cmd, desc, security, example) in enumerate(lessons, 1):
            console.print(f"\n{'='*60}")
            console.print(f"🌐 Network Lesson {i}/{len(lessons)}")
            
            if self.run_networking_lesson(cmd, desc, security, example):
                completed += 1
                console.print(f"✅ Lesson {i} completed! ({completed}/{len(lessons)})", style="bold green")
            else:
                console.print("↩️ Returning to main menu", style="yellow")
                break
                
            if i < len(lessons):
                continue_prompt = Prompt.ask("\nContinue to next lesson?", choices=["y", "n", "back"], default="y")
                if continue_prompt in ["n", "back"]:
                    break
        
        if completed == len(lessons):
            console.print("\n🎉 [bold green]NETWORKING MODULE COMPLETED![/bold green] 🎉")
            self.show_network_security_tips()
        
        return completed

# modules/forensics.py
"""
Digital Forensics Module - File investigation and analysis
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import time

console = Console()

class ForensicsModule:
    def __init__(self):
        self.commands_completed = 0
        
    def simulate_file_command(self, filename=""):
        """Simulate file command output"""
        outputs = {
            "suspicious.exe": "suspicious.exe: PE32 executable (GUI) Intel 80386, for MS Windows",
            "document.pdf": "document.pdf: PDF document, version 1.4",
            "image.jpg": "image.jpg: JPEG image data, JFIF standard 1.01",
            "script.sh": "script.sh: Bourne-Again shell script, ASCII text executable",
            "data.bin": "data.bin: data"
        }
        return outputs.get(filename, f"{filename}: ASCII text")

    def simulate_strings(self, filename=""):
        """Simulate strings command output"""
        return """HTTP/1.1
User-Agent: Mozilla/5.0
www.suspicious-site.com
password123
admin@company.com
C:\\Windows\\System32\\
CreateProcess
LoadLibrary
/tmp/malware.txt"""

    def simulate_hexdump(self, filename=""):
        """Simulate hexdump output"""
        return """0000000 4d5a 9000 0003 0000 0004 0000 ffff 0000
0000010 00b8 0000 0000 0000 0040 0000 0000 0000
0000020 0000 0000 0000 0000 0000 0000 0000 0000
0000030 0000 0000 0000 0000 0000 0000 0080 0000
0000040 0e1f ba0e 00b4 09cd 21b8 014c cd21 5468"""

    def simulate_hash(self, filename="", algo="md5"):
        """Simulate hash calculation"""
        hashes = {
            "md5": "d41d8cd98f00b204e9800998ecf8427e",
            "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
        return f"{hashes.get(algo, hashes['md5'])}  {filename}"

    def simulate_stat(self, filename=""):
        """Simulate stat command output"""
        return f"""  File: {filename}
  Size: 4096      	Blocks: 8          IO Block: 4096   regular file
Device: 801h/2049d	Inode: 123456      Links: 1
Access: (0644/-rw-r--r--)  Uid: (1000/   user)   Gid: (1000/   user)
Access: 2024-12-15 10:30:45.123456789 +0000
Modify: 2024-12-15 10:25:32.987654321 +0000
Change: 2024-12-15 10:25:32.987654321 +0000
 Birth: -"""

    def run_forensics_lesson(self, cmd, explanation, security_context, example):
        """Run forensics lesson"""
        console.print(f"\n🔍 Learning: [bold magenta]{cmd}[/bold magenta]")
        
        panel = Panel.fit(f"""
🔧 Command: {cmd}
📖 Description: {explanation}
🛡️ Forensics Use: {security_context}
💡 Example: {example}
        """, title="Forensics Command", border_style="magenta")
        console.print(panel)
        
        console.print(f"\n💻 Try it: [bold green]{example}[/bold green]")
        
        while True:
            user_input = Prompt.ask("$ ").strip()
            
            if user_input.lower() == "back":
                return False
                
            cmd_base = cmd.split()[0]
            if user_input.startswith(cmd_base):
                console.print("🔄 Analyzing (simulated)...", style="dim")
                time.sleep(1)
                
                if cmd_base == "file":
                    filename = user_input.split()[-1] if len(user_input.split()) > 1 else "suspicious.exe"
                    output = self.simulate_file_command(filename)
                elif cmd_base == "strings":
                    filename = user_input.split()[-1] if len(user_input.split()) > 1 else "binary"
                    output = self.simulate_strings(filename)
                elif cmd_base == "hexdump":
                    output = self.simulate_hexdump()
                elif cmd_base == "md5sum":
                    filename = user_input.split()[-1] if len(user_input.split()) > 1 else "file.txt"
                    output = self.simulate_hash(filename, "md5")
                elif cmd_base == "sha256sum":
                    filename = user_input.split()[-1] if len(user_input.split()) > 1 else "file.txt"
                    output = self.simulate_hash(filename, "sha256")
                elif cmd_base == "stat":
                    filename = user_input.split()[-1] if len(user_input.split()) > 1 else "evidence.txt"
                    output = self.simulate_stat(filename)
                else:
                    output = f"Simulated forensics output for: {user_input}"
                
                console.print(output, style="dim white")
                console.print("✅ Analysis complete!", style="bold green")
                return True
            else:
                console.print(f"❌ Try: {example}", style="bold red")

    def show_forensics_workflow(self):
        """Show typical forensics workflow"""
        workflow_table = Table(title="🔬 Digital Forensics Workflow", show_header=True)
        workflow_table.add_column("Step", style="bold cyan", width=5)
        workflow_table.add_column("Action", style="green")
        workflow_table.add_column("Commands Used", style="yellow")
        
        steps = [
            ("1", "Identify file type", "file, xxd"),
            ("2", "Calculate hashes", "md5sum, sha256sum"),
            ("3", "Extract strings", "strings"),
            ("4", "Examine metadata", "stat, exiftool"),
            ("5", "Hex analysis", "hexdump, xxd"),
            ("6", "Timeline analysis", "ls -la, stat"),
            ("7", "Content analysis", "grep, awk"),
            ("8", "Document findings", "Report creation")
        ]
        
        for step, action, commands in steps:
            workflow_table.add_row(step, action, commands)
            
        console.print(workflow_table)

    def run(self):
        console.print("\n🔍 [bold magenta]DIGITAL FORENSICS MODULE[/bold magenta] 🔍")
        console.print("Learn file investigation and analysis techniques")
        
        # Show forensics principles
        principles = Panel.fit("""
🔬 Key Forensics Principles:

1. PRESERVATION - Never modify original evidence
2. DOCUMENTATION - Record everything you do
3. CHAIN OF CUSTODY - Track who handled evidence when
4. VERIFICATION - Use multiple tools to confirm findings
5. REPEATABILITY - Others should get same results

⚠️ Always work on COPIES of evidence files!
        """, title="🧪 Forensics Fundamentals", border_style="magenta")
        console.print(principles)
        
        lessons = [
            ("file", "Identify file type and format", 
             "Determine actual file type regardless of extension - malware often disguises itself", "file suspicious.exe"),
            ("strings", "Extract readable text from binary files", 
             "Find URLs, passwords, commands, or other indicators in malware or evidence", "strings binary_file"),
            ("hexdump -C", "Display file contents in hexadecimal", 
             "Low-level analysis, find file signatures, examine data structure", "hexdump -C file.bin"),
            ("md5sum", "Calculate MD5 hash for file integrity", 
             "Verify file hasn't changed, compare against known malware databases", "md5sum evidence.txt"),
            ("sha256sum", "Calculate SHA256 hash (more secure than MD5)", 
             "Better cryptographic integrity verification than MD5", "sha256sum evidence.txt"),
            ("stat", "Display detailed file metadata and timestamps", 
             "Timeline analysis - when was file created, modified, accessed", "stat suspicious_file")
        ]
        
        completed = 0
        for i, (cmd, desc, security, example) in enumerate(lessons, 1):
            console.print(f"\n{'='*60}")
            console.print(f"🔍 Forensics Lesson {i}/{len(lessons)}")
            
            if self.run_forensics_lesson(cmd, desc, security, example):
                completed += 1
                console.print(f"✅ Lesson {i} completed! ({completed}/{len(lessons)})", style="bold green")
            else:
                console.print("↩️ Returning to main menu", style="yellow")
                break
                
            if i < len(lessons):
                continue_prompt = Prompt.ask("\nContinue to next lesson?", choices=["y", "n", "back"], default="y")
                if continue_prompt in ["n", "back"]:
                    break
        
        if completed == len(lessons):
            console.print("\n🎉 [bold green]FORENSICS MODULE COMPLETED![/bold green] 🎉")
            self.show_forensics_workflow()
        
        return completed

# modules/permissions.py
"""
Permissions Module - File permissions and security
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import time

console = Console()

class PermissionsModule:
    def __init__(self):
        self.commands_completed = 0
        
    def simulate_ls_permissions(self, args=""):
        """Simulate ls -l output with focus on permissions"""
        return """-rwxr-xr-x 1 root   root    12288 Dec 15 10:30 /usr/bin/sudo
-rw-r--r-- 1 user   user     1024 Dec 15 09:15 document.txt
-rw------- 1 user   user      256 Dec 15 08:30 private.key
drwxrwxrwx 1 user   user     4096 Dec 15 07:45 public_folder
-rwsr-xr-x 1 root   root     8192 Dec 15 06:20 setuid_binary
-rwxrwxrwx 1 nobody nobody   2048 Dec 15 05:10 dangerous_script.sh"""

    def simulate_chmod_result(self, perms, filename):
        """Simulate result of chmod command"""
        return f"Permissions changed for {filename}"

    def simulate_find_permissions(self, args=""):
        """Simulate find command for permission-based searches"""
        if "4000" in args or "u+s" in args:
            return """/usr/bin/sudo
/usr/bin/passwd
/usr/bin/su
/bin/mount
/bin/umount"""
        elif "2000" in args or "g+s" in args:
            return """/usr/bin/ssh-agent
/var/mail
/usr/bin/wall"""
        elif "777" in args:
            return """/tmp/dangerous_file
/var/tmp/world_writable
/home/user/public_folder"""
        else:
            return "/tmp/some_file\n/home/user/document.txt"

    def explain_permissions(self):
        """Explain Linux permission system"""
        perm_table = Table(title="🔐 Linux Permission System", show_header=True)
        perm_table.add_column("Symbol", style="cyan", width=8)
        perm_table.add_column("Octal", style="green", width=8)
        perm_table.add_column("Meaning", style="white")
        perm_table.add_column("Security Risk", style="red")
        
        perms = [
            ("---", "0", "No permissions", "Safe"),
            ("r--", "4", "Read only", "Low risk"),
            ("-w-", "2", "Write only", "Medium risk"),
            ("--x", "1", "Execute only", "Medium risk"),
            ("rwx", "7", "Full permissions", "HIGH RISK"),
            ("rws", "4+7", "SUID bit set", "CRITICAL RISK"),
            ("rwt", "1+7", "Sticky bit set", "Check context")
        ]
        
        for symbol, octal, meaning, risk in perms:
            perm_table.add_row(symbol, octal, meaning, risk)
        
        console.print(perm_table)
        
        # Explain permission format
        format_explanation = Panel.fit("""
📋 Permission String Format: -rwxrwxrwx

Position 1: File type (- = file, d = directory, l = link)
Positions 2-4: Owner permissions (rwx)
Positions 5-7: Group permissions (rwx)
Positions 8-10: Other permissions (rwx)

🚨 Special Bits:
• SUID (s in owner execute): Run as file owner
• SGID (s in group execute): Run as file group
• Sticky (t in other execute): Only owner can delete

Example: -rwsr-xr-x = SUID binary (security critical!)
        """, title="Permission Format Guide", border_style="blue")
        console.print(format_explanation)

    def run_permissions_lesson(self, cmd, explanation, security_context, example):
        """Run permissions lesson"""
        console.print(f"\n🔐 Learning: [bold blue]{cmd}[/bold blue]")
        
        panel = Panel.fit(f"""
🔧 Command: {cmd}
📖 Description: {explanation}
🛡️ Security Impact: {security_context}
💡 Example: {example}
        """, title="Permissions Command", border_style="blue")
        console.print(panel)
        
        console.print(f"\n💻 Try it: [bold green]{example}[/bold green]")
        
        while True:
            user_input = Prompt.ask("$ ").strip()
            
            if user_input.lower() == "back":
                return False
                
            cmd_base = cmd.split()[0]
            if user_input.startswith(cmd_base):
                console.print("🔄 Checking permissions (simulated)...", style="dim")
                time.sleep(0.5)
                
                if cmd_base == "ls" and "-l" in user_input:
                    output = self.simulate_ls_permissions(user_input)
                elif cmd_base == "chmod":
                    parts = user_input.split()
                    if len(parts) >= 3:
                        output = self.simulate_chmod_result(parts[1], parts[2])
                    else:
                        output = "chmod: missing operand"
                elif cmd_base == "find":
                    output = self.simulate_find_permissions(user_input)
                elif cmd_base == "umask":
                    output = "0022"
                elif cmd_base == "whoami":
                    output = "user"
                elif cmd_base == "id":
                    output = "uid=1000(user) gid=1000(user) groups=1000(user),4(adm),24(cdrom),27(sudo)"
                else:
                    output = f"Simulated permissions output for: {user_input}"
                
                console.print(output, style="dim white")
                console.print("✅ Permission check complete!", style="bold green")
                return True
            else:
                console.print(f"❌ Try: {example}", style="bold red")

    def show_security_checklist(self):
        """Show permission security checklist"""
        checklist = Panel.fit("""
🔍 PERMISSION SECURITY CHECKLIST:

✓ Find all SUID/SGID binaries: find / -perm /6000 2>/dev/null
✓ Check world-writable files: find / -perm -2 -type f 2>/dev/null
✓ Verify critical file permissions:
  • /etc/passwd should be 644
  • /etc/shadow should be 640 or 600
  • SSH keys should be 600
  • Home directories should NOT be world-readable
✓ Review user accounts and groups
✓ Check for files with no owner: find / -nouser -o -nogroup 2>/dev/null

🚨 RED FLAGS:
• World-writable system files
• Unusual SUID binaries
• Files owned by deleted users
• Overly permissive directories
        """, title="🛡️ Security Audit Checklist", border_style="red")
        console.print(checklist)

    def run(self):
        console.print("\n🔐 [bold blue]PERMISSIONS MODULE[/bold blue] 🔐")
        console.print("Master Linux file permissions and security")
        
        # First explain the permission system
        self.explain_permissions()
        
        lessons = [
            ("ls -la", "List files with detailed permissions", 
             "Identify files with dangerous permissions, find SUID binaries", "ls -la /usr/bin/"),
            ("chmod 644", "Change file permissions using octal notation", 
             "Fix insecure permissions, prevent unauthorized access", "chmod 644 document.txt"),
            ("chmod u+x", "Change permissions using symbolic notation", 
             "Add/remove specific permissions without affecting others", "chmod u+x script.sh"),
            ("find / -perm -4000", "Find files with SUID bit set", 
             "Discover potential privilege escalation vectors", "find /usr -perm -4000 2>/dev/null"),
            ("find / -perm 777", "Find world-writable files", 
             "Locate files that anyone can modify (major security risk)", "find /tmp -perm 777"),
            ("umask", "Display default permission mask", 
             "Understand default permissions for new files", "umask"),
            ("id", "Display user and group IDs", 
             "Check current user privileges and group memberships", "id")
        ]
        
        completed = 0
        for i, (cmd, desc, security, example) in enumerate(lessons, 1):
            console.print(f"\n{'='*60}")
            console.print(f"🔐 Permissions Lesson {i}/{len(lessons)}")
            
            if self.run_permissions_lesson(cmd, desc, security, example):
                completed += 1
                console.print(f"✅ Lesson {i} completed! ({completed}/{len(lessons)})", style="bold green")
            else:
                console.print("↩️ Returning to main menu", style="yellow")
                break
                
            if i < len(lessons):
                continue_prompt = Prompt.ask("\nContinue to next lesson?", choices=["y", "n", "back"], default="y")
                if continue_prompt in ["n", "back"]:
                    break
        
        if completed == len(lessons):
            console.print("\n🎉 [bold green]PERMISSIONS MODULE COMPLETED![/bold green] 🎉")
            self.show_security_checklist()
        
        return completed

# modules/challenge.py
"""
Challenge Module - Hands-on cybersecurity scenarios
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import time
import random

console = Console()

class ChallengeModule:
    def __init__(self, user_progress):
        self.user_progress = user_progress
        self.completed_challenges = []
        
    def check_prerequisites(self):
        """Check if user has completed enough basic modules"""
        basic_modules = ['basics', 'networking', 'forensics', 'permissions']
        min_completion = 5  # Minimum commands completed per module
        
        ready = all(self.user_progress.get(module, 0) >= min_completion for module in basic_modules)
        
        if not ready:
            console.print("🚫 [bold red]Challenges Locked![/bold red]", style="bold red")
            console.print("Complete at least 5 lessons in each basic module first:")
            
            progress_table = Table(title="📊 Your Progress", show_header=True)
            progress_table.add_column("Module", style="cyan")
            progress_table.add_column("Completed", style="green") 
            progress_table.add_column("Required", style="yellow")
            progress_table.add_column("Status", style="white")
            
            for module in basic_modules:
                completed = self.user_progress.get(module, 0)
                status = "✅ Ready" if completed >= min_completion else "❌ Need more"
                progress_table.add_row(module.title(), str(completed), str(min_completion), status)
            
            console.print(progress_table)
            return False
        
        return True

    def run_challenge_1(self):
        """Challenge 1: Suspicious Log Analysis"""
        console.print("\n🔍 [bold red]CHALLENGE 1: SUSPICIOUS LOG ANALYSIS[/bold red] 🔍")
        
        scenario = Panel.fit("""
📋 SCENARIO:
You're a security analyst investigating a potential breach. 
The system administrator noticed unusual activity and provided you with log files.
Your task is to analyze the logs and identify the security incident.

🎯 OBJECTIVES:
1. Find evidence of failed login attempts
2. Identify the source IP address of the attacks
3. Determine which user accounts were targeted
4. Find any successful login attempts
        """, title="🚨 Security Incident", border_style="red")
        console.print(scenario)
        
        # Simulated log content
        log_content = """Dec 15 08:30:15 server sshd[1234]: Failed password for root from 192.168.1.50 port 54321
Dec 15 08:30:20 server sshd[1235]: Failed password for admin from 192.168.1.50 port 54322
Dec 15 08:30:25 server sshd[1236]: Failed password for root from 192.168.1.50 port 54323
Dec 15 08:30:30 server sshd[1237]: Failed password for user from 192.168.1.50 port 54324
Dec 15 08:30:35 server sshd[1238]: Failed password for test from 192.168.1.50 port 54325
Dec 15 08:31:42 server sshd[1239]: Accepted password for admin from 192.168.1.50 port 54326
Dec 15 08:32:15 server sshd[1240]: pam_unix(sshd:session): session opened for user admin
Dec 15 08:45:22 server sudo[1255]: admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/cat /etc/passwd
Dec 15 08:46:10 server sudo[1256]: admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/cat /etc/shadow"""
        
        questions = [
            ("What IP address is the source of the suspicious activity?", "192.168.1.50"),
            ("Which user account was successfully compromised?", "admin"),
            ("How many failed login attempts occurred before the successful login?", "5"),
            ("What sensitive file did the attacker access after gaining admin privileges?", "/etc/shadow")
        ]
        
        console.print("\n📄 Log file content:")
        console.print(log_content, style="dim white")
        
        score = 0
        for i, (question, answer) in enumerate(questions, 1):
            console.print(f"\n❓ Question {i}: {question}")
            user_answer = Prompt.ask("Your answer").strip()
            
            if answer.lower() in user_answer.lower():
                console.print("✅ Correct!", style="bold green")
                score += 1
            else:
                console.print(f"❌ Incorrect. The answer was: {answer}", style="bold red")
        
        if score >= 3:
            console.print(f"\n🎉 Challenge 1 PASSED! Score: {score}/4", style="bold green")
            console.print("🔍 Analysis: This was a brute force attack followed by privilege escalation!")
            return True
        else:
            console.print(f"\n❌ Challenge 1 FAILED. Score: {score}/4", style="bold red")
            console.print("💡 Tip: Look for patterns in timestamps, IP addresses, and usernames")
            return False

    def run_challenge_2(self):
        """Challenge 2: Network Intrusion Detection"""
        console.print("\n🌐 [bold red]CHALLENGE 2: NETWORK INTRUSION DETECTION[/bold red] 🌐")
        
        scenario = Panel.fit("""
📋 SCENARIO:
Your network monitoring tools detected unusual traffic patterns.
Multiple port scans and connection attempts have been logged.
Analyze the network data to understand the attack pattern.

🎯 OBJECTIVES:
1. Identify the scanning technique used
2. Find which services were targeted
3. Determine if any connections were successful
4. Assess the threat level
        """, title="🚨 Network Security Alert", border_style="red")
        console.print(scenario)
        
        # Simulated network data
        network_data = """
NMAP SCAN DETECTED:
Source: 10.0.0.100
Target: 192.168.1.10
Scan Type: SYN Stealth Scan
Ports Scanned: 21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389

OPEN PORTS FOUND:
22/tcp   open  ssh
80/tcp   open  http  
443/tcp  open  https
3389/tcp open  ms-wbt-server

CONNECTION ATTEMPTS:
10.0.0.100:54321 -> 192.168.1.10:22 [SYN]
10.0.0.100:54322 -> 192.168.1.10:80 [SYN]
10.0.0.100:54323 -> 192.168.1.10:443 [SYN]
10.0.0.100:54324 -> 192.168.1.10:3389 [SYN_ACK] - CONNECTION ESTABLISHED

ALERT: RDP brute force attempts detected on port 3389
Failed logins: Administrator (15 attempts), admin (12 attempts), guest (8 attempts)
CRITICAL: Successful RDP login detected for user 'backup' at 09:45:22
        """
        
        console.print("📊 Network monitoring data:")
        console.print(network_data, style="dim white")
        
        questions = [
            ("What type of port scan was performed?", "syn stealth scan"),
            ("Which service was successfully compromised?", "rdp"),
            ("What username was used for the successful login?", "backup"),
            ("Which port number is associated with the compromised service?", "3389")
        ]
        
        score = 0
        for i, (question, answer) in enumerate(questions, 1):
            console.print(f"\n❓ Question {i}: {question}")
            user_answer = Prompt.ask("Your answer").strip()
            
            if answer.lower() in user_answer.lower():
                console.print("✅ Correct!", style="bold green")
                score += 1
            else:
                console.print(f"❌ Incorrect. The answer was: {answer}", style="bold red")
        
        if score >= 3:
            console.print(f"\n🎉 Challenge 2 PASSED! Score: {score}/4", style="bold green")
            console.print("🌐 Analysis: Reconnaissance followed by targeted RDP attack!")
            return True
        else:
            console.print(f"\n❌ Challenge 2 FAILED. Score: {score}/4", style="bold red")
            console.print("💡 Tip: Focus on the scan type, open ports, and successful connections")
            return False

    def run_challenge_3(self):
        """Challenge 3: Malware Analysis"""
        console.print("\n🦠 [bold red]CHALLENGE 3: MALWARE ANALYSIS[/bold red] 🦠")
        
        scenario = Panel.fit("""
📋 SCENARIO:
A suspicious executable file was found on a user's computer.
Your job is to analyze the file without executing it to determine
if it's malicious and understand its potential impact.

🎯 OBJECTIVES:
1. Determine the file type and architecture
2. Extract readable strings and identify suspicious content
3. Calculate file hash for malware database lookup
4. Assess the malware's capabilities
        """, title="🚨 Malware Investigation", border_style="red")
        console.print(scenario)
        
        # Simulated analysis data
        analysis_data = {
            'file_info': "suspicious.exe: PE32 executable (console) Intel 80386 (stripped to external PDB), for MS Windows, UPX compressed",
            'strings': """kernel32.dll
CreateProcessA
WriteFile
RegSetValueA
SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run
http://malicious-c2.darkweb.onion/beacon
cmd.exe /c del /f /q %TEMP%\\*.log
powershell.exe -windowstyle hidden -executionpolicy bypass
admin123
password
192.168.1.1
/upload.php""",
            'hash': "a1b2c3d4e5f6789012345678901234567890abcdef",
            'size': "45,632 bytes"
        }
        
        console.print("🔬 File Analysis Results:")
        console.print(f"File Type: {analysis_data['file_info']}", style="yellow")
        console.print(f"File Size: {analysis_data['size']}", style="yellow")
        console.print(f"MD5 Hash: {analysis_data['hash']}", style="yellow")
        console.print("\n📝 Extracted Strings:", style="cyan")
        console.print(analysis_data['strings'], style="dim white")
        
        questions = [
            ("What type of executable is this? (PE32/ELF/Mach-O)", "PE32"),
            ("What compression/packing method was used?", "UPX"),
            ("What registry key does the malware try to modify for persistence?", "Run"),
            ("What suspicious network activity is indicated by the strings?", "c2")
        ]
        
        score = 0
        for i, (question, answer) in enumerate(questions, 1):
            console.print(f"\n❓ Question {i}: {question}")
            user_answer = Prompt.ask("Your answer").strip()
            
            if answer.lower() in user_answer.lower():
                console.print("✅ Correct!", style="bold green")
                score += 1
            else:
                console.print(f"❌ Incorrect. Look for: {answer}", style="bold red")
        
        if score >= 3:
            console.print(f"\n🎉 Challenge 3 PASSED! Score: {score}/4", style="bold green")
            console.print("🦠 Analysis: This appears to be a trojan with C2 communication capability!")
            return True
        else:
            console.print(f"\n❌ Challenge 3 FAILED. Score: {score}/4", style="bold red")
            console.print("💡 Tip: Look at file headers, registry keys, and network indicators")
            return False

    def run_challenge_4(self):
        """Challenge 4: Privilege Escalation Hunt"""
        console.print("\n⬆️ [bold red]CHALLENGE 4: PRIVILEGE ESCALATION HUNT[/bold red] ⬆️")
        
        scenario = Panel.fit("""
📋 SCENARIO:
You have limited user access to a Linux system and suspect there might be
ways to escalate privileges. Analyze the system to find potential
privilege escalation vectors.

🎯 OBJECTIVES:
1. Find SUID binaries that could be exploited
2. Identify world-writable files in sensitive locations
3. Check for misconfigured sudo permissions
4. Look for unprotected sensitive files
        """, title="🚨 Privilege Escalation Assessment", border_style="red")
        console.print(scenario)
        
        # Simulated system enumeration results
        enum_results = """
=== SUID BINARIES ===
/usr/bin/passwd
/usr/bin/sudo
/bin/su
/usr/bin/vim.basic  <- UNUSUAL!
/home/user/backup_script  <- SUSPICIOUS!

=== WORLD-WRITABLE FILES ===
/tmp/secret_backup
/var/log/application.log
/etc/passwd.bak  <- CRITICAL!

=== SUDO PERMISSIONS ===
User user may run the following commands on this host:
    (root) NOPASSWD: /usr/bin/find
    (root) NOPASSWD: /bin/cat /var/log/*

=== INTERESTING FILES ===
/home/user/.ssh/id_rsa (readable by others)
/etc/crontab (world-writable)
/var/www/.htpasswd (contains: admin:$apr1$xyz$hash)
        """
        
        console.print("🔍 System Enumeration Results:")
        console.print(enum_results, style="dim white")
        
        questions = [
            ("Which SUID binary is most unusual and exploitable?", "vim"),
            ("What critical system file is world-writable?", "/etc/passwd.bak"),
            ("Which sudo command could be used for privilege escalation?", "find"),
            ("What type of authentication file was found in /var/www/?", ".htpasswd")
        ]
        
        score = 0
        for i, (question, answer) in enumerate(questions, 1):
            console.print(f"\n❓ Question {i}: {question}")
            user_answer = Prompt.ask("Your answer").strip()
            
            if answer.lower() in user_answer.lower():
                console.print("✅ Correct!", style="bold green")
                score += 1
            else:
                console.print(f"❌ Incorrect. Look for: {answer}", style="bold red")
        
        if score >= 3:
            console.print(f"\n🎉 Challenge 4 PASSED! Score: {score}/4", style="bold green")
            console.print("⬆️ Analysis: Multiple privilege escalation vectors identified!")
            return True
        else:
            console.print(f"\n❌ Challenge 4 FAILED. Score: {score}/4", style="bold red")
            console.print("💡 Tip: Look for unusual SUID binaries and dangerous sudo permissions")
            return False

    def run_challenge_5(self):
        """Challenge 5: Incident Response Scenario"""
        console.print("\n🚨 [bold red]CHALLENGE 5: INCIDENT RESPONSE[/bold red] 🚨")
        
        scenario = Panel.fit("""
📋 SCENARIO:
A critical server has been compromised. You're the incident response lead.
Multiple indicators suggest an advanced persistent threat (APT).
Coordinate the response and identify the attack timeline.

🎯 OBJECTIVES:
1. Identify the initial attack vector
2. Determine the scope of compromise
3. Find evidence of data exfiltration
4. Recommend containment actions
        """, title="🚨 CRITICAL INCIDENT", border_style="red")
        console.print(scenario)
        
        # Complex scenario with multiple data sources
        incident_data = """
=== TIMELINE ANALYSIS ===
Dec 14 15:30 - Phishing email received by finance@company.com
Dec 14 15:45 - Suspicious macro-enabled document opened
Dec 14 16:00 - PowerShell execution detected
Dec 14 16:15 - Lateral movement to DC01.company.local
Dec 14 18:30 - Large data transfer to external IP 185.234.72.45
Dec 15 02:00 - Ransomware deployment across network

=== NETWORK INDICATORS ===
Outbound connections to:
- 185.234.72.45:443 (25GB transferred)
- tor-relay.darknet.onion:9050
- tempfile-share.ru (customer database uploaded)

=== FILE SYSTEM EVIDENCE ===
/tmp/.hidden_toolkit/
├── mimikatz.exe
├── psexec.exe  
├── customer_db_backup.sql.gz
└── ransom_note.txt

=== AFFECTED SYSTEMS ===
- FINANCE-WS01 (patient zero)
- DC01.company.local (domain controller)
- FILE-SRV01 (encrypted)
- DATABASE-01 (data copied)
        """
        
        console.print("📊 Incident Investigation Data:")
        console.print(incident_data, style="dim white")
        
        questions = [
            ("What was the initial attack vector?", "phishing"),
            ("How much data was exfiltrated (in GB)?", "25"),
            ("Which system was the patient zero?", "FINANCE-WS01"),
            ("What is the final stage of this attack campaign?", "ransomware")
        ]
        
        score = 0
        for i, (question, answer) in enumerate(questions, 1):
            console.print(f"\n❓ Question {i}: {question}")
            user_answer = input("Your answer: ").strip().lower()
            if user_answer == answer.lower():
                console.print("[green]✓ Correct![/]")
                score += 1
            else:
                console.print(f"[red]✗ Incorrect! The correct answer was: {answer}[/]")
        
        if score >= 3:
            self.completed_challenges.append(5)
            console.print("\n[bold green]🎉 Challenge 5 Completed![/]")
            return True
        else:
            console.print("\n[red]❌ Try again! Review the case details carefully.[/]")
            return False