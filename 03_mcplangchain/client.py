import asyncio
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from mcpdemo.langchain_settings import LangChainAgentSettings


async def main():
    load_dotenv()
    settings = LangChainAgentSettings.from_env()
    os.environ["GROQ_API_KEY"] = settings.groq_api_key

    client = MultiServerMCPClient(settings.mcp_servers())

    tools = await client.get_tools()
    model = ChatGroq(model=settings.groq_model)
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
