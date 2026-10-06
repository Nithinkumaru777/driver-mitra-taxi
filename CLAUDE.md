Read BRIEF.md before every task. Track phase status in PROGRESS.md.

## Project notes

- npm installs go through `registry.yarnpkg.com` (see `.npmrc`): `registry.npmjs.org` TLS is blocked on this network.
- Stack: Astro (static) + Tailwind CSS v4 (via `@tailwindcss/vite`) + GSAP/Lenis (Phase 5) + `@google/model-viewer` (Phase 3).

## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)
