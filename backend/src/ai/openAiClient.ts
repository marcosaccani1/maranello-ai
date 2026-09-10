import OpenAI from "openai";

import { env } from "../config/env.js";


export interface OpenAIResponsesProvider {
  responses: OpenAI["responses"];
}


export class OpenAIClient {
  private readonly client: OpenAI;


  constructor(
    apiKey: string = env.openAiApiKey,
    timeout: number =
      env.llmTimeoutMilliseconds,
  ) {
    if (!apiKey.trim()) {
      throw new Error(
        "OPENAI_API_KEY is required to use the LLM.",
      );
    }

    this.client = new OpenAI({
      apiKey,
      timeout,
    });
  }


  get responses(): OpenAI["responses"] {
    return this.client.responses;
  }
}