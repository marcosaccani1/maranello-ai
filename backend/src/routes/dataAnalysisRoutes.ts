import { Router } from "express";

import { analyzeData } from "../controllers/dataAnalysisController.js";


export const dataAnalysisRouter = Router();

dataAnalysisRouter.post(
  "/",
  analyzeData,
);