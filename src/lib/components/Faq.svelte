<script>
  import JsonLd from '$lib/components/JsonLd.svelte';

  let { items } = $props();

  function stripHtml(html) {
    return html.replace(/<[^>]*>/g, '');
  }

  const jsonLd = $derived({
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
  });
</script>

{#each items as item}
  <details>
    <summary>{item.question}</summary>
    {@html item.answer}
  </details>
{/each}

<JsonLd data={jsonLd} />
