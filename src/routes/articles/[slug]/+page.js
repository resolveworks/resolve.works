import { error } from '@sveltejs/kit';
import { articles } from '$lib/articles.js';

// Prerender every article slug.
export function entries() {
  return articles.map((article) => ({ slug: article.slug }));
}

export async function load({ params }) {
  // mdsvex compiles each markdown file into a Svelte component (`default`)
  // with its frontmatter in `metadata`. The dynamic import keeps every
  // article in its own chunk; a universal load may return the component
  // directly because its data is never serialized.
  try {
    const post = await import(`../../../content/articles/${params.slug}.md`);
    return { content: post.default, slug: params.slug, ...post.metadata };
  } catch {
    error(404, 'Article not found');
  }
}
