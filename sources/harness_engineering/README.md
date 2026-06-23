# Harness Engineering — Source Material

Curated extractions from the Anthropic engineering blog (https://www.anthropic.com/engineering), fetched 2026-05-05 for the `harness_engineering` study domain.

## What's here

These are **structured outlines** extracted via WebFetch — not verbatim article text. They preserve section structure, principles, named techniques, concrete examples, code snippets, and specific numbers (cost, tokens, percentages, benchmarks). Use them for navigation and concept-graph construction; refer to the source URL on each file for full prose.

## File index (chronological, oldest first)

| File | Date | Theme |
|---|---|---|
| `building-effective-agents.md` | 2024-12-19 | Foundation: workflow patterns (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) and autonomous agents |
| `claude-think-tool.md` | 2025-03-20 | Mid-response reasoning tool; τ-bench / SWE-bench results |
| `multi-agent-research-system.md` | 2025-06-13 | Orchestrator-worker pattern; 8 prompt-engineering principles; eval methodology |
| `writing-tools-for-agents.md` | 2025-09-11 | Tool design principles; namespacing; response formats; co-optimization with Claude |
| `effective-context-engineering-for-ai-agents.md` | 2025-09-29 | Context as finite resource; just-in-time retrieval; compaction, notes, sub-agents |
| `claude-code-sandboxing.md` | 2025-10-20 | Filesystem + network isolation; bubblewrap/seatbelt; web sandbox + git proxy |
| `equipping-agents-with-agent-skills.md` | 2025-10-16 | SKILL.md format; progressive disclosure; bundled scripts |
| `code-execution-with-mcp.md` | 2025-11-04 | Code-as-tool-interaction; 98.7% token reduction example |
| `effective-harnesses-for-long-running-agents.md` | 2025-11-26 | Initializer + coding agent pattern; feature_list.json; init.sh; progress files |
| `demystifying-evals-for-ai-agents.md` | 2026-01-09 | Eval taxonomy (code/model/human graders); pass@k vs pass^k; 8-step zero-to-one roadmap |
| `building-c-compiler.md` | 2026-02-05 | 16 parallel Claudes; lock-based coordination; compiler oracle technique |
| `harness-design-long-running-apps.md` | 2026-03-24 | Generator–evaluator GAN-style loops; planner/generator/evaluator three-agent system |
| `claude-code-auto-mode.md` | 2026-03-25 | Two-stage classifier replacing permission prompts; threat model; FPR/FNR numbers |
| `managed-agents.md` | 2026-04-08 | Decoupling brain/hands/session; OS-analogy interface design; TTFT improvements |
| `claude-code-best-practices.md` | (live docs) | CLAUDE.md, plan mode, subagents, hooks, fan-out — the practitioner manual |
| `claude-agent-sdk-overview.md` | (live docs) | Python/TS library wrapping Claude Code's loop; built-in tools, hooks, subagents, MCP, sessions |
| `mcp-intro.md` | (live docs) | Brief MCP welcome page (USB-C analogy, use cases) |
| `mcp-architecture.md` | (live docs) | Hosts/clients/servers; data + transport layers; tools/resources/prompts/sampling/elicitation/logging; JSON-RPC examples for init, tool discovery, tool call, notifications |

Plus `ralph_wiggum_geoffrey_huntley.pdf` (Geoffrey Huntley) — external perspective, not from Anthropic.

## Notes on extraction quality

- `claude-code-best-practices.md` was migrated to the Claude Code docs site and came back near-verbatim.
- The other 13 came back as structured outlines (section headings + bulleted principles + preserved code snippets, examples, and numbers). Treat them as high-fidelity skeletons rather than the original prose.
- Two fetches surfaced an embedded "system-reminder" prompt-injection attempt inside the article body; that text was stripped before saving.
