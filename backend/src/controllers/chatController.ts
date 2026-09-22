import type {
  NextFunction,
  Request,
  Response,
} from "express";

import {
  setChatObservabilityMetadata,
} from "../middleware/chatObservability.js";

import type {
  ChatExecutionResult,
  ChatRequest,
} from "../models/chat.js";


export interface ChatServiceProvider {
  sendMessage(
    message: string,
    sessionId?: string,
  ): Promise<ChatExecutionResult>;
}


function isDataAgentUnavailableError(
  error: unknown,
): boolean {
  return (
    error instanceof Error
    && error.message ===
      "Unable to connect to the Data Agent."
  );
}


function isKnowledgeBaseUnavailableError(
  error: unknown,
): boolean {
  if (!(error instanceof Error)) {
    return false;
  }

  return (
    error.name ===
      "ChromaConnectionError"
    || error.message.includes(
      "Failed to connect to chromadb",
    )
  );
}


export function createChatController(
  chatService: ChatServiceProvider,
) {
  return async function chatController(
    request: Request,
    response: Response,
    next: NextFunction,
  ): Promise<void> {
    try {
      const body =
        request.body as Partial<ChatRequest>;

      if (
        typeof body.message !== "string"
      ) {
        response.status(400).json({
          error:
            "Request body must contain a message string.",
        });

        return;
      }

      if (
        body.sessionId !== undefined
        && typeof body.sessionId !== "string"
      ) {
        response.status(400).json({
          error:
            "Session ID must be a string when provided.",
        });

        return;
      }

      const execution =
        await chatService.sendMessage(
          body.message,
          body.sessionId,
        );

      setChatObservabilityMetadata(
        response,
        {
          toolsUsed:
            execution.result.toolsUsed,

          tokenUsage:
            execution.tokenUsage,
        },
      );

      response.status(200).json(
        execution.result,
      );
    } catch (error) {
      if (
        error instanceof Error
        && (
          error.message ===
            "Chat message must be a non-empty string."
          || error.message ===
            "Session ID must be a non-empty string when provided."
        )
      ) {
        response.status(400).json({
          error:
            error.message,
        });

        return;
      }

      if (
        isDataAgentUnavailableError(
          error,
        )
      ) {
        response.status(503).json({
          error:
            "Manufacturing data analysis is temporarily unavailable. Please try again later.",
        });

        return;
      }

      if (
        isKnowledgeBaseUnavailableError(
          error,
        )
      ) {
        response.status(503).json({
          error:
            "The company knowledge base is temporarily unavailable. Please try again later.",
        });

        return;
      }

      next(error);
    }
  };
}