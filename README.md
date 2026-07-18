# Resolve.

Source for [resolve.works](https://resolve.works) — the site of **Resolve.**, an
IT consulting practice helping ethical SMBs build modern software that saves
time without replacing people. Run by [Johan Schuijt](https://www.linkedin.com/in/johanschuijt/).

The site is **fully static**: prerendered HTML/CSS/JS, no database, no CMS.

## Tech stack

- [SvelteKit 2](https://kit.svelte.dev/) + [Svelte 5](https://svelte.dev/), [mdsvex](https://mdsvex.pngwn.io/) for article markdown, [`@sveltejs/adapter-static`](https://github.com/sveltejs/kit/tree/master/packages/adapter-static)
- [pnpm](https://pnpm.io/) for dependencies
- A [uv](https://docs.astral.sh/uv/) script (`scripts/generate_embeddings.py`, sentence-transformers + UMAP) that builds the article-visualization data — run manually after editing articles
- Docker (nginx) for serving the static build

## Local development

```bash
pnpm install      # install dependencies
pnpm dev          # dev server (http://localhost:5173)
pnpm build        # prerender the static site into build/
pnpm preview      # serve the built site locally
```

After adding or editing an article, regenerate the visualization data:

```bash
uv run scripts/generate_embeddings.py --output static/embeddings.json
```

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
- D3 visualizations (bundled): `src/lib/visualization.js`, `src/lib/roadmap.js`
