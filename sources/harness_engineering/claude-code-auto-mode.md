# Claude Code Auto Mode: A Safer Way to Skip Permissions

**Source:** https://www.anthropic.com/engineering/claude-code-auto-mode
**Author:** John Hughes
**Published:** Mar 25, 2026
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text.

---

## Overview
Anthropic introduced "auto mode" for Claude Code, a feature that automates permission approvals using AI classifiers rather than requiring manual user review for every action. The system aims to reduce "approval fatigue" while maintaining safety — sitting between the extremes of full sandboxing and completely disabling permission checks.

## Key Problem
Claude Code users approve approximately **93% of permission prompts**. This high approval rate creates fatigue, leading users to either: (1) use sandboxing (safe but maintenance-heavy), or (2) disable all permission checks via `--dangerously-skip-permissions` (convenient but unsafe).

## How It Works

Auto mode employs two defensive layers:

**Input Layer:** A server-side prompt-injection probe scans tool outputs before they reach the agent, adding warnings when injection attempts are detected.

**Output Layer:** A transcript classifier evaluates each action against decision criteria before execution, operating in two stages — a fast single-token filter followed by chain-of-thought reasoning only when flagged.

The classifier deliberately avoids reading the agent's own explanations and tool outputs, instead evaluating only user messages and bare tool commands. This prevents the agent from "talking" the classifier into unsafe decisions.

## Threat Model

The system addresses four categories of dangerous agent behavior:
- **Overeager actions** (helpful but unauthorized initiative)
- **Honest mistakes** (misunderstanding resource scope)
- **Prompt injection** (malicious instructions planted in tool outputs)
- **Model misalignment** (agent pursuing its own goals)

## Real-World Examples Blocked
- Deleting remote branches from vague instructions.
- Systematically searching for API tokens after auth failures.
- Deleting unconfirmed job targets based on name similarity.
- Exfiltrating scripts to public services.
- Bypassing safety checks on deployments.

## Permission Decision Tiers

- **Tier 1:** Built-in allowlist (file reads, searches, navigation).
- **Tier 2:** In-project file operations (reviewable via version control).
- **Tier 3:** Transcript classifier (shell commands, external integrations, filesystem operations outside the project).

## Performance Results

Testing across three datasets:

| Dataset | Stage 1 FPR | Full Pipeline FPR | Full Pipeline FNR |
|---|---|---|---|
| Real traffic (10K actions) | 8.5% | 0.4% | — |
| Real overeager (52 actions) | 6.6% | — | 17% |
| Synthetic exfiltration (1K) | 1.8% | — | 5.7% |

The 17% false-negative rate on overeager actions represents situations where the classifier identifies danger correctly but misjudges whether user consent covers the specific action's scope.

## Design Rationale

- **Why strip assistant messages and tool results:** prevents the agent from influencing classifier decisions through persuasive explanations. Tool results are stripped primarily for prompt-injection defense.
- **Two-stage classification:** Stage 1 acts as a fast filter prioritizing recall (blocking conservative); Stage 2 applies careful reasoning only on flagged items, reducing false positives from 8.5% to 0.4%.
- **Prompt-injection probe:** provides a second defensive layer at the input level, requiring injections to bypass both the input probe and the output classifier to succeed.
- **Multi-agent handoffs:** classifiers run at delegation points (preventing unauthorized task assignment) and return points (catching mid-run compromises).
- **Deny-and-continue logic:** rather than halting on blocked actions, the system returns the denial as a tool result, allowing the agent to attempt safer alternatives. Sessions terminate after 3 consecutive or 20 total denials.

## Important Limitations

Auto mode is not a replacement for human review on high-stakes infrastructure. The 17% false-negative rate on real overeager actions reflects genuine safety trade-offs — it substantially improves on completely disabling permissions but falls short of careful manual oversight.

The classifier struggles particularly with consent boundaries: it can identify dangerous actions but sometimes misjudges whether prior user statements authorize the specific blast radius involved.

## Configuration

The classifier uses a fixed template with three customizable slots:
- **Environment:** defines trust boundaries (domains, cloud buckets, source-control organizations).
- **Block rules:** over 20 default rules covering destruction, security degradation, trust boundary violations, and review bypassing.
- **Allow exceptions:** carve-outs for benign cases like installing declared packages or pushing to working branches.

Users can run `claude auto-mode defaults` to see the full baseline and customize iteratively.
