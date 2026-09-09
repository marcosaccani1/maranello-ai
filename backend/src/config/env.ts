import path from "node:path";
import { fileURLToPath } from "node:url";

import dotenv from "dotenv";


const currentFilePath =
  fileURLToPath(import.meta.url);

const currentDirectory =
  path.dirname(currentFilePath);

const rootEnvPath =
  path.resolve(
    currentDirectory,
    "../../../.env",
  );


dotenv.config({
  path: rootEnvPath,
});


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


export const env = {
  nodeEnv:
    process.env.NODE_ENV
    ?? "development",

  port: getPort(),

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
    process.env.OPENAI_API_KEY
    ?? "",

  openAiEmbeddingModel:
    process.env.OPENAI_EMBEDDING_MODEL
    ?? "text-embedding-3-small",
} as const;