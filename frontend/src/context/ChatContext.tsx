/**
 * src/context/ChatContext.tsx
 * Chat context for managing state of the chat with Claude
 * Provides chat functionality to all components in the application
 */

"use client"

import { createContext, useState, useContext, ReactNode } from 'react';
import { v4 as uuid } from 'uuid';
import { Message, ChatState } from '../types';
import { sendChatMessage, resetConversation } from '../services/api';

// Default state for the chat
const defaultChatState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
};

// Context interface
interface ChatContextProps {
  chatState: ChatState;
  sendMessage: (content: string) => Promise<void>;
  resetChat: () => Promise<void>;
  clearError: () => void;
}

// Create the context
const ChatContext = createContext<ChatContextProps | undefined>(undefined);

// Context provider component
export function ChatProvider({ children }: { children: ReactNode }) {
  const [chatState, setChatState] = useState<ChatState>(defaultChatState);

  // Send a message to Claude
  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Add user message to the state
    const userMessage: Message = {
      id: uuid(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    setChatState((prev) => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      // Send message to API
      const response = await sendChatMessage(content);
      
      // Add Claude's response to the state
      const claudeMessage: Message = {
        id: uuid(),
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
      };

      setChatState((prev) => ({
        ...prev,
        messages: [...prev.messages, claudeMessage],
        isLoading: false,
      }));
    } catch (error) {
      setChatState((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'An unknown error occurred',
      }));
    }
  };

  // Reset the conversation
  const resetChat = async () => {
    setChatState((prev) => ({
      ...prev,
      isLoading: true,
      error: null,
    }));

    try {
      await resetConversation();
      setChatState(defaultChatState);
    } catch (error) {
      setChatState((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to reset conversation',
      }));
    }
  };

  // Clear any errors
  const clearError = () => {
    setChatState((prev) => ({
      ...prev,
      error: null,
    }));
  };

  return (
    <ChatContext.Provider
      value={{
        chatState,
        sendMessage,
        resetChat,
        clearError,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

// Custom hook to use the chat context
export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
} 