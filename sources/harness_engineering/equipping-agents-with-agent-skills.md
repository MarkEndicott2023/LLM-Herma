# Equipping Agents for the Real World with Agent Skills

**Source:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
**Authors:** Barry Zhang, Keith Lazuka, Mahesh Murag
**Published:** Oct 16, 2025
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text.

---

## Overview
Anthropic introduced **Agent Skills**, a framework enabling Claude to perform specialized tasks through organized collections of instructions, scripts, and resources. Rather than building separate custom agents for each use case, users can equip general-purpose agents with domain-specific expertise by packaging procedural knowledge into composable, reusable capabilities.

## The Anatomy of a Skill

At its core, a skill consists of a directory containing a `SKILL.md` file with required YAML metadata: a `name` and `description`. The framework employs **progressive disclosure** — revealing information in layers rather than all at once.

The system operates across three disclosure levels:

1. **Metadata layer:** skills' names and descriptions load into the system prompt at startup, enabling Claude to determine when each skill applies to a task.
2. **Core content layer:** when Claude identifies a skill as relevant, it reads the complete `SKILL.md` file into context.
3. **Supplementary layers:** skills can bundle additional files (like `reference.md` or `forms.md`) that Claude accesses only as needed for specific scenarios.

This design principle keeps the core skill lean while allowing unbounded context through linked files.

## Skills and the Context Window

When triggered by a user message:
- The context window initially contains the system prompt, skill metadata, and the user's message.
- Claude invokes a Bash tool to read the `SKILL.md` contents when the skill becomes relevant.
- Claude selectively reads bundled files based on task requirements.
- The agent proceeds with newly loaded contextual instructions.

## Code Execution Within Skills

Skills can include executable code — typically Python scripts — that Claude runs as tools. This approach offers advantages over token-based solutions:
- Sorting algorithms execute deterministically rather than through generation.
- Code performs operations that require reliability beyond what language generation provides.
- Example: a PDF skill might include a pre-written Python script that extracts form fields without loading either the script or PDF into context.

## Development and Evaluation Guidelines

- **Start with evaluation:** run agents on representative tasks to identify capability gaps, then build skills incrementally to address shortcomings.
- **Structure for scale:** when `SKILL.md` becomes unwieldy, split content across separate files. Keep mutually exclusive or rarely-used-together contexts separate to reduce token usage.
- **Think from Claude's perspective:** monitor how Claude uses skills in real scenarios. Pay particular attention to skill names and descriptions, which Claude uses when deciding whether to trigger them.
- **Iterate with Claude:** as you work through tasks, ask Claude to capture successful approaches and mistakes into reusable context and code. If the skill causes off-track behavior, request self-reflection on what went wrong.

## Security Considerations

Since skills provide Claude with new capabilities through instructions and code, malicious skills could introduce vulnerabilities or direct Claude toward unintended actions like data exfiltration.

**Recommendation:** install skills only from trusted sources. For less-trusted sources, audit skill contents before use — examine bundled files, code dependencies, and instructions that direct Claude toward external network connections.

## Current Support and Future Direction

Agent Skills currently function across Claude.ai, Claude Code, the Claude Agent SDK, and the Claude Developer Platform. Upcoming features will support the complete lifecycle of creating, editing, discovering, sharing, and using skills.

Future possibilities include enabling agents to create, edit, and evaluate their own skills, allowing them to "codify their own patterns of behavior into reusable capabilities."
