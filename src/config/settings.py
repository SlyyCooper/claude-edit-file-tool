"""
Configuration settings for the Claude Text Editor Chatbot application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = "claude-3-7-sonnet-20250219"
MAX_TOKENS = 4096

# File system configuration
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "workspace"))
BACKUP_DIR = os.path.join(WORKSPACE_DIR, ".backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

# Security settings
ALLOWED_EXTENSIONS = {
    ".py", ".txt", ".md", ".json", ".yaml", ".yml", 
    ".html", ".css", ".js", ".ts", ".jsx", ".tsx"
}

# Tool definitions
TEXT_EDITOR_TOOL_DEFINITION = {
    "name": "str_replace_editor",
    "description": "A text editor tool that can view and modify text files. Use this tool to read files, make precise edits, create new files, or insert text at specific locations. This tool operates on files within the allowed workspace directory.",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "enum": ["view", "str_replace", "create", "insert", "undo_edit"],
                "description": "The command to execute: 'view' to read a file/directory, 'str_replace' to replace text, 'create' to make a new file, 'insert' to add text at a position, 'undo_edit' to revert changes."
            },
            "path": {
                "type": "string",
                "description": "The path to the file or directory to operate on, relative to the workspace directory."
            },
            "old_str": {
                "type": "string",
                "description": "The text to replace (for str_replace command). Must match exactly with whitespace and indentation."
            },
            "new_str": {
                "type": "string",
                "description": "The new text to insert (for str_replace and insert commands)."
            },
            "file_text": {
                "type": "string",
                "description": "The content for a new file (for create command)."
            },
            "insert_line": {
                "type": "integer",
                "description": "The line number after which to insert text (for insert command). Line numbers start at 1, and 0 means insert at the beginning."
            },
            "view_range": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "The range of lines to view [start, end] (for view command). Line numbers start at 1, and -1 for end means read to the end of the file."
            }
        },
        "required": ["command", "path"]
    }
}
