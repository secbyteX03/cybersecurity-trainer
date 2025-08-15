# Cybersecurity Command Trainer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A safe, beginner-friendly command-line interface (CLI) tool designed to help you learn essential cybersecurity commands in a risk-free environment.

## Table of Contents

- [Project Overview](#project-overview)
- [Why I Built This](#why-i-built-this)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [How to Use](#how-to-use)
- [Module Reference](#module-reference)
- [Challenge Mode](#challenge-mode)
- [Development & Contribution](#development--contribution)
- [Testing & Validation](#testing--validation)
- [Security & Safety](#security--safety)
- [Roadmap](#roadmap)
- [Credits & Resources](#credits--resources)
- [License](#license)
- [Contact & Support](#contact--support)

## Project Overview

The Cybersecurity Command Trainer is an interactive learning platform that simulates a Linux terminal environment, allowing users to practice cybersecurity commands without the risk of damaging their system. It's perfect for beginners who want to learn Linux commands in a safe, guided environment.

## Why I Built This

As cybersecurity becomes increasingly important, there's a growing need for accessible training tools that allow beginners to practice safely. Many existing tools either require complex setups or risk damaging the user's system. This trainer was created to provide a completely safe, self-contained learning environment.

## Features

- **Safe Learning Environment**: No real system changes or dangerous commands
- **Interactive Command Practice**: Hands-on experience with immediate feedback
- **Progressive Learning Path**: Structured modules that build on each other
- **Real-world Scenarios**: Practical challenges based on actual security tasks
- **Cross-platform**: Works on Windows, macOS, and Linux
- **No Internet Required**: All training is self-contained

## Project Structure

```
cybersecurity-trainer/
├── modules/               # Training modules
│   ├── __init__.py
│   ├── basics.py         # Linux basics module
│   ├── networking.py     # Network analysis
│   ├── forensics.py      # Digital forensics
│   ├── permissions.py    # File permissions
│   └── challenge.py      # Security challenges
├── tests/                # Test files
│   └── test_trainer.py
├── trainer.py            # Main application
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── LICENSE              # MIT License
```

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)
- Windows, macOS, or Linux operating system

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/secbyteX03/cybersecurity-trainer.git
   cd cybersecurity-trainer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the trainer**:
   ```bash
   python trainer.py
   ```

## How to Use

1. **Main Menu Navigation**:
   - Use number keys (0-7) to select options
   - Type 'back' during lessons to return to the main menu
   - Type 'exit' or use Ctrl+C to quit

### Guided Lesson Mode

The trainer includes a guided learning path that takes you through cybersecurity concepts step by step:

1. From the main menu, select "Guided Lessons" (option 1)
2. Choose a lesson from the available options
3. Follow the on-screen instructions to complete each step
4. Type the commands exactly as shown to progress
5. Use the following commands during lessons:
   - `next` - Go to the next step
   - `prev` - Go back to the previous step
   - `exit` - Return to the lesson selection
   - `help` - Show available commands

Example lesson structure:
```json
{
  "module": "linux_basics",
  "title": "Linux Basics",
  "description": "Learn essential Linux commands and concepts",
  "lessons": [
    {
      "id": "intro",
      "title": "Introduction to Linux",
      "content": "Welcome to Linux Basics! In this module, you'll learn essential Linux commands.",
      "expected_input": "next"
    },
    {
      "id": "pwd",
      "title": "Finding Your Way: pwd",
      "content": "The 'pwd' command shows your current working directory.\n\nTry it now by typing: pwd",
      "command": "pwd",
      "hint": "Type 'pwd' and press Enter",
      "success_message": "Great! You've learned how to find your current directory."
    }
  ]
}
```

### Interactive Modules

2. **Example Session**:
   ```
   === CYBERSECURITY COMMAND TRAINER ===

   MAIN MENU

   [1] Linux Basics
      Progress: 0/10
   [2] Networking
      Progress: 0/8
   [3] Digital Forensics
      Progress: 0/6
   [4] Permissions
      Progress: 0/7
   [5] Challenges
      Completed: 0/5
   [6] Help
      Command reference and tips
   [0] Exit
      Quit the trainer

   Select a training module (1-6, 0 to exit): 1
   ```

## Module Reference

### 1. Linux Basics
- **Commands Covered**: `ls`, `cd`, `pwd`, `find`, `grep`, `cat`, `head`, `tail`, `wc`, `history`
- **Skills Learned**: File system navigation, text searching, command history
- **Security Focus**: Identifying suspicious files, analyzing logs, system reconnaissance

### 2. Networking
- **Commands Covered**: `ping`, `netstat`, `nmap`, `ss`, `ifconfig`/`ip`
- **Skills Learned**: Network scanning, connection monitoring, port analysis
- **Security Focus**: Network reconnaissance, identifying open ports, detecting suspicious connections

### 3. Digital Forensics
- **Commands Covered**: `file`, `strings`, `hexdump`, `md5sum`/`shasum`, `stat`
- **Skills Learned**: File analysis, string extraction, hashing, metadata examination
- **Security Focus**: File identification, evidence collection, integrity verification

### 4. File Permissions
- **Commands Covered**: `ls -l`, `chmod`, `chown`, `umask`, `find` with permissions
- **Skills Learned**: Permission management, ownership, access control
- **Security Focus**: Secure file permissions, privilege escalation prevention

## Challenge Mode

Test your skills with realistic security scenarios:

1. **Log Analysis**
   - Analyze server logs to identify a security breach
   - Use `grep`, `awk`, and other text processing tools

2. **Network Intrusion**
   - Detect and analyze suspicious network activity
   - Use network analysis tools to identify the attack

3. **File System Forensics**
   - Investigate a compromised system
   - Find and analyze suspicious files

4. **Permission Audit**
   - Identify and fix insecure file permissions
   - Prevent privilege escalation vulnerabilities

5. **Incident Response**
   - Respond to a simulated security incident
   - Document findings and recommend fixes

## Development & Contribution

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Testing & Validation

Run the test suite:
```bash
python -m pytest tests/
```

Or run specific tests:
```bash
python -m pytest tests/test_module.py::TestClass::test_method
```

## Security & Safety

### Safety Features
- No actual system commands are executed
- All outputs are simulated
- No network access required
- No root/administrator privileges needed

### Best Practices
- Always review code before execution
- Use in a controlled environment
- Don't use real credentials or sensitive data

## Roadmap

### Upcoming Features
- [ ] Additional modules (Web Security, Cryptography)
- [ ] More interactive challenges
- [ ] Progress tracking and achievements
- [ ] Docker support for easy setup
- [ ] Multi-language support

## Credits & Resources

### Built With
- [Python](https://www.python.org/) - Programming language
- [Rich](https://github.com/willmcgugan/rich) - Terminal formatting
- [Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io/) - Interactive prompts

### Learning Resources
- [Linux Command Line Basics](https://ubuntu.com/tutorials/command-line-for-beginners)
- [Cybersecurity Essentials](https://www.cisco.com/c/en/us/products/security/cybersecurity-essentials.html)
- [OWASP Security Knowledge Framework](https://owasp.org/www-project-security-knowledge-framework/)

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact & Support

- **GitHub Issues**: [Report Issues](https://github.com/secbyteX03/cybersecurity-trainer/issues)
- **Email**: [amaizing.faith1@gmail.com](mailto:amaizing.faith1@gmail.com)
- **Twitter**: [@faith_magret](https://x.com/faith_magret)

---

<div align="center">
  Made with ❤️ for cybersecurity education
</div>
