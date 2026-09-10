import express from "express";
import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  createChatRouter,
} from "../../src/routes/chatRoutes.js";


describe(
  "POST /api/chat",
  () => {
    afterEach(
      () => {
        vi.restoreAllMocks();
      },
    );


    it(
      "returns a chat response",
      async () => {
        const chatService = {
          sendMessage:
            vi.fn()
              .mockResolvedValue({
                sessionId:
                  "session-1",

                responseId:
                  "response-1",

                answer:
                  "The critical threshold is above 3.5%.",

                toolsUsed: [
                  "search_knowledge_base",
                ],
              }),
        };

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
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

          expect(
            await response.json(),
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
            chatService.sendMessage,
          ).toHaveBeenCalledWith(
            "What is the critical defect rate threshold?",
            undefined,
          );
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
                sessionId:
                  "existing-session",

                responseId:
                  "response-2",

                answer:
                  "Analysis completed.",

                toolsUsed: [
                  "analyze_manufacturing_data",
                ],
              }),
        };

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
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
            chatService.sendMessage,
          ).toHaveBeenCalledWith(
            "Which supplier has the highest defect rate?",
            "existing-session",
          );
        } finally {
          server.close();
        }
      },
    );


    it(
      "rejects a missing message",
      async () => {
        const chatService = {
          sendMessage:
            vi.fn(),
        };

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
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

          expect(
            await response.json(),
          ).toEqual({
            error:
              "Request body must contain a message string.",
          });

          expect(
            chatService.sendMessage,
          ).not.toHaveBeenCalled();
        } finally {
          server.close();
        }
      },
    );


    it(
      "rejects a non-string session id",
      async () => {
        const chatService = {
          sendMessage:
            vi.fn(),
        };

        const app =
          express();

        app.use(
          express.json(),
        );

        app.use(
          "/api/chat",
          createChatRouter(
            chatService,
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

          expect(
            await response.json(),
          ).toEqual({
            error:
              "Session ID must be a string when provided.",
          });

          expect(
            chatService.sendMessage,
          ).not.toHaveBeenCalled();
        } finally {
          server.close();
        }
      },
    );
  },
);