<script>
  import { page } from '$app/state';
  import ErrorPage from '$lib/components/ErrorPage.svelte';
</script>

{#if page.status === 404}
  <ErrorPage
    title="Page not found"
    message="Sorry, this page could not be found."
    description="The page you requested could not be found."
  />
{:else}
  <ErrorPage
    title="Something went wrong"
    message="Sorry, something went wrong. Please try again later."
    description="The page could not be loaded."
  />
{/if}
