import {
  randomUUID,
} from "node:crypto";

import type {
  ConversationMessage,
  ConversationRole,
  ConversationSession,
} from "./types.js";


export class ConversationManager {
  private readonly sessions =
    new Map<
      string,
      ConversationSession
    >();


  createSession(): ConversationSession {
    const now =
      new Date().toISOString();

    const session: ConversationSession = {
      id:
        randomUUID(),

      messages: [],

      previousResponseId:
        null,

      createdAt:
        now,

      updatedAt:
        now,
    };

    this.sessions.set(
      session.id,
      session,
    );

    return this.cloneSession(
      session,
    );
  }


  getSession(
    sessionId: string,
  ): ConversationSession | null {
    const session =
      this.sessions.get(
        sessionId,
      );

    if (!session) {
      return null;
    }

    return this.cloneSession(
      session,
    );
  }


  getOrCreateSession(
    sessionId?: string,
  ): ConversationSession {
    if (sessionId) {
      const existing =
        this.getSession(
          sessionId,
        );

      if (existing) {
        return existing;
      }
    }

    return this.createSession();
  }


  addMessage(
    sessionId: string,
    role: ConversationRole,
    content: string,
  ): ConversationSession {
    const normalizedContent =
      content.trim();

    if (!normalizedContent) {
      throw new Error(
        "Conversation message content must be non-empty.",
      );
    }

    const session =
      this.sessions.get(
        sessionId,
      );

    if (!session) {
      throw new Error(
        `Conversation session not found: ${sessionId}`,
      );
    }

    const message:
    ConversationMessage = {
      role,

      content:
        normalizedContent,

      createdAt:
        new Date().toISOString(),
    };

    session.messages.push(
      message,
    );

    session.updatedAt =
      message.createdAt;

    return this.cloneSession(
      session,
    );
  }


  setPreviousResponseId(
    sessionId: string,
    responseId: string,
  ): ConversationSession {
    const normalizedResponseId =
      responseId.trim();

    if (!normalizedResponseId) {
      throw new Error(
        "Previous response ID must be non-empty.",
      );
    }

    const session =
      this.sessions.get(
        sessionId,
      );

    if (!session) {
      throw new Error(
        `Conversation session not found: ${sessionId}`,
      );
    }

    session.previousResponseId =
      normalizedResponseId;

    session.updatedAt =
      new Date().toISOString();

    return this.cloneSession(
      session,
    );
  }


  clearSession(
    sessionId: string,
  ): boolean {
    return this.sessions.delete(
      sessionId,
    );
  }


  private cloneSession(
    session: ConversationSession,
  ): ConversationSession {
    return {
      ...session,

      messages:
        session.messages.map(
          (message) => ({
            ...message,
          }),
        ),
    };
  }
}