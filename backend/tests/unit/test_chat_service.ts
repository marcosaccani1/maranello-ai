import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import type {
  ConversationSession,
} from "../../src/conversation/types.js";

import {
  ChatService,
} from "../../src/services/chatService.js";


function createSession(
  id = "session-1",
  previousResponseId:
    string | null = null,
): ConversationSession {
  return {
    id,

    messages: [],

    previousResponseId,

    createdAt:
      "2026-01-01T00:00:00.000Z",

    updatedAt:
      "2026-01-01T00:00:00.000Z",
  };
}


function createConversationManager(
  session: ConversationSession,
) {
  return {
    getOrCreateSession:
      vi.fn()
        .mockReturnValue(
          session,
        ),

    addMessage:
      vi.fn()
        .mockReturnValue(
          session,
        ),

    setPreviousResponseId:
      vi.fn()
        .mockReturnValue(
          session,
        ),
  };
}


describe(
  "ChatService",
  () => {
    it(
      "creates a session and processes a message",
      async () => {
        const session =
          createSession();

        const conversationManager =
          createConversationManager(
            session,
          );

        const orchestrator = {
          run:
            vi.fn()
              .mockResolvedValue({
                responseId:
                  "response-1",

                answer:
                  "The critical threshold is above 3.5%.",

                toolsUsed: [
                  "search_knowledge_base",
                ],
              }),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        const result =
          await service.sendMessage(
            "What is the critical defect rate threshold?",
          );

        expect(
          conversationManager
            .getOrCreateSession,
        ).toHaveBeenCalledWith(
          undefined,
        );

        expect(
          orchestrator.run,
        ).toHaveBeenCalledWith(
          "What is the critical defect rate threshold?",
          undefined,
        );

        expect(result).toEqual({
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
      },
    );


    it(
      "passes the previous response id to the orchestrator",
      async () => {
        const session =
          createSession(
            "existing-session",
            "response-previous",
          );

        const conversationManager =
          createConversationManager(
            session,
          );

        const orchestrator = {
          run:
            vi.fn()
              .mockResolvedValue({
                responseId:
                  "response-new",

                answer:
                  "Follow-up completed.",

                toolsUsed: [],
              }),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        await service.sendMessage(
          "What about its quality policy?",
          "existing-session",
        );

        expect(
          orchestrator.run,
        ).toHaveBeenCalledWith(
          "What about its quality policy?",
          "response-previous",
        );
      },
    );


    it(
      "stores the new response id after a successful turn",
      async () => {
        const session =
          createSession();

        const conversationManager =
          createConversationManager(
            session,
          );

        const orchestrator = {
          run:
            vi.fn()
              .mockResolvedValue({
                responseId:
                  "response-new",

                answer:
                  "Analysis completed.",

                toolsUsed: [
                  "analyze_manufacturing_data",
                ],
              }),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        await service.sendMessage(
          "Analyze production lines.",
        );

        expect(
          conversationManager
            .setPreviousResponseId,
        ).toHaveBeenCalledWith(
          "session-1",
          "response-new",
        );
      },
    );


    it(
      "maps a Data Agent chart URL to the backend chart proxy",
      async () => {
        const session =
          createSession();

        const conversationManager =
          createConversationManager(
            session,
          );

        const orchestrator = {
          run:
            vi.fn()
              .mockResolvedValue({
                responseId:
                  "response-chart",

                answer:
                  "The monthly defect rate trend has been generated.",

                toolsUsed: [
                  "analyze_manufacturing_data",
                ],

                chartUrl:
                  "/charts/monthly_defect_rate_test.png",
              }),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        const result =
          await service.sendMessage(
            "Show the monthly defect rate trend.",
          );

        expect(
          result.chartUrl,
        ).toBe(
          "/api/charts/monthly_defect_rate_test.png",
        );
      },
    );


    it(
      "reuses a provided session id",
      async () => {
        const session =
          createSession(
            "existing-session",
          );

        const conversationManager =
          createConversationManager(
            session,
          );

        const orchestrator = {
          run:
            vi.fn()
              .mockResolvedValue({
                responseId:
                  "response-2",

                answer:
                  "Analysis completed.",

                toolsUsed: [
                  "analyze_manufacturing_data",
                ],
              }),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        const result =
          await service.sendMessage(
            "Analyze production lines.",
            "existing-session",
          );

        expect(
          conversationManager
            .getOrCreateSession,
        ).toHaveBeenCalledWith(
          "existing-session",
        );

        expect(
          result.sessionId,
        ).toBe(
          "existing-session",
        );
      },
    );


    it(
      "stores the user and assistant messages",
      async () => {
        const session =
          createSession();

        const conversationManager =
          createConversationManager(
            session,
          );

        const orchestrator = {
          run:
            vi.fn()
              .mockResolvedValue({
                responseId:
                  "response-3",

                answer:
                  "Line 3 has the highest defect rate.",

                toolsUsed: [
                  "analyze_manufacturing_data",
                ],
              }),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        await service.sendMessage(
          "Which line has the highest defect rate?",
        );

        expect(
          conversationManager.addMessage,
        ).toHaveBeenNthCalledWith(
          1,
          "session-1",
          "user",
          "Which line has the highest defect rate?",
        );

        expect(
          conversationManager.addMessage,
        ).toHaveBeenNthCalledWith(
          2,
          "session-1",
          "assistant",
          "Line 3 has the highest defect rate.",
        );
      },
    );


    it(
      "trims the message and session id",
      async () => {
        const session =
          createSession(
            "session-2",
          );

        const conversationManager =
          createConversationManager(
            session,
          );

        const orchestrator = {
          run:
            vi.fn()
              .mockResolvedValue({
                responseId:
                  "response-4",

                answer:
                  "Done.",

                toolsUsed: [],
              }),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        await service.sendMessage(
          "  Hello  ",
          "  session-2  ",
        );

        expect(
          conversationManager
            .getOrCreateSession,
        ).toHaveBeenCalledWith(
          "session-2",
        );

        expect(
          orchestrator.run,
        ).toHaveBeenCalledWith(
          "Hello",
          undefined,
        );
      },
    );


    it(
      "rejects an empty message",
      async () => {
        const conversationManager = {
          getOrCreateSession:
            vi.fn(),

          addMessage:
            vi.fn(),

          setPreviousResponseId:
            vi.fn(),
        };

        const orchestrator = {
          run:
            vi.fn(),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        await expect(
          service.sendMessage(
            "   ",
          ),
        ).rejects.toThrow(
          "Chat message must be a non-empty string.",
        );

        expect(
          conversationManager
            .getOrCreateSession,
        ).not.toHaveBeenCalled();

        expect(
          orchestrator.run,
        ).not.toHaveBeenCalled();
      },
    );


    it(
      "rejects an empty session id",
      async () => {
        const conversationManager = {
          getOrCreateSession:
            vi.fn(),

          addMessage:
            vi.fn(),

          setPreviousResponseId:
            vi.fn(),
        };

        const orchestrator = {
          run:
            vi.fn(),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        await expect(
          service.sendMessage(
            "Hello",
            "   ",
          ),
        ).rejects.toThrow(
          "Session ID must be a non-empty string when provided.",
        );

        expect(
          conversationManager
            .getOrCreateSession,
        ).not.toHaveBeenCalled();
      },
    );


    it(
      "does not update the conversation when orchestration fails",
      async () => {
        const session =
          createSession(
            "session-1",
            "response-previous",
          );

        const conversationManager =
          createConversationManager(
            session,
          );

        const orchestrator = {
          run:
            vi.fn()
              .mockRejectedValue(
                new Error(
                  "LLM unavailable",
                ),
              ),
        };

        const service =
          new ChatService(
            conversationManager,
            orchestrator,
          );

        await expect(
          service.sendMessage(
            "Test question",
          ),
        ).rejects.toThrow(
          "LLM unavailable",
        );

        expect(
          conversationManager.addMessage,
        ).not.toHaveBeenCalled();

        expect(
          conversationManager
            .setPreviousResponseId,
        ).not.toHaveBeenCalled();
      },
    );
  },
);