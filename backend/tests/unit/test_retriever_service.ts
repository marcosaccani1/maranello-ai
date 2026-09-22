import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import { RetrieverService } from "../../src/rag/retrieverService.js";


describe("RetrieverService", () => {
  it("retrieves and maps relevant knowledge chunks", async () => {
    const query = vi.fn()
      .mockResolvedValue({
        ids: [
          [
            "chunk-1",
            "chunk-2",
          ],
        ],
        documents: [
          [
            "Critical defect rate policy.",
            "Warning defect rate policy.",
          ],
        ],
        metadatas: [
          [
            {
              source:
                "manufacturing_quality_policy.md",
              section:
                "4.2 Defect Rate Thresholds",
              chunkIndex: 7,
            },
            {
              source:
                "manufacturing_quality_policy.md",
              section:
                "4.2 Defect Rate Thresholds",
              chunkIndex: 6,
            },
          ],
        ],
        distances: [
          [
            0.12,
            0.24,
          ],
        ],
      });

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          query,
        }),
    };

    const service = new RetrieverService(
      chromaClient,
      {
        topK: 2,
      },
    );

    const results = await service.retrieve(
      "What is the critical defect rate threshold?",
    );

    expect(query).toHaveBeenCalledWith({
      queryTexts: [
        "What is the critical defect rate threshold?",
      ],
      nResults: 2,
    });

    expect(results).toEqual([
      {
        id: "chunk-1",
        source:
          "manufacturing_quality_policy.md",
        section:
          "4.2 Defect Rate Thresholds",
        content:
          "Critical defect rate policy.",
        chunkIndex: 7,
        distance: 0.12,
      },
      {
        id: "chunk-2",
        source:
          "manufacturing_quality_policy.md",
        section:
          "4.2 Defect Rate Thresholds",
        content:
          "Warning defect rate policy.",
        chunkIndex: 6,
        distance: 0.24,
      },
    ]);
  });


  it("filters chunks beyond the maximum distance", async () => {
    const query = vi.fn()
      .mockResolvedValue({
        ids: [
          [
            "relevant-chunk",
            "irrelevant-chunk",
          ],
        ],
        documents: [
          [
            "Relevant quality policy.",
            "Unrelated content.",
          ],
        ],
        metadatas: [
          [
            {
              source: "policy.md",
              section: "Quality",
              chunkIndex: 1,
            },
            {
              source: "policy.md",
              section: "Other",
              chunkIndex: 2,
            },
          ],
        ],
        distances: [
          [
            0.45,
            0.71,
          ],
        ],
      });

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          query,
        }),
    };

    const service = new RetrieverService(
      chromaClient,
      {
        maxDistance: 0.7,
      },
    );

    const results = await service.retrieve(
      "Manufacturing quality policy",
    );

    expect(results).toEqual([
      {
        id: "relevant-chunk",
        source: "policy.md",
        section: "Quality",
        content:
          "Relevant quality policy.",
        chunkIndex: 1,
        distance: 0.45,
      },
    ]);
  });


  it("keeps chunks exactly at the maximum distance", async () => {
    const query = vi.fn()
      .mockResolvedValue({
        ids: [
          [
            "boundary-chunk",
          ],
        ],
        documents: [
          [
            "Boundary relevance content.",
          ],
        ],
        metadatas: [
          [
            {
              source: "policy.md",
              section: "Quality",
              chunkIndex: 3,
            },
          ],
        ],
        distances: [
          [
            0.7,
          ],
        ],
      });

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          query,
        }),
    };

    const service = new RetrieverService(
      chromaClient,
      {
        maxDistance: 0.7,
      },
    );

    const results = await service.retrieve(
      "Quality question",
    );

    expect(results).toHaveLength(1);
    expect(
      results[0]?.distance,
    ).toBe(0.7);
  });


  it("returns no chunks when all results exceed the maximum distance", async () => {
    const query = vi.fn()
      .mockResolvedValue({
        ids: [
          [
            "chunk-1",
            "chunk-2",
          ],
        ],
        documents: [
          [
            "Unrelated content one.",
            "Unrelated content two.",
          ],
        ],
        metadatas: [
          [
            {
              source: "policy.md",
              section: "Other",
              chunkIndex: 1,
            },
            {
              source: "policy.md",
              section: "Other",
              chunkIndex: 2,
            },
          ],
        ],
        distances: [
          [
            0.82,
            0.91,
          ],
        ],
      });

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          query,
        }),
    };

    const service = new RetrieverService(
      chromaClient,
    );

    const results = await service.retrieve(
      "How do I make carbonara?",
    );

    expect(results).toEqual([]);
  });


  it("filters chunks without a valid distance", async () => {
    const query = vi.fn()
      .mockResolvedValue({
        ids: [
          [
            "missing-distance",
            "invalid-distance",
            "valid-distance",
          ],
        ],
        documents: [
          [
            "Missing distance.",
            "Invalid distance.",
            "Valid content.",
          ],
        ],
        metadatas: [
          [
            {
              source: "policy.md",
              section: "Quality",
              chunkIndex: 1,
            },
            {
              source: "policy.md",
              section: "Quality",
              chunkIndex: 2,
            },
            {
              source: "policy.md",
              section: "Quality",
              chunkIndex: 3,
            },
          ],
        ],
        distances: [
          [
            null,
            Number.NaN,
            0.4,
          ],
        ],
      });

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          query,
        }),
    };

    const service = new RetrieverService(
      chromaClient,
    );

    const results = await service.retrieve(
      "Quality policy",
    );

    expect(results).toEqual([
      {
        id: "valid-distance",
        source: "policy.md",
        section: "Quality",
        content: "Valid content.",
        chunkIndex: 3,
        distance: 0.4,
      },
    ]);
  });


  it("rejects an empty retrieval question", async () => {
    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn(),
    };

    const service = new RetrieverService(
      chromaClient,
    );

    await expect(
      service.retrieve("   "),
    ).rejects.toThrow(
      "Retrieval question must not be empty.",
    );

    expect(
      chromaClient
        .getOrCreateKnowledgeCollection,
    ).not.toHaveBeenCalled();
  });


  it("rejects invalid topK values", () => {
    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn(),
    };

    expect(
      () =>
        new RetrieverService(
          chromaClient,
          {
            topK: 0,
          },
        ),
    ).toThrow(
      "Retriever topK must be a positive integer.",
    );
  });


  it("rejects invalid maximum distance values", () => {
    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn(),
    };

    expect(
      () =>
        new RetrieverService(
          chromaClient,
          {
            maxDistance: -0.1,
          },
        ),
    ).toThrow(
      "Retriever maxDistance must be a non-negative finite number.",
    );

    expect(
      () =>
        new RetrieverService(
          chromaClient,
          {
            maxDistance:
              Number.POSITIVE_INFINITY,
          },
        ),
    ).toThrow(
      "Retriever maxDistance must be a non-negative finite number.",
    );
  });


  it("skips results without document content", async () => {
    const query = vi.fn()
      .mockResolvedValue({
        ids: [
          [
            "chunk-1",
            "chunk-2",
          ],
        ],
        documents: [
          [
            null,
            "Valid policy content.",
          ],
        ],
        metadatas: [
          [
            null,
            {
              source: "policy.md",
              section: "Quality",
              chunkIndex: 1,
            },
          ],
        ],
        distances: [
          [
            0.1,
            0.2,
          ],
        ],
      });

    const chromaClient = {
      getOrCreateKnowledgeCollection:
        vi.fn().mockResolvedValue({
          query,
        }),
    };

    const service = new RetrieverService(
      chromaClient,
    );

    const results = await service.retrieve(
      "Quality policy",
    );

    expect(results).toEqual([
      {
        id: "chunk-2",
        source: "policy.md",
        section: "Quality",
        content:
          "Valid policy content.",
        chunkIndex: 1,
        distance: 0.2,
      },
    ]);
  });
});