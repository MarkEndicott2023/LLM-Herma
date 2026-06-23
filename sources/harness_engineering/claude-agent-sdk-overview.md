# Claude Agent SDK Overview

**Source:** https://code.claude.com/docs/en/agent-sdk/overview
**Fetched:** 2026-05-05
**Note:** This is the official docs page. Content is closer to verbatim than the Anthropic engineering blog articles in this directory.

---

## What the SDK Is

> Build production AI agents with Claude Code as a library.

> The Claude Code SDK has been renamed to the Claude Agent SDK. (Migration guide available.)

Build AI agents that autonomously read files, run commands, search the web, edit code, and more. The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in **Python and TypeScript**.

> Opus 4.7 (`claude-opus-4-7`) requires Agent SDK v0.2.111 or later.

---

## Minimal Example

**Python:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)

asyncio.run(main())
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.ts",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);
}
```

The SDK includes built-in tools so your agent can start working immediately without you implementing tool execution.

---

## Get Started

### Step 1: Install
- TypeScript: `npm install @anthropic-ai/claude-agent-sdk`
- Python: `pip install claude-agent-sdk`
- The TypeScript SDK bundles a native Claude Code binary as an optional dependency.

### Step 2: Set API Key
```bash
export ANTHROPIC_API_KEY=your-api-key
```

The SDK supports authentication via third-party API providers:
- **Amazon Bedrock:** `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials.
- **Google Vertex AI:** `CLAUDE_CODE_USE_VERTEX=1` + GCP credentials.
- **Microsoft Azure (Foundry):** `CLAUDE_CODE_USE_FOUNDRY=1` + Azure credentials.

> Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use API key authentication.

### Step 3: Run Your First Agent
```python
async for message in query(
    prompt="What files are in this directory?",
    options=ClaudeAgentOptions(allowed_tools=["Bash", "Glob"]),
):
    if hasattr(message, "result"):
        print(message.result)
```

---

## Capabilities

### Built-in Tools

| Tool | What it does |
|---|---|
| **Read** | Read any file in the working directory |
| **Write** | Create new files |
| **Edit** | Make precise edits to existing files |
| **Bash** | Run terminal commands, scripts, git operations |
| **Monitor** | Watch a background script and react to each output line as an event |
| **Glob** | Find files by pattern (`**/*.ts`, `src/**/*.py`) |
| **Grep** | Search file contents with regex |
| **WebSearch** | Search the web for current information |
| **WebFetch** | Fetch and parse web page content |
| **AskUserQuestion** | Ask the user clarifying questions with multiple choice options |

### Hooks

Run custom code at key points in the agent lifecycle. SDK hooks use callback functions to validate, log, block, or transform agent behavior.

**Available hooks:** `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, and more.

**Example — log all file changes to an audit file:**
```python
async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

# ...
options=ClaudeAgentOptions(
    permission_mode="acceptEdits",
    hooks={"PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_file_change])]},
),
```

### Subagents

Spawn specialized agents to handle focused subtasks. Your main agent delegates work, and subagents report back with results.

Define custom agents with specialized instructions. **Include `Agent` in `allowedTools`** since subagents are invoked via the Agent tool.

```python
options=ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Agent"],
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code reviewer for quality and security reviews.",
            prompt="Analyze code quality and suggest improvements.",
            tools=["Read", "Glob", "Grep"],
        )
    },
),
```

Messages from within a subagent's context include a `parent_tool_use_id` field, letting you track which messages belong to which subagent execution.

### MCP

Connect to external systems via the Model Context Protocol: databases, browsers, APIs, and hundreds more.

**Example — connect Playwright MCP server for browser automation:**
```python
options=ClaudeAgentOptions(
    mcp_servers={
        "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
    }
),
```

### Permissions

Control exactly which tools your agent can use. Allow safe operations, block dangerous ones, or require approval for sensitive actions.

```python
options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
```

### Sessions

Maintain context across multiple exchanges. Resume sessions later, or fork them to explore different approaches.

```python
session_id = None

# First query: capture the session ID
async for message in query(
    prompt="Read the authentication module",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"]),
):
    if isinstance(message, SystemMessage) and message.subtype == "init":
        session_id = message.data["session_id"]

# Resume with full context
async for message in query(
    prompt="Now find all places that call it",
    options=ClaudeAgentOptions(resume=session_id),
):
    ...
```

---

## Claude Code Features (Filesystem-Based Configuration)

The SDK loads these from `.claude/` in your working directory and `~/.claude/` by default. Restrict which sources load via `setting_sources` (Python) / `settingSources` (TypeScript).

| Feature | Description | Location |
|---|---|---|
| **Skills** | Specialized capabilities defined in Markdown | `.claude/skills/*/SKILL.md` |
| **Slash commands** | Custom commands for common tasks | `.claude/commands/*.md` |
| **Memory** | Project context and instructions | `CLAUDE.md` or `.claude/CLAUDE.md` |
| **Plugins** | Extend with custom commands, agents, and MCP servers | Programmatic via `plugins` option |

---

## Compare the Agent SDK to Other Claude Tools

### Agent SDK vs. Client SDK
- **Client SDK:** direct API access; you implement the tool loop.
- **Agent SDK:** Claude with built-in tool execution; Claude handles the loop.

```python
# Client SDK: you implement the tool loop
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)

# Agent SDK: Claude handles tools autonomously
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

### Agent SDK vs. Claude Code CLI
Same capabilities, different interface:

| Use case | Best choice |
|---|---|
| Interactive development | CLI |
| CI/CD pipelines | SDK |
| Custom applications | SDK |
| One-off tasks | CLI |
| Production automation | SDK |

Many teams use both: CLI for daily development, SDK for production.

### Agent SDK vs. Managed Agents

| | Agent SDK | Managed Agents |
|---|---|---|
| **Runs in** | Your process, your infrastructure | Anthropic-managed infrastructure |
| **Interface** | Python or TypeScript library | REST API |
| **Agent works on** | Files on your infrastructure | A managed sandbox per session |
| **Session state** | JSONL on your filesystem | Anthropic-hosted event log |
| **Custom tools** | In-process Python or TypeScript functions | Claude triggers the tool; you execute and return results |
| **Best for** | Local prototyping, agents that work directly on your filesystem and services | Production agents without operating sandbox/session infrastructure, long-running and asynchronous sessions |

**Common path:** prototype with the Agent SDK locally, then move to Managed Agents for production.

---

## Branding Guidelines (Partner Use)

**Allowed:**
- "Claude Agent" (preferred for dropdown menus)
- "Claude" (when within a menu already labeled "Agents")
- "{YourAgentName} Powered by Claude" (if you have an existing agent name)

**Not permitted:**
- "Claude Code" or "Claude Code Agent"
- Claude Code-branded ASCII art or visual elements that mimic Claude Code

Your product should maintain its own branding and not appear to be Claude Code or any Anthropic product.
