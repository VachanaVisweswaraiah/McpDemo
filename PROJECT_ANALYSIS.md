# MCP Demo: Project Analysis and Explanation

## 1) Project Overview

### What this project is

This project is a practical, end-to-end walkthrough of the **Model Context Protocol (MCP)** ecosystem. It demonstrates both sides of MCP development:

- **Client-first usage** (`01_basic_mcp`): consuming existing MCP servers from an AI agent workflow.
- **Server-first development** (`02_mcpcrashcourse`): implementing and exposing your own MCP tools/resources, then connecting clients to that server.

The repository is therefore not just a single app, but a learning track that shows how to move from "using MCP" to "building MCP services."

### What MCP is (Model Context Protocol)

MCP is a standard protocol that allows AI assistants and agent runtimes to interact with external capabilities in a structured, interoperable way. In practical terms, MCP defines how:

- A **server** exposes capabilities (tools/resources).
- A **client** discovers and calls those capabilities.
- A host environment (IDE, desktop app, agent runtime) connects both in a repeatable way.

This abstraction lets you build tools once and use them in multiple MCP-capable environments (e.g., custom clients, VS Code integrations, Claude Desktop integrations, and agent frameworks).

### How MCP works in this project

At a high level:

1. An MCP server is implemented using `FastMCP`.
2. Tools (like weather lookups) and resources (like echo resource URIs) are registered.
3. Clients connect through **stdio** or **SSE** transport.
4. The client lists available tools/resources and executes tool calls.
5. Agent runtimes (via `mcp-use`) can orchestrate tool calls during chat.

### Purpose of this repository

- Teach MCP architecture through concrete code.
- Demonstrate multiple transport options (`stdio` and `sse`).
- Show integration paths from local scripts to IDE/desktop AI environments.
- Provide a foundation to extend with more real-world tools and APIs.

---

## 2) General Workflow and MCP Ecosystem Fit

### Typical workflow represented in this repository

1. **Define capabilities** in the server (`@mcp.tool`, `@mcp.resource`).
2. **Run the server** in development or normal mode.
3. **Connect clients** (scripted clients, agent runtime, IDE/desktop integration).
4. **Execute tool calls** from prompts or direct client invocation.
5. **Return structured results** to the model/user for final response generation.

### Ecosystem role of each part

- **MCP Server Layer**: your capability provider (`weather` tools/resources).
- **MCP Client Layer**: transport/session handling and tool invocation.
- **Agent Layer** (`mcp-use` + LLM): reasoning + capability selection + memory.
- **Host Layer** (VS Code / Claude Desktop): user-facing MCP interaction surface.

This separation is valuable because each layer can evolve independently while preserving compatibility through MCP.

---

## 3) Folder Structure Analysis

## Root-Level Structure

- `01_basic_mcp/`: introductory client/agent workflow using external MCP services.
- `02_mcpcrashcourse/`: custom MCP server implementation and local client examples.
- `pyproject.toml`: root dependency and project metadata.
- `uv.lock`: locked dependency graph for reproducible installs.
- `README.md`: setup-oriented quick guide.
- `PROJECT_ANALYSIS.md`: this deep-dive explanation document.

### Relationship between `01_basic_mcp` and `02_mcpcrashcourse`

These folders represent two complementary stages:

- `01_basic_mcp` = **MCP consumer perspective** (how an agent uses configured MCP servers).
- `02_mcpcrashcourse` = **MCP producer + consumer perspective** (how to build a server, then consume it via clients and config).

Conceptually, `02_mcpcrashcourse` is an extension of the ideas in `01_basic_mcp`:
first consume capabilities, then create your own capabilities.

---

## 4) File-by-File Breakdown

### `01_basic_mcp/`

- `app.py`
  - Interactive memory-enabled chat loop using `MCPAgent` and `MCPClient`.
  - Loads API keys from environment variables and routes user prompts through MCP-aware agent orchestration.
- `browser_mcp.json`
  - MCP server configuration for third-party servers (`playwright`, `airbnb`, `duckduckgo-search`).
  - Demonstrates server registration format and command/args wiring.
- `main.py`
  - Minimal starter script (`Hello from mcpdemo!`) useful as baseline template.

### `02_mcpcrashcourse/`

- `client.py`
  - Agent-based client flow (`MCPAgent`, `MCPClient`) for interactive usage with conversation memory.
  - Shows how an LLM-driven loop can call MCP tools dynamically.
- `weather.json`
  - MCP server registration targeting local weather server via `uv run mcp run ...`.
  - Designed for environments that consume MCP config files.

#### `02_mcpcrashcourse/server/`

- `weather.py`
  - FastMCP weather server exposing:
    - tool: `get_alerts(state)`
    - resource: `echo://{message}`
  - Demonstrates minimal but complete MCP server with API-backed functionality.

#### `02_mcpcrashcourse/mcpserver/`

- `server.py`
  - Expanded weather server with two tools:
    - `get_alerts(state)`
    - `get_forecast(latitude, longitude)`
  - Includes transport selection logic (`stdio`/`sse`) and NWS API helper functions.
- `client-stdio.py`
  - Demonstrates stdio session setup, tool discovery, and tool invocation.
- `client-sse.py`
  - Demonstrates SSE session setup to `http://localhost:8000/sse`.
- `requirements.txt`
  - Minimal dependencies for this folder (`mcp[cli]`).
- `Dockerfile`
  - Containerized execution path for the MCP server.

---

## 5) Setup and Installation Instructions

## Prerequisites

- Python `>= 3.11`
- `uv` installed
- Optional: Claude Desktop and an MCP-capable VS Code setup
- Optional: `.env` containing `GROQ_API_KEY` for agent-driven chat scripts

## Local setup (recommended)

### Step 1: clone and enter repo

```bash
git clone <repo-url>
cd McpDemo
```

### Step 2: create virtual environment

```bash
uv venv
```

Activate:

- macOS/Linux:

```bash
source .venv/bin/activate
```

- Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### Step 3: install dependencies

Project-level install:

```bash
uv sync
```

Crash-course server folder dependencies:

```bash
uv pip install -r 02_mcpcrashcourse/mcpserver/requirements.txt
```

### Step 4: environment variables (if running agent chat)

Create `.env` with:

```env
GROQ_API_KEY=your_key_here
```

### Step 5: configure MCP server registration (if needed)

Use `02_mcpcrashcourse/weather.json` for MCP host integration, or add equivalent config in your IDE/host.

---

## 6) Features and Tools

## Core server features

- FastMCP-based server setup.
- External API integration (National Weather Service API).
- Tool registration via decorators.
- Resource registration via URI scheme.
- Multi-transport support (`stdio` and `sse`).

## Tool descriptions

### `get_alerts(state: str)`

- **Purpose**: fetch active weather alerts for a US state (two-letter code).
- **Input**: `state` such as `CA`, `NY`, `TX`.
- **Behavior**:
  - calls `https://api.weather.gov/alerts/active/area/{state}`
  - formats results into readable output blocks.
- **Output**:
  - formatted alert text or no-alert/error message.

### `get_forecast(latitude: float, longitude: float)` (in `mcpserver/server.py`)

- **Purpose**: fetch forecast details for geographic coordinates.
- **Input**: coordinates, e.g. `(37.77, -122.42)`.
- **Behavior**:
  - resolves forecast endpoint from `/points/{lat},{lon}`
  - fetches forecast periods
  - returns first 5 period summaries.
- **Output**:
  - text sections containing temperature, wind, and detailed forecast.

## Resource descriptions

### `echo://{message}` (in `server/weather.py`)

- **Purpose**: demonstrates MCP resource retrieval semantics.
- **Input**: URI parameterized message.
- **Output**: `Resource echo: <message>`.

This is a pedagogical resource that helps validate resource wiring before implementing richer data resources.

---

## 7) Running the Project

## A) Development mode (MCP Inspector)

Use this when debugging server behavior and tool schema:

```bash
uv run mcp dev 02_mcpcrashcourse/server/weather.py
```

## B) Normal run mode

Run server as MCP service:

```bash
uv run mcp run 02_mcpcrashcourse/server/weather.py
```

## C) Install into Claude Desktop

Install MCP server registration:

```bash
uv run mcp install 02_mcpcrashcourse/server/weather.py
```

## D) Run script clients

Stdio client:

```bash
cd 02_mcpcrashcourse/mcpserver
uv run client-stdio.py
```

SSE client (requires server running with SSE):

```bash
cd 02_mcpcrashcourse/mcpserver
uv run server.py
uv run client-sse.py
```

## E) VS Code MCP workflow

1. Open repo in VS Code.
2. Ensure dependencies are installed (`uv sync`).
3. Add MCP server config in your MCP extension/user settings.
4. Start server if required by your workflow.
5. Open MCP chat interface and test with weather prompts.

Sample MCP config:

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

---

## 8) Usage Examples

## Example 1: List and call tools via stdio client

Command:

```bash
cd 02_mcpcrashcourse/mcpserver
uv run client-stdio.py
```

Expected output shape:

```text
Available tools:
  - get_alerts: Get weather alerts for a US state.
  - get_forecast: Get weather forecast for a location.
The weather alerts are = <formatted alert text or "No active alerts for this state.">
```

## Example 2: Call alerts in a chat host

Prompt:

```text
Get weather alerts for CA
```

Expected behavior:

- host invokes `get_alerts` with `{ "state": "CA" }`
- response includes event, area, severity, and instructions when available.

## Example 3: Forecast request

Prompt:

```text
Get forecast for latitude 37.77 and longitude -122.42
```

Expected output shape:

```text
Tonight:
Temperature: ...
Wind: ...
Forecast: ...
---
Tomorrow:
...
```

## Example 4: Resource usage

Resource URI:

```text
echo://hello-mcp
```

Expected response:

```text
Resource echo: hello-mcp
```

---

## 9) Potential Improvements and Next Steps

## High-impact improvements

1. **Unify server entry points**
   - Consolidate `server/weather.py` and `mcpserver/server.py` or document clear purpose split.
2. **Fix and standardize config paths**
   - Ensure `client.py` config path aligns with actual file locations.
3. **Typed/structured tool output**
   - Return structured payloads (JSON-style models) for easier downstream reasoning.
4. **Validation and error taxonomy**
   - Validate state codes and coordinates explicitly; improve actionable error messages.
5. **Testing**
   - Add unit tests for formatter/helpers and integration tests for MCP tool calls.

## Feature extensions

- Add new tools:
  - severe weather by county/zone
  - geocoding tool (city -> lat/lon)
  - historical weather summary
- Add richer resources:
  - `weather://alerts/{state}`
  - `weather://forecast/{lat},{lon}`
- Add caching/rate-limit control for API calls.
- Add auth-aware integrations for external APIs beyond NWS.
- Add CI checks (lint, test, type-check) and container publishing.

## Deployment direction

- Run as a managed service (containerized MCP server behind reverse proxy).
- Provide environment profiles (dev/stage/prod).
- Package reusable server module for internal MCP platform catalogs.

---

## 10) Conclusion

This project delivers a strong MCP learning and prototyping foundation by covering both consumer and producer workflows:

- It shows how to **use** MCP servers in agent-driven chat workflows (`01_basic_mcp`).
- It shows how to **build** and expose MCP tools/resources with real API integrations (`02_mcpcrashcourse`).
- It demonstrates practical local integration paths into development environments and AI hosts.

Its value is in combining architecture clarity with executable examples. With modest hardening (tests, unified configs, structured outputs, and deployment automation), this repository can evolve from a learning demo into a reusable production starter template for MCP-based tool platforms.
