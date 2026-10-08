// @ts-check
import { defineConfig, fontProviders } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  // [TBD: domain] Canonical, og:url/og:image, sitemap and robots.txt need the absolute URL.
  // Set SITE_URL in the host's build settings (e.g. https://www.example.in) once the domain is bought.
  // The .example fallback is a reserved, never-real domain so a missing setting is obvious.
  site: process.env.SITE_URL || 'https://Nithinkumaru777.github.io',
  base: '/driver-mitra-taxi',
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
    // The car viewer chunk = three.js + Spark with its WASM inlined (~3 MB min, ~1 MB gzip). It's lazy: imported only
    // when a splat is configured, the device passes the low-end checks and a car stage nears the viewport.
    build: { chunkSizeWarningLimit: 3200 },
  }
});
