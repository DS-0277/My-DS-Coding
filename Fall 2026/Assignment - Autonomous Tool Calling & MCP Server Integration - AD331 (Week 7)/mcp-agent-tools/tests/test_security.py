"""Security regression tests for SQL and math tools."""

import json

import pytest

from server.tools.math_tool import calculate_expression
from server.tools.sql_tool import query_database


@pytest.mark.parametrize(
    "query",
    [
        "DROP TABLE inventory",
        "UPDATE inventory SET quantity = 0",
        "INSERT INTO inventory VALUES (99, 1, 'Seattle', 0, 0)",
        "SELECT * FROM orders; DROP TABLE inventory;--",
    ],
)
def test_sql_ddl_dml_rejection(query: str) -> None:
    result = json.loads(query_database(query))
    assert "error" in result


@pytest.mark.parametrize(
    "expression",
    [
        '__import__("os").listdir(".")',
        'open(".env").read()',
        'exec("import os")',
    ],
)
def test_arbitrary_code_execution_block(expression: str) -> None:
    result = json.loads(calculate_expression(expression))
    assert "error" in result
