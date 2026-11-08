# Production Two-Stage RAG Pipeline

This project implements the initial draft of a query-rewriting, two-stage retrieval-augmented generation pipeline with confidence-based web fallback.

## Step 1 status

The initial draft includes typed schemas, a deterministic query rewriter, Markdown document retrieval, sigmoid-normalized re-ranking, confidence gating, a web-fallback adapter boundary, grounded local synthesis, and pipeline orchestration. Live OpenAI and web-provider calls are intentionally configuration-dependent.

## Selected hybrid architecture

The final target architecture uses OpenAI for query rewriting and answer generation, local Sentence Transformer models for embeddings and cross-encoder re-ranking, ChromaDB for persistent vector storage, and DuckDuckGo for key-free web fallback. `RAG_MODE=local` keeps the deterministic demo available; `RAG_MODE=hybrid` enables the live model adapters after their configuration is completed.

To enable the hybrid adapters, add this non-secret setting to `.env`:

```env
RAG_MODE=hybrid
```

The first hybrid run downloads the selected local model weights and may take longer than local mode. OpenAI calls are only made when hybrid mode is enabled.

## Local smoke check

```bash
uv run python -m compileall -q src
uv run python -c 'from src.pipeline import RAGPipeline; print(RAGPipeline().run("How do I deploy a service safely?").route_taken)'
```

## Streamlit interface

```bash
uv run streamlit run src/app.py
```

The interface runs on port 8500 by default and displays the transformed query, Stage 1 candidates, Stage 2 scores, confidence threshold, route decision, and grounded citations. DuckDuckGo provides the no-key web fallback.

## QA test suite

```bash
uv run pytest -v
```

The tests automatically force deterministic local mode, so they do not call OpenAI or download model weights. They cover conversational rewriting, score normalization, confidence gating, internal routing, web fallback routing, and web prompt-injection filtering.

## Docker demo

Build and start the container:

```bash
docker compose up --build
```

Open the application at `http://localhost:8501`. Docker maps host port 8501 to Streamlit's container port 8500. Stop it with:

```bash
docker compose down
```

