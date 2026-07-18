<script>
  import { onMount } from 'svelte';
  import { initRoadmap } from '$lib/roadmap.js';

  let { steps } = $props();
  let ol;

  onMount(() => initRoadmap(ol));
</script>

<ol bind:this={ol}>
  {#each steps as step}
    <li>
      <h3>{step.heading}</h3>
      <p>{step.description}</p>
    </li>
  {/each}
</ol>
