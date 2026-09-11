export type ChatRole =
  | "user"
  | "assistant";


export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  chartUrl?: string;
}


export interface ChatApiRequest {
  message: string;
  sessionId?: string;
}


export interface ChatApiResponse {
  sessionId: string;
  responseId: string;
  answer: string;
  toolsUsed: string[];
  chartUrl?: string;
}