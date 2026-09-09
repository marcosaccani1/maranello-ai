export interface KnowledgeDocument {
  source: string;
  content: string;
}

export interface KnowledgeChunk {
  id: string;
  source: string;
  section: string | null;
  content: string;
  chunkIndex: number;
}

export interface RetrievedKnowledgeChunk {
  id: string;
  source: string;
  section: string;
  content: string;
  chunkIndex: number;
  distance: number | null;
}