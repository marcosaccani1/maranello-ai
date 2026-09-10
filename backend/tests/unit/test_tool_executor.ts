import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import type {
  DataAgentResponse,
} from "../../src/models/dataAgent.js";
import type {
  RetrievedKnowledgeChunk,
} from "../../src/rag/types.js";

import {
  ToolExecutor,
} from "../../src/ai/toolExecutor.js";

import {
  TOOL_NAMES,
} from "../../src/ai/toolDefinitions.js";


describe(
  "ToolExecutor",
  () => {
    it(
      "executes knowledge base retrieval",
      async () => {
        const retrievedChunks:
        RetrievedKnowledgeChunk[] = [
          {
            id: "chunk-1",
            source:
              "manufacturing_quality_policy.md",
            section:
              "4.2 Defect Rate Thresholds",
            content:
              "Critical defect rate threshold.",
            chunkIndex: 4,
            distance: 0.25,
          },
        ];

        const retriever = {
          retrieve: vi.fn()
            .mockResolvedValue(
              retrievedChunks,
            ),
        };

        const dataAgent = {
          analyze: vi.fn(),
        };

        const executor =
          new ToolExecutor(
            retriever,
            dataAgent,
          );

        const result =
          await executor.execute(
            TOOL_NAMES.searchKnowledgeBase,
            {
              question:
                "What is the critical defect rate threshold?",
            },
          );

        expect(
          retriever.retrieve,
        ).toHaveBeenCalledWith(
          "What is the critical defect rate threshold?",
        );

        expect(
          dataAgent.analyze,
        ).not.toHaveBeenCalled();

        expect(result).toEqual({
          toolName:
            TOOL_NAMES.searchKnowledgeBase,
          data: retrievedChunks,
        });
      },
    );


    it(
      "executes manufacturing data analysis",
      async () => {
        const dataAgentResponse = {
          success: true,
        } as DataAgentResponse;

        const retriever = {
          retrieve: vi.fn(),
        };

        const dataAgent = {
          analyze: vi.fn()
            .mockResolvedValue(
              dataAgentResponse,
            ),
        };

        const executor =
          new ToolExecutor(
            retriever,
            dataAgent,
          );

        const result =
          await executor.execute(
            TOOL_NAMES.analyzeManufacturingData,
            {
              question:
                "Which supplier has the highest defect rate?",
            },
          );

        expect(
          dataAgent.analyze,
        ).toHaveBeenCalledWith(
          "Which supplier has the highest defect rate?",
        );

        expect(
          retriever.retrieve,
        ).not.toHaveBeenCalled();

        expect(result).toEqual({
          toolName:
            TOOL_NAMES.analyzeManufacturingData,
          data: dataAgentResponse,
        });
      },
    );


    it(
      "trims the question before executing a tool",
      async () => {
        const retriever = {
          retrieve: vi.fn()
            .mockResolvedValue([]),
        };

        const dataAgent = {
          analyze: vi.fn(),
        };

        const executor =
          new ToolExecutor(
            retriever,
            dataAgent,
          );

        await executor.execute(
          TOOL_NAMES.searchKnowledgeBase,
          {
            question:
              "  What is the defect rate policy?  ",
          },
        );

        expect(
          retriever.retrieve,
        ).toHaveBeenCalledWith(
          "What is the defect rate policy?",
        );
      },
    );


    it(
      "rejects unsupported tools",
      async () => {
        const retriever = {
          retrieve: vi.fn(),
        };

        const dataAgent = {
          analyze: vi.fn(),
        };

        const executor =
          new ToolExecutor(
            retriever,
            dataAgent,
          );

        await expect(
          executor.execute(
            "unknown_tool",
            {
              question: "Test question",
            },
          ),
        ).rejects.toThrow(
          "Unsupported tool: unknown_tool",
        );

        expect(
          retriever.retrieve,
        ).not.toHaveBeenCalled();

        expect(
          dataAgent.analyze,
        ).not.toHaveBeenCalled();
      },
    );


    it(
      "rejects an empty question",
      async () => {
        const retriever = {
          retrieve: vi.fn(),
        };

        const dataAgent = {
          analyze: vi.fn(),
        };

        const executor =
          new ToolExecutor(
            retriever,
            dataAgent,
          );

        await expect(
          executor.execute(
            TOOL_NAMES.searchKnowledgeBase,
            {
              question: "   ",
            },
          ),
        ).rejects.toThrow(
          "Tool argument question must be a non-empty string.",
        );
      },
    );


    it(
      "rejects non-object arguments",
      async () => {
        const retriever = {
          retrieve: vi.fn(),
        };

        const dataAgent = {
          analyze: vi.fn(),
        };

        const executor =
          new ToolExecutor(
            retriever,
            dataAgent,
          );

        await expect(
          executor.execute(
            TOOL_NAMES.searchKnowledgeBase,
            "invalid",
          ),
        ).rejects.toThrow(
          "Tool arguments must be an object.",
        );
      },
    );


    it(
      "rejects unexpected argument fields",
      async () => {
        const retriever = {
          retrieve: vi.fn(),
        };

        const dataAgent = {
          analyze: vi.fn(),
        };

        const executor =
          new ToolExecutor(
            retriever,
            dataAgent,
          );

        await expect(
          executor.execute(
            TOOL_NAMES.searchKnowledgeBase,
            {
              question:
                "What is the quality policy?",
              unexpected: true,
            },
          ),
        ).rejects.toThrow(
          "Tool arguments must contain only the question field.",
        );
      },
    );
  },
);