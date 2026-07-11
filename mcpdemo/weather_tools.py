from typing import Any

import httpx

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


def alerts_url(state: str) -> str:
    return f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"


def points_url(latitude: float, longitude: float) -> str:
    return f"{NWS_API_BASE}/points/{latitude},{longitude}"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the National Weather Service API."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict[str, Any]) -> str:
    props = feature["properties"]
    return "\n".join(
        [
            f"Event: {props.get('event', 'Unknown')}",
            f"Area: {props.get('areaDesc', 'Unknown')}",
            f"Severity: {props.get('severity', 'Unknown')}",
            f"Description: {props.get('description', 'No description available')}",
            f"Instructions: {props.get('instruction', 'No specific instructions provided')}",
        ]
    )


def format_forecast_period(period: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"{period['name']}:",
            f"Temperature: {period['temperature']} {period['temperatureUnit']}",
            f"Wind: {period['windSpeed']} {period['windDirection']}",
            f"Forecast: {period['detailedForecast']}",
        ]
    )


def format_forecast_periods(periods: list[dict[str, Any]], limit: int = 5) -> str:
    return "\n---\n".join(format_forecast_period(period) for period in periods[:limit])
