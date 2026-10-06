import type { APIRoute } from 'astro';

// Single-page site: only the home page is indexable (/styleguide is noindex).
export const GET: APIRoute = ({ site }) =>
  new Response(
    `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>${new URL('/', site)}</loc></url>
</urlset>
`,
    { headers: { 'Content-Type': 'application/xml' } },
  );
