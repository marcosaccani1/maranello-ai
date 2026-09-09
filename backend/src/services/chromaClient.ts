import { OpenAIEmbeddingFunction } from "@chroma-core/openai";
import { ChromaClient } from "chromadb";

import { env } from "../config/env.js";


function parseChromaUrl(url: string): {
  host: string;
  port: number;
  ssl: boolean;
} {
  const parsedUrl = new URL(url);

  const ssl = parsedUrl.protocol === "https:";

  if (
    parsedUrl.protocol !== "http:"
    && parsedUrl.protocol !== "https:"
  ) {
    throw new Error(
      `Unsupported Chroma protocol: ${parsedUrl.protocol}`,
    );
  }

  const defaultPort = ssl ? 443 : 80;

  const port = parsedUrl.port
    ? Number(parsedUrl.port)
    : defaultPort;

  return {
    host: parsedUrl.hostname,
    port,
    ssl,
  };
}


function createEmbeddingFunction(): OpenAIEmbeddingFunction {
  if (!env.openAiApiKey) {
    throw new Error(
      "OPENAI_API_KEY is required to use OpenAI embeddings.",
    );
  }

  return new OpenAIEmbeddingFunction({
    apiKey: env.openAiApiKey,
    modelName: env.openAiEmbeddingModel,
  });
}


export class MaranelloChromaClient {
  private readonly client: ChromaClient;

  private readonly embeddingFunction =
    createEmbeddingFunction();

  constructor(
    baseUrl: string = env.chromaUrl,
  ) {
    const connection =
      parseChromaUrl(baseUrl);

    this.client = new ChromaClient({
      host: connection.host,
      port: connection.port,
      ssl: connection.ssl,
    });
  }

  async heartbeat(): Promise<number> {
    return this.client.heartbeat();
  }

  async getOrCreateKnowledgeCollection() {
    return this.client.getOrCreateCollection({
      name: env.chromaCollection,
      embeddingFunction:
        this.embeddingFunction,
    });
  }
}