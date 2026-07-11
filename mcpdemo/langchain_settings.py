from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True)
class LangChainAgentSettings:
    groq_api_key: str
    groq_model: str = "qwen-qwq-32b"
    weather_url: str = "http://localhost:8000/mcp"
    math_command: str = "uv"
    math_args: tuple[str, ...] = field(default=("run", "python", "mathserver.py"))

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> LangChainAgentSettings:
        source = env or os.environ
        groq_api_key = source.get("GROQ_API_KEY")
        if not groq_api_key:
            raise RuntimeError("GROQ_API_KEY is required. Add it to your environment or .env file.")

        return cls(
            groq_api_key=groq_api_key,
            groq_model=source.get("GROQ_MODEL", cls.groq_model),
            weather_url=source.get("MCP_WEATHER_URL", cls.weather_url),
            math_command=source.get("MCP_MATH_COMMAND", cls.math_command),
            math_args=tuple(source.get("MCP_MATH_ARGS", " ".join(cls.math_args)).split()),
        )

    def mcp_servers(self) -> dict[str, dict[str, object]]:
        return {
            "math": {
                "command": self.math_command,
                "args": list(self.math_args),
                "transport": "stdio",
            },
            "weather": {
                "url": self.weather_url,
                "transport": "streamable_http",
            },
        }
