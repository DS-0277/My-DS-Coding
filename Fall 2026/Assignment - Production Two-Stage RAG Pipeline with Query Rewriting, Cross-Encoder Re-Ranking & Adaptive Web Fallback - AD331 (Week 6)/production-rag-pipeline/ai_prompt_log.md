# AI Prompt and Audit Log

## Initial implementation prompt

You are a Principal AI Systems Architect specializing in production RAG systems.

Design a modular Python 3.11+ two-stage Retrieval-Augmented Generation pipeline with adaptive web-search fallback.

The pipeline must include:

- A query transformation module that rewrites conversational or underspecified questions into precise search queries while preserving technical identifiers.
- Stage 1 broad candidate retrieval from internal Markdown documentation, targeting up to 20 candidates.
- Stage 2 relevance re-ranking, targeting the top 3–5 chunks.
- Cross-encoder-style score normalization using a sigmoid so confidence values are between 0.0 and 1.0.
- A configurable confidence threshold, initially 0.55.
- An internal-document route when confidence is high.
- A web-search fallback route when confidence is low.
- Grounded answer generation with citations to internal chunk IDs or external URLs.
- Typed Pydantic schemas for retrieved chunks, pipeline state, and final responses.
- Modular files for schemas, rewriting, retrieval, re-ranking, web fallback, generation, and pipeline orchestration.
- Safe local fallbacks so the architecture can be tested without requiring API credentials.

The implementation should be clear, typed, testable, and organized for later integration with OpenAI, ChromaDB, a real cross-encoder, and DuckDuckGo or Tavily.

## Initial output summary

The Step 2 draft created:

- `src/schemas.py` for shared data models.
- `src/rewriter.py` for query transformation.
- `src/retriever.py` for internal Markdown retrieval.
- `src/reranker.py` for normalized scoring and confidence gating.
- `src/web_fallback.py` for the external search adapter boundary.
- `src/generator.py` for grounded local answer formatting.
- `src/pipeline.py` for end-to-end orchestration.

The current implementation uses deterministic local behavior so it can be inspected and smoke-tested without an OpenAI or Tavily key. Live providers will be connected in later steps.

## Step 3 audit findings

### 1. Cross-encoder score scaling and normalization — [OK]

The draft applies a sigmoid in `src/reranker.py` before comparing the score with `0.55`. It does not treat raw logits as probabilities. Threshold and `top_k` validation were added, and the hybrid model uses a documented logit calibration bias so the threshold is meaningful for the selected cross-encoder.

### 2. Context-window contamination and prompt injection — [OK] corrected

The initial generator did not explicitly sanitize web text. A malicious result could contain text such as `Ignore previous instructions`. The generator now removes common instruction-like lines and the OpenAI prompt wraps web results in explicit `<untrusted_source>` boundaries.

### 3. Query rewriter latency and failure modes — [OK]

The rewriter rejects empty queries, preserves technical wording, gives the OpenAI request a 15-second timeout, and falls back to the original/local rewrite if the live request fails.

### 4. Vector-store duplication on rerun — [OK]

The retriever uses persistent ChromaDB storage, stable chunk IDs, and SHA-256 content hashes. Unchanged chunks are skipped, while changed chunks are safely upserted instead of duplicated.

## Step 3 corrections

- Added external-content sanitization and untrusted-source boundaries.
- Added validation and calibration for confidence scoring.
- Added OpenAI timeout and safe rewrite fallback behavior.
- Added persistent ChromaDB content-hash checks and upsert behavior.

## Verification

The initial smoke check successfully routed an in-domain query through `INTERNAL_RAG`, produced a normalized confidence score, and passed three selected chunks to the generator. The structured test suite will be added in Step 5.

## Presentation commands

### Local Streamlit demo on port 8500

```bash
cd /Users/sendara/Desktop/production-rag-pipeline
uv run streamlit run src/app.py
```

Open `http://localhost:8500`.

### Docker demo on port 8501

```bash
cd /Users/sendara/Desktop/production-rag-pipeline
docker compose up --build
```

Open `http://localhost:8501`.

### QA test suite

```bash
cd /Users/sendara/Desktop/production-rag-pipeline
uv run pytest -v
```

Expected result: `8 passed`.

