<script>
  let { items } = $props();

  function stripHtml(html) {
    return html.replace(/<[^>]*>/g, '');
  }

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: stripHtml(item.answer)
      }
    }))
  };

  const ld = `<script type="application/ld+json">${JSON.stringify(jsonLd, null, 4)}<\/script>`;
</script>

{#each items as item}
  <details>
    <summary>{item.question}</summary>
    {@html item.answer}
  </details>
{/each}

{@html ld}
