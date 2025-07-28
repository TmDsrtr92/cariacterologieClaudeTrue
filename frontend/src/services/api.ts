import type { QARequest, QAResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

class ApiError extends Error {
  public status: number;
  
  constructor(status: number, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

const handleResponse = async (response: Response) => {
  if (!response.ok) {
    let errorMessage = 'API request failed';
    try {
      const errorText = await response.text();
      errorMessage = errorText || `HTTP ${response.status}: ${response.statusText}`;
    } catch (e) {
      errorMessage = `HTTP ${response.status}: ${response.statusText}`;
    }
    console.error('API Error:', response.status, errorMessage);
    throw new ApiError(response.status, errorMessage);
  }
  return response.json();
};

export const api = {
  // Question & Answer
  askQuestion: async (request: QARequest): Promise<QAResponse> => {
    console.log('Making API request to:', `${API_BASE_URL}/api/qa`);
    console.log('Request payload:', request);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/qa`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('Network error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      throw new ApiError(0, `Network error: ${errorMessage}. Make sure the backend is running on ${API_BASE_URL}`);
    }
  },

  // Conversations
  getConversations: async () => {
    const response = await fetch(`${API_BASE_URL}/api/conversations`);
    return handleResponse(response);
  },

  getConversation: async (conversationId: string) => {
    const response = await fetch(`${API_BASE_URL}/api/conversations/${conversationId}`);
    return handleResponse(response);
  },

  deleteConversation: async (conversationId: string) => {
    const response = await fetch(`${API_BASE_URL}/api/conversations/${conversationId}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },

  // Transparency/Processing updates
  getProcessingStatus: async (messageId: string) => {
    const response = await fetch(`${API_BASE_URL}/api/processing/${messageId}`);
    return handleResponse(response);
  },

  // Health check
  healthCheck: async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return handleResponse(response);
  },
};

// WebSocket URL for real-time updates
export const getWebSocketUrl = () => {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const wsHost = import.meta.env.VITE_WS_URL || `${wsProtocol}://localhost:8001`;
  return `${wsHost}/ws`;
};

export { ApiError };