import express from "express";

import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  createChartRouter,
} from "../../src/routes/chartRoutes.js";


describe(
  "GET /api/charts/:filename",
  () => {
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

        const chartProvider = {
          getChart:
            vi.fn()
              .mockResolvedValue({
                contentType:
                  "image/png",

                data:
                  pngBytes.buffer,
              }),
        };

        const app =
          express();

        app.use(
          "/api/charts",
          createChartRouter(
            chartProvider,
          ),
        );

        const server =
          app.listen(0);

        try {
          const address =
            server.address();

          if (
            !address
            || typeof address === "string"
          ) {
            throw new Error(
              "Expected server address.",
            );
          }

          const response =
            await fetch(
              `http://127.0.0.1:${address.port}/api/charts/test.png`,
            );

          expect(
            response.status,
          ).toBe(200);

          expect(
            response.headers.get(
              "content-type",
            ),
          ).toContain(
            "image/png",
          );

          expect(
            chartProvider.getChart,
          ).toHaveBeenCalledWith(
            "test.png",
          );

          const result =
            new Uint8Array(
              await response.arrayBuffer(),
            );

          expect(
            Array.from(result),
          ).toEqual(
            Array.from(
              pngBytes,
            ),
          );
        } finally {
          server.close();
        }
      },
    );


    it(
      "returns an error when the chart provider rejects the filename",
      async () => {
        const chartProvider = {
          getChart:
            vi.fn()
              .mockRejectedValue(
                new Error(
                  "Invalid chart filename.",
                ),
              ),
        };

        const app =
          express();

        app.use(
          "/api/charts",
          createChartRouter(
            chartProvider,
          ),
        );

        const server =
          app.listen(0);

        try {
          const address =
            server.address();

          if (
            !address
            || typeof address === "string"
          ) {
            throw new Error(
              "Expected server address.",
            );
          }

          const response =
            await fetch(
              `http://127.0.0.1:${address.port}/api/charts/invalid.png`,
            );

          expect(
            response.status,
          ).toBe(400);

          expect(
            await response.json(),
          ).toEqual({
            error:
              "Invalid chart filename.",
          });
        } finally {
          server.close();
        }
      },
    );
  },
);