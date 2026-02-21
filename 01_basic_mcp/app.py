"""
MCP Agent Chat Script

Execution Flow:

1. User provides input
2. MCPAgent receives input
3. Agent checks conversation memory
4. Agent decides tool usage via MCPClient
5. Agent calls LLM (ChatGroq)
6. Agent combines tool output + LLM reasoning
7. Agent returns response

Supports:
- Memory
- Tool usage via MCP
- Interactive chat
"""

import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import os

async def run_memory_chat():
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    config_file ="browser_mcp.json"
    print("Initializing chat...")

    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="qwen/qwen3-32b")
    agent = MCPAgent(
        llm=llm,
        client = client,
        max_steps = 15,
        memory_enabled = True,
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the chat.")
    print("type 'clear' to clear conversation history")
    print("--------------------------------")

    try:
        while True : 
            user_input = input("\n You: ")
            if user_input.lower() in ["exit","quit"]:
                print("Ending conversation..")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            print("\n Assistant : ", end="", flush=True)

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

