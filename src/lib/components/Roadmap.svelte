<script>
  let { steps } = $props();
</script>

<ol>
  {#each steps as step}
    <li>
      <h3>{step.heading}</h3>
      <p>{step.description}</p>
    </li>
  {/each}
</ol>
