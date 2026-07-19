<script>
  import JsonLd from '$lib/components/JsonLd.svelte';

  let { questions, children } = $props();

  const jsonLd = $derived({
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: questions.map(({ question, answer }) => ({
      '@type': 'Question',
      name: question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: answer
      }
    }))
  });
</script>

{@render children()}

<JsonLd data={jsonLd} />
