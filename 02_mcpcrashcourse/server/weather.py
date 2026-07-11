from mcp.server.fastmcp import FastMCP

from mcpdemo.weather_tools import alerts_url, format_alert, make_nws_request

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    data = await make_nws_request(alerts_url(state))

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource."""
    return f"Resource echo: {message}"
