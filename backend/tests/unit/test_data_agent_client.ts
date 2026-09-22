import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import { DataAgentClient } from "../../src/services/dataAgentClient.js";


describe("DataAgentClient", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });


  it(
    "returns a successful Data Agent response",
    async () => {
      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        );

      fetchMock.mockResolvedValue(
        new Response(
          JSON.stringify({
            success: true,
            result: {
              analysis_type:
                "global_kpis",
              summary:
                "Analysis completed.",
              data: {
                defect_rate: 2.0,
              },
              chart_url: null,
            },
            error: null,
          }),
          {
            status: 200,
            headers: {
              "Content-Type":
                "application/json",
            },
          },
        ),
      );

      const client =
        new DataAgentClient(
          "http://data-agent.test",
        );

      const response =
        await client.analyze(
          "What is the defect rate?",
        );

      expect(
        response.success,
      ).toBe(true);

      expect(
        response.result?.analysis_type,
      ).toBe(
        "global_kpis",
      );

      expect(
        fetchMock,
      ).toHaveBeenCalledOnce();

      expect(
        fetchMock,
      ).toHaveBeenCalledWith(
        "http://data-agent.test/api/analysis",
        expect.objectContaining({
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            question:
              "What is the defect rate?",
          }),
          signal:
            expect.any(
              AbortSignal,
            ),
        }),
      );
    },
  );


  it(
    "does not retry when the Data Agent returns a client error",
    async () => {
      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockResolvedValue(
            new Response(
              JSON.stringify({
                detail:
                  "Unsupported analysis request.",
              }),
              {
                status: 400,
                statusText:
                  "Bad Request",
                headers: {
                  "Content-Type":
                    "application/json",
                },
              },
            ),
          );

      const client =
        new DataAgentClient(
          "http://data-agent.test",
        );

      await expect(
        client.analyze(
          "Unsupported question",
        ),
      ).rejects.toThrow(
        "Data Agent request failed with status 400: "
        + "Unsupported analysis request.",
      );

      expect(
        fetchMock,
      ).toHaveBeenCalledOnce();
    },
  );


  it(
    "retries transient server errors and returns a later successful response",
    async () => {
      vi.useFakeTimers();

      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockResolvedValueOnce(
            new Response(
              JSON.stringify({
                detail:
                  "Temporarily unavailable.",
              }),
              {
                status: 503,
                statusText:
                  "Service Unavailable",
                headers: {
                  "Content-Type":
                    "application/json",
                },
              },
            ),
          )
          .mockResolvedValueOnce(
            new Response(
              JSON.stringify({
                detail:
                  "Temporarily unavailable.",
              }),
              {
                status: 503,
                statusText:
                  "Service Unavailable",
                headers: {
                  "Content-Type":
                    "application/json",
                },
              },
            ),
          )
          .mockResolvedValueOnce(
            new Response(
              JSON.stringify({
                success: true,
                result: {
                  analysis_type:
                    "global_kpis",
                  summary:
                    "Analysis completed.",
                  data: {
                    defect_rate: 2.0,
                  },
                  chart_url: null,
                },
                error: null,
              }),
              {
                status: 200,
                headers: {
                  "Content-Type":
                    "application/json",
                },
              },
            ),
          );

      const client =
        new DataAgentClient(
          "http://data-agent.test",
        );

      const requestPromise =
        client.analyze(
          "What is the defect rate?",
        );

      await vi.runAllTimersAsync();

      const response =
        await requestPromise;

      expect(
        response.success,
      ).toBe(true);

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(3);
    },
  );


  it(
    "retries network failures and reports the Data Agent as unreachable",
    async () => {
      vi.useFakeTimers();

      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockRejectedValue(
            new Error(
              "Connection refused",
            ),
          );

      const client =
        new DataAgentClient(
          "http://data-agent.test",
        );

      const requestPromise =
        client.analyze(
          "What is the defect rate?",
        );

      const expectation =
        expect(
          requestPromise,
        ).rejects.toThrow(
          "Unable to connect to the Data Agent.",
        );

      await vi.runAllTimersAsync();

      await expectation;

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(3);
    },
  );
});