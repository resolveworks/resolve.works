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
    ogImage = null,
    // All og images are the generated cards from src/lib/server/og.js, which
    // are always 1200x630 and contain only the wordmark over the embedding
    // scatter — hence the shared alt default.
    ogImageWidth = 1200,
    ogImageHeight = 630,
    ogImageAlt = "Resolve. wordmark over a scatter plot of the site's content embeddings",
    publishedTime = null,
    modifiedTime = null,
    twitterCard = null
  } = $props();

  // OG/Twitter title matches the visible page name; `title` may carry the
  // " - Resolve." suffix, so pages pass socialTitle to override it.
  const social = $derived(socialTitle ?? title);

  // No image tags unless a page passes a real social card; the twitter card
  // type follows automatically.
  const card = $derived(twitterCard ?? (ogImage ? 'summary_large_image' : 'summary'));
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
  <meta property="og:site_name" content="Resolve." />
  {#if ogImage}
    <meta property="og:image" content={ogImage} />
    <meta property="og:image:width" content={ogImageWidth} />
    <meta property="og:image:height" content={ogImageHeight} />
    <meta property="og:image:alt" content={ogImageAlt} />
  {/if}
  {#if publishedTime}
    <meta property="article:published_time" content={publishedTime} />
  {/if}
  {#if modifiedTime}
    <meta property="article:modified_time" content={modifiedTime} />
  {/if}
  {#if description}
    <meta property="og:description" content={description} />
  {/if}
  <meta name="twitter:card" content={card} />
  <meta name="twitter:url" content={canonical} />
  <meta name="twitter:title" content={social} />
  {#if ogImage}
    <meta name="twitter:image" content={ogImage} />
    <meta name="twitter:image:alt" content={ogImageAlt} />
  {/if}
  {#if description}
    <meta name="twitter:description" content={description} />
  {/if}
</svelte:head>
