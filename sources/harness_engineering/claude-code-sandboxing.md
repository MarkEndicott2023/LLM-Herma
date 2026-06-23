# Beyond Permission Prompts: Making Claude Code More Secure and Autonomous

**Source:** https://www.anthropic.com/engineering/claude-code-sandboxing
**Authors:** David Dworken and Oliver Weller-Davies (with contributions from Meaghan Choi, Catherine Wu, Molly Vorwerck, Alex Isken, Kier Bradwell, Kevin Garcia)
**Published:** Oct 20, 2025
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text.

---

## Section 1: Introduction
- Claude Code writes, tests, debugs code, and navigates codebases with multiple file access.
- Extended codebase access introduces security risks, particularly prompt injection threats.
- Two new sandboxing features aim to reduce permission prompts while enhancing security.
- Internal usage shows sandboxing reduces permission prompts by **84%**.
- Defining work boundaries increases both security and agent autonomy.

---

## Section 2: Keeping Users Secure on Claude Code

### Permission-Based Model
- Claude Code operates in read-only mode by default, requiring permission before modifications.
- Safe commands (`echo`, `cat`) receive auto-approval; most operations require explicit approval.
- Frequent approval requests create "approval fatigue," reducing user attention to security.
- Fatigue undermines development safety through inattentive approvals.

---

## Section 3: Sandboxing — A Safer and More Autonomous Approach

### Core Sandboxing Strategy
- Pre-defined boundaries enable Claude to work more freely without per-action permission requests.
- Drastically fewer permission prompts combined with increased safety.
- Built on operating system-level features.

### Two Isolation Boundaries

**Filesystem Isolation**
- Restricts Claude to access/modify only specific directories.
- Prevents prompt-injected Claude from modifying sensitive system files.

**Network Isolation**
- Ensures Claude can only connect to approved servers.
- Prevents exfiltration of sensitive information.
- Prevents malware downloads.

### Both Are Necessary
- Effective sandboxing requires **both** filesystem AND network isolation.
- Without network isolation: compromised agents could exfiltrate files (SSH keys).
- Without filesystem isolation: compromised agents could escape sandbox and access network.
- Combined approach provides safer, faster agentic experience.

---

## Section 4: Two New Sandboxing Features in Claude Code

### Feature 1: Sandboxed Bash Tool

**Technical Implementation**
- New sandbox runtime available in beta as research preview.
- Allows defining exactly which directories and network hosts agents can access.
- Eliminates overhead of spinning up/managing containers.
- Can sandbox arbitrary processes, agents, and MCP servers.
- Available as open source research preview on GitHub.

**Execution Model**
- Claude runs commands within defined limits inside safe sandbox.
- Claude executes commands autonomously without permission prompts.
- User notified immediately if Claude attempts out-of-sandbox access.
- User can choose whether to allow out-of-bounds attempts.

**OS-Level Enforcement**
- Built on Linux **bubblewrap** and macOS **seatbelt**.
- Enforces restrictions at OS level.
- Covers Claude Code direct interactions AND spawned scripts/programs/subprocesses.

**Filesystem Isolation Configuration**
- Allows read and write access to current working directory.
- Blocks modification of files outside the working directory.
- Configurable for specific file paths.

**Network Isolation Configuration**
- Internet access only through unix domain socket connected to proxy server.
- Proxy server runs outside sandbox.
- Proxy enforces restrictions on domain connections.
- Proxy handles user confirmation for newly requested domains.
- Supports customizable proxy rules for arbitrary outbound traffic restrictions.

**Getting Started**
- Run `/sandbox` command in Claude Code.
- Open-sourced feature available for other teams building safer agents.

---

### Feature 2: Claude Code on the Web

**Overview**
- Enables running Claude Code in isolated sandbox in cloud.
- Each Claude Code session executes in isolated sandbox.
- Full server access in safe, secure manner.

**Credential Security Model**
- Sensitive credentials never inside sandbox with Claude Code.
- Git credentials and signing keys kept external.
- Even if code in sandbox is compromised, user remains protected.

**Git Proxy Architecture**
- Custom proxy service transparently handles all git interactions.
- Git client inside sandbox authenticates to proxy with custom-built scoped credential.
- Proxy verifies credential and git interaction contents.
- Proxy ensures pushes only occur to configured branch.
- Proxy attaches correct authentication token before GitHub request.

**Security Benefits**
- Prevents unauthorized repository pushes.
- Validates branch destinations.
- Isolates authentication tokens from sandbox environment.

---

## Section 5: Getting Started

1. Run `/sandbox` in Claude and review configuration documentation.
2. Visit claude.com/code to try Claude Code on the web.
3. For custom agent builders: integrate open-sourced sandboxing code from GitHub.
