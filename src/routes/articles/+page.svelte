<script>
  import Seo from '$lib/components/Seo.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Visualization from '$lib/components/Visualization.svelte';
  import { articles } from '$lib/articles.js';
  import { formatDate } from '$lib/site.js';
</script>

<Seo title="Articles - Resolve." socialTitle="Articles" author={null} robots={null} />

<main>
  <Hero title="Articles" size="small" intro="Thoughts on AI, automation, and building practical systems." />

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
