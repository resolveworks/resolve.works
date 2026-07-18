import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { mdsvex } from 'mdsvex';

// mdsvex hard-codes `rel: ['nofollow']` on external links (no option to disable
// it). The live article body has no rel on its links, so strip it from <a>
// elements after rendering. This only touches mdsvex-rendered markdown; the
// author aside links keep their own rel="noopener noreferrer".
function stripAnchorRel() {
  return (tree) => {
    const walk = (node) => {
      if (node?.type === 'element' && node.tagName === 'a' && node.properties) {
        delete node.properties.rel;
      }
      node?.children?.forEach(walk);
    };
    walk(tree);
    return tree;
  };
}

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // mdsvex turns `.md` files in src/content/articles/ into Svelte components.
  // smartypants is disabled so article copy (straight quotes, em dashes) is
  // preserved verbatim; the article route components own their own layout.
  preprocess: [
    vitePreprocess(),
    mdsvex({
      extensions: ['.md'],
      smartypants: false,
      highlight: false,
      rehypePlugins: [stripAnchorRel]
    })
  ],
  extensions: ['.svelte', '.md'],
  kit: {
    // Default pages/assets output is `build/`.
    adapter: adapter()
  }
};

export default config;
