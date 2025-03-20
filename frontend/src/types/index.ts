/**
 * src/types/index.ts
 * Application-specific type definitions
 * Contains shared types used across the application
 */

// Message types for the chat interface
export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

// Chat state
export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

// File system types
export interface FileSystem {
  currentPath: string;
  files: string[];
  directories: string[];
  isLoading: boolean;
  error: string | null;
}

// File operation parameters
export interface ViewFileParams {
  content?: string;
}

export interface StrReplaceParams {
  old_content: string;
  new_content: string;
  start_line?: number; 
  end_line?: number;
}

export interface CreateFileParams {
  content: string;
}

export interface InsertParams {
  content: string;
  line?: number;
}

// Using Record<never, never> for an empty object type
export type UndoEditParams = Record<string, never>;

// Union type for all file operation parameters
export type FileOperationParams = 
  | ViewFileParams
  | StrReplaceParams
  | CreateFileParams
  | InsertParams
  | UndoEditParams
  | Record<string, unknown>; // Allow for flexible parameters with safer unknown type 