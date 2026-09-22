import fs from "node:fs";
import path from "node:path";

import dotenv from "dotenv";


function findRootEnvPath(): string {
  const backendEnvPath =
    path.resolve(
      process.cwd(),
      ".env",
    );

  const projectRootEnvPath =
    path.resolve(
      process.cwd(),
      "../.env",
    );

  if (
    fs.existsSync(
      backendEnvPath,
    )
  ) {
    return backendEnvPath;
  }

  if (
    fs.existsSync(
      projectRootEnvPath,
    )
  ) {
    return projectRootEnvPath;
  }

  return backendEnvPath;
}


dotenv.config({
  path: findRootEnvPath(),
});


function getRequiredEnvironmentVariable(
  name: string,
): string {
  const value =
    process.env[name]?.trim();

  if (!value) {
    throw new Error(
      `${name} environment variable is required.`,
    );
  }

  return value;
}


function getPositiveNumber(
  name: string,
  defaultValue: string,
): number {
  const value =
    process.env[name]
    ?? defaultValue;

  const numberValue =
    Number(value);

  if (
    !Number.isFinite(numberValue)
    || numberValue <= 0
  ) {
    throw new Error(
      `Invalid ${name} environment variable: ${value}`,
    );
  }

  return numberValue;
}


function getPositiveInteger(
  name: string,
  defaultValue: string,
): number {
  const value =
    process.env[name]
    ?? defaultValue;

  const numberValue =
    Number(value);

  if (
    !Number.isInteger(numberValue)
    || numberValue <= 0
  ) {
    throw new Error(
      `Invalid ${name} environment variable: ${value}`,
    );
  }

  return numberValue;
}


function getPort(): number {
  const value =
    process.env.PORT
    ?? "3000";

  const port = Number(value);

  if (
    !Number.isInteger(port)
    || port <= 0
    || port > 65535
  ) {
    throw new Error(
      `Invalid PORT environment variable: ${value}`,
    );
  }

  return port;
}


function getLlmTemperature(): number {
  const value =
    process.env.LLM_TEMPERATURE
    ?? "0";

  const temperature =
    Number(value);

  if (
    !Number.isFinite(temperature)
    || temperature < 0
    || temperature > 2
  ) {
    throw new Error(
      `Invalid LLM_TEMPERATURE environment variable: ${value}`,
    );
  }

  return temperature;
}


function getLlmTimeoutMilliseconds(): number {
  const value =
    process.env.LLM_TIMEOUT_SECONDS
    ?? "30";

  const seconds =
    Number(value);

  if (
    !Number.isFinite(seconds)
    || seconds <= 0
  ) {
    throw new Error(
      `Invalid LLM_TIMEOUT_SECONDS environment variable: ${value}`,
    );
  }

  return seconds * 1000;
}


function getChatRateLimitWindowMilliseconds():
number {
  const minutes =
    getPositiveNumber(
      "CHAT_RATE_LIMIT_WINDOW_MINUTES",
      "15",
    );

  return minutes * 60 * 1000;
}


export const env = {
  nodeEnv:
    process.env.NODE_ENV
    ?? "development",

  port:
    getPort(),

  dataAgentUrl:
    process.env.DATA_AGENT_URL
    ?? "http://127.0.0.1:8001",

  chromaUrl:
    process.env.CHROMA_URL
    ?? "http://127.0.0.1:8000",

  chromaCollection:
    process.env.CHROMA_COLLECTION
    ?? "maranello_ai_knowledge_base",

  openAiApiKey:
    getRequiredEnvironmentVariable(
      "OPENAI_API_KEY",
    ),

  openAiEmbeddingModel:
    process.env.OPENAI_EMBEDDING_MODEL
    ?? "text-embedding-3-small",

  llmModel:
    process.env.LLM_MODEL
    ?? "gpt-5-mini",

  llmTemperature:
    getLlmTemperature(),

  llmTimeoutMilliseconds:
    getLlmTimeoutMilliseconds(),

  chatRateLimitWindowMilliseconds:
    getChatRateLimitWindowMilliseconds(),

  chatRateLimitMaxRequests:
    getPositiveInteger(
      "CHAT_RATE_LIMIT_MAX_REQUESTS",
      "30",
    ),
} as const;