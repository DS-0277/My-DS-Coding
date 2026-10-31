from src.chunking import FixedSizeChunker, StructureAwareChunker


def test_fixed_chunk_overlap_is_preserved() -> None:
    chunks = FixedSizeChunker(chunk_size=10, chunk_overlap=3).split(" ".join(f"w{i}" for i in range(30)), "doc.md")
    first = chunks[0].content.split()
    second = chunks[1].content.split()
    assert first[-3:] == second[:3]


def test_structure_chunker_keeps_code_fence_inside_section() -> None:
    text = "## Example\n\n```json\n{\"method\": \"GET\"}\n```\n\n## Next\nText."
    chunks = StructureAwareChunker().split(text, "doc.md")
    assert len(chunks) == 2
    assert "```json" in chunks[0].content
    assert chunks[0].content.count("```") == 2


def test_fixed_chunks_keep_section_metadata() -> None:
    text = "## HTTP Methods\nGET retrieves data.\n\n## Status Codes\n404 means missing."
    chunks = FixedSizeChunker(chunk_size=4, chunk_overlap=1).split(text, "doc.md")
    assert any(chunk.metadata.get("section_id") == "http-methods" for chunk in chunks)
    assert any(chunk.metadata.get("section_id") == "status-codes" for chunk in chunks)
