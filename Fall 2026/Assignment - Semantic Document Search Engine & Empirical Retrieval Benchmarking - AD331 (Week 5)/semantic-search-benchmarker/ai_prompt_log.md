# AI Prompt and Audit Log

## Step 1: Environment and Project Layout Summary

Step 1 created the reproducible Python project environment with `uv`, installed the required search and evaluation libraries, and established separate folders for source documents, evaluation data, application code, and tests. The corpus was selected as beginner-friendly HTTP and REST documentation from official MDN pages. The evaluation file contains 15 exact-keyword and conceptual questions with stable section labels used for grading after retrieval.

## Step 2: Exact Initial Prompt Used

The following is the sample initial prompt provided in the assignment. It was used as the specification for the initial draft.

```text
You are a Staff Information Retrieval and Search Engineer. I need a modular Python 3.11+ semantic search and evaluation pipeline that indexes technical Markdown documentation, evaluates multiple chunking strategies, and benchmarks dense vector retrieval against BM25 keyword search.

Requirements:

Ingestion & Chunking (src/chunking.py):
   - Implement FixedSizeChunker(chunk_size: int, chunk_overlap: int) that splits text on whitespace/tokens using tiktoken.

   - Implement StructureAwareChunker() that splits on Markdown headers (#, ##, ###) while preserving code blocks (```) intact inside their parent sections.

   - Each chunk must be a Pydantic model DocumentChunk with: chunk_id (str), content (str), metadata (dict with header hierarchy, line numbers), and parent_doc (str).

Dual Indexing (src/indexer.py):
   - Dense Vector Store: Use ChromaDB (or LanceDB/FAISS) to embed and store chunks using OpenAI's text-embedding-3-small or HuggingFace all-MiniLM-L6-v2. Normalize embeddings to unit length for cosine distance.

   - Sparse Keyword Index: Use rank_bm25.BM25Okapi with tokenized, lower-cased, punctuation-stripped text.

Benchmark Engine (src/benchmarker.py):
   - Ingest an evaluation dataset eval_queries.json with queries and target ground-truth chunk_ids or source header names.

   - Implement retrieval evaluation computing:

     - Hit Rate@K (fraction of queries where target chunk appears in top-K)

     - Recall@K

     - Mean Reciprocal Rank (MRR@K = average of 1 / rank of first relevant chunk)

     - Latency (p50 and p95 query latency in milliseconds)

   - Benchmark 4 configurations across the same dataset:

BM25 (Baseline)
Dense Vector (Small Chunks: 256 tokens)
Dense Vector (Large Chunks: 1024 tokens)
Dense Vector (Structure-Aware Chunking)

Clean Code Standards:
   - Typed functions, clear docstrings, and decoupled search interfaces returning a standardized SearchResult model.

Provide production-grade, well-commented code split into chunking.py, indexer.py, and benchmarker.py.
```

The initial draft was generated from this prompt. The implementation uses the local `all-MiniLM-L6-v2` model and an in-memory NumPy cosine-similarity index for the first draft rather than requiring an external API key or database service.

## Step 2: Prompt Summary

The prompt asked the AI to build a modular retrieval pipeline. It requested two chunking strategies, BM25 and dense-vector indexes, a standardized `SearchResult` model, and benchmark calculations for Hit Rate, Recall, MRR, and latency. It also required typed functions, docstrings, and separate modules for chunking, indexing, and benchmarking.

## Step 3 audit

### 1. Ground-truth leakage: initially passed, then a scoring identity bug was found

The search function receives only the query text. It does not receive `relevant_sections` while retrieving, so the retrieval phase does not peek at the answer key.

However, the initial benchmark compared labels such as `http-request-methods` directly with full chunk IDs such as `http-methods.html:section:4:http-request-methods`. That could mark a correct retrieval as a miss. The benchmark now evaluates the stable `section_id` stored in chunk metadata while still displaying the full chunk ID.

### 2. Cosine distance versus similarity: passed

The dense index normalizes document and query vectors and calculates their dot product. With unit vectors, this is cosine similarity. Results are sorted from highest similarity to lowest similarity, so the ranking direction is correct.

### 3. BM25 tokenization asymmetry: passed

Documents and queries both use the same `tokenize()` function in `src/indexer.py`. It lowercases text and applies the same regular expression to both sides. This prevents differences such as `Cache-Control` and `cache-control?` from being treated inconsistently.

### 4. Code-block slicing: partial risk documented

Structure-aware chunking avoids treating headings inside Markdown fenced code as new sections. However, fixed-size chunking is intentionally token-window based and can split a long code block across two chunks. This is a known limitation of the initial draft and must be addressed or clearly documented during later QA.

### 5. MRR calculation: passed

`mrr_at_k()` gives a relevant result at rank `r` a score of `1 / r`. It assigns `0.0` when no relevant result appears in the top K and does not divide by zero. The deterministic smoke test confirmed the expected result for a rank-two hit and a miss.

## Additional defect found during verification

The original result extraction expression evaluated a dictionary lookup even when the result was an object, which could raise an error for normal `SearchResult` instances. It was replaced with explicit object/dictionary handling in `run_benchmark()`.

## Verification performed

- Python syntax compilation passed.
- Hit Rate and MRR smoke checks passed.
- Corpus loading and structure-aware chunk creation passed.
- The source manifest and teaching sample are excluded from searchable corpus documents.

## Step 5 QA Verification

The automated suite runs in the project terminal with `uv run pytest -v`. It covers fixed-chunk overlap, code-fence preservation, fixed-chunk section metadata, exact BM25 identifier retrieval, consistent tokenization, Hit Rate/Recall/MRR mathematics, and zero MRR for a miss. Final result: **7 passed**.
