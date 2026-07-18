<script>
  import Seo from '$lib/components/Seo.svelte';
  import { articles, formatDate } from '$lib/articles.js';
</script>

<Seo
  title="Articles - Resolve."
  canonical="https://resolve.works/articles/"
  socialTitle="Articles"
  ogType="website"
  author={null}
  robots={null}
/>

<svelte:head>
  <script type="module" src="/visualization.js"></script>
</svelte:head>

<main>
  <section class="section section-hero section-hero-small section-light">
    <header class="hero-block">
      <h1>Articles</h1>
      <p>Thoughts on AI, automation, and building practical systems.</p>
    </header>
  </section>

  <section class="section section-light">
    <ul class="article-list">
      {#each articles as article (article.slug)}
        <li>
          <article>
            <div class="visualization" data-embeddings={`articles/${article.slug}`}></div>
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
