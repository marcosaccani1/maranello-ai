import {
  rateLimit,
} from "express-rate-limit";

import { env } from "../config/env.js";


export interface ChatRateLimiterOptions {
  windowMs?: number;
  limit?: number;
}


export function createChatRateLimiter(
  options: ChatRateLimiterOptions = {},
) {
  return rateLimit({
    windowMs:
      options.windowMs
      ?? env.chatRateLimitWindowMilliseconds,

    limit:
      options.limit
      ?? env.chatRateLimitMaxRequests,

    standardHeaders:
      "draft-8",

    legacyHeaders:
      false,

    message: {
      error:
        "Too many chat requests. Please try again later.",
    },
  });
}