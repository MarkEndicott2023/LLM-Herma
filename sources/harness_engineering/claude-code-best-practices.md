# Best Practices for Claude Code

**Source:** https://www.anthropic.com/engineering/claude-code-best-practices (redirects to https://code.claude.com/docs/en/best-practices)
**Fetched:** 2026-05-05
**Note:** This article was migrated to the Claude Code docs site. The fetched content is unusually complete — closer to verbatim than the other articles in this directory.

---

> Tips and patterns for getting the most out of Claude Code, from configuring your environment to scaling across parallel sessions.

Claude Code is an agentic coding environment. Unlike a chatbot that answers questions and waits, Claude Code can read your files, run commands, make changes, and autonomously work through problems while you watch, redirect, or step away entirely.

This changes how you work. Instead of writing code yourself and asking Claude to review it, you describe what you want and Claude figures out how to build it. Claude explores, plans, and implements.

But this autonomy still comes with a learning curve. Claude works within certain constraints you need to understand.

This guide covers patterns that have proven effective across Anthropic's internal teams and for engineers using Claude Code across various codebases, languages, and environments.

---

Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills.

Claude's context window holds your entire conversation, including every message, every file Claude reads, and every command output. However, this can fill up fast. A single debugging session or codebase exploration might generate and consume tens of thousands of tokens.

This matters since LLM performance degrades as context fills. When the context window is getting full, Claude may start "forgetting" earlier instructions or making more mistakes. The context window is the most important resource to manage.

---

## Give Claude a way to verify its work

> Include tests, screenshots, or expected outputs so Claude can check itself. This is the single highest-leverage thing you can do.

Claude performs dramatically better when it can verify its own work, like run tests, compare screenshots, and validate outputs. Without clear success criteria, it might produce something that looks right but actually doesn't work.

| Strategy | Before | After |
|---|---|---|
| **Provide verification criteria** | *"implement a function that validates email addresses"* | *"write a `validateEmail` function. example test cases: `user@example.com` is true, `invalid` is false, `user@.com` is false. run the tests after implementing"* |
| **Verify UI changes visually** | *"make the dashboard look better"* | *"[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them"* |
| **Address root causes, not symptoms** | *"the build is failing"* | *"the build fails with this error: [paste error]. fix it and verify the build succeeds. address the root cause, don't suppress the error"* |

UI changes can be verified using the Claude in Chrome extension. Your verification can also be a test suite, a linter, or a Bash command that checks output. Invest in making your verification rock-solid.

---

## Explore first, then plan, then code

> Separate research and planning from implementation to avoid solving the wrong problem.

Letting Claude jump straight to coding can produce code that solves the wrong problem. Use plan mode to separate exploration from execution.

The recommended workflow has four phases:

1. **Explore** — Enter plan mode. Claude reads files and answers questions without making changes.
   ```
   read /src/auth and understand how we handle sessions and login.
   also look at how we manage environment variables for secrets.
   ```
2. **Plan** — Ask Claude to create a detailed implementation plan.
   ```
   I want to add Google OAuth. What files need to change?
   What's the session flow? Create a plan.
   ```
   Press `Ctrl+G` to open the plan in your text editor for direct editing before Claude proceeds.
3. **Implement** — Switch out of plan mode and let Claude code, verifying against its plan.
   ```
   implement the OAuth flow from your plan. write tests for the
   callback handler, run the test suite and fix any failures.
   ```
4. **Commit** — Ask Claude to commit with a descriptive message and create a PR.

> Plan mode is useful, but also adds overhead. For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly. Planning is most useful when you're uncertain about the approach, when the change modifies multiple files, or when you're unfamiliar with the code being modified. **If you could describe the diff in one sentence, skip the plan.**

---

## Provide specific context in your prompts

> The more precise your instructions, the fewer corrections you'll need.

| Strategy | Before | After |
|---|---|---|
| **Scope the task** | *"add tests for foo.py"* | *"write a test for foo.py covering the edge case where the user is logged out. avoid mocks."* |
| **Point to sources** | *"why does ExecutionFactory have such a weird api?"* | *"look through ExecutionFactory's git history and summarize how its api came to be"* |
| **Reference existing patterns** | *"add a calendar widget"* | *"look at how existing widgets are implemented on the home page... HotDogWidget.php is a good example. follow the pattern..."* |
| **Describe the symptom** | *"fix the login bug"* | *"users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it"* |

Vague prompts can be useful when you're exploring and can afford to course-correct. A prompt like `"what would you improve in this file?"` can surface things you wouldn't have thought to ask about.

### Provide rich content

- **Reference files with `@`** instead of describing where code lives.
- **Paste images directly** — copy/paste or drag and drop into the prompt.
- **Give URLs** for documentation. Use `/permissions` to allowlist frequently-used domains.
- **Pipe in data** — `cat error.log | claude`.
- **Let Claude fetch what it needs** via Bash, MCP tools, or by reading files.

---

## Configure your environment

### Write an effective CLAUDE.md

> Run `/init` to generate a starter CLAUDE.md file based on your current project structure, then refine over time.

CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules.

Example:
```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, use skills instead.

Keep it concise. For each line, ask: *"Would removing this cause Claude to make mistakes?"* If not, cut it. **Bloated CLAUDE.md files cause Claude to ignore your actual instructions!**

| ✅ Include | ❌ Exclude |
|---|---|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

You can tune instructions by adding emphasis (e.g., "IMPORTANT" or "YOU MUST"). Check CLAUDE.md into git so your team can contribute.

CLAUDE.md files can import additional files using `@path/to/import` syntax:
```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

Locations:
- `~/.claude/CLAUDE.md` — applies to all Claude sessions.
- `./CLAUDE.md` — check into git to share with your team.
- `./CLAUDE.local.md` — personal project-specific notes; gitignore this.
- Parent directories — useful for monorepos.
- Child directories — pulled in on demand.

### Configure permissions

> Use auto mode to let a classifier handle approvals, `/permissions` to allowlist specific commands, or `/sandbox` for OS-level isolation.

Three ways to reduce permission interruptions:
- **Auto mode:** a separate classifier model reviews commands and blocks only what looks risky.
- **Permission allowlists:** permit specific tools you know are safe, like `npm run lint` or `git commit`.
- **Sandboxing:** OS-level isolation that restricts filesystem and network access.

### Use CLI tools
> Tell Claude Code to use CLI tools like `gh`, `aws`, `gcloud`, and `sentry-cli` when interacting with external services.

CLI tools are the most context-efficient way to interact with external services. Claude is also effective at learning CLI tools it doesn't already know — try `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

### Connect MCP servers
> Run `claude mcp add` to connect external tools like Notion, Figma, or your database.

### Set up hooks
> Use hooks for actions that must happen every time with zero exceptions.

Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens. Try prompts like *"Write a hook that runs eslint after every file edit"* or *"Write a hook that blocks writes to the migrations folder."*

### Create skills
Create `SKILL.md` files in `.claude/skills/`. Example:
```markdown
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Skills can also define repeatable workflows you invoke directly:
```markdown
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

### Create custom subagents
Define specialized assistants in `.claude/agents/`:
```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

### Install plugins
Run `/plugin` to browse the marketplace. Plugins bundle skills, hooks, subagents, and MCP servers.

---

## Communicate effectively

### Ask codebase questions
Use Claude Code as you'd query a senior engineer:
- How does logging work?
- How do I make a new API endpoint?
- What does `async move { ... }` do on line 134 of `foo.rs`?
- What edge cases does `CustomerOnboardingFlowImpl` handle?
- Why does this code call `foo()` instead of `bar()` on line 333?

### Let Claude interview you
For larger features, have Claude interview you first:
```
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Once the spec is complete, start a fresh session to execute it.

---

## Manage your session

### Course-correct early and often
- **`Esc`** — stop Claude mid-action; context is preserved.
- **`Esc + Esc` or `/rewind`** — open the rewind menu.
- **`"Undo that"`** — have Claude revert.
- **`/clear`** — reset context between unrelated tasks.

If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt.

### Manage context aggressively
- Use `/clear` frequently between tasks.
- When auto compaction triggers, Claude summarizes what matters most.
- For more control: `/compact <instructions>` — e.g., `/compact Focus on the API changes`.
- To compact only part: `Esc + Esc`, select a checkpoint, **Summarize from here**.
- Customize compaction behavior in CLAUDE.md.
- For quick questions that don't need to stay in context, use `/btw`.

### Use subagents for investigation
> Delegate research with `"use subagents to investigate X"`.

```
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

You can also use subagents for verification: `use a subagent to review this code for edge cases`.

### Rewind with checkpoints
Every action Claude makes creates a checkpoint. Double-tap `Escape` or run `/rewind`. **Checkpoints only track changes made *by Claude*, not external processes. This isn't a replacement for git.**

### Resume conversations
- `claude --continue` — pick up most recent session.
- `claude --resume` — choose from a list.
- Name sessions with `/rename` and treat them like branches.

---

## Automate and scale

### Run non-interactive mode
```bash
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

### Run multiple Claude sessions
- **Worktrees:** separate CLI sessions in isolated git checkouts.
- **Desktop app:** manage multiple local sessions visually.
- **Claude Code on the web:** Anthropic-managed cloud infrastructure.
- **Agent teams:** automated coordination of multiple sessions.

**Writer/Reviewer pattern:**
| Session A (Writer) | Session B (Reviewer) |
|---|---|
| `Implement a rate limiter for our API endpoints` | |
| | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` | |

### Fan out across files
For large migrations or analyses:
1. Have Claude list all files that need migrating.
2. Loop through with `claude -p`:
   ```bash
   for file in $(cat files.txt); do
     claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
       --allowedTools "Edit,Bash(git commit *)"
   done
   ```
3. Test on a few files, then run at scale.

You can also pipe Claude into pipelines:
```bash
claude -p "<your prompt>" --output-format json | your_command
```

### Run autonomously with auto mode
```bash
claude --permission-mode auto -p "fix all lint errors"
```
For non-interactive runs with `-p`, auto mode aborts if the classifier repeatedly blocks actions.

---

## Avoid common failure patterns

- **The kitchen sink session.** Context full of irrelevant tasks. **Fix:** `/clear` between unrelated tasks.
- **Correcting over and over.** Context polluted with failed approaches. **Fix:** after two failed corrections, `/clear` and write a better prompt.
- **The over-specified CLAUDE.md.** Important rules get lost in noise. **Fix:** ruthlessly prune.
- **The trust-then-verify gap.** Plausible-looking implementation that doesn't handle edge cases. **Fix:** always provide verification. **If you can't verify it, don't ship it.**
- **The infinite exploration.** Claude reads hundreds of files filling context. **Fix:** scope investigations narrowly or use subagents.

---

## Develop your intuition
The patterns in this guide aren't set in stone. They're starting points that work well in general, but might not be optimal for every situation. Pay attention to what works. Over time, you'll develop intuition that no guide can capture.
