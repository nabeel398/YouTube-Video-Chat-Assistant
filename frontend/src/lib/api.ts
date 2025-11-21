const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export class ApiError extends Error {
  constructor(public detail: string, public status?: number) {
    super(detail);
    this.name = 'ApiError';
  }
}

export const api = {
  async processVideo(url: string, sessionId: string = 'default') {
    const response = await fetch(`${API_BASE_URL}/video/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new ApiError(errorData.detail || 'Failed to process video', response.status);
    }

    return response.json();
  },

  async sendChatMessage(query: string, sessionId: string = 'default') {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new ApiError(errorData.detail || 'Failed to send message', response.status);
    }

    return response.json();
  },

  async exportChatToPDF(chatHistory: any[]) {
    const response = await fetch(`${API_BASE_URL}/export/export-pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(chatHistory),
    });

    if (!response.ok) {
      throw new ApiError('Failed to export PDF');
    }

    return response;
  },

  async getUsageStats() {
    const response = await fetch(`${API_BASE_URL}/chat/usage`);
    if (!response.ok) {
      throw new ApiError('Failed to get usage stats');
    }
    return response.json();
  },
};