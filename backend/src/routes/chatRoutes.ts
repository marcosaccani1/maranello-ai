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
  ChatService,
} from "../services/chatService.js";


export function createChatRouter(
  providedChatService?:
  ChatServiceProvider,
): Router {
  const router =
    Router();

  let chatService =
    providedChatService;


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