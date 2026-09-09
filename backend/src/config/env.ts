import dotenv from "dotenv";

dotenv.config();

function getPort(): number {
  const value = process.env.PORT ?? "3000";
  const port = Number(value);

  if (!Number.isInteger(port) || port <= 0 || port > 65535) {
    throw new Error(
      `Invalid PORT environment variable: ${value}`,
    );
  }

  return port;
}

export const env = {
  nodeEnv: process.env.NODE_ENV ?? "development",
  port: getPort(),
  dataAgentUrl:
    process.env.DATA_AGENT_URL ?? "http://127.0.0.1:8001",
} as const;