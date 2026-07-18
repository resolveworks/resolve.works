<script>
  let {
    title,
    description,
    canonical = 'https://resolve.works/',
    socialTitle,
    socialDescription,
    robots = 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1',
    author = 'Johan Schuijt',
    ogType = 'website',
    twitterCard = 'summary_large_image'
  } = $props();

  const resolvedSocialTitle = socialTitle ?? title;
  const resolvedSocialDescription = socialDescription ?? description;
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
  <meta property="og:title" content={resolvedSocialTitle} />
  {#if resolvedSocialDescription}
    <meta property="og:description" content={resolvedSocialDescription} />
  {/if}
  <meta name="twitter:card" content={twitterCard} />
  <meta name="twitter:url" content={canonical} />
  <meta name="twitter:title" content={resolvedSocialTitle} />
  {#if resolvedSocialDescription}
    <meta name="twitter:description" content={resolvedSocialDescription} />
  {/if}
</svelte:head>
