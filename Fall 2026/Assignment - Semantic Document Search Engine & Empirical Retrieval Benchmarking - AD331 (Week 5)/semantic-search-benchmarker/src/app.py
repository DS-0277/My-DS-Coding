"""Streamlit interface for live search comparison and benchmark results."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.benchmarker import load_queries, run_benchmark  # noqa: E402
from src.chunking import FixedSizeChunker, StructureAwareChunker, load_corpus  # noqa: E402
from src.indexer import BM25Index, DenseVectorIndex  # noqa: E402


st.set_page_config(page_title="SearchWorkbench", page_icon="🔎", layout="wide")
st.title("SearchWorkbench")
st.caption("Compare lexical BM25 retrieval with semantic vector retrieval over HTTP and REST documentation.")


@st.cache_data
def corpus_texts() -> list[tuple[str, str]]:
    return load_corpus(ROOT / "corpus")


@st.cache_resource
def build_search_indexes(strategy: str, chunk_size: int):
    all_chunks = []
    for name, text in corpus_texts():
        if strategy == "Structure-aware":
            chunks = StructureAwareChunker().split(text, name)
        else:
            chunks = FixedSizeChunker(chunk_size=chunk_size, chunk_overlap=max(1, chunk_size // 8)).split(text, name)
        all_chunks.extend(chunks)
    return BM25Index(all_chunks), DenseVectorIndex(all_chunks)


def render_results(title: str, results) -> None:
    st.subheader(title)
    if not results:
        st.info("No results returned.")
        return
    for result in results:
        section = result.metadata.get("section_id") or result.metadata.get("headers") or result.chunk_id
        with st.container(border=True):
            st.markdown(f"**Rank {result.rank} · Score {result.score:.4f}**")
            st.caption(f"Section: {section} · Source: {result.chunk_id.split(':')[0]}")
            st.write(result.content[:1200] + ("…" if len(result.content) > 1200 else ""))


def live_search() -> None:
    st.header("Live Search Comparator")
    query = st.text_input("Enter an HTTP/REST question", "Which HTTP method retrieves a resource?")
    left, right = st.columns(2)
    with left:
        strategy = st.selectbox("Chunking strategy", ["Structure-aware", "Fixed-size"], key="live_strategy")
    with right:
        top_k = st.slider("Results to show", 1, 10, 5)
    chunk_size = 256 if strategy == "Fixed-size" else 512
    if st.button("Search", type="primary"):
        with st.spinner("Building indexes and searching…"):
            bm25, dense = build_search_indexes(strategy, chunk_size)
            bm25_results = bm25.search(query, top_k)
            dense_results = dense.search(query, top_k)
        col1, col2 = st.columns(2)
        with col1:
            render_results("BM25 keyword search", bm25_results)
        with col2:
            render_results("Dense vector search", dense_results)


def benchmark_dashboard() -> None:
    st.header("Benchmark & Evaluation Dashboard")
    k = st.slider("Evaluate top K", 1, 10, 5, key="benchmark_k")
    if not st.button("Run Benchmark", type="primary"):
        st.info("Click Run Benchmark to evaluate the 15 labeled queries.")
        return

    queries = load_queries(ROOT / "data" / "eval_queries.json")
    configurations = [("BM25 · structure-aware", "Structure-aware", 512, "bm25"), ("Dense · 256 tokens", "Fixed-size", 256, "dense"), ("Dense · 1024 tokens", "Fixed-size", 1024, "dense"), ("Dense · structure-aware", "Structure-aware", 512, "dense")]
    summaries = []
    failures = []
    with st.spinner("Running the evaluation suite…"):
        for name, strategy, size, method in configurations:
            bm25, dense = build_search_indexes(strategy, size)
            index = bm25 if method == "bm25" else dense
            result = run_benchmark(queries, index.search, k)
            summaries.append({"Configuration": name, "Hit Rate": result["hit_rate"], "Recall": result["recall"], "MRR": result["mrr"], "Average latency (ms)": result["average_latency_ms"], "p50 (ms)": result["p50_latency_ms"], "p95 (ms)": result["p95_latency_ms"]})
            for row in result["queries"]:
                if not row["matched_sections"]:
                    failures.append({"Configuration": name, "Query ID": row["query_id"], "Query": row["query"], "Expected": ", ".join(queries[int(row["query_id"][1:]) - 1]["relevant_sections"]), "Retrieved": ", ".join(row["retrieved"][:3])})

    frame = pd.DataFrame(summaries)
    st.dataframe(frame.style.format({"Hit Rate": "{:.2%}", "Recall": "{:.2%}", "MRR": "{:.3f}", "Average latency (ms)": "{:.2f}", "p50 (ms)": "{:.2f}", "p95 (ms)": "{:.2f}"}), use_container_width=True)
    st.subheader("Ranking quality")
    st.bar_chart(frame.set_index("Configuration")[["Hit Rate", "MRR"]])
    st.subheader("Failure analysis")
    st.dataframe(pd.DataFrame(failures), use_container_width=True)


tab_live, tab_benchmark = st.tabs(["Live Search", "Benchmark Dashboard"])
with tab_live:
    live_search()
with tab_benchmark:
    benchmark_dashboard()
