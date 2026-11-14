"""Tests for the individual MCP tool implementations."""

import json

import pytest

from server.tools.math_tool import calculate_expression
from server.tools.sql_tool import query_database
from server.tools import weather_tool


def test_sql_read_accuracy() -> None:
    result = json.loads(
        query_database(
            "SELECT quantity FROM inventory "
            "WHERE city = 'Seattle' AND product_id = 1"
        )
    )
    assert result["rows"] == [{"quantity": 28}]


@pytest.mark.asyncio
async def test_weather_api_formatting(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeResponse:
        def __init__(self, payload: dict) -> None:
            self.payload = payload

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return self.payload

    class FakeAsyncClient:
        def __init__(self, **kwargs: object) -> None:
            self.kwargs = kwargs

        async def __aenter__(self) -> "FakeAsyncClient":
            return self

        async def __aexit__(self, *args: object) -> None:
            return None

        async def get(self, url: str, params: dict) -> FakeResponse:
            if "geocoding" in url:
                return FakeResponse(
                    {"results": [{"name": "Seattle", "country": "United States", "latitude": 47.6, "longitude": -122.3}]}
                )
            return FakeResponse(
                {"current": {"temperature_2m": 55.0, "precipitation": 0.2, "wind_speed_10m": 7.5, "weather_code": 61}}
            )

    monkeypatch.setattr(weather_tool.httpx, "AsyncClient", FakeAsyncClient)
    result = json.loads(await weather_tool.get_current_weather("Seattle"))
    assert result["city"] == "Seattle"
    assert result["temperature"] == 55.0
    assert result["precipitation"] == 0.2
    assert result["weather_code"] == 61


def test_math_evaluator_precision() -> None:
    result = json.loads(calculate_expression("2 + 3 * (4 - 1) ** 2"))
    assert result["result"] == 29
