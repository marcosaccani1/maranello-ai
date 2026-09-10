export type ConversationRole =
  | "user"
  | "assistant";


export interface ConversationMessage {
  role: ConversationRole;
  content: string;
  createdAt: string;
}


export interface ConversationSession {
  id: string;
  messages: ConversationMessage[];
  previousResponseId: string | null;
  createdAt: string;
  updatedAt: string;
}