from conftest import load_module

weather_server = load_module(
    "weather_server_under_test",
    "02_mcpcrashcourse/mcpserver/server.py",
)


def test_format_alert_uses_defaults_for_missing_fields():
    alert = weather_server.format_alert({"properties": {"event": "Flood Watch"}})

    assert "Event: Flood Watch" in alert
    assert "Area: Unknown" in alert
    assert "No description available" in alert
    assert "No specific instructions provided" in alert


async def test_get_alerts_returns_no_active_alerts(monkeypatch):
    async def fake_request(url: str):
        assert url.endswith("/alerts/active/area/CA")
        return {"features": []}

    monkeypatch.setattr(weather_server, "make_nws_request", fake_request)

    assert await weather_server.get_alerts("CA") == "No active alerts for this state."


async def test_get_alerts_formats_active_alerts(monkeypatch):
    async def fake_request(url: str):
        assert url.endswith("/alerts/active/area/NY")
        return {
            "features": [
                {
                    "properties": {
                        "event": "Winter Storm Warning",
                        "areaDesc": "Albany",
                        "severity": "Severe",
                        "description": "Heavy snow expected.",
                        "instruction": "Avoid travel.",
                    }
                }
            ]
        }

    monkeypatch.setattr(weather_server, "make_nws_request", fake_request)

    result = await weather_server.get_alerts("NY")

    assert "Winter Storm Warning" in result
    assert "Albany" in result
    assert "Avoid travel." in result


async def test_get_forecast_formats_first_five_periods(monkeypatch):
    async def fake_request(url: str):
        if url.endswith("/points/38.9,-77.0"):
            return {"properties": {"forecast": "https://api.weather.gov/gridpoints/test"}}
        return {
            "properties": {
                "periods": [
                    {
                        "name": f"Period {index}",
                        "temperature": 70 + index,
                        "temperatureUnit": "F",
                        "windSpeed": "5 mph",
                        "windDirection": "NW",
                        "detailedForecast": f"Forecast {index}",
                    }
                    for index in range(6)
                ]
            }
        }

    monkeypatch.setattr(weather_server, "make_nws_request", fake_request)

    result = await weather_server.get_forecast(38.9, -77.0)

    assert "Period 0" in result
    assert "Forecast 4" in result
    assert "Period 5" not in result
