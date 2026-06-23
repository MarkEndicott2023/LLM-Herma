# What Is the Model Context Protocol (MCP)?

**Source:** https://modelcontextprotocol.io/docs/getting-started/intro
**Fetched:** 2026-05-05
**Note:** This is the brief MCP welcome page only. The deeper conceptual model lives at `/docs/learn/architecture` (not included here). Consider adding that page if you want the formal vocabulary (clients, servers, tools, resources, prompts).

---

## What MCP Is

> MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems.

Using MCP, AI applications like Claude or ChatGPT can connect to:
- **Data sources** (e.g., local files, databases)
- **Tools** (e.g., search engines, calculators)
- **Workflows** (e.g., specialized prompts)

This enables AI applications to access key information and perform tasks.

**Analogy:** "Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems."

[Diagram: simple architecture diagram showing AI applications connecting to external systems via MCP]

---

## What MCP Enables

- Agents can access your Google Calendar and Notion, acting as a more personalized AI assistant.
- Claude Code can generate an entire web app using a Figma design.
- Enterprise chatbots can connect to multiple databases across an organization, empowering users to analyze data using chat.
- AI models can create 3D designs on Blender and print them out using a 3D printer.

---

## Why MCP Matters

- **Developers:** MCP reduces development time and complexity when building, or integrating with, an AI application or agent.
- **AI applications or agents:** MCP provides access to an ecosystem of data sources, tools, and apps which enhance capabilities and improve end-user experience.
- **End-users:** MCP results in more capable AI applications or agents that can access your data and take actions on your behalf when necessary.

---

## Broad Ecosystem Support

MCP is an open protocol supported across a wide range of clients and servers:
- AI assistants: Claude, ChatGPT.
- Development tools: Visual Studio Code, Cursor, MCPJam, and many others.

"Build once and integrate everywhere."

---

## Build With MCP

- **Build servers:** create MCP servers to expose your data and tools (`/docs/develop/build-server`).
- **Build clients:** develop applications that connect to MCP servers (`/docs/develop/build-client`).
- **Build MCP Apps:** build interactive apps that run inside AI clients (`/extensions/apps/overview`).

---

## Learn More

- **Understand concepts:** core concepts and architecture of MCP at `/docs/learn/architecture`.
- **Documentation index:** `https://modelcontextprotocol.io/llms.txt` for full discovery.
