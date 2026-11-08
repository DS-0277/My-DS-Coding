"""Stage 1 candidate retrieval over Markdown documents."""

from pathlib import Path
import hashlib
import re

from .schemas import RetrievedChunk
from .settings import CHROMA_PERSIST_DIR, EMBEDDING_MODEL, RAG_MODE


class DocumentRetriever:
    def __init__(self, docs_dir: str | Path = "docs", chunk_size: int = 700) -> None:
        self.docs_dir = Path(docs_dir)
        self.chunk_size = chunk_size
        self._chunks: list[RetrievedChunk] = []
        self._indexed = False
        self._collection = None
        self._embedder = None

    def index_documents(self) -> None:
        if self._indexed:
            return
        for path in sorted(self.docs_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            words = text.split()
            for offset in range(0, len(words), self.chunk_size):
                content = " ".join(words[offset : offset + self.chunk_size])
                if content:
                    chunk_id = f"{path.stem}:{offset // self.chunk_size + 1}"
                    self._chunks.append(
                        RetrievedChunk(chunk_id=chunk_id, content=content, source="internal_doc")
                    )
        if RAG_MODE == "hybrid":
            import chromadb
            from sentence_transformers import SentenceTransformer

            self._embedder = SentenceTransformer(EMBEDDING_MODEL)
            client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
            self._collection = client.get_or_create_collection("internal_docs")
            existing_data = self._collection.get(include=["metadatas"])
            existing_ids = existing_data.get("ids", [])
            existing_metadata = existing_data.get("metadatas", [])
            known_hashes = {
                chunk_id: (metadata or {}).get("content_hash")
                for chunk_id, metadata in zip(existing_ids, existing_metadata)
            }
            pending = [
                chunk
                for chunk in self._chunks
                if known_hashes.get(chunk.chunk_id)
                != hashlib.sha256(chunk.content.encode("utf-8")).hexdigest()
            ]
            if pending:
                pending_ids = [chunk.chunk_id for chunk in pending]
                pending_documents = [chunk.content for chunk in pending]
                self._collection.upsert(
                    ids=pending_ids,
                    documents=pending_documents,
                    embeddings=self._embedder.encode(pending_documents).tolist(),
                    metadatas=[
                        {"source": "internal_doc", "content_hash": hashlib.sha256(content.encode("utf-8")).hexdigest()}
                        for content in pending_documents
                    ],
                )
        self._indexed = True

    def search(self, query: str, k: int = 20) -> list[RetrievedChunk]:
        self.index_documents()
        if RAG_MODE == "hybrid" and self._collection is not None and self._embedder is not None:
            result = self._collection.query(query_embeddings=[self._embedder.encode(query).tolist()], n_results=k)
            documents = result.get("documents", [[]])[0]
            ids = result.get("ids", [[]])[0]
            distances = result.get("distances", [[]])[0]
            return [RetrievedChunk(chunk_id=i, content=d, score=1.0 / (1.0 + float(dist)), initial_score=1.0 / (1.0 + float(dist)), original_rank=rank, source="internal_doc") for rank, (i, d, dist) in enumerate(zip(ids, documents, distances), 1)]
        query_terms = set(re.findall(r"[a-z0-9_-]+", query.lower()))
        scored: list[RetrievedChunk] = []
        for chunk in self._chunks:
            terms = set(re.findall(r"[a-z0-9_-]+", chunk.content.lower()))
            score = len(query_terms & terms) / max(len(query_terms), 1)
            scored.append(chunk.model_copy(update={"score": score, "initial_score": score}))
        scored.sort(key=lambda item: item.score, reverse=True)
        return [item.model_copy(update={"original_rank": rank}) for rank, item in enumerate(scored[:k], 1)]

