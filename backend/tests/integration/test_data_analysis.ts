import request from "supertest";
import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import { app } from "../../src/app.js";


describe("POST /api/data-analysis", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("returns Data Agent analysis results", async () => {
    vi.spyOn(
      globalThis,
      "fetch",
    ).mockResolvedValue(
      new Response(
        JSON.stringify({
          success: true,
          result: {
            analysis_type: "grouped_defect_rate",
            summary: (
              "The highest defect rate by supplier_id "
              + "is SUP-07 at 2.99%."
            ),
            data: [
              {
                group: "SUP-07",
                total_production: 13266,
                total_defective_units: 396,
                defect_rate: 2.99,
              },
            ],
            chart_url: null,
          },
          error: null,
        }),
        {
          status: 200,
          headers: {
            "Content-Type": "application/json",
          },
        },
      ),
    );

    const response = await request(app)
      .post("/api/data-analysis")
      .send({
        question: (
          "Which supplier has the highest defect rate?"
        ),
      })
      .expect(200);

    expect(response.body.success).toBe(true);

    expect(
      response.body.result.analysis_type,
    ).toBe("grouped_defect_rate");

    expect(
      response.body.result.data[0].group,
    ).toBe("SUP-07");
  });

  it("rejects a missing question", async () => {
    const response = await request(app)
      .post("/api/data-analysis")
      .send({})
      .expect(400);

    expect(response.body).toEqual({
      success: false,
      error: "Question is required.",
    });
  });

  it("rejects an empty question", async () => {
    const response = await request(app)
      .post("/api/data-analysis")
      .send({
        question: "   ",
      })
      .expect(400);

    expect(response.body).toEqual({
      success: false,
      error: "Question is required.",
    });
  });

  it("returns 502 when the Data Agent is unavailable", async () => {
    vi.spyOn(
      globalThis,
      "fetch",
    ).mockRejectedValue(
      new Error("Connection refused"),
    );

    const response = await request(app)
      .post("/api/data-analysis")
      .send({
        question: "What is the defect rate?",
      })
      .expect(502);

    expect(response.body.success).toBe(false);

    expect(response.body.error).toBe(
      "Unable to connect to the Data Agent.",
    );
  });
});