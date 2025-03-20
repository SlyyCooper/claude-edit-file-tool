/**
 * src/services/api.ts
 * API service for interacting with the Claude Text Editor API
 * This file provides functions to communicate with the backend API endpoints
 */

import { components } from "../types/api";

const API_BASE_URL = "http://localhost:8000";

// Types based on the OpenAPI schema
export type UserMessage = components["schemas"]["UserMessage"];
export type ChatResponse = components["schemas"]["ChatResponse"];
export type FileOperation = {
  command: string;
  path: string;
  parameters?: Record<string, unknown>;
};
export type FileOperationResponse = components["schemas"]["FileOperationResponse"];
export type ListFilesResponse = components["schemas"]["ListFilesResponse"];

// API client functions
async function fetchWithErrorHandling<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "An unknown error occurred");
    }
    
    return await response.json() as T;
  } catch (error) {
    console.error("API request failed:", error);
    throw error;
  }
}

/**
 * Send a message to Claude and get a response
 */
export async function sendChatMessage(content: string): Promise<ChatResponse> {
  return fetchWithErrorHandling<ChatResponse>(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content,
    }),
  });
}

/**
 * Reset the conversation with Claude
 */
export async function resetConversation(): Promise<string> {
  return fetchWithErrorHandling<string>(`${API_BASE_URL}/api/reset`, {
    method: "POST",
  });
}

/**
 * List files in the workspace directory
 */
export async function listFiles(path: string = ""): Promise<ListFilesResponse> {
  const url = new URL(`${API_BASE_URL}/api/files`);
  if (path) {
    url.searchParams.append("path", path);
  }
  
  return fetchWithErrorHandling<ListFilesResponse>(url.toString());
}

/**
 * Perform a file operation using the text editor tool
 */
export async function fileOperation(
  operation: FileOperation
): Promise<FileOperationResponse> {
  return fetchWithErrorHandling<FileOperationResponse>(
    `${API_BASE_URL}/api/file/operation`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(operation),
    }
  );
}

/**
 * Create a sample Python file in the workspace
 */
export async function createSampleFile(): Promise<FileOperationResponse> {
  return fetchWithErrorHandling<FileOperationResponse>(
    `${API_BASE_URL}/api/sample`,
    {
      method: "POST",
    }
  );
} 