# Resolve.works

## Overview

Consulting site, fully static SvelteKit. All content lives in the repo — no
database, no CMS. Homepage is section-based; articles are markdown.

## Structure

- `src/routes/` — pages (`+page.svelte` homepage, `articles/`, `404/`) and the prerendered social-card endpoints (`og/`)
- `src/lib/components/` — homepage sections (`Features`, `DefinitionList`, `Roadmap`, `Faq`, `About`) and shared (`Hero`, `Seo`, `JsonLd`, `Visualization`)
- `src/lib/data/` — `business.json` (incl. contact email template), `author.json`
- `src/lib/site.js` — site URL, `mailtoHref`, `formatDate` helpers
- `src/content/articles/*.md` — mdsvex articles (frontmatter: `title`, `intro`, `date`); `articles/[slug]/+page.js` imports each post dynamically, `src/lib/articles.js` globs metadata only for listings/entries
- `static/` — global assets and the generated `embeddings.json`
- `src/lib/visualization.js`, `src/lib/roadmap.js` — D3 rendering for the embedding scatter plots and roadmap arrows (initialized by components on mount)
- `src/lib/server/og.js` — social-card renderer (hand-serialized SVG + resvg); cards use the page's embedding scatter as background; the "Resolve." wordmark is pre-baked glyph paths in `src/lib/server/wordmark.svg`
- `tools/generate-embeddings.mjs` — Node generator for `static/embeddings.json` (transformers.js + UMAP)

## Tech Stack

- SvelteKit 2 + Svelte 5, mdsvex, adapter-static (`build/`, `trailingSlash = 'always'`)
- pnpm; @resvg/resvg-js for social cards; @huggingface/transformers + umap-js for embedding data; Docker (nginx) to serve

## Commands

```bash
pnpm dev                              # dev server
pnpm build                            # prerender to build/ (incl. og/*.png cards)
pnpm generate-embeddings              # build/ HTML -> static/embeddings.json, then rebuild
docker build -t resolve.works . && docker run --rm -p 8080:80 resolve.works
```

## Conventions

- Reuse existing `styles.css` classes; scope page-specific CSS by wrapping the
  page in a classed div (`home-page`, `article-page`), not body classes.
- Use the `Seo` component for head meta. Every page must keep full SEO
  coverage: meta description, OG/Twitter, canonical `https` URL, JSON-LD, and
  a `static/sitemap.xml` entry.
- Embeddings are content-derived: the generator embeds the prerendered HTML
  of every page, so after editing any page content (article or page copy) run
  `pnpm build` and `pnpm generate-embeddings`, and update lastmod for the
  changed pages in `static/sitemap.xml`.
