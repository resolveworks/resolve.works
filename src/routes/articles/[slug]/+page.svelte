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

  const articleLd = $derived({
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: data.title,
    description: data.intro,
    datePublished: data.date,
    url: `${SITE_URL}/articles/${data.slug}/`,
    author: {
      '@type': 'Person',
      name: author.name,
      url: business.linkedin
    }
  });
</script>

<Seo
  title={`${data.title} - Resolve.`}
  socialTitle={data.title}
  description={data.intro}
  ogType="article"
  ogImage={`${SITE_URL}/og/articles/${data.slug}.png`}
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
