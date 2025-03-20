/**
 * src/components/FileExplorer.tsx
 * File explorer component for browsing and interacting with files
 * Used by: src/components/AppLayout.tsx
 * Dependencies: FileContext from src/context/FileContext.tsx
 */

"use client"

import React, { useState } from 'react';
import { useFiles } from '../context/FileContext';

// ===== COMPONENT =====
export default function FileExplorer() {
  const { fileSystem, refreshFiles, viewFile, setCurrentPath } = useFiles();
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Navigate to a directory
  const handleNavigateToDirectory = (directory: string) => {
    const newPath = fileSystem.currentPath 
      ? `${fileSystem.currentPath}/${directory}` 
      : directory;
    setCurrentPath(newPath);
    setSelectedFile(null);
    setFileContent(null);
  };

  // Navigate up one directory
  const handleNavigateUp = () => {
    if (!fileSystem.currentPath) return;
    
    const pathParts = fileSystem.currentPath.split('/');
    pathParts.pop();
    const newPath = pathParts.join('/');
    setCurrentPath(newPath);
    setSelectedFile(null);
    setFileContent(null);
  };

  // View file content
  const handleViewFile = async (file: string) => {
    setIsLoading(true);
    setSelectedFile(file);
    
    try {
      const path = fileSystem.currentPath 
        ? `${fileSystem.currentPath}/${file}` 
        : file;
      
      const response = await viewFile(path);
      if (response.success && response.message) {
        setFileContent(response.message);
      } else {
        setFileContent(`Error: ${response.error ? response.message : 'Could not load file content'}`);
      }
    } catch (error) {
      setFileContent(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Refresh the current directory
  const handleRefresh = () => {
    refreshFiles(fileSystem.currentPath);
    if (selectedFile && fileSystem.currentPath) {
      handleViewFile(selectedFile);
    }
  };

  // Get breadcrumb segments for navigation
  const getBreadcrumbs = () => {
    if (!fileSystem.currentPath) return [{ label: 'Root', path: '' }];
    
    const segments = fileSystem.currentPath.split('/');
    return [
      { label: 'Root', path: '' },
      ...segments.map((segment, index) => ({
        label: segment,
        path: segments.slice(0, index + 1).join('/')
      }))
    ];
  };

  const breadcrumbs = getBreadcrumbs();

  return (
    <div className="h-full flex flex-col border rounded-lg overflow-hidden bg-white shadow-sm">
      {/* Toolbar */}
      <div className="bg-gray-50 px-4 py-3 border-b flex items-center justify-between">
        <div className="flex items-center space-x-2 overflow-x-auto">
          {breadcrumbs.map((crumb, index) => (
            <React.Fragment key={crumb.path}>
              {index > 0 && (
                <span className="text-gray-400">/</span>
              )}
              <button
                onClick={() => setCurrentPath(crumb.path)}
                className="px-2 py-1 hover:bg-gray-200 rounded text-sm text-gray-700 whitespace-nowrap"
              >
                {crumb.label}
              </button>
            </React.Fragment>
          ))}
        </div>
        <div className="flex space-x-2">
          <button 
            onClick={handleNavigateUp}
            disabled={!fileSystem.currentPath}
            className="p-1.5 rounded hover:bg-gray-200 disabled:opacity-50 text-gray-600"
            aria-label="Navigate up"
            title="Navigate up"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
              <path fillRule="evenodd" d="M9.293 2.293a1 1 0 0 1 1.414 0l7 7A1 1 0 0 1 17 11h-3v6a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-6H3a1 1 0 0 1-.707-1.707l7-7Z" clipRule="evenodd" />
            </svg>
          </button>
          <button 
            onClick={handleRefresh}
            className="p-1.5 rounded hover:bg-gray-200 text-gray-600"
            aria-label="Refresh"
            title="Refresh"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
              <path fillRule="evenodd" d="M15.312 11.424a5.5 5.5 0 0 1-9.201 2.466l-.312-.311h2.433a.75.75 0 0 0 0-1.5H3.989a.75.75 0 0 0-.75.75v4.242a.75.75 0 0 0 1.5 0v-2.43l.31.31a7 7 0 0 0 11.712-3.138.75.75 0 0 0-1.449-.39Zm1.23-3.723a.75.75 0 0 0 .219-.53V2.929a.75.75 0 0 0-1.5 0V5.36l-.31-.31A7 7 0 0 0 3.239 8.188a.75.75 0 1 0 1.448.389A5.5 5.5 0 0 1 13.89 6.11l.311.31h-2.432a.75.75 0 0 0 0 1.5h4.243a.75.75 0 0 0 .53-.219Z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
      
      {/* Content area */}
      {fileSystem.isLoading ? (
        <div className="flex-1 flex items-center justify-center p-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#d9b5a7]"></div>
        </div>
      ) : fileSystem.error ? (
        <div className="flex-1 p-4 text-red-500 flex items-center justify-center">
          <div className="bg-red-50 p-4 rounded-lg border border-red-200 max-w-md">
            <div className="font-semibold mb-2">Error</div>
            <div>{fileSystem.error}</div>
          </div>
        </div>
      ) : (
        <div className="flex flex-1 overflow-hidden">
          {/* File/directory list */}
          <div className="w-1/3 overflow-y-auto border-r">
            {fileSystem.directories.length === 0 && fileSystem.files.length === 0 ? (
              <div className="p-8 text-gray-500 text-center">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-10 h-10 mx-auto mb-2 text-gray-300">
                  <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0016.5 9h-1.875a1.875 1.875 0 01-1.875-1.875V5.25A3.75 3.75 0 009 1.5H5.625z" />
                  <path d="M12.971 1.816A5.23 5.23 0 0114.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 013.434 1.279 9.768 9.768 0 00-6.963-6.963z" />
                </svg>
                <div>No files or directories</div>
              </div>
            ) : (
              <ul className="divide-y">
                {fileSystem.directories.map((dir) => (
                  <li key={dir} className="hover:bg-gray-50">
                    <button
                      onClick={() => handleNavigateToDirectory(dir)}
                      className="w-full text-left px-4 py-3 flex items-center transition-colors hover:text-[#d9b5a7]"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 mr-3 text-yellow-500 flex-shrink-0">
                        <path fillRule="evenodd" d="M2 4.75C2 3.784 2.784 3 3.75 3h4.836c.464 0 .909.184 1.237.513l1.414 1.414a.25.25 0 0 0 .177.073h4.836c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 16.25 17H3.75A1.75 1.75 0 0 1 2 15.25V4.75Z" clipRule="evenodd" />
                      </svg>
                      <span className="truncate">{dir}</span>
                    </button>
                  </li>
                ))}
                {fileSystem.files.map((file) => (
                  <li key={file} className={`hover:bg-gray-50 ${file === selectedFile ? 'bg-blue-50' : ''}`}>
                    <button
                      onClick={() => handleViewFile(file)}
                      className={`w-full text-left px-4 py-3 flex items-center transition-colors ${
                        file === selectedFile ? 'text-blue-600 font-medium' : 'hover:text-[#d9b5a7]'
                      }`}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 mr-3 text-blue-500 flex-shrink-0">
                        <path fillRule="evenodd" d="M4.5 2A1.5 1.5 0 0 0 3 3.5v13A1.5 1.5 0 0 0 4.5 18h11a1.5 1.5 0 0 0 1.5-1.5V7.621a1.5 1.5 0 0 0-.44-1.06l-4.12-4.122A1.5 1.5 0 0 0 11.378 2H4.5Zm2.25 8.5a.75.75 0 0 0 0 1.5h6.5a.75.75 0 0 0 0-1.5h-6.5Zm0 3a.75.75 0 0 0 0 1.5h6.5a.75.75 0 0 0 0-1.5h-6.5Z" clipRule="evenodd" />
                      </svg>
                      <span className="truncate">{file}</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
          
          {/* File content */}
          <div className="w-2/3 overflow-y-auto bg-gray-50 flex flex-col">
            {isLoading ? (
              <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#d9b5a7]"></div>
              </div>
            ) : selectedFile ? (
              <div className="flex-1 p-4 flex flex-col h-full">
                <div className="bg-gray-100 rounded-t-lg px-4 py-2 border border-gray-200 border-b-0 flex justify-between items-center">
                  <h3 className="font-medium">{selectedFile}</h3>
                </div>
                <pre className="flex-1 whitespace-pre-wrap font-mono text-sm bg-white p-4 rounded-b-lg border border-gray-200 overflow-auto h-full">
                  {fileContent}
                </pre>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-gray-400 p-8">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-16 h-16 mb-4 text-gray-300">
                  <path fillRule="evenodd" d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0016.5 9h-1.875a1.875 1.875 0 01-1.875-1.875V5.25A3.75 3.75 0 009 1.5H5.625zM7.5 15a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5A.75.75 0 017.5 15zm.75 2.25a.75.75 0 000 1.5H12a.75.75 0 000-1.5H8.25z" />
                  <path d="M12.971 1.816A5.23 5.23 0 0114.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 013.434 1.279 9.768 9.768 0 00-6.963-6.963z" />
                </svg>
                <p className="text-lg font-medium mb-2">No file selected</p>
                <p className="text-center">Select a file from the list to view its contents</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 