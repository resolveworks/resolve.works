# Resolve.works

## Overview

Consulting site, fully static SvelteKit. All content lives in the repo — no
database, no CMS. Homepage is section-based; articles are markdown.

## Structure

- `src/routes/` — pages (`+page.svelte` homepage, `articles/`, `404/`)
- `src/lib/components/` — sections: `Hero`, `Features`, `DefinitionList`, `Roadmap`, `Faq`, `About`, `Seo`
- `src/lib/data/` — `business.json`, `author.json`
- `src/content/articles/*.md` — mdsvex articles (frontmatter: `title`, `intro`, `date`)
- `static/` — `styles.css` (global stylesheet, kept verbatim), `visualization.js`, `roadmap.js`, `embeddings.json`, `avatar.webp`, `robots.txt`, `sitemap.xml`
- `scripts/generate_embeddings.py` — uv script for the visualization data

## Tech Stack

- SvelteKit 2 + Svelte 5, mdsvex, adapter-static (`build/`, `trailingSlash = 'always'`)
- pnpm; uv for the embeddings script; Docker (nginx) to serve

## Commands

```bash
pnpm dev                              # dev server
pnpm build                            # prerender to build/
uv run scripts/generate_embeddings.py --output static/embeddings.json
docker build -t resolve.works . && docker run --rm -p 8080:80 resolve.works
```

## Conventions & SEO

Reuse existing `styles.css` classes; pages wrap content in a classed div
(`home-page`/`article-page`) instead of body classes; use the `Seo` component for
head meta. Preserve all SEO features (meta, OG/Twitter, canonical `https` URLs,
JSON-LD, sitemap). After adding/editing an article, rerun the embeddings script
and update `static/sitemap.xml` lastmod.
