import { IngestionService } from "./ingestionService.js";


async function main(): Promise<void> {
  console.log(
    "Starting Maranello AI Knowledge Base ingestion...",
  );

  try {
    const ingestionService =
      new IngestionService();

    const result =
      await ingestionService.ingest();

    console.log(
      "Knowledge Base ingestion completed successfully.",
    );

    console.log(
      `Documents loaded: ${result.documentsLoaded}`,
    );

    console.log(
      `Chunks indexed: ${result.chunksIndexed}`,
    );

    console.log(
      `ChromaDB collection: ${result.collectionName}`,
    );
  } catch (error: unknown) {
    console.error(
      "Knowledge Base ingestion failed.",
    );

    if (error instanceof Error) {
      console.error(
        error.message,
      );
    } else {
      console.error(
        "Unknown ingestion error.",
      );
    }

    process.exitCode = 1;
  }
}


await main();