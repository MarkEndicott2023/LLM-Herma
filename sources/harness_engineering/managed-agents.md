# Scaling Managed Agents: Decoupling the Brain from the Hands

**Source:** https://www.anthropic.com/engineering/managed-agents
**Authors:** Lance Martin, Gabe Cemaj, Michael Cohen
**Published:** Apr 8, 2026
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text.

---

## Introduction
- Harnesses encode assumptions that become outdated as models advance.
- Managed Agents is a hosted service for long-horizon agent work built on stable interfaces.
- "Harnesses encode assumptions about what Claude can't do on its own."
- Example: Claude Sonnet 4.5 exhibited "context anxiety" by wrapping tasks prematurely near context limits; Claude Opus 4.5 no longer exhibited this behavior, making context resets "dead weight."
- Managed Agents designed with interfaces meant to outlast specific implementations.

## Design Philosophy: Operating System Analogy
- Draws parallel to how operating systems virtualized hardware into abstractions (process, file) that outlasted implementations.
- The `read()` command remains agnostic to whether accessing 1970s disk packs or modern SSDs.
- Three virtualized agent components:
  - **Session** (append-only log of all events)
  - **Harness** (loop calling Claude, routing tool calls)
  - **Sandbox** (execution environment for code and file editing)
- Implementation details can be swapped without disrupting other components.
- Opinionated about interface shapes, not implementation details.

## Don't Adopt a Pet (Problem with Coupled Design)
- All agent components placed in single container (session, harness, sandbox shared one environment).
- Benefits included direct syscalls for file edits and no service boundaries to design.
- Adopting "pets" paradigm: named, hand-tended individuals (containers) that couldn't fail without losing sessions.
- Unresponsive stuck sessions required manual debugging through WebSocket event streams.
- Unable to distinguish harness bugs from packet drops or container failures.
- Debugging required shell access inside containers holding user data, creating security/privacy concerns.
- Harness assumed resources lived within same container, requiring network peering for customer VPC connectivity.

## Decouple the Brain from the Hands

### The Harness Leaves the Container
- Harness no longer lives inside container; calls container via `execute(name, input) → string`.
- Container becomes "cattle" (interchangeable); container death treated as tool-call error.
- New containers provisioned via `provision({resources})` with standard recipes.
- No manual recovery of failed containers required.

### Recovering from Harness Failure
- Session log sits outside harness; nothing in harness must survive crashes.
- Harness also becomes "cattle."
- Recovery via `wake(sessionId)`.
- Retrieve event log with `getSession(id)` to resume from last event.
- Harness writes durable records via `emitEvent(id, event)` during agent loop.

### The Security Boundary
- Coupled design vulnerability: untrusted generated code ran in same container as credentials.
- Prompt injection could expose tokens, enabling attackers to spawn unrestricted sessions.
- **Structural fix:** ensure tokens never reachable from sandbox where Claude's code executes.

**Two credential patterns:**
- **Bundle auth with resource:** Git example — use repository access token to clone during sandbox init, wire into local git remote; push/pull work without agent handling token.
- **External vault:** custom tools support MCP with OAuth tokens stored in secure vault; Claude calls MCP tools via dedicated proxy taking session-associated token; proxy fetches credentials from vault.
- Harness never made aware of credentials.

## The Session Is Not Claude's Context Window

**Long-Horizon Task Challenges:**
- Tasks often exceed Claude's context window length.
- Standard solutions involve irreversible decisions about retained content.
- Prior techniques explored: compaction (save context summaries), memory tools (write to files for cross-session learning), context trimming (selectively remove tokens).

**Risks of Irreversible Context Decisions:**
- Difficult predicting which tokens future turns will need.
- Compaction-transformed messages, when removed from context, only recoverable if stored separately.
- Prior work explored storing context as objects outside context window (accessible via code in REPL for filtering/slicing).

**Managed Agents Solution:**
- Session serves as context object living outside Claude's context window.
- Rather than sandbox/REPL storage, context durably stored in session log.
- Interface `getEvents()` allows brain to interrogate context via positional slices of event stream.
- Flexible usage: pick up from last read position, rewind before specific moment, reread before actions.
- Fetched events can be transformed in harness before passing to Claude (context organization for prompt cache hit rate, context engineering).
- Separated recoverable storage (session) from arbitrary management (harness) because future context engineering requirements unpredictable.

## Many Brains, Many Hands

**Many Brains**
- Decoupling solved early customer complaint about resources in private VPCs.
- Previously required network peering; once harness left container, assumption disappeared.
- **Performance improvement:** eliminated dead time of container provisioning.
- Many brains no longer required many containers; inference starts once orchestration layer pulls events from session log without waiting for container.
- Time-to-first-token (TTFT) metrics: "our p50 TTFT dropped roughly 60% and p95 dropped over 90%."
- TTFT is "the latency the user most acutely feels."
- Scaling to many brains means starting many stateless harnesses, connecting to hands only if needed.

**Many Hands**
- Connect each brain to multiple execution environments.
- Claude reasons about many environments and decides work routing (harder cognitive task than single shell).
- Earlier models incapable; single container became limitation as intelligence scaled.
- Each hand becomes tool interface: `execute(name, input) → string`.
- Interface agnostic about sandbox type (container, phone, emulator).
- No hand coupled to brain; brains can pass hands to one another.

## Conclusion

**Meta-Harness Design Philosophy**
- Addresses old computing challenge: designing for "programs as yet unthought of."
- Operating systems lasted decades by virtualizing hardware into general abstractions.
- Managed Agents uninformed about specific future harness needs.
- System with general interfaces accommodating many different harnesses.
- Accommodates examples like Claude Code and task-specific agent harnesses.

**Design Assumptions:**
- Opinionated about interfaces around Claude.
- Expects Claude will need: state manipulation (session), computation (sandbox).
- Expects Claude will require scaling to many brains and many hands.
- Interfaces designed for reliable, secure long-horizon operation.
- No assumptions about number or location of brains/hands needed.
