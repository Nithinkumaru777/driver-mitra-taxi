# Driver Mitra Taxi website

> Full handover guide comes in Phase 8. Until then, the essentials below.

## Adding a driver photo

> **Only add photos of drivers who have given consent to appear on the website.**

1. Put the photo in `assets/drivers-original/` (e.g. `ramesh.jpg`). It stays on your computer; it is never uploaded to git.
2. Run `npm run drivers`. This makes small WebP + AVIF versions in `public/drivers/`, turns them the right way up, and removes all hidden data (camera, date, GPS location).
3. Add one line to `gallery` in `src/content/site.ts`:
   `{ image: 'ramesh', name: 'Ramesh', city: 'Bengaluru', plan: '3 Years Flexible Plan', handoverDate: 'March 2026' },`
4. Delete the `placeholder-*` lines (and their files in `assets/drivers-original/`) once real photos are in, then run `npm run drivers` again.

---

# Astro Starter Kit: Minimal

```sh
npm create astro@latest -- --template minimal
```

> 🧑‍🚀 **Seasoned astronaut?** Delete this file. Have fun!

## 🚀 Project Structure

Inside of your Astro project, you'll see the following folders and files:

```text
/
├── public/
├── src/
│   └── pages/
│       └── index.astro
└── package.json
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro/React/Vue/Svelte/Preact components.

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

## 👀 Want to learn more?

Feel free to check [our documentation](https://docs.astro.build) or jump into our [Discord server](https://astro.build/chat).
