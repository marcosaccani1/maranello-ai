import request from "supertest";
import { describe, expect, it } from "vitest";

import { app } from "../../src/app.js";


describe("Backend health endpoints", () => {
  it("returns the backend health status", async () => {
    const response = await request(app)
      .get("/health")
      .expect(200);

    expect(response.body).toEqual({
      status: "ok",
      service: "maranello-ai-backend",
      environment: "test",
    });
  });

  it("returns the backend root status", async () => {
    const response = await request(app)
      .get("/")
      .expect(200);

    expect(response.body).toEqual({
      service: "maranello-ai-backend",
      status: "running",
      environment: "test",
    });
  });
});