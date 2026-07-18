<script>
  let { title, tagline, emailHref, phoneHref, phoneText, emailText } = $props();
</script>

<section class="section section-hero section-light">
  <header class="hero-block">
    <h1>{title}</h1>
    <p class="tagline">{tagline}</p>
    <p class="hero-cta">
      <a href={emailHref}>{emailText}</a>
      <a href={phoneHref}>{phoneText}</a>
    </p>
  </header>
</section>
