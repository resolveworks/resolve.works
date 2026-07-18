---
title: "AI agents are human too"
intro: "The monetization models on the web rely not on the content itself, but on the ecosystem surrounding it: the ads, recommendations, and engagement features that capture attention alongside the actual information."
date: "2025-12-06T01:17:21.590384+00:00"
---

The way we access information online is changing. Sure you can use a web browser and search engines, but if you're like me, you're probably using AI agents to research everything. Having the model automatically fill its context with content from the web is great, however, more and more often it can't. Increasingly, the model is unable to fetch web pages. Why is this happening?

The root cause isn't technical—it's economic. The monetization models on the web rely not on the content itself, but on the ecosystem surrounding it: the ads, recommendations, and engagement features that capture attention alongside the actual information. When people use text-based language models to fetch the content, they don't see ads, don't engage, and don't build brand-loyalty. This defeats most business models on the web. It's traffic that can't be monetized.

## Zero-sum cat-and-mouse

Faced with this threat, content producers have reached for a short-sighted solution: blocking these requests. They try to force people back to the old method of using a browser, desperate to keep control over how their content is consumed.

But blocking creates more problems than it solves. First, it degrades the experience for regular browser-based visitors. Some will face CAPTCHA pages: "Verify you are human", every time they visit a website. It can take as little as a couple of extensions to have a non-default browser and end up endlessly proving you are a human.

More importantly, blocking doesn't actually work. There is no identity system baked into HTTP, so circumventing these blocks is very easy. It's so mundane that it’s [offered as a professional service](https://docs.brightdata.com/scraping-automation/web-unlocker/introduction), and [popular modules exist](https://github.com/ultrafunkamsterdam/undetected-chromedriver) to make your bot look like a default browser. There simply is no reliable way to block automated scraping while allowing normal use without massively impacting the openness of the web.

This has created an absurd economic dynamic. Content producers pay network operators to block automated traffic. Companies pulling in content pay network operators to circumvent those blocks. It's textbook economic inefficiency: both sides pouring resources into neutralizing each other. In war, the only winner is the arms dealer.

## Do you trust me?

What makes this blocking war particularly futile is that the web was never designed for it. The entire web is built on trust and "gentleman's agreements". Websites publish a `/robots.txt` file to signal what can be automatically scraped, which is just a request and completely unenforceable. These trust based systems are not an exception, they are the rule. Email assumes you won't forge sender addresses, browsers voluntarily identify themselves, and sites trust you won't flood them with requests. The entire web stack is held together by good faith.

In the past we even trusted public networks with our plain-text communication. However, we've learned that trust is not always justified. Now, we usually encrypt our traffic, but still, the system for doing so is built on trust. Instead of trusting everyone not to eaves-drop, we're trusting certified identities. That trust only works one way though: the content consumer trusts the content provider. The web was designed for anonymous browsing. Creating the reverse system, where producers verify the identity of consumers, would mean every site tracks your identity by design. That would destroy privacy altogether.

All the identity systems that currently *do* exist on the web are tied to specific companies or websites. Our agents can't fetch articles behind the paywall of services we're actually paying for—there's no authentication system that can handle this. Some companies are trying to position themselves as identity brokers, wanting to gate-keep every interaction and turn every website visit into a micro-transaction.

However, I would argue that if we want to keep the web open, while also facilitating a fair exchange of information, we should come up with an open protocol instead.

## Human after all

What everyone seems to be forgetting, is that there are actual humans behind most "automated" access. When someone uses an AI agent to research a topic, they're not "a bot", they're a person using a sophisticated tool to navigate information.

Which is actually the realization of Tim Berners-Lee's vision for the [Semantic Web](https://en.wikipedia.org/wiki/Semantic_Web): a web that can be processed by machines, to help humans navigate the information more effectively. We are witnessing exactly that, just not through [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework) and [ontologies](<https://en.wikipedia.org/wiki/Ontology_(information_science)>), but through the capabilities of language models to parse unstructured content.

## So, what now?

Our current trajectory is unsustainable. We're clinging to the "browser-only" web, as if the colorful boxes and branded experiences were the point, rather than the information exchange between humans that the web was meant to facilitate. By blocking AI agents, we're not protecting business models, we're just degrading the web for everyone while the real scrapers continue unimpeded.

Instead of fighting this evolution, we need to recognize that AI agents represent a new, legitimate way for people to interact with content. The question isn't how to stop it, but how to build sustainable business models that work with this new paradigm.

The solution won't come from blocking or from centralized gatekeepers. It will come from re-imagining how we value and exchange information when the interface between human and content is no longer a browser window, but an "intelligent" machine.

Machines parsing content to help humans navigate information. Instead of treating this as a threat, we should see it for what it is: it's what the web was supposed to be.
