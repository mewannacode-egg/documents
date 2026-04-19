SHHO is a beginner-friendly Python wrapper designed to simplify os and subprocess calls into human-readable functions. It provides a safer, more intuitive way to handle files and system operations without the complexity of standard libraries.

Official Discord: https://discord.gg/B9fGhbPGkP

# Features
Human-Readable Syntax: Replace dense os code with clear, simple commands.

Developer Utilities: Built-in tools for version tracking and function discovery.

# Installation
Install the latest version (0.1.1) via pip:
pip install shho --upgrade

# Quick Demo
from shho import fle, folder, path, system

file.create("test.py")

file.write("test.py", "print('Hello World!'", mode="overwrite")

system.run("test.py")

output: Hello World!

# Create a file easily
file.create("hello.txt", "Hello from SHHO!").

Refined file handling logic for better reliability.

Why use SHHO?
Standard Python system calls can be intimidating for beginners. SHHO acts as a bridge, allowing you to focus on building your project.

# Check out the source code
https://raw.githubusercontent.com/mewannacode-egg/SHHO/refs/heads/main/shho.py

# And the documentation
https://raw.githubusercontent.com/mewannacode-egg/SHHO/refs/heads/main/documents


# -Update LOG- #
# ver 0.1.0:
-First version ever! May contain bugs, i hope you can send me feedback!!
# ver 0.1.1:
-This version fixes some bugs.
