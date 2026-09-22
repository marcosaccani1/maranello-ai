import { env } from "../config/env.js";
import type {
  DataAgentRequest,
  DataAgentResponse,
} from "../models/dataAgent.js";

import {
  fetchWithRetry,
} from "./fetchWithRetry.js";


export class DataAgentClient {
  constructor(
    private readonly baseUrl: string = env.dataAgentUrl,
  ) {}

  async analyze(
    question: string,
  ): Promise<DataAgentResponse> {
    const payload: DataAgentRequest = {
      question,
    };

    let response: Response;

    try {
      response = await fetchWithRetry(
        `${this.baseUrl}/api/analysis`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        },
      );
    } catch (error) {
      throw new Error(
        "Unable to connect to the Data Agent.",
        {
          cause: error,
        },
      );
    }

    if (!response.ok) {
      const detail = await this.readErrorDetail(
        response,
      );

      throw new Error(
        `Data Agent request failed with status `
        + `${response.status}: ${detail}`,
      );
    }

    const data = (
      await response.json()
    ) as DataAgentResponse;

    return data;
  }

  private async readErrorDetail(
    response: Response,
  ): Promise<string> {
    try {
      const payload = (
        await response.json()
      ) as {
        detail?: unknown;
      };

      if (
        typeof payload.detail === "string"
        && payload.detail.length > 0
      ) {
        return payload.detail;
      }

      return response.statusText || "Unknown error";
    } catch {
      return response.statusText || "Unknown error";
    }
  }
}