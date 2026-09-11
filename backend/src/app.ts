import cors from "cors";
import express from "express";

import { env } from "./config/env.js";

import {
  createChartRouter,
} from "./routes/chartRoutes.js";

import {
  createChatRouter,
} from "./routes/chatRoutes.js";

import {
  dataAnalysisRouter,
} from "./routes/dataAnalysisRoutes.js";


export const app =
  express();


app.disable(
  "x-powered-by",
);

app.use(
  cors(),
);

app.use(
  express.json(),
);


app.get(
  "/",
  (_request, response) => {
    response.status(200).json({
      service:
        "maranello-ai-backend",

      status:
        "running",

      environment:
        env.nodeEnv,
    });
  },
);


app.get(
  "/health",
  (_request, response) => {
    response.status(200).json({
      status:
        "ok",

      service:
        "maranello-ai-backend",

      environment:
        env.nodeEnv,
    });
  },
);


app.use(
  "/api/chat",
  createChatRouter(),
);


app.use(
  "/api/charts",
  createChartRouter(),
);


app.use(
  "/api/data-analysis",
  dataAnalysisRouter,
);