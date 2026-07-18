import { error } from '@sveltejs/kit';
import { articles, getArticle } from '$lib/articles.js';

// Prerender every article slug.
export function entries() {
  return articles.map((article) => ({ slug: article.slug }));
}

export function load({ params }) {
  if (!getArticle(params.slug)) {
    throw error(404, 'Article not found');
  }
  // Only the slug crosses the load-data boundary; the page component resolves
  // the article (including its non-serializable mdsvex component) itself.
  return { slug: params.slug };
}
