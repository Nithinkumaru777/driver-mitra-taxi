import type { APIRoute } from 'astro';
import { getCopy } from '../content/site';

const t = getCopy();

// Colors match the royal-deep header and white page (tokens in global.css). Icons come from `npm run icons`.
export const GET: APIRoute = () =>
  Response.json({
    name: t.brand.name,
    short_name: 'Driver Mitra',
    description: t.meta.description,
    lang: 'en-IN',
    start_url: '/',
    display: 'standalone',
    theme_color: '#072A66',
    background_color: '#FFFFFF',
    icons: [
      { src: '/icon-192.png', sizes: '192x192', type: 'image/png' },
      { src: '/icon-512.png', sizes: '512x512', type: 'image/png' },
      { src: '/icon-maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
    ],
  });
