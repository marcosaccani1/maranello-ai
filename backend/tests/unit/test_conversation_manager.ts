import {
  describe,
  expect,
  it,
} from "vitest";

import {
  ConversationManager,
} from "../../src/conversation/conversationManager.js";


describe(
  "ConversationManager",
  () => {
    it(
      "creates an empty session",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        expect(
          session.id,
        ).toBeTruthy();

        expect(
          session.messages,
        ).toEqual([]);

        expect(
          session.previousResponseId,
        ).toBeNull();

        expect(
          session.createdAt,
        ).toBeTruthy();

        expect(
          session.updatedAt,
        ).toBe(
          session.createdAt,
        );
      },
    );


    it(
      "retrieves an existing session",
      () => {
        const manager =
          new ConversationManager();

        const created =
          manager.createSession();

        const retrieved =
          manager.getSession(
            created.id,
          );

        expect(
          retrieved,
        ).toEqual(
          created,
        );
      },
    );


    it(
      "returns null for an unknown session",
      () => {
        const manager =
          new ConversationManager();

        expect(
          manager.getSession(
            "unknown-session",
          ),
        ).toBeNull();
      },
    );


    it(
      "adds messages in order",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        manager.addMessage(
          session.id,
          "user",
          "What is the defect rate?",
        );

        const updated =
          manager.addMessage(
            session.id,
            "assistant",
            "The defect rate is 2.47%.",
          );

        expect(
          updated.messages,
        ).toHaveLength(2);

        expect(
          updated.messages[0],
        ).toMatchObject({
          role:
            "user",

          content:
            "What is the defect rate?",
        });

        expect(
          updated.messages[1],
        ).toMatchObject({
          role:
            "assistant",

          content:
            "The defect rate is 2.47%.",
        });
      },
    );


    it(
      "trims message content",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        const updated =
          manager.addMessage(
            session.id,
            "user",
            "  Hello  ",
          );

        expect(
          updated.messages[0]?.content,
        ).toBe(
          "Hello",
        );
      },
    );


    it(
      "rejects empty messages",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        expect(
          () =>
            manager.addMessage(
              session.id,
              "user",
              "   ",
            ),
        ).toThrow(
          "Conversation message content must be non-empty.",
        );
      },
    );


    it(
      "rejects messages for unknown sessions",
      () => {
        const manager =
          new ConversationManager();

        expect(
          () =>
            manager.addMessage(
              "unknown-session",
              "user",
              "Hello",
            ),
        ).toThrow(
          "Conversation session not found: unknown-session",
        );
      },
    );


    it(
      "reuses an existing session",
      () => {
        const manager =
          new ConversationManager();

        const created =
          manager.createSession();

        const resolved =
          manager.getOrCreateSession(
            created.id,
          );

        expect(
          resolved.id,
        ).toBe(
          created.id,
        );
      },
    );


    it(
      "creates a new session when no id is provided",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.getOrCreateSession();

        expect(
          session.id,
        ).toBeTruthy();
      },
    );


    it(
      "creates a new session when the requested id does not exist",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.getOrCreateSession(
            "missing-session",
          );

        expect(
          session.id,
        ).not.toBe(
          "missing-session",
        );
      },
    );


    it(
      "stores the previous OpenAI response id",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        const updated =
          manager.setPreviousResponseId(
            session.id,
            "response-123",
          );

        expect(
          updated.previousResponseId,
        ).toBe(
          "response-123",
        );

        expect(
          manager.getSession(
            session.id,
          )?.previousResponseId,
        ).toBe(
          "response-123",
        );
      },
    );


    it(
      "trims the previous OpenAI response id",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        const updated =
          manager.setPreviousResponseId(
            session.id,
            "  response-123  ",
          );

        expect(
          updated.previousResponseId,
        ).toBe(
          "response-123",
        );
      },
    );


    it(
      "rejects an empty previous response id",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        expect(
          () =>
            manager.setPreviousResponseId(
              session.id,
              "   ",
            ),
        ).toThrow(
          "Previous response ID must be non-empty.",
        );
      },
    );


    it(
      "rejects previous response updates for unknown sessions",
      () => {
        const manager =
          new ConversationManager();

        expect(
          () =>
            manager.setPreviousResponseId(
              "unknown-session",
              "response-123",
            ),
        ).toThrow(
          "Conversation session not found: unknown-session",
        );
      },
    );


    it(
      "clears an existing session",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        expect(
          manager.clearSession(
            session.id,
          ),
        ).toBe(true);

        expect(
          manager.getSession(
            session.id,
          ),
        ).toBeNull();
      },
    );


    it(
      "does not expose internal mutable state",
      () => {
        const manager =
          new ConversationManager();

        const session =
          manager.createSession();

        const retrieved =
          manager.getSession(
            session.id,
          );

        if (!retrieved) {
          throw new Error(
            "Expected session to exist.",
          );
        }

        retrieved.messages.push({
          role:
            "user",

          content:
            "Injected message",

          createdAt:
            new Date().toISOString(),
        });

        retrieved.previousResponseId =
          "injected-response";

        const secondRead =
          manager.getSession(
            session.id,
          );

        expect(
          secondRead?.messages,
        ).toEqual([]);

        expect(
          secondRead?.previousResponseId,
        ).toBeNull();
      },
    );
  },
);