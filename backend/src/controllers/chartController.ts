import type {
  NextFunction,
  Request,
  Response,
} from "express";

import type {
  ChartFile,
} from "../services/chartClient.js";


export interface ChartProvider {
  getChart(
    filename: string,
  ): Promise<ChartFile>;
}


export function createChartController(
  chartProvider: ChartProvider,
) {
  return async function chartController(
    request: Request,
    response: Response,
    next: NextFunction,
  ): Promise<void> {
    try {
      const filename =
        request.params.filename;

      if (
        typeof filename !== "string"
        || !filename.trim()
      ) {
        response.status(400).json({
          error:
            "Chart filename is required.",
        });

        return;
      }

      const chart =
        await chartProvider.getChart(
          filename,
        );

      response.setHeader(
        "Content-Type",
        chart.contentType,
      );

      response.setHeader(
        "Cache-Control",
        "private, max-age=3600",
      );

      response.status(200).send(
        Buffer.from(
          chart.data,
        ),
      );
    } catch (error) {
      if (
        error instanceof Error
        && (
          error.message ===
            "Chart filename must be non-empty."
          || error.message ===
            "Invalid chart filename."
        )
      ) {
        response.status(400).json({
          error:
            error.message,
        });

        return;
      }

      next(error);
    }
  };
}