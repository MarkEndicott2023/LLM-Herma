# Building Effective Agents

**Source:** https://www.anthropic.com/engineering/building-effective-agents
**Authors:** Erik S. and Barry Zhang
**Published:** Dec 19, 2024
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text. Use this as a navigation/curation aid; refer to the source URL for full prose.

---

## 1. Introduction
- Anthropic has worked with dozens of teams building LLM agents across industries.
- Most successful implementations use "simple, composable patterns rather than complex frameworks."
- Post shares lessons from customer work and internal agent development.

---

## 2. What Are Agents?

### Key Definitions
- **Agentic systems:** umbrella term for all LLM agent variations.
- **Workflows:** systems where LLMs and tools operate through predefined code paths.
- **Agents:** systems where LLMs dynamically direct their own processes and tool usage, maintaining control.

### Distinction
- Workflows offer predetermined execution routes.
- Agents enable model-driven decision-making with dynamic control.

---

## 3. When (and When Not) to Use Agents

- "Find the simplest solution possible, and only increase complexity when needed."
- Agentic systems trade latency and cost for better task performance.
- For well-defined tasks with predictable paths: workflows provide predictability and consistency.
- For tasks requiring flexibility and model-driven decisions at scale: agents are preferable.
- For many applications: optimizing single LLM calls with retrieval and in-context examples suffices.

---

## 4. When and How to Use Frameworks

**Available Frameworks Listed:**
- Claude Agent SDK
- Strands Agents SDK by AWS
- Rivet (drag-and-drop GUI LLM workflow builder)
- Vellum (GUI tool for building and testing complex workflows)

**Framework Benefits:**
- Simplify standard tasks: LLM calls, tool definition/parsing, call chaining.
- Enable quick starts.

**Framework Drawbacks:**
- Create abstraction layers that obscure underlying prompts and responses.
- Make debugging harder.
- Encourage unnecessary complexity.

**Recommendations:**
- Start by using LLM APIs directly; many patterns require only a few lines of code.
- If using frameworks, ensure understanding of underlying code.
- Incorrect assumptions about framework internals cause common customer errors.

---

## 5. Building Blocks, Workflows, and Agents

### 5.1 Building Block: The Augmented LLM
- Basic foundation: LLM enhanced with augmentations (retrieval, tools, memory).
- Current models can actively generate search queries, select appropriate tools, determine information to retain.
- Tailor capabilities to specific use cases.
- Ensure easy, well-documented interface for the LLM.
- Model Context Protocol allows developers to integrate with third-party tools via simple client implementation.

[Diagram: The Augmented LLM — shows LLM with retrieval, tools, and memory capabilities]

### 5.2 Workflow Pattern: Prompt Chaining

- **Definition:** decomposes tasks into a sequence of steps where each LLM call processes previous output.
- Can add programmatic checks ("gates") on intermediate steps to ensure process stays on track.

**When to Use:**
- Tasks easily decomposed into fixed subtasks.
- Goal is trading latency for higher accuracy.
- Each LLM call becomes simpler.

**Examples:**
- Generate marketing copy, then translate to a different language.
- Write document outline, verify against criteria, then write full document based on outline.

[Diagram: The Prompt Chaining Workflow — sequential LLM calls with gates]

### 5.3 Workflow Pattern: Routing

- **Definition:** classifies input and directs to specialized follow-up task.
- Enables separation of concerns and specialized prompts; prevents optimization for one input type from hurting performance on others.

**When to Use:**
- Complex tasks with distinct categories better handled separately.
- Classification can be handled accurately by LLM or traditional methods.

**Examples:**
- Direct customer service queries (general, refunds, technical) to different processes, prompts, tools.
- Route easy/common questions to cost-efficient models (Claude Haiku 4.5) and hard/unusual questions to capable models (Claude Sonnet 4.5).

[Diagram: The Routing Workflow — input classification leading to specialized branches]

### 5.4 Workflow Pattern: Parallelization

- **Definition:** LLMs work simultaneously on a task with outputs aggregated programmatically.

**Two Variations:**
- **Sectioning:** breaking task into independent subtasks run in parallel.
- **Voting:** running same task multiple times to get diverse outputs.

**Performance Insight:** for complex tasks with multiple considerations, LLMs generally perform better when each consideration receives a dedicated LLM call.

**Sectioning Examples:**
- Guardrails: one instance processes queries while another screens for inappropriate content.
- LLM evaluation: each call evaluates a different performance aspect.

**Voting Examples:**
- Code review for vulnerabilities across multiple prompt variations.
- Content appropriateness evaluation with multiple prompts assessing different aspects or requiring different vote thresholds.

[Diagram: The Parallelization Workflow — sectioning and voting patterns]

### 5.5 Workflow Pattern: Orchestrator-Workers

- **Definition:** central LLM dynamically breaks down tasks, delegates to worker LLMs, and synthesizes results.
- **Key difference from Parallelization:** flexibility in subtask determination — subtasks aren't predefined but determined by orchestrator based on specific input.

**When to Use:**
- Complex tasks where required subtasks can't be predicted.
- Need for dynamic task decomposition.

**Examples:**
- Coding products making complex changes across multiple files.
- Search tasks requiring information gathering and analysis from multiple sources.

[Diagram: The Orchestrator-Workers Workflow — central coordinator with multiple worker branches]

### 5.6 Workflow Pattern: Evaluator-Optimizer

- **Definition:** one LLM call generates a response while another provides evaluation and feedback in a loop.

**When to Use:**
- Clear evaluation criteria exist.
- Iterative refinement provides measurable value.
- Two success indicators:
  - LLM responses demonstrably improve with human feedback articulation.
  - LLM can provide such feedback itself.

**Examples:**
- Literary translation where translator LLM may miss nuances but evaluator LLM provides useful critique.
- Complex search tasks requiring multiple search/analysis rounds where evaluator determines if further searches warranted.

[Diagram: The Evaluator-Optimizer Workflow — iterative feedback loop]

### 5.7 Pattern: Autonomous Agents

- **Definition:** agents that begin with user command or discussion, then plan and operate independently with potential returns to human for information/judgment.
- **Critical implementation aspect:** agents must gain "ground truth" from environment at each step (tool results, code execution) to assess progress.

**Operational Features:**
- Can pause for human feedback at checkpoints.
- Include stopping conditions (maximum iterations) to maintain control.
- Task terminates upon completion or hitting stopping conditions.

**Implementation Simplicity:** often straightforward — just LLMs using tools based on environmental feedback in a loop.

**Critical Design Element:** tool design and documentation are crucial; requires equal attention to prompt engineering.

**When to Use:**
- Open-ended problems where required steps can't be predicted.
- Can't hardcode fixed execution path.
- LLM will operate for many turns.
- Some level of trust in LLM decision-making exists.

**Essential Precautions:**
- Extensive testing in sandboxed environments required.
- Appropriate guardrails essential.
- Higher costs than simpler approaches.
- Potential for compounding errors.

**Anthropic Implementation Examples:**
- Coding agent resolving SWE-bench tasks (edits to many files based on task description).
- "Computer use" reference implementation where Claude uses computer to accomplish tasks.

[Diagram: High-level flow of a coding agent — multi-step iteration with feedback loops]

---

## 6. Combining and Customizing These Patterns
- Building blocks aren't prescriptive — they're common patterns developers can shape and combine.
- Key to success: measuring performance and iterating on implementations.
- Add complexity only when it demonstrably improves outcomes.

---

## 7. Summary and Core Principles

**Success Philosophy:**
- "Success in the LLM space isn't about building the most sophisticated system."
- Build "the right system for your needs."

**Implementation Sequence:**
1. Start with simple prompts.
2. Optimize with comprehensive evaluation.
3. Add multi-step agentic systems only when simpler solutions fall short.

**Three Core Principles for Agent Implementation:**
1. **Simplicity:** maintain simple agent design.
2. **Transparency:** explicitly show agent's planning steps.
3. **Documentation and Testing:** carefully craft agent-computer interface (ACI) through thorough tool documentation and testing.

---

## 8. Appendix 1: Agents in Practice

### A. Customer Support
- Combines familiar chatbot interfaces with enhanced tool capabilities.
- Support interactions naturally follow conversation flow while requiring external information/actions.
- Tools integrate customer data, order history, knowledge base articles.
- Programmatic actions: issuing refunds, updating tickets.
- Clear success measurement through user-defined resolutions.
- **Market validation:** several companies use usage-based pricing (charging only for successful resolutions).

### B. Coding Agents
- Capabilities evolved from code completion to autonomous problem-solving.
- Code solutions verifiable through automated tests; agents iterate on solutions using test results as feedback.
- Problem space well-defined and structured.
- Output quality measurable objectively.
- **Anthropic implementation:** agents now solve real GitHub issues in SWE-bench Verified benchmark based on pull request description alone.
- **Important limitation:** while automated testing verifies functionality, human review remains crucial for ensuring solutions align with broader system requirements.

---

## 9. Appendix 2: Prompt Engineering Your Tools

- Tool definitions and specifications require same prompt engineering attention as overall prompts.
- Tools enable Claude to interact with external services/APIs by specifying exact structure and definition.
- Claude's API response includes tool use block when invoking tool.
- Developers specify tool format and structure.

**Format Selection Principle:** multiple ways exist to specify same action (e.g., file edits via diff vs. file rewrite; structured output via markdown vs. JSON). Some formats are much more difficult for LLM to write than others:
- Writing diffs requires knowing line count changes before writing new code.
- Writing code in JSON requires extra escaping of newlines and quotes.

**Tool Format Recommendations:**
1. Give the model enough tokens to "think" before getting stuck.
2. Keep format close to naturally occurring internet text.
3. Ensure no formatting "overhead" (e.g., accurate line counts, string-escaping).

**Agent-Computer Interface (ACI) Design Philosophy:**
- Invest in ACI design effort equivalent to human-computer interface (HCI) effort.

**Specific ACI Best Practices:**
1. **User Perspective Test:** put yourself in the model's shoes — is tool usage obvious from description/parameters? Good tool definitions include example usage, edge cases, input format requirements, clear boundaries from other tools.
2. **Parameter Optimization:** change parameter names/descriptions for clarity. Treat as writing docstring for junior developer.
3. **Empirical Testing:** test model's tool usage. Run many example inputs in Anthropic workbench. Observe mistakes and iterate.
4. **Error Prevention (Poka-yoke):** change arguments to make mistakes harder. Example from SWE-bench agent: switched from relative to absolute filepaths because model made path mistakes after moving out of root directory. Result: model used absolute filepaths flawlessly.

**Development Investment Reality:** SWE-bench agent implementation spent more time optimizing tools than overall prompt.
