/**
 * src/components/ChatInput.tsx
 * Provides the chat input field component with send button
 * Used by: src/components/ChatContainer.tsx
 */

"use client"

import React, { useState, useRef, useEffect } from 'react';

// ===== TYPES =====
interface ChatInputProps {
  onSend: (message: string) => void;
  placeholder?: string;
}

// ===== COMPONENT =====
export default function ChatInput({ onSend, placeholder = 'Type your message here...' }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);
  
  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSend(message);
      setMessage('');
    }
  };
  
  // Auto-resize textarea
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const target = e.target;
    setMessage(target.value);
    
    // Reset height to auto to get the correct scrollHeight
    target.style.height = 'auto';
    
    // Set the height to the scrollHeight to expand the textarea
    target.style.height = `${Math.min(target.scrollHeight, 200)}px`;
  };

  // Handle key press
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <textarea
          ref={inputRef}
          value={message}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="w-full resize-none min-h-[52px] max-h-[200px] py-3 px-4 pr-14 rounded-xl border border-gray-300 shadow-sm focus:outline-none focus:border-[#d9b5a7] focus:ring-2 focus:ring-[#f9f3f0]"
          rows={1}
        />
        <button
          type="submit"
          disabled={!message.trim()}
          className="absolute right-2 bottom-2 rounded-full p-2.5 text-white bg-[#d9b5a7] hover:bg-[#c9a594] disabled:opacity-50 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#d9b5a7]"
          aria-label="Send message"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
            <path d="M3.478 2.404a.75.75 0 0 0-.926.941l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.404Z" />
          </svg>
        </button>
      </form>
      <p className="text-xs text-gray-500 mt-2 text-center">
        Press Enter to send, Shift+Enter for new line
      </p>
    </div>
  );
} 