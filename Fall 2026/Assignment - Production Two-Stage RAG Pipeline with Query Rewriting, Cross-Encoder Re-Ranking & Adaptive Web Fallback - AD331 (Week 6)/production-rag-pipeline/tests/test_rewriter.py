from src.rewriter import QueryRewriter


def test_conversational_pronoun_resolution() -> None:
    rewritten = QueryRewriter().rewrite(
        "What are its system requirements?",
        "We were discussing Kubernetes Worker Nodes.",
    )

    assert "Kubernetes Worker Nodes" in rewritten


def test_empty_query_is_rejected() -> None:
    try:
        QueryRewriter().rewrite(" ")
    except ValueError as exc:
        assert "empty" in str(exc).lower()
    else:
        raise AssertionError("Expected empty query to be rejected")

