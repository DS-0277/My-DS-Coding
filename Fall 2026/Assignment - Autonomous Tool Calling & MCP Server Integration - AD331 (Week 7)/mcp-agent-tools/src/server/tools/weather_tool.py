"""Weather and geocoding tool using Open-Meteo."""

import json
import httpx


async def get_current_weather(city: str) -> str:
    """Geocode a city and return a compact current-conditions summary."""
    city = city.strip()
    if not city or len(city) > 100:
        return json.dumps({"error": "City must be between 1 and 100 characters."})

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            geocode_response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "en", "format": "json"},
            )
            geocode_response.raise_for_status()
            locations = geocode_response.json().get("results", [])
            if not locations:
                return json.dumps({"error": f"No location found for {city}."})

            location = locations[0]
            forecast_response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "current": "temperature_2m,precipitation,wind_speed_10m,weather_code",
                    "temperature_unit": "fahrenheit",
                    "wind_speed_unit": "mph",
                },
            )
            forecast_response.raise_for_status()
            current = forecast_response.json().get("current", {})
    except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
        return json.dumps({"error": f"Weather service request failed: {exc}"})

    return json.dumps({
        "city": location.get("name", city),
        "country": location.get("country"),
        "temperature": current.get("temperature_2m"),
        "precipitation": current.get("precipitation"),
        "wind_speed": current.get("wind_speed_10m"),
        "weather_code": current.get("weather_code"),
    })
