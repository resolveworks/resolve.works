// Loads frontmatter metadata for every article markdown file, sorted
// newest-first. Used by the articles index and the [slug] route's prerender
// entries; the rendered article component is imported by the [slug] route
// itself, so listings never pull article bodies into their bundle.

const modules = import.meta.glob('/src/content/articles/*.md', {
  eager: true,
  import: 'metadata'
});

export const articles = Object.entries(modules)
  .map(([path, metadata]) => ({
    slug: path.split('/').pop().replace(/\.md$/, ''),
    ...metadata
  }))
  .sort((a, b) => new Date(b.date) - new Date(a.date));
