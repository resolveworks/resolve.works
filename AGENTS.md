# Resolve.works

## Overview

Consulting site, fully static SvelteKit. All content lives in the repo — no
database, no CMS. Homepage is section-based; articles are markdown.

## Structure

- `src/routes/` — pages (`+page.svelte` homepage, `articles/`, `404/`)
- `src/lib/components/` — homepage sections (`Features`, `DefinitionList`, `Roadmap`, `Faq`, `About`) and shared (`Hero`, `Seo`, `JsonLd`, `Visualization`)
- `src/lib/data/` — `business.json` (incl. contact email template), `author.json`
- `src/lib/site.js` — site URL, `mailtoHref`, `formatDate` helpers
- `src/content/articles/*.md` — mdsvex articles (frontmatter: `title`, `intro`, `date`); `articles/[slug]/+page.js` imports each post dynamically, `src/lib/articles.js` globs metadata only for listings/entries
- `static/` — `styles.css` (global stylesheet), `embeddings.json`, `avatar.webp`, `robots.txt`, `sitemap.xml`
- `src/lib/visualization.js`, `src/lib/roadmap.js` — D3 rendering for the embedding scatter plots and roadmap arrows (initialized by components on mount)
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

## Conventions

- Reuse existing `styles.css` classes; scope page-specific CSS by wrapping the
  page in a classed div (`home-page`, `article-page`), not body classes.
- Use the `Seo` component for head meta. Every page must keep full SEO
  coverage: meta description, OG/Twitter, canonical `https` URL, JSON-LD, and
  a `static/sitemap.xml` entry.
- After adding/editing an article, rerun the embeddings script and update
  `static/sitemap.xml` lastmod.
