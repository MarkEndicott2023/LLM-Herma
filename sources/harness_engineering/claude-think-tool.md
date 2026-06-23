# The "Think" Tool: Enabling Claude to Stop and Think in Complex Tool Use Situations

**Source:** https://www.anthropic.com/engineering/claude-think-tool
**Published:** Mar 20, 2025
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text. The original article includes an update noting that extended thinking is now generally recommended over the dedicated "think" tool.

---

## 1. Introduction & Core Concept
- The "think" tool creates dedicated reasoning space during complex tasks.
- Different from extended thinking — operates **after** response generation begins, not before.
- Particularly effective for agentic tool use scenarios.
- Minimal implementation overhead required.

## 2. What Is the "Think" Tool?

**Definitional Distinctions:**
- "Think" tool allows mid-response pauses for structured reflection.
- Extended thinking occurs before response generation starts.
- "Think" tool suited for processing external tool call results.
- Extended thinking recommended for simpler scenarios, non-sequential tool calls.
- "Think" tool better for complex tool chains, policy-heavy environments, sequential decisions.

**Sample Tool Implementation (JSON):**
```json
{
  "name": "think",
  "description": "Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.",
  "input_schema": {
    "type": "object",
    "properties": {
      "thought": {
        "type": "string",
        "description": "A thought to think about."
      }
    },
    "required": ["thought"]
  }
}
```

---

## 3. Performance on τ-Bench

**Benchmark Overview:**
- τ-Bench evaluates tool use in realistic customer service scenarios.
- Tests navigation of complex conversations, policy adherence, database manipulation.
- Primary metric: **pass^k** (probability all k trials succeed, averaged across tasks). Unlike pass@k, measures consistency and reliability.

**Airline Domain Results:**
- Baseline (no tool, no extended thinking): 0.370.
- "Think" tool with optimized prompt: **0.570** (54% relative improvement).
- Extended thinking alone: 0.412.
- "Think" tool alone: 0.404.

**Retail Domain Results:**
- Baseline: 0.783.
- "Think" tool alone: **0.812**.
- Extended thinking: 0.770.

**Optimized Prompting Example (Airline Domain):**
```
Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness
```

**Key τ-Bench Insights:**
- Prompting significantly impacts difficult domains; less critical for easier domains.
- Improvements maintained across multiple trials (pass^k up to k=5).
- Demonstrates enhanced edge-case handling.

---

## 4. Performance on SWE-Bench

**Adapted Tool Definition:**
```json
{
  "name": "think",
  "description": "Use the tool to think about something. It will not obtain new information or make any changes to the repository, but just log the thought. Use it when complex reasoning or brainstorming is needed.",
  "input_schema": {
    "type": "object",
    "properties": {
      "thought": {
        "type": "string",
        "description": "Your thoughts."
      }
    },
    "required": ["thought"]
  }
}
```

**Evaluation Results:**
- Claude 3.7 Sonnet achieved state-of-the-art score of **0.623**.
- "Think" tool improved performance by **1.6% on average**.
- Statistical significance: Welch's t-test: t(38.89) = 6.71, p < .001, d = 1.47.
- Sample sizes: n=30 with tool, n=144 without.

---

## 5. When to Use the "Think" Tool

**Recommended:**
- Tool output analysis requiring careful processing and potential backtracking.
- Policy-heavy environments with detailed compliance guidelines.
- Sequential decision-making where mistakes have high costs.
- Multi-step domains with interdependent actions.

**Not Recommended:**
- Non-sequential tool calls (single or parallel calls).
- Simple instruction following without numerous constraints.
- Cases where default model behavior already performs adequately.

---

## 6. Implementation Best Practices

**Practice 1: Strategic Prompting with Examples**
- Provide clear instructions on when/how to use "think" tool.
- Domain-specific examples substantially improve effectiveness.
- Examples should show:
  - Expected reasoning detail level.
  - Breaking complex instructions into actionable steps.
  - Decision trees for common scenarios.
  - Information completeness checks.

**Practice 2: System Prompt Placement**
- Place complex/lengthy "think" instructions in system prompt rather than tool description.
- Provides broader context integration.
- Improves model's overall behavioral integration.

---

## 7. Getting Started

1. Test with agentic tool use scenarios where Claude struggles.
2. Add customized tool definition to domain; include usage instructions and examples in system prompt.
3. Monitor Claude's practical tool usage; refine prompts to encourage effective thinking patterns.

---

## 8. Additional Findings

- Claude 3.5 Sonnet (New) also achieves performance gains with same configuration as 3.7 Sonnet.
- Minimal downside risk — external behavior unchanged unless Claude uses tool.
- Does not interfere with existing tools or workflows.
- Increases prompt length and output tokens.

---

## Update Note
Article includes an update stating extended thinking capabilities have improved sufficiently that "extended thinking" is now recommended over the dedicated "think" tool for most use cases, with extended thinking providing better integration and performance.
