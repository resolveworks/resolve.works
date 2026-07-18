<script>
  import author from '$lib/data/author.json';
  import business from '$lib/data/business.json';
  import { mailtoHref } from '$lib/site.js';

  const emailHref = mailtoHref(business.contact.subject, business.contact.bodyPersonal);
</script>

{#each author.bio as paragraph}
  <p>{paragraph}</p>
{/each}

<div class="two-column-block">
  <p>
    <img src={author.avatar} alt="Profile shot of {author.name}" class="two-column-right" />
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
      <dd><a target="_blank" href={business.linkedin}>{business.linkedin}</a></dd>
      <dt>GitHub</dt>
      <dd><a target="_blank" href={business.github}>{business.github}</a></dd>
      <dt>Email</dt>
      <dd><a href={emailHref}>{business.email}</a></dd>
      <dt>Phone</dt>
      <dd><a href="tel:{business.phone.href}">{business.phone.display}</a></dd>
    </dl>
  </address>
</div>
