<script>
  import business from '$lib/data/business.json';

  let { children } = $props();
</script>

<svelte:head>
  <script type="module" src="/roadmap.js"></script>
</svelte:head>

<nav>
  <a class="site-name" href="/">Resolve.</a>
</nav>

{@render children()}

<footer class="section">
  <a class="site-name" href="/">Resolve.</a>
  <section>
    <div>
      {#each business.taglines as tagline}
        <p>{tagline}</p>
      {/each}
    </div>
    <address>
      <dl>
        <dt>LinkedIn</dt>
        <dd><a target="_blank" href={business.linkedin}>{business.linkedin}</a></dd>
        <dt>GitHub</dt>
        <dd><a target="_blank" href={business.github}>{business.github}</a></dd>
        <dt>Email</dt>
        <dd><a href={`mailto:${business.email}`}>{business.email}</a></dd>
        <dt>Phone</dt>
        <dd><a href={`tel:${business.phone.href}`}>{business.phone.display}</a></dd>
      </dl>
    </address>
    <address>
      <dl>
        <dt>Address</dt>
        <dd>{business.address}</dd>
        <dt>VAT</dt>
        <dd>{business.vat}</dd>
        <dt>Register</dt>
        <dd><a href={business.register.url} target="_blank">{business.register.display}</a></dd>
      </dl>
      <p>{business.registrationNote}</p>
    </address>
  </section>
</footer>
