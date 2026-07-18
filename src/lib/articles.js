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
