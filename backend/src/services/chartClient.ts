import { env } from "../config/env.js";

import {
  fetchWithRetry,
} from "./fetchWithRetry.js";


export interface ChartFile {
  contentType: string;
  data: ArrayBuffer;
}


export class ChartClient {
  constructor(
    private readonly baseUrl:
    string = env.dataAgentUrl,
  ) {}


  async getChart(
    filename: string,
  ): Promise<ChartFile> {
    const normalizedFilename =
      filename.trim();

    if (!normalizedFilename) {
      throw new Error(
        "Chart filename must be non-empty.",
      );
    }

    if (
      normalizedFilename.includes("/")
      || normalizedFilename.includes("\\")
      || normalizedFilename.includes("..")
    ) {
      throw new Error(
        "Invalid chart filename.",
      );
    }

    let response: Response;

    try {
      response =
        await fetchWithRetry(
          `${this.baseUrl}/charts/${encodeURIComponent(
            normalizedFilename,
          )}`,
        );
    } catch (error) {
      throw new Error(
        "Unable to connect to the Data Agent chart service.",
        {
          cause: error,
        },
      );
    }

    if (!response.ok) {
      throw new Error(
        `Chart request failed with status ${response.status}.`,
      );
    }

    const contentType =
      response.headers.get(
        "content-type",
      )
      ?? "image/png";

    const data =
      await response.arrayBuffer();

    return {
      contentType,
      data,
    };
  }
}