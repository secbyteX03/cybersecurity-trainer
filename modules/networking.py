"""
Networking Module - Network analysis and security commands
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import random
import time

console = Console()

class NetworkingModule:
    def __init__(self):
        self.commands_completed = 0
        self.total_commands = 8

    def simulate_ping(self, target=""):
        """Simulate ping command output"""
        if not target:
            return "Usage: ping [hostname/IP]"
            
        time.sleep(1)  # Simulate network delay
        
        if "example.com" in target or "8.8.8.8" in target:
            return f"""
            PING {target} (93.184.216.34) 56(84) bytes of data.
            64 bytes from 93.184.216.34: icmp_seq=1 ttl=57 time=12.3 ms
            64 bytes from 93.184.216.34: icmp_seq=2 ttl=57 time=11.8 ms
            64 bytes from 93.184.216.34: icmp_seq=3 ttl=57 time=12.1 ms
            
            --- {target} ping statistics ---
            3 packets transmitted, 3 received, 0% packet loss, time 2003ms
            rtt min/avg/max/mdev = 11.879/12.105/12.345/0.189 ms
            """
        else:
            return f"ping: {target}: Name or service not known"

    def simulate_netstat(self, args=""):
        """Simulate netstat command output"""
        if "-tuln" in args:
            return """
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address  Foreign Address  State
            tcp        0      0 0.0.0.0:22     0.0.0.0:*        LISTEN
            tcp        0      0 127.0.0.1:631   0.0.0.0:*        LISTEN
            tcp6       0      0 :::80           :::*             LISTEN
            tcp6       0      0 :::22           :::*             LISTEN
            udp        0      0 0.0.0.0:68      0.0.0.0:*
            """
        else:
            return """
            Active Internet connections
            Proto Recv-Q Send-Q Local Address  Foreign Address  State
            tcp        0      0 192.168.1.5:ssh 192.168.1.10:56789 ESTABLISHED
            tcp6       0      0 localhost:mysql localhost:45678  TIME_WAIT
            """

    def simulate_nmap(self, target=""):
        """Simulate nmap scan output"""
        if not target:
            return "Usage: nmap [options] [target]"
            
        time.sleep(2)  # Simulate scanning delay
        
        return f"""
        Starting Nmap 7.80 ( https://nmap.org )
        Nmap scan report for {target} (192.168.1.1)
        Host is up (0.012s latency).
        Not shown: 997 filtered ports
        PORT    STATE  SERVICE    VERSION
        22/tcp  open   ssh        OpenSSH 7.9p1 (protocol 2.0)
        80/tcp  open   http       Apache httpd 2.4.41
        443/tcp closed https
        
        Nmap done: 1 IP address (1 host up) scanned in 2.34 seconds
        """

    def simulate_ss(self, args=""):
        """Simulate ss command output (socket statistics)"""
        return """
        Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
        tcp   ESTAB 0      0      192.168.1.5:ssh     192.168.1.10:56789
        tcp   LISTEN0      128    0.0.0.0:http          0.0.0.0:*
        tcp   LISTEN0      128    0.0.0.0:ssh           0.0.0.0:*
        """

    def run_networking_lesson(self, cmd, explanation, security_context, example):
        """Run interactive networking lesson"""
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
            if cmd.startswith("ping"):
                target = user_input.split()[1] if len(user_input.split()) > 1 else ""
                console.print(self.simulate_ping(target))
            elif cmd.startswith("netstat"):
                console.print(self.simulate_netstat(user_input))
            elif cmd.startswith("nmap"):
                target = user_input.split()[-1] if len(user_input.split()) > 1 else ""
                console.print(self.simulate_nmap(target))
            elif cmd.startswith("ss"):
                console.print(self.simulate_ss(user_input))
            else:
                console.print("Command output simulation not implemented yet.")
            
            self.commands_completed += 1
            console.print(f"\n[green]✓ Command executed! ({self.commands_completed}/{self.total_commands} completed)[/]")
            break

    def show_network_security_tips(self):
        """Display network security best practices"""
        tips = [
            "🔒 Always use SSH keys instead of passwords for remote access",
            "🌐 Use a VPN when connecting to public Wi-Fi networks",
            "🔍 Regularly scan your network for unauthorized devices",
            "🚫 Disable unnecessary services to reduce attack surface",
            "📊 Monitor network traffic for unusual patterns",
            "🛡️  Use a firewall to control incoming/outgoing connections",
            "🔑 Implement network segmentation to limit lateral movement"
        ]
        
        console.print("\n[bold]Network Security Tips:[/bold]")
        for tip in tips:
            console.print(f"• {tip}")

    def run(self):
        """Run the networking module"""
        console.print(Panel.fit("🌐 [bold]Module 2: Networking[/bold]", 
                             subtitle="Master network analysis and security"))
        
        lessons = [
            {
                "cmd": "ping",
                "explanation": "Test network connectivity to a host",
                "security": "Often used in network reconnaissance.\n"
                           "- Can be used to map out a network\n"
                           "- ICMP echo requests might be blocked by firewalls",
                "example": "example.com"
            },
            {
                "cmd": "netstat",
                "explanation": "Display network connections and listening ports",
                "security": "Reveals open ports and active connections.\n"
                           "- Look for unusual listening services\n"
                           "- Identify unauthorized connections",
                "example": "-tuln"
            },
            {
                "cmd": "nmap",
                "explanation": "Network exploration and security auditing",
                "security": "Powerful tool for network discovery.\n"
                           "- Used for security assessments\n"
                           "- Can be used maliciously for reconnaissance",
                "example": "-sV -sC 192.168.1.1"
            },
            {
                "cmd": "ss",
                "explanation": "Socket statistics (modern replacement for netstat)",
                "security": "Shows socket connections.\n"
                           "- Faster than netstat\n"
                           "- Useful for troubleshooting network issues",
                "example": "-tuln"
            }
        ]
        
        for lesson in lessons:
            self.run_networking_lesson(
                lesson["cmd"],
                lesson["explanation"],
                lesson["security"],
                lesson.get("example", "")
            )
        
        self.show_network_security_tips()
        
        console.print("\n[bold green]🎉 Module 2 Complete![/]")
        console.print("You've learned essential network analysis commands for cybersecurity.")
        
        return self.commands_completed
