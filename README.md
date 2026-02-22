# MCP Project README

This project demonstrates end-to-end **Model Context Protocol (MCP)** workflows across three folders:

- `01_basic_mcp/`: basic MCP agent/client workflow using external MCP servers from config.
- `02_mcpcrashcourse/`: MCP weather server examples with `stdio` and `sse` clients.
- `03_mcplangchain/`: LangChain + MCP adapter workflow with multiple MCP servers (`math` + `weather`).

It is designed as a practical learning and development reference for creating MCP tools/resources and integrating them into local clients, VS Code, and Claude Desktop.

## All Folders Quick Run

| Folder | Run from | Command | What it does |
| --- | --- | --- | --- |
| `01_basic_mcp` | `01_basic_mcp/` | `uv run python app.py` | Starts basic MCP agent chat using external MCP servers from `browser_mcp.json`. |
| `02_mcpcrashcourse` (Inspector) | repo root | `uv run mcp dev 02_mcpcrashcourse/server/weather.py` | Runs crash-course weather MCP server in development mode. |
| `02_mcpcrashcourse` (stdio client) | `02_mcpcrashcourse/mcpserver/` | `uv run python client-stdio.py` | Connects to local stdio MCP server and executes weather tool calls. |
| `02_mcpcrashcourse` (sse server) | repo root | `uv run 02_mcpcrashcourse/mcpserver/server.py` | Starts SSE weather server on port `8000`. |
| `02_mcpcrashcourse` (sse client) | repo root | `uv run 02_mcpcrashcourse/mcpserver/client-sse.py` | Connects to SSE server at `http://localhost:8000/sse`. |
| `03_mcplangchain` (weather server) | repo root | `uv run 03_mcplangchain/weather.py` | Starts streamable HTTP weather MCP server for LangChain client. |
| `03_mcplangchain` (agent client) | `03_mcplangchain/` | `uv run client.py` | Runs multi-server LangChain MCP agent (`math` + `weather`). |

### Recommended First Run Order (Beginner)

1. **Start with the easiest flow (`01_basic_mcp`)**
   - `cd 01_basic_mcp`
   - `uv run python app.py`
2. **Try the crash-course server workflow (`02_mcpcrashcourse`)**
   - From repo root: `uv run mcp dev 02_mcpcrashcourse/server/weather.py`
   - In another terminal: `cd 02_mcpcrashcourse/mcpserver && uv run python client-stdio.py`
3. **Run the multi-server LangChain workflow (`03_mcplangchain`)**
   - Terminal 1 (repo root): `uv run 03_mcplangchain/weather.py`
   - Terminal 2: `cd 03_mcplangchain && uv run client.py`

## Introduction

MCP is a standard interface that lets AI assistants and clients interact with external tools/resources through MCP servers. In this project, you can see both:

- how to build MCP servers with `FastMCP`
- how to consume MCP tools from Python clients and agent workflows
- how to connect MCP servers to editor/desktop chat environments

### Requirements

- Python `3.11+`
- `uv`
- Node.js + `npx` (required for `01_basic_mcp/browser_mcp.json` servers)
- Internet access (for weather APIs in crash course example)
- Optional: VS Code MCP-compatible extension and Claude Desktop
- Optional: `.env` with `GROQ_API_KEY` for LangChain agent examples

**Command verification:** All commands below assume you are in the **repository root** (`McpDemo/`) unless a step says otherwise. Client scripts that spawn a server (e.g. stdio) or load config by relative path must be run from the directory indicated.

## Setup Steps

### 1) Clone and open project

```bash
git clone <your-repo-url>
cd McpDemo
```

If you are starting a brand-new project from scratch (optional):

```bash
uv init mcpdemo
cd mcpdemo
```

### 2) Create virtual environment

```bash
uv venv
```

Activate it:

- macOS/Linux:

```bash
source .venv/bin/activate
```

- Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

Root dependencies:

```bash
uv sync
```

Crash course server dependencies (`requirements.txt`):

```bash
uv pip install -r 02_mcpcrashcourse/mcpserver/requirements.txt
```

LangChain MCP dependencies (`requirements.txt`):

```bash
uv pip install -r 03_mcplangchain/requirements.txt
```

If you are initializing fresh and adding MCP CLI manually:

```bash
uv add "mcp[cli]"
```

## Features

### Tools and resources in `02_mcpcrashcourse`

- `get_alerts(state: str)`:
  Fetches active weather alerts by US state.
- `get_forecast(latitude: float, longitude: float)`:
  Fetches detailed weather forecast periods.
- `echo://{message}` resource:
  Returns a simple echo response as an MCP resource.

### Tools in `03_mcplangchain`

- `add(a: int, b: int)`:
  Adds two numbers.
- `multiple(a: int, b: int)`:
  Multiplies two numbers.
- `get_weather(location: str)`:
  Returns weather text from the sample weather server.

### Client workflows

- `01_basic_mcp/app.py`:
  Interactive MCP agent chat using config from `01_basic_mcp/browser_mcp.json` (Playwright, Airbnb, DuckDuckGo servers).
- `02_mcpcrashcourse/mcpserver/client-stdio.py`:
  Demonstrates stdio connection and tool calls.
- `02_mcpcrashcourse/mcpserver/client-sse.py`:
  Demonstrates SSE connection and tool calls.
- `03_mcplangchain/client.py`:
  Connects to multiple MCP servers using `MultiServerMCPClient` and invokes tools through a LangGraph ReAct agent. Run from `03_mcplangchain/` and start the weather server first in another terminal (`uv run 03_mcplangchain/weather.py`).

- `02_mcpcrashcourse/client.py`:
  Interactive MCP agent chat; run from `02_mcpcrashcourse/` so `weather.json` is in the current directory.

- `01_basic_mcp/main.py`:
  Minimal starter entrypoint for the basic folder.

## Running the Server

## MCP Inspector (development mode)

For weather crash course server:

```bash
uv run mcp dev 02_mcpcrashcourse/server/weather.py
```

For math server:

```bash
uv run mcp dev 03_mcplangchain/mathserver.py
```

For LangChain weather server:

```bash
uv run mcp dev 03_mcplangchain/weather.py
```

## Normal mode

Crash course weather server:

```bash
uv run mcp run 02_mcpcrashcourse/server/weather.py
```

Math server (stdio):

```bash
uv run 03_mcplangchain/mathserver.py
```

Weather server in LangChain folder (streamable HTTP):

```bash
uv run 03_mcplangchain/weather.py
```

## Install server in Claude Desktop

Install crash course weather server:

```bash
uv run mcp install 02_mcpcrashcourse/server/weather.py
```

Install math server:

```bash
uv run mcp install 03_mcplangchain/mathserver.py
```

Install LangChain weather server:

```bash
uv run mcp install 03_mcplangchain/weather.py
```

## Run `01_basic_mcp` Workflow

Run from the `01_basic_mcp/` directory (so `browser_mcp.json` is in the current directory):

```bash
cd 01_basic_mcp
uv run python app.py
```

This workflow uses `01_basic_mcp/browser_mcp.json`, which starts external MCP servers via `npx`.

## MCP Connect in VS Code

### Step-by-step setup

1. Open `McpDemo` in VS Code.
2. Create/activate virtual environment and install dependencies.
3. Add MCP server config in your MCP extension/settings.
4. Start needed servers (if your setup requires manual launch).
5. Open chat panel and verify tools can be called.

Example MCP configuration (paths are relative to the workspace root where the MCP host runs):

```json
{
  "mcpServers": {
    "weather-crash-course": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "02_mcpcrashcourse/server/weather.py"
      ]
    },
    "math": {
      "command": "python",
      "args": ["03_mcplangchain/mathserver.py"]
    },
    "weather-langchain": {
      "command": "python",
      "args": ["03_mcplangchain/weather.py"]
    }
  }
}
```

Then test prompts:

- "Get alerts for CA"
- "What is the forecast for 37.77, -122.42?"
- "What is (3 + 5) x 12?"

## Project Structure

```text
McpDemo/
├── 01_basic_mcp/
│   ├── app.py                        # Basic MCP agent chat workflow using browser_mcp.json
│   ├── browser_mcp.json              # External MCP server config (playwright/airbnb/duckduckgo-search)
│   └── main.py                       # Minimal starter file
├── 02_mcpcrashcourse/
│   ├── client.py                     # Agent-based MCP client flow
│   ├── weather.json                  # MCP config for weather server
│   ├── server/
│   │   └── weather.py                # FastMCP weather server (tools + resource)
│   └── mcpserver/
│       ├── server.py                 # FastMCP server with SSE/stdio examples
│       ├── client-stdio.py           # Stdio client example
│       ├── client-sse.py             # SSE client example
│       ├── requirements.txt          # Folder-specific dependencies
│       └── Dockerfile                # Docker setup for server
├── 03_mcplangchain/
│   ├── client.py                     # Multi-server MCP client using LangChain adapters
│   ├── mathserver.py                 # Math MCP server (stdio) with add/multiple tools
│   ├── weather.py                    # Weather MCP server (streamable HTTP)
│   ├── main.py                       # Basic starter file
│   └── requirements.txt              # LangChain MCP dependencies
├── pyproject.toml                    # Project metadata/dependencies
├── uv.lock                           # Locked dependency graph
└── README.md                         # Documentation
```

## Quick Start

From repository root:

```bash
uv sync
uv run mcp dev 02_mcpcrashcourse/server/weather.py
```

In another terminal, run the stdio client **from the mcpserver directory** (so it can spawn `server.py` in the same folder):

```bash
cd 02_mcpcrashcourse/mcpserver
uv run python client-stdio.py
```

To run the SSE client instead: start the server from root (`uv run 02_mcpcrashcourse/mcpserver/server.py`), then in a second terminal from root run `uv run 02_mcpcrashcourse/mcpserver/client-sse.py`. The weather server in `mcpserver/server.py` uses SSE on port 8000 by default.

