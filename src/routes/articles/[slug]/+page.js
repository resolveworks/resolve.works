import { error } from '@sveltejs/kit';
import { articles, getArticle } from '$lib/articles.js';

// Prerender every article slug.
export function entries() {
  return articles.map((article) => ({ slug: article.slug }));
}

export function load({ params }) {
  const article = getArticle(params.slug);
  if (!article) {
    throw error(404, 'Article not found');
  }
  return { article };
}
