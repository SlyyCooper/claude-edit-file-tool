#!/usr/bin/env python3
"""
FastAPI backend for the Claude Text Editor Chatbot.
This application provides a REST API to interact with Claude,
allowing it to view and modify text files through its text editor tool.
"""

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------
import os
import sys
import logging
from typing import Dict, List, Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.chatbot import ClaudeTextEditorChatbot
from src.config.settings import WORKSPACE_DIR
from src.api.models import (
    UserMessage, 
    ChatResponse, 
    FileOperation, 
    FileOperationResponse,
    ListFilesResponse
)
from src.api.dependencies import get_chatbot

# ----------------------------------------------------------------------
# Create FastAPI app
# ----------------------------------------------------------------------
app = FastAPI(
    title="Claude Text Editor API",
    description="API for interacting with Claude Text Editor Tool",
    version="1.0.0"
)

# ----------------------------------------------------------------------
# Configure CORS
# ----------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# API Routes
# ----------------------------------------------------------------------

@app.get("/")
async def root():
    """Root endpoint, provides API information."""
    return {
        "message": "Claude Text Editor API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: UserMessage, chatbot: ClaudeTextEditorChatbot = Depends(get_chatbot)):
    """Send a message to Claude and get a response."""
    try:
        response = chatbot.chat(message.content)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

@app.post("/api/file/operation", response_model=FileOperationResponse)
async def file_operation(operation: FileOperation, chatbot: ClaudeTextEditorChatbot = Depends(get_chatbot)):
    """Perform a file operation using the text editor tool."""
    try:
        # Convert the operation to a tool use format Claude would use
        tool_use = {
            "id": "api_tool_use",
            "name": "str_replace_editor",
            "input": {
                "command": operation.command,
                "path": operation.path,
                **operation.parameters
            }
        }
        
        # Handle the tool use directly
        result = chatbot.handle_tool_use(tool_use)
        
        # Return the result
        return FileOperationResponse(
            success=not result.get("is_error", False),
            message=result.get("content", ""),
            error=result.get("is_error", False)
        )
    except Exception as e:
        logger.error(f"Error in file operation endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file operation: {str(e)}"
        )

@app.get("/api/files", response_model=ListFilesResponse)
async def list_files(path: str = ""):
    """List files in the workspace directory."""
    try:
        import os
        from src.utils.file_utils import validate_path, list_directory_contents
        
        # Validate the path
        target_path = os.path.join(WORKSPACE_DIR, path) if path else WORKSPACE_DIR
        is_valid, abs_path, error = validate_path(target_path)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error or "Invalid path"
            )
            
        if not os.path.isdir(abs_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Path is not a directory: {path}"
            )
            
        # List the contents
        contents = list_directory_contents(abs_path)
        
        # Parse the contents into files and directories
        files = []
        directories = []
        
        for item in contents:
            if item.startswith("[DIR]"):
                directories.append(item[6:].strip())
            elif item.startswith("[FILE]"):
                files.append(item[7:].strip())
                
        return ListFilesResponse(
            path=path,
            files=files,
            directories=directories
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing files: {str(e)}"
        )

@app.post("/api/reset")
async def reset_conversation(background_tasks: BackgroundTasks):
    """Reset the conversation with Claude."""
    # We'll recreate the chatbot in the background
    background_tasks.add_task(ClaudeTextEditorChatbot)
    return {"status": "success", "message": "Conversation reset"}

# ----------------------------------------------------------------------
# Sample file creation endpoint (for demonstration)
# ----------------------------------------------------------------------

@app.post("/api/sample", response_model=FileOperationResponse)
async def create_sample_file():
    """Create a sample Python file in the workspace for demonstration."""
    import os
    from src.utils.file_utils import create_new_file
    
    sample_path = os.path.join(WORKSPACE_DIR, "sample.py")
    sample_content = '''def calculate_factorial(n):
    """Calculate the factorial of a number."""
    if n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial(n - 1)

def main():
    print("Factorial of 5:", calculate_factorial(5))
    
if __name__ == "__main__":
    main()
'''
    
    success, message = create_new_file(sample_path, sample_content)
    
    return FileOperationResponse(
        success=success,
        message=message,
        error=not success
    )

# ----------------------------------------------------------------------
# Main function for running the application
# ----------------------------------------------------------------------

def main():
    """Main function to run the FastAPI application with Uvicorn."""
    # Create workspace directory if it doesn't exist
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)
        print(f"Created workspace directory: {WORKSPACE_DIR}")
        
    # Create .backups directory if it doesn't exist
    backups_dir = os.path.join(WORKSPACE_DIR, ".backups")
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)
        print(f"Created backups directory: {backups_dir}")
    
    # Run the application with Uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

# ----------------------------------------------------------------------
# Script Execution
# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
