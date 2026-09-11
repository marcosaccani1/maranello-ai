import {
  Router,
} from "express";

import {
  createChartController,
} from "../controllers/chartController.js";

import type {
  ChartProvider,
} from "../controllers/chartController.js";

import {
  ChartClient,
} from "../services/chartClient.js";


export function createChartRouter(
  providedChartProvider?:
  ChartProvider,
): Router {
  const router =
    Router();

  const chartProvider =
    providedChartProvider
    ?? new ChartClient();

  router.get(
    "/:filename",
    (request, response, next) => {
      const controller =
        createChartController(
          chartProvider,
        );

      void controller(
        request,
        response,
        next,
      );
    },
  );

  return router;
}