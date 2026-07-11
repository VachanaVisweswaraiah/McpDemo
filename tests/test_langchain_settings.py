import pytest

from mcpdemo.langchain_settings import LangChainAgentSettings


def test_langchain_settings_requires_groq_api_key():
    with pytest.raises(RuntimeError, match="GROQ_API_KEY"):
        LangChainAgentSettings.from_env({})


def test_langchain_settings_builds_mcp_server_config():
    settings = LangChainAgentSettings.from_env(
        {
            "GROQ_API_KEY": "test-key",
            "GROQ_MODEL": "test-model",
            "MCP_WEATHER_URL": "http://localhost:9000/mcp",
        }
    )

    assert settings.groq_model == "test-model"
    assert settings.mcp_servers()["weather"]["url"] == "http://localhost:9000/mcp"
    assert settings.mcp_servers()["math"]["transport"] == "stdio"
