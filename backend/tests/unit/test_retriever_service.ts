import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import { RetrieverService } from "../../src/rag/retrieverService.js";


describe("RetrieverService", () => {
  it("retrieves and maps knowledge chunks", async () => {
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