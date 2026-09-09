import type { Collection } from "chromadb";

import { MaranelloChromaClient } from "../services/chromaClient.js";
import { KnowledgeLoader } from "./knowledgeLoader.js";
import { TextChunker } from "./textChunker.js";

import type {
  KnowledgeChunk,
  KnowledgeDocument,
} from "./types.js";


export interface IngestionResult {
  documentsLoaded: number;
  chunksIndexed: number;
  collectionName: string;
}


interface KnowledgeLoaderProvider {
  loadDocuments(): Promise<KnowledgeDocument[]>;
}


interface TextChunkerProvider {
  chunkDocuments(
    documents: KnowledgeDocument[],
  ): KnowledgeChunk[];
}


interface KnowledgeCollection {
  name: string;

  upsert(input: {
    ids: string[];
    documents: string[];
    metadatas: Array<{
      source: string;
      section: string;
      chunkIndex: number;
    }>;
  }): Promise<unknown>;
}


interface ChromaClientProvider {
  getOrCreateKnowledgeCollection(): Promise<
    Collection | KnowledgeCollection
  >;
}


export class IngestionService {
  constructor(
    private readonly loader: KnowledgeLoaderProvider =
      new KnowledgeLoader(),

    private readonly chunker: TextChunkerProvider =
      new TextChunker(),

    private readonly chromaClient: ChromaClientProvider =
      new MaranelloChromaClient(),
  ) {}

  async ingest(): Promise<IngestionResult> {
    const documents =
      await this.loader.loadDocuments();

    const chunks =
      this.chunker.chunkDocuments(documents);

    const collection =
      await this.chromaClient
        .getOrCreateKnowledgeCollection();

    if (chunks.length === 0) {
      return {
        documentsLoaded: documents.length,
        chunksIndexed: 0,
        collectionName: collection.name,
      };
    }

    await collection.upsert(
      this.createUpsertPayload(chunks),
    );

    return {
      documentsLoaded: documents.length,
      chunksIndexed: chunks.length,
      collectionName: collection.name,
    };
  }

  private createUpsertPayload(
    chunks: KnowledgeChunk[],
  ): {
    ids: string[];
    documents: string[];
    metadatas: Array<{
      source: string;
      section: string;
      chunkIndex: number;
    }>;
  } {
    return {
      ids: chunks.map(
        (chunk) => chunk.id,
      ),

      documents: chunks.map(
        (chunk) => chunk.content,
      ),

      metadatas: chunks.map(
        (chunk) => ({
          source: chunk.source,
          section:
            chunk.section
            ?? "Unsectioned",
          chunkIndex: chunk.chunkIndex,
        }),
      ),
    };
  }
}