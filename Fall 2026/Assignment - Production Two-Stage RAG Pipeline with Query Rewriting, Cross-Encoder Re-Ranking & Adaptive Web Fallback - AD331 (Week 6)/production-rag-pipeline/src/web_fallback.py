"""External search fallback adapters."""

from duckduckgo_search import DDGS

from .schemas import RetrievedChunk


class WebFallback:
    def search(self, query: str, limit: int = 3) -> list[RetrievedChunk]:
        """Search DuckDuckGo and convert results into trusted pipeline objects."""
        if not query.strip():
            return []

        try:
            results = list(DDGS().text(query, max_results=limit))
        except Exception as exc:
            raise RuntimeError(f"DuckDuckGo search failed: {exc}") from exc

        chunks: list[RetrievedChunk] = []
        for index, result in enumerate(results[:limit], 1):
            url = result.get("href") or result.get("url")
            content = result.get("body") or result.get("snippet") or result.get("title") or ""
            if not url or not content:
                continue
            chunks.append(
                RetrievedChunk(
                    chunk_id=f"web:{index}",
                    content=content,
                    source="web",
                    url=url,
                    score=1.0 / index,
                )
            )
        return chunks

