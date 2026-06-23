# Effective Context Engineering for AI Agents

**Source:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Authors:** Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield (Anthropic Applied AI team)
**Published:** Sep 29, 2025
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text. Use this as a navigation/curation aid; refer to the source URL for full prose.

---

## 1. Context Engineering vs. Prompt Engineering

- Context engineering represents progression beyond prompt engineering as AI systems become more complex.
- Scope shift from optimizing individual prompts to managing entire context state across multi-turn interactions.

**Key Definitions:**
- Context = "the set of tokens included when sampling from a large-language model."
- Engineering problem = optimizing token utility against LLM constraints.
- Prompt engineering = writing and organizing instructions for optimal outcomes.
- Context engineering = "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."
- Includes managing system instructions, tools, Model Context Protocol (MCP), external data, and message history.
- Context engineering is iterative; curation occurs at each inference step.
- Agent loops generate accumulating data requiring cyclical refinement.

---

## 2. Why Context Engineering Is Important

**Problem: Context Rot**
- "As the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."
- Context must be treated as a finite resource with diminishing marginal returns.
- LLMs possess a limited "attention budget" similar to human working memory.

**Architectural Root Causes:**
- Transformer architecture requires every token attending to every other token across context.
- Creates n² pairwise relationships for n tokens.
- Longer contexts stretch model's ability to capture these relationships.
- Models trained on distributions where shorter sequences predominate, creating less specialized parameters for context-wide dependencies.
- Position encoding interpolation allows longer sequences but with degradation.
- Performance degrades gradually rather than at a hard cliff, showing reduced precision for retrieval and long-range reasoning.

---

## 3. The Anatomy of Effective Context

**Overarching Principle:** find "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

### 3.1 System Prompts

**The "Altitude" Concept:**
- Avoid brittle, hardcoded complex logic in prompts (creates fragility and maintenance complexity).
- Avoid vague, high-level guidance lacking concrete signals or falsely assuming shared understanding.
- Target optimal zone: "specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics."

**Structural Recommendations:**
- Organize into distinct sections using XML tagging or Markdown headers (e.g., `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`).
- Exact formatting becomes less critical as models improve.
- Strive for minimal information set fully outlining expected behavior.
- Minimal ≠ short; provide sufficient up-front information.

**Implementation Approach:**
- Start with minimal prompt using best available model.
- Test initial performance.
- Add clear instructions and examples based on identified failure modes.

### 3.2 Tools

- Tools define the contract between agents and their information/action space.
- Must promote efficiency in both token output and encouraging efficient behaviors.
- Should be self-contained, robust to error, extremely clear regarding intended use.
- Input parameters must be descriptive, unambiguous, and play to model strengths.

**Common Failure Mode:**
- Bloated tool sets with excessive functionality or ambiguous decision points.
- "If engineers cannot definitively specify which tool to use in a given situation, agents cannot be expected to perform better."

**Maintenance Benefits:**
- Curating minimal viable tool sets enables more reliable maintenance.
- Simplifies context pruning over long interactions.

### 3.3 Examples (Few-Shot Prompting)

- Continue strongly advising use of examples.
- Avoid stuffing laundry lists of edge cases into prompts.
- Curate diverse, canonical examples portraying expected behavior.
- "Examples are the 'pictures' worth a thousand words" for LLMs.

**Overall Guidance:** Keep context "informative, yet tight" across all components.

---

## 4. Context Retrieval and Agentic Search

**Definition of Agents:** "LLMs autonomously using tools in a loop." Field is converging on this paradigm; autonomy scales with model capability.

**Shift in Context Design Thinking:**
- Moving from embedding-based pre-inference retrieval to "just in time" context strategies.
- Rather than pre-processing all relevant data upfront, agents maintain lightweight identifiers and dynamically load data at runtime.

**Just-In-Time Approach:**
- Uses file paths, stored queries, web links as references.
- Dynamic loading via tools at runtime.
- Example: Claude Code performs complex data analysis over large databases using targeted queries, storing results, using Bash commands (`head`, `tail`) to analyze without loading full data objects into context.
- Mirrors human cognition of external organization systems (file systems, inboxes, bookmarks) rather than memorizing entire corpuses.

**Metadata as Behavioral Signal:**
- File names, folder hierarchies, naming conventions, timestamps provide important signals.
- Example: file named `test_utils.py` in `tests` folder implies different purpose than same file in `src/core_logic/`.

**Progressive Disclosure:**
- Agents incrementally discover relevant context through exploration.
- Each interaction yields context informing the next decision.
- File sizes suggest complexity; naming conventions hint at purpose; timestamps proxy for relevance.
- Agents maintain only necessary working memory, using note-taking for additional persistence.

**Trade-offs:**
- Runtime exploration slower than pre-computed retrieval.
- Requires opinionated engineering to provide right tools and heuristics.
- Risk of context waste through tool misuse, dead-ends, or failure to identify key information.

**Hybrid Strategy:**
- Most effective agents employ a hybrid approach: retrieve some data upfront for speed while pursuing autonomous exploration at discretion.
- Example: Claude Code naively drops `CLAUDE.md` files into context upfront while using primitives like `glob` and `grep` for just-in-time file retrieval.
- Avoids issues of stale indexing and complex syntax trees.
- Better suited for less dynamic content (legal, finance work).

**Future Direction:** as model capabilities improve, agentic design trends toward "letting intelligent models act intelligently, with progressively less human curation." Best advice: "do the simplest thing that works."

---

## 5. Context Engineering for Long-Horizon Tasks

**Challenge:** tasks spanning tens of minutes to multiple hours require maintaining coherence, context, and goal-directed behavior exceeding context window limits. Examples: large codebase migrations, comprehensive research projects.

**Context Window Limitations:**
- Waiting for larger context windows is insufficient as solution.
- "Likely that for the foreseeable future, context windows of all sizes will be subject to context pollution and information relevance concerns."
- Strongest agent performance requires addressing these constraints directly.

### 5.1 Compaction

- Practice of summarizing conversation nearing context window limit and reinitiating new context window with summary.
- Distills contents in high-fidelity manner enabling continued work with minimal performance degradation.
- First lever in context engineering for better long-term coherence.

**Implementation Example (Claude Code):** passes message history to model for summarization; model preserves architectural decisions, unresolved bugs, implementation details while discarding redundant tool outputs. Agent continues with compressed context plus five most recently accessed files.

**Critical Balance:**
- Art lies in selecting what to keep versus discard.
- Overly aggressive compaction risks losing subtle but critical context.
- Only later becomes apparent which details prove important.

**Implementation Guidance:**
- Carefully tune compaction prompt on complex agent traces.
- Start by maximizing recall ensuring prompt captures all relevant information.
- Iterate to improve precision by eliminating superfluous content.

**Low-Hanging Optimization:**
- Clearing tool calls and results once a tool is called deep in history.
- Lightest-touch compaction form: tool result clearing.
- Recently launched as feature on Claude Developer Platform.

### 5.2 Structured Note-Taking

- Agent regularly writes notes persisted to memory outside context window.
- Notes retrieved back into context window at later times.
- Provides persistent memory with minimal overhead.

**Pattern Description:**
- Agent maintains external notes (e.g., to-do lists, `NOTES.md` files).
- Allows tracking progress across complex tasks.
- Maintains critical context and dependencies across dozens of tool calls.

**Concrete Example: Claude Playing Pokémon**
- Demonstrates memory transforming capabilities in non-coding domains.
- Maintains precise tallies across thousands of game steps.
- Example: "for the last 1,234 steps I've been training my Pokémon in Route 1, Pikachu has gained 8 levels toward the target of 10."
- Develops maps of explored regions without explicit prompting about memory structure.
- Remembers unlocked achievements; maintains strategic notes about combat strategies.
- After context resets, reads own notes and continues multi-hour sequences.

**Platform Support:**
- Anthropic released a memory tool in public beta on Claude Developer Platform (Sonnet 4.5 launch).
- File-based system for storing and consulting information outside context window.
- Allows agents to build knowledge bases over time, maintain project state across sessions, reference previous work without keeping everything in context.

### 5.3 Sub-Agent Architectures

- Rather than one agent maintaining state across entire project, specialized sub-agents handle focused tasks.
- Each maintains a clean context window.
- Main agent coordinates high-level plan while sub-agents perform deep technical work or information retrieval.

**Mechanism:**
- Sub-agents explore extensively using tens of thousands of tokens or more.
- Return only condensed, distilled summary of work (typically 1,000–2,000 tokens).
- Detailed search context remains isolated within sub-agents.
- Lead agent focuses on synthesizing and analyzing results.

**Benefits:**
- Clear separation of concerns.
- Showed substantial improvement over single-agent systems on complex research tasks.
- Reference: "How we built our multi-agent research system."

**Task-Dependent Selection:**
- Compaction: maintains conversational flow for tasks requiring extensive back-and-forth.
- Note-taking: excels for iterative development with clear milestones.
- Multi-agent architectures: handle complex research and analysis where parallel exploration yields dividends.

---

## 6. Conclusion

**Core Paradigm Shift:**
- Context engineering represents fundamental shift in building with LLMs.
- Challenge moves beyond "crafting the perfect prompt" to "thoughtfully curating what information enters the model's limited attention budget at each step."

**Unified Principle:** whether implementing compaction, designing token-efficient tools, or enabling autonomous exploration: "find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."

**Evolution & Scaling:**
- Techniques continue evolving as models improve.
- Smarter models require less prescriptive engineering.
- Agents operate with more autonomy.
- Treating context as "precious, finite resource" remains central regardless of capability scaling.
