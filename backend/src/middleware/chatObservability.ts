import {
  randomUUID,
} from "node:crypto";

import type {
  NextFunction,
  Request,
  RequestHandler,
  Response,
} from "express";

import type {
  TokenUsage,
} from "../ai/aiOrchestrator.js";


export interface ChatObservabilityMetadata {
  toolsUsed?: string[];
  tokenUsage?: TokenUsage;
}


export interface ChatObservabilityLocals {
  observability?:
    ChatObservabilityMetadata;
}


export interface StructuredChatLog {
  timestamp: string;
  event: "chat_request_completed";
  requestId: string;
  method: string;
  path: string;
  statusCode: number;
  latencyMs: number;
  toolsUsed: string[];
  tokenUsage: TokenUsage;
}


export type ChatLogWriter = (
  entry: StructuredChatLog,
) => void;


function defaultLogWriter(
  entry: StructuredChatLog,
): void {
  console.log(
    JSON.stringify(
      entry,
    ),
  );
}


export function setChatObservabilityMetadata(
  response: Response,
  metadata: ChatObservabilityMetadata,
): void {
  const locals =
    response.locals as ChatObservabilityLocals;

  locals.observability = {
    toolsUsed:
      metadata.toolsUsed
        ? [
            ...metadata.toolsUsed,
          ]
        : undefined,

    tokenUsage:
      metadata.tokenUsage
        ? {
            ...metadata.tokenUsage,
          }
        : undefined,
  };
}


export function createChatObservabilityMiddleware(
  logWriter:
    ChatLogWriter =
      defaultLogWriter,
): RequestHandler {
  return function chatObservabilityMiddleware(
    request: Request,
    response: Response,
    next: NextFunction,
  ): void {
    const requestId =
      randomUUID();

    const startedAt =
      process.hrtime.bigint();

    response.setHeader(
      "X-Request-Id",
      requestId,
    );

    response.once(
      "finish",
      () => {
        const elapsedNanoseconds =
          process.hrtime.bigint()
          - startedAt;

        const latencyMs =
          Number(
            elapsedNanoseconds,
          )
          / 1_000_000;

        const locals =
          response.locals as ChatObservabilityLocals;

        const metadata =
          locals.observability;

        const tokenUsage =
          metadata?.tokenUsage
          ?? {
            inputTokens: 0,
            outputTokens: 0,
            totalTokens: 0,
          };

        logWriter({
          timestamp:
            new Date().toISOString(),

          event:
            "chat_request_completed",

          requestId,

          method:
            request.method,

          path:
            request.originalUrl,

          statusCode:
            response.statusCode,

          latencyMs:
            Number(
              latencyMs.toFixed(3),
            ),

          toolsUsed:
            metadata?.toolsUsed
              ? [
                  ...metadata.toolsUsed,
                ]
              : [],

          tokenUsage: {
            ...tokenUsage,
          },
        });
      },
    );

    next();
  };
}