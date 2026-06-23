# Code Execution with MCP: Building More Efficient AI Agents

**Source:** https://www.anthropic.com/engineering/code-execution-with-mcp
**Authors:** Adam Jones, Conor Kelly
**Published:** Nov 4, 2025
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text.

---

## Overview
The article explores how code execution environments can improve the efficiency of AI agents using the Model Context Protocol (MCP). The core challenge addressed: as agents connect to hundreds or thousands of tools, traditional approaches that load all tool definitions upfront and pass results through the context window become inefficient.

## Key Problems Identified

**Token consumption inefficiencies occur through two mechanisms:**

1. **Tool definition overload** — loading all MCP tool definitions directly into context consumes substantial tokens upfront, creating bottlenecks when managing thousands of tools.
2. **Intermediate result duplication** — when agents call multiple tools sequentially, results must pass through the model context repeatedly. The article's example shows a meeting transcript flowing through context twice, potentially adding **50,000+ tokens**.

## Proposed Solution: Code-Based Tool Interaction

Rather than exposing tools as direct function calls, agents can write code to interact with MCP servers. This approach allows:

- **On-demand tool discovery** — agents explore a filesystem structure to find and load only needed tool definitions.
- **In-environment data filtering** — large datasets (like 10,000-row spreadsheets) can be filtered in the execution environment before results reach the model.
- **Efficient control flow** — loops, conditionals, and error handling execute without chaining individual tool calls.

The article claims this approach reduced token usage from **150,000 to 2,000 tokens — a 98.7% reduction**.

## Additional Benefits

- **Privacy preservation** — sensitive data can remain in the execution environment, with tokenization preventing PII from entering model context.
- **State persistence** — agents can save progress to files and develop reusable skills for future tasks.
- **Reduced latency** — complex logic executes in code rather than waiting for model inference on conditional evaluations.

## Implementation Considerations

The article acknowledges that code execution introduces operational complexity requiring sandboxing, resource limits, and security monitoring. These infrastructure requirements must be weighed against efficiency gains.
