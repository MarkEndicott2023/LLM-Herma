# Demystifying Evals for AI Agents

**Source:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
**Authors:** Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe
**Published:** Jan 9, 2026
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text. Use this as a navigation/curation aid; refer to the source URL for full prose.

---

## Introduction
- Agent capabilities that enable usefulness (autonomy, intelligence, flexibility) simultaneously create evaluation challenges.
- Evaluations help teams ship agents confidently by identifying issues before production deployment.
- Reactive debugging loops (catching failures only in production) create cascading issues.
- Evaluation value compounds across an agent's lifecycle.

---

## The Structure of an Evaluation

### Core Evaluation Types
- **Single-turn evaluations:** traditional prompt-response-grading pattern.
- **Multi-turn evaluations:** required as AI capabilities advanced beyond basic chatbot interactions.
- **Agent evaluations:** most complex due to tool use across many turns, state modification, and error propagation.

### Key Definitions
- **Task** (problem/test case): a single test with defined inputs and success criteria.
- **Trial:** one attempt at a task; multiple trials run to account for output variance.
- **Grader:** logic that scores agent performance; tasks can have multiple graders.
- **Transcript** (trace/trajectory): complete record including outputs, tool calls, reasoning, intermediate results; for Anthropic API = full messages array.
- **Outcome:** final environmental state at trial end (e.g., whether reservation exists in database, not just confirmation message).
- **Evaluation harness:** infrastructure running evals end-to-end with instructions, tools, concurrent task execution, step recording, output grading, and result aggregation.
- **Agent harness** (scaffold): system enabling model to act as agent; evaluation assesses harness and model together.
- **Evaluation suite:** collection of tasks measuring specific capabilities or behaviors, typically sharing a broad goal.

### Challenge: Creative Solutions Beyond Static Evals
- Frontier models may discover solutions surpassing evaluation design (example: Claude Opus 4.5 finding flight booking loophole).
- Task described as "failure" may actually represent better user outcome.
- Evaluation design must accommodate valid alternative solutions.

---

## Why Build Evaluations?

### The Breaking Point
- Early-stage teams can succeed with manual testing, dogfooding, and intuition.
- Rigor appears to slow shipping initially but becomes essential after production scale.
- Breaking point: users report degradation and team cannot verify except through guessing.
- Without evals: debugging remains reactive (complaints → manual reproduction → fix → hope no regressions).
- Teams cannot distinguish real regressions from noise.

### Real-World Progressions
- **Claude Code:** started with fast employee/user feedback iteration; later added narrow evals (concision, file edits); evolved to complex behavior evals (over-engineering); evals now guide research-product collaboration alongside production monitoring and A/B tests.
- **Descript:** defined success on three dimensions (don't break things, do what asked, do it well); evolved from manual to LLM graders with periodic human calibration; now runs separate quality benchmarking and regression suites.
- **Bolt:** built evals 3 months after launch when already widely used; implemented static analysis, browser agent testing, LLM judges for instruction following.

### Strategic Value Beyond Regression Testing
- Evals force product teams to explicitly specify success definition early.
- Resolve ambiguity between engineers reading same spec.
- Accelerate model adoption: teams with evals determine strengths/weaknesses in days vs. weeks.
- Baselines and regression tests obtained free: latency, token usage, cost per task, error rates.
- **Highest-bandwidth communication channel between product and research teams; defines metrics researchers can optimize.**

---

## How to Evaluate AI Agents

### Types of Graders

#### Code-Based Graders
- **Methods:** string match (exact, regex, fuzzy); binary tests (fail-to-pass, pass-to-pass); static analysis (lint, type, security); outcome verification; tool calls verification; transcript analysis.
- **Strengths:** fast, low cost, objective and reproducible, easy debugging.
- **Weaknesses:** brittle to valid variations not matching expected patterns; lack nuance; limited for subjective tasks.

#### Model-Based Graders
- **Methods:** rubric-based scoring; natural language assertions; pairwise comparison; reference-based evaluation; multi-judge consensus.
- **Strengths:** flexible and scalable; captures nuance; handles open-ended tasks; processes freeform output.
- **Weaknesses:** non-deterministic; more expensive; requires human calibration.

#### Human Graders
- **Methods:** SME review; crowdsourced judgment; spot-check sampling; A/B testing; inter-annotator agreement.
- **Strengths:** gold standard quality; matches expert user judgment; calibrates model-based graders.
- **Weaknesses:** expensive and slow; often requires expert access at scale.

**Scoring Approaches:**
- Weighted: combined grader scores must hit threshold.
- Binary: all graders must pass.
- Hybrid combinations.

### Capability vs. Regression Evals
- **Capability ("quality") evals:** ask "What can this agent do well?"; should start at low pass rate targeting agent struggles; provide hill to climb.
- **Regression evals:** ask "Does agent still handle tasks it used to?"; should maintain ~100% pass rate; declining scores signal broken systems.
- **Graduated evals:** as capability evals achieve high pass rates post-launch, they "graduate" to regression suites run continuously to catch drift.

---

## Evaluating Coding Agents

- Write, test, debug code; navigate codebases; run commands.
- Deterministic graders natural fit since software outcomes straightforward to evaluate.
- Well-specified tasks, stable test environments, thorough generated code tests required.

**Benchmark Examples:**
- **SWE-bench Verified:** assigns GitHub issues from popular Python repos; grades by running test suite. LLM progress: 40% → >80% in one year.
- **Terminal-Bench:** end-to-end technical tasks (build Linux kernel, train ML model).

**Multi-Dimensional Grading Strategy:**
- **Outcome grading:** pass-or-fail unit tests validating key task results.
- **Transcript grading:** heuristics-based code quality rules; model-based rubrics assessing behaviors (tool calls, user interaction).

**Example Coding Eval Task Structure (illustrative):**
- Deterministic tests: required test files that must pass.
- LLM rubric: code quality assessment with rubric file.
- Static analysis: ruff, mypy, bandit checks.
- State check: verify security logs show blocked auth.
- Tool call verification: confirm required tool sequence (`read_file` paths, `edit_file`, `run_tests`).
- Tracked metrics: transcript (turns, tool calls, tokens); latency (TTFT, tokens/sec, time to last token).

**Practical note:** actual coding evals typically rely on unit tests for correctness and LLM rubric for quality; additional graders/metrics added only as needed.

---

## Evaluating Conversational Agents

- Interact in domains: support, sales, coaching.
- Maintain state, use tools, take mid-conversation actions.
- Quality of interaction itself is evaluation component.
- Often require second LLM to simulate user.

**Success Dimensions:**
- State checks (ticket resolved).
- Transcript constraints (completed in <10 turns).
- LLM rubrics (appropriate tone).

**Benchmark Examples:**
- **τ-Bench:** multi-turn interactions across domains (retail support, airline booking); one model plays user persona while agent navigates.
- **τ2-Bench:** successor benchmark with similar multi-turn approach.

**Example Conversational Eval Task Structure:**
- LLM rubric: support quality with assertions (showed empathy, resolution clearly explained, response grounded in tool results).
- State check: verify ticket status = resolved, refund status = processed.
- Tool call verification: required sequence (`verify_identity`, `process_refund` with amount ≤$100, `send_confirmation`).
- Transcript constraint: maximum 10 turns.

---

## Evaluating Research Agents

**Characteristics & Challenges:**
- Gather, synthesize, analyze information; produce answers or reports.
- Binary pass/fail signals unavailable.
- Quality judged relative to task context.
- Experts may disagree on comprehensiveness.
- Ground truth shifts as reference content changes constantly.

**Benchmark Example:**
- **BrowseComp:** tests whether agents find needles in haystacks across open web; questions designed easy to verify but hard to solve.

**Multi-Grader Strategy:**
- **Groundedness checks:** claims supported by retrieved sources.
- **Coverage checks:** key facts a good answer must include.
- **Source quality checks:** consulted sources authoritative, not merely first-retrieved.
- **Objective matching:** for factual questions, exact match works.
- **LLM synthesis evaluation:** flags unsupported claims, coverage gaps; verifies coherence and completeness.

**Calibration:** LLM-based rubrics require frequent calibration against expert human judgment.

---

## Computer Use Agents

- Interact with software through human interfaces: screenshots, mouse clicks, keyboard inputs, scrolling.
- Evaluation requires real or sandboxed environment.

**Benchmark Examples:**
- **WebArena:** browser-based tasks using URL and page state checks; backend state verification for data-modifying tasks (confirm order placed, not just confirmation page appears).
- **OSWorld:** full OS control testing; evaluation scripts inspect file system state, application configs, database contents, UI element properties.

**Token Efficiency vs. Latency Trade-off:**
- **DOM-based interactions:** execute quickly but consume many tokens.
- **Screenshot-based interactions:** slower but more token-efficient.
- Example decision logic: Wikipedia summarization more efficient with DOM text extraction; Amazon laptop case search more efficient with screenshots.

---

## Non-Determinism in Agent Evaluations

### Challenge
- Agent behavior varies between runs.
- Individual tasks have own success rates.
- Task passing in one run might fail in next.

### pass@k (pass at k)
- Likelihood agent achieves at least one correct solution in k attempts.
- As k increases, pass@k rises (more "shots on goal" = higher success odds).
- Example: 50% pass@1 means model succeeds at half of eval tasks on first try.
- Useful when: one successful solution among multiple attempts is valid.

### pass^k (pass all k)
- Probability all k trials succeed.
- As k increases, pass^k falls.
- Example: 75% per-trial success rate → (0.75)³ ≈ 42% probability passing all 3 trials.
- Useful when: customer-facing agents require reliable every-time behavior.

### Selection Guidance
- **pass@k:** tools where one success matters.
- **pass^k:** agents requiring consistency.
- At k=1, both metrics identical; at k=10, pass@k approaches 100% while pass^k approaches 0%.

---

## Going From Zero to One: Roadmap

### Step 0: Start Early
- Do not delay evals waiting for hundreds of tasks.
- 20–50 simple tasks from real failures = great start.
- Early development: small sample sizes sufficient due to large effect sizes of changes.
- More mature agents need larger, more difficult evals.

### Step 1: Start With What You Already Test Manually
- Convert behaviors verified before each release into test cases.
- Consult bug tracker and support queue for production agents.
- Prioritize by user impact.
- Source realistic test data from actual failures.

### Step 2: Write Unambiguous Tasks With Reference Solutions
- **Task quality criterion:** two domain experts independently reach same pass/fail verdict.
- **Passability requirement:** experts must be able to pass task themselves.
- **Specification clarity:** ambiguity in specifications becomes metric noise.
- **Grader clarity:** vague rubrics produce inconsistent LLM judge verdicts.
- **Frontier model reality check:** 0% pass rate across many trials (pass@100) signals broken task, not incapable agent.
- **Verification method:** create reference solution proving task solvable.

### Step 3: Build Balanced Problem Sets
- Test both cases where behavior should occur and where it shouldn't occur.
- Avoid one-sided optimization (search-only evals create over-searching agents).
- Example: Claude.ai web search required balancing undertriggering against overtriggering.

### Step 4: Build Robust Eval Harness With Stable Environment
- Agent in eval must function roughly identically to production agent.
- Each trial requires clean start state (isolated trials).
- Eliminate unnecessary shared state between runs.
- Prevent unfair advantages from shared state (e.g., agent examining git history from previous trials).
- Independent trials essential.

### Step 5: Design Graders Thoughtfully
- Prefer deterministic graders where possible; use LLM graders where necessary; use human graders judiciously.
- **Avoid overly rigid path checking:** grade outputs not paths to avoid punishing creativity.
- **Build in partial credit:** represent success continuum.
- **LLM grader calibration:** carefully iterate; closely calibrate with human experts.
- **Hallucination prevention:** give LLM way out (return "Unknown"); structured rubrics with isolated LLM-as-judge per dimension.
- **Subtle failure mode example:** Opus 4.5 CORE-Bench jumped 42% → 95% after fixing rigid grading, ambiguous specs, stochastic irreproducibility, and loose scaffolding.
- **Bypass-resistant design:** prevent agent "cheating."

### Step 6: Check the Transcripts
- Read transcripts and grades from many trials; invest in transcript viewing tooling.
- Verify graders working well by examining failures.
- Determine whether agent made genuine mistake or graders rejected valid solution.
- **Critical skill:** reading transcripts validates eval measures what matters.

### Step 7: Monitor for Capability Eval Saturation
- **Saturation:** agent passes all solvable tasks leaving no improvement room.
- **Deceptive metrics example:** Qodo initially unimpressed by Opus 4.5 because one-shot coding evals missed gains on longer complex tasks; developed agentic eval framework revealing clearer picture.
- **Validation:** do not take eval scores at face value without transcript investigation.

### Step 8: Keep Evaluation Suites Healthy Long-Term
- Eval suite as living artifact requiring ongoing attention and clear ownership.
- **Anthropic's approach:** dedicated evals teams own core infrastructure; domain experts and product teams contribute tasks.
- **Eval-driven development:** build evals defining planned capabilities before agents fulfill them.
- **User-centric contribution:** PMs, customer success, salespeople using Claude Code can contribute eval tasks as PRs.

---

## How Evals Fit With Other Methods

| Method | Pros | Cons |
|--------|------|------|
| **Automated evals** | Faster iteration; reproducible; no user impact; runs on every commit; tests at scale | Upfront investment; ongoing maintenance; false confidence if mismatched to real usage |
| **Production monitoring** | Reveals real user behavior; catches synthetic eval misses; provides ground truth | Reactive; noisy signals; requires instrumentation; lacks grading ground truth |
| **A/B testing** | Measures actual outcomes (retention, completion); controls confounds; scalable | Slow (days/weeks); only tests deployed changes; less "why" without transcript review |
| **User feedback** | Surfaces unanticipated problems; comes with real examples; correlates with goals | Sparse; skews toward severe issues; users rarely explain "why"; not automated |
| **Manual transcript review** | Builds intuition; catches subtle quality issues; calibrates "good" understanding | Time-intensive; doesn't scale; reviewer fatigue affects signal |
| **Systematic human studies** | Gold-standard judgments; handles subjective tasks; signals for improving model graders | Expensive and slow; hard to run frequently; complex domains require human experts |

### Lifecycle Application
- **Pre-launch and CI/CD:** automated evals as first-line defense.
- **Post-launch:** production monitoring detecting distribution drift.
- **Scale milestone:** A/B testing validating significant changes once sufficient traffic exists.
- **Continuous practices:** triage user feedback constantly; sample transcripts weekly.
- **Calibration:** systematic human studies for calibrating LLM graders.

### Multi-Layer Defense Model
- **Swiss Cheese Model from safety engineering:** single evaluation layer cannot catch every issue.
- Multiple combined methods: failures slipping through one layer caught by another.

---

## Conclusion

**Fundamental Principles:**
- Start early; do not wait for perfect suite.
- Source realistic tasks from observed failures.
- Define unambiguous, robust success criteria.
- Design graders thoughtfully combining multiple types.
- Ensure problems hard enough for model.
- Iterate improving signal-to-noise ratio.
- **Read the transcripts.**

---

## Appendix: Eval Frameworks

- **Harbor:** designed for containerized environment agents; standardized task and grader format; popular benchmarks like Terminal-Bench 2.0 ship through Harbor registry.
- **Braintrust:** combines offline evaluation with production observability and experiment tracking; includes `autoevals` library with pre-built scorers.
- **LangSmith:** tracing, offline/online evaluations, dataset management; tight LangChain ecosystem integration.
- **Langfuse:** self-hosted open-source alternative to LangSmith.
- **Arize:** offers Phoenix (open-source LLM tracing) and AX (SaaS extending Phoenix for scale).
- **Arize Phoenix:** open-source platform for LLM tracing and debugging.

**Selection Guidance:**
- Many teams combine multiple tools or roll custom.
- Frameworks valuable for accelerating progress and standardizing.
- **Framework quality limited to eval tasks run through it.**
- Recommended: quickly pick framework fitting workflow, then invest energy in eval tasks themselves.
