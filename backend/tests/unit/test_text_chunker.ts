import {
  describe,
  expect,
  it,
} from "vitest";

import { TextChunker } from "../../src/rag/textChunker.js";

import type { KnowledgeDocument } from "../../src/rag/types.js";


describe("TextChunker", () => {
  it("creates one chunk for a short Markdown section", () => {
    const document: KnowledgeDocument = {
      source: "quality_policy.md",
      content:
        "## Defect Rate Thresholds\n\n"
        + "The normal defect rate must remain below the threshold.",
    };

    const chunker = new TextChunker();

    const chunks = chunker.chunkDocument(
      document,
    );

    expect(chunks).toHaveLength(1);

    expect(chunks[0]).toMatchObject({
      source: "quality_policy.md",
      section: "Defect Rate Thresholds",
      chunkIndex: 0,
      content:
        "## Defect Rate Thresholds\n\n"
        + "The normal defect rate must remain below the threshold.",
    });
  });

  it("preserves Markdown sections", () => {
    const document: KnowledgeDocument = {
      source: "policy.md",
      content: [
        "# Manufacturing Policy",
        "",
        "General policy content.",
        "",
        "## Escalation",
        "",
        "Escalation content.",
        "",
        "## Responsibilities",
        "",
        "Responsibility content.",
      ].join("\n"),
    };

    const chunker = new TextChunker();

    const chunks = chunker.chunkDocument(
      document,
    );

    expect(chunks).toHaveLength(3);

    expect(
      chunks.map(
        (chunk) => chunk.section,
      ),
    ).toEqual([
      "Manufacturing Policy",
      "Escalation",
      "Responsibilities",
    ]);
  });

  it("splits long sections into multiple chunks", () => {
    const document: KnowledgeDocument = {
      source: "policy.md",
      content: [
        "## Long Section",
        "",
        "First paragraph contains useful policy information.",
        "",
        "Second paragraph contains additional policy information.",
        "",
        "Third paragraph contains more policy information.",
      ].join("\n"),
    };

    const chunker = new TextChunker({
      maxChunkChars: 100,
    });

    const chunks = chunker.chunkDocument(
      document,
    );

    expect(chunks.length).toBeGreaterThan(1);

    for (const chunk of chunks) {
      expect(chunk.content.length).toBeLessThanOrEqual(
        100,
      );

      expect(chunk.section).toBe(
        "Long Section",
      );

      expect(chunk.content).toContain(
        "## Long Section",
      );
    }
  });

  it("hard-splits a paragraph that exceeds the maximum size", () => {
    const document: KnowledgeDocument = {
      source: "policy.md",
      content:
        "## Large Paragraph\n\n"
        + "quality ".repeat(80),
    };

    const chunker = new TextChunker({
      maxChunkChars: 120,
    });

    const chunks = chunker.chunkDocument(
      document,
    );

    expect(chunks.length).toBeGreaterThan(1);

    for (const chunk of chunks) {
      expect(chunk.content.length).toBeLessThanOrEqual(
        120,
      );
    }
  });

  it("creates deterministic chunk identifiers", () => {
    const document: KnowledgeDocument = {
      source: "policy.md",
      content:
        "## Quality\n\n"
        + "Deterministic policy content.",
    };

    const chunker = new TextChunker();

    const firstRun = chunker.chunkDocument(
      document,
    );

    const secondRun = chunker.chunkDocument(
      document,
    );

    expect(firstRun[0]?.id).toBe(
      secondRun[0]?.id,
    );
  });

  it("creates continuous chunk indexes", () => {
    const document: KnowledgeDocument = {
      source: "policy.md",
      content: [
        "## Section One",
        "",
        "First content.",
        "",
        "## Section Two",
        "",
        "Second content.",
        "",
        "## Section Three",
        "",
        "Third content.",
      ].join("\n"),
    };

    const chunker = new TextChunker();

    const chunks = chunker.chunkDocument(
      document,
    );

    expect(
      chunks.map(
        (chunk) => chunk.chunkIndex,
      ),
    ).toEqual([
      0,
      1,
      2,
    ]);
  });

  it("does not create empty chunks", () => {
    const document: KnowledgeDocument = {
      source: "policy.md",
      content: [
        "",
        "",
        "## Quality",
        "",
        "",
        "Policy content.",
        "",
        "",
      ].join("\n"),
    };

    const chunker = new TextChunker();

    const chunks = chunker.chunkDocument(
      document,
    );

    expect(chunks).toHaveLength(1);

    expect(
      chunks.every(
        (chunk) =>
          chunk.content.trim().length > 0,
      ),
    ).toBe(true);
  });

  it("chunks multiple documents while preserving their sources", () => {
    const documents: KnowledgeDocument[] = [
      {
        source: "quality.md",
        content:
          "## Quality\n\nQuality policy.",
      },
      {
        source: "supplier.md",
        content:
          "## Supplier\n\nSupplier policy.",
      },
    ];

    const chunker = new TextChunker();

    const chunks = chunker.chunkDocuments(
      documents,
    );

    expect(
      chunks.map(
        (chunk) => chunk.source,
      ),
    ).toEqual([
      "quality.md",
      "supplier.md",
    ]);
  });
});