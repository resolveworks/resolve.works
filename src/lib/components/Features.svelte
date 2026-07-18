<script>
  let { columns, items } = $props();
</script>

<ul class="features-block features-block-{columns}">
  {#each items as item}
    <li>
      <h3>{item.heading}</h3>
      {@html item.description}
    </li>
  {/each}
</ul>
