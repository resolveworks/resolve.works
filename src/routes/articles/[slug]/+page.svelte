<script>
  import Seo from '$lib/components/Seo.svelte';
  import Visualization from '$lib/components/Visualization.svelte';
  import author from '$lib/data/author.json';
  import business from '$lib/data/business.json';
  import { formatDate } from '$lib/articles.js';

  let { data } = $props();
  const { article } = data;
  const Article = article.component;
</script>

<Seo
  title={`${article.title} - Resolve.`}
  canonical={`https://resolve.works/articles/${article.slug}/`}
  socialTitle={article.title}
  ogType="article"
/>

<div class="article-page">
  <div class="visualization-container">
    <Visualization embeddingsKey={`articles/${article.slug}`} />
  </div>

  <main>
    <article>
      <section class="section section-hero section-hero-medium section-light">
        <header class="hero-block">
          <h1>{article.title}</h1>
          <p class="tagline">{article.intro}</p>
          <time datetime={article.date}>{formatDate(article.date)}</time>
        </header>
      </section>

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
</div>
