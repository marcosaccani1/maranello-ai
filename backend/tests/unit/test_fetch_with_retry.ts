import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  fetchWithRetry,
} from "../../src/services/fetchWithRetry.js";


describe("fetchWithRetry", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });


  it(
    "returns immediately after a successful response",
    async () => {
      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockResolvedValue(
            new Response(
              "ok",
              {
                status: 200,
              },
            ),
          );

      const response =
        await fetchWithRetry(
          "http://service.test",
          undefined,
          {
            timeoutMilliseconds: 1000,
            initialBackoffMilliseconds: 0,
          },
        );

      expect(
        response.status,
      ).toBe(200);

      expect(
        fetchMock,
      ).toHaveBeenCalledOnce();

      const requestInit =
        fetchMock.mock.calls[0]?.[1];

      expect(
        requestInit?.signal,
      ).toBeInstanceOf(
        AbortSignal,
      );
    },
  );


  it(
    "retries a server error and returns a later successful response",
    async () => {
      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockResolvedValueOnce(
            new Response(
              "temporary failure",
              {
                status: 503,
              },
            ),
          )
          .mockResolvedValueOnce(
            new Response(
              "ok",
              {
                status: 200,
              },
            ),
          );

      const response =
        await fetchWithRetry(
          "http://service.test",
          undefined,
          {
            timeoutMilliseconds: 1000,
            initialBackoffMilliseconds: 0,
          },
        );

      expect(
        response.status,
      ).toBe(200);

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(2);

      const firstSignal =
        fetchMock.mock.calls[0]?.[1]?.signal;

      const secondSignal =
        fetchMock.mock.calls[1]?.[1]?.signal;

      expect(
        firstSignal,
      ).toBeInstanceOf(
        AbortSignal,
      );

      expect(
        secondSignal,
      ).toBeInstanceOf(
        AbortSignal,
      );

      expect(
        firstSignal,
      ).not.toBe(
        secondSignal,
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
              "bad request",
              {
                status: 400,
              },
            ),
          );

      const response =
        await fetchWithRetry(
          "http://service.test",
          undefined,
          {
            timeoutMilliseconds: 1000,
            initialBackoffMilliseconds: 0,
          },
        );

      expect(
        response.status,
      ).toBe(400);

      expect(
        fetchMock,
      ).toHaveBeenCalledOnce();
    },
  );


  it(
    "retries a network error",
    async () => {
      const networkError =
        new Error(
          "Connection refused",
        );

      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockRejectedValueOnce(
            networkError,
          )
          .mockResolvedValueOnce(
            new Response(
              "ok",
              {
                status: 200,
              },
            ),
          );

      const response =
        await fetchWithRetry(
          "http://service.test",
          undefined,
          {
            timeoutMilliseconds: 1000,
            initialBackoffMilliseconds: 0,
          },
        );

      expect(
        response.status,
      ).toBe(200);

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(2);
    },
  );


  it(
    "throws the last network error after all attempts fail",
    async () => {
      const networkError =
        new Error(
          "Connection refused",
        );

      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockRejectedValue(
            networkError,
          );

      await expect(
        fetchWithRetry(
          "http://service.test",
          undefined,
          {
            timeoutMilliseconds: 1000,
            maxAttempts: 3,
            initialBackoffMilliseconds: 0,
          },
        ),
      ).rejects.toBe(
        networkError,
      );

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(3);
    },
  );


  it(
    "returns the final server error after exhausting retries",
    async () => {
      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockResolvedValue(
            new Response(
              "unavailable",
              {
                status: 503,
              },
            ),
          );

      const response =
        await fetchWithRetry(
          "http://service.test",
          undefined,
          {
            timeoutMilliseconds: 1000,
            maxAttempts: 3,
            initialBackoffMilliseconds: 0,
          },
        );

      expect(
        response.status,
      ).toBe(503);

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(3);
    },
  );


  it(
    "aborts timed-out attempts and retries them",
    async () => {
      vi.useFakeTimers();

      const receivedSignals:
        AbortSignal[] = [];

      const fetchMock =
        vi.spyOn(
          globalThis,
          "fetch",
        )
          .mockImplementation(
            (
              _input,
              init,
            ) => {
              const signal =
                init?.signal;

              if (
                !(signal instanceof AbortSignal)
              ) {
                return Promise.reject(
                  new Error(
                    "Expected an AbortSignal.",
                  ),
                );
              }

              receivedSignals.push(
                signal,
              );

              return new Promise<Response>(
                (
                  _resolve,
                  reject,
                ) => {
                  signal.addEventListener(
                    "abort",
                    () => {
                      reject(
                        new DOMException(
                          "The operation was aborted.",
                          "AbortError",
                        ),
                      );
                    },
                    {
                      once: true,
                    },
                  );
                },
              );
            },
          );

      const requestPromise =
        fetchWithRetry(
          "http://service.test",
          undefined,
          {
            timeoutMilliseconds: 100,
            maxAttempts: 3,
            initialBackoffMilliseconds: 0,
          },
        );

      const expectation =
        expect(
          requestPromise,
        ).rejects.toMatchObject({
          name: "AbortError",
        });

      await vi.runAllTimersAsync();

      await expectation;

      expect(
        fetchMock,
      ).toHaveBeenCalledTimes(3);

      expect(
        receivedSignals,
      ).toHaveLength(3);

      expect(
        receivedSignals.every(
          (signal) =>
            signal.aborted,
        ),
      ).toBe(true);

      expect(
        new Set(
          receivedSignals,
        ).size,
      ).toBe(3);
    },
  );


  it(
    "rejects invalid retry configuration",
    async () => {
      await expect(
        fetchWithRetry(
          "http://service.test",
          undefined,
          {
            timeoutMilliseconds: 0,
          },
        ),
      ).rejects.toThrow(
        "timeoutMilliseconds must be a positive integer.",
      );

      await expect(
        fetchWithRetry(
          "http://service.test",
          undefined,
          {
            maxAttempts: 0,
          },
        ),
      ).rejects.toThrow(
        "maxAttempts must be a positive integer.",
      );

      await expect(
        fetchWithRetry(
          "http://service.test",
          undefined,
          {
            initialBackoffMilliseconds: -1,
          },
        ),
      ).rejects.toThrow(
        "initialBackoffMilliseconds must be a non-negative integer.",
      );
    },
  );
});