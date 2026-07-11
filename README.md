# MCP Demo: AI Tooling and Agent Orchestration

<p>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-blue.svg">
  <img alt="Model Context Protocol" src="https://img.shields.io/badge/MCP-Model%20Context%20Protocol-black.svg">
  <img alt="LangChain" src="https://img.shields.io/badge/LangChain-Agent%20Orchestration-green.svg">
  <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-ReAct%20Agents-purple.svg">
  <img alt="uv" src="https://img.shields.io/badge/uv-Dependency%20Management-orange.svg">
  <img alt="CI" src="https://img.shields.io/badge/CI-Ruff%20%2B%20Pytest-informational.svg">
</p>

Python examples for building Model Context Protocol (MCP) servers, connecting MCP clients, and orchestrating tools through LangChain/LangGraph agents.

This repository is meant to be easy for another developer to clone, run, understand, and extend. It keeps the README focused on the information needed to work on the project, while the longer walkthrough lives in `PROJECT_ANALYSIS.md`.

## What This Demonstrates

- Builds custom MCP tools and resources with `FastMCP`.
- Demonstrates multiple MCP transports: `stdio`, `sse`, and `streamable-http`.
- Connects MCP servers to direct clients and LangChain/LangGraph ReAct agents.
- Uses `uv` with a locked dependency graph for repeatable local setup.
- Includes deterministic tests plus a stdio MCP transport integration test.
- Keeps CI in place with Ruff and Pytest checks.

## Project Map

```text
McpDemo/
├── 01_basic_mcp/              # Config-driven client using external MCP servers
├── 02_mcpcrashcourse/
│   ├── server/weather.py      # FastMCP weather alerts + echo resource
│   ├── mcpserver/server.py    # Weather alerts + forecast MCP server
│   ├── mcpserver/client-*.py  # stdio and SSE clients
│   └── weather.json           # Portable MCP server config
├── 03_mcplangchain/
│   ├── mathserver.py          # FastMCP math tools
│   ├── weather.py             # Streamable HTTP weather tool
│   └── client.py              # LangChain multi-server agent client
├── mcpdemo/                   # Shared weather helpers and typed config
├── tests/                     # Unit tests for deterministic behavior
├── .github/workflows/ci.yml   # Ruff + Pytest workflow
├── pyproject.toml             # Project metadata and dependencies
└── uv.lock                    # Locked dependency graph
```

## Where To Work

| Goal | Start here | Notes |
| --- | --- |
| Add or change weather MCP tools | `02_mcpcrashcourse/mcpserver/server.py` | Main weather server with `get_alerts` and `get_forecast` |
| Reuse weather formatting/request logic | `mcpdemo/weather_tools.py` | Shared National Weather Service helpers used by weather servers |
| Test deterministic and transport behavior | `tests/` | Tests mock external calls and include a stdio MCP server/client check |
| Experiment with MCP transports | `02_mcpcrashcourse/mcpserver/client-stdio.py`, `client-sse.py` | Direct client examples for `stdio` and `sse` |
| Add LangChain agent behavior | `03_mcplangchain/client.py` | Aggregates MCP tools through `MultiServerMCPClient` |
| Change LangChain provider/model settings | `mcpdemo/langchain_settings.py` | Typed settings from environment variables |
| Add simple MCP tools | `03_mcplangchain/mathserver.py` | Small deterministic tool server, useful for testing orchestration |
| Change dependencies or tooling | `pyproject.toml` | Runtime/dev dependencies, Ruff, and Pytest config |

## Quick Start

Prerequisites:

- Python `3.11+`
- `uv`
- Node.js + `npx` for the external servers used by `01_basic_mcp/browser_mcp.json`
- Optional: `GROQ_API_KEY` in `.env` for LLM-backed clients

```bash
git clone <repo-url>
cd McpDemo
uv sync --all-groups
```

Optional `.env`:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=qwen-qwq-32b
MCP_WEATHER_URL=http://localhost:8000/mcp
```

## Verify The Project

Run these checks before opening a PR:

```bash
uv sync --frozen --all-groups
uv run ruff check .
uv run pytest
```

The GitHub Actions workflow runs the same lint and test checks on pushes and pull requests.

## Run Examples

| Workflow | Run from | Command |
| --- | --- | --- |
| Basic external MCP chat | `01_basic_mcp/` | `uv run python app.py` |
| Weather MCP Inspector | repo root | `uv run mcp dev 02_mcpcrashcourse/server/weather.py` |
| Weather stdio client | `02_mcpcrashcourse/mcpserver/` | `uv run python client-stdio.py` |
| Weather SSE server | repo root | `uv run python 02_mcpcrashcourse/mcpserver/server.py` |
| Weather SSE client | repo root | `uv run python 02_mcpcrashcourse/mcpserver/client-sse.py` |
| LangChain weather server | repo root | `uv run python 03_mcplangchain/weather.py` |
| LangChain multi-server client | `03_mcplangchain/` | `uv run python client.py` |

## Example Tool Surface

- `get_alerts(state: str)` - fetches and formats active US weather alerts.
- `get_forecast(latitude: float, longitude: float)` - resolves a weather grid point and returns forecast periods.
- `add(a: int, b: int)` - deterministic MCP math tool.
- `multiple(a: int, b: int)` - deterministic MCP math tool.
- `get_weather(location: str)` - simple streamable HTTP weather tool for agent demos.
- `echo://{message}` - MCP resource example.

## Development Notes

- Keep `uv` as the single dependency manager and commit updates to `uv.lock`.
- Keep tests deterministic: mock network calls and avoid requiring LLM keys in CI.
- Put reusable tool logic behind small functions so it can be tested outside an MCP runtime.
- Use `.env` only for local interactive clients that need provider keys.
- Prefer adding focused examples over large tutorial dumps in the README.

## Docker

Build and run the crash-course MCP weather server:

```bash
docker build -f 02_mcpcrashcourse/mcpserver/Dockerfile -t mcp-weather-demo .
docker run --rm -p 8000:8000 mcp-weather-demo
```

## Notes For Reviewers

The important review paths are quick to check: dependencies install with `uv sync --frozen --all-groups`, deterministic tests run without LLM keys, and interactive examples are kept separate from CI-safe checks.

For a deeper file-by-file walkthrough, see `PROJECT_ANALYSIS.md`.
