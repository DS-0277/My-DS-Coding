"""Orchestration for the two-stage RAG pipeline."""

from .generator import GroundedGenerator
from .reranker import CrossEncoderReranker
from .retriever import DocumentRetriever
from .rewriter import QueryRewriter
from .schemas import RAGResponse
from .web_fallback import WebFallback


class RAGPipeline:
    def __init__(self, docs_dir: str = "docs") -> None:
        self.rewriter = QueryRewriter()
        self.retriever = DocumentRetriever(docs_dir)
        self.reranker = CrossEncoderReranker()
        self.web_fallback = WebFallback()
        self.generator = GroundedGenerator()

    def run(self, query: str, conversation_context: str | None = None) -> RAGResponse:
        transformed = self.rewriter.rewrite(query, conversation_context)
        candidates = self.retriever.search(transformed, k=20)
        reranked, confidence, low_confidence = self.reranker.rerank(transformed, candidates)

        if low_confidence:
            web_chunks = self.web_fallback.search(transformed, limit=3)
            answer, citations = self.generator.generate(transformed, web_chunks)
            return RAGResponse(
                answer=answer,
                citations=citations,
                route_taken="WEB_FALLBACK",
                confidence_score=confidence,
                transformed_query=transformed,
                retrieved_chunks=web_chunks,
            )

        answer, citations = self.generator.generate(transformed, reranked[:3])
        return RAGResponse(
            answer=answer,
            citations=citations,
            route_taken="INTERNAL_RAG",
            confidence_score=confidence,
            transformed_query=transformed,
            retrieved_chunks=reranked[:3],
        )

