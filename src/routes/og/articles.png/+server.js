import { cardResponse } from '$lib/server/og.js';

export const prerender = true;

export function GET() {
  return cardResponse({ embeddingsKey: 'articles' });
}
