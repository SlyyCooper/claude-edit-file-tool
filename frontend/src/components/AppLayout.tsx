/**
 * src/components/AppLayout.tsx
 * Main application layout combining chat and file explorer components
 * Used by: src/app/page.tsx
 * Dependencies: ChatContainer, FileExplorer
 */

"use client"

import React, { useState } from 'react';
import ChatContainer from './ChatContainer';
import FileExplorer from './FileExplorer';

// ===== COMPONENT =====
export default function AppLayout() {
  const [activeTab, setActiveTab] = useState<'chat' | 'files'>('chat');

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b shadow-sm px-6 py-4 sticky top-0 z-10">
        <div className="flex justify-between items-center max-w-7xl mx-auto">
          <h1 className="text-2xl font-semibold text-[#d9b5a7]">Claude Text Editor</h1>
          
          {/* Tabs */}
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-5 py-2 rounded-md font-medium transition-colors ${
                activeTab === 'chat'
                  ? 'bg-[#f9f3f0] text-[#d9b5a7] shadow-sm'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Chat
            </button>
            <button
              onClick={() => setActiveTab('files')}
              className={`px-5 py-2 rounded-md font-medium transition-colors ${
                activeTab === 'files'
                  ? 'bg-[#f9f3f0] text-[#d9b5a7] shadow-sm'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Files
            </button>
          </div>
        </div>
      </header>
      
      {/* Content */}
      <main className="flex-1 overflow-hidden max-w-7xl w-full mx-auto my-4">
        <div className="h-full bg-white rounded-lg shadow-sm overflow-hidden">
          {activeTab === 'chat' ? (
            <ChatContainer />
          ) : (
            <div className="p-4 h-full">
              <FileExplorer />
            </div>
          )}
        </div>
      </main>
    </div>
  );
} 