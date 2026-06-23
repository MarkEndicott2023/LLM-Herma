# Effective Harnesses for Long-Running Agents

**Source:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**Author:** Justin Young (with contributions from David Hershey, Prithvi Rajasekaran, Jeremy Hadfield)
**Published:** Nov 26, 2025
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text. Use this as a navigation/curation aid; refer to the source URL for full prose.

---

## The Long-Running Agent Problem

- Core challenge: agents must work in discrete sessions with no memory of previous context.
- Metaphor: like engineers working in shifts with no knowledge of prior work.
- Context window limitations prevent complex projects from completing in a single session.
- Even frontier models like Opus 4.5 fail to build production-quality apps with only high-level prompts.
- **First failure pattern:** agent attempts "one-shotting" entire app, runs out of context mid-implementation, leaving half-finished undocumented features.
- **Second failure pattern:** agent declares project complete after partial progress, missing remaining features.
- Compaction alone is insufficient to bridge context gaps.
- Solution requires two-part decomposition: environment setup plus incremental progress guidance.

---

## Solution Overview: Two-Agent Architecture

**Initializer Agent (First Session)**
- Specialized prompt for environment setup.
- Creates `init.sh` script for running development server.
- Creates `claude-progress.txt` file to log agent work.
- Makes initial git commit showing added files.
- Provides foundation for all required features.

**Coding Agent (Subsequent Sessions)**
- Tasked with incremental progress per session.
- Leaves structured updates and clean state.
- Works feature-by-feature rather than all-at-once.
- Code appropriate for merging to main branch (no major bugs, orderly, well-documented).

---

## Environment Management

### Feature List
- Addresses the "one-shotting" and premature completion problems.
- Initializer creates a comprehensive JSON file expanding the user's initial prompt.
- Example: a claude.ai clone required 200+ features like "user can open new chat, type query, press enter, see AI response."
- All features initially marked as "failing."
- Structure includes category, description, steps, and `passes` field.
- JSON format preferred because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown."
- Strict instruction: "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
- Coding agents restricted to only changing the `passes` field status.

### Incremental Progress
- Work on one feature at a time (critical to prevent doing too much at once).
- Model must leave environment in a clean state after code changes.
- Use git with descriptive commit messages to document changes.
- Write progress file summaries after each session.
- Git enables reverting bad changes and recovering working states.
- Eliminates need for agents to guess what happened and waste time fixing a broken app.
- Increases efficiency and preserves continuity.

### Testing
- **Failure mode:** Claude marks features complete without proper testing.
- Claude tended to do unit tests or curl commands but miss end-to-end verification.
- **Solution:** explicitly prompt to use browser automation tools (Puppeteer MCP).
- Test as human users would, not just programmatically.
- Dramatically improved performance by identifying bugs invisible in code alone.
- **Known limitation:** Claude vision and Puppeteer can't detect browser-native alert modals, making those features buggier.

---

## Getting Up to Speed (Session Startup Procedure)

**Recommended startup steps for each coding agent:**
1. Run `pwd` to confirm working directory (can only edit files in this directory).
2. Read git logs and progress files to understand recent work.
3. Read features list and choose highest-priority incomplete feature.

**Development server setup:**
- Initializer writes `init.sh` script to run development server.
- Coding agent runs `init.sh` at session start.
- Run a basic end-to-end test before implementing new feature (e.g., start local server, create new chat, send message, receive response).
- Saves tokens by not requiring agent to figure out testing each session.
- Allows agent to identify if app left in broken state and fix immediately.
- Prevents compounding problems by starting new features on a broken foundation.

**Typical session flow:**
- Get bearings and check current project state.
- Read `claude-progress.txt`.
- Review `feature_list.json`.
- Check git log for recent work.
- Start development server via `init.sh`.
- Verify fundamental features still working.
- Choose next feature from list.
- Work on single feature.
- Test thoroughly before marking complete.
- Commit with descriptive message.
- Update progress file.

---

## Agent Failure Modes and Solutions Table

| Problem | Initializer Agent Solution | Coding Agent Solution |
|---------|---------------------------|----------------------|
| Claude declares project complete too early | Create structured JSON feature list with end-to-end descriptions | Read feature list at session start; work on one feature at a time |
| Environment left with bugs/undocumented progress | Initialize git repo and progress notes file | Start session reading progress notes and git logs; run basic development server test; end with git commit and progress update |
| Features marked done prematurely | Create feature list | Self-verify all features through testing; only mark passing after careful testing |
| Agent unsure how to run app | Write `init.sh` script for development server | Start session by reading `init.sh` |

---

## Future Work
- Unclear whether single general-purpose coding agent or multi-agent architecture performs better.
- Potential specialized agents: testing agent, quality assurance agent, code cleanup agent for software development lifecycle sub-tasks.
- Current demo optimized for full-stack web app development.
- Need to generalize findings to other fields: scientific research, financial modeling.
- Open question: how to scale these patterns beyond coding tasks.
