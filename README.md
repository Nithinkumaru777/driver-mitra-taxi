# Driver Mitra Taxi website

This guide is for anyone looking after the site. You don't need to be a developer. Follow the steps in order and copy the commands exactly.

**Contents**

1. [One-time setup](#1-one-time-setup)
2. [See the site on your computer](#2-see-the-site-on-your-computer)
3. [Change words, phone numbers and other details](#3-change-words-phone-numbers-and-other-details)
4. [Change prices (daily rent)](#4-change-prices-daily-rent)
5. [Add a driver photo](#5-add-a-driver-photo)
6. [Add the 3D car (splat scan)](#6-add-the-3d-car-splat-scan)
7. [Put the site online (Netlify or Vercel)](#7-put-the-site-online-netlify-or-vercel)
8. [If something goes wrong](#8-if-something-goes-wrong)

Anything still waiting on information from the business is listed in [TBD.md](TBD.md).

---

## 1. One-time setup

You only do this once per computer.

1. Install **Node.js** version 22 or newer from <https://nodejs.org> (choose the "LTS" button). Accept all the default options.
2. Get the project folder onto your computer (copy it, or download it from GitHub).
3. Open a terminal **in the project folder**:
   - **Windows:** open the folder in File Explorer, click the address bar, type `cmd` and press Enter.
   - **Mac:** right-click the folder in Finder → *New Terminal at Folder*.
4. Type this and press Enter. It downloads the tools the site needs and takes a few minutes:

   ```
   npm install
   ```

From now on, "run" a command means: type it into this terminal and press Enter.

## 2. See the site on your computer

```
npm run dev
```

Open <http://localhost:4321> in your browser. While this is running, the page refreshes by itself every time you save a change. Press `Ctrl + C` in the terminal to stop it.

To check the finished version exactly as visitors will see it:

```
npm run build
npm run preview
```

If `npm run build` ends with an error, the site would also fail to go online. Fix the error first (see [section 8](#8-if-something-goes-wrong)).

## 3. Change words, phone numbers and other details

**Almost everything you'll want to change is in one file: `src/content/site.ts`.** Open it in any text editor. A free editor like [VS Code](https://code.visualstudio.com) is easiest, but Notepad works too.

| What you want to change | Where to find it in `site.ts` |
|---|---|
| Phone numbers | `contact` → `phones` |
| WhatsApp number | `contact` → `whatsapp`, digits only with 91 in front, e.g. `'919876543210'` |
| Email, office address | `contact` → `email`, `address` |
| Daily rent prices | `plans` (see [section 4](#4-change-prices-daily-rent)) |
| "Most Popular" badge | `mostPopularPlan` |
| "___+ drivers on the road" | `driversOnRoad`, e.g. `'250'` |
| Driver photos and captions | `gallery` (see [section 5](#5-add-a-driver-photo)) |
| Headings, buttons, FAQ answers, car specs | The long `en = { … }` block further down. Each section of the page has its own group, e.g. `faq`, `car`, `benefits`. |

**Rules for editing:**

- Change only the text **between the quote marks** `'like this'`. Leave the quote marks, commas and brackets alone.
- If your text contains an apostrophe, put a backslash in front of it: `'Driver\'s licence'`.
- `TBD` means "not decided yet". It shows on the website as **[TBD]**. Replace it with the real text in quotes, e.g. change `email: TBD,` to `email: 'hello@drivermitra.in',`.
- Never put in made-up prices, numbers or names. If you don't know something yet, leave it as `TBD`.

Save the file and check the page at <http://localhost:4321>. When it looks right, put it online ([section 7](#7-put-the-site-online-netlify-or-vercel)).

**Example: FAQ answer.** Change

```ts
{ q: 'Is the ₹10,000 refundable?', a: TBD },
```

to

```ts
{ q: 'Is the ₹10,000 refundable?', a: 'Yes, fully refundable if you cancel before the car is handed over.' },
```

## 4. Change prices (daily rent)

In `src/content/site.ts`, find:

```ts
export const plans: { years: PlanYears; dailyRent: string }[] = [
  { years: 3, dailyRent: TBD },
  { years: 4, dailyRent: TBD },
  { years: 5, dailyRent: TBD },
];
```

Replace each `TBD` with the amount **in quotes, without the ₹ sign**. The site adds the ₹ sign for you:

```ts
  { years: 3, dailyRent: '1,200' },
```

That plan card on the page will read **Daily rent: ₹1,200**.

To put the yellow **Most Popular** badge on a plan, change `export const mostPopularPlan: PlanYears | null = null;` so the last `null` becomes `3`, `4` or `5`:

```ts
export const mostPopularPlan: PlanYears | null = 4;
```

The ₹10,000 booking amount appears in many places in the wording (headline, steps, page title). To change it, use your editor's *Find and Replace* (`Ctrl + H`) on `₹10,000` across `src/content/site.ts`.

## 5. Add a driver photo

> ⚠️ **Only add photos of drivers who have given their consent to appear on the website.** Ask each driver first, and keep a record (a WhatsApp message or signed note saying yes is enough). If a driver later asks to be removed, delete their photo and their `gallery` line, then redeploy.

**Steps:**

1. **Name the photo file simply.** Use lowercase letters and dashes, no spaces, e.g. `ramesh-kumar.jpg`. JPG, PNG and WebP all work. A normal phone photo is fine. Bigger is better, and portrait (taller than wide) looks best.

2. **Put it in the folder `assets/drivers-original/`.**
   This folder stays on your computer only. It is deliberately never uploaded, because phone photos secretly contain the GPS location where they were taken. **Keep a backup copy of these originals** (see the warning below).

3. **Run the photo tool:**

   ```
   npm run drivers
   ```

   This makes small, fast-loading copies in `public/drivers/`, turns sideways photos the right way up, and **removes all hidden data (camera, date and GPS location)**. You'll see a ✓ next to each photo.

4. **Add the driver to the gallery.** In `src/content/site.ts`, find `export const gallery` and add one line inside the square brackets. `image` is the file name **without** `.jpg`:

   ```ts
   export const gallery = [
     { image: 'ramesh-kumar', name: 'Ramesh Kumar', city: 'Bengaluru', plan: '3 Years Flexible Plan', handoverDate: 'March 2026' },
   ];
   ```

   You can add an optional short quote from the driver: `…, handoverDate: 'March 2026', quote: 'Best decision for my family.' },`

5. **Remove the grey placeholder photos** once you have real ones: delete the four `placeholder-…` lines from `gallery`. You can also delete the `placeholder-…jpg` files in `assets/drivers-original/`, then run `npm run drivers` again.

6. **Check it** with `npm run dev`, then **put it online** ([section 7](#7-put-the-site-online-netlify-or-vercel)).

> ⚠️ **Important: `npm run drivers` rebuilds every photo from scratch** using whatever is in `assets/drivers-original/` *on this computer*. If you run it on a different computer that doesn't have the original photos, it will **delete those drivers' photos from the website**. Always run it on a computer that has *all* the original photos (keep them backed up in Google Drive or similar).

## 6. Add the 3D car (splat scan)

Right now the site shows a **real photo** of the white Dzire in the top section and in "Our Car". It's built to turn into a **photo-real 3D car** that visitors can spin, once you have a **Gaussian-splat scan** of the car. A splat scan is a 3D capture made from a walk-around video or lots of photos. Until you add one, the site simply keeps showing the photo, and nothing is broken.

1. **Get a scan.** Film a slow walk-around of a white Dzire Tour S (two loops: one at waist height, one higher). Outdoors on a cloudy day is best, with no people, balloons or other cars close by. Turn it into a splat with an app such as Polycam, Luma or Postshot (or ask a developer), and export it as a **`.ply`** file. The car must be the sedan, never a hatchback.

2. Name the file `dzire.ply` and put it in `assets/car-3d/` (create the folder if needed). This folder is not uploaded to GitHub, because scans are very large.

3. **Compress it** so it loads fast on mobile data:

   ```
   npm run splats
   ```

   This makes two files in `public/car-3d/`: `dzire.sog` for computers (10 MB or less) and `dzire-mobile.sog` for phones (5 MB or less). If the scan is too big, it automatically lowers the quality step by step until the file fits. If it says the file is still too big at the lowest step, ask a developer to crop the room out of the scan.

   If the car shows **upside down** or facing the wrong way later, add a turn after the file name, for example: `npm run splats -- assets/car-3d/dzire.ply -r 180,0,0`.

4. **Switch it on.** In `src/content/site.ts`, find `carModel` and change the `splat` line to:

   ```ts
   splat: { desktop: '/car-3d/dzire.sog', mobile: '/car-3d/dzire-mobile.sog' } as { desktop: string; mobile: string } | null,
   ```

5. Run `npm run dev`, open <http://localhost:4321>, and move the mouse once. The car should appear and turn slowly. Drag it to spin it, and scroll the mouse wheel over it to zoom.

6. **Check the yellow labels** ("Spacious boot", "CNG option", "Comfortable rear seats"). They are pinned to points on the car. If one sits in the wrong place, a developer adjusts `hotspotAnchors` in the same `carModel` block (about 10 minutes).

7. Put the site online ([section 7](#7-put-the-site-online-netlify-or-vercel)).

**Changing the photo:** the photo comes from `reference/dzire-3d/photos/02-front-three-quarter-left.jpg`. To use a different one, replace that file (or change the file name in `scripts/car-poster.mjs`), then run `npm run car:poster` and `npm run icons`. The second command also updates the picture shown when the link is shared on WhatsApp/Facebook.

**Tip for checking:** you can try any splat file in `public/` without changing `site.ts` by adding `?splat=` to the address, e.g. <http://localhost:4321/?splat=/car-3d/dzire.sog>.

## 7. Put the site online (Netlify or Vercel)

Pick **one** host. Both have a free plan that is plenty for this site.

### Option A (recommended): connect GitHub, then it updates by itself

You set this up once. After that, every change you save to GitHub goes live in about a minute.

**First-time setup on Netlify** (<https://app.netlify.com>):

1. Put the project on GitHub (a developer can do this in a few minutes).
2. In Netlify: **Add new site → Import an existing project → GitHub** → pick the repository.
3. Fill in:
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
4. Under **Environment variables**, add:
   - `SITE_URL` = your real web address, e.g. `https://www.drivermitrataxi.in`
   - `NODE_VERSION` = `22`
5. Click **Deploy**.

**First-time setup on Vercel** (<https://vercel.com>):

1. **Add New → Project** → import the GitHub repository. Vercel recognises the site as "Astro" automatically.
2. Under **Environment Variables**, add `SITE_URL` = your real web address.
3. Click **Deploy**.

**Every time you make a change after that:**

1. Save your edits (and run `npm run drivers` if you added photos).
2. Upload the changes to GitHub. The easiest way is [GitHub Desktop](https://desktop.github.com): write a short summary (e.g. "Add Ramesh photo"), click **Commit**, then **Push**.
3. Netlify/Vercel publishes the new version on its own. Check the live site after a minute or two.

### Option B: drag and drop (Netlify only, no GitHub)

1. Run `npm run build`. This creates a folder called `dist`.
2. Go to <https://app.netlify.com/drop> and drag the **`dist` folder** onto the page.

To update the site later, run `npm run build` again. In Netlify, open your site → **Deploys**, and drag the new `dist` folder onto the box there. That replaces the live site. (Dropping it on the *Drop* page again would make a second, separate site.)

> With drag and drop, `SITE_URL` must be set **on your computer** before building. Otherwise Google and WhatsApp previews point at a placeholder address. On Windows, run `set SITE_URL=https://www.drivermitrataxi.in` and then `npm run build` in the same terminal. On Mac, run `SITE_URL=https://www.drivermitrataxi.in npm run build`.

### Your own domain name

Once you've bought the domain (e.g. `drivermitrataxi.in`): in Netlify go to **Domain management → Add a domain**, or in Vercel go to **Settings → Domains**. Follow the on-screen DNS instructions. Then make sure `SITE_URL` matches the domain exactly, and redeploy.

## 8. If something goes wrong

| What you see | What to do |
|---|---|
| `Driver photo "ramesh-kumar" is missing` | The `image` name in `gallery` doesn't match a photo. Check the spelling (no `.jpg`, no capital letters), make sure the photo is in `assets/drivers-original/`, then run `npm run drivers`. |
| An error mentioning `site.ts` with a line number | A quote mark, comma or bracket got deleted near that line. Compare it with the lines around it. |
| `npm` is not recognised | Node.js isn't installed, or the terminal was open before you installed it. Close the terminal, open a new one and try again. |
| The page doesn't change after an edit | Make sure you saved the file. Refresh the browser with `Ctrl + F5`. |
| The live site didn't update | Open the **Deploys** page on Netlify (or **Deployments** on Vercel). A red/failed deploy shows the error message. It's usually the same error `npm run build` shows on your computer. |
| The 3D car shows only a still picture | Normal until a splat scan is added (section 6). After that, it's still normal on older or low-memory phones, with Data Saver on, and before the visitor first scrolls or taps. If it never loads on a good computer, check that `carModel.splat` in `site.ts` matches the file names in `public/car-3d/`. |

### For developers

Astro 7 (static) + Tailwind CSS v4 + GSAP/Lenis + three.js with Spark (Gaussian-splat car viewer). All copy and business data is in `src/content/site.ts`. Build decisions and their reasons are recorded in `PROGRESS.md`, and the original brief is in `BRIEF.md`. `npm test` runs the enquiry-form tests. npm installs use `registry.yarnpkg.com` (`.npmrc`), because `registry.npmjs.org` was blocked on the build network. Remove `.npmrc` if that doesn't apply to you.
