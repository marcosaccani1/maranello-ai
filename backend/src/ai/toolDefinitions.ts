export const TOOL_NAMES = {
  searchKnowledgeBase:
    "search_knowledge_base",

  analyzeManufacturingData:
    "analyze_manufacturing_data",
} as const;


export type ToolName =
  typeof TOOL_NAMES[
    keyof typeof TOOL_NAMES
  ];


export interface ToolParameterProperty {
  type: "string";
  description: string;
}


export interface ToolParametersSchema {
  [key: string]: unknown;

  type: "object";

  properties: Record<
    string,
    ToolParameterProperty
  >;

  required: string[];

  additionalProperties: false;
}


export interface ToolDefinition {
  type: "function";
  name: ToolName;
  description: string;
  strict: true;
  parameters: ToolParametersSchema;
}


export const SEARCH_KNOWLEDGE_BASE_TOOL:
ToolDefinition = {
  type: "function",

  name:
    TOOL_NAMES.searchKnowledgeBase,

  description:
    "Search the internal manufacturing knowledge base "
    + "for company policies, procedures, quality rules, "
    + "thresholds, escalation requirements, responsibilities, "
    + "and operational guidance. Preserve the user's requested "
    + "scope when formulating the search question.",

  strict: true,

  parameters: {
    type: "object",

    properties: {
      question: {
        type: "string",
        description:
          "A focused knowledge question derived from the user's "
          + "request. Preserve the user's scope and do not add "
          + "requirements that were not requested.",
      },
    },

    required: [
      "question",
    ],

    additionalProperties: false,
  },
};


export const ANALYZE_MANUFACTURING_DATA_TOOL:
ToolDefinition = {
  type: "function",

  name:
    TOOL_NAMES.analyzeManufacturingData,

  description:
    "Analyze structured manufacturing data to calculate "
    + "KPIs, defect rates, trends, comparisons, supplier "
    + "performance, production-line performance, shifts, "
    + "components, models, plants, teams, and charts. "
    + "Preserve the user's analytical scope exactly. "
    + "Do not add a time period, trend analysis, comparison "
    + "period, grouping dimension, or other analytical "
    + "requirement unless the user explicitly requested it.",

  strict: true,

  parameters: {
    type: "object",

    properties: {
      question: {
        type: "string",
        description:
          "The manufacturing analysis requested by the user. "
          + "Keep the question focused on exactly the requested "
          + "metric and dimensions. Do not introduce time periods, "
          + "historical trends, prior-period comparisons, or other "
          + "constraints unless they were explicitly requested "
          + "by the user.",
      },
    },

    required: [
      "question",
    ],

    additionalProperties: false,
  },
};


export const TOOL_DEFINITIONS:
readonly ToolDefinition[] = [
  SEARCH_KNOWLEDGE_BASE_TOOL,
  ANALYZE_MANUFACTURING_DATA_TOOL,
];