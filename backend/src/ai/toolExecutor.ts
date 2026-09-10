import type {
  DataAgentResponse,
} from "../models/dataAgent.js";
import type {
  RetrievedKnowledgeChunk,
} from "../rag/types.js";
import { RetrieverService } from "../rag/retrieverService.js";
import { DataAgentClient } from "../services/dataAgentClient.js";

import {
  TOOL_NAMES,
} from "./toolDefinitions.js";

import type {
  ToolName,
} from "./toolDefinitions.js";


interface RetrieverProvider {
  retrieve(
    question: string,
  ): Promise<RetrievedKnowledgeChunk[]>;
}


interface DataAgentProvider {
  analyze(
    question: string,
  ): Promise<DataAgentResponse>;
}


export interface ToolArguments {
  question: string;
}


export interface KnowledgeBaseToolResult {
  toolName:
    typeof TOOL_NAMES.searchKnowledgeBase;

  data: RetrievedKnowledgeChunk[];
}


export interface ManufacturingDataToolResult {
  toolName:
    typeof TOOL_NAMES.analyzeManufacturingData;

  data: DataAgentResponse;
}


export type ToolExecutionResult =
  | KnowledgeBaseToolResult
  | ManufacturingDataToolResult;


function parseToolArguments(
  args: unknown,
): ToolArguments {
  if (
    typeof args !== "object"
    || args === null
    || Array.isArray(args)
  ) {
    throw new Error(
      "Tool arguments must be an object.",
    );
  }

  const record =
    args as Record<string, unknown>;

  const keys =
    Object.keys(record);

  if (
    keys.length !== 1
    || keys[0] !== "question"
  ) {
    throw new Error(
      "Tool arguments must contain only the question field.",
    );
  }

  if (
    typeof record.question !== "string"
    || record.question.trim().length === 0
  ) {
    throw new Error(
      "Tool argument question must be a non-empty string.",
    );
  }

  return {
    question: record.question.trim(),
  };
}


function isToolName(
  value: string,
): value is ToolName {
  return Object.values(
    TOOL_NAMES,
  ).some(
    (toolName) => toolName === value,
  );
}


export class ToolExecutor {
  constructor(
    private readonly retriever:
    RetrieverProvider =
      new RetrieverService(),

    private readonly dataAgent:
    DataAgentProvider =
      new DataAgentClient(),
  ) {}


  async execute(
    toolName: string,
    args: unknown,
  ): Promise<ToolExecutionResult> {
    if (!isToolName(toolName)) {
      throw new Error(
        `Unsupported tool: ${toolName}`,
      );
    }

    const parsedArguments =
      parseToolArguments(args);

    switch (toolName) {
      case TOOL_NAMES.searchKnowledgeBase:
        return {
          toolName,
          data:
            await this.retriever.retrieve(
              parsedArguments.question,
            ),
        };

      case TOOL_NAMES.analyzeManufacturingData:
        return {
          toolName,
          data:
            await this.dataAgent.analyze(
              parsedArguments.question,
            ),
        };
    }
  }
}