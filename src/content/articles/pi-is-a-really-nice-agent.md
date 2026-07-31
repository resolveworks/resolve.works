---
title: "Pi is a really nice agent"
intro: "Pi starts with a small core and lets you build the rest yourself. The result is an agent environment that works the way I think."
description: "How I shaped pi around my work with focused extensions, delegated contexts, deterministic code intelligence, and open-weight models."
date: "2026-07-30T19:06:28.631064+00:00"
---

I have always built my own working environment. I use nvim, customized through plugins. I use ergodox keyboards with a keymap that probably makes sense only to me. Oh, and I use Arch, by the way. Not because everyone should manage their computer this way, but because I want my tools to adapt to how I work—not the other way around.

There is an entirely reasonable alternative: let somebody else assemble the system, maintain it, and decide how its parts fit together. That removes responsibility and lets you concentrate on the work. The tradeoff is that you can only work within boundaries designed for the whole market. An open ecosystem lets you draw those boundaries yourself.

For years, I have assembled my development environment from tools people shared on the internet. That ecosystem has given me more than software. I have learned from the code, documentation, and ideas that other people published freely.

For about a year, Claude Code was an exception. I had used Anthropic’s coding harness since its early beta, its models were among the best for programming, and the whole thing did its job well. I had no reason to look elsewhere.

Then, in early 2026, Anthropic [restricted Claude subscription credentials to its own products](https://code.claude.com/docs/en/legal-and-compliance), preventing third-party harnesses from using them. API access remained available, but was metered separately.

The change clarified what Claude Max was: not a general model subscription, but a subscription to Anthropic’s products. That did not suit how I wanted to work. I wanted a harness I could shape myself, so I started looking for an open-source alternative.

## It extends itself

I found what I wanted in the [pi coding agent](https://github.com/earendil-works/pi). Pi starts with a deliberately small core: `read`, `write`, `edit`, and `bash`. Everything else—extensions, skills, prompt templates, themes, and packages—is pluggable. It feels more like the open ecosystem I came from than a product trying to anticipate every workflow. Pi even encourages you to ask the agent to build extensions for itself, and ships comprehensive documentation and examples to support it. The tool is designed to help you build the tool.

Having used coding agents since their early days, I already had a good idea of where they struggled. The largest gap was exploration: building a global understanding of a codebase instead of accumulating a fragmented collection of files and snippets. I followed pi’s philosophy and resisted recreating every feature I had left behind. I would add only small, sharp tools for problems I had actually seen.

Tool descriptions are instructions: they tell the model what it can call, when to call it, and how to structure the call. Adding more tools therefore adds more instructions and more competing choices. In [ManyIFEval](https://openreview.net/forum?id=R6q67CDBCH), models became steadily less reliable as they were asked to follow more simultaneous instructions. [LongFuncEval](https://arxiv.org/abs/2505.10570) found the same pattern in function calling. There is no universal cliff or safe number. The practical rule is simply to keep the active surface as small as the work allows, and make every tool earn its place.

### What I've built

Over the past six months, I've converged on this minimal set of extensions:

**[fork](https://github.com/resolveworks/fork)** — lets one Pi session hand a focused task to another. Each sub-agent starts with a fresh context in its own `tmux` window, reports its result to the parent, and remains available for review or revisions. For coding tasks that can run in parallel, fork can give each child an isolated Git worktree on its own branch.

**[trace](https://github.com/resolveworks/trace)** — gives Pi three deterministic ways to navigate code: `outline` maps the definitions in a file or directory, `def` retrieves a complete definition by name, and `callers` finds call sites to inspect. Tree-sitter provides the syntax trees, while SQLite caches the resulting index. `callers` is deliberately simple: it finds call-shaped syntax without resolving imports or types, so it also works on incomplete and broken source.

**[scry](https://github.com/resolveworks/scry)** — lets Pi search the web. Its single `web_search` tool returns links with enough context for the agent to decide what to open, and can restrict searches to recent results.

**[mine](https://github.com/resolveworks/mine)** — lets Pi read those pages. Its `web_fetch` tool opens a URL in Chrome, waits for JavaScript to render, dismisses cookie banners, and extracts the main content as clean markdown. Using a browser rather than a simple HTTP request makes client-rendered sites work too.

So far, I haven't needed anything else.

Writing these extensions taught me a lot about how agentic LLMs function under the hood. That knowledge has been as valuable as the extensions themselves.

### Explore, then validate

LSP is the obvious source of semantic code intelligence: precise answers about types, references, and diagnostics. But in Claude Code, language servers were slow to start and diagnostics often arrived too late, confusing the model.

Tree-sitter is a better fit for exploration. It builds a syntax tree on demand and is [designed to produce useful results even when the source contains syntax errors](https://tree-sitter.github.io/tree-sitter/). That makes it dependable on half-edited files.

Exploration does not require every result to be semantically exact; it needs to point the agent toward the right code. Correctness belongs at an explicit boundary: a Git `pre-commit` hook formats, lints, type-checks, and tests each change. Together, Tree-sitter and the hook give me what I wanted from a language server, while being simpler and faster.

## Branch, not loop

I structure agent work around fresh contexts and explicit handoffs. Long-running sessions eventually fill the context window, and a common response is compaction: replace the earlier conversation with a summary and continue. This keeps the context bounded, but [summarization is inherently lossy](https://arxiv.org/abs/2605.23296). Constraints, decisions, and failed approaches can disappear. I think of it as entropy: each rewrite introduces a little more noise.

I keep one Pi session at the center of the work, focused on direction and decisions. Research questions go from there to fresh agents, which return focused reports for us to discuss. Once the next step is clear, I ask the main agent to divide the implementation into chunks. It delegates each chunk, reviews the result, and commits it. The main session plays much the same role as plan mode in other harnesses: it carries the plan, while the other agents carry only what they need for their task.

Keeping those roles separate also lets me choose a model for each. I use more capable models for the main session, while smaller, faster models handle well-scoped implementation work. Given a clear assignment and the relevant context, those smaller models are surprisingly capable.

On larger jobs, a delegated agent can branch the work again. The principle stays the same: each agent gets a focused context, and its results return through an explicit, reviewable handoff.

## Mistakes happen

All agents run within `tmux`, inside [Ward](https://github.com/resolveworks/ward), a single rootless container. The container exposes only the parts of the filesystem they need. This is not a complete security boundary against an adversary; it is a way to limit the blast radius of ordinary mistakes. If an agent misreads a cleanup instruction or constructs a destructive command, it can only damage what the container can reach.

## The models

Lately I'm mostly using open-weight models from Moonshot, Zhipu, and DeepSeek. These are no longer budget alternatives to the frontier; they are part of it. Kimi K3 currently sits near the top of the [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/models), while GLM and DeepSeek remain competitive at API prices often far below those of the leading closed providers. There's also a less obvious reason: these labs release their models, while closed providers do not. If my usage data contributes to training, I would rather that value flow toward models the public can run and build on than remain entirely inside a closed product.

I still keep subscriptions to closed providers. For harder problems, I let models from different families respond to one another—either through sub-agents or by pasting one model's output into another context. They critique and build on each other's work. In my experience, the exchange surfaces ambiguities, edge cases, and bad assumptions that either model might accept on its own.

Models will come and go. What I wanted was an environment that could change with them and with me. That is what I have now, and creating it has given me a satisfaction that no bought software ever could.

Pi gave me a small core I could understand and change. Everything I added came from a problem I had actually encountered. I no longer have to adapt my work to a harness designed for everyone else. I can adapt the harness to my work.
