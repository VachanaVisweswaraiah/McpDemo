import asyncio
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


async def main():
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY is required. Add it to your environment or .env file.")
    os.environ["GROQ_API_KEY"] = groq_api_key

    client = MultiServerMCPClient(
        {
            "math": {
                "command": "uv",
                "args": ["run", "python", "mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    tools = await client.get_tools()
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print("Math response:", math_response["messages"][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("Weather response:", weather_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
