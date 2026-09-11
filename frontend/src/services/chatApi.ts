import type {
  ChatApiRequest,
  ChatApiResponse,
} from "../types/chat";


const API_BASE_URL = (
  import.meta.env.VITE_API_URL
  ?? "http://127.0.0.1:3000"
).replace(
  /\/+$/,
  "",
);


export function resolveApiUrl(
  path: string,
): string {
  const normalizedPath =
    path.trim();

  if (
    normalizedPath.startsWith(
      "http://",
    )
    || normalizedPath.startsWith(
      "https://",
    )
  ) {
    return normalizedPath;
  }

  if (
    normalizedPath.startsWith(
      "/",
    )
  ) {
    return `${API_BASE_URL}${normalizedPath}`;
  }

  return `${API_BASE_URL}/${normalizedPath}`;
}


export async function sendChatMessage(
  request: ChatApiRequest,
): Promise<ChatApiResponse> {
  let response: Response;

  try {
    response =
      await fetch(
        resolveApiUrl(
          "/api/chat",
        ),
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body:
            JSON.stringify(
              request,
            ),
        },
      );
  } catch (error) {
    throw new Error(
      "Unable to connect to the Maranello AI backend.",
      {
        cause: error,
      },
    );
  }


  if (!response.ok) {
    const message =
      await readErrorMessage(
        response,
      );

    throw new Error(
      `Chat request failed with status ${response.status}: ${message}`,
    );
  }


  const payload =
    await response.json();

  return payload as ChatApiResponse;
}


async function readErrorMessage(
  response: Response,
): Promise<string> {
  try {
    const payload =
      await response.json() as {
        error?: unknown;
      };

    if (
      typeof payload.error === "string"
      && payload.error.trim()
    ) {
      return payload.error;
    }
  } catch {
    // Fall back to the HTTP status text.
  }

  return response.statusText
    || "Unknown error";
}