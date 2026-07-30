
I have always built my own working environment. I used to heavily customize my editor through plugins. I use a Moonlander keyboard with a keymap that probably makes sense only to me. I use Arch, by the way. Not because everyone should manage their computer this way, but because I want my tools to adapt to how I work—not the other way around.

There is an entirely reasonable alternative: let somebody else assemble the system, maintain it, and decide how its parts fit together. That removes responsibility and lets you concentrate on the work. The tradeoff is that you can only work within boundaries designed for the whole market. An open ecosystem lets you draw those boundaries yourself.

For years, I have assembled my development environment from tools people shared on the internet. That ecosystem has given me more than software. I have learned from the code, documentation, and ideas that other people published freely.

For about a year, Claude Code was an exception. I had used Anthropic’s coding harness since its early beta, its models were among the best for programming, and the whole thing did its job well. I had no reason to look elsewhere.

Then, in early 2026, Anthropic [restricted Claude subscription credentials to its own products](https://code.claude.com/docs/en/legal-and-compliance), preventing third-party harnesses from using them. API access remained available, but was metered separately.

The change clarified what Claude Max was: not a general model subscription, but a subscription to Anthropic’s products. That did not suit how I wanted to work. I wanted a harness I could shape myself, so I started looking for an open-source alternative.

## The harness that extends itself

I found what I wanted in the [pi coding agent](https://github.com/earendil-works/pi). Pi starts with a deliberately small core: `read`, `write`, `edit`, and `bash`. Everything else—extensions, skills, prompt templates, themes, and packages—is pluggable. It feels more like the open ecosystem I came from than a product trying to anticipate every workflow. Pi even encourages you to ask the agent to build extensions for itself, and ships comprehensive documentation and examples to support it. The tool is designed to help you build the tool.

Having used coding agents since their early days, I already had a good idea of where they struggled. The largest gap was exploration: building a global understanding of a codebase instead of accumulating a fragmented collection of files and snippets. I followed pi’s philosophy and resisted recreating every feature I had left behind. I would add only small, sharp tools for problems I had actually seen.

Tool descriptions are instructions: they tell the model what it can call, when to call it, and how to structure the call. Adding more tools therefore adds more instructions and more competing choices. In [ManyIFEval](https://openreview.net/forum?id=R6q67CDBCH), models became steadily less reliable as they were asked to follow more simultaneous instructions. [LongFuncEval](https://arxiv.org/abs/2505.10570) found the same pattern in function calling. There is no universal cliff or safe number. The practical rule is simply to keep the active surface as small as the work allows, and make every tool earn its place.

### What I use

Over the past six months, I've converged on this minimal set of extensions:

**[fork](https://github.com/resolveworks/fork)** — spawn sub-agents in separate `tmux` windows. The parent gets `spawn_agent`, `message_agent`, and `close_agent`. A child gets the `report_result` tool and can run in an isolated Git worktree on its own branch, or share the parent's working tree.

**[trace](https://github.com/resolveworks/trace)** — three deterministic tools (`def`, `callers`, `outline`) backed by tree-sitter and a SQLite index. Point it at any file or directory and it works. `callers` is intentionally syntactic — it finds call-shaped syntax without resolving imports or types — it's simple, and works on incomplete and broken source.

**[scry](https://github.com/resolveworks/scry)** — web search via the Brave Search API. One tool: `web_search`, with optional freshness filtering.

**[mine](https://github.com/resolveworks/mine)** — web fetch through a real Chrome browser on a virtual display. JavaScript-heavy pages work fine. Cookie banners are dismissed automatically. Output is clean markdown.

So far, I haven't needed anything else.

Writing these extensions taught me a lot about how agentic LLMs function under the hood. That knowledge has been as valuable as the extensions themselves.

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

In the end, I have an environment that works the way I think. Creating it has given me a satisfaction that no bought software ever could.

Pi gave me a small core I could understand and change. Everything I added came from a problem I had actually encountered. I no longer have to adapt my work to a harness designed for everyone else. I can adapt the harness to my work.

