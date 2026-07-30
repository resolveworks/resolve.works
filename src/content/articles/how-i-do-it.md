
## When the tool becomes a product

For a long time, Anthropic's models and coding harness worked well for me. The models were good, and the harness was initially simple. Over time, though, the harness became bloated and slow. Then, in early 2026, Anthropic began [locking Claude subscription credentials to its own products](https://code.claude.com/docs/en/legal-and-compliance), blocking their use with third-party harnesses. API access remained available, but metered separately. That lock-in was the trigger for me to leave.

To me, this marked the difference between buying inference and buying a product. An inference provider sells access to a model and leaves you to decide how to use it. A product bundles the model with a prescribed way of using it. Once the harness and subscription become one product, you inherit decisions made for the whole market—and all the compromises that come with them.

## The harness that extends itself

The [pi coding agent](https://github.com/earendil-works/pi) is built around a different idea: keep the default surface small—`read`, `write`, `edit`, and `bash`—and make everything else pluggable. Extensions, skills, prompt templates, themes, and packages let you add only what you need. Pi explicitly encourages you to ask the agent to build extensions for you, and ships comprehensive documentation and examples to support it.

Tool descriptions are instructions: they tell the model what it can call, when to call it, and how to structure the call. Adding more tools therefore adds more instructions and more competing choices. In [ManyIFEval](https://openreview.net/forum?id=R6q67CDBCH), models became steadily less reliable as they were asked to follow more simultaneous instructions. [LongFuncEval](https://arxiv.org/abs/2505.10570) found the same pattern in function calling. There is no universal cliff or safe number. The practical rule is simply to keep the active surface as small as the work allows, and make every tool earn its place.

### What I use

Over the past six months, I've converged on this minimal set of extensions:

**[fork](https://github.com/resolveworks/fork)** — spawn sub-agents in separate `tmux` windows. The parent gets `spawn_agent`, `message_agent`, and `close_agent`. A child gets the `report_result` tool and can run in an isolated Git worktree on its own branch, or share the parent's working tree.

**[trace](https://github.com/resolveworks/trace)** — three deterministic tools (`def`, `callers`, `outline`) backed by tree-sitter and a SQLite index. Point it at any file or directory and it works. `callers` is intentionally syntactic — it finds call-shaped syntax without resolving imports or types — it's simple, and works on incomplete and broken source.

**[scry](https://github.com/resolveworks/scry)** — web search via the Brave Search API. One tool: `web_search`, with optional freshness filtering.

**[mine](https://github.com/resolveworks/mine)** — web fetch through a real Chrome browser on a virtual display. JavaScript-heavy pages work fine. Cookie banners are dismissed automatically. Output is clean markdown.

So far, I haven't needed anything else.

### A different intelligence

LSP is the obvious source of semantic code intelligence: precise answers about types, references, and diagnostics. But it carries a session model built for editors—a client starts a language server, synchronizes open documents, and asks position-based questions. What bothered me most was the timing. Language servers can take time to start and index a project, while [diagnostics are often published asynchronously](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocument_publishDiagnostics). By the time a result reaches the agent, it may already have continued editing, turning correct advice about an earlier state into confusing advice about the current one. Freshness checks, version tracking, and waiting can mitigate this, but add still more coordination. That slowness and complexity were the opposite of what I wanted from an agent tool.

Tree-sitter is the right foundation for exploration. It builds a syntax tree on demand, without a daemon or synchronized session, and is [designed to produce useful results even when the source contains syntax errors](https://tree-sitter.github.io/tree-sitter/). That makes it dependable on half-edited files.

Syntactic indexing provides most of what the agent needs to navigate: file outlines, definitions, and candidate call sites. It does not have to prove that every result is semantically exact; it has to point the agent toward the right code, which the agent can then read. Correctness belongs elsewhere. The linter, type checker, and test suite validate changes at explicit boundaries. This division gives the agent useful code intelligence with very little machinery.

## Never roll back

Long-running agent sessions eventually fill the context window. A common response is compaction: replace the earlier conversation with a summary and continue from there. This keeps the context bounded, but [summarization is inherently lossy](https://arxiv.org/abs/2605.23296). Constraints, decisions, and failed approaches can disappear, and repeated compactions make it harder to know what changed or why. I think of it as entropy: each rewrite introduces a little more noise.

I avoid long-running specialist sessions by delegating early. Research goes to fresh agents, each returning a focused report. I talk through those reports with the orchestrator until the next step is clear. When we reach implementation, I give it a simple instruction: chunk the work and implement it. It delegates each chunk, reviews the result, and commits it. No specialist needs the history of the entire project; each starts with clean context and only its assignment.

The same reasoning applies to task-list tools. In a long-running single-agent session, `TodoWrite` can serve as external memory as well as making the plan visible to the human. Here, the orchestrator is the task list: it maintains the plan and hands each sub-agent one focused task at a time. That makes a dedicated checklist tool obsolete.

Delegation also lets me choose a model for each role. I keep more capable models in the orchestration and review loop, while using smaller, faster models for well-scoped implementation work. Given a clear assignment and the relevant context, those smaller models are surprisingly capable.

The pattern can recurse: an orchestrator spawns feature leads, which spawn specialists of their own. Each branch gets a focused context, and its results flow back up through explicit, reviewable handoffs.

## Mistakes happen

All agents run within `tmux`, inside [Ward](https://github.com/resolveworks/ward), a single rootless container. The container exposes only the parts of the filesystem they need. This is not a complete security boundary against an adversary; it is a way to limit the blast radius of ordinary mistakes. If an agent misreads a cleanup instruction or constructs a destructive command, it can only damage what the container can reach.

Git hooks are the other half of the deterministic layer. A `post-checkout` hook prepares each new worktree, while `pre-commit` formats, lints, type-checks, and tests the result. This gives the agent lightweight tools for exploration and authoritative, project-specific validation before anything enters history.

## Who's driving?

Lately I'm mostly using open-weight models from Kimi, GLM, and DeepSeek. These are no longer budget alternatives to the frontier; they are part of it. Kimi K3 currently sits near the top of the [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/models), while GLM and DeepSeek remain competitive at API prices often far below those of the leading closed providers. There's also a less obvious reason: these labs release their models, while closed providers do not. If my usage data contributes to training, I would rather that value flow toward models the public can run and build on than remain entirely inside a closed product.

I still keep subscriptions to closed providers. For harder problems, I let models from different families respond to one another—either through sub-agents or by pasting one model's output into another context. They critique and build on each other's work. In my experience, the exchange surfaces ambiguities, edge cases, and bad assumptions that either model might accept on its own.

