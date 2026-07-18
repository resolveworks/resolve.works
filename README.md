# Resolve.

Source for [resolve.works](https://resolve.works) — the site of **Resolve.**, an
IT consulting practice helping ethical SMBs build modern software that saves
time without replacing people. Run by [Johan Schuijt](https://www.linkedin.com/in/johanschuijt/).

The site is **fully static**: prerendered HTML/CSS/JS, no database, no CMS.

## Tech stack

- [SvelteKit 2](https://kit.svelte.dev/) + [Svelte 5](https://svelte.dev/), [mdsvex](https://mdsvex.pngwn.io/) for article markdown, [`@sveltejs/adapter-static`](https://github.com/sveltejs/kit/tree/master/packages/adapter-static)
- Social cards prerendered from hand-serialized SVG to PNG endpoints with [resvg](https://github.com/yisibl/resvg-js) during `pnpm build`
- [pnpm](https://pnpm.io/) for dependencies
- Docker (nginx) for serving the static build

## Local development

```bash
pnpm install      # install dependencies
pnpm dev          # dev server (http://localhost:5173)
pnpm build        # prerender the static site into build/
pnpm preview      # serve the built site locally
```

Regenerate the visualization data after adding or editing an article (embeds the prerendered HTML with transformers.js + UMAP, then rebuilds so `build/` picks up the fresh JSON and card backgrounds):

```bash
pnpm build
pnpm generate-embeddings
```

Also update the affected `lastmod` values in `static/sitemap.xml`.

## Docker

```bash
docker build -t resolve.works .
docker run --rm -p 8080:80 resolve.works   # http://localhost:8080
```

## Where content lives

- Homepage: `src/routes/+page.svelte` (composed from `src/lib/components/`)
- Articles: `src/content/articles/*.md` (mdsvex, frontmatter: `title`, `intro`, `date`)
- Site data: `src/lib/data/business.json`, `src/lib/data/author.json`
- Static assets (served as-is): `static/styles.css`, `static/embeddings.json`, `static/avatar.webp`, `static/robots.txt`, `static/sitemap.xml`
- Social cards (prerendered endpoints): `src/routes/og/`, renderer in `src/lib/server/og.js`, pre-baked wordmark glyphs in `src/lib/server/wordmark.svg`
- D3 visualizations (bundled): `src/lib/visualization.js`, `src/lib/roadmap.js`
- Embedding data generator: `tools/generate-embeddings.mjs`
