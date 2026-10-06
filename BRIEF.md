# Driver Mitra Taxi — Website Build Brief

> **How this brief is used:** Antigravity is the **orchestrator** (project manager + reviewer). Claude Code is the **builder**. Antigravity hands Claude Code one phase at a time, reviews the result in the browser against the acceptance criteria, and only then moves to the next phase.
>
> **Claude Code:** save this file in the project root as `BRIEF.md` and add a line to `CLAUDE.md` saying "Read BRIEF.md before every task", so the full context survives across sessions.

---

## 0. Roles and working rules

### Antigravity (orchestrator)
1. Give Claude Code **one phase at a time** (Section 9). Never ask for the whole site in one go.
2. After each phase:
   - Ask Claude Code to run the dev server and the build, and report errors.
   - Open the site in the browser and take screenshots at **360px, 768px and 1440px** widths.
   - Check every acceptance criterion for that phase. If anything fails, send Claude Code a precise fix list and re-check.
3. Keep a running `PROGRESS.md` in the project root: phase, status, open issues, decisions made.
4. Never let placeholder data be replaced with invented numbers. Unknowns stay as `[TBD]`.
5. If Claude Code proposes something that conflicts with this brief, this brief wins unless the user approves the change.

### Claude Code (builder)
1. **Before writing any code, discover and use every relevant installed skill** (Section 1).
2. Work only on the phase you were given. At the end of each phase, report: files changed, skills used, what was verified, anything left as `[TBD]`.
3. Commit after each phase with a clear message (`phase 3: 3D car viewer`).
4. Run the build and fix all errors and warnings before reporting a phase as done.
5. Never invent prices, rent amounts, driver names, or insurance details. Use `[TBD]`.
6. Never use Ola or Uber logos. Text only.

---

## 1. Skills — discover and use ALL relevant ones

At the start of Phase 0, Claude Code must:

1. List every skill and plugin available in this environment (check the skills listing, `~/.claude/skills/`, project `.claude/skills/`, and installed plugins).
2. Write the list into `PROGRESS.md` with one line each: skill name → which phase(s) it will be used in, or "not relevant".
3. **Load and follow every skill that touches any of these areas**, before doing work in that area:
   - **UI / visual design** (e.g. `frontend-design`, theme, design-system, UI/UX skills) → Phases 1, 2, 5
   - **Motion / animation** (any animation, GSAP, Framer Motion, scroll, micro-interaction skills) → Phase 5
   - **3D / WebGL** (three.js, model-viewer, 3D skills) → Phase 3
   - **Website / web app building** (web-artifacts, landing page, Astro/Next/React, Tailwind skills) → Phases 1–2
   - **Images / media** (image optimization, asset pipeline skills) → Phase 4
   - **Forms / SEO / accessibility / performance** skills → Phases 6–7
   - **Testing / QA** (e.g. `webapp-testing`, Playwright, Lighthouse skills) → Phase 7
4. If a skill's guidance conflicts with this brief on **content, brand colors, or business facts**, this brief wins. On **craft** (layout quality, typography detail, animation technique, code quality), follow the skill.
5. If an important skill category has nothing installed, say so in `PROGRESS.md` and continue with best practices. Don't stop.

---

## 2. About the business

Driver Mitra Taxi runs a **rent-to-own car program for taxi drivers**. Its customers are drivers, not passengers.

- A driver pays a **₹10,000 booking amount**.
- The driver receives a **Maruti Suzuki Dzire Tour S**, the commercial taxi sedan. It's white.
- The driver pays a **daily rental**.
- The driver can **drive anywhere**: attached to Ola, Uber, any other platform, or independently.
- After completing a **3, 4 or 5-year flexible plan**, **the driver owns the car**.
- Members get **health insurance** and **education insurance** benefits for **themselves and their families**.

**Audience:** taxi and cab drivers in India. Most are on mobile phones, often on slow or expensive data. Many prefer simple language. Design for a 5-inch Android phone first.

**Primary goal of the site:** get drivers to **call**, **WhatsApp**, or **submit the enquiry form**. Every section should lead toward one of these.

---

## 3. Exact copy from the client's pamphlet (use this wording)

- DRIVER MITRA TAXI
- YOUR DRIVE • YOUR INCOME • YOUR CAR
- JUST PAY ₹10,000/- FOR YOUR CAR BOOKING
- TAKE A CAR & DRIVE ANYWHERE
- ATTACH ANYWHERE (OLA, UBER OR OTHER COMPANY)
- DRIVE AND OWN THE CAR
- NEW DZIRE TOUR S — DAILY RENTALS
- 3 YEARS FLEXIBLE PLAN / 4 YEARS FLEXIBLE PLAN / 5 YEARS FLEXIBLE PLAN
- BUY YOUR OWN CAR TODAY
- COMPANY BENEFITS: EDUCATION INSURANCE BENEFITS · HEALTH INSURANCE BENEFITS · FOR DRIVER AND HIS FAMILY
- JOIN DRIVER MITRA — GET ALL BENEFITS
- ATTACH ANYWHERE: OLA · UBER · OTHER COMPANY
- DRIVE MORE · EARN MORE · SECURE FUTURE
- CONTACT US: 8296611117 | 9060772111

The pamphlet image is at `reference/pamphlet.jpg`. Use it **only** as a reference for brand colors and energy. Do not copy its layout. Its car photo is a hatchback; the website must show the **sedan**.

---

## 4. Brand and visual direction

- **Colors** (define as design tokens / CSS variables):
  - Royal blue (primary): around `#0B3D91`, with a deeper shade for backgrounds and a lighter tint for surfaces
  - Taxi yellow (accent): around `#FFD400`
  - White, plus one near-black for text
  - Check all text/background pairs for WCAG AA contrast.
- **Typography:** a bold, condensed, uppercase display face for headings (e.g. Anton, Oswald, or Bebas Neue) and a clean, highly legible sans for body text (e.g. Inter or Poppins). Self-host or preload the fonts and use `font-display: swap`.
- **Signature motif:** the checkered taxi pattern (yellow/blue or yellow/black). Use it sparingly as dividers, section edges, and a transition wipe. Don't plaster it everywhere.
- **Feel:** energetic, confident, trustworthy, premium but not corporate. It should feel like a strong Indian mobility brand, not a generic template. Avoid stock "SaaS landing page" look: no generic gradient blobs, no Lorem-style filler, no emoji icons.
- **Icons:** one consistent line-icon set (e.g. Lucide or Phosphor). Pick one.

---

## 5. Site structure (single page, smooth scroll, sticky header)

1. **Sticky header:** text logo "DRIVER MITRA TAXI"; nav: How It Works, Our Car, Plans, Our Drivers, Benefits, Contact; a prominent yellow **Call Now** button. Collapses to a hamburger on mobile. Shrinks slightly and gains a solid background on scroll.
2. **Hero:**
   - Headline: "Just Pay ₹10,000 For Your Car Booking"
   - Subline: "Take a car, drive anywhere, and own it."
   - Tagline: "Your Drive • Your Income • Your Car"
   - CTAs: **Call Now** (`tel:`) and **WhatsApp Us**
   - Right side on desktop, below the text on mobile: the **interactive 3D car** (Section 6).
3. **Three key points** with icons: Take a Car & Drive Anywhere · Attach Anywhere (Ola, Uber or Other Company) · Drive and Own the Car.
4. **How It Works:** 4-step timeline:
   1. Pay ₹10,000 booking
   2. Get your Dzire Tour S
   3. Drive anywhere & pay daily rental
   4. Complete your plan & own the car
5. **Our Car: 3D showcase.** Heading "New Dzire Tour S — Daily Rentals". Large 3D viewer, plus a spec list with placeholders (fuel type, seating, mileage, boot space: `[TBD]`). Optional 3–4 hotspots on the model (e.g. "Spacious boot", "CNG option", "Comfortable rear seats") with `[TBD]` text.
6. **Plans:** heading "Buy Your Own Car Today". Three cards: 3 / 4 / 5 Years Flexible Plan, each showing "Daily rent: ₹[TBD]" and an **Enquire** button that scrolls to the form with that plan pre-selected. Highlight one card as "Most Popular `[TBD]`" only if the client confirms; leave a config flag for it.
7. **Our Drivers: handover gallery.** Heading "Happy Drivers, New Cars"; subline "Real drivers who received their car from Driver Mitra". A counter "`[TBD]`+ drivers on the road". Responsive grid (2 columns mobile, 3–4 desktop). Each item: photo, first name, city, plan, handover month/year, optional short quote. Click opens a lightbox with swipe and arrow navigation.
8. **Company Benefits:** Education Insurance Benefits · Health Insurance Benefits · For Driver and His Family. CTA "Join Driver Mitra — Get All Benefits".
9. **Attach Anywhere:** text-only badges "Ola", "Uber", "Other Companies". **No logos.**
10. **FAQ** accordion with placeholder answers (`[TBD]`):
    - Is the ₹10,000 refundable?
    - What documents do I need?
    - What does the daily rent include?
    - Who pays for maintenance and insurance?
    - When does the car transfer to my name?
    - Can I choose which app to work with?
11. **Enquiry form:** Name, Mobile (10-digit Indian validation), City, Preferred plan (3/4/5 years), "Do you have a commercial driving licence/badge?" (Yes/No), Message. On submit, open WhatsApp (`wa.me`) with the details pre-filled. Keep the submit logic in one module so a real backend or email service can be plugged in later. Show a clear success state.
12. **Contact + footer:** phones as `tel:` links (`+918296611117`, `+919060772111`), WhatsApp `[TBD]`, address `[TBD]`, email `[TBD]`, map embed placeholder `[TBD]`, copyright.

**Always visible on mobile:** a floating WhatsApp button, and a sticky bottom bar with **Call Now**. They must not cover the form's submit button or the footer links.

---

## 6. 3D car viewer

- Use **Google `<model-viewer>`**. It's the lightest way to get auto-rotate, drag-to-rotate, zoom, shadows and AR. Use three.js only if a specific effect needs it.
- **Model file:** `public/models/dzire-tour-s.glb` (white Maruti Suzuki Dzire Tour S sedan). If it's missing, use a free generic car GLB placeholder and log `[TBD: replace with Dzire Tour S model]` in `PROGRESS.md`. Don't block the build.
- **Behaviour:**
  - Slow auto-rotate (about 20–30°/sec). It pauses while the user interacts and resumes after about 3 seconds idle.
  - `camera-controls` on, `disable-pan`, sensible min/max zoom, soft contact shadow, neutral studio lighting.
  - A hint chip "Drag to rotate 360°" that fades after the first interaction.
  - Background is transparent over a subtle blue-to-light gradient "stage" with a faint road or floor reflection.
  - AR on supported phones (`ar`, `ar-modes="webxr scene-viewer quick-look"`) with a "View in your space" button.
- **Performance (critical):**
  - Show a poster image (`public/models/dzire-poster.webp`) instantly. Lazy-load the GLB only when the viewer is near the viewport.
  - Show a branded loading bar while it downloads.
  - Add an npm script using `gltf-transform` to compress the GLB (Draco or Meshopt + WebP/KTX2 textures). Target **under 3–5 MB**.
  - Fall back to the poster if WebGL is unavailable or loading fails.
  - With `prefers-reduced-motion`, disable auto-rotate and scroll-linked rotation.
- Give the viewer an accessible label: "3D model of the Maruti Suzuki Dzire Tour S. Drag to rotate."

---

## 7. Motion design

Use every installed motion/animation skill. Recommended stack: **GSAP + ScrollTrigger** for scroll choreography, with **Lenis** for smooth scrolling, or the equivalent the motion skills recommend. Motion must feel purposeful, fast and premium. Never slow down the user's path to Call or WhatsApp.

**Signature moments:**
1. **Page load:** a short checkered-flag wipe reveals the hero (under 800ms total). The headline animates in word by word. The "₹10,000" lands with a stamp/scale effect.
2. **Hero car:** gentle float plus auto-rotate. As the user scrolls from the hero into "Our Car", the camera orbit is **scroll-linked**, so the car turns to show its side, then rear.
3. **Road motif:** animated dashed road lines guide the eye down the How It Works timeline. Each step lights up as it enters the viewport.
4. **Counters:** "`[TBD]`+ drivers on the road" and the plan years count up when visible.
5. **Plan cards:** lift and subtle 3D tilt on hover (desktop only); a yellow glow ring on the focused/selected card.
6. **Gallery:** staggered reveal. On hover the photo zooms slightly and the caption slides up. The lightbox opens with a smooth shared-element style expand.
7. **Attach Anywhere:** a slow infinite marquee: "OLA • UBER • ANY APP • DRIVE ANYWHERE •".
8. **Micro-interactions:** button press states, Call button gentle pulse every few seconds (stops after interaction), form field focus animations, success checkmark animation on submit.

**Rules:**
- Animate only `transform` and `opacity`. No layout-thrashing animations.
- Respect `prefers-reduced-motion`: replace movement with simple fades or no animation.
- On low-end devices (`navigator.hardwareConcurrency <= 4` or Save-Data on), reduce motion intensity and skip scroll-linked 3D.
- No animation may delay content being readable for more than about 1 second.

---

## 8. Driver gallery and images

- Original driver photos go in `assets/drivers-original/`. An npm script (using `sharp`) outputs optimized versions to `public/drivers/`: WebP + AVIF, 3–4 widths for `srcset`, auto-rotated from EXIF, and **all EXIF/GPS metadata stripped** for privacy.
- Gallery data lives in the content file as a list: `{ image, name, city, plan, handoverDate, quote? }`. Adding a driver means dropping in a photo and adding one entry.
- Until real photos arrive, use neutral placeholders with `[TBD]` captions.
- Alt text pattern: "Ramesh from Bengaluru receiving his Dzire Tour S".
- README note: **only add photos of drivers who have given consent** to appear on the website.

---

## 9. Build phases (Antigravity: issue these one at a time)

### Phase 0: Setup and skill discovery
- Discover and list all skills (Section 1) in `PROGRESS.md`.
- Choose the stack. Recommended: **Astro + Tailwind CSS + GSAP + model-viewer** (static output, very fast, free hosting). Justify any deviation.
- Scaffold the project, with `BRIEF.md`, `CLAUDE.md`, `PROGRESS.md`, and git initialised.
- ✅ **Accept when:** dev server runs; skills list is written; stack decision is recorded.

### Phase 1: Design system and content
- Design tokens (colors, type scale, spacing, radii, shadows), fonts, icon set, checkered pattern component, button/card/badge components.
- One content file (e.g. `src/content/site.ts` or JSON) holding **all** copy, phone numbers, plans, FAQ and gallery entries, structured to support English / Hindi / Kannada later.
- ✅ **Accept when:** a `/styleguide` page shows all tokens and components; contrast passes AA; no copy is hard-coded in components.

### Phase 2: All sections (static, no heavy motion yet)
- Build sections 1–12 from Section 5, fully responsive.
- ✅ **Accept when:** screenshots at 360 / 768 / 1440 look polished with no overflow or horizontal scroll; all `tel:` and WhatsApp links work; the mobile sticky bar and floating button don't cover content.

### Phase 3: 3D car viewer
- Implement Section 6 completely, including poster, lazy load, loader, fallback, AR, and the compression script.
- ✅ **Accept when:** the car auto-rotates, can be dragged and zoomed, pauses and resumes correctly, and falls back to the poster with WebGL disabled; the GLB is under 5 MB or a `[TBD]` note explains why.

### Phase 4: Driver gallery
- Implement Section 8: image pipeline, grid, captions, lightbox, counter.
- ✅ **Accept when:** adding a photo plus one content entry shows a new card; the lightbox works with touch swipe and keyboard; output images have no EXIF.

### Phase 5: Motion
- Implement Section 7 using the motion skills.
- ✅ **Accept when:** all signature moments work; there's no jank on a throttled mid-range mobile profile; reduced-motion mode is calm and fully usable.

### Phase 6: Form, SEO and integrations
- Enquiry form with validation and WhatsApp hand-off; plan pre-select from plan cards.
- SEO: title, meta description, Open Graph and Twitter tags (car poster as `og:image`), `LocalBusiness` JSON-LD with `[TBD]` address, `sitemap.xml`, `robots.txt`, favicon set, `manifest.webmanifest`.
- ✅ **Accept when:** the form blocks bad numbers and opens WhatsApp with correct text; the structured data validates.

### Phase 7: QA and polish
- Use the testing skills (e.g. Playwright) to test: navigation, all CTAs, form, lightbox, 3D fallback, mobile menu.
- Lighthouse on mobile: target **Performance ≥ 85, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95**.
- Keyboard-only and screen-reader pass (labels, focus states, skip link).
- Final visual review at 360 / 768 / 1440 against Section 4.
- ✅ **Accept when:** targets are met or the reasons are documented; zero console errors.

### Phase 8: Handover
- `README.md` in plain language covering: how to run the site, edit content, change prices, add a driver photo, replace and compress the 3D model, and deploy to Netlify or Vercel.
- A `TBD.md` listing every remaining `[TBD]` and what's needed from the client.
- ✅ **Accept when:** a non-developer could follow the README to add a driver photo and redeploy.

---

## 10. Things that must stay `[TBD]` until the client confirms

Daily rent per plan · what the ₹10,000 covers and whether it's refundable · documents and eligibility · what daily rent includes (insurance, permit, maintenance) · insurance provider and coverage · cities served · office address · WhatsApp number · email · logo file · real car photos · the 3D model · driver photos and consent · domain name.

---

## 11. Hard rules (never break)

- No Ola or Uber logos. Text names only.
- No invented prices, rents, statistics, testimonials or driver names.
- The car shown is always the **Dzire Tour S sedan**, never a hatchback.
- Mobile first. Fast on slow 4G. Calls and WhatsApp reachable within one tap from anywhere on the page.
- Accessible: semantic HTML, alt text, focus states, AA contrast, reduced-motion support.
