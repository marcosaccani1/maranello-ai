import { createHash } from "node:crypto";

import type {
  KnowledgeChunk,
  KnowledgeDocument,
} from "./types.js";


interface MarkdownSection {
  title: string | null;
  heading: string | null;
  content: string;
}


export interface TextChunkerOptions {
  maxChunkChars?: number;
}


const DEFAULT_MAX_CHUNK_CHARS = 1800;


function createChunkId(
  source: string,
  section: string | null,
  chunkIndex: number,
  content: string,
): string {
  const value = [
    source,
    section ?? "",
    chunkIndex.toString(),
    content,
  ].join("::");

  const hash = createHash("sha256")
    .update(value)
    .digest("hex")
    .slice(0, 16);

  return `${source.replace(/[^a-zA-Z0-9]+/g, "-")}-${hash}`;
}


function parseMarkdownSections(
  content: string,
): MarkdownSection[] {
  const lines = content.split(/\r?\n/);

  const sections: MarkdownSection[] = [];

  let currentTitle: string | null = null;
  let currentHeading: string | null = null;
  let currentLines: string[] = [];

  const flushSection = (): void => {
    const sectionContent = currentLines
      .join("\n")
      .trim();

    if (
      currentHeading === null
      && sectionContent.length === 0
    ) {
      currentLines = [];
      return;
    }

    sections.push({
      title: currentTitle,
      heading: currentHeading,
      content: sectionContent,
    });

    currentLines = [];
  };

  for (const line of lines) {
    const headingMatch = line.match(
      /^(#{1,6})\s+(.+?)\s*$/,
    );

    if (headingMatch) {
      flushSection();

      currentHeading = line.trim();
      currentTitle =
        headingMatch[2]?.trim() ?? null;

      continue;
    }

    currentLines.push(line);
  }

  flushSection();

  return sections;
}


function hardSplitText(
  text: string,
  maxChunkChars: number,
): string[] {
  const chunks: string[] = [];

  let remaining = text.trim();

  while (remaining.length > maxChunkChars) {
    let splitIndex = remaining.lastIndexOf(
      " ",
      maxChunkChars,
    );

    if (splitIndex <= 0) {
      splitIndex = maxChunkChars;
    }

    const chunk = remaining
      .slice(0, splitIndex)
      .trim();

    if (chunk.length > 0) {
      chunks.push(chunk);
    }

    remaining = remaining
      .slice(splitIndex)
      .trim();
  }

  if (remaining.length > 0) {
    chunks.push(remaining);
  }

  return chunks;
}


function splitSectionContent(
  section: MarkdownSection,
  maxChunkChars: number,
): string[] {
  const headingPrefix = section.heading
    ? `${section.heading}\n\n`
    : "";

  const availableBodyChars =
    maxChunkChars - headingPrefix.length;

  if (availableBodyChars <= 0) {
    throw new Error(
      "Maximum chunk size is too small for the Markdown heading.",
    );
  }

  const body = section.content.trim();

  if (body.length === 0) {
    return section.heading
      ? [section.heading]
      : [];
  }

  const completeContent =
    `${headingPrefix}${body}`;

  if (completeContent.length <= maxChunkChars) {
    return [completeContent];
  }

  const paragraphs = body
    .split(/\n\s*\n/)
    .map((paragraph) => paragraph.trim())
    .filter((paragraph) => paragraph.length > 0);

  const bodyChunks: string[] = [];
  let currentBody = "";

  const flushCurrentBody = (): void => {
    const trimmed = currentBody.trim();

    if (trimmed.length > 0) {
      bodyChunks.push(trimmed);
    }

    currentBody = "";
  };

  for (const paragraph of paragraphs) {
    if (paragraph.length > availableBodyChars) {
      flushCurrentBody();

      bodyChunks.push(
        ...hardSplitText(
          paragraph,
          availableBodyChars,
        ),
      );

      continue;
    }

    const candidate = currentBody.length > 0
      ? `${currentBody}\n\n${paragraph}`
      : paragraph;

    if (candidate.length <= availableBodyChars) {
      currentBody = candidate;
      continue;
    }

    flushCurrentBody();
    currentBody = paragraph;
  }

  flushCurrentBody();

  return bodyChunks.map(
    (bodyChunk) =>
      `${headingPrefix}${bodyChunk}`.trim(),
  );
}


export class TextChunker {
  private readonly maxChunkChars: number;

  constructor(
    options: TextChunkerOptions = {},
  ) {
    this.maxChunkChars =
      options.maxChunkChars
      ?? DEFAULT_MAX_CHUNK_CHARS;

    if (this.maxChunkChars <= 0) {
      throw new Error(
        "Maximum chunk size must be greater than zero.",
      );
    }
  }

  chunkDocument(
    document: KnowledgeDocument,
  ): KnowledgeChunk[] {
    const sections = parseMarkdownSections(
      document.content,
    );

    const chunks: KnowledgeChunk[] = [];

    for (const section of sections) {
      const sectionChunks = splitSectionContent(
        section,
        this.maxChunkChars,
      );

      for (const content of sectionChunks) {
        const normalizedContent = content.trim();

        if (normalizedContent.length === 0) {
          continue;
        }

        const chunkIndex = chunks.length;

        chunks.push({
          id: createChunkId(
            document.source,
            section.title,
            chunkIndex,
            normalizedContent,
          ),
          source: document.source,
          section: section.title,
          content: normalizedContent,
          chunkIndex,
        });
      }
    }

    return chunks;
  }

  chunkDocuments(
    documents: KnowledgeDocument[],
  ): KnowledgeChunk[] {
    return documents.flatMap(
      (document) =>
        this.chunkDocument(document),
    );
  }
}