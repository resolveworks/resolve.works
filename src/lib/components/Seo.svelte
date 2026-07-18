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
  <meta name="description" content={description} />
  <meta name="author" content={author} />
  <meta name="robots" content={robots} />
  <link rel="canonical" href={canonical} />
  <meta property="og:type" content={ogType} />
  <meta property="og:url" content={canonical} />
  <meta property="og:title" content={resolvedSocialTitle} />
  <meta property="og:description" content={resolvedSocialDescription} />
  <meta name="twitter:card" content={twitterCard} />
  <meta name="twitter:url" content={canonical} />
  <meta name="twitter:title" content={resolvedSocialTitle} />
  <meta name="twitter:description" content={resolvedSocialDescription} />
</svelte:head>
