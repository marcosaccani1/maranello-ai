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
      "describes direct execution for supported manufacturing analyses",
      () => {
        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL.description,
        ).toContain(
          "Use this tool directly",
        );

        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL.description,
        ).toContain(
          "available structured manufacturing dataset",
        );

        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL.description,
        ).toContain(
          "do not require",
        );
      },
    );


    it(
      "uses the available manufacturing dataset as the default scope",
      () => {
        const questionProperty =
          ANALYZE_MANUFACTURING_DATA_TOOL
            .parameters
            .properties
            .question;

        expect(
          questionProperty,
        ).toBeDefined();

        expect(
          questionProperty?.description,
        ).toContain(
          "Use the available manufacturing dataset as the default scope.",
        );

        expect(
          questionProperty?.description,
        ).toContain(
          "Do not introduce",
        );
      },
    );


    it(
      "preserves the user's analytical scope",
      () => {
        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL.description,
        ).toContain(
          "Preserve the user's analytical scope exactly.",
        );

        expect(
          ANALYZE_MANUFACTURING_DATA_TOOL.description,
        ).toContain(
          "unless the user explicitly requested it",
        );
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