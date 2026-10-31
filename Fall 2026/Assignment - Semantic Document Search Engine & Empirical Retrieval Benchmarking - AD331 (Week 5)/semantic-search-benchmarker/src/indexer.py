"""BM25 and local dense retrieval indexes for the initial draft."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from rank_bm25 import BM25Okapi

from .chunking import DocumentChunk


def tokenize(text: str) -> list[str]:
    """Apply the same lowercase tokenization to documents and queries."""

    return re.findall(r"[a-z0-9][a-z0-9_-]*", text.lower())


@dataclass(frozen=True)
class SearchResult:
    chunk_id: str
    content: str
    metadata: dict
    score: float
    rank: int


class BM25Index:
    """Sparse lexical index over document chunks."""

    def __init__(self, chunks: list[DocumentChunk]) -> None:
        self.chunks = chunks
        self.tokens = [tokenize(chunk.content) for chunk in chunks]
        self.index = BM25Okapi(self.tokens)

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        scores = self.index.get_scores(tokenize(query))
        order = np.argsort(scores)[::-1][:top_k]
        return [self._result(int(i), float(scores[i]), rank + 1) for rank, i in enumerate(order)]

    def _result(self, index: int, score: float, rank: int) -> SearchResult:
        chunk = self.chunks[index]
        return SearchResult(chunk.chunk_id, chunk.content, chunk.metadata, score, rank)


class DenseVectorIndex:
    """Local embedding index using sentence-transformers and cosine similarity."""

    def __init__(self, chunks: list[DocumentChunk], model_name: str = "all-MiniLM-L6-v2") -> None:
        from sentence_transformers import SentenceTransformer

        self.chunks = chunks
        self.model = SentenceTransformer(model_name)
        self.embeddings = self._normalize(self.model.encode([c.content for c in chunks], convert_to_numpy=True))

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.clip(norms, 1e-12, None)

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        query_vector = self._normalize(self.model.encode([query], convert_to_numpy=True))[0]
        scores = self.embeddings @ query_vector
        order = np.argsort(scores)[::-1][:top_k]
        return [self._result(int(i), float(scores[i]), rank + 1) for rank, i in enumerate(order)]

    def _result(self, index: int, score: float, rank: int) -> SearchResult:
        chunk = self.chunks[index]
        return SearchResult(chunk.chunk_id, chunk.content, chunk.metadata, score, rank)


def build_indexes(chunks: Iterable[DocumentChunk]) -> tuple[BM25Index, DenseVectorIndex]:
    """Build both retrieval backends from the same chunk collection."""

    materialized = list(chunks)
    if not materialized:
        raise ValueError("At least one document chunk is required")
    return BM25Index(materialized), DenseVectorIndex(materialized)
