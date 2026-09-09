import type {
  Request,
  Response,
} from "express";

import { DataAgentClient } from "../services/dataAgentClient.js";


const dataAgentClient = new DataAgentClient();


export async function analyzeData(
  request: Request,
  response: Response,
): Promise<void> {
  const question = request.body?.question;

  if (
    typeof question !== "string"
    || question.trim().length === 0
  ) {
    response.status(400).json({
      success: false,
      error: "Question is required.",
    });

    return;
  }

  try {
    const result = await dataAgentClient.analyze(
      question.trim(),
    );

    response.status(200).json(result);
  } catch (error) {
    const message = (
      error instanceof Error
        ? error.message
        : "Unknown Data Agent error."
    );

    response.status(502).json({
      success: false,
      error: message,
    });
  }
}