<script>
  import { formatDate } from '$lib/site.js';

  // Hero variants across the site: full (homepage, with CTA links),
  // "small" (articles index, plain intro) and "medium" (article, with date).
  let { title, size = null, tagline = null, intro = null, date = null, cta = [] } = $props();
</script>

<section class="section section-hero{size ? ` section-hero-${size}` : ''} section-light">
  <header class="hero-block">
    <h1>{title}</h1>
    {#if tagline}
      <p class="tagline">{tagline}</p>
    {/if}
    {#if intro}
      <p>{intro}</p>
    {/if}
    {#if date}
      <time datetime={date}>{formatDate(date)}</time>
    {/if}
    {#if cta.length}
      <p class="hero-cta">
        {#each cta as link}
          <a href={link.href}>{link.text}</a>
        {/each}
      </p>
    {/if}
  </header>
</section>
