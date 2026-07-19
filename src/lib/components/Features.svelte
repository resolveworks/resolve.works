<script>
  let { columns, children } = $props();
</script>

<ul class="features-block features-block-{columns}">
  {@render children()}
</ul>
