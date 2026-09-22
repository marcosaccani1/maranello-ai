import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";


vi.mock(
  "dotenv",
  () => ({
    default: {
      config: vi.fn(),
    },
  }),
);


const ORIGINAL_ENV = {
  ...process.env,
};


async function importEnvironment() {
  vi.resetModules();

  return import(
    "../../src/config/env.js"
  );
}


describe(
  "environment configuration",
  () => {
    beforeEach(
      () => {
        process.env = {
          ...ORIGINAL_ENV,
        };

        process.env.OPENAI_API_KEY =
          "test-api-key";

        delete process.env
          .CHAT_RATE_LIMIT_WINDOW_MINUTES;

        delete process.env
          .CHAT_RATE_LIMIT_MAX_REQUESTS;
      },
    );


    afterEach(
      () => {
        process.env = {
          ...ORIGINAL_ENV,
        };

        vi.resetModules();
      },
    );


    it(
      "loads when the OpenAI API key is configured",
      async () => {
        const { env } =
          await importEnvironment();

        expect(
          env.openAiApiKey,
        ).toBe(
          "test-api-key",
        );
      },
    );


    it(
      "fails fast when the OpenAI API key is missing",
      async () => {
        delete process.env.OPENAI_API_KEY;

        await expect(
          importEnvironment(),
        ).rejects.toThrow(
          "OPENAI_API_KEY environment variable is required.",
        );
      },
    );


    it(
      "fails fast when the OpenAI API key is empty",
      async () => {
        process.env.OPENAI_API_KEY =
          "";

        await expect(
          importEnvironment(),
        ).rejects.toThrow(
          "OPENAI_API_KEY environment variable is required.",
        );
      },
    );


    it(
      "fails fast when the OpenAI API key contains only whitespace",
      async () => {
        process.env.OPENAI_API_KEY =
          "   ";

        await expect(
          importEnvironment(),
        ).rejects.toThrow(
          "OPENAI_API_KEY environment variable is required.",
        );
      },
    );


    it(
      "uses the default chat rate limit configuration",
      async () => {
        const { env } =
          await importEnvironment();

        expect(
          env.chatRateLimitWindowMilliseconds,
        ).toBe(
          15 * 60 * 1000,
        );

        expect(
          env.chatRateLimitMaxRequests,
        ).toBe(
          30,
        );
      },
    );


    it(
      "loads a custom chat rate limit configuration",
      async () => {
        process.env
          .CHAT_RATE_LIMIT_WINDOW_MINUTES =
          "5";

        process.env
          .CHAT_RATE_LIMIT_MAX_REQUESTS =
          "12";

        const { env } =
          await importEnvironment();

        expect(
          env.chatRateLimitWindowMilliseconds,
        ).toBe(
          5 * 60 * 1000,
        );

        expect(
          env.chatRateLimitMaxRequests,
        ).toBe(
          12,
        );
      },
    );


    it(
      "rejects a non-positive chat rate limit window",
      async () => {
        process.env
          .CHAT_RATE_LIMIT_WINDOW_MINUTES =
          "0";

        await expect(
          importEnvironment(),
        ).rejects.toThrow(
          "Invalid CHAT_RATE_LIMIT_WINDOW_MINUTES environment variable: 0",
        );
      },
    );


    it(
      "rejects an invalid chat rate limit request count",
      async () => {
        process.env
          .CHAT_RATE_LIMIT_MAX_REQUESTS =
          "2.5";

        await expect(
          importEnvironment(),
        ).rejects.toThrow(
          "Invalid CHAT_RATE_LIMIT_MAX_REQUESTS environment variable: 2.5",
        );
      },
    );
  },
);