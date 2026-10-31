"""Evaluation metrics and benchmark runner for retrieval experiments."""

from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
from typing import Any, Callable, Sequence


def hit_rate_at_k(retrieved: Sequence[Sequence[str]], relevant: Sequence[set[str]], k: int) -> float:
    """Return the fraction of queries with a relevant item in the top K."""

    if not retrieved:
        return 0.0
    hits = sum(bool(set(results[:k]) & expected) for results, expected in zip(retrieved, relevant))
    return hits / len(retrieved)


def recall_at_k(retrieved: Sequence[Sequence[str]], relevant: Sequence[set[str]], k: int) -> float:
    """Return average relevant-item recall in the top K."""

    if not relevant:
        return 0.0
    values = [len(set(results[:k]) & expected) / len(expected) if expected else 0.0 for results, expected in zip(retrieved, relevant)]
    return statistics.mean(values)


def mrr_at_k(retrieved: Sequence[Sequence[str]], relevant: Sequence[set[str]], k: int) -> float:
    """Return mean reciprocal rank; missed queries contribute zero."""

    if not retrieved:
        return 0.0
    values: list[float] = []
    for results, expected in zip(retrieved, relevant):
        reciprocal = 0.0
        for rank, chunk_id in enumerate(results[:k], start=1):
            if chunk_id in expected:
                reciprocal = 1.0 / rank
                break
        values.append(reciprocal)
    return statistics.mean(values)


def load_queries(path: str | Path) -> list[dict[str, Any]]:
    """Load evaluation records from JSON."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_benchmark(
    queries: list[dict[str, Any]],
    search: Callable[[str, int], Sequence[Any]],
    k: int = 5,
) -> dict[str, Any]:
    """Run queries, collect per-query rows, and calculate aggregate metrics."""

    retrieved_sections: list[list[str]] = []
    relevant = [set(item["relevant_sections"]) for item in queries]
    rows: list[dict[str, Any]] = []
    latencies: list[float] = []
    for item in queries:
        started = time.perf_counter()
        results = list(search(item["query"], k))
        latency_ms = (time.perf_counter() - started) * 1000
        ids: list[str] = []
        sections: list[str] = []
        for result in results:
            if isinstance(result, dict):
                chunk_id = str(result["chunk_id"])
                metadata = result.get("metadata", {})
            else:
                chunk_id = str(result.chunk_id)
                metadata = getattr(result, "metadata", {})
            ids.append(chunk_id)
            sections.append(str(metadata.get("section_id", chunk_id)))
        retrieved_sections.append(sections)
        matching = [section for section in item["relevant_sections"] if any(section in chunk_id for chunk_id in ids)]
        rows.append({"query_id": item["query_id"], "query": item["query"], "type": item["type"], "retrieved": ids, "matched_sections": matching, "latency_ms": latency_ms})
        latencies.append(latency_ms)

    return {
        "k": k,
        "queries": rows,
        "hit_rate": hit_rate_at_k(retrieved_sections, relevant, k),
        "recall": recall_at_k(retrieved_sections, relevant, k),
        "mrr": mrr_at_k(retrieved_sections, relevant, k),
        "average_latency_ms": statistics.mean(latencies) if latencies else 0.0,
        "p50_latency_ms": statistics.median(latencies) if latencies else 0.0,
        "p95_latency_ms": sorted(latencies)[max(0, int(len(latencies) * 0.95) - 1)] if latencies else 0.0,
    }
