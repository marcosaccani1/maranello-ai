import { MaranelloChromaClient } from "../services/chromaClient.js";

import type {
  RetrievedKnowledgeChunk,
} from "./types.js";


interface QueryMetadata {
  source?: unknown;
  section?: unknown;
  chunkIndex?: unknown;
}


interface KnowledgeQueryResult {
  ids: string[][];
  documents: Array<Array<string | null>>;
  metadatas: Array<Array<QueryMetadata | null>>;
  distances?: Array<Array<number | null>> | null;
}


interface KnowledgeCollection {
  query(input: {
    queryTexts: string[];
    nResults: number;
  }): Promise<KnowledgeQueryResult>;
}


interface ChromaClientProvider {
  getOrCreateKnowledgeCollection(): Promise<
    KnowledgeCollection
  >;
}


export interface RetrieverOptions {
  topK?: number;
}


const DEFAULT_TOP_K = 5;


function asString(
  value: unknown,
  fallback: string,
): string {
  return typeof value === "string"
    ? value
    : fallback;
}


function asNumber(
  value: unknown,
  fallback: number,
): number {
  return typeof value === "number"
    ? value
    : fallback;
}


export class RetrieverService {
  private readonly topK: number;

  constructor(
    private readonly chromaClient: ChromaClientProvider =
      new MaranelloChromaClient(),
    options: RetrieverOptions = {},
  ) {
    this.topK =
      options.topK
      ?? DEFAULT_TOP_K;

    if (
      !Number.isInteger(this.topK)
      || this.topK <= 0
    ) {
      throw new Error(
        "Retriever topK must be a positive integer.",
      );
    }
  }

  async retrieve(
    question: string,
  ): Promise<RetrievedKnowledgeChunk[]> {
    const normalizedQuestion =
      question.trim();

    if (normalizedQuestion.length === 0) {
      throw new Error(
        "Retrieval question must not be empty.",
      );
    }

    const collection =
      await this.chromaClient
        .getOrCreateKnowledgeCollection();

    const result = await collection.query({
      queryTexts: [
        normalizedQuestion,
      ],
      nResults: this.topK,
    });

    const ids = result.ids[0] ?? [];
    const documents =
      result.documents[0] ?? [];
    const metadatas =
      result.metadatas[0] ?? [];
    const distances =
      result.distances?.[0] ?? [];

    return ids.flatMap(
      (
        id,
        index,
      ): RetrievedKnowledgeChunk[] => {
        const content =
          documents[index];

        if (
          content === null
          || content === undefined
        ) {
          return [];
        }

        const metadata =
          metadatas[index] ?? {};

        const distance =
          distances[index];

        return [
          {
            id,
            source: asString(
              metadata.source,
              "Unknown",
            ),
            section: asString(
              metadata.section,
              "Unsectioned",
            ),
            content,
            chunkIndex: asNumber(
              metadata.chunkIndex,
              index,
            ),
            distance:
              typeof distance === "number"
                ? distance
                : null,
          },
        ];
      },
    );
  }
}