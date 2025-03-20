/**
 * src/context/FileContext.tsx
 * File system context for managing state of the file operations
 * Provides file operations functionality to all components in the application
 */

"use client"

import { createContext, useState, useContext, ReactNode, useEffect, useCallback } from 'react';
import { FileSystem } from '../types';
import { listFiles, fileOperation } from '../services/api';
import { FileOperationResponse } from '../services/api';

// Default state for the file system
const defaultFileSystemState: FileSystem = {
  currentPath: '',
  files: [],
  directories: [],
  isLoading: false,
  error: null,
};

// Context interface
interface FileContextProps {
  fileSystem: FileSystem;
  refreshFiles: (path?: string) => Promise<void>;
  viewFile: (path: string) => Promise<FileOperationResponse>;
  createFile: (path: string, content: string) => Promise<FileOperationResponse>;
  editFile: (path: string, oldContent: string, newContent: string) => Promise<FileOperationResponse>;
  insertToFile: (path: string, content: string, line?: number) => Promise<FileOperationResponse>;
  undoEdit: (path: string) => Promise<FileOperationResponse>;
  setCurrentPath: (path: string) => void;
  clearError: () => void;
}

// Create the context
const FileContext = createContext<FileContextProps | undefined>(undefined);

// Context provider component
export function FileProvider({ children }: { children: ReactNode }) {
  const [fileSystem, setFileSystem] = useState<FileSystem>(defaultFileSystemState);

  // Refresh the file list - memoized with useCallback to avoid dependency issues
  const refreshFiles = useCallback(async (path: string = '') => {
    setFileSystem((prev) => ({
      ...prev,
      isLoading: true,
      error: null,
    }));

    try {
      const response = await listFiles(path);
      
      setFileSystem({
        currentPath: response.path,
        files: response.files || [],
        directories: response.directories || [],
        isLoading: false,
        error: null,
      });
    } catch (error) {
      setFileSystem((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to load files',
      }));
    }
  }, []);

  // Load initial file list
  useEffect(() => {
    refreshFiles(fileSystem.currentPath);
  }, [refreshFiles, fileSystem.currentPath]);

  // View file content
  const viewFile = async (path: string): Promise<FileOperationResponse> => {
    try {
      return await fileOperation({
        command: 'view',
        path,
        parameters: {},
      });
    } catch (error) {
      setFileSystem((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to view file',
      }));
      throw error;
    }
  };

  // Create a new file
  const createFile = async (path: string, content: string): Promise<FileOperationResponse> => {
    try {
      const result = await fileOperation({
        command: 'create',
        path,
        parameters: { content } as Record<string, unknown>,
      });
      
      if (result.success) {
        await refreshFiles(fileSystem.currentPath);
      }
      
      return result;
    } catch (error) {
      setFileSystem((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to create file',
      }));
      throw error;
    }
  };

  // Edit file content
  const editFile = async (
    path: string,
    oldContent: string,
    newContent: string
  ): Promise<FileOperationResponse> => {
    try {
      return await fileOperation({
        command: 'str_replace',
        path,
        parameters: {
          old_content: oldContent,
          new_content: newContent,
        } as Record<string, unknown>,
      });
    } catch (error) {
      setFileSystem((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to edit file',
      }));
      throw error;
    }
  };

  // Insert content into a file
  const insertToFile = async (
    path: string,
    content: string,
    line?: number
  ): Promise<FileOperationResponse> => {
    try {
      return await fileOperation({
        command: 'insert',
        path,
        parameters: {
          content,
          line,
        } as Record<string, unknown>,
      });
    } catch (error) {
      setFileSystem((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to insert into file',
      }));
      throw error;
    }
  };

  // Undo last edit
  const undoEdit = async (path: string): Promise<FileOperationResponse> => {
    try {
      return await fileOperation({
        command: 'undo_edit',
        path,
        parameters: {},
      });
    } catch (error) {
      setFileSystem((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to undo edit',
      }));
      throw error;
    }
  };

  // Set current path
  const setCurrentPath = useCallback((path: string) => {
    setFileSystem((prev) => ({
      ...prev,
      currentPath: path,
    }));
    refreshFiles(path);
  }, [refreshFiles]);

  // Clear any errors
  const clearError = () => {
    setFileSystem((prev) => ({
      ...prev,
      error: null,
    }));
  };

  return (
    <FileContext.Provider
      value={{
        fileSystem,
        refreshFiles,
        viewFile,
        createFile,
        editFile,
        insertToFile,
        undoEdit,
        setCurrentPath,
        clearError,
      }}
    >
      {children}
    </FileContext.Provider>
  );
}

// Custom hook to use the file context
export function useFiles() {
  const context = useContext(FileContext);
  if (context === undefined) {
    throw new Error('useFiles must be used within a FileProvider');
  }
  return context;
} 