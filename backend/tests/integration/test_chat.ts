import express from "express";

import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import type {
  StructuredChatLog,
} from "../../src/middleware/chatObservability.js";

import {
  createChatRateLimiter,
} from "../../src/middleware/chatRateLimiter.js";

import {
  createChatRouter,
} from "../../src/routes/chatRoutes.js";


function createTokenUsage() {
  return {
    inputTokens: 100,
    outputTokens: 25,
    totalTokens: 125,
  };
}


function createLogWriter() {
  return vi.fn<
    (entry: StructuredChatLog) => void
  >();
}


describe(
  "POST /api/chat",
  () => {
    afterEach(
      () => {
        vi.restoreAllMocks();
      },
    );


    it(
      "returns a chat response and records structured observability data",
      async () => {
        const chatService = {
          sendMessage:
            vi.fn()
              .mockResolvedValue({
                result: {
                  sessionId:
                    "session-1",

                  responseId:
                    "response-1",

                  answer:
                    "The critical threshold is above 3.5%.",

                  toolsUsed: [
                    "search_knowledge_base",
                  ],
                },

                tokenUsage:
                  createTokenUsage(),
              }),
        };

        const logWriter =
          createLogWriter();

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
            undefined,
            logWriter,
          ),
        );

        const server =
          app.listen(0);

        try {
          const address =
            server.address();

          if (
            !address
            || typeof address === "string"
          ) {
            throw new Error(
              "Expected server address.",
            );
          }

          const response =
            await fetch(
              `http://127.0.0.1:${address.port}/api/chat`,
              {
                method:
                  "POST",

                headers: {
                  "Content-Type":
                    "application/json",
                },

                body:
                  JSON.stringify({
                    message:
                      "What is the critical defect rate threshold?",
                  }),
              },
            );

          expect(
            response.status,
          ).toBe(200);

          const requestId =
            response.headers.get(
              "x-request-id",
            );

          expect(
            requestId,
          ).toBeTruthy();

          expect(
            requestId,
          ).toMatch(
            /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
          );

          const responseBody =
            await response.json();

          expect(
            responseBody,
          ).toEqual({
            sessionId:
              "session-1",

            responseId:
              "response-1",

            answer:
              "The critical threshold is above 3.5%.",

            toolsUsed: [
              "search_knowledge_base",
            ],
          });

          expect(
            responseBody,
          ).not.toHaveProperty(
            "tokenUsage",
          );

          expect(
            chatService.sendMessage,
          ).toHaveBeenCalledWith(
            "What is the critical defect rate threshold?",
            undefined,
          );

          expect(
            logWriter,
          ).toHaveBeenCalledTimes(1);

          const logEntry =
            logWriter.mock.calls[0]?.[0];

          expect(
            logEntry,
          ).toBeDefined();

          expect(
            logEntry,
          ).toEqual(
            expect.objectContaining({
              event:
                "chat_request_completed",

              requestId,

              method:
                "POST",

              path:
                "/api/chat",

              statusCode:
                200,

              toolsUsed: [
                "search_knowledge_base",
              ],

              tokenUsage: {
                inputTokens:
                  100,

                outputTokens:
                  25,

                totalTokens:
                  125,
              },
            }),
          );

          expect(
            logEntry?.latencyMs,
          ).toBeGreaterThanOrEqual(
            0,
          );

          expect(
            Number.isFinite(
              logEntry?.latencyMs,
            ),
          ).toBe(true);

          expect(
            logEntry?.timestamp,
          ).toBeTruthy();

          expect(
            Number.isNaN(
              Date.parse(
                logEntry?.timestamp
                ?? "",
              ),
            ),
          ).toBe(false);
        } finally {
          server.close();
        }
      },
    );


    it(
      "passes an existing session id",
      async () => {
        const chatService = {
          sendMessage:
            vi.fn()
              .mockResolvedValue({
                result: {
                  sessionId:
                    "existing-session",

                  responseId:
                    "response-2",

                  answer:
                    "Analysis completed.",

                  toolsUsed: [
                    "analyze_manufacturing_data",
                  ],
                },

                tokenUsage:
                  createTokenUsage(),
              }),
        };

        const logWriter =
          createLogWriter();

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
            undefined,
            logWriter,
          ),
        );

        const server =
          app.listen(0);

        try {
          const address =
            server.address();

          if (
            !address
            || typeof address === "string"
          ) {
            throw new Error(
              "Expected server address.",
            );
          }

          const response =
            await fetch(
              `http://127.0.0.1:${address.port}/api/chat`,
              {
                method:
                  "POST",

                headers: {
                  "Content-Type":
                    "application/json",
                },

                body:
                  JSON.stringify({
                    message:
                      "Which supplier has the highest defect rate?",

                    sessionId:
                      "existing-session",
                  }),
              },
            );

          expect(
            response.status,
          ).toBe(200);

          expect(
            response.headers.get(
              "x-request-id",
            ),
          ).toBeTruthy();

          expect(
            chatService.sendMessage,
          ).toHaveBeenCalledWith(
            "Which supplier has the highest defect rate?",
            "existing-session",
          );

          expect(
            logWriter,
          ).toHaveBeenCalledTimes(1);

          expect(
            logWriter.mock.calls[0]?.[0],
          ).toEqual(
            expect.objectContaining({
              statusCode:
                200,

              toolsUsed: [
                "analyze_manufacturing_data",
              ],

              tokenUsage:
                createTokenUsage(),
            }),
          );
        } finally {
          server.close();
        }
      },
    );


    it(
      "rejects a missing message and records the request",
      async () => {
        const chatService = {
          sendMessage:
            vi.fn(),
        };

        const logWriter =
          createLogWriter();

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
            undefined,
            logWriter,
          ),
        );

        const server =
          app.listen(0);

        try {
          const address =
            server.address();

          if (
            !address
            || typeof address === "string"
          ) {
            throw new Error(
              "Expected server address.",
            );
          }

          const response =
            await fetch(
              `http://127.0.0.1:${address.port}/api/chat`,
              {
                method:
                  "POST",

                headers: {
                  "Content-Type":
                    "application/json",
                },

                body:
                  JSON.stringify({}),
              },
            );

          expect(
            response.status,
          ).toBe(400);

          const requestId =
            response.headers.get(
              "x-request-id",
            );

          expect(
            requestId,
          ).toBeTruthy();

          expect(
            await response.json(),
          ).toEqual({
            error:
              "Request body must contain a message string.",
          });

          expect(
            chatService.sendMessage,
          ).not.toHaveBeenCalled();

          expect(
            logWriter,
          ).toHaveBeenCalledTimes(1);

          expect(
            logWriter.mock.calls[0]?.[0],
          ).toEqual(
            expect.objectContaining({
              requestId,

              statusCode:
                400,

              toolsUsed: [],

              tokenUsage: {
                inputTokens:
                  0,

                outputTokens:
                  0,

                totalTokens:
                  0,
              },
            }),
          );
        } finally {
          server.close();
        }
      },
    );


    it(
      "rejects a non-string session id and records the request",
      async () => {
        const chatService = {
          sendMessage:
            vi.fn(),
        };

        const logWriter =
          createLogWriter();

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
            undefined,
            logWriter,
          ),
        );

        const server =
          app.listen(0);

        try {
          const address =
            server.address();

          if (
            !address
            || typeof address === "string"
          ) {
            throw new Error(
              "Expected server address.",
            );
          }

          const response =
            await fetch(
              `http://127.0.0.1:${address.port}/api/chat`,
              {
                method:
                  "POST",

                headers: {
                  "Content-Type":
                    "application/json",
                },

                body:
                  JSON.stringify({
                    message:
                      "Hello",

                    sessionId:
                      123,
                  }),
              },
            );

          expect(
            response.status,
          ).toBe(400);

          const requestId =
            response.headers.get(
              "x-request-id",
            );

          expect(
            requestId,
          ).toBeTruthy();

          expect(
            await response.json(),
          ).toEqual({
            error:
              "Session ID must be a string when provided.",
          });

          expect(
            chatService.sendMessage,
          ).not.toHaveBeenCalled();

          expect(
            logWriter,
          ).toHaveBeenCalledTimes(1);

          expect(
            logWriter.mock.calls[0]?.[0],
          ).toEqual(
            expect.objectContaining({
              requestId,

              statusCode:
                400,

              toolsUsed: [],

              tokenUsage: {
                inputTokens:
                  0,

                outputTokens:
                  0,

                totalTokens:
                  0,
              },
            }),
          );
        } finally {
          server.close();
        }
      },
    );


    it(
      "rate limits excessive chat requests and records the limited request",
      async () => {
        const chatService = {
          sendMessage:
            vi.fn()
              .mockResolvedValue({
                result: {
                  sessionId:
                    "session-rate-limit",

                  responseId:
                    "response-rate-limit",

                  answer:
                    "Request completed.",

                  toolsUsed: [],
                },

                tokenUsage:
                  createTokenUsage(),
              }),
        };

        const rateLimiter =
          createChatRateLimiter({
            windowMs:
              60_000,

            limit:
              2,
          });

        const logWriter =
          createLogWriter();

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
            rateLimiter,
            logWriter,
          ),
        );

        const server =
          app.listen(0);

        try {
          const address =
            server.address();

          if (
            !address
            || typeof address === "string"
          ) {
            throw new Error(
              "Expected server address.",
            );
          }

          const url =
            `http://127.0.0.1:${address.port}/api/chat`;

          const requestOptions = {
            method:
              "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body:
              JSON.stringify({
                message:
                  "Run a manufacturing analysis.",
              }),
          };

          const firstResponse =
            await fetch(
              url,
              requestOptions,
            );

          const secondResponse =
            await fetch(
              url,
              requestOptions,
            );

          const limitedResponse =
            await fetch(
              url,
              requestOptions,
            );

          expect(
            firstResponse.status,
          ).toBe(200);

          expect(
            secondResponse.status,
          ).toBe(200);

          expect(
            limitedResponse.status,
          ).toBe(429);

          const limitedRequestId =
            limitedResponse.headers.get(
              "x-request-id",
            );

          expect(
            limitedRequestId,
          ).toBeTruthy();

          expect(
            await limitedResponse.json(),
          ).toEqual({
            error:
              "Too many chat requests. Please try again later.",
          });

          expect(
            chatService.sendMessage,
          ).toHaveBeenCalledTimes(
            2,
          );

          expect(
            logWriter,
          ).toHaveBeenCalledTimes(
            3,
          );

          const limitedLog =
            logWriter.mock.calls[2]?.[0];

          expect(
            limitedLog,
          ).toEqual(
            expect.objectContaining({
              requestId:
                limitedRequestId,

              statusCode:
                429,

              toolsUsed: [],

              tokenUsage: {
                inputTokens:
                  0,

                outputTokens:
                  0,

                totalTokens:
                  0,
              },
            }),
          );
        } finally {
          server.close();
        }
      },
    );
  },
);