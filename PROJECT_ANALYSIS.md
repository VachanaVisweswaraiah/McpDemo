# MCP Demo: Detailed Project Analysis and Explanation

## 1) Project Overview

This repository is an MCP learning and development workspace built around three complementary folders:

- `01_basic_mcp/` - foundational MCP agent/client workflow using external MCP servers from a config file.
- `02_mcpcrashcourse/` - MCP server-first workflow (build server tools/resources, run transports, connect clients).
- `03_mcplangchain/` - MCP + LangChain workflow (connect multiple MCP servers and orchestrate tools through an LLM agent).

The project demonstrates how MCP can be used across local scripts, agent frameworks, and developer environments.

### What is MCP (Model Context Protocol)?

MCP is a protocol that standardizes how AI systems interact with external capabilities. Instead of hard-coding integrations per model/tool, MCP provides a common contract between:

- **MCP servers** (providers of tools/resources)
- **MCP clients** (consumers that call tools/read resources)
- **Hosts** (IDE apps, desktop chat apps, agent runtimes)

In practical usage, MCP gives your assistant structured access to live capabilities (e.g., weather APIs, custom business logic, browser automation, math engines).

### How MCP works in this project

1. MCP servers are implemented with `FastMCP`.
2. Tools/resources are registered with decorators (`@mcp.tool`, `@mcp.resource`).
3. Servers run over transport modes (`stdio`, `sse`, `streamable-http`).
4. Clients discover tools and invoke them with arguments.
5. Agent wrappers (LangChain/LangGraph) decide when to call tools during conversation.

### Why this project matters

- It moves from basic MCP server operation to multi-server orchestration.
- It shows transport diversity (`stdio`, `sse`, `streamable-http`).
- It demonstrates both direct client invocation and agent-mediated usage.
- It is a reusable starter for building real MCP integrations.

---

## 2) MCP Workflow and Ecosystem Fit

### Typical MCP lifecycle represented here

1. **Define** tools/resources on a server.
2. **Run** the server in dev or normal mode.
3. **Register/connect** the server in client configs (JSON or runtime config).
4. **Invoke** tools from scripts, chat clients, or agents.
5. **Return** tool results to the model, which turns them into user-facing responses.

### Ecosystem mapping for this repo

- **Server layer**: `weather.py`, `mathserver.py`, `mcpserver/server.py`
- **Client layer**: `client-stdio.py`, `client-sse.py`, `client.py`
- **Agent orchestration layer**: `03_mcplangchain/client.py` using LangGraph ReAct agent
- **Host integration layer**: VS Code MCP config and Claude Desktop install flow

---

## 3) Folder Structure

## Root

- `README.md` - quick-start setup and run instructions.
- `PROJECT_ANALYSIS.md` - detailed technical explanation (this document).
- `pyproject.toml` / `uv.lock` - dependency and environment control.

## `01_basic_mcp/` (intro MCP consumer workflow)

- Basic MCP agent chat flow
- Config-driven external MCP server connections
- Introductory entrypoint and minimal starter script

## `02_mcpcrashcourse/` (server-centric MCP workflow)

- Custom MCP weather server logic
- Local MCP clients for `stdio` and `sse`
- MCP config file for host registration

## `03_mcplangchain/` (agent-centric MCP workflow)

- Independent MCP math/weather servers
- Multi-server client using LangChain MCP adapters
- ReAct agent executing tool calls over MCP servers

### Relationship between `01_basic_mcp`, `02_mcpcrashcourse`, and `03_mcplangchain`

- `01_basic_mcp` introduces config-driven MCP consumption with an interactive agent.
- `02_mcpcrashcourse` adds custom MCP server implementation and transport-level client examples.
- `03_mcplangchain` extends this into multi-server LLM orchestration via LangChain/LangGraph.

In short: the repo progresses from **basic MCP usage** -> **custom server development** -> **multi-server agent orchestration**.

---

## 4) Key File Breakdown

## `01_basic_mcp/`

- `app.py`
  - Interactive MCP agent chat using `MCPAgent`/`MCPClient`.
  - Reads MCP server definitions from `browser_mcp.json`.
- `browser_mcp.json`
  - External MCP server config for Playwright, Airbnb, and DuckDuckGo Search via `npx`.
- `main.py`
  - Minimal starter script.

## `02_mcpcrashcourse/`

- `client.py`
  - Interactive agent client using `MCPAgent` + `MCPClient`.
  - Uses memory-enabled chat flow.
- `weather.json`
  - MCP server registration config targeting weather server command.

### `02_mcpcrashcourse/server/`

- `weather.py`
  - FastMCP weather server.
  - Includes tool: `get_alerts(state)` and resource: `echo://{message}`.

### `02_mcpcrashcourse/mcpserver/`

- `server.py`
  - Weather server with two tools:
    - `get_alerts(state)`
    - `get_forecast(latitude, longitude)`
  - Supports transport selection logic (`stdio`/`sse`).
- `client-stdio.py`
  - Stdio client example: connect, list tools, call tool.
- `client-sse.py`
  - SSE client example: connect to `http://localhost:8000/sse`.
- `requirements.txt`
  - Minimal folder-level dependency (`mcp[cli]`).
- `Dockerfile`
  - Containerized run path for server.

## `03_mcplangchain/`

- `mathserver.py`
  - FastMCP math server (`stdio`).
  - Tools:
    - `add(a, b)`
    - `multiple(a, b)`
- `weather.py`
  - FastMCP weather server (`streamable-http`).
  - Tool:
    - `get_weather(location)`
- `client.py`
  - `MultiServerMCPClient` setup with both `math` and `weather` servers.
  - `create_react_agent` invocation over aggregated MCP tools.
- `requirements.txt`
  - LangChain/MCP adapter dependencies.
- `main.py`
  - Basic starter script scaffold.

---

## 5) Setup and Installation Instructions

## Prerequisites

- Python `>= 3.11`
- `uv`
- Node.js + `npx` (for `01_basic_mcp/browser_mcp.json` servers)
- Optional: `.env` with `GROQ_API_KEY` for LangChain examples
- Optional: VS Code MCP setup / Claude Desktop

## Local setup

### Step 1: clone

```bash
git clone <repo-url>
cd McpDemo
```

### Step 2: (optional) initialize new project skeleton

```bash
uv init mcpdemo
cd mcpdemo
```

### Step 3: create and activate virtual environment

```bash
uv venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### Step 4: install dependencies

Root dependencies:

```bash
uv sync
```

Crash course folder:

```bash
uv pip install -r 02_mcpcrashcourse/mcpserver/requirements.txt
```

LangChain folder:

```bash
uv pip install -r 03_mcplangchain/requirements.txt
```

### Step 5: environment variables (for agent clients)

Create `.env`:

```env
GROQ_API_KEY=your_key_here
```

### Command verification (run-from and paths)

- **Repository root:** All `uv run`, `uv sync`, and `uv pip install` commands are intended to be run from the repository root (`McpDemo/`). Server entry points use paths like `02_mcpcrashcourse/server/weather.py` relative to root.
- **Stdio client (`client-stdio.py`):** Must be run from `02_mcpcrashcourse/mcpserver/` because it spawns `server.py` in the current working directory. Use `uv run python client-stdio.py` (or `uv run ./client-stdio.py`) from that directory.
- **SSE client:** Start the server from root with `uv run 02_mcpcrashcourse/mcpserver/server.py`, then from root run `uv run 02_mcpcrashcourse/mcpserver/client-sse.py`. No need to `cd` into mcpserver.
- **`02_mcpcrashcourse/client.py`:** Run from `02_mcpcrashcourse/` so that `weather.json` is in the current directory (config path in code is `weather.json`).
- **`03_mcplangchain/client.py`:** Run from `03_mcplangchain/` so that `mathserver.py` is found when the client spawns the math server. Start the LangChain weather server first in another terminal: `uv run 03_mcplangchain/weather.py` (client expects it at `http://localhost:8000/mcp`).
- **`01_basic_mcp/app.py`:** Run from `01_basic_mcp/` so `browser_mcp.json` is in the current directory. This config launches external servers via `npx`.
- **VS Code MCP config:** Paths in the example JSON are relative to the workspace root; the MCP host typically runs with workspace root as cwd.

---

## 6) Features, Tools, and Resources

## A) Crash course weather capabilities

### Tool: `get_alerts(state: str)`

- Fetches active weather alerts for a state.
- Uses National Weather Service API.
- Returns formatted alert blocks (event, area, severity, description, instructions).

### Tool: `get_forecast(latitude: float, longitude: float)`

- Resolves forecast endpoint using `points` API.
- Returns forecast details (temperature, wind, detailed forecast) for upcoming periods.

### Resource: `echo://{message}`

- Returns `Resource echo: <message>`.
- Useful for validating resource wiring.

## B) LangChain workflow capabilities

### Tool: `add(a, b)`

- Returns arithmetic sum.

### Tool: `multiple(a, b)`

- Returns arithmetic product.

### Tool: `get_weather(location)`

- Returns sample weather text from the streamable HTTP weather server.

### Multi-server orchestration

`03_mcplangchain/client.py` combines tools from two MCP servers into one agent context, allowing one prompt stream to invoke math and weather tools as needed.

## C) Basic MCP workflow capabilities

- `01_basic_mcp/app.py` demonstrates MCP agent chat with memory using configured external MCP servers.
- `01_basic_mcp/browser_mcp.json` provides a reusable pattern for declarative MCP server registration.

---

## 7) Running the Project

## A) Development mode with MCP Inspector

Crash course weather server:

```bash
uv run mcp dev 02_mcpcrashcourse/server/weather.py
```

LangChain math server:

```bash
uv run mcp dev 03_mcplangchain/mathserver.py
```

LangChain weather server:

```bash
uv run mcp dev 03_mcplangchain/weather.py
```

## B) Normal mode

Crash course weather server:

```bash
uv run mcp run 02_mcpcrashcourse/server/weather.py
```

Math server:

```bash
uv run 03_mcplangchain/mathserver.py
```

LangChain weather server:

```bash
uv run 03_mcplangchain/weather.py
```

## C) Install into Claude Desktop

Crash course weather server:

```bash
uv run mcp install 02_mcpcrashcourse/server/weather.py
```

Math server:

```bash
uv run mcp install 03_mcplangchain/mathserver.py
```

LangChain weather server:

```bash
uv run mcp install 03_mcplangchain/weather.py
```

## D) Run local script clients

Crash course stdio client (must run from `mcpserver/` so `server.py` is in cwd):

```bash
cd 02_mcpcrashcourse/mcpserver
uv run python client-stdio.py
```

Crash course SSE client (run server from root first, then client from root):

```bash
# Terminal 1 (from repo root)
uv run 02_mcpcrashcourse/mcpserver/server.py

# Terminal 2 (from repo root)
uv run 02_mcpcrashcourse/mcpserver/client-sse.py
```

Crash course agent client (run from `02_mcpcrashcourse/` so `weather.json` is in cwd):

```bash
cd 02_mcpcrashcourse
uv run python client.py
```

Basic MCP agent client (run from `01_basic_mcp/` so `browser_mcp.json` is in cwd):

```bash
cd 01_basic_mcp
uv run python app.py
```

LangChain multi-server client (run from `03_mcplangchain/`; start weather server first in another terminal):

```bash
# Terminal 1 (from repo root)
uv run 03_mcplangchain/weather.py

# Terminal 2
cd 03_mcplangchain
uv run client.py
```

---

## 8) MCP Connect in VS Code

### Step-by-step

1. Open repository in VS Code.
2. Activate `.venv` and install dependencies.
3. Configure MCP servers in your MCP extension/user settings.
4. Start required servers or let MCP host launch them by config.
5. Open chat and verify tool discovery.

Example configuration (paths are relative to workspace root; ensure the MCP host runs with workspace root as cwd):

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

Example prompts in chat:

- "Get alerts for CA."
- "Forecast for 37.77, -122.42."
- "What is (3 + 5) x 12?"
- "Search for best flights to New York next weekend" (through configured external MCP search/tooling in `01_basic_mcp`).

---

## 9) Usage Examples

## Example 1: stdio client tool discovery and call

Run from `02_mcpcrashcourse/mcpserver/` so the client can spawn `server.py` in the same directory:

```bash
cd 02_mcpcrashcourse/mcpserver
uv run python client-stdio.py
```

Expected output shape:

```text
Available tools:
  - get_alerts
  - get_forecast
The weather alerts are = <formatted result>
```

## Example 2: SSE client

Start the server from repo root, then run the client from root:

```bash
# Terminal 1
uv run 02_mcpcrashcourse/mcpserver/server.py

# Terminal 2
uv run 02_mcpcrashcourse/mcpserver/client-sse.py
```

Expected output shape:

```text
Available tools:
  - get_alerts
  - get_forecast
The weather alerts are = <formatted result>
```

## Example 3: LangChain multi-server agent

Start the weather server first (it listens on port 8000), then run the client from `03_mcplangchain/`:

```bash
# Terminal 1 (from repo root)
uv run 03_mcplangchain/weather.py

# Terminal 2
cd 03_mcplangchain
uv run client.py
```

Expected output shape:

```text
Math response: 96
Weather response: It's always raining in California
```

---

## 10) Potential Improvements and Next Steps

## Improvements

1. Consolidate overlapping weather server logic between folders or clearly document intent split.
2. Normalize config paths and file references to avoid relative-path runtime issues.
3. Add typed outputs (Pydantic models) for tool responses.
4. Add robust input validation and explicit error messages.
5. Add tests:
   - unit tests for formatting/helpers
   - integration tests for MCP tool calls and transport modes
6. Add lint/type checks in CI.
7. Improve observability with request logs and tool latency metrics.

## Extension ideas

- Add geocoding tool (city/state to coordinates).
- Add severe weather summary tool by county/zone.
- Add persistent caching for API responses.
- Add authenticated enterprise API integrations.
- Package servers for deployment in containerized environments.

---

## 11) Conclusion

This project provides a strong MCP foundation by combining:

- server implementation patterns,
- multi-transport client connectivity,
- and agent-driven tool orchestration.

`02_mcpcrashcourse` gives the practical mechanics of MCP tools/resources, while `03_mcplangchain` demonstrates how to operationalize those capabilities in an LLM-agent workflow. With incremental hardening (tests, validation, CI, and deployment packaging), this repository can evolve from a learning project into a production-ready MCP starter template.
