import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  ChartClient,
} from "../../src/services/chartClient.js";


describe("ChartClient", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });


  it(
    "returns a chart image",
    async () => {
      const pngBytes =
        new Uint8Array([
          137,
          80,
          78,
          71,
        ]);

      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockResolvedValue(
            new Response(
              pngBytes,
              {
                status: 200,
                headers: {
                  "Content-Type":
                    "image/png",
                },
              },
            ),
          );

      const client =
        new ChartClient(
          "http://data-agent.test",
        );

      const chart =
        await client.getChart(
          "monthly_defect_rate_test.png",
        );

      expect(
        chart.contentType,
      ).toBe(
        "image/png",
      );

      expect(
        Array.from(
          new Uint8Array(
            chart.data,
          ),
        ),
      ).toEqual(
        Array.from(
          pngBytes,
        ),
      );

      expect(
        fetchMock,
      ).toHaveBeenCalledOnce();

      expect(
        fetchMock,
      ).toHaveBeenCalledWith(
        "http://data-agent.test/charts/monthly_defect_rate_test.png",
        expect.objectContaining({
          signal:
            expect.any(
              AbortSignal,
            ),
        }),
      );
    },
  );


  it(
    "does not retry a client error",
    async () => {
      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockResolvedValue(
            new Response(
              "Not found",
              {
                status: 404,
                statusText:
                  "Not Found",
              },
            ),
          );

      const client =
        new ChartClient(
          "http://data-agent.test",
        );

      await expect(
        client.getChart(
          "missing.png",
        ),
      ).rejects.toThrow(
        "Chart request failed with status 404.",
      );

      expect(
        fetchMock,
      ).toHaveBeenCalledOnce();
    },
  );


  it(
    "retries transient server errors and returns a later chart",
    async () => {
      vi.useFakeTimers();

      const pngBytes =
        new Uint8Array([
          137,
          80,
          78,
          71,
        ]);

      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockResolvedValueOnce(
            new Response(
              "Unavailable",
              {
                status: 503,
              },
            ),
          )
          .mockResolvedValueOnce(
            new Response(
              "Unavailable",
              {
                status: 503,
              },
            ),
          )
          .mockResolvedValueOnce(
            new Response(
              pngBytes,
              {
                status: 200,
                headers: {
                  "Content-Type":
                    "image/png",
                },
              },
            ),
          );

      const client =
        new ChartClient(
          "http://data-agent.test",
        );

      const requestPromise =
        client.getChart(
          "monthly_defect_rate_test.png",
        );

      await vi.runAllTimersAsync();

      const chart =
        await requestPromise;

      expect(
        chart.contentType,
      ).toBe(
        "image/png",
      );

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(3);
    },
  );


  it(
    "retries network failures and reports the chart service as unreachable",
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
        new ChartClient(
          "http://data-agent.test",
        );

      const requestPromise =
        client.getChart(
          "monthly_defect_rate_test.png",
        );

      const expectation =
        expect(
          requestPromise,
        ).rejects.toThrow(
          "Unable to connect to the Data Agent chart service.",
        );

      await vi.runAllTimersAsync();

      await expectation;

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(3);
    },
  );


  it(
    "rejects an empty chart filename without making a request",
    async () => {
      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        );

      const client =
        new ChartClient(
          "http://data-agent.test",
        );

      await expect(
        client.getChart(
          "   ",
        ),
      ).rejects.toThrow(
        "Chart filename must be non-empty.",
      );

      expect(
        fetchMock,
      ).not.toHaveBeenCalled();
    },
  );


  it(
    "rejects unsafe chart filenames without making a request",
    async () => {
      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        );

      const client =
        new ChartClient(
          "http://data-agent.test",
        );

      const unsafeFilenames = [
        "../secret.png",
        "folder/chart.png",
        "folder\\chart.png",
      ];

      for (
        const filename
        of unsafeFilenames
      ) {
        await expect(
          client.getChart(
            filename,
          ),
        ).rejects.toThrow(
          "Invalid chart filename.",
        );
      }

      expect(
        fetchMock,
      ).not.toHaveBeenCalled();
    },
  );
});