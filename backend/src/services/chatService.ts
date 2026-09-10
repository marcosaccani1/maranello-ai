import type {
  OrchestrationResult,
} from "../ai/aiOrchestrator.js";
import {
  AIOrchestrator,
} from "../ai/aiOrchestrator.js";

import type {
  ConversationSession,
} from "../conversation/types.js";
import {
  ConversationManager,
} from "../conversation/conversationManager.js";

import type {
  ChatResult,
} from "../models/chat.js";


interface ConversationProvider {
  getOrCreateSession(
    sessionId?: string,
  ): ConversationSession;

  addMessage(
    sessionId: string,
    role: "user" | "assistant",
    content: string,
  ): ConversationSession;

  setPreviousResponseId(
    sessionId: string,
    responseId: string,
  ): ConversationSession;
}


interface OrchestratorProvider {
  run(
    question: string,
    previousResponseId?: string,
  ): Promise<OrchestrationResult>;
}


export class ChatService {
  constructor(
    private readonly conversationManager:
    ConversationProvider =
      new ConversationManager(),

    private readonly orchestrator:
    OrchestratorProvider =
      new AIOrchestrator(),
  ) {}


  async sendMessage(
    message: string,
    sessionId?: string,
  ): Promise<ChatResult> {
    const normalizedMessage =
      message.trim();

    if (!normalizedMessage) {
      throw new Error(
        "Chat message must be a non-empty string.",
      );
    }

    const normalizedSessionId =
      sessionId?.trim();

    if (
      sessionId !== undefined
      && !normalizedSessionId
    ) {
      throw new Error(
        "Session ID must be a non-empty string when provided.",
      );
    }

    const session =
      this.conversationManager
        .getOrCreateSession(
          normalizedSessionId,
        );

    const result =
      await this.orchestrator.run(
        normalizedMessage,
        session.previousResponseId
          ?? undefined,
      );

    this.conversationManager
      .addMessage(
        session.id,
        "user",
        normalizedMessage,
      );

    this.conversationManager
      .addMessage(
        session.id,
        "assistant",
        result.answer,
      );

    this.conversationManager
      .setPreviousResponseId(
        session.id,
        result.responseId,
      );

    return {
      sessionId:
        session.id,

      responseId:
        result.responseId,

      answer:
        result.answer,

      toolsUsed: [
        ...result.toolsUsed,
      ],
    };
  }
}