"""
Utility functions for file operations with security checks.
"""

import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Union

from src.config.settings import WORKSPACE_DIR, BACKUP_DIR, ALLOWED_EXTENSIONS

# --------------------------------------------------
# --- Path Validation Functions
# --------------------------------------------------

def validate_path(path: str) -> Tuple[bool, str, Optional[str]]:
    """
    Validate that a path is within the allowed workspace directory and has allowed extension.
    
    Args:
        path: The path to validate (absolute or relative)
        
    Returns:
        Tuple of (is_valid, absolute_path, error_message)
    """
    # Normalize the path
    if os.path.isabs(path):
        abs_path = os.path.normpath(path)
    else:
        abs_path = os.path.normpath(os.path.join(WORKSPACE_DIR, path))
    
    # Check if the path is within the allowed directory
    if not abs_path.startswith(WORKSPACE_DIR):
        return False, abs_path, f"Access denied: Path must be within the workspace directory: {WORKSPACE_DIR}"
    
    # Check if the extension is allowed (only for files, not directories)
    if os.path.isfile(abs_path) or not os.path.exists(abs_path):
        file_ext = os.path.splitext(abs_path)[1].lower()
        if file_ext and file_ext not in ALLOWED_EXTENSIONS:
            return False, abs_path, f"Access denied: File extension '{file_ext}' is not allowed"
    
    return True, abs_path, None

# --------------------------------------------------
# --- Backup and Restore Functions
# --------------------------------------------------

def create_backup(file_path: str) -> Optional[str]:
    """
    Create a backup of a file before modifying it.
    
    Args:
        file_path: The absolute path to the file
        
    Returns:
        The path to the backup file or None if creation failed
    """
    if not os.path.exists(file_path):
        return None
        
    try:
        # Create a unique backup file name with timestamp and UUID
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_name = os.path.basename(file_path)
        backup_file = os.path.join(BACKUP_DIR, f"{file_name}.{timestamp}.{unique_id}.bak")
        
        # Copy the file to the backup location
        shutil.copy2(file_path, backup_file)
        return backup_file
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return None

def get_most_recent_backup(file_path: str) -> Optional[str]:
    """
    Get the most recent backup for a file.
    
    Args:
        file_path: The absolute path to the file
        
    Returns:
        The path to the most recent backup file or None if not found
    """
    file_name = os.path.basename(file_path)
    backup_files = [
        os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR)
        if f.startswith(file_name + ".")
    ]
    
    if not backup_files:
        return None
        
    # Sort by creation time, newest first
    backup_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
    return backup_files[0]

# --------------------------------------------------
# --- Directory Listing Functions
# --------------------------------------------------

def list_directory_contents(directory_path: str) -> List[str]:
    """
    List the contents of a directory with [FILE] and [DIR] prefixes.
    
    Args:
        directory_path: The absolute path to the directory
        
    Returns:
        A list of directory entries with type prefixes
    """
    contents = []
    
    for item in sorted(os.listdir(directory_path)):
        item_path = os.path.join(directory_path, item)
        
        # Skip hidden files and backup directory
        if item.startswith('.') or item_path == BACKUP_DIR:
            continue
            
        prefix = "[DIR]" if os.path.isdir(item_path) else "[FILE]"
        contents.append(f"{prefix} {item}")
    
    return contents

# --------------------------------------------------
# --- File Reading Functions
# --------------------------------------------------

def read_file_with_line_numbers(file_path: str, view_range: Optional[List[int]] = None) -> str:
    """
    Read a file and add line numbers to each line.
    
    Args:
        file_path: The absolute path to the file
        view_range: Optional range of lines to read [start, end]
        
    Returns:
        The file content with line numbers
    """
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        start = 1
        end = len(lines)
        
        if view_range and len(view_range) == 2:
            start = max(1, view_range[0])
            if view_range[1] != -1:
                end = min(len(lines), view_range[1])
            
        # Add line numbers to the selected range
        numbered_lines = [f"{i}: {lines[i-1]}" for i in range(start, end + 1)]
        return ''.join(numbered_lines)
    except Exception as e:
        return f"Error reading file: {str(e)}"

# --------------------------------------------------
# --- File Modification Functions
# --------------------------------------------------

def replace_text_in_file(file_path: str, old_str: str, new_str: str) -> Tuple[bool, str]:
    """
    Replace text in a file, ensuring there's exactly one match.
    
    Args:
        file_path: The absolute path to the file
        old_str: The text to replace
        new_str: The new text
        
    Returns:
        Tuple of (success, message)
    """
    if not os.path.exists(file_path):
        return False, f"Error: File not found: {file_path}"
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for the number of matches
        match_count = content.count(old_str)
        
        if match_count == 0:
            return False, "Error: No match found for replacement text"
        elif match_count > 1:
            return False, f"Error: Found {match_count} matches for replacement text. Please provide more context for a unique match."
            
        # Create a backup before modifying
        backup_path = create_backup(file_path)
        
        # Perform the replacement
        new_content = content.replace(old_str, new_str)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return True, f"Successfully replaced text. Backup created at {os.path.basename(backup_path)}."
    except Exception as e:
        return False, f"Error replacing text: {str(e)}"

def insert_text_at_line(file_path: str, insert_line: int, new_str: str) -> Tuple[bool, str]:
    """
    Insert text after a specific line in the file.
    
    Args:
        file_path: The absolute path to the file
        insert_line: The line number after which to insert text (0 means beginning of file)
        new_str: The text to insert
        
    Returns:
        Tuple of (success, message)
    """
    try:
        # Create the file if it doesn't exist
        if not os.path.exists(file_path):
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(file_path, 'w', encoding='utf-8') as f:
                pass
        
        # Create a backup before modifying
        backup_path = create_backup(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Ensure the insert_line is valid
        if insert_line < 0:
            insert_line = 0
        elif insert_line > len(lines):
            insert_line = len(lines)
            
        # Add a newline to the inserted text if needed
        if not new_str.endswith('\n'):
            new_str += '\n'
            
        # Insert the text
        lines.insert(insert_line, new_str)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
        return True, f"Successfully inserted text at line {insert_line}. Backup created at {os.path.basename(backup_path) if backup_path else 'N/A'}."
    except Exception as e:
        return False, f"Error inserting text: {str(e)}"

# --------------------------------------------------
# --- File Creation Functions
# --------------------------------------------------

def create_new_file(file_path: str, file_text: str) -> Tuple[bool, str]:
    """
    Create a new file with the specified content.
    
    Args:
        file_path: The absolute path to the file
        file_text: The content to write to the file
        
    Returns:
        Tuple of (success, message)
    """
    try:
        # Check if the file already exists
        if os.path.exists(file_path):
            return False, f"Error: File already exists: {file_path}"
            
        # Create the directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_text)
            
        return True, f"Successfully created file: {file_path}"
    except Exception as e:
        return False, f"Error creating file: {str(e)}"

# --------------------------------------------------
# --- File Restoration Functions
# --------------------------------------------------

def restore_from_backup(file_path: str) -> Tuple[bool, str]:
    """
    Restore a file from its most recent backup.
    
    Args:
        file_path: The absolute path to the file
        
    Returns:
        Tuple of (success, message)
    """
    try:
        backup_path = get_most_recent_backup(file_path)
        
        if not backup_path:
            return False, f"Error: No backup found for {file_path}"
            
        # Copy the backup back to the original location
        shutil.copy2(backup_path, file_path)
        
        return True, f"Successfully restored from backup: {os.path.basename(backup_path)}"
    except Exception as e:
        return False, f"Error restoring from backup: {str(e)}"
