"""
Cryptography Module - Teaches encryption, hashing, and cryptographic concepts.
"""
import hashlib
import base64
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table

console = Console()

class CryptographyModule:
    def __init__(self):
        self.name = "cryptography"
        self.completed_topics = set()
        self.commands = {
            "hash": "Generate hashes of text",
            "encrypt": "Encrypt text with common algorithms",
            "decode": "Decode base64/hex/rot13",
            "cert": "View SSL certificate info",
            "genkey": "Generate encryption keys"
        }

    def run(self):
        """Run the cryptography module."""
        console.print(Panel.fit(
            "🔐 [bold blue]Cryptography Module[/bold blue] 🔐\n"
            "Learn about encryption, hashing, and cryptographic concepts.",
            style="blue"
        ))
        
        while True:
            self._show_menu()
            choice = Prompt.ask("\n> ").strip().lower()
            
            if choice == 'back':
                return len(self.completed_topics)
                
            if choice in self.commands:
                if choice == 'hash':
                    self._hash_tool()
                elif choice == 'encrypt':
                    self._encrypt_tool()
                elif choice == 'decode':
                    self._decode_tool()
                elif choice == 'cert':
                    self._cert_tool()
                elif choice == 'genkey':
                    self._genkey_tool()
                self.completed_topics.add(choice)
            else:
                console.print("[yellow]Invalid choice. Try again or type 'back'.[/]")
    
    def _show_menu(self):
        """Display the cryptography menu."""
        console.print("\n[bold]Available cryptographic tools:[/]")
        for cmd, desc in self.commands.items():
            status = "[green]✓[/] " if cmd in self.completed_topics else "  "
            console.print(f"  {status}{cmd:<10} - {desc}")
        console.print("\nEnter a tool name to use it, or 'back' to return.")
    
    def _hash_tool(self):
        """Interactive hash generator."""
        console.print("\n[bold]Hash Generator[/]")
        text = Prompt.ask("Enter text to hash").encode()
        
        hashes = [
            ("MD5", hashlib.md5(text).hexdigest()),
            ("SHA-1", hashlib.sha1(text).hexdigest()),
            ("SHA-256", hashlib.sha256(text).hexdigest()),
            ("SHA-512", hashlib.sha512(text).hexdigest()),
            ("BLAKE2b", hashlib.blake2b(text).hexdigest())
        ]
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Algorithm")
        table.add_column("Hash Value")
        
        for algo, hash_val in hashes:
            table.add_row(algo, hash_val)
        
        console.print("\nHash values:")
        console.print(table)
        console.print("\n[dim]Note: MD5 and SHA-1 are considered cryptographically broken. Use stronger hashes like SHA-256 or SHA-3 for security.[/]")
    
    def _encrypt_tool(self):
        """Demonstrate encryption concepts."""
        console.print("\n[bold]Encryption Demonstration[/]")
        console.print("This is a simplified demonstration. In practice, use established libraries.")
        
        text = Prompt.ask("Enter text to encrypt").encode()
        
        # Simple Caesar cipher for demonstration
        shift = IntPrompt.ask("Enter shift value (1-25)", default=3)
        encrypted = "".join(chr((c - 97 + shift) % 26 + 97) if c >= 97 and c <= 122 else chr(c) for c in text)
        
        console.print(f"\nOriginal: {text.decode()}")
        console.print(f"Encrypted (Caesar Cipher): {encrypted}")
        
        # Show base64 encoding
        b64 = base64.b64encode(text).decode()
        console.print(f"\nBase64 Encoded: {b64}")
        
        console.print("\n[dim]Note: This is a basic demonstration. Use libraries like PyCryptodome for real encryption.[/]")
    
    def _decode_tool(self):
        """Decode common encodings."""
        console.print("\n[bold]Decoder Tool[/]")
        console.print("Supported formats: base64, hex, ROT13")
        
        text = Prompt.ask("Enter encoded text").strip()
        
        try:
            # Try Base64
            decoded = base64.b64decode(text).decode('utf-8', errors='ignore')
            console.print(f"\nBase64 Decoded: {decoded}")
        except:
            pass
            
        try:
            # Try Hex
            if all(c in '0123456789abcdefABCDEF ' for c in text.replace("0x", "").replace(":", "").replace(" ", "")):
                hex_str = text.replace("0x", "").replace(":", "").replace(" ", "")
                decoded = bytes.fromhex(hex_str).decode('utf-8', errors='ignore')
                console.print(f"\nHex Decoded: {decoded}")
        except:
            pass
            
        # ROT13
        rot13 = str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        )
        console.print(f"\nROT13: {text.translate(rot13)}")
    
    def _cert_tool(self):
        """Show certificate information."""
        console.print("\n[bold]Certificate Information[/]")
        console.print("This would show SSL/TLS certificate details in a real implementation.")
        console.print("Example command: openssl s_client -connect example.com:443 | openssl x509 -text")
    
    def _genkey_tool(self):
        """Generate encryption keys."""
        console.print("\n[bold]Key Generation[/]")
        console.print("This would generate encryption keys in a real implementation.")
        console.print("Example commands:")
        console.print("  openssl genrsa -out private.key 2048")
        console.print("  openssl rsa -in private.key -pubout -out public.key")
