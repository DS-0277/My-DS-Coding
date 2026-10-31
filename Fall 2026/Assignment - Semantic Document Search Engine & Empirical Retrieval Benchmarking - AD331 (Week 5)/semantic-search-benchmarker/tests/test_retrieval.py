from src.chunking import DocumentChunk
from src.indexer import BM25Index


def test_bm25_finds_exact_identifier_first() -> None:
    chunks = [
        DocumentChunk(chunk_id="a", content="The CUSTOM_CONFIG_FLAG_XYZ enables caching.", parent_doc="doc"),
        DocumentChunk(chunk_id="b", content="The server supports ordinary requests.", parent_doc="doc"),
        DocumentChunk(chunk_id="c", content="The server handles response headers.", parent_doc="doc"),
        DocumentChunk(chunk_id="d", content="The server returns status codes.", parent_doc="doc"),
    ]
    results = BM25Index(chunks).search("CUSTOM_CONFIG_FLAG_XYZ", top_k=1)
    assert results[0].chunk_id == "a"


def test_bm25_uses_consistent_tokenization() -> None:
    chunks = [DocumentChunk(chunk_id="a", content="Use Cache-Control for caching.", parent_doc="doc")]
    results = BM25Index(chunks).search("what does cache-control? do", top_k=1)
    assert results[0].chunk_id == "a"
