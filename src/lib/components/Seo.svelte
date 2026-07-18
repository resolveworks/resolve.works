<script>
  import { page } from '$app/state';
  import { SITE_URL } from '$lib/site.js';

  let {
    title,
    description = null,
    canonical = `${SITE_URL}${page.url.pathname}`,
    socialTitle = null,
    robots = 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1',
    author = 'Johan Schuijt',
    ogType = 'website',
    twitterCard = 'summary_large_image'
  } = $props();

  // OG/Twitter title matches the visible page name; `title` may carry the
  // " - Resolve." suffix, so pages pass socialTitle to override it.
  const social = $derived(socialTitle ?? title);
</script>

<svelte:head>
  <title>{title}</title>
  {#if description}
    <meta name="description" content={description} />
  {/if}
  {#if author}
    <meta name="author" content={author} />
  {/if}
  {#if robots}
    <meta name="robots" content={robots} />
  {/if}
  <link rel="canonical" href={canonical} />
  <meta property="og:type" content={ogType} />
  <meta property="og:url" content={canonical} />
  <meta property="og:title" content={social} />
  {#if description}
    <meta property="og:description" content={description} />
  {/if}
  <meta name="twitter:card" content={twitterCard} />
  <meta name="twitter:url" content={canonical} />
  <meta name="twitter:title" content={social} />
  {#if description}
    <meta name="twitter:description" content={description} />
  {/if}
</svelte:head>
