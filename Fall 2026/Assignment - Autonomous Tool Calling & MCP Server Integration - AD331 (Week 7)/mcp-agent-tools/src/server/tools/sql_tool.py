"""Secure read-only SQLite query tool."""

import json
from pathlib import Path
import re
import sqlite3


DATABASE_PATH = Path(__file__).resolve().parents[3] / "data" / "enterprise_ops.db"
_SELECT_START = re.compile(r"^\s*select\b", re.IGNORECASE)
_BLOCKED_WORDS = re.compile(
    r"\b(drop|delete|update|insert|alter|truncate|attach|detach|replace|vacuum|reindex| pragma)\b",
    re.IGNORECASE,
)


def query_database(sql_query: str) -> str:
    """Run one safe SELECT query against a read-only SQLite connection."""
    normalized = sql_query.strip()
    if not _SELECT_START.match(normalized):
        return json.dumps({"error": "Only SELECT statements are allowed."})
    if ";" in normalized.rstrip(";"):
        return json.dumps({"error": "Multiple SQL statements are not allowed."})
    if _BLOCKED_WORDS.search(normalized):
        return json.dumps({"error": "The query contains a blocked SQL operation."})
    if normalized.endswith(";"):
        normalized = normalized[:-1].rstrip()

    uri = f"file:{DATABASE_PATH}?mode=ro"
    try:
        with sqlite3.connect(uri, uri=True, timeout=2.0) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(normalized).fetchall()
    except sqlite3.Error as exc:
        return json.dumps({"error": f"Database query failed: {exc}"})

    if not rows:
        return json.dumps({"columns": [], "rows": []})

    columns = rows[0].keys()
    values = [dict(row) for row in rows]
    return json.dumps({"columns": list(columns), "rows": values})
