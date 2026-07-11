from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_math_server_stdio_transport_lists_and_calls_tools():
    server_path = Path("03_mcplangchain/mathserver.py")
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", str(server_path)],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tool_names = {tool.name for tool in tools_result.tools}

            assert {"add", "multiple"}.issubset(tool_names)

            result = await session.call_tool("add", arguments={"a": 3, "b": 5})

            assert result.content[0].text == "8"
