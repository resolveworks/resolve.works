import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // mdsvex will be wired in here in a later chunk.
  preprocess: vitePreprocess(),
  kit: {
    // Default pages/assets output is `build/`.
    adapter: adapter()
  }
};

export default config;
