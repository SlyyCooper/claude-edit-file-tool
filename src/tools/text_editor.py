"""
Implementation of the text editor tool for Claude.
"""

import os
from typing import Dict, List, Optional, Any, Union

from src.utils.file_utils import (
    validate_path,
    read_file_with_line_numbers,
    list_directory_contents,
    replace_text_in_file,
    insert_text_at_line,
    create_new_file,
    restore_from_backup
)

class TextEditorTool:
    """Tool for Claude to view and modify text files."""
    
    @staticmethod
    def handle_tool_use(tool_use) -> Dict[str, Any]:
        """
        Process a text editor tool use request from Claude.
        
        Args:
            tool_use: The tool use request containing command and parameters
            
        Returns:
            A dictionary with the tool result
        """
        # Handle both object and dictionary access patterns
        tool_id = getattr(tool_use, "id", None)
        if tool_id is None and isinstance(tool_use, dict):
            tool_id = tool_use.get("id", "")
            
        # Get input parameters - handle both object and dict access
        if isinstance(tool_use, dict):
            input_params = tool_use.get("input", {})
        else:
            input_params = getattr(tool_use, "input", {})
            # If input is an object and not a dict, convert attributes to dict
            if input_params and not isinstance(input_params, dict):
                try:
                    # Build a dictionary from the object's attributes
                    input_params = {
                        "command": getattr(input_params, "command", ""),
                        "path": getattr(input_params, "path", ""),
                        "old_str": getattr(input_params, "old_str", ""),
                        "new_str": getattr(input_params, "new_str", ""),
                        "file_text": getattr(input_params, "file_text", ""),
                        "insert_line": getattr(input_params, "insert_line", 0),
                        "view_range": getattr(input_params, "view_range", None)
                    }
                except Exception as e:
                    return {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": f"Error accessing tool parameters: {str(e)}",
                        "is_error": True
                    }
            
        # Now we should have input_params as a dict
        command = input_params.get("command", "")
        path = input_params.get("path", "")
        
        # Validate the path
        is_valid, abs_path, error_message = validate_path(path)
        if not is_valid:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": error_message,
                "is_error": True
            }
            
        # Process the command
        result = {"content": "", "is_error": False}
        
        try:
            if command == "view":
                result = TextEditorTool._handle_view(abs_path, input_params.get("view_range"))
            elif command == "str_replace":
                result = TextEditorTool._handle_str_replace(abs_path, input_params.get("old_str", ""), input_params.get("new_str", ""))
            elif command == "create":
                result = TextEditorTool._handle_create(abs_path, input_params.get("file_text", ""))
            elif command == "insert":
                result = TextEditorTool._handle_insert(abs_path, input_params.get("insert_line", 0), input_params.get("new_str", ""))
            elif command == "undo_edit":
                result = TextEditorTool._handle_undo_edit(abs_path)
            else:
                result = {"content": f"Error: Unknown command '{command}'", "is_error": True}
        except Exception as e:
            result = {"content": f"Error executing {command}: {str(e)}", "is_error": True}
            
        return {
            "type": "tool_result",
            "tool_use_id": tool_id,
            "content": result["content"],
            "is_error": result["is_error"]
        }
        
    @staticmethod
    def _handle_view(path: str, view_range: Optional[List[int]]) -> Dict[str, Union[str, bool]]:
        """Handle the 'view' command."""
        if os.path.isdir(path):
            try:
                contents = list_directory_contents(path)
                return {
                    "content": "\n".join(contents),
                    "is_error": False
                }
            except Exception as e:
                return {
                    "content": f"Error listing directory: {str(e)}",
                    "is_error": True
                }
        elif os.path.isfile(path):
            content = read_file_with_line_numbers(path, view_range)
            return {
                "content": content,
                "is_error": False
            }
        else:
            return {
                "content": f"Error: Path not found: {path}",
                "is_error": True
            }
            
    @staticmethod
    def _handle_str_replace(path: str, old_str: str, new_str: str) -> Dict[str, Union[str, bool]]:
        """Handle the 'str_replace' command."""
        if not old_str:
            return {
                "content": "Error: old_str parameter is required for str_replace command",
                "is_error": True
            }
            
        if not os.path.isfile(path):
            return {
                "content": f"Error: File not found: {path}",
                "is_error": True
            }
            
        success, message = replace_text_in_file(path, old_str, new_str)
        return {
            "content": message,
            "is_error": not success
        }
        
    @staticmethod
    def _handle_create(path: str, file_text: str) -> Dict[str, Union[str, bool]]:
        """Handle the 'create' command."""
        success, message = create_new_file(path, file_text)
        return {
            "content": message,
            "is_error": not success
        }
        
    @staticmethod
    def _handle_insert(path: str, insert_line: int, new_str: str) -> Dict[str, Union[str, bool]]:
        """Handle the 'insert' command."""
        success, message = insert_text_at_line(path, insert_line, new_str)
        return {
            "content": message,
            "is_error": not success
        }
        
    @staticmethod
    def _handle_undo_edit(path: str) -> Dict[str, Union[str, bool]]:
        """Handle the 'undo_edit' command."""
        success, message = restore_from_backup(path)
        return {
            "content": message,
            "is_error": not success
        }
