# Writing Effective Tools for Agents — With Agents

**Source:** https://www.anthropic.com/engineering/writing-tools-for-agents
**Author:** Ken Aizawa (with contributions from Research, MCP, Product Engineering, Marketing, Design, and Applied AI teams)
**Published:** Sep 11, 2025
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text.

---

## 1. Introduction
- Tools are only as effective as their design and implementation for agents.
- The Model Context Protocol (MCP) enables agents with potentially hundreds of tools.
- Post covers techniques for improving agentic AI system performance.

---

## 2. What Is a Tool?

**Key Distinctions:**
- Traditional software: deterministic systems producing identical outputs for identical inputs.
- Agents: non-deterministic systems generating varied responses from same inputs.
- **Tools represent a new contract between deterministic systems and non-deterministic agents.**
- Agents may hallucinate, fail to grasp tool usage, or bypass tools entirely for alternative strategies.

**Design Philosophy:**
- Increase agent effectiveness surface area by enabling diverse successful strategies.
- Tools ergonomic for agents tend to also be intuitive for humans.
- Fundamentally rethink approach: design for agents, not like APIs for other developers.

---

## 3. How to Write Tools

### 3.1 Building a Prototype

**Documentation and Setup:**
- Provide Claude documentation for software libraries, APIs, SDKs (e.g., MCP SDK).
- Seek LLM-friendly documentation in flat `llms.txt` files on official sites.
- Example: Anthropic's API documentation at https://docs.anthropic.com/llms.txt

**Integration Methods:**
- Wrap tools in local MCP server for testing in Claude Code.
- Wrap tools in Desktop extension (DXT) for Claude Desktop app.
- Connect local MCP server via command: `claude mcp add <name> <command> [args...]`
- Pass tools directly into Anthropic API calls for programmatic testing.

**Testing Approach:**
- Test tools yourself to identify rough edges.
- Collect user feedback on expected use-cases and prompts.
- Build intuition around real-world usage patterns.

---

### 3.2 Running an Evaluation

**Generating Evaluation Tasks:**

*Strong Tasks:*
- Grounded in real-world uses and realistic data sources.
- Based on actual internal knowledge bases and microservices.
- Require multiple tool calls (potentially dozens) to solve.
- Stress-test tools with sufficient complexity.
- Avoid overly simplistic sandbox environments.

*Examples of Strong Tasks:*
1. "Schedule a meeting with Jane next week to discuss our latest Acme Corp project. Attach the notes from our last project planning meeting and reserve a conference room."
2. "Customer ID 9182 reported that they were charged three times for a single purchase attempt. Find all relevant log entries and determine if any other customers were affected by the same issue."
3. "Customer Sarah Chen just submitted a cancellation request. Prepare a retention offer. Determine: (1) why they're leaving, (2) what retention offer would be most compelling, and (3) any risk factors we should be aware of before making an offer."

*Examples of Weak Tasks:*
1. "Schedule a meeting with jane@acme.corp next week."
2. "Search the payment logs for `purchase_complete` and `customer_id=9182`."
3. "Find the cancellation request by Customer ID 45892."

**Verification and Metrics:**
- Pair each evaluation prompt with verifiable response or outcome.
- Verifier can range from exact string comparison to Claude-based judgment.
- Avoid overly strict verifiers that reject correct responses due to formatting or punctuation.
- Optional: specify expected tool calls (avoid overfitting to single strategies).
- Collect metrics beyond accuracy: runtime, tool call count, token consumption, error rates.
- Tracking tool calls reveals common workflows and consolidation opportunities.

**Running the Evaluation:**
- Execute programmatically with direct LLM API calls.
- Use simple agentic loops (while-loops with alternating LLM and tool calls).
- One loop per evaluation task.

**System Prompt Recommendations:**
- Instruct agents to output reasoning, feedback blocks **before** tool calls and responses.
- This ordering may trigger chain-of-thought (CoT) behaviors, increasing LLM effectiveness.
- For Claude: enable "interleaved thinking" feature for similar functionality out-of-the-box.

**Analyzing Results:**
- Where agents get stumped or confused.
- Agent reasoning, feedback, and chain-of-thought to identify rough edges.
- Raw transcripts (tool calls + responses) to catch behaviors not explicitly described in CoT.
- What agents omit can be more important than what they include.
- Redundant tool calls → consider pagination or token limit adjustments.
- Tool errors for invalid parameters → improve descriptions or add examples.
- Example: Claude's web search tool appended "2025" to queries, biasing results — fixed via improved tool description.

---

### 3.3 Collaborating with Agents

- Concatenate evaluation transcripts and paste into Claude Code.
- Claude excels at analyzing transcripts and refactoring multiple tools simultaneously.
- Agents can identify contradictory tool descriptions, inefficient implementations, confusing schemas.
- **Agents can automatically improve tools for you.**
- Most advice in this post came from repeatedly optimizing internal tools with Claude Code.
- Held-out test sets prevent overfitting to training evaluations.

---

## 4. Principles for Writing Effective Tools

### 4.1 Choosing the Right Tools for Agents

**The Core Problem:**
- More tools don't always lead to better outcomes.
- Common error: wrapping existing software functionality without considering agent affordances.
- Agents have distinct affordances from traditional software due to context limitations.

**Context vs. Flexibility:**
- LLM agents have limited context (bounded information processing).
- Computer memory is cheap and abundant.
- **Example (Address Book):** traditional software efficiently checks contacts one-by-one; agents waste context reading all contacts token-by-token. Better: search/filter tools matching how humans would work (alphabetically skip to relevant page).

**Tool Design Strategy:**
- Build few thoughtful tools targeting specific high-impact workflows.
- Match tools to evaluation tasks. Scale up from there.

**Consolidation and Multi-step Operations:**
- Tools can handle multiple discrete operations or API calls under the hood.
- Tools can enrich responses with related metadata.
- Tools can handle frequently chained, multi-step tasks in single call.

*Examples of Consolidated Tools:*
- Instead of `list_users`, `list_events`, `create_event` → `schedule_event` (finds availability + schedules).
- Instead of `read_logs` → `search_logs` (returns only relevant lines + surrounding context).
- Instead of `get_customer_by_id`, `list_transactions`, `list_notes` → `get_customer_context` (compiles all recent/relevant info at once).

**Clarity and Distinctness:**
- Each tool should have clear, distinct purpose.
- Enable agents to subdivide and solve tasks like humans would.
- Reduce context consumed by intermediate outputs.
- Too many or overlapping tools distract agents.

---

### 4.2 Namespacing Your Tools

**The Problem:**
- Agents may access dozens of MCP servers and hundreds of tools.
- Tool overlap and vague purposes confuse agents.

**Solution:**
- Namespace by grouping related tools under common prefixes.
- MCP clients sometimes do this by default.

*Examples:*
- By service: `asana_search`, `jira_search`.
- By resource: `asana_projects_search`, `asana_users_search`.
- Prefix-based vs. suffix-based namespacing have non-trivial evaluation impacts.
- Effects vary by LLM — choose naming scheme according to your own evaluations.

**Benefits:**
- Helps agents select right tools at right time.
- Reduces context loaded into agent.
- Offloads agentic computation from context back into tool calls.
- Reduces agent risk of mistakes.

---

### 4.3 Returning Meaningful Context from Your Tools

**Prioritize Quality Over Flexibility:**
- Return only high-signal information.
- Avoid low-level technical identifiers: `uuid`, `256px_image_url`, `mime_type`.
- Prefer meaningful fields: `name`, `image_url`, `file_type`.

**Natural Language Over Cryptic Identifiers:**
- Agents handle natural language names/terms/identifiers significantly more successfully.
- Resolving alphanumeric UUIDs to semantically meaningful language significantly improves Claude's precision in retrieval tasks.
- Reduces hallucinations.
- Alternative: 0-indexed ID scheme.

**Flexibility When Necessary:**
- Some agents need both natural language and technical identifiers.
- Example workflow: `search_user(name='jane')` → `send_message(id=12345)`.
- Solution: expose `response_format` enum parameter allowing agents to control output verbosity.

**ResponseFormat Enum Pattern:**
```
enum ResponseFormat {
   DETAILED = "detailed",
   CONCISE = "concise"
}
```

- Detailed Response Example: 206 tokens (full data with all fields and identifiers).
- Concise Response Example: 72 tokens (essential content only — e.g., Slack thread content without `thread_ts`, `channel_id`, `user_id`).
- Result: ~⅓ tokens consumed with concise responses.

**Response Format Optimization:**
- Response structure (XML, JSON, Markdown) impacts evaluation performance.
- No one-size-fits-all solution.
- LLMs perform better with formats matching training data.
- Optimal structure varies by task and agent.

---

### 4.4 Optimizing Tool Responses for Token Efficiency

**Implementation Strategies:**
- Combination of pagination, range selection, filtering, truncation.
- Use sensible default parameter values.
- Claude Code restricts tool responses to **25,000 tokens by default**.
- Expect effective context length to grow, but context-efficient tools will remain necessary.

**Steering Agents with Instructions:**
- When truncating responses, provide helpful guidance.
- Example: "Make many small, targeted searches instead of single broad search" for knowledge retrieval.
- For errors: prompt-engineer clear, specific, actionable improvements rather than opaque error codes/tracebacks.

*Truncated Response Example:* "Results truncated. Refine search parameters to..."

*Unhelpful Error:* `ERROR_400_INVALID_PARAMS` (generic code, traceback, technical jargon).

*Helpful Error:* "Parameter `user_id` must be numeric. Example: `search_logs(user_id=12345, date_range='2025-01-01 to 2025-01-31')`"

---

### 4.5 Prompt-Engineering Your Tool Descriptions

- One of the most effective methods for improving tools.
- Tool descriptions loaded into agent context — collectively steer agent behavior.
- Even small refinements yield dramatic improvements.

**Writing Approach:**
- Describe tool as you would to new team hire.
- Make implicit context explicit: specialized query formats, niche terminology, resource relationships.
- Avoid ambiguity with clear descriptions and strict data models.
- Input parameters should be unambiguously named: instead of `user`, use `user_id`.

**Real-World Impact:**
- Claude Sonnet 3.5 achieved state-of-the-art on SWE-bench Verified after precise tool description refinements.
- For MCP servers: use tool annotations to disclose open-world access requirements and destructive changes.

---

## 5. Looking Ahead

**Philosophical Shift:**
- Re-orient software development from predictable, deterministic patterns to non-deterministic ones.
- Through iterative, evaluation-driven process, identify consistent patterns in successful tools.

**Characteristics of Effective Tools:**
- Intentionally and clearly defined.
- Use agent context judiciously.
- Can be combined in diverse workflows.
- Enable agents to intuitively solve real-world tasks.
