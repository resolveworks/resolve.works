<script>
  let { data } = $props();
</script>

{@html `<script type="application/ld+json">${JSON.stringify(data, null, 4)}<\/script>`}
