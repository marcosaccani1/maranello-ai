import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import { IngestionService } from "../../src/rag/ingestionService.js";

import type { KnowledgeDocument } from "../../src/rag/types.js";


describe("IngestionService", () => {
  it("loads, chunks, and upserts knowledge documents", async () => {
    const documents: KnowledgeDocument[] = [
      {
        source: "quality_policy.md",
        content:
          "## Defect Rate\n\n"
          + "The defect rate threshold is 2.5%.",
      },
      {
        source: "supplier_policy.md",
        content:
          "## Supplier Quality\n\n"
          + "Suppliers must be reviewed regularly.",
      },
    ];

    const loader = {
      loadDocuments: vi.fn()
        .mockResolvedValue(documents),
    };

    const chunker = {
      chunkDocuments: vi.fn()
        .mockReturnValue([
          {
            id: "chunk-1",
            source: "quality_policy.md",
            section: "Defect Rate",
            content:
              "## Defect Rate\n\n"
              + "The defect rate threshold is 2.5%.",
            chunkIndex: 0,
          },
          {
            id: "chunk-2",
            source: "supplier_policy.md",
            section: "Supplier Quality",
            content:
              "## Supplier Quality\n\n"
              + "Suppliers must be reviewed regularly.",
            chunkIndex: 0,
          },
        ]),
    };

    const upsert = vi.fn()
      .mockResolvedValue(undefined);

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          name: "test_collection",
          upsert,
        }),
    };

    const service = new IngestionService(
      loader,
      chunker,
      chromaClient,
    );

    const result = await service.ingest();

    expect(
      loader.loadDocuments,
    ).toHaveBeenCalledOnce();

    expect(
      chunker.chunkDocuments,
    ).toHaveBeenCalledWith(documents);

    expect(
      chromaClient
        .getOrCreateKnowledgeCollection,
    ).toHaveBeenCalledOnce();

    expect(upsert).toHaveBeenCalledWith({
      ids: [
        "chunk-1",
        "chunk-2",
      ],
      documents: [
        "## Defect Rate\n\n"
          + "The defect rate threshold is 2.5%.",
        "## Supplier Quality\n\n"
          + "Suppliers must be reviewed regularly.",
      ],
      metadatas: [
        {
          source: "quality_policy.md",
          section: "Defect Rate",
          chunkIndex: 0,
        },
        {
          source: "supplier_policy.md",
          section: "Supplier Quality",
          chunkIndex: 0,
        },
      ],
    });

    expect(result).toEqual({
      documentsLoaded: 2,
      chunksIndexed: 2,
      collectionName: "test_collection",
    });
  });

  it("does not call upsert when no chunks exist", async () => {
    const loader = {
      loadDocuments: vi.fn()
        .mockResolvedValue([]),
    };

    const chunker = {
      chunkDocuments: vi.fn()
        .mockReturnValue([]),
    };

    const upsert = vi.fn();

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          name: "test_collection",
          upsert,
        }),
    };

    const service = new IngestionService(
      loader,
      chunker,
      chromaClient,
    );

    const result = await service.ingest();

    expect(upsert).not.toHaveBeenCalled();

    expect(result).toEqual({
      documentsLoaded: 0,
      chunksIndexed: 0,
      collectionName: "test_collection",
    });
  });

  it("replaces missing section metadata with Unsectioned", async () => {
    const loader = {
      loadDocuments: vi.fn()
        .mockResolvedValue([
          {
            source: "policy.md",
            content: "Policy content.",
          },
        ]),
    };

    const chunker = {
      chunkDocuments: vi.fn()
        .mockReturnValue([
          {
            id: "chunk-1",
            source: "policy.md",
            section: null,
            content: "Policy content.",
            chunkIndex: 0,
          },
        ]),
    };

    const upsert = vi.fn()
      .mockResolvedValue(undefined);

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          name: "test_collection",
          upsert,
        }),
    };

    const service = new IngestionService(
      loader,
      chunker,
      chromaClient,
    );

    await service.ingest();

    expect(upsert).toHaveBeenCalledWith({
      ids: [
        "chunk-1",
      ],
      documents: [
        "Policy content.",
      ],
      metadatas: [
        {
          source: "policy.md",
          section: "Unsectioned",
          chunkIndex: 0,
        },
      ],
    });
  });
});