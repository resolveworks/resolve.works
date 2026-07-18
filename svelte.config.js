import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { mdsvex } from 'mdsvex';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // mdsvex turns `.md` files in src/content/articles/ into Svelte components.
  // smartypants is disabled so article copy (straight quotes, em dashes) is
  // preserved as written.
  preprocess: [
    vitePreprocess(),
    mdsvex({
      extensions: ['.md'],
      smartypants: false,
      highlight: false
    })
  ],
  extensions: ['.svelte', '.md'],
  kit: {
    // Default pages/assets output is `build/`.
    adapter: adapter()
  }
};

export default config;
