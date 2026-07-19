<script>
  import business from '$lib/data/business.json';
  import author from '$lib/data/author.json';
  import { SITE_URL, mailtoHref } from '$lib/site.js';
  import Seo from '$lib/components/Seo.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Features from '$lib/components/Features.svelte';
  import DefinitionList from '$lib/components/DefinitionList.svelte';
  import Roadmap from '$lib/components/Roadmap.svelte';
  import Visualization from '$lib/components/Visualization.svelte';
  import About from '$lib/components/About.svelte';
  import Faq from '$lib/components/Faq.svelte';
  import JsonLd from '$lib/components/JsonLd.svelte';

  const description =
    'Software and data engineering for work that matters. I build LLM-assisted pipelines, verification interfaces and search infrastructure for journalism, accountability and open data.';

  // The FAQ copy is repeated as plain text only because JSON-LD must be data rather
  // than rendered markup. The visible content below stays normal Svelte markup.
  const faqQuestions = [
    {
      question: 'What kinds of problems are you best at solving?',
      answer:
        "Data problems where information is scattered, unstructured, or trapped in formats that don't talk to each other. Think: extracting structured facts from thousands of documents, connecting data across systems, or building pipelines that turn messy inputs into something reliable and searchable. I use LLMs where they genuinely help—extraction, matching, classification—but they're usually one piece of a larger system. If your problem is better solved with a spreadsheet or a well-written SQL query, I'll tell you that."
    },
    {
      question: 'How involved does our team need to be?',
      answer:
        "More at the start, less over time. Early on I need access to the people who understand the problem—what's actually painful, what the data looks like, what \"good enough\" means. That might be a few hours in the first week or two. During prototyping I'll share work frequently and need feedback. Once we're building for real, involvement drops to occasional check-ins and testing. By handover, the goal is that your team understands what's running and can operate it without me."
    },
    {
      question: 'What does a typical project timeline look like?',
      answer:
        "It depends entirely on the problem. A small integration might take a few weeks; a complex data pipeline with verification workflows takes months and evolves as we learn what actually works. Rather than give you made-up estimates, I'd point you to the PoliLoom devlog—it shows how a real project unfolded, including the dead ends and course corrections. That's more honest than a tidy timeline. What I can promise: I ship early and often. You'll see working pieces within the first few weeks, not a big reveal after months of silence."
    },
    {
      question: 'Who owns the code?',
      answer:
        "You do. Everything I build for you is yours—code, configurations, documentation. I prefer to build things that could be open-sourced if you wanted, and I'll actively suggest it when it makes sense. No vendor lock-in, no proprietary dependencies that tie you to me."
    },
    {
      question: 'Do you also build the user interface, or just the backend?',
      answer:
        "Both. I design and build the full system—data pipelines, APIs, and the interface people actually use. A clear UI isn't optional; it's what makes the difference between a tool that gets used and one that gets abandoned."
    },
    {
      question: 'What do you charge?',
      answer:
        "People hire me when the problem matters and the result has to hold up—if the deciding factor is price, I'm probably not the right hire."
    },
    {
      question: "What do you need from us to figure out if we're a good fit?",
      answer:
        "A conversation about the actual problem—not a polished pitch, just what's frustrating and why it matters. I work best with organizations doing something meaningful: journalism, accountability, public interest, open data, or businesses that genuinely care about doing good work rather than just scaling revenue. If your goal is \"add AI to make investors happy,\" we're probably not a match. If you're trying to solve a real problem and want to understand what you're building, let's talk."
    }
  ];

  const professionalService = {
    '@context': 'https://schema.org',
    '@type': 'ProfessionalService',
    name: business.name,
    description:
      'Software and data engineering for organizations doing public-interest work: LLM-assisted data pipelines with human verification, entity resolution, search infrastructure, and full product development.',
    url: `${SITE_URL}/`,
    telephone: business.phone.href,
    email: business.email,
    address: {
      '@type': 'PostalAddress',
      addressCountry: 'Estonia'
    },
    priceRange: '€€€',
    openingHours: 'Mo-Fr 09:00-18:00',
    founder: {
      '@type': 'Person',
      name: author.name,
      jobTitle: author.jobTitle,
      url: business.linkedin
    },
    sameAs: [business.linkedin, business.github],
    knowsAbout: [
      'AI',
      'Machine Learning',
      'LLM',
      'Entity Resolution',
      'Data Engineering',
      'Software Engineering',
      'Open Data'
    ]
  };
</script>

<Seo
  title="Software & data engineering for work that matters - Resolve."
  {description}
  socialTitle="Software & data engineering for work that matters"
  ogImage={`${SITE_URL}/og/home.png`}
/>

<div class="home-page">
  <div class="visualization-container">
    <Visualization embeddingsKey="home" />
  </div>

  <main>
    <Hero
      title="Most IT work is pointless."
      tagline="I take on the part that isn't: hard software and data problems for organizations doing work that matters."
    >
      <a href={mailtoHref(business.contact.subject, business.contact.body)}>
        <span aria-hidden="true">→</span>
        Contact me
      </a>
      <a href="#work" class="secondary">
        <span aria-hidden="true">↓</span>
        See my work
      </a>
    </Hero>

    <section class="section section-light">
      <h2>Something resembling a plan.</h2>
      <p>
        Every engagement starts with the best plan we can make — and the near-certainty that real data will punch holes in
        it. What stays fixed is how I work: in the open, in small pieces, with you close enough to steer.
      </p>
      <Features columns={3}>
        <li>
          <h3>Demos, not decks.</h3>
          <p>You judge <b>working software</b> running against your data, early enough that changing course is still cheap.</p>
        </li>
        <li>
          <h3>Dead ends included.</h3>
          <p>
            I write down <b>what didn't work</b> and why. Read the <a
              href="https://discuss.opensanctions.org/t/poliloom-loom-for-weaving-politicians-data/121">PoliLoom devlog</a> to see what that looks like.
          </p>
        </li>
        <li>
          <h3>You keep the keys.</h3>
          <p><b>Code, documentation, and a team</b> that understands what's running. Built to hand over, not to be needed.</p>
        </li>
      </Features>
    </section>

    <section class="section section-dark">
      <h2>What I do</h2>
      <p>Fifteen years of production work keeps circling back to the same set of capabilities:</p>
      <Features columns={2}>
        <li>
          <h3>LLM extraction &amp; search</h3>
          <p>
            Structured facts from unstructured documents, and agents that do the research. Underneath both is hybrid
            search, reconciling records across sources and languages over millions of entities.
          </p>
        </li>
        <li>
          <h3>Interfaces for working with data</h3>
          <p>
            Review screens, research tools, search frontends: interfaces where people judge, correct and explore. Built
            for people whose work depends on the data being right.
          </p>
        </li>
        <li>
          <h3>The full stack</h3>
          <p>
            Database, pipelines, API, the interface people work with, and the servers it runs on—auth, backups, deploys and
            monitoring included. One person, end to end.
          </p>
        </li>
        <li>
          <h3>Stay up to date</h3>
          <p>
            New models, tools and techniques, evaluated against real problems and adopted when they earn it. Right now that
            means coding agents and LLM tooling; next year it will mean something else.
          </p>
        </li>
      </Features>
    </section>

    <section class="section section-light">
      <h2>From roadmap to rollout</h2>
      <Roadmap>
        <li>
          <h3>Find the hard part</h3>
          <p>Every project has one. We go there first, with real data.</p>
        </li>
        <li>
          <h3>Try the smallest useful thing</h3>
          <p>A prototype that does something real, within weeks.</p>
        </li>
        <li>
          <h3>Learn where it breaks</h3>
          <p>Real users, real edge cases, honest notes.</p>
        </li>
        <li>
          <h3>Make it boring</h3>
          <p>Tested, monitored, documented: software your team can run without me.</p>
        </li>
      </Roadmap>
    </section>

    <section id="work" class="section section-light">
      <h2>Current work</h2>
      <DefinitionList>
        <dt>Project</dt>
        <dd>
          <p>
            <a href="https://loom.everypolitician.org">PoliLoom</a>, part of <a href="https://everypolitician.org/"
              >EveryPolitician</a
            >: structuring politicians' data for investigators and the accountability sector.
          </p>
        </dd>
        <dt>Client</dt>
        <dd><p><a href="https://www.opensanctions.org/">OpenSanctions</a></p></dd>
        <dt>Role</dt>
        <dd><p>Project lead, EveryPolitician (2025–present)</p></dd>
      </DefinitionList>
      <Features columns={3}>
        <li>
          <h3>The problem</h3>
          <p>
            Assemble and verify structured politician data from Wikipedia/Wikidata and the wider web, across languages,
            ensuring provenance, correctness, and scale.
          </p>
        </li>
        <li>
          <h3>Solution highlights</h3>
          <p>
            <b>Two-stage extraction pipeline</b>: LLM extracts free-text positions → hybrid search maps to existing entities
            → LLM reconciles.
          </p>
          <p>
            <b>Fast hybrid search</b>: Meilisearch with OpenAI embeddings for combined semantic and lexical entity matching
          </p>
          <p>
            <b>Source verification</b>: web sources archived as MHTML via Playwright and reviewed through a FastAPI + Next.js
            confirmation UI
          </p>
        </li>
        <li>
          <h3>Impact</h3>
          <p><b>Clarity</b>: From unstructured source documents to structured, linkable records.</p>
          <p>
            <b>Trust</b>: Every extracted fact links back to a specific passage in an archived snapshot of the source.
          </p>
          <p><b>Scale</b>: Handles Wikidata-sized inputs through an incremental, parallelized pipeline.</p>
        </li>
      </Features>
      <p>
        LLM entity reconciliation actually works well, and with human-in-the-loop verification, it's both accurate and accountable. <a
          href="https://discuss.opensanctions.org/t/poliloom-loom-for-weaving-politicians-data/121">Read the devlog</a
        >, or the <a href="https://blog.wikimedia.de/2026/07/08/everypolitician-mit-wikidata/">Wikimedia Deutschland interview</a> about the project.
      </p>
      <p>
        Where this goes next: the same machinery pointed at the long tail of public institutions—regional water boards, municipal councils, specialised agencies—in the <a
          href="https://discuss.opensanctions.org/t/kolkhoz-pravda/322">Kolkhoz &amp; Pravda experiments</a
        >.
      </p>
    </section>

    <section class="section section-light">
      <h2>About Johan</h2>
      <About />
    </section>

    <section class="section section-light">
      <h2>Frequently asked questions</h2>
      <Faq questions={faqQuestions}>
        <details>
          <summary>What kinds of problems are you best at solving?</summary>
          <p>
            Data problems where information is scattered, unstructured, or trapped in formats that don't talk to each
            other. Think: extracting structured facts from thousands of documents, connecting data across systems, or
            building pipelines that turn messy inputs into something reliable and searchable.
          </p>
          <p>
            I use LLMs where they genuinely help—extraction, matching, classification—but they're usually one piece of a
            larger system. If your problem is better solved with a spreadsheet or a well-written SQL query, I'll tell you
            that.
          </p>
        </details>
        <details>
          <summary>How involved does our team need to be?</summary>
          <p>
            More at the start, less over time. Early on I need access to the people who understand the problem—what's
            actually painful, what the data looks like, what "good enough" means. That might be a few hours in the first
            week or two.
          </p>
          <p>
            During prototyping I'll share work frequently and need feedback. Once we're building for real, involvement
            drops to occasional check-ins and testing. By handover, the goal is that your team understands what's running
            and can operate it without me.
          </p>
        </details>
        <details>
          <summary>What does a typical project timeline look like?</summary>
          <p>
            It depends entirely on the problem. A small integration might take a few weeks; a complex data pipeline with
            verification workflows takes months and evolves as we learn what actually works.
          </p>
          <p>
            Rather than give you made-up estimates, I'd point you to the <a
              href="https://discuss.opensanctions.org/t/poliloom-loom-for-weaving-politicians-data/121">PoliLoom devlog</a
            >—it shows how a real project unfolded, including the dead ends and course corrections. That's more honest than
            a tidy timeline.
          </p>
          <p>
            What I can promise: I ship early and often. You'll see working pieces within the first few weeks, not a big
            reveal after months of silence.
          </p>
        </details>
        <details>
          <summary>Who owns the code?</summary>
          <p>
            You do. Everything I build for you is yours—code, configurations, documentation. I prefer to build things that
            could be open-sourced if you wanted, and I'll actively suggest it when it makes sense. No vendor lock-in, no
            proprietary dependencies that tie you to me.
          </p>
        </details>
        <details>
          <summary>Do you also build the user interface, or just the backend?</summary>
          <p>
            Both. I design and build the full system—data pipelines, APIs, and the interface people actually use. A clear
            UI isn't optional; it's what makes the difference between a tool that gets used and one that gets abandoned.
          </p>
        </details>
        <details>
          <summary>What do you charge?</summary>
          <p>
            People hire me when the problem matters and the result has to hold up—if the deciding factor is price, I'm
            probably not the right hire.
          </p>
        </details>
        <details>
          <summary>What do you need from us to figure out if we're a good fit?</summary>
          <p>
            A conversation about the actual problem—not a polished pitch, just what's frustrating and why it matters. I
            work best with organizations doing something meaningful: journalism, accountability, public interest, open
            data, or businesses that genuinely care about doing good work rather than just scaling revenue.
          </p>
          <p>
            If your goal is "add AI to make investors happy," we're probably not a match. If you're trying to solve a real
            problem and want to understand what you're building, let's talk.
          </p>
        </details>
      </Faq>
    </section>
  </main>

  <JsonLd data={professionalService} />
</div>
