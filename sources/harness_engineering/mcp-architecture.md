# MCP Architecture Overview

**Source:** https://modelcontextprotocol.io/docs/learn/architecture
**Fetched:** 2026-05-05
**Note:** Official docs page. Content is closer to verbatim than blog-post extractions; preserves the protocol vocabulary and JSON-RPC examples. Companion to `mcp-intro.md` (which is just the welcome page).

---

## Scope

The Model Context Protocol includes:
- **MCP Specification:** outlines implementation requirements for clients and servers (modelcontextprotocol.io/specification/latest).
- **MCP SDKs:** SDKs for different programming languages.
- **MCP Development Tools:** including the MCP Inspector (github.com/modelcontextprotocol/inspector).
- **MCP Reference Server Implementations** (github.com/modelcontextprotocol/servers).

> MCP focuses solely on the protocol for context exchange — it does not dictate how AI applications use LLMs or manage the provided context.

---

## Concepts of MCP

### Participants

MCP follows a **client-server architecture** where an **MCP host** (an AI application like Claude Code or Claude Desktop) establishes connections to one or more **MCP servers**. The host creates one **MCP client** for each MCP server. Each MCP client maintains a dedicated connection with its corresponding MCP server.

- Local MCP servers using the **STDIO transport** typically serve a single MCP client.
- Remote MCP servers using the **Streamable HTTP transport** typically serve many MCP clients.

**Key Participants:**
- **MCP Host:** the AI application that coordinates and manages one or multiple MCP clients.
- **MCP Client:** a component that maintains a connection to an MCP server and obtains context for the host to use.
- **MCP Server:** a program that provides context to MCP clients.

**Example:** Visual Studio Code acts as an MCP host. When VS Code connects to a Sentry MCP server, the runtime instantiates an MCP client object that maintains the connection. When VS Code connects to another server (e.g., local filesystem), the runtime instantiates an additional MCP client.

[Diagram: MCP Host with 4 MCP Clients connecting to 3 MCP Servers (Filesystem local, Database local, Sentry remote — Sentry having two clients connected)]

**Note:** "MCP server" refers to the program that serves context data, regardless of where it runs. Servers can execute locally or remotely:
- Filesystem server: runs locally on the same machine via STDIO transport. ("Local" MCP server.)
- Sentry MCP server: runs on the Sentry platform, uses Streamable HTTP transport. ("Remote" MCP server.)

---

### Layers

MCP consists of two layers:

- **Data layer:** defines the JSON-RPC based protocol for client-server communication, including lifecycle management and core primitives (tools, resources, prompts, notifications).
- **Transport layer:** defines the communication mechanisms and channels enabling data exchange between clients and servers, including transport-specific connection establishment, message framing, and authorization.

Conceptually the data layer is the inner layer, the transport layer is the outer layer.

#### Data layer
JSON-RPC 2.0 based exchange protocol defining message structure and semantics. Includes:
- **Lifecycle management:** connection initialization, capability negotiation, and connection termination.
- **Server features:** tools for AI actions, resources for context data, and prompts for interaction templates.
- **Client features:** sampling from the host LLM, eliciting input from the user, and logging messages.
- **Utility features:** notifications for real-time updates and progress tracking for long-running operations.

#### Transport layer
Manages communication channels and authentication. Handles connection establishment, message framing, and secure communication.

MCP supports **two transport mechanisms**:
- **Stdio transport:** uses standard input/output streams for direct process communication between local processes on the same machine. Optimal performance, no network overhead.
- **Streamable HTTP transport:** uses HTTP POST for client-to-server messages with optional Server-Sent Events for streaming. Enables remote server communication. Supports standard HTTP authentication (bearer tokens, API keys, custom headers). **MCP recommends OAuth to obtain authentication tokens.**

The transport layer abstracts communication details from the protocol layer, enabling the same JSON-RPC 2.0 message format across all transports.

---

### Data Layer Protocol

MCP uses **JSON-RPC 2.0** as its underlying RPC protocol. Clients and servers send requests to each other and respond accordingly. **Notifications** can be used when no response is required.

#### Lifecycle management
MCP is a **stateful protocol** that requires lifecycle management. (A subset of MCP can be made stateless using Streamable HTTP transport.) The purpose of lifecycle management is to negotiate the **capabilities** that both client and server support — features and operations such as tools, resources, or prompts.

#### Primitives

> Primitives are the most important concept within MCP. They define what clients and servers can offer each other.

**Three core primitives that *servers* can expose:**
- **Tools:** executable functions that AI applications can invoke to perform actions (e.g., file operations, API calls, database queries).
- **Resources:** data sources that provide contextual information to AI applications (e.g., file contents, database records, API responses).
- **Prompts:** reusable templates that help structure interactions with language models (e.g., system prompts, few-shot examples).

Each primitive type has associated methods for:
- **Discovery** (`*/list`)
- **Retrieval** (`*/get`)
- **Execution** (where applicable, e.g., `tools/call`)

Listings are **dynamic** — clients use `*/list` methods to discover available primitives.

**Concrete example:** an MCP server providing context about a database can expose tools for querying the database, a resource containing the schema, and a prompt with few-shot examples for interacting with the tools.

**Three primitives that *clients* can expose** (allow MCP server authors to build richer interactions):
- **Sampling:** allows servers to request language model completions from the client's AI application via `sampling/createMessage`. Useful when server authors want access to a language model but want to stay model-independent and not include a language model SDK in their MCP server.
- **Elicitation:** allows servers to request additional information from users via `elicitation/create`. Useful for getting more information from the user or asking for confirmation of an action.
- **Logging:** enables servers to send log messages to clients for debugging and monitoring.

**Cross-cutting utility primitives:**
- **Tasks (Experimental):** durable execution wrappers that enable deferred result retrieval and status tracking for MCP requests (expensive computations, workflow automation, batch processing, multi-step operations).

#### Notifications

The protocol supports **real-time notifications** to enable dynamic updates between servers and clients. When a server's available tools change, the server can send `tools/list_changed` notifications to inform connected clients. Notifications are JSON-RPC 2.0 notification messages (no response expected).

---

## Example: Step-by-Step Walkthrough

### Step 1: Initialization (Lifecycle Management)

MCP begins with a **capability negotiation handshake**. The client sends an `initialize` request to establish the connection and negotiate supported features.

**Initialize Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "elicitation": {}
    },
    "clientInfo": {
      "name": "example-client",
      "version": "1.0.0"
    }
  }
}
```

**Initialize Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": {
        "listChanged": true
      },
      "resources": {}
    },
    "serverInfo": {
      "name": "example-server",
      "version": "1.0.0"
    }
  }
}
```

**Three critical purposes of initialization:**
1. **Protocol Version Negotiation:** the `protocolVersion` field ensures both client and server are using compatible protocol versions. If a mutually compatible version is not negotiated, the connection should be terminated.
2. **Capability Discovery:** the `capabilities` object allows each party to declare what features they support. Avoids unsupported operations.
3. **Identity Exchange:** `clientInfo` and `serverInfo` provide identification and versioning for debugging and compatibility.

**In this example:**
- **Client capability:** `"elicitation": {}` — client can work with user interaction requests (can receive `elicitation/create` calls).
- **Server capabilities:**
  - `"tools": {"listChanged": true}` — server supports tools primitive AND can send `tools/list_changed` notifications.
  - `"resources": {}` — server supports resources primitive (can handle `resources/list` and `resources/read`).

**After successful initialization, the client sends:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

**Pseudo-code for AI application initialization:**
```python
async with stdio_client(server_config) as (read, write):
    async with ClientSession(read, write) as session:
        init_response = await session.initialize()
        if init_response.capabilities.tools:
            app.register_mcp_server(session, supports_tools=True)
        app.set_server_ready(session)
```

---

### Step 2: Tool Discovery (Primitives)

The client sends a `tools/list` request to discover available tools.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

**Response (excerpt):**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "calculator_arithmetic",
        "title": "Calculator",
        "description": "Perform mathematical calculations including basic arithmetic, trigonometric functions, and algebraic operations",
        "inputSchema": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4', 'sin(30)', 'sqrt(16)')"
            }
          },
          "required": ["expression"]
        }
      },
      {
        "name": "weather_current",
        "title": "Weather Information",
        "description": "Get current weather information for any location worldwide",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "City name, address, or coordinates"},
            "units": {"type": "string", "enum": ["metric", "imperial", "kelvin"], "default": "metric"}
          },
          "required": ["location"]
        }
      }
    ]
  }
}
```

**Each tool object includes:**
- **`name`:** unique identifier within the server's namespace. Should follow a clear naming pattern (e.g., `calculator_arithmetic` rather than just `calculate`).
- **`title`:** human-readable display name.
- **`description`:** detailed explanation of what the tool does and when to use it.
- **`inputSchema`:** JSON Schema defining expected input parameters; enables type validation.

**Pseudo-code:**
```python
available_tools = []
for session in app.mcp_server_sessions():
    tools_response = await session.list_tools()
    available_tools.extend(tools_response.tools)
conversation.register_available_tools(available_tools)
```

---

### Step 3: Tool Execution (Primitives)

**Tool Call Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "weather_current",
    "arguments": {
      "location": "San Francisco",
      "units": "imperial"
    }
  }
}
```

**Tool Call Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Current weather in San Francisco: 68°F, partly cloudy with light winds from the west at 8 mph. Humidity: 65%"
      }
    ]
  }
}
```

**Key elements:**
1. **`name`:** must match exactly the tool name from the discovery response.
2. **`arguments`:** input parameters as defined by the tool's `inputSchema`.
3. **JSON-RPC structure:** uses standard 2.0 format with unique `id` for request-response correlation.

**Response structure:**
1. **`content` Array:** allows rich, multi-format responses (text, images, resources).
2. **Content Types:** each object has a `type` field (`"type": "text"` for plain text; MCP supports various content types).
3. **Structured Output:** actionable information for the AI application.

**Pseudo-code:**
```python
async def handle_tool_call(conversation, tool_name, arguments):
    session = app.find_mcp_session_for_tool(tool_name)
    result = await session.call_tool(tool_name, arguments)
    conversation.add_tool_result(result.content)
```

---

### Step 4: Real-time Updates (Notifications)

Servers can proactively notify clients about state changes.

**Tool list change notification (no `id` field, no response expected):**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

**Key features of MCP notifications:**
1. **No response required:** follows JSON-RPC 2.0 notification semantics.
2. **Capability-based:** only sent by servers that declared `"listChanged": true` in their tools capability during initialization.
3. **Event-driven:** the server decides when to send notifications based on internal state changes.

**Client response — request the updated tool list:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/list"
}
```

**Why notifications matter:**
1. **Dynamic environments:** tools may come and go based on server state, external dependencies, or user permissions.
2. **Efficiency:** clients don't need to poll.
3. **Consistency:** clients always have accurate information about available server capabilities.
4. **Real-time collaboration:** enables responsive AI applications.

**Pseudo-code:**
```python
async def handle_tools_changed_notification(session):
    tools_response = await session.list_tools()
    app.update_available_tools(session, tools_response.tools)
    if app.conversation.is_active():
        app.conversation.notify_llm_of_new_capabilities()
```
