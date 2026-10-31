from src.benchmarker import hit_rate_at_k, mrr_at_k, recall_at_k


def test_metric_math_for_hit_recall_and_mrr() -> None:
    retrieved = [["R1", "R2"], ["X1", "X2"], ["R3", "X3"]]
    relevant = [{"R2"}, {"R9"}, {"R3"}]
    assert hit_rate_at_k(retrieved, relevant, 2) == 2 / 3
    assert recall_at_k(retrieved, relevant, 2) == 2 / 3
    assert mrr_at_k(retrieved, relevant, 2) == (0.5 + 0.0 + 1.0) / 3


def test_mrr_miss_is_zero() -> None:
    assert mrr_at_k([["A"]], [{"B"}], 1) == 0.0
