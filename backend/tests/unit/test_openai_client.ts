import {
  describe,
  expect,
  it,
} from "vitest";

import {
  OpenAIClient,
} from "../../src/ai/openAiClient.js";


describe(
  "OpenAIClient",
  () => {
    it(
      "creates a client with a valid API key",
      () => {
        const client =
          new OpenAIClient(
            "test-api-key",
            5000,
          );

        expect(
          client.responses,
        ).toBeDefined();
      },
    );


    it(
      "rejects an empty API key",
      () => {
        expect(
          () =>
            new OpenAIClient(
              "",
              5000,
            ),
        ).toThrow(
          "OPENAI_API_KEY is required to use the LLM.",
        );
      },
    );


    it(
      "rejects a whitespace-only API key",
      () => {
        expect(
          () =>
            new OpenAIClient(
              "   ",
              5000,
            ),
        ).toThrow(
          "OPENAI_API_KEY is required to use the LLM.",
        );
      },
    );
  },
);