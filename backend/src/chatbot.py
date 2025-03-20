"""
Main ChatBot implementation with Claude text editor tool integration.
"""

import json
import os
from typing import Dict, List, Optional, Any, Union, Tuple

import anthropic
from anthropic import Anthropic

from src.config.settings import (
    ANTHROPIC_API_KEY,
    MODEL_NAME,
    MAX_TOKENS,
    TEXT_EDITOR_TOOL_DEFINITION
)
from src.tools.text_editor import TextEditorTool

# ----------------------------------------------------------------------
# --- Class Definition -------------------------------------------------
# ----------------------------------------------------------------------


class ClaudeTextEditorChatbot:
    """
    A chatbot implementation that integrates Claude with text editor tool capabilities.
    """

    # ------------------------------------------------------------------
    # --- Initialization -----------------------------------------------
    # ------------------------------------------------------------------
    
    def __init__(self):
        """Initialize the chatbot with Claude client and conversation history."""
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.conversation: List[Dict[str, Any]] = []
        self.tools = [TEXT_EDITOR_TOOL_DEFINITION]

    # ------------------------------------------------------------------
    # --- Conversation Management Methods --------------------------------
    # ------------------------------------------------------------------
        
    def add_user_message(self, message: str) -> None:
        """
        Add a user message to the conversation history.
        
        Args:
            message: The user's message text
        """
        self.conversation.append({
            "role": "user",
            "content": message
        })
        
    def add_assistant_message(self, content: List[Dict[str, Any]]) -> None:
        """
        Add an assistant message to the conversation history.
        
        Args:
            content: The assistant's message content (list of content blocks)
        """
        self.conversation.append({
            "role": "assistant",
            "content": content
        })
        
    def add_tool_result(self, tool_use_id: str, content: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation history.
        
        Args:
            tool_use_id: The ID of the tool use request this is a result for
            content: The result content
            is_error: Whether the tool execution resulted in an error
        """
        self.conversation.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": content,
                "is_error": is_error
            }]
        })

    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.conversation = []

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history."""
        return self.conversation.copy()

    # ------------------------------------------------------------------
    # --- Claude Interaction Methods -------------------------------------
    # ------------------------------------------------------------------
        
    def get_assistant_response(self):
        """
        Get a response from Claude based on the current conversation.
        
        Returns:
            The response from Claude
        """
        try:
            response = self.client.messages.create(
                model=MODEL_NAME,
                messages=self.conversation,
                tools=self.tools,
                max_tokens=MAX_TOKENS
            )
            return response
        except Exception as e:
            print(f"Error getting response from Claude: {str(e)}")
            # Create a minimal object to represent an error
            class ErrorResponse:
                def __init__(self, error_message):
                    self.content = [{"type": "text", "text": f"Error: {error_message}"}]
                    self.stop_reason = "error"
            
            return ErrorResponse(str(e))

    async def get_assistant_response_async(self):
        """
        Get a response from Claude asynchronously.
        
        Returns:
            The response from Claude
        """
        try:
            from anthropic import AsyncAnthropic
            
            async_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
            response = await async_client.messages.create(
                model=MODEL_NAME,
                messages=self.conversation,
                tools=self.tools,
                max_tokens=MAX_TOKENS
            )
            return response
        except Exception as e:
            print(f"Error getting async response from Claude: {str(e)}")
            # Create a minimal object to represent an error
            class ErrorResponse:
                def __init__(self, error_message):
                    self.content = [{"type": "text", "text": f"Error: {error_message}"}]
                    self.stop_reason = "error"
            
            return ErrorResponse(str(e))

    # ------------------------------------------------------------------
    # --- Tool Handling Methods ------------------------------------------
    # ------------------------------------------------------------------
            
    def handle_tool_use(self, tool_use) -> Dict[str, Any]:
        """
        Handle a tool use request from Claude.
        
        Args:
            tool_use: The tool use request object
            
        Returns:
            The tool result
        """
        # Handle both dict-like and object-like access
        tool_name = getattr(tool_use, "name", None)
        if tool_name is None and isinstance(tool_use, dict):
            tool_name = tool_use.get("name", "")
        
        if tool_name == "str_replace_editor":
            return TextEditorTool.handle_tool_use(tool_use)
        else:
            tool_id = getattr(tool_use, "id", None)
            if tool_id is None and isinstance(tool_use, dict):
                tool_id = tool_use.get("id", "")
                
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": f"Error: Unknown tool '{tool_name}'",
                "is_error": True
            }

    # ------------------------------------------------------------------
    # --- Response Processing Methods ------------------------------------
    # ------------------------------------------------------------------
            
    def process_response(self, response):
        """
        Process a response from Claude, handling tool use if necessary.
        
        Args:
            response: The response object from Claude
            
        Returns:
            The final response after handling any tool use
        """
        # Add the response to the conversation history - handle object attributes
        content = getattr(response, "content", None)
        if content is None and isinstance(response, dict):
            content = response.get("content", [])
            
        self.add_assistant_message(content)
        
        # Check if Claude wants to use a tool
        stop_reason = getattr(response, "stop_reason", None)
        if stop_reason is None and isinstance(response, dict):
            stop_reason = response.get("stop_reason", "")
            
        if stop_reason == "tool_use":
            for content_block in content:
                # Handle both dict-like and object-like access for content blocks
                block_type = None
                if isinstance(content_block, dict):
                    block_type = content_block.get("type", "")
                else:
                    block_type = getattr(content_block, "type", "")
                    
                if block_type == "tool_use":
                    # Handle the tool use and get the result
                    tool_result = self.handle_tool_use(content_block)
                    
                    # Add the tool result to the conversation
                    self.add_tool_result(
                        tool_result["tool_use_id"],
                        tool_result["content"],
                        tool_result.get("is_error", False)
                    )
                    
                    # Get a new response from Claude with the tool result
                    return self.get_assistant_response()
                    
        return response

    async def process_response_async(self, response):
        """
        Process a response from Claude asynchronously, handling tool use if necessary.
        
        Args:
            response: The response object from Claude
            
        Returns:
            The final response after handling any tool use
        """
        # Add the response to the conversation history - handle object attributes
        content = getattr(response, "content", None)
        if content is None and isinstance(response, dict):
            content = response.get("content", [])
            
        self.add_assistant_message(content)
        
        # Check if Claude wants to use a tool
        stop_reason = getattr(response, "stop_reason", None)
        if stop_reason is None and isinstance(response, dict):
            stop_reason = response.get("stop_reason", "")
            
        if stop_reason == "tool_use":
            for content_block in content:
                # Handle both dict-like and object-like access for content blocks
                block_type = None
                if isinstance(content_block, dict):
                    block_type = content_block.get("type", "")
                else:
                    block_type = getattr(content_block, "type", "")
                    
                if block_type == "tool_use":
                    # Handle the tool use and get the result
                    tool_result = self.handle_tool_use(content_block)
                    
                    # Add the tool result to the conversation
                    self.add_tool_result(
                        tool_result["tool_use_id"],
                        tool_result["content"],
                        tool_result.get("is_error", False)
                    )
                    
                    # Get a new response from Claude with the tool result
                    return await self.get_assistant_response_async()
                    
        return response

    # ------------------------------------------------------------------
    # --- Utility Methods -----------------------------------------------
    # ------------------------------------------------------------------

    def extract_text_content(self, response) -> str:
        """
        Extract text content from a Claude response.
        
        Args:
            response: The response object from Claude
            
        Returns:
            The extracted text content
        """
        response_text = ""
        content = getattr(response, "content", None)
        if content is None and isinstance(response, dict):
            content = response.get("content", [])
            
        for content_block in content:
            # Handle both dict-like and object-like access
            block_type = None
            block_text = None
            
            if isinstance(content_block, dict):
                block_type = content_block.get("type", "")
                if block_type == "text":
                    block_text = content_block.get("text", "")
            else:
                block_type = getattr(content_block, "type", "")
                if block_type == "text":
                    block_text = getattr(content_block, "text", "")
                    
            if block_text:
                response_text += block_text
                
        return response_text

    # ------------------------------------------------------------------
    # --- Main Chat Methods ---------------------------------------------
    # ------------------------------------------------------------------
        
    def chat(self, message: str) -> str:
        """
        Send a message to the chatbot and get a response.
        
        Args:
            message: The user's message
            
        Returns:
            The chatbot's response text
        """
        # Add the user message to the conversation
        self.add_user_message(message)
        
        # Get the initial response from Claude
        response = self.get_assistant_response()
        
        # Process the response, handling any tool use
        final_response = self.process_response(response)
        
        # Extract the text content from the response
        return self.extract_text_content(final_response)

    async def chat_async(self, message: str) -> str:
        """
        Send a message to the chatbot asynchronously and get a response.
        
        Args:
            message: The user's message
            
        Returns:
            The chatbot's response text
        """
        # Add the user message to the conversation
        self.add_user_message(message)
        
        # Get the initial response from Claude
        response = await self.get_assistant_response_async()
        
        # Process the response, handling any tool use
        final_response = await self.process_response_async(response)
        
        # Extract the text content from the response
        return self.extract_text_content(final_response)

    def chat_with_tool_use(self, message: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Send a message to the chatbot and get a response along with any tools used.
        
        Args:
            message: The user's message
            
        Returns:
            A tuple of (response_text, tool_uses)
        """
        # Add the user message to the conversation
        self.add_user_message(message)
        
        # Save conversation length before chat to track new messages
        prev_conversation_length = len(self.conversation)
        
        # Get the initial response from Claude
        response = self.get_assistant_response()
        
        # Process the response, handling any tool use
        final_response = self.process_response(response)
        
        # Extract the text content from the response
        response_text = self.extract_text_content(final_response)
        
        # Extract tool uses from conversation history
        tool_uses = []
        for message in self.conversation[prev_conversation_length:]:
            if message["role"] == "assistant":
                for content_block in message["content"]:
                    if isinstance(content_block, dict) and content_block.get("type") == "tool_use":
                        tool_uses.append(content_block)
                        
        return response_text, tool_uses
