import type {
  TokenUsage,
} from "../ai/aiOrchestrator.js";


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


export interface ChatExecutionResult {
  result: ChatResult;
  tokenUsage: TokenUsage;
}