<script>
  import { onMount } from 'svelte';
  import { initRoadmap } from '$lib/roadmap.js';

  let { children } = $props();
  let ol;

  onMount(() => initRoadmap(ol));
</script>

<ol bind:this={ol}>
  {@render children()}
</ol>
