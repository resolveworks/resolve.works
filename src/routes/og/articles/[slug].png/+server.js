import { error } from '@sveltejs/kit';
import { articles } from '$lib/articles.js';
import { cardResponse } from '$lib/server/og.js';

export const prerender = true;

export function entries() {
  return articles.map((article) => ({ slug: article.slug }));
}

export function GET({ params }) {
  if (!articles.some((a) => a.slug === params.slug)) error(404, 'Article not found');
  return cardResponse({ embeddingsKey: `articles/${params.slug}` });
}
