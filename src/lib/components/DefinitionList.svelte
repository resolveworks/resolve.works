<script>
  let { items } = $props();
</script>

<dl>
  {#each items as item}
    <dt>{item.term}</dt>
    <dd>{@html item.definition}</dd>
  {/each}
</dl>
