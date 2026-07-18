<script>
  let { author, linkedinHref, githubHref, emailHref, emailText, phoneHref, phoneText } = $props();
</script>

{#each author.bio as paragraph}
  <p>{paragraph}</p>
{/each}

<div class="two-column-block">
  <p>
    <img src={author.avatar} alt="Profile shot of Johan Schuijt" class="two-column-right" />
  </p>

  <h3>Selected experience</h3>
  <dl>
    {#each author.experience as item}
      <dt>{item.company}</dt>
      <dd>{item.role} ({item.range})</dd>
    {/each}
  </dl>

  <h3>Let's get in touch</h3>
  <address>
    <dl>
      <dt>LinkedIn</dt>
      <dd><a target="_blank" href={linkedinHref}>{linkedinHref}</a></dd>
      <dt>GitHub</dt>
      <dd><a target="_blank" href={githubHref}>{githubHref}</a></dd>
      <dt>Email</dt>
      <dd><a href={emailHref}>{emailText}</a></dd>
      <dt>Phone</dt>
      <dd><a href={phoneHref}>{phoneText}</a></dd>
    </dl>
  </address>
</div>
