"""Streamlit interface for inspecting the RAG pipeline."""

import sys
from pathlib import Path

import streamlit as st

# Streamlit executes this file as a script, so make the project root importable
# before loading the package-style source modules.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generator import GroundedGenerator
from src.pipeline import RAGPipeline


st.set_page_config(page_title="Production RAG Pipeline", page_icon="🔎", layout="wide")


@st.cache_resource
def get_pipeline() -> RAGPipeline:
    return RAGPipeline()


pipeline = get_pipeline()

st.title("Production Two-Stage RAG Pipeline")
st.caption("Inspect query rewriting, candidate retrieval, re-ranking, confidence gating, and citations.")

with st.sidebar:
    st.header("Pipeline settings")
    st.metric("Confidence threshold", f"{pipeline.reranker.threshold:.2f}")
    st.write("Stage 1 candidate limit: 20")
    st.write(f"Stage 2 display limit: {pipeline.reranker.top_k}")
    st.info("The current Step 4 demo uses local deterministic rewriting, retrieval, and generation.")

query = st.text_area("Ask a question", placeholder="How do I deploy a service safely?")
use_context = st.checkbox("Include conversation context")
context = st.text_area("Previous context", disabled=not use_context, placeholder="Earlier discussion about staging deployments...")

if st.button("Run pipeline", type="primary", disabled=not query.strip()):
    transformed = pipeline.rewriter.rewrite(query, context if use_context else None)
    stage_one = pipeline.retriever.search(transformed, k=20)
    reranked, confidence, low_confidence = pipeline.reranker.rerank(transformed, stage_one)

    st.subheader("Pipeline decision")
    left, middle, right = st.columns(3)
    left.metric("Confidence", f"{confidence:.3f}", f"threshold {pipeline.reranker.threshold:.2f}")
    middle.metric("Route", "WEB_FALLBACK" if low_confidence else "INTERNAL_RAG")
    right.metric("Final chunks", 3)
    st.write("**Transformed query:**", transformed)

    with st.expander("Stage 1 — broad retrieval candidates", expanded=False):
        st.dataframe(
            [
                {
                    "rank": chunk.original_rank,
                    "chunk_id": chunk.chunk_id,
                    "initial_score": round(chunk.initial_score or 0.0, 3),
                    "preview": chunk.content[:180],
                }
                for chunk in stage_one
            ],
            use_container_width=True,
            hide_index=True,
        )

    with st.expander("Stage 2 — re-ranked candidates", expanded=True):
        st.dataframe(
            [
                {
                    "new_rank": rank,
                    "original_rank": chunk.original_rank,
                    "chunk_id": chunk.chunk_id,
                    "reranked_score": round(chunk.score, 3),
                    "preview": chunk.content[:180],
                }
                for rank, chunk in enumerate(reranked, 1)
            ],
            use_container_width=True,
            hide_index=True,
        )

    try:
        if low_confidence:
            selected = pipeline.web_fallback.search(transformed, limit=3)
            route = "WEB_FALLBACK"
        else:
            selected = reranked[:3]
            route = "INTERNAL_RAG"
        answer, citations = GroundedGenerator().generate(transformed, selected)
        st.subheader("Grounded answer")
        st.write(answer)
        st.subheader("Citations")
        for citation in citations:
            if citation.startswith("http"):
                st.markdown(f"- [{citation}]({citation})")
            else:
                st.write(f"- `{citation}`")
    except RuntimeError as exc:
        st.warning(str(exc))
        st.info("Configure a web-search provider before demonstrating WEB_FALLBACK.")

