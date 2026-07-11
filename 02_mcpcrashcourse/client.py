import asyncio
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient


async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY is required. Add it to your environment or .env file.")
    os.environ["GROQ_API_KEY"] = groq_api_key

    config_file = "weather.json"

    print("Initializing chat...")

    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="qwen-qwq-32b")

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")

    try:
        # Main chat loop
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            print("\nAssistant: ", end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())
