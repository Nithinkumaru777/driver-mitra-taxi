// @ts-check
import { defineConfig, fontProviders } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  // [TBD: domain] Canonical, og:url/og:image, sitemap and robots.txt need the absolute URL.
  // Set SITE_URL in the host's build settings (e.g. https://www.example.in) once the domain is bought.
  // The .example fallback is a reserved, never-real domain so a missing setting is obvious.
  site: process.env.SITE_URL || 'https://drivermitrataxi.example',
  // Self-hosted at build time; Astro adds font-display: swap and metric-matched fallbacks.
  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: 'Anton',
      cssVariable: '--font-anton',
      weights: [400],
      styles: ['normal'],
      subsets: ['latin'],
    },
    {
      provider: fontProviders.fontsource(),
      name: 'Inter',
      cssVariable: '--font-inter',
      weights: ['400 700'],
      styles: ['normal'],
      subsets: ['latin'],
    },
  ],
  vite: {
    plugins: [tailwindcss()],
    // model-viewer bundles three.js (~1 MB min, ~285 KB gzip). It's a lazy chunk, imported only when a car stage nears the viewport.
    build: { chunkSizeWarningLimit: 1100 },
  }
});
