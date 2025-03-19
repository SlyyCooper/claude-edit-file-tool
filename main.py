#!/usr/bin/env python3
"""
Main entry point for the Claude Text Editor Chatbot.
This application provides a command-line interface to interact with Claude,
allowing it to view and modify text files through its text editor tool.
"""

import os
import sys
import argparse
from typing import Optional

from src.chatbot import ClaudeTextEditorChatbot
from src.config.settings import WORKSPACE_DIR

def create_sample_file() -> None:
    """Create a sample Python file in the workspace for demonstration."""
    sample_path = os.path.join(WORKSPACE_DIR, "sample.py")
    
    if not os.path.exists(sample_path):
        with open(sample_path, "w") as f:
            f.write('''def calculate_factorial(n):
    """Calculate the factorial of a number."""
    if n == 0 or n == 1:
        return 1
    else
        return n * calculate_factorial(n - 1)

def main():
    print("Factorial of 5:", calculate_factorial(5))
    
if __name__ == "__main__":
    main()
''')
        print(f"Created sample file with a deliberate syntax error at {sample_path}")

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_help() -> None:
    """Print help information."""
    print("\nClaude Text Editor Chatbot Help:")
    print("--------------------------------")
    print("  /help       - Show this help message")
    print("  /clear      - Clear the screen")
    print("  /reset      - Reset the conversation")
    print("  /sample     - Create a sample Python file with a syntax error")
    print("  /workspace  - Print the workspace directory path")
    print("  /exit       - Exit the chatbot")
    print("  /list       - List files in the workspace directory")
    print("\nExample commands for Claude:")
    print("  - Can you check the files in my workspace?")
    print("  - Please fix the syntax error in sample.py")
    print("  - Create a new file called hello.py that prints 'Hello, World!'")
    print("  - Add proper documentation to all functions in sample.py")
    print("--------------------------------")

def run_cli(chatbot: ClaudeTextEditorChatbot) -> None:
    """
    Run the command-line interface for the chatbot.
    
    Args:
        chatbot: The initialized chatbot instance
    """
    clear_screen()
    print("Claude Text Editor Chatbot")
    print("=========================")
    print("Type '/help' for available commands or '/exit' to quit")
    print(f"Workspace directory: {WORKSPACE_DIR}")
    print("=========================")
    
    # Create the workspace directory if it doesn't exist
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)
        print(f"Created workspace directory: {WORKSPACE_DIR}")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")
            
            # Process command shortcuts
            if user_input.startswith("/"):
                command = user_input.lower()
                
                if command == "/exit":
                    print("Exiting chatbot. Goodbye!")
                    break
                elif command == "/help":
                    print_help()
                    continue
                elif command == "/clear":
                    clear_screen()
                    continue
                elif command == "/reset":
                    chatbot = ClaudeTextEditorChatbot()
                    print("Conversation reset.")
                    continue
                elif command == "/sample":
                    create_sample_file()
                    continue
                elif command == "/workspace":
                    print(f"Workspace directory: {WORKSPACE_DIR}")
                    continue
                elif command == "/list":
                    if os.path.exists(WORKSPACE_DIR):
                        files = os.listdir(WORKSPACE_DIR)
                        if files:
                            print("\nFiles in workspace:")
                            for file in files:
                                if file.startswith('.'):
                                    continue
                                file_path = os.path.join(WORKSPACE_DIR, file)
                                type_prefix = "[DIR]" if os.path.isdir(file_path) else "[FILE]"
                                print(f"  {type_prefix} {file}")
                        else:
                            print("Workspace is empty.")
                    else:
                        print(f"Workspace directory not found: {WORKSPACE_DIR}")
                    continue
            
            # Process regular message with Claude
            response = chatbot.chat(user_input)
            
            # Print Claude's response
            print("\nClaude:", response)
            
        except KeyboardInterrupt:
            print("\nExiting chatbot. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Type '/reset' to reset the conversation or '/exit' to quit.")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Claude Text Editor Chatbot")
    parser.add_argument("--sample", action="store_true", help="Create a sample file with a syntax error")
    
    args = parser.parse_args()
    
    if args.sample:
        create_sample_file()
    
    try:
        # Initialize the chatbot
        chatbot = ClaudeTextEditorChatbot()
        
        # Run the CLI
        run_cli(chatbot)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
