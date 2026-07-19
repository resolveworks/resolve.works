# Resolve.

Source for [resolve.works](https://resolve.works) — the site of **Resolve.**, the
software and data engineering practice of [Johan Schuijt](https://www.linkedin.com/in/johanschuijt/):
LLM extraction and search, interfaces for working with data, and the full stack
underneath — for organizations doing work that matters.

The site is **fully static**: prerendered HTML/CSS/JS, no database, no CMS.

## Tech stack

- [SvelteKit 2](https://kit.svelte.dev/) + [Svelte 5](https://svelte.dev/), [mdsvex](https://mdsvex.pngwn.io/) for article markdown, [`@sveltejs/adapter-static`](https://github.com/sveltejs/kit/tree/master/packages/adapter-static)
- [D3](https://d3js.org/) for the embedding scatter visualizations (the only runtime dependency)
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

Regenerate the visualization data after editing any page content, article or otherwise (embeds the prerendered HTML with transformers.js + UMAP, then rebuilds so `build/` picks up the fresh JSON and card backgrounds):

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
