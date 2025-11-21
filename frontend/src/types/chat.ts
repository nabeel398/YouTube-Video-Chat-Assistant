export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  answer: string;
  used_llm: boolean;
  word_count: number;
  quality: string;
}

export interface VideoRequest {
  url: string;
  session_id?: string;
}

export interface VideoResponse {
  message: string;
  chunks_count: number;
  total_characters: number;
  session_id: string;
}

export interface ApiError {
  detail: string;
}