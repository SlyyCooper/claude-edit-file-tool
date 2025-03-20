"""
Pydantic models for the Claude Text Editor API.
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field

# ----------------------------------------------------------------------
# --- Chat Models
# ----------------------------------------------------------------------

class UserMessage(BaseModel):
    """Model for user messages sent to the chatbot."""
    content: str = Field(..., description="The content of the user's message")
    
class ChatResponse(BaseModel):
    """Model for chatbot responses."""
    response: str = Field(..., description="The chatbot's response")

# ----------------------------------------------------------------------
# --- File Operation Models
# ----------------------------------------------------------------------

class FileOperation(BaseModel):
    """Model for file operations using the text editor tool."""
    command: str = Field(..., description="The command to execute (view, str_replace, create, insert, undo_edit)")
    path: str = Field(..., description="The path to the file or directory")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters for the command")
    
class FileOperationResponse(BaseModel):
    """Model for file operation responses."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="A message describing the result")
    error: bool = Field(False, description="Whether an error occurred")
    
class ListFilesResponse(BaseModel):
    """Model for the response when listing files."""
    path: str = Field(..., description="The path that was listed")
    files: List[str] = Field(default_factory=list, description="List of files in the path")
    directories: List[str] = Field(default_factory=list, description="List of directories in the path")

# ----------------------------------------------------------------------
# --- Text Editor Command Parameter Models
# ----------------------------------------------------------------------

class ViewParams(BaseModel):
    """Parameters for the view command."""
    view_range: Optional[List[int]] = Field(None, description="Range of lines to view [start, end]")
    
class StrReplaceParams(BaseModel):
    """Parameters for the str_replace command."""
    old_str: str = Field(..., description="Text to replace")
    new_str: str = Field(..., description="New text to insert")
    
class CreateParams(BaseModel):
    """Parameters for the create command."""
    file_text: str = Field(..., description="Content for the new file")
    
class InsertParams(BaseModel):
    """Parameters for the insert command."""
    insert_line: int = Field(..., description="Line number after which to insert text")
    new_str: str = Field(..., description="Text to insert") 