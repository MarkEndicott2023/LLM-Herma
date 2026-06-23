# How We Built Our Multi-Agent Research System

**Source:** https://www.anthropic.com/engineering/multi-agent-research-system
**Authors:** Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford
**Published:** Jun 13, 2025
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text.

---

## Overview
Anthropic's Research feature employs multiple Claude agents working together to explore complex topics more effectively. The system uses an **orchestrator-worker pattern** where a lead agent coordinates research while delegating tasks to specialized subagents operating in parallel.

## Key Benefits of Multi-Agent Systems

- Multi-agent architectures excel at research tasks because they handle unpredictable, open-ended problems requiring dynamic pivoting.
- Internal evaluation: "a multi-agent system with Claude Opus 4 as lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2%."
- The system distributes work across agents with separate context windows, effectively scaling token usage.
- **Three factors explained 95% of performance variance** on the BrowseComp evaluation: token usage (80%), number of tool calls, and model choice.
- Multi-agent systems consume substantially more tokens — approximately **15× more than chat interactions** — making them economically viable only for high-value tasks with significant parallelization potential.

## Architecture and Process Flow

1. **Lead agent planning** — analyzes queries and develops research strategy.
2. **Subagent spawning** — creates specialized agents for parallel exploration.
3. **Iterative searching** — subagents gather information and return findings.
4. **Synthesis and iteration** — lead agent compiles results and determines if more research is needed.
5. **Citation processing** — a CitationAgent attributes all claims to sources.
6. **Final delivery** — results with citations returned to user.

## Eight Prompt Engineering Principles

1. **Think like your agents** — build simulations to observe failure modes.
2. **Teach delegation** — lead agents need clear task decomposition with specific objectives.
3. **Scale effort to complexity** — embed rules for resource allocation based on query type.
4. **Tool design matters** — clear descriptions and explicit heuristics prevent agents from using wrong tools.
5. **Enable self-improvement** — Claude models can diagnose and suggest prompt improvements.
6. **Start wide, narrow down** — begin with broad queries before drilling into specifics.
7. **Guide thinking** — extended thinking mode serves as controllable scratchpad for planning.
8. **Parallel tool calling** — simultaneous searches cut research time by up to 90%.

## Evaluation Approaches

- **Small-scale testing first:** early development benefits from evaluating just 20 representative queries, where prompt changes often produce dramatic effects.
- **LLM-as-judge:** a single model-based judge evaluated outputs against rubrics including factual accuracy, citation accuracy, completeness, source quality, and tool efficiency.
- **Human evaluation:** manual testing catches edge cases, hallucinations, and subtle biases that automated evaluations miss — such as preferring SEO-optimized content over authoritative academic sources.

## Production Engineering Challenges

- **State management:** agents run for extended periods maintaining state across many tool calls. The system implements checkpoints and resumable execution rather than restarting from beginning.
- **Debugging complexity:** non-deterministic agent behavior makes traditional debugging difficult. Full production tracing monitors decision patterns and interaction structures while maintaining user privacy.
- **Deployment strategy:** rainbow deployments gradually shift traffic between versions while keeping both running, preventing updates from disrupting active agents.
- **Synchronous bottlenecks:** currently, lead agents wait for subagent groups to complete sequentially. Asynchronous execution would enable additional parallelism but adds coordination complexity.

## Additional Considerations

- **End-state evaluation:** for agents modifying persistent state, focus on whether final outcomes match goals rather than validating every intermediate step.
- **Long-horizon management:** extended conversations require intelligent context compression and external memory systems. Agents summarize phases and retrieve stored context when approaching token limits.
- **Subagent output architecture:** specialized agents store outputs in external systems rather than routing everything through the lead agent, reducing token overhead and preventing information loss.

## Results and Use Cases

The Clio embedding analysis shows primary usage categories: developing software systems (10%), creating professional content (8%), generating business strategies (8%), academic research support (7%), and information verification (5%).

Human users report finding business opportunities, navigating complex healthcare decisions, resolving technical problems, and saving days of work through research connections they wouldn't have discovered alone.
