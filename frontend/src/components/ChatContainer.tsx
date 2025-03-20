/**
 * src/components/ChatContainer.tsx
 * Main container for the chat interface with messages and input field
 * Used by: src/app/page.tsx
 * Dependencies: ChatContext from src/context/ChatContext.tsx
 */

"use client"

import React, { useRef, useEffect } from 'react';
import ChatInput from './ChatInput';
import { useChat } from '../context/ChatContext';
import { Message } from '../types';

// ===== COMPONENT =====
export default function ChatContainer() {
  const { chatState, sendMessage } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatState.messages]);
  
  const formatMessageDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }).format(date);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 pt-4 pb-2">
        {chatState.messages.length === 0 ? (
          <div className="h-full flex items-center justify-center flex-col">
            <div className="w-16 h-16 mb-4 rounded-full bg-[#f9f3f0] flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-[#d9b5a7]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <p className="text-gray-500 font-medium">Ask a question to get started</p>
            <p className="text-gray-400 text-sm mt-2">Claude is ready to help with your text editing needs</p>
          </div>
        ) : (
          <div className="space-y-4 pb-2">
            {chatState.messages.map((message: Message) => (
              <div 
                key={message.id}
                className={`max-w-3xl mx-auto p-4 rounded-lg ${
                  message.role === 'user' 
                    ? 'bg-[#f9f3f0] ml-auto mr-0' 
                    : 'bg-white border border-gray-200 shadow-sm'
                }`}
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="font-semibold">
                    {message.role === 'user' ? 'You' : 'Claude'}
                  </span>
                  <span className="text-xs text-gray-500">
                    {formatMessageDate(message.timestamp)}
                  </span>
                </div>
                <p className="whitespace-pre-wrap">{message.content}</p>
              </div>
            ))}
            {chatState.isLoading && (
              <div className="max-w-3xl mx-auto p-4 rounded-lg bg-white border border-gray-200 shadow-sm">
                <div className="flex space-x-2 items-center">
                  <div className="font-semibold">Claude</div>
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 rounded-full bg-gray-300 animate-pulse"></div>
                    <div className="w-2 h-2 rounded-full bg-gray-300 animate-pulse delay-75"></div>
                    <div className="w-2 h-2 rounded-full bg-gray-300 animate-pulse delay-150"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      {/* Input Area - Fixed at bottom */}
      <div className="border-t bg-white p-4 sticky bottom-0 left-0 right-0 z-10 shadow-sm">
        <ChatInput onSend={sendMessage} />
        {chatState.error && (
          <div className="mt-2 text-red-500 text-sm text-center">
            Error: {chatState.error}
          </div>
        )}
      </div>
    </div>
  );
} 