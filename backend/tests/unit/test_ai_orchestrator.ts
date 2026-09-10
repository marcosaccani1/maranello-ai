import type OpenAI from "openai";

import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  AIOrchestrator,
} from "../../src/ai/aiOrchestrator.js";

import {
  TOOL_NAMES,
} from "../../src/ai/toolDefinitions.js";


function createResponse(
  overrides: Partial<
    OpenAI.Responses.Response
  > = {},
): OpenAI.Responses.Response {
  const response = {
    id: "response-1",
    status: "completed",
    error: null,
    incomplete_details: null,
    output: [],
    output_text: "",
    ...overrides,
  };

  return response as OpenAI.Responses.Response;
}


describe(
  "AIOrchestrator",
  () => {
    it(
      "returns a direct final answer when no tool is requested",
      async () => {
        const responses = {
          create: vi.fn()
            .mockResolvedValue(
              createResponse({
                id: "response-direct",

                output_text:
                  "Hello from Maranello AI.",
              }),
            ),
        };

        const openAI = {
          responses,
        };

        const toolExecutor = {
          execute: vi.fn(),
        };

        const orchestrator =
          new AIOrchestrator(
            openAI,
            toolExecutor,
          );

        const result =
          await orchestrator.run(
            "Hello",
          );

        expect(result).toEqual({
          responseId:
            "response-direct",

          answer:
            "Hello from Maranello AI.",

          toolsUsed: [],
        });

        expect(
          toolExecutor.execute,
        ).not.toHaveBeenCalled();
      },
    );


    it(
      "continues an existing OpenAI conversation",
      async () => {
        const responses = {
          create: vi.fn()
            .mockResolvedValue(
              createResponse({
                id:
                  "response-follow-up",

                output_text:
                  "SUP-07 remains the supplier being discussed.",
              }),
            ),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            {
              execute: vi.fn(),
            },
          );

        await orchestrator.run(
          "What about its quality policy?",
          "response-previous",
        );

        expect(
          responses.create,
        ).toHaveBeenCalledTimes(1);

        expect(
          responses.create,
        ).toHaveBeenCalledWith(
          expect.objectContaining({
            input:
              "What about its quality policy?",

            previous_response_id:
              "response-previous",
          }),
        );
      },
    );


    it(
      "trims the previous response id",
      async () => {
        const responses = {
          create: vi.fn()
            .mockResolvedValue(
              createResponse({
                output_text:
                  "Follow-up response.",
              }),
            ),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            {
              execute: vi.fn(),
            },
          );

        await orchestrator.run(
          "Follow-up question",
          "  response-previous  ",
        );

        expect(
          responses.create,
        ).toHaveBeenCalledWith(
          expect.objectContaining({
            previous_response_id:
              "response-previous",
          }),
        );
      },
    );


    it(
      "executes a requested tool and returns the final answer",
      async () => {
        const firstResponse =
          createResponse({
            id:
              "response-tool",

            output: [
              {
                type:
                  "function_call",

                id:
                  "function-call-item",

                call_id:
                  "call-1",

                name:
                  TOOL_NAMES.searchKnowledgeBase,

                arguments:
                  JSON.stringify({
                    question:
                      "What is the critical defect rate threshold?",
                  }),

                status:
                  "completed",
              },
            ],
          });

        const finalResponse =
          createResponse({
            id:
              "response-final",

            output_text:
              "The critical threshold is defined by policy.",
          });

        const responses = {
          create: vi.fn()
            .mockResolvedValueOnce(
              firstResponse,
            )
            .mockResolvedValueOnce(
              finalResponse,
            ),
        };

        const toolExecutor = {
          execute: vi.fn()
            .mockResolvedValue({
              toolName:
                TOOL_NAMES.searchKnowledgeBase,

              data: [],
            }),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            toolExecutor,
          );

        const result =
          await orchestrator.run(
            "What is the critical defect rate threshold?",
          );

        expect(
          toolExecutor.execute,
        ).toHaveBeenCalledWith(
          TOOL_NAMES.searchKnowledgeBase,
          {
            question:
              "What is the critical defect rate threshold?",
          },
        );

        expect(
          responses.create,
        ).toHaveBeenCalledTimes(2);

        const secondRequest =
          responses.create.mock
            .calls[1]?.[0];

        expect(
          secondRequest
            ?.previous_response_id,
        ).toBe(
          "response-tool",
        );

        expect(
          secondRequest?.input,
        ).toEqual([
          {
            type:
              "function_call_output",

            call_id:
              "call-1",

            output:
              JSON.stringify({
                toolName:
                  TOOL_NAMES.searchKnowledgeBase,

                data: [],
              }),
          },
        ]);

        expect(result).toEqual({
          responseId:
            "response-final",

          answer:
            "The critical threshold is defined by policy.",

          toolsUsed: [
            TOOL_NAMES.searchKnowledgeBase,
          ],
        });
      },
    );


    it(
      "executes multiple tool calls from the same response",
      async () => {
        const firstResponse =
          createResponse({
            id:
              "response-hybrid",

            output: [
              {
                type:
                  "function_call",

                id:
                  "call-item-1",

                call_id:
                  "call-1",

                name:
                  TOOL_NAMES.analyzeManufacturingData,

                arguments:
                  JSON.stringify({
                    question:
                      "What was Line 3 defect rate?",
                  }),

                status:
                  "completed",
              },

              {
                type:
                  "function_call",

                id:
                  "call-item-2",

                call_id:
                  "call-2",

                name:
                  TOOL_NAMES.searchKnowledgeBase,

                arguments:
                  JSON.stringify({
                    question:
                      "What action is required for a critical defect rate?",
                  }),

                status:
                  "completed",
              },
            ],
          });

        const finalResponse =
          createResponse({
            id:
              "response-final",

            output_text:
              "Line 3 performance requires escalation.",
          });

        const responses = {
          create: vi.fn()
            .mockResolvedValueOnce(
              firstResponse,
            )
            .mockResolvedValueOnce(
              finalResponse,
            ),
        };

        const toolExecutor = {
          execute: vi.fn()
            .mockResolvedValue({
              success: true,
            }),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            toolExecutor,
          );

        const result =
          await orchestrator.run(
            "Analyze Line 3 and tell me what policy requires.",
          );

        expect(
          toolExecutor.execute,
        ).toHaveBeenCalledTimes(2);

        expect(
          result.toolsUsed,
        ).toEqual([
          TOOL_NAMES.analyzeManufacturingData,
          TOOL_NAMES.searchKnowledgeBase,
        ]);
      },
    );


    it(
      "rejects an empty question",
      async () => {
        const responses = {
          create: vi.fn(),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            {
              execute: vi.fn(),
            },
          );

        await expect(
          orchestrator.run(
            "   ",
          ),
        ).rejects.toThrow(
          "Question must be a non-empty string.",
        );

        expect(
          responses.create,
        ).not.toHaveBeenCalled();
      },
    );


    it(
      "rejects an empty previous response id",
      async () => {
        const responses = {
          create: vi.fn(),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            {
              execute: vi.fn(),
            },
          );

        await expect(
          orchestrator.run(
            "Follow-up question",
            "   ",
          ),
        ).rejects.toThrow(
          "Previous response ID must be a non-empty string when provided.",
        );

        expect(
          responses.create,
        ).not.toHaveBeenCalled();
      },
    );


    it(
      "rejects invalid JSON tool arguments",
      async () => {
        const responses = {
          create: vi.fn()
            .mockResolvedValue(
              createResponse({
                output: [
                  {
                    type:
                      "function_call",

                    id:
                      "call-item-1",

                    call_id:
                      "call-1",

                    name:
                      TOOL_NAMES.searchKnowledgeBase,

                    arguments:
                      "{invalid-json",

                    status:
                      "completed",
                  },
                ],
              }),
            ),
        };

        const toolExecutor = {
          execute: vi.fn(),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            toolExecutor,
          );

        await expect(
          orchestrator.run(
            "Test question",
          ),
        ).rejects.toThrow(
          "The LLM returned invalid JSON tool arguments.",
        );

        expect(
          toolExecutor.execute,
        ).not.toHaveBeenCalled();
      },
    );


    it(
      "rejects incomplete OpenAI responses",
      async () => {
        const responses = {
          create: vi.fn()
            .mockResolvedValue(
              createResponse({
                status:
                  "incomplete",
              }),
            ),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            {
              execute: vi.fn(),
            },
          );

        await expect(
          orchestrator.run(
            "Test question",
          ),
        ).rejects.toThrow(
          "OpenAI response did not complete successfully",
        );
      },
    );


    it(
      "rejects a completed response without a final answer",
      async () => {
        const responses = {
          create: vi.fn()
            .mockResolvedValue(
              createResponse(),
            ),
        };

        const orchestrator =
          new AIOrchestrator(
            {
              responses,
            },
            {
              execute: vi.fn(),
            },
          );

        await expect(
          orchestrator.run(
            "Test question",
          ),
        ).rejects.toThrow(
          "OpenAI returned no final answer.",
        );
      },
    );
  },
);