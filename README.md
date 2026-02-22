# MCP Demo Project

This repository demonstrates practical **Model Context Protocol (MCP)** workflows using two learning tracks:

- `01_basic_mcp/`: MCP client-side chat workflow using external MCP servers (Playwright, Airbnb, DuckDuckGo).
- `02_mcpcrashcourse/`: MCP server workflow with custom weather tools/resources, plus stdio and SSE clients.

The goal is to help you understand the full cycle: define tools/resources, run an MCP server, connect a client, and use the setup in local development tools like VS Code and Claude Desktop.

## Introduction

This project is designed as a hands-on MCP reference for:

- Building and running a custom MCP server.
- Exposing tools/resources to MCP clients.
- Testing with both `stdio` and `sse` transports.
- Integrating MCP servers with chat-based developer workflows.

### Requirements

- Python `3.11+`
- `uv` package manager
- Internet access (for weather API calls to `api.weather.gov`)
- Optional: Claude Desktop and VS Code MCP-compatible extension/workflow

## Setup Steps

### 1) Clone and enter the project

```bash
git clone <your-repo-url>
cd McpDemo
```

### 2) Initialize project and virtual environment (if starting fresh)

```bash
uv init mcpdemo
cd mcpdemo
uv venv
```

Activate the environment:

- macOS/Linux:

```bash
source .venv/bin/activate
```

- Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

This repo supports both project-level dependencies and folder-specific requirements.

Using `pyproject.toml`:

```bash
uv sync
```

Using `requirements.txt` for the crash course MCP server:

```bash
uv pip install -r 02_mcpcrashcourse/mcpserver/requirements.txt
```

Or add directly with `uv`:

```bash
uv add "mcp[cli]"
```

## Features

### MCP Tools

From `02_mcpcrashcourse/mcpserver/server.py` and `02_mcpcrashcourse/server/weather.py`:

- `get_alerts(state: str)`: Fetches active weather alerts for a US state.
- `get_forecast(latitude: float, longitude: float)`: Fetches forecast periods for a location.

### MCP Resources

From `02_mcpcrashcourse/server/weather.py`:

- `echo://{message}`: Returns an echoed message as an MCP resource.

### Client and Agent Workflows

- `client-stdio.py`: Connects to the server over stdio and calls tools.
- `client-sse.py`: Connects to the server over SSE (`http://localhost:8000/sse`).
- `01_basic_mcp/app.py`: Interactive MCP agent chat with memory via `mcp-use`.

## Running the Server

Use the weather server in `02_mcpcrashcourse/server/weather.py` for MCP CLI workflows.

### Development mode (MCP Inspector)

```bash
uv run mcp dev 02_mcpcrashcourse/server/weather.py
```

### Normal mode

```bash
uv run mcp run 02_mcpcrashcourse/server/weather.py
```

### Install in Claude Desktop

```bash
uv run mcp install 02_mcpcrashcourse/server/weather.py
```

You can also use the existing MCP config file at `02_mcpcrashcourse/weather.json` if you prefer manual configuration.

## MCP Connect in VS Code

### Step-by-step setup

1. Open this repository in VS Code.
2. Create/activate your virtual environment and install dependencies (`uv sync`).
3. Start the MCP server in one terminal:

```bash
uv run mcp run 02_mcpcrashcourse/server/weather.py
```

4. Configure MCP servers in your VS Code MCP settings or extension config. Example:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "02_mcpcrashcourse/server/weather.py"
      ]
    }
  }
}
```

5. Launch the chat panel in your MCP-compatible VS Code extension.
6. Confirm the `weather` server is available, then test prompts like:
   - "Get alerts for CA"
   - "Get forecast for latitude 37.77 and longitude -122.42"

## Project Structure

```text
McpDemo/
├── 01_basic_mcp/
│   ├── app.py                # Interactive MCP agent chat using MCPClient + memory
│   ├── browser_mcp.json      # MCP server definitions for Playwright/Airbnb/DuckDuckGo
│   └── main.py               # Minimal starter script
├── 02_mcpcrashcourse/
│   ├── client.py             # Agent-based MCP client flow
│   ├── weather.json          # MCP config targeting local weather server
│   ├── server/
│   │   └── weather.py        # FastMCP weather server (tools + echo resource)
│   └── mcpserver/
│       ├── server.py         # FastMCP server with SSE/stdio transport switch
│       ├── client-stdio.py   # Stdio MCP client example
│       ├── client-sse.py     # SSE MCP client example
│       ├── requirements.txt  # Minimal dependency set for mcpserver folder
│       └── Dockerfile        # Containerized server setup
├── pyproject.toml            # Project dependencies and metadata
├── uv.lock                   # Locked dependency resolution
└── README.md                 # Project documentation
```

## Quick Start (Recommended)

```bash
uv sync
uv run mcp dev 02_mcpcrashcourse/server/weather.py
```

Then connect using `02_mcpcrashcourse/mcpserver/client-stdio.py`, `client-sse.py`, VS Code, or Claude Desktop.

