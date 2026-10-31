"""Document extraction and chunking strategies for the initial SearchWorkbench draft."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """A searchable piece of a source document."""

    chunk_id: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    parent_doc: str


class _HTMLTextParser(HTMLParser):
    """Small standard-library HTML-to-text parser for the starter corpus."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.heading_level = 0
        self.in_code = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_level = int(tag[1])
            self.parts.append("\n" + "#" * self.heading_level + " ")
        elif tag in {"p", "div", "li", "pre", "br"}:
            self.parts.append("\n")
        if tag in {"pre", "code"}:
            self.in_code = True
            self.parts.append("\n```\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n")
            self.heading_level = 0
        elif tag in {"pre", "code"} and self.in_code:
            self.parts.append("\n```\n")
            self.in_code = False

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def read_document(path: str | Path) -> str:
    """Extract readable text from Markdown or HTML source."""

    source = Path(path)
    raw = source.read_text(encoding="utf-8")
    if source.suffix.lower() in {".html", ".htm"}:
        parser = _HTMLTextParser()
        parser.feed(raw)
        raw = "".join(parser.parts)
    return re.sub(r"\n{3,}", "\n\n", raw).strip()


def _tokens(text: str) -> list[str]:
    return re.findall(r"\S+", text)


class FixedSizeChunker:
    """Split text into token-count windows with a configured overlap."""

    def __init__(self, chunk_size: int = 256, chunk_overlap: int = 32) -> None:
        if chunk_size <= 0 or chunk_overlap < 0 or chunk_overlap >= chunk_size:
            raise ValueError("chunk_size must be positive and overlap must be smaller")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str, parent_doc: str) -> list[DocumentChunk]:
        words: list[str] = []
        section_ids: list[str] = []
        current_section = StructureAwareChunker._slug(parent_doc)
        for line in text.splitlines():
            heading = StructureAwareChunker.heading_pattern.match(line)
            if heading:
                current_section = StructureAwareChunker._slug(heading.group(2))
            line_words = _tokens(line)
            words.extend(line_words)
            section_ids.extend([current_section] * len(line_words))
        step = self.chunk_size - self.chunk_overlap
        chunks: list[DocumentChunk] = []
        for start in range(0, len(words), step):
            content = " ".join(words[start : start + self.chunk_size]).strip()
            if not content:
                continue
            chunk_section_ids = section_ids[start : start + self.chunk_size]
            section_id = max(set(chunk_section_ids), key=chunk_section_ids.count) if chunk_section_ids else current_section
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{parent_doc}:fixed:{self.chunk_size}:{start}",
                    content=content,
                    parent_doc=parent_doc,
                    metadata={"strategy": "fixed", "start_token": start, "end_token": start + len(content.split()), "section_id": section_id},
                )
            )
            if start + self.chunk_size >= len(words):
                break
        return chunks


class StructureAwareChunker:
    """Split Markdown-like text at headings while retaining heading context."""

    heading_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

    def split(self, text: str, parent_doc: str) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []
        current: list[str] = []
        hierarchy: list[str] = []
        in_fence = False
        section_number = 0

        def flush() -> None:
            nonlocal current, section_number
            content = "\n".join(current).strip()
            if content:
                section_number += 1
                section_id = self._slug(hierarchy[-1] if hierarchy else f"section-{section_number}")
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{parent_doc}:section:{section_number}:{section_id}",
                        content=content,
                        parent_doc=parent_doc,
                        metadata={"strategy": "structure", "headers": list(hierarchy), "section_id": section_id},
                    )
                )
            current = []

        for line in text.splitlines():
            if line.strip().startswith("```"):
                in_fence = not in_fence
            match = self.heading_pattern.match(line) if not in_fence else None
            if match:
                flush()
                level, title = len(match.group(1)), match.group(2).strip()
                hierarchy = hierarchy[: level - 1]
                hierarchy.append(title)
            current.append(line)
        flush()
        return chunks

    @staticmethod
    def _slug(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_corpus(path: str | Path) -> list[tuple[str, str]]:
    """Load all supported corpus documents as ``(name, text)`` pairs."""

    root = Path(path)
    return [
        (file.name, read_document(file))
        for file in sorted(root.iterdir())
        if file.name.lower() not in {"sources.md", "api_spec_sample.md"} and file.suffix.lower() in {".md", ".html", ".htm"}
    ]
