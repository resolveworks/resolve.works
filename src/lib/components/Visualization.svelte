<script>
  import { onMount } from 'svelte';
  import { initVisualization } from '$lib/visualization.js';

  let { embeddingsKey } = $props();
  let container;

  onMount(() => {
    initVisualization(container, embeddingsKey);
  });
</script>

<div class="visualization" bind:this={container}></div>
