import {
  describe,
  expect,
  it,
} from "vitest";

import {
  ANALYZE_MANUFACTURING_DATA_TOOL,
  SEARCH_KNOWLEDGE_BASE_TOOL,
  TOOL_DEFINITIONS,
  TOOL_NAMES,
} from "../../src/ai/toolDefinitions.js";


describe(
  "toolDefinitions",
  () => {
    it(
      "defines the knowledge base search tool",
      () => {
        expect(
          SEARCH_KNOWLEDGE_BASE_TOOL.type,
        ).toBe(
          "function",
        );

        expect(
          SEARCH_KNOWLEDGE_BASE_TOOL.name,
        ).toBe(
          "search_knowledge_base",
        );

        expect(
          SEARCH_KNOWLEDGE_BASE_TOOL.strict,
        ).toBe(true);

        expect(
          SEARCH_KNOWLEDGE_BASE_TOOL.parameters
            .required,
        ).toEqual([
          "question",
        ]);

        expect(
          SEARCH_KNOWLEDGE_BASE_TOOL.parameters
            .additionalProperties,
        ).toBe(false);
      },
    );


    it(
      "defines the manufacturing analysis tool",
      () => {
        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL.type,
        ).toBe(
          "function",
        );

        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL.name,
        ).toBe(
          "analyze_manufacturing_data",
        );

        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL.strict,
        ).toBe(true);

        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL
            .parameters
            .required,
        ).toEqual([
          "question",
        ]);

        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL
            .parameters
            .additionalProperties,
        ).toBe(false);
      },
    );


    it(
      "exposes exactly the supported tools",
      () => {
        expect(
          TOOL_DEFINITIONS,
        ).toHaveLength(2);

        expect(
          TOOL_DEFINITIONS.map(
            (tool) => tool.name,
          ),
        ).toEqual([
          TOOL_NAMES.searchKnowledgeBase,
          TOOL_NAMES.analyzeManufacturingData,
        ]);
      },
    );


    it(
      "uses unique tool names",
      () => {
        const names =
          TOOL_DEFINITIONS.map(
            (tool) => tool.name,
          );

        expect(
          new Set(names).size,
        ).toBe(names.length);
      },
    );
  },
);