import type OpenAI from "openai";

import { env } from "../config/env.js";

import {
  OpenAIClient,
} from "./openAiClient.js";

import {
  TOOL_DEFINITIONS,
  TOOL_NAMES,
} from "./toolDefinitions.js";

import {
  ToolExecutor,
} from "./toolExecutor.js";


const SYSTEM_INSTRUCTIONS = `
You are Maranello AI, an enterprise manufacturing knowledge
and data assistant for a fictional premium automotive manufacturer.

Use the available tools autonomously whenever the user's request
requires internal company knowledge or manufacturing data.

Use search_knowledge_base for:
- internal policies
- procedures
- quality thresholds
- escalation rules
- responsibilities
- operational guidance

Use analyze_manufacturing_data for:
- KPIs
- defect rates
- trends
- comparisons
- supplier performance
- production-line performance
- shifts
- components
- models
- plants
- teams
- manufacturing charts

When a manufacturing analysis request is directly supported by
an available tool, execute the tool without asking unnecessary
clarifying questions.

Use the available manufacturing dataset as the default analytical
scope unless the user explicitly requests a different supported
scope.

Do not ask the user to specify a time range, grouping dimension,
comparison period, dataset scope, or output format when those
details are not required to execute the requested analysis.

For example, a request for the monthly defect rate trend is already
sufficient to run the corresponding manufacturing analysis over
the available dataset.

Ask for clarification only when information that is genuinely
required to execute the request is missing, when the request has
multiple materially different interpretations that cannot be
resolved from the conversation, or when the requested analysis is
not supported by the available tools.

When formulating a tool question, preserve the user's analytical
scope. Do not invent additional filters, periods, groupings,
comparisons, or constraints that the user did not request.

If a question requires both historical manufacturing data and
company policy, use both tools.

Do not invent internal policies, thresholds, manufacturing values,
or analytical results. Base those claims on tool results.

Answer in the same language used by the user.

When knowledge-base information is used, mention the relevant
source document and section naturally in the answer.
`.trim();


export const MAX_TOOL_ROUNDS = 5;


interface ResponsesProvider {
  create(
    params: OpenAI.Responses.ResponseCreateParamsNonStreaming,
  ): Promise<OpenAI.Responses.Response>;
}


interface OpenAIProvider {
  responses: ResponsesProvider;
}


interface ToolExecutionProvider {
  execute(
    toolName: string,
    args: unknown,
  ): Promise<unknown>;
}


export interface TokenUsage {
  inputTokens: number;
  outputTokens: number;
  totalTokens: number;
}


export interface OrchestrationResult {
  responseId: string;
  answer: string;
  toolsUsed: string[];
  tokenUsage: TokenUsage;
  chartUrl?: string;
}


function parseArguments(
  argumentsJson: string,
): unknown {
  try {
    return JSON.parse(
      argumentsJson,
    ) as unknown;
  } catch {
    throw new Error(
      "The LLM returned invalid JSON tool arguments.",
    );
  }
}


function extractChartUrl(
  result: unknown,
): string | null {
  if (
    typeof result !== "object"
    || result === null
  ) {
    return null;
  }

  const toolResult =
    result as Record<
      string,
      unknown
    >;

  if (
    toolResult.toolName
    !== TOOL_NAMES.analyzeManufacturingData
  ) {
    return null;
  }

  const data =
    toolResult.data;

  if (
    typeof data !== "object"
    || data === null
  ) {
    return null;
  }

  const dataResponse =
    data as Record<
      string,
      unknown
    >;

  const analysisResult =
    dataResponse.result;

  if (
    typeof analysisResult !== "object"
    || analysisResult === null
  ) {
    return null;
  }

  const analysisRecord =
    analysisResult as Record<
      string,
      unknown
    >;

  const chartUrl =
    analysisRecord.chart_url;

  if (
    typeof chartUrl !== "string"
    || !chartUrl.trim()
  ) {
    return null;
  }

  return chartUrl.trim();
}


function addResponseUsage(
  tokenUsage: TokenUsage,
  response: OpenAI.Responses.Response,
): void {
  const usage =
    response.usage;

  if (!usage) {
    return;
  }

  tokenUsage.inputTokens +=
    usage.input_tokens;

  tokenUsage.outputTokens +=
    usage.output_tokens;

  tokenUsage.totalTokens +=
    usage.total_tokens;
}


export class AIOrchestrator {
  constructor(
    private readonly openAI:
    OpenAIProvider =
      new OpenAIClient(),

    private readonly toolExecutor:
    ToolExecutionProvider =
      new ToolExecutor(),
  ) {}


  async run(
    question: string,
    previousResponseId?: string,
  ): Promise<OrchestrationResult> {
    const normalizedQuestion =
      question.trim();

    if (!normalizedQuestion) {
      throw new Error(
        "Question must be a non-empty string.",
      );
    }

    const normalizedPreviousResponseId =
      previousResponseId?.trim();

    if (
      previousResponseId !== undefined
      && !normalizedPreviousResponseId
    ) {
      throw new Error(
        "Previous response ID must be a non-empty string when provided.",
      );
    }

    const tokenUsage: TokenUsage = {
      inputTokens: 0,
      outputTokens: 0,
      totalTokens: 0,
    };

    let response =
      await this.openAI.responses.create({
        model:
          env.llmModel,

        instructions:
          SYSTEM_INSTRUCTIONS,

        input:
          normalizedQuestion,

        previous_response_id:
          normalizedPreviousResponseId,

        tools: [
          ...TOOL_DEFINITIONS,
        ],
      });

    addResponseUsage(
      tokenUsage,
      response,
    );

    const toolsUsed: string[] = [];

    let chartUrl:
      string | null = null;

    let toolRounds = 0;

    while (true) {
      if (
        response.status !== "completed"
      ) {
        const details =
          response.error
          ?? response.incomplete_details;

        throw new Error(
          "OpenAI response did not complete successfully: "
          + JSON.stringify(
            details ?? response.status,
          ),
        );
      }

      const functionCalls =
        response.output.filter(
          (
            item,
          ): item is OpenAI.Responses.ResponseFunctionToolCall =>
            item.type === "function_call",
        );

      if (
        functionCalls.length === 0
      ) {
        const answer =
          response.output_text.trim();

        if (!answer) {
          throw new Error(
            "OpenAI returned no final answer.",
          );
        }

        return {
          responseId:
            response.id,

          answer,

          toolsUsed,

          tokenUsage,

          ...(chartUrl
            ? {
                chartUrl,
              }
            : {}),
        };
      }

      if (
        toolRounds >= MAX_TOOL_ROUNDS
      ) {
        throw new Error(
          `Maximum tool-calling rounds exceeded (${MAX_TOOL_ROUNDS}).`,
        );
      }

      toolRounds += 1;

      const toolOutputs =
        await Promise.all(
          functionCalls.map(
            async (call) => {
              const args =
                parseArguments(
                  call.arguments,
                );

              const result =
                await this.toolExecutor.execute(
                  call.name,
                  args,
                );

              const detectedChartUrl =
                extractChartUrl(
                  result,
                );

              if (detectedChartUrl) {
                chartUrl =
                  detectedChartUrl;
              }

              toolsUsed.push(
                call.name,
              );

              return {
                type:
                  "function_call_output" as const,

                call_id:
                  call.call_id,

                output:
                  JSON.stringify(
                    result,
                  ),
              };
            },
          ),
        );

      response =
        await this.openAI.responses.create({
          model:
            env.llmModel,

          instructions:
            SYSTEM_INSTRUCTIONS,

          previous_response_id:
            response.id,

          input:
            toolOutputs,

          tools: [
            ...TOOL_DEFINITIONS,
          ],
        });

      addResponseUsage(
        tokenUsage,
        response,
      );
    }
  }
}