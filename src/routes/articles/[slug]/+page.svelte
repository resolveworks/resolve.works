<script>
  import Seo from '$lib/components/Seo.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Visualization from '$lib/components/Visualization.svelte';
  import JsonLd from '$lib/components/JsonLd.svelte';
  import author from '$lib/data/author.json';
  import business from '$lib/data/business.json';
  import { SITE_URL } from '$lib/site.js';

  let { data } = $props();
  const Article = $derived(data.content);

  const articleUrl = $derived(`${SITE_URL}/articles/${data.slug}/`);

  // Stable @ids: the same Person and Organization are declared on the
  // homepage; repeating the ids lets crawlers merge them into one node each.
  const articleLd = $derived({
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    '@id': `${articleUrl}#article`,
    headline: data.title,
    description: data.description ?? data.intro,
    datePublished: data.date,
    dateModified: data.modified ?? data.date,
    image: `${SITE_URL}/og/articles/${data.slug}.png`,
    url: articleUrl,
    mainEntityOfPage: { '@type': 'WebPage', '@id': articleUrl },
    author: {
      '@type': 'Person',
      '@id': `${SITE_URL}/#person`,
      name: author.name,
      url: business.linkedin,
      sameAs: [business.linkedin, business.github]
    },
    publisher: {
      '@type': 'Organization',
      '@id': `${SITE_URL}/#organization`,
      name: business.name,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/apple-touch-icon.png`,
        width: 180,
        height: 180
      }
    }
  });
</script>

<Seo
  title={`${data.title} - Resolve.`}
  socialTitle={data.title}
  description={data.description ?? data.intro}
  ogType="article"
  ogImage={`${SITE_URL}/og/articles/${data.slug}.png`}
  publishedTime={data.date}
  modifiedTime={data.modified ?? data.date}
/>

<div class="article-page">
  <div class="visualization-container">
    <Visualization embeddingsKey={`articles/${data.slug}`} />
  </div>

  <main>
    <article>
      <Hero title={data.title} size="medium" tagline={data.intro} date={data.date} />

      <section class="section section-light">
        <Article />
      </section>

      <section class="section section-light">
        <aside class="author-block">
          <img src={author.avatar} alt={author.name} class="author-avatar" />
          <div class="author-info">
            <p class="author-name">{author.name}</p>
            <div class="author-bio">
              {#each author.bio as paragraph}
                <p>{paragraph}</p>
              {/each}
            </div>
            <dl class="author-links">
              <dt>LinkedIn</dt>
              <dd>
                <a href={business.linkedin} target="_blank" rel="noopener noreferrer">{business.linkedin}</a>
              </dd>
              <dt>GitHub</dt>
              <dd>
                <a href={business.github} target="_blank" rel="noopener noreferrer">{business.github}</a>
              </dd>
            </dl>
          </div>
        </aside>
      </section>
    </article>
  </main>

  <JsonLd data={articleLd} />
</div>
