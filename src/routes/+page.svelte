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

  const approachItems = [
    {
      heading: 'Human-centered',
      description: "<p>I don't aim to replace people, but <b>amplify their capabilities</b>.</p>"
    },
    {
      heading: 'Flexible',
      description: "<p>I meet you where you are, hooking into <b>what you already know.</b></p>"
    },
    {
      heading: 'Transparent',
      description: '<p><b>You are involved</b>, understand the process, and give direction.</p>'
    }
  ];

  const capabilityItems = [
    {
      heading: 'LLM extraction & agents',
      description:
        '<p>Structured facts from unstructured documents, and agents that do the research.</p>'
    },
    {
      heading: 'Search & entity resolution',
      description:
        '<p>Hybrid keyword and semantic matching, reconciling records across sources and languages.</p>'
    },
    {
      heading: 'Verification interfaces',
      description:
        '<p>Human review as part of the pipeline: archived sources, highlighted evidence, citations.</p>'
    },
    {
      heading: 'Stay up to date',
      description:
        '<p>New models, tools and techniques, evaluated against real problems, adopted when they earn it.</p>'
    },
    {
      heading: 'Linux infrastructure',
      description:
        '<p>Servers are home turf: containers, deploy pipelines, backups, terabyte-scale processing.</p>'
    },
    {
      heading: 'The full product',
      description:
        '<p>Auth, frontend, ops and everything in between: working software, running in production.</p>'
    }
  ];

  const roadmapSteps = [
    { heading: 'Diagnose', description: 'Goals, data, constraints, and risks' },
    { heading: 'Prototype', description: 'Rapid iterations with real user flows' },
    { heading: 'Pilot', description: 'Roll out to a small group' },
    { heading: 'Scale', description: 'Adapt, monitor, and train the team' }
  ];

  const showcaseDefinitionItems = [
    {
      term: 'Project',
      definition:
        '<p><a href="https://loom.everypolitician.org">PoliLoom</a>, part of <a href="https://everypolitician.org/">EveryPolitician</a>: structuring politicians\' data for investigators and the accountability sector.</p>'
    },
    {
      term: 'Client',
      definition: '<p><a href="https://www.opensanctions.org/">OpenSanctions</a></p>'
    },
    {
      term: 'Role',
      definition: '<p>Project lead, EveryPolitician (2025–present)</p>'
    }
  ];

  const showcaseItems = [
    {
      heading: 'The problem',
      description:
        '<p>Assemble and verify structured politician data from Wikipedia/Wikidata and the wider web, across languages, ensuring provenance, correctness, and scale.</p>'
    },
    {
      heading: 'Solution highlights',
      description:
        '<p><b>Two-stage extraction pipeline</b>: LLM extracts free-text positions → hybrid search maps to existing entities → LLM reconciles.</p>' +
        '<p><b>Fast hybrid search</b>: Meilisearch with OpenAI embeddings for combined semantic and lexical entity matching</p>' +
        '<p><b>Source verification</b>: web sources archived as MHTML via Playwright and reviewed through a FastAPI + Next.js confirmation UI</p>'
    },
    {
      heading: 'Impact',
      description:
        '<p><b>Clarity</b>: From unstructured source documents to structured, linkable records.</p>' +
        '<p><b>Trust</b>: Every extracted fact links back to a specific passage in an archived snapshot of the source.</p>' +
        '<p><b>Scale</b>: Handles Wikidata-sized inputs through an incremental, parallelized pipeline.</p>'
    }
  ];

  const faqItems = [
    {
      question: 'What kinds of problems are you best at solving?',
      answer:
        "<p>Data problems where information is scattered, unstructured, or trapped in formats that don't talk to each other. Think: extracting structured facts from thousands of documents, connecting data across systems, or building pipelines that turn messy inputs into something reliable and searchable.</p>" +
        "<p>I use LLMs where they genuinely help—extraction, matching, classification—but they're usually one piece of a larger system. If your problem is better solved with a spreadsheet or a well-written SQL query, I'll tell you that.</p>"
    },
    {
      question: 'How involved does our team need to be?',
      answer:
        "<p>More at the start, less over time. Early on I need access to the people who understand the problem—what's actually painful, what the data looks like, what \"good enough\" means. That might be a few hours in the first week or two.</p>" +
        "<p>During prototyping I'll share work frequently and need feedback. Once we're building for real, involvement drops to occasional check-ins and testing. By handover, the goal is that your team understands what's running and can operate it without me.</p>"
    },
    {
      question: 'What does a typical project timeline look like?',
      answer:
        '<p>It depends entirely on the problem. A small integration might take a few weeks; a complex data pipeline with verification workflows takes months and evolves as we learn what actually works.</p>' +
        '<p>Rather than give you made-up estimates, I\'d point you to the <a href="https://discuss.opensanctions.org/t/poliloom-loom-for-weaving-politicians-data/121">PoliLoom devlog</a>—it shows how a real project unfolded, including the dead ends and course corrections. That\'s more honest than a tidy timeline.</p>' +
        "<p>What I can promise: I ship early and often. You'll see working pieces within the first few weeks, not a big reveal after months of silence.</p>"
    },
    {
      question: 'Who owns the code?',
      answer:
        "<p>You do. Everything I build for you is yours—code, configurations, documentation. I prefer to build things that could be open-sourced if you wanted, and I'll actively suggest it when it makes sense. No vendor lock-in, no proprietary dependencies that tie you to me.</p>"
    },
    {
      question: 'Do you also build the user interface, or just the backend?',
      answer:
        "<p>Both. I design and build the full system—data pipelines, APIs, and the interface people actually use. A clear UI isn't optional; it's what makes the difference between a tool that gets used and one that gets abandoned.</p>"
    },
    {
      question: 'What do you charge?',
      answer:
        "<p>People hire me when the problem matters and the result has to hold up—if the deciding factor is price, I'm probably not the right hire.</p>"
    },
    {
      question: "What do you need from us to figure out if we're a good fit?",
      answer:
        "<p>A conversation about the actual problem—not a polished pitch, just what's frustrating and why it matters. I work best with organizations doing something meaningful: journalism, accountability, public interest, open data, or businesses that genuinely care about doing good work rather than just scaling revenue.</p>" +
        '<p>If your goal is "add AI to make investors happy," we\'re probably not a match. If you\'re trying to solve a real problem and want to understand what you\'re building, let\'s talk.</p>'
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
      cta={[
        {
          href: mailtoHref(business.contact.subject, business.contact.body),
          text: 'Contact me',
          icon: '→'
        },
        { href: '#work', text: 'See my work', icon: '↓', variant: 'secondary' }
      ]}
    />

    <section class="section section-light">
      <h2>Understandable process</h2>
      <p>From roadmap to rollout, I prototype rapidly and build production systems with your team. My approach is:</p>
      <Features columns={3} items={approachItems} />
    </section>

    <section class="section section-dark">
      <h2>What I do</h2>
      <p>Fifteen years of production work keeps circling back to the same set of capabilities:</p>
      <Features columns={3} items={capabilityItems} />
    </section>

    <section class="section section-light">
      <h2>From roadmap to rollout</h2>
      <Roadmap steps={roadmapSteps} />
    </section>

    <section id="work" class="section section-light">
      <h2>Current work</h2>
      <DefinitionList items={showcaseDefinitionItems} />
      <Features columns={3} items={showcaseItems} />
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
      <Faq items={faqItems} />
    </section>
  </main>

  <JsonLd data={professionalService} />
</div>
