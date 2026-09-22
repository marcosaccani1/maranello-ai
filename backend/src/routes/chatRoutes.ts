import type {
  RequestHandler,
} from "express";

import {
  Router,
} from "express";

import {
  createChatController,
} from "../controllers/chatController.js";

import type {
  ChatServiceProvider,
} from "../controllers/chatController.js";

import {
  createChatObservabilityMiddleware,
} from "../middleware/chatObservability.js";

import type {
  ChatLogWriter,
} from "../middleware/chatObservability.js";

import {
  createChatRateLimiter,
} from "../middleware/chatRateLimiter.js";

import {
  ChatService,
} from "../services/chatService.js";


export function createChatRouter(
  providedChatService?:
  ChatServiceProvider,

  providedRateLimiter?:
  RequestHandler,

  providedLogWriter?:
  ChatLogWriter,
): Router {
  const router =
    Router();

  let chatService =
    providedChatService;

  const observabilityMiddleware =
    createChatObservabilityMiddleware(
      providedLogWriter,
    );

  const rateLimiter =
    providedRateLimiter
    ?? createChatRateLimiter();


  function getChatService():
  ChatServiceProvider {
    if (!chatService) {
      chatService =
        new ChatService();
    }

    return chatService;
  }


  router.post(
    "/",
    observabilityMiddleware,
    rateLimiter,
    (request, response, next) => {
      const controller =
        createChatController(
          getChatService(),
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