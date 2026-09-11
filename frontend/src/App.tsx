import {
  type FormEvent,
  useState,
} from "react";

import "./App.css";

import {
  resolveApiUrl,
  sendChatMessage,
} from "./services/chatApi";

import type {
  ChatMessage,
} from "./types/chat";


const INITIAL_MESSAGE: ChatMessage = {
  id: "welcome-message",
  role: "assistant",
  content:
    "Hello, I am Maranello AI. Ask me about manufacturing "
    + "performance, quality data, internal policies, or procedures.",
};


function createMessageId(): string {
  return crypto.randomUUID();
}


function App() {
  const [
    messages,
    setMessages,
  ] = useState<ChatMessage[]>([
    INITIAL_MESSAGE,
  ]);

  const [
    sessionId,
    setSessionId,
  ] = useState<string>();

  const [
    input,
    setInput,
  ] = useState("");

  const [
    isLoading,
    setIsLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<string | null>(
    null,
  );


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    const normalizedInput =
      input.trim();

    if (
      !normalizedInput
      || isLoading
    ) {
      return;
    }

    const userMessage:
    ChatMessage = {
      id:
        createMessageId(),

      role:
        "user",

      content:
        normalizedInput,
    };

    setMessages(
      (currentMessages) => [
        ...currentMessages,
        userMessage,
      ],
    );

    setInput("");
    setError(null);
    setIsLoading(true);

    try {
      const response =
        await sendChatMessage({
          message:
            normalizedInput,

          sessionId,
        });

      setSessionId(
        response.sessionId,
      );

      const assistantMessage:
      ChatMessage = {
        id:
          createMessageId(),

        role:
          "assistant",

        content:
          response.answer,

        ...(response.chartUrl
          ? {
              chartUrl:
                resolveApiUrl(
                  response.chartUrl,
                ),
            }
          : {}),
      };

      setMessages(
        (currentMessages) => [
          ...currentMessages,
          assistantMessage,
        ],
      );
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "An unexpected error occurred.";

      setError(
        message,
      );
    } finally {
      setIsLoading(false);
    }
  }


  return (
    <main className="chat-app">
      <header className="chat-header">
        <div>
          <p className="chat-eyebrow">
            Manufacturing Intelligence
          </p>

          <h1>
            Maranello AI
          </h1>

          <p>
            Enterprise Knowledge & Data Assistant
          </p>
        </div>
      </header>

      <section
        className="chat-messages"
        aria-label="Conversation"
      >
        {messages.map(
          (message) => (
            <article
              key={message.id}
              className={
                `chat-message chat-message--${message.role}`
              }
            >
              <strong>
                {message.role === "user"
                  ? "You"
                  : "Maranello AI"}
              </strong>

              <p>
                {message.content}
              </p>

              {message.chartUrl && (
                <img
                  src={message.chartUrl}
                  alt="Manufacturing analysis chart"
                />
              )}
            </article>
          ),
        )}

        {isLoading && (
          <article
            className="
              chat-message
              chat-message--assistant
              chat-message--loading
            "
            aria-live="polite"
          >
            <strong>
              Maranello AI
            </strong>

            <p>
              Analyzing your request...
            </p>
          </article>
        )}
      </section>

      {error && (
        <div
          className="chat-error"
          role="alert"
        >
          {error}
        </div>
      )}

      <form
        className="chat-form"
        onSubmit={handleSubmit}
      >
        <label
          htmlFor="chat-input"
          className="chat-form__label"
        >
          Ask Maranello AI
        </label>

        <textarea
          id="chat-input"
          value={input}
          onChange={
            (event) =>
              setInput(
                event.target.value,
              )
          }
          placeholder="
            Ask about production quality,
            manufacturing KPIs, policies...
          "
          disabled={isLoading}
          rows={3}
        />

        <button
          type="submit"
          disabled={
            isLoading
            || !input.trim()
          }
        >
          {isLoading
            ? "Analyzing..."
            : "Send"}
        </button>
      </form>

      {sessionId && (
        <p className="chat-session">
          Active conversation
        </p>
      )}
    </main>
  );
}


export default App;