import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';
import sitemap from '@astrojs/sitemap';
import { remarkContainers } from './src/plugins/remark-containers.mjs';
import { rehypeBadges as remarkBadges } from './src/plugins/rehype-badges.mjs';

// https://astro.build/config
export default defineConfig({
  site: 'https://bit-dots.com',
  integrations: [
    vue(),
    sitemap({
      filter: (page) => !page.includes('/404')
    }),
  ],
  markdown: {
    remarkPlugins: [
      remarkContainers,
      remarkBadges,
    ],
    rehypePlugins: [
    ],
    syntaxHighlight: 'shiki',
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
      langs: [],
      wrap: true,
    },
  },
});