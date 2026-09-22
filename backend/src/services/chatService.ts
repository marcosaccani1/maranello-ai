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
  ChatExecutionResult,
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


function toPublicChartUrl(
  chartUrl?: string,
): string | undefined {
  if (!chartUrl) {
    return undefined;
  }

  const normalizedChartUrl =
    chartUrl.trim();

  if (!normalizedChartUrl) {
    return undefined;
  }

  const chartPrefix =
    "/charts/";

  if (
    !normalizedChartUrl.startsWith(
      chartPrefix,
    )
  ) {
    return normalizedChartUrl;
  }

  const filename =
    normalizedChartUrl.slice(
      chartPrefix.length,
    );

  if (!filename) {
    return undefined;
  }

  return `/api/charts/${filename}`;
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
  ): Promise<ChatExecutionResult> {
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

    const orchestrationResult =
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
        orchestrationResult.answer,
      );

    this.conversationManager
      .setPreviousResponseId(
        session.id,
        orchestrationResult.responseId,
      );

    const chartUrl =
      toPublicChartUrl(
        orchestrationResult.chartUrl,
      );

    return {
      result: {
        sessionId:
          session.id,

        responseId:
          orchestrationResult.responseId,

        answer:
          orchestrationResult.answer,

        toolsUsed: [
          ...orchestrationResult.toolsUsed,
        ],

        ...(chartUrl
          ? {
              chartUrl,
            }
          : {}),
      },

      tokenUsage: {
        ...orchestrationResult.tokenUsage,
      },
    };
  }
}