from src.reranker import CrossEncoderReranker, sigmoid
from src.schemas import RetrievedChunk


def chunk(content: str) -> RetrievedChunk:
    return RetrievedChunk(chunk_id="test:1", content=content, source="internal_doc")


def test_sigmoid_logit_normalization_stays_in_bounds() -> None:
    for logit in (-100.0, -2.0, 0.0, 2.0, 100.0):
        score = sigmoid(logit)
        assert 0.0 <= score <= 1.0


def test_low_confidence_triggers_fallback() -> None:
    _, confidence, low_confidence = CrossEncoderReranker(threshold=0.55).rerank(
        "quantum cooking recipes",
        [chunk("deployment rollback and cloud access policies")],
    )
    assert confidence < 0.55
    assert low_confidence is True


def test_high_confidence_passes_internal_gate() -> None:
    _, confidence, low_confidence = CrossEncoderReranker(threshold=0.55).rerank(
        "deployment rollback cloud access",
        [chunk("deployment rollback and cloud access policies")],
    )
    assert confidence >= 0.55
    assert low_confidence is False

