
## When the tool becomes a product

For a long time, using Anthropic's models through their coding harness worked well for me. The models were good, and initially the harness was simple. However, over time, the harness became bloated and slow, and starting in January 2026, Anthropic disallowed using your subscription with third-party harnesses. 

This was a shift from selling tokens to selling a product. An inference provider gives you a model and stays out of how you use it. A product draws a boundary around what you're allowed to do. That boundary however, has to work for everyone, which means a lot of compromises.

## The harness that extends itself

The [pi coding agent](https://github.com/earendil-works/pi) is built around a different idea. Its core is intentionally minimal — a small, focused tool that does one thing well. Everything else is an extension. You add only what you need. You can build extensions yourself, using the agent, its built-in documentation is great and encourages this. 

The more tools an agent has access to, the more its performance degrades. This is one of the most thoroughly replicated findings in the agent literature. The failure mode isn't a graceful slope — it's a cliff. Transformer attention is a fixed budget, and every irrelevant tool description steals weight from the correct one. A model that handles 19 tools without issue can [fail entirely at 46](https://arxiv.org/abs/2411.15399). The practical threshold is clear: keep the active tool set under 10. Four is well within the safe zone.

### A different intelligence

Language Server Protocol is the obvious choice for code intelligence — it gives compiler-accurate answers about types, references, and diagnostics. But LSP was designed for a human sitting in an IDE: stateful, cursor-position-based, a session you connect to. An agent needs something different. It needs answers in milliseconds, with no daemon to start or crash. It needs to work on broken source, because the codebase is in an intermediate state while the agent is working on it. It needs tools designed for its exploration pattern.

Tree-sitter is the right foundation. It parses source in roughly a millisecond per 10K lines, it has no startup cost, it consumes no memory when idle, and because it's purely syntactic, it works on half-edited code that would choke a compiler-backed tool. For what an agent spends most of its time doing — finding definitions, tracing callers, mapping file structure — syntactic understanding is enough. The agent can read the file directly when it needs deeper context.

The same reasoning applies to task list tools. `TodoWrite` is useful — for the human watching the terminal. It makes the agent's internal plan visible. But the model doesn't need to maintain a formatted checklist to decompose a task; it needs clear instructions in a clean context. Adding a tool for this adds tokens to every turn, competing for the same limited attention budget.

### The four

**[fork](https://github.com/resolveworks/fork)** — spawn sub-agents in separate `tmux` windows. The parent gets `spawn_agent`, `message_agent`, and `close_agent`. A child gets the `report_result` tool and can run in an isolated Git worktree on its own branch, or share the parent's working tree. 

**[trace](https://github.com/resolveworks/trace)** — three deterministic tools (`def`, `callers`, `outline`) backed by tree-sitter and a SQLite index. Point it at any file or directory and it works. `callers` is intentionally syntactic — it finds call-shaped syntax without resolving imports or types — it's simple, and works on incomplete and broken source.

**[scry](https://github.com/resolveworks/scry)** — web search via the Brave Search API. One tool: `web_search`, with optional freshness filtering.

**[mine](https://github.com/resolveworks/mine)** — web fetch through a real Chrome browser on a virtual display. JavaScript-heavy pages work fine. Cookie banners are dismissed automatically. Output is clean markdown.

Four extensions. So far, that's all I really need. When context is the scarcest resource, every tool description that doesn't earn its place is actively harmful.

## Never roll back

Long-running agent sessions eventually exceed the context window. Something we "solve" with compaction — periodically summarizing conversation history. However, errors compound across cycles and important context gets lossed. I see it as a sort of entropy, we're introducing more and more noise.

The approach here is to avoid the need for compaction and long-horizon plans by using sub-agents from the start. Instead of one agent doing research, making a plan, implementing, and compacting along the way: spawn research sub-agents that return summaries, from those summaries, make a plan, then spawn implementation sub-agents that receive chunks of the plan as tasks. After each chunk, the orchestrator can review and commit. Each agent's context stays clean and focused. 

The orchestrator maintains the high-level picture, the plan if you will; the specialists do the detailed work. This has the added benefit of using different models for these different tasks. Implementation can be done with surprisingly small and quick models, especially if the orchestrator is made to supply a bit more context.

This pattern can repeat into a tree. An orchestrator spawns feature leads, which spawn specialists. Unlike compaction, delegation doesn't lose information — it isolates it.

## Mistakes happen

The agent runs inside a container inside a `tmux` instance, with access only to the parts of the filesystem it needs. This won't stop a genuinely malicious agent, but the container protects against the far more common failure: an agent, especially a less capable one, making an "honest mistake". 

Git hooks are the other half of the deterministic enforcement layer. A `post-checkout` hook sets up worktrees, and `pre-commit` runs the linter, type checker, and test suite.

## Who's driving?

Lately I'm mostly using open-weight models — Kimi, GLM and DeepSeek. These models are  competitive, matching frontier performance at a fraction of the cost. There's also a less obvious reason. These labs publish their research. When data flows to an open-science lab, some of that value returns to the community as papers, weights, and techniques others can build on.

I still keep around subscriptions to closed providers. Using multiple models from different providers for looking at the same problem from different angles surfaces issues that any single model would miss. Models trained on different datasets bring different assumptions and catch different problems.

