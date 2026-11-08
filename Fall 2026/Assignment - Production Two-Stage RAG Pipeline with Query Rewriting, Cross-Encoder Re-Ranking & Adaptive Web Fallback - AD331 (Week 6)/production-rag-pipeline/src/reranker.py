"""Stage 2 re-ranking and confidence gating."""

import math
import re

from .schemas import RetrievedChunk
from .settings import CROSS_ENCODER_LOGIT_BIAS, CROSS_ENCODER_MODEL, RAG_MODE


def sigmoid(logit: float) -> float:
    """Convert a cross-encoder logit into a probability-like value."""
    if logit >= 0:
        z = math.exp(-logit)
        return 1.0 / (1.0 + z)
    z = math.exp(logit)
    return z / (1.0 + z)


class CrossEncoderReranker:
    def __init__(self, threshold: float = 0.55, top_k: int = 5) -> None:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0.0 and 1.0")
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        self.threshold = threshold
        self.top_k = top_k

    def rerank(self, query: str, candidates: list[RetrievedChunk]) -> tuple[list[RetrievedChunk], float, bool]:
        if RAG_MODE == "hybrid":
            from sentence_transformers import CrossEncoder

            model = CrossEncoder(CROSS_ENCODER_MODEL)
            logits = model.predict([(query, candidate.content) for candidate in candidates])
            scored = [candidate.model_copy(update={"score": sigmoid(float(logit) + CROSS_ENCODER_LOGIT_BIAS)}) for candidate, logit in zip(candidates, logits)]
            scored.sort(key=lambda item: item.score, reverse=True)
            confidence = scored[0].score if scored else 0.0
            return scored[: self.top_k], confidence, confidence < self.threshold

        query_terms = set(re.findall(r"[a-z0-9_-]+", query.lower()))
        scored = []
        for candidate in candidates:
            terms = set(re.findall(r"[a-z0-9_-]+", candidate.content.lower()))
            overlap = len(query_terms & terms) / max(len(query_terms), 1)
            logit = (overlap * 8.0) - 2.0
            score = sigmoid(logit)
            scored.append(candidate.model_copy(update={"score": score}))
        scored.sort(key=lambda item: item.score, reverse=True)
        confidence = scored[0].score if scored else 0.0
        return scored[: self.top_k], confidence, confidence < self.threshold

