import {
  mkdtemp,
  rm,
  writeFile,
} from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
} from "vitest";

import { KnowledgeLoader } from "../../src/rag/knowledgeLoader.js";


describe("KnowledgeLoader", () => {
  let temporaryDirectory: string;

  beforeEach(async () => {
    temporaryDirectory = await mkdtemp(
      path.join(
        os.tmpdir(),
        "maranello-ai-kb-",
      ),
    );
  });

  afterEach(async () => {
    await rm(
      temporaryDirectory,
      {
        recursive: true,
        force: true,
      },
    );
  });

  it("loads Markdown documents", async () => {
    await writeFile(
      path.join(
        temporaryDirectory,
        "quality_policy.md",
      ),
      "# Quality Policy\n\nPolicy content.",
      "utf-8",
    );

    const loader = new KnowledgeLoader(
      temporaryDirectory,
    );

    const documents = await loader.loadDocuments();

    expect(documents).toHaveLength(1);
    expect(documents[0]).toEqual({
      source: "quality_policy.md",
      content:
        "# Quality Policy\n\nPolicy content.",
    });
  });

  it("ignores non-Markdown files", async () => {
    await writeFile(
      path.join(
        temporaryDirectory,
        "policy.md",
      ),
      "# Policy",
      "utf-8",
    );

    await writeFile(
      path.join(
        temporaryDirectory,
        "notes.txt",
      ),
      "This file must be ignored.",
      "utf-8",
    );

    const loader = new KnowledgeLoader(
      temporaryDirectory,
    );

    const documents = await loader.loadDocuments();

    expect(documents).toHaveLength(1);
    expect(documents[0]?.source).toBe(
      "policy.md",
    );
  });

  it("excludes the Knowledge Base README", async () => {
    await writeFile(
      path.join(
        temporaryDirectory,
        "README.md",
      ),
      "# Knowledge Base Documentation",
      "utf-8",
    );

    await writeFile(
      path.join(
        temporaryDirectory,
        "policy.md",
      ),
      "# Business Policy",
      "utf-8",
    );

    const loader = new KnowledgeLoader(
      temporaryDirectory,
    );

    const documents = await loader.loadDocuments();

    expect(documents).toHaveLength(1);
    expect(documents[0]?.source).toBe(
      "policy.md",
    );
  });

  it("returns documents in deterministic order", async () => {
    await writeFile(
      path.join(
        temporaryDirectory,
        "supplier.md",
      ),
      "# Supplier",
      "utf-8",
    );

    await writeFile(
      path.join(
        temporaryDirectory,
        "manufacturing.md",
      ),
      "# Manufacturing",
      "utf-8",
    );

    const loader = new KnowledgeLoader(
      temporaryDirectory,
    );

    const documents = await loader.loadDocuments();

    expect(
      documents.map(
        (document) => document.source,
      ),
    ).toEqual([
      "manufacturing.md",
      "supplier.md",
    ]);
  });

  it("returns an empty array when no eligible Markdown files exist", async () => {
    await writeFile(
      path.join(
        temporaryDirectory,
        "README.md",
      ),
      "# Documentation",
      "utf-8",
    );

    await writeFile(
      path.join(
        temporaryDirectory,
        "notes.txt",
      ),
      "No business Markdown here.",
      "utf-8",
    );

    const loader = new KnowledgeLoader(
      temporaryDirectory,
    );

    const documents = await loader.loadDocuments();

    expect(documents).toEqual([]);
  });
});