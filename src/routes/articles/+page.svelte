<script>
  import Seo from '$lib/components/Seo.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Visualization from '$lib/components/Visualization.svelte';
  import JsonLd from '$lib/components/JsonLd.svelte';
  import { articles } from '$lib/articles.js';
  import { SITE_URL, formatDate } from '$lib/site.js';

  const articlesLd = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Articles',
    description: 'What I think about while the machines run.',
    url: `${SITE_URL}/articles/`,
    mainEntity: {
      '@type': 'ItemList',
      itemListElement: articles.map((article, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        url: `${SITE_URL}/articles/${article.slug}/`,
        name: article.title
      }))
    }
  };
</script>

<Seo
  title="Articles - Resolve."
  socialTitle="Articles"
  description="What I think about while the machines run."
  author={null}
  robots={null}
  ogImage={`${SITE_URL}/og/articles.png`}
/>

<main>
  <Hero title="Articles" size="small" intro="What I think about while the machines run." />

  <section class="section section-light">
    <ul class="article-list">
      {#each articles as article (article.slug)}
        <li>
          <article>
            <Visualization embeddingsKey={`articles/${article.slug}`} />
            <div class="article-content">
              <h2><a href={`/articles/${article.slug}/`}>{article.title}</a></h2>
              <p>{article.intro}</p>
              <time datetime={article.date}>{formatDate(article.date)}</time>
            </div>
          </article>
        </li>
      {/each}
    </ul>
  </section>
</main>

<JsonLd data={articlesLd} />
