import { app } from "./app.js";
import { env } from "./config/env.js";

const server = app.listen(env.port, () => {
  console.log(
    `Maranello AI backend running on http://localhost:${env.port}`,
  );
});

function shutdown(signal: string): void {
  console.log(`${signal} received. Shutting down.`);

  server.close((error) => {
    if (error) {
      console.error("Failed to close HTTP server.", error);
      process.exit(1);
    }

    process.exit(0);
  });
}

process.on("SIGTERM", () => {
  shutdown("SIGTERM");
});

process.on("SIGINT", () => {
  shutdown("SIGINT");
});