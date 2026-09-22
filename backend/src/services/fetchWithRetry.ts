export interface FetchWithRetryOptions {
  timeoutMilliseconds?: number;
  maxAttempts?: number;
  initialBackoffMilliseconds?: number;
}


const DEFAULT_TIMEOUT_MILLISECONDS =
  10_000;

const DEFAULT_MAX_ATTEMPTS =
  3;

const DEFAULT_INITIAL_BACKOFF_MILLISECONDS =
  200;


function validatePositiveInteger(
  value: number,
  name: string,
): void {
  if (
    !Number.isInteger(value)
    || value <= 0
  ) {
    throw new Error(
      `${name} must be a positive integer.`,
    );
  }
}


function validateNonNegativeInteger(
  value: number,
  name: string,
): void {
  if (
    !Number.isInteger(value)
    || value < 0
  ) {
    throw new Error(
      `${name} must be a non-negative integer.`,
    );
  }
}


function isRetryableStatus(
  status: number,
): boolean {
  return (
    status >= 500
    && status <= 599
  );
}


function wait(
  milliseconds: number,
): Promise<void> {
  return new Promise(
    (resolve) => {
      setTimeout(
        resolve,
        milliseconds,
      );
    },
  );
}


export async function fetchWithRetry(
  input: string | URL,
  init?: RequestInit,
  options: FetchWithRetryOptions = {},
): Promise<Response> {
  const timeoutMilliseconds =
    options.timeoutMilliseconds
    ?? DEFAULT_TIMEOUT_MILLISECONDS;

  const maxAttempts =
    options.maxAttempts
    ?? DEFAULT_MAX_ATTEMPTS;

  const initialBackoffMilliseconds =
    options.initialBackoffMilliseconds
    ?? DEFAULT_INITIAL_BACKOFF_MILLISECONDS;

  validatePositiveInteger(
    timeoutMilliseconds,
    "timeoutMilliseconds",
  );

  validatePositiveInteger(
    maxAttempts,
    "maxAttempts",
  );

  validateNonNegativeInteger(
    initialBackoffMilliseconds,
    "initialBackoffMilliseconds",
  );

  let lastError: unknown;

  for (
    let attempt = 1;
    attempt <= maxAttempts;
    attempt += 1
  ) {
    const controller =
      new AbortController();

    const timeout =
      setTimeout(
        () => {
          controller.abort();
        },
        timeoutMilliseconds,
      );

    try {
      const response =
        await fetch(
          input,
          {
            ...init,
            signal:
              controller.signal,
          },
        );

      if (
        !isRetryableStatus(
          response.status,
        )
        || attempt === maxAttempts
      ) {
        return response;
      }
    } catch (error) {
      lastError = error;

      if (
        attempt === maxAttempts
      ) {
        throw error;
      }
    } finally {
      clearTimeout(
        timeout,
      );
    }

    const backoffMilliseconds =
      initialBackoffMilliseconds
      * (2 ** (attempt - 1));

    if (
      backoffMilliseconds > 0
    ) {
      await wait(
        backoffMilliseconds,
      );
    }
  }

  throw (
    lastError
    ?? new Error(
      "HTTP request failed after all retry attempts.",
    )
  );
}