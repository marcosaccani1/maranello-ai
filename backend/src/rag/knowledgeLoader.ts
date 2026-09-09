import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

import type { KnowledgeDocument } from "./types.js";


const EXCLUDED_FILES = new Set([
  "README.md",
]);


export class KnowledgeLoader {
  constructor(
    private readonly knowledgeBasePath: string = path.resolve(
      process.cwd(),
      "../knowledge_base",
    ),
  ) {}

  async loadDocuments(): Promise<KnowledgeDocument[]> {
    const entries = await readdir(
      this.knowledgeBasePath,
      {
        withFileTypes: true,
      },
    );

    const markdownFiles = entries
      .filter(
        (entry) =>
          entry.isFile()
          && entry.name.endsWith(".md")
          && !EXCLUDED_FILES.has(entry.name),
      )
      .map((entry) => entry.name)
      .sort();

    const documents = await Promise.all(
      markdownFiles.map(
        async (fileName): Promise<KnowledgeDocument> => {
          const filePath = path.join(
            this.knowledgeBasePath,
            fileName,
          );

          const content = await readFile(
            filePath,
            "utf-8",
          );

          return {
            source: fileName,
            content,
          };
        },
      ),
    );

    return documents;
  }
}