<script>
  import Hero from '$lib/components/Hero.svelte';
  import Seo from '$lib/components/Seo.svelte';

  let { title, message, description = message } = $props();
</script>

<Seo
  title={`${title} - Resolve.`}
  socialTitle={title}
  {description}
  robots="noindex, follow"
  author={null}
/>

<main>
  <Hero {title} intro={message}>
    <a href="/">Back to home</a>
  </Hero>
</main>
