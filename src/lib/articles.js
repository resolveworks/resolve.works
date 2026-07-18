// Loads every article markdown file as an mdsvex component and exposes the
// collection sorted newest-first, plus a slug lookup for the [slug] route.
//
// Each `.md` module exposes `metadata` (parsed frontmatter) and `default`
// (the rendered Svelte component).

const modules = import.meta.glob('/src/content/articles/*.md', { eager: true });

export const articles = Object.entries(modules)
  .map(([path, module]) => {
    const slug = path.split('/').pop().replace(/\.md$/, '');
    const { title, intro, date } = module.metadata;
    return { slug, title, intro, date, component: module.default };
  })
  .sort((a, b) => new Date(b.date) - new Date(a.date));

export function getArticle(slug) {
  return articles.find((article) => article.slug === slug);
}

const MONTHS = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
];

/** Format an ISO date string as "Month D, YYYY" (locale-independent). */
export function formatDate(iso) {
  const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);
  const [, year, month, day] = match;
  return `${MONTHS[Number(month) - 1]} ${Number(day)}, ${year}`;
}
