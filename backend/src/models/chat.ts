export interface ChatRequest {
  message: string;
  sessionId?: string;
}


export interface ChatResult {
  sessionId: string;
  responseId: string;
  answer: string;
  toolsUsed: string[];
  chartUrl?: string;
}