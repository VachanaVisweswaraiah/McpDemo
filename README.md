# MCP Demo: AI Tooling and Agent Orchestration

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-MCP-black)
![LangChain](https://img.shields.io/badge/LangChain-Agent%20Orchestration-green)
![LangGraph](https://img.shields.io/badge/LangGraph-ReAct%20Agents-purple)
![uv](https://img.shields.io/badge/uv-Dependency%20Management-orange)
![CI](https://img.shields.io/badge/CI-Ruff%20%2B%20Pytest-informational)

## Overview

This repository demonstrates end-to-end Model Context Protocol (MCP) workflows in Python: building MCP servers, connecting MCP clients, and orchestrating multiple tools through LangChain/LangGraph agents.

The project is structured as a progression:

- `01_basic_mcp/` - config-driven MCP client workflow using external MCP servers.
- `02_mcpcrashcourse/` - custom weather MCP servers, resources, stdio/SSE clients, and Docker support.
- `03_mcplangchain/` - multi-server MCP orchestration with LangChain and LangGraph.

It covers the core lifecycle of an MCP integration:

- MCP server design with typed tools and resources.
- Multiple MCP transports: `stdio`, `sse`, and `streamable-http`.
- Agent integration using LangChain, LangGraph, and `mcp-use`.
- Reproducible dependency management with `uv`.
- Automated tests and CI for deterministic tool behavior.
- Clear local development workflow for future extensions.

## Architecture

```text
McpDemo/
├── 01_basic_mcp/              # External MCP server client demo
├── 02_mcpcrashcourse/
│   ├── server/weather.py      # FastMCP weather alerts + echo resource
│   ├── mcpserver/server.py    # Weather alerts + forecast server
│   ├── mcpserver/client-*.py  # stdio and SSE clients
│   └── weather.json           # Portable MCP server config
├── 03_mcplangchain/
│   ├── mathserver.py          # FastMCP math tools
│   ├── weather.py             # Streamable HTTP weather tool
│   └── client.py              # LangChain multi-server agent client
├── tests/                     # Unit tests for deterministic tool behavior
├── .github/workflows/ci.yml   # Lint and test workflow
├── pyproject.toml             # Runtime and dev dependencies
└── uv.lock                    # Locked dependency graph
```

## Prerequisites

- Python `3.11+`
- `uv`
- Node.js + `npx` for the external MCP servers in `01_basic_mcp/browser_mcp.json`
- Optional: `GROQ_API_KEY` in `.env` for LLM-backed agent clients

## Setup

```bash
git clone <your-repo-url>
cd McpDemo
uv sync --all-groups
```

Create a `.env` file only if you want to run the LLM-backed interactive clients:

```env
GROQ_API_KEY=your_key_here
```

## Development Lifecycle

Use these commands before every commit:

```bash
uv run ruff check .
uv run pytest
```

Run the full project setup from a clean machine:

```bash
uv sync --frozen --all-groups
uv run ruff check .
uv run pytest
```

The CI workflow runs the same lint and test checks on pushes and pull requests.

## Quick Runs

| Workflow | Run from | Command |
| --- | --- | --- |
| Basic external MCP chat | `01_basic_mcp/` | `uv run python app.py` |
| Weather MCP Inspector | repo root | `uv run mcp dev 02_mcpcrashcourse/server/weather.py` |
| Weather stdio client | `02_mcpcrashcourse/mcpserver/` | `uv run python client-stdio.py` |
| Weather SSE server | repo root | `uv run 02_mcpcrashcourse/mcpserver/server.py` |
| Weather SSE client | repo root | `uv run 02_mcpcrashcourse/mcpserver/client-sse.py` |
| LangChain weather server | repo root | `uv run 03_mcplangchain/weather.py` |
| LangChain multi-server client | `03_mcplangchain/` | `uv run python client.py` |

## Example Capabilities

`02_mcpcrashcourse/server/weather.py`

- `get_alerts(state: str)` - fetches active US weather alerts.
- `echo://{message}` - resource example for MCP resource wiring.

`02_mcpcrashcourse/mcpserver/server.py`

- `get_alerts(state: str)` - fetches and formats active alerts.
- `get_forecast(latitude: float, longitude: float)` - resolves the forecast grid and returns the next five forecast periods.

`03_mcplangchain/mathserver.py`

- `add(a: int, b: int)` - deterministic math tool.
- `multiple(a: int, b: int)` - deterministic math tool.

`03_mcplangchain/weather.py`

- `get_weather(location: str)` - simple streamable HTTP weather tool for agent orchestration demos.

## Docker

Build the crash-course MCP weather server from the repository root:

```bash
docker build -f 02_mcpcrashcourse/mcpserver/Dockerfile -t mcp-weather-demo .
docker run --rm -p 8000:8000 mcp-weather-demo
```

## Engineering Notes

This repo is organized like a maintained Python project:

- `uv` is the single dependency manager.
- Tests avoid live LLM calls and live API assumptions.
- CI verifies deterministic logic on every change.
- Demo folders remain readable for learning, while the root workflow behaves like a maintained Python project.

## Next Engineering Improvements

- Factor duplicate weather formatting into a shared package module.
- Add transport-level integration tests that spin up MCP servers locally.
- Add typed configuration for model/provider selection.
- Add screenshots or terminal recordings to show MCP Inspector and LangChain agent runs.
