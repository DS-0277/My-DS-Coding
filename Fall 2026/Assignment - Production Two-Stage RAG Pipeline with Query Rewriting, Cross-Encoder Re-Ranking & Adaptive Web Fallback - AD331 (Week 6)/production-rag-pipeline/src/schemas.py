"""Shared typed models for the RAG pipeline."""

from typing import Literal

from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    chunk_id: str
    content: str
    score: float = 0.0
    source: Literal["internal_doc", "web"]
    url: str | None = None
    initial_score: float | None = None
    original_rank: int | None = None


class RAGResponse(BaseModel):
    answer: str
    citations: list[str] = Field(default_factory=list)
    route_taken: Literal["INTERNAL_RAG", "WEB_FALLBACK"]
    confidence_score: float
    transformed_query: str
    retrieved_chunks: list[RetrievedChunk] = Field(default_factory=list)


class PipelineState(BaseModel):
    original_query: str
    transformed_query: str
    stage_one_candidates: list[RetrievedChunk] = Field(default_factory=list)
    reranked_candidates: list[RetrievedChunk] = Field(default_factory=list)
    confidence_score: float = 0.0
    route_taken: Literal["INTERNAL_RAG", "WEB_FALLBACK"] | None = None

