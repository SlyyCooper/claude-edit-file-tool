"""
FastAPI dependencies for the Claude Text Editor API.
"""

from functools import lru_cache
from fastapi import Depends, HTTPException, status

from src.chatbot import ClaudeTextEditorChatbot
from src.config.settings import ANTHROPIC_API_KEY

# ----------------------------------------------------------------------
# --- Chatbot Dependencies
# ----------------------------------------------------------------------

@lru_cache()
def get_chatbot():
    """
    Create and cache a ClaudeTextEditorChatbot instance.
    This function is cached to avoid creating a new instance for each request.
    """
    if not ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ANTHROPIC_API_KEY is not set in environment variables"
        )
    
    try:
        return ClaudeTextEditorChatbot()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize chatbot: {str(e)}"
        ) 