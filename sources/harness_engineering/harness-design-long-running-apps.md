# Harness Design for Long-Running Application Development

**Source:** https://www.anthropic.com/engineering/harness-design-long-running-apps
**Author:** Prithvi Rajasekaran (Anthropic Labs)
**Published:** Mar 24, 2026
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text. Use this as a navigation/curation aid; refer to the source URL for full prose.

---

## Why Naive Implementations Fall Short

**Context Window and Coherence Problems:**
- Models lose coherence on lengthy tasks as the context window fills.
- "Context anxiety" causes models to wrap up work prematurely near perceived limits.
- Context resets (clearing the window entirely with structured handoffs) solve both issues better than compaction.
- Compaction preserves continuity but doesn't provide a clean slate, leaving context anxiety unresolved.
- Claude Sonnet 4.5 exhibited context anxiety strongly enough that compaction alone was insufficient.
- Context resets add orchestration complexity, token overhead, and latency to harness runs.

**Self-Evaluation Problems:**
- Agents confidently praise their own work even when quality is mediocre.
- Problem is especially pronounced for subjective tasks like design lacking binary verification.
- Separating the agent doing work from the agent judging it provides strong leverage.
- External feedback allows generator to iterate against concrete criteria.
- Tuning a standalone evaluator to be skeptical is more tractable than making a generator self-critical.

---

## Frontend Design: Making Subjective Quality Gradable

**Design Principles and Approach:**
- Aesthetics can be improved with grading criteria encoding design principles and preferences.
- Separating frontend generation from grading creates a feedback loop driving better outputs.
- Implementation used Claude Agent SDK for straightforward orchestration.
- Generator agent created HTML/CSS/JS frontend from user prompt.
- Evaluator agent used Playwright MCP to interact with live page before scoring.

**Four Grading Criteria (weighted toward design and originality):**
1. **Design Quality:** Does design feel coherent rather than a collection of parts? Colors, typography, layout, imagery combine to create distinct mood and identity.
2. **Originality:** Evidence of custom decisions vs. template/library defaults? Human designers should recognize deliberate creative choices; unmodified stock components fail.
3. **Craft:** Technical execution including typography hierarchy, spacing consistency, color harmony, contrast ratios; competence check rather than creativity check.
4. **Functionality:** Usability independent of aesthetics; users understand interface, find primary actions, complete tasks without guessing.

**Calibration and Execution:**
- Evaluator calibrated using few-shot examples with detailed score breakdowns to align with preferences.
- Evaluator actively navigated pages, taking screenshots before scoring — not grading static images.
- Generator instructed to make strategic decisions after each evaluation: refine current direction if trending well, or pivot to a different aesthetic if approach not working.
- Ran 5–15 iterations per generation; full runs stretched up to four hours.
- Prompting criteria wording steered the generator in unanticipated ways (e.g., "museum quality" language pushed toward particular visual convergence).

**Results and Observations:**
- Evaluator assessments improved over iterations before plateauing with remaining headroom.
- Pattern was not cleanly linear; preferred middle iterations sometimes over final ones.
- Implementation complexity increased across rounds as generator reached for more ambitious solutions.
- Even first iteration was notably better than baseline with no prompting — suggesting criteria language itself steered away from generic defaults.
- Example: Dutch art museum website evolved from clean dark-themed landing page to a 3D spatial experience with checkered floor rendered in CSS perspective by iteration 10.

---

## Scaling to Full-Stack Coding

### The Architecture

**Three-Agent System Overview:**
- Addressed gaps observed in prior single-agent runs.
- Eliminated context resets entirely (different from frontend work) because Opus 4.5 largely removed "context anxiety" behavior.
- Used continuous session across whole build with Claude Agent SDK automatic compaction handling context growth.

**Planner Agent:**
- Took simple 1–4 sentence prompt and expanded to full product spec.
- Prompted to be ambitious about scope while staying on product context and high-level technical design.
- Avoided detailed technical implementation specs to prevent cascading errors downstream.
- Asked to find opportunities weaving AI features into product specs.
- Focused on deliverables rather than granular technical paths.

**Generator Agent:**
- Applied one-feature-at-a-time model from earlier harness for scope management.
- Worked in sprints, picking one feature from spec at a time.
- Tech stack: React, Vite, FastAPI, SQLite (later PostgreSQL).
- Self-evaluated work at end of each sprint before handing off to QA.
- Used git for version control.
- Sprint-by-sprint iteration with clear feature boundaries.

**Evaluator Agent:**
- Used Playwright MCP to click through running application like a user would.
- Tested UI features, API endpoints, database states.
- Graded each sprint against bugs found plus criteria adapted from frontend work (product depth, functionality, visual design, code quality).
- Each criterion had hard threshold; failure on any meant sprint failed and generator got detailed feedback.
- **Sprint contract pattern:** before code was written, evaluator and generator agreed on "done" criteria and success verification. Generator proposed what it would build and how success would be verified; evaluator reviewed to ensure generator was building the right thing. Both iterated until agreement reached.

**Communication Method:**
- Handled via files: one agent wrote a file, another read and responded in same file or new file.
- Kept work faithful to spec without over-specifying implementation too early.

### Running the Harness (Version 1)

**Model and Setup:**
- Used Claude Opus 4.5 (best coding model at time).
- Tested against single-agent system for comparison.

**Example Prompt:**
> "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

**Cost/Performance Comparison:**
- Solo harness: 20 min, $9
- Full harness: 6 hr, $200
- Full harness over 20× more expensive but dramatically better quality.

**Solo Harness Issues:**
- Layout wasted space with fixed-height panels leaving viewport empty.
- Workflow rigid and not intuitive about sprite/entity creation sequence.
- Game broken: entities appeared but nothing responded to input.
- Entity-to-runtime wiring broken with no UI indication of problem.

**Full Harness Output Advantages:**
- Interface showed more polish and smoothness; canvas used full viewport with sensibly-sized panels.
- Consistent visual identity tracking design direction from spec.
- Planner created 16-feature spec across ten sprints including: sprite animation system, behavior templates, sound/music, AI-assisted sprite/level generation, shareable game export.
- Planner had access to a frontend design skill and used it to create visual design language in spec.
- Built-in Claude integration let user generate game parts through prompting.
- Sprite editor richer and more featured with cleaner palettes, better color picker, usable zoom.
- Play mode actually functional: users could move entity and play the game (though physics had rough edges).
- Some workflow intuitiveness gaps remained — gaps in base model's product intuition rather than harness design.

**QA Effectiveness:**
- Evaluator kept implementation aligned with spec.
- Each sprint, evaluator walked through contract's test criteria and exercised application via Playwright.
- Contracts granular (Sprint 3 had 27 criteria for level editor alone).
- Findings specific enough to act on without investigation.
- Examples of identified issues: fill tool filling only at drag endpoints not region; delete key handler missing condition branches; FastAPI route ordering preventing reorder endpoint from being reached.

**Tuning Required:**
- Out-of-the-box Claude is a poor QA agent.
- Early runs: evaluator identified legitimate issues, then talked itself into approving anyway.
- Tested superficially rather than probing edge cases, allowing subtle bugs to slip through.
- Multiple iterative tuning rounds matching evaluator logs against personal preferences.
- Even after tuning: small layout issues, unintuitive interactions, undiscovered bugs in deeply-nested features remained.
- Compared to solo run where central feature didn't work, lift was obvious.

### Iterating on the Harness (Version 2)

**Simplification Philosophy:**
- Every harness component encodes an assumption about model incapability.
- Assumptions worth stress-testing: they may be incorrect or quickly go stale.
- Principle: "find the simplest solution possible, and only increase complexity when needed."

**Initial Simplification Attempts:**
- First attempt cut harness radically and tried creative ideas but couldn't replicate performance.
- Difficult to identify which pieces were load-bearing and in what ways.
- Moved to methodical approach: removing one component at a time, reviewing impact.

**Claude Opus 4.6 Release as Catalyst:**
- Provided motivation to reduce complexity.
- Good reason to expect 4.6 would need less scaffolding than 4.5.
- 4.6 features: plans more carefully, sustains agentic tasks longer, operates reliably in larger codebases, better code review/debugging, improved long-context retrieval.

**Removing Sprint Construct:**
- Removed sprint structure entirely; model could handle decomposition without it.
- Kept planner and evaluator as both continued adding obvious value.
- Without planner: generator under-scoped, starting building without speccing work first.
- Moved evaluator to single-pass end-of-run grading rather than per-sprint.
- Load-bearing nature of evaluator became task-dependent on where task sat relative to model capabilities.
- On 4.5: boundary close to model capability edge; evaluator caught meaningful issues.
- On 4.6: model raw capability increased, boundary moved outward; evaluator became unnecessary overhead for tasks inside boundary but continued adding value at capability frontier.
- **Practical implication:** evaluator is cost-effective when task sits beyond what current model reliably does solo.

**Prompting Improvements:**
- Added prompting to improve how harness built AI features into apps.
- Got generator to build proper agent driving app functionality through tools.
- Knowledge recent enough that Claude's training covers thinly.
- Took real iteration but with tuning the generator built agents correctly.

### Results from Updated Harness (Version 2)

**Example Prompt:**
> "Build a fully featured DAW in the browser using the Web Audio API."

**Duration and Cost:**
- Run length: ~4 hours, $124 total token costs.
- Most time spent in builder which ran coherently for 2+ hours without sprint decomposition.

**Breakdown by Agent/Phase:**
- Planner: 4.7 min, $0.46
- Build (Round 1): 2 hr 7 min, $71.08
- QA (Round 1): 8.8 min, $3.24
- Build (Round 2): 1 hr 2 min, $36.89
- QA (Round 2): 6.8 min, $3.09
- Build (Round 3): 10.9 min, $5.88
- QA (Round 3): 9.6 min, $4.06

**QA Feedback Round 1:** "strong app with excellent design fidelity, solid AI agent, and good backend" but main failure in feature completeness: clips couldn't be dragged/moved on timeline, no instrument UI panels (synth knobs, drum pads), no visual effect editors (EQ curves, compressor meters).

**QA Feedback Round 2:**
- Audio recording was stub-only (button toggled but no mic capture).
- Clip resize by edge drag and clip split not implemented.
- Effect visualizations were numeric sliders not graphical (no EQ curve).

**Generator Performance:**
- Still liable to miss details or stub features when left to own devices.
- QA added value catching last-mile issues for generator to fix.

**Final App Characteristics:**
- Far from professional music production program.
- Agent's song composition skills needed work.
- Claude's inability to hear limited QA feedback effectiveness on musical taste.
- Had core pieces of functional program: working arrangement view, mixer, transport running in browser.
- Able to create song snippet entirely through prompting: agent set tempo/key, laid melody, built drum track, adjusted mixer, added reverb.

---

## What Comes Next

**Model Improvement Trajectory:**
- Models continuing to improve; capability for longer work and complex tasks increasing.
- Sometimes better models solve problems without additional scaffolding; can wait for next model.
- Conversely, as models improve, more space exists to develop harnesses achieving complex tasks beyond baseline.

**Key Lessons Forward:**
- Always good to experiment with the model you're building against, read traces on realistic problems, tune performance.
- On complex tasks, sometimes headroom exists from decomposing and applying specialized agents to each aspect.
- When new model releases, re-examine harness, stripping non-load-bearing pieces and adding pieces enabling greater capability.

**Future Direction:**
- Space of interesting harness combinations doesn't shrink as models improve; it moves.
- Interesting work for AI engineers is finding the next novel combination.
