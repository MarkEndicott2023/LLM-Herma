# Building a C Compiler with a Team of Parallel Claudes

**Source:** https://www.anthropic.com/engineering/building-c-compiler
**Author:** Nicholas Carlini (Safeguards team researcher)
**Published:** Feb 5, 2026
**Fetched:** 2026-05-05
**Note:** Structured outline extracted via WebFetch — not verbatim article text.

---

## Section 1: Introduction & Overview

- 16 parallel Claude Opus 4.6 agents tasked with writing a Rust-based C compiler from scratch.
- Compiler capable of compiling Linux kernel across x86, ARM, and RISC-V architectures.
- Project consumed nearly **2,000 Claude Code sessions** with ~**$20,000** API costs.
- Produced a 100,000-line compiler.
- Approach termed "agent teams" — multiple Claude instances working in parallel on a shared codebase without active human intervention.
- Source code publicly available in GitHub repository.

---

## Section 2: Enabling Long-Running Claudes

**Core Architecture:**
- Existing scaffolds (Claude Code) require operator availability; model stops and waits for input.
- Solution: infinite loop harness that automatically sequences tasks without human intervention.
- Loop structure: agent completes task → immediately picks next task → repeat indefinitely.

**Bash Loop Implementation:**
- `while true` loop structure (run in container, not on personal machine).
- Captures git commit hash: `COMMIT=$(git rev-parse --short=6 HEAD)`.
- Logs output to timestamped file: `agent_logs/agent_${COMMIT}.log`.
- Executes Claude with `--dangerously-skip-permissions` flag.
- Loads agent instructions from `AGENT_PROMPT.md` file.

**Agent Instructions:**
- Break problems into small pieces.
- Track current work status.
- Determine next work items autonomously.
- Continue until work is perfect (no stopping condition).

---

## Section 3: Running Claude in Parallel

**Two Key Advantages:**
- Single Claude Code session performs one task sequentially; parallelization enables simultaneous debugging.
- Multiple agents enable specialization (documentation maintenance, code quality oversight, specialized subtasks).

**Synchronization Architecture:**
- Create a bare git repository as central coordination point.
- Spin up Docker container for each agent with repository mounted at `/upstream`.
- Each agent clones local copy to `/workspace` within container.
- Agents push changes from local workspace to upstream repository.

**Lock-Based Task Coordination:**
- Agents claim tasks by writing text files to `current_tasks/` directory.
- Examples: `current_tasks/parse_if_statement.txt`, `current_tasks/codegen_function_definition.txt`.
- Git synchronization forces second agent claiming same task to choose different one.
- Workflow sequence: take lock → work on task → pull from upstream → merge changes → push → remove lock.

**Conflict Resolution:**
- Merge conflicts occur frequently.
- Claude capable of resolving conflicts autonomously.
- No explicit orchestration agent implemented.
- Each Claude agent decides actions independently.
- Agents typically select "next most obvious" problem.
- When stuck, agents maintain running documentation of failed approaches and remaining tasks.

---

## Section 4: Lessons from Programming with Claude Agent Teams

### Write Extremely High-Quality Tests

- "Claude will work autonomously to solve whatever problem I give it. So it's important that the task verifier is nearly perfect."
- Task verification determines what Claude solves; imperfect tests cause wrong problems to be solved.

**Practical Implementation:**
- Source high-quality compiler test suites.
- Write verifiers for open-source software packages.
- Create build scripts for external projects.
- Monitor Claude's mistakes and design new tests based on failure modes.

**Specific Example:**
- Issue: Claude frequently broke existing functionality when implementing new features.
- Solution: built continuous integration pipeline with stricter enforcement.
- Result: new commits prevented from breaking existing code.

### Put Yourself in Claude's Shoes

- Write test harness for Claude's needs, not human preferences.
- Constant reassessment of assumptions about test communication.

**Orientation Challenges:**
- Each agent starts in fresh container with no context.
- Agents spend significant time orienting on large projects before reaching tests.

**Documentation Strategy:**
- Maintain extensive READMEs.
- Maintain detailed progress files.
- Update status frequently and explicitly.

**Context Window Pollution:**
- Avoid printing thousands of useless bytes.
- Print only few lines of output to context.
- Log important information to separate files for Claude to retrieve when needed.
- Make logfiles easy to process automatically (e.g., "ERROR" keyword on same line as reason for grep searching).
- Pre-compute aggregate summary statistics to prevent Claude recomputation.

**Time Blindness:**
- Claude cannot track elapsed time.
- Left alone, Claude happily spends hours running tests instead of making progress.
- Print incremental progress infrequently to avoid context pollution.
- Include default `--fast` option running 1% or 10% random sample.
- Make subsampling deterministic per-agent but random across VMs.
- Ensures all files covered while allowing each agent to identify regressions.

### Make Parallelism Easy

**Initial Parallelization Strategy:**
- Multiple distinct failing tests: trivial parallelization.
- Each agent picks different failing test to work on.
- Scales naturally across independent test cases.

**Mid-Project Scaling:**
- After test suite reached 99% pass rate, each agent worked on different small open-source project.
- Examples: SQLite, Redis, libjpeg, MQuickJS, Lua.

**Bottleneck: Monolithic Tasks**
- Linux kernel compilation created single giant task.
- All 16 agents would hit same bug, fix it, overwrite each other's changes.
- Parallelism advantage eliminated.

**Solution: Compiler Oracle Technique**
- Use GCC as known-good reference compiler.
- New test harness randomly compiles kernel files using GCC.
- Only remaining files compiled with Claude's compiler.
- If kernel works: problem not in Claude's subset.
- If kernel fails: refine by re-compiling subset with GCC.
- Result: agents work in parallel fixing different bugs in different files.
- Continued until Claude's compiler compiled all files independently.

**Additional Technique:**
- Apply delta debugging for files that fail together but work independently.

### Multiple Agent Roles

**Specialization Strategy:**
- One agent: deduplication (prevent re-implementation of existing functionality).
- One agent: compiler performance optimization.
- One agent: generated code efficiency optimization.
- One agent: Rust design critique and structural improvements.
- One agent: documentation maintenance.

---

## Section 5: Stress Testing the Limits of Agent Teams

**Project as Capability Benchmark:**
- Designed to test limits of current LLM capabilities.
- Identifies what models can "barely achieve" now to predict reliable future capabilities.
- Used as benchmark across Claude 4 model series.

**Specified Design Requirements:**
- From-scratch optimizing compiler.
- No dependencies beyond Rust standard library.
- GCC-compatible.
- Able to compile Linux kernel.
- Support for multiple backends.
- Unspecified implementation details left to Claude.

**Prior Model Performance:**
- Previous Opus 4 models: barely functional compilers.
- Opus 4.5: first to produce functional compiler passing large test suites; failed on real large projects.
- Opus 4.6: goal to stress limits further.

### Evaluation

**Resource Consumption:**
- Nearly 2,000 Claude Code sessions across two weeks.
- 2 billion input tokens consumed.
- 140 million output tokens generated.
- Total cost: just under $20,000.
- Fraction of cost to produce manually; exponentially lower than team production cost.

**Clean-Room Implementation:**
- Claude had no internet access during development.
- Depends only on Rust standard library.
- 100,000-line compiler.

**Demonstrated Capabilities:**
- Builds bootable Linux 6.9 on x86, ARM, and RISC-V.
- Compiles QEMU, FFmpeg, SQLite, PostgreSQL, Redis.
- 99% pass rate on most compiler test suites including "GCC torture test suite."
- Successfully compiles and runs Doom.

**Documented Limitations:**

1. **16-bit x86 Compiler Gap:**
   - Necessary to boot Linux from real mode.
   - Falls back to GCC for this phase.
   - x86_32 and x86_64 compilers are Claude's own implementation.

2. **Missing Assembler/Linker:**
   - No proprietary assembler and linker.
   - These were last items Claude started automating.
   - Still somewhat buggy.
   - Demo video used GCC assembler and linker.

3. **Incomplete Project Support:**
   - Successfully builds many projects but not all.
   - Not yet drop-in replacement for production compiler.

4. **Code Generation Efficiency:**
   - Generated code less efficient than GCC with optimizations disabled.
   - Even with all optimizations enabled.

5. **Rust Code Quality:**
   - Reasonable but not expert-level.

**Performance Ceiling:**
- Compiler nearly reached limits of Opus 4.6 abilities.
- Multiple difficult attempts by author to fix limitations only partially successful.
- New features and bugfixes frequently broke existing functionality.

---

## Section 6: Looking Forward

**Historical Model Evolution:**
- Early models: useful for IDE tab-completion.
- Progression: function body completion from docstrings.
- Claude Code launch: agent-based pair-programming mainstream.
- Historical assumption: user defines task → LLM runs seconds/minutes → returns answer → user provides follow-up.

**Agent Teams Innovation:**
- Enable autonomous implementation of entire complex projects.
- Shift in user capability: become more ambitious with goals.

**Caveats and Concerns:**
- Still early-stage with real risks.
- Human supervision during development ensures quality control and real-time error catching.
- Autonomous systems risk: tests pass but job incomplete — common failure mode.
- Author's security background: concern about programmers deploying personally unverified software.
- Author expresses excitement mixed with unease.
