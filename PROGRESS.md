# PROGRESS — Driver Mitra Taxi

## Phase status

| Phase | Status | Notes |
|---|---|---|
| 0. Setup & skill discovery | ✅ Done (awaiting review) | Astro scaffolded, Tailwind wired, dev server runs, git initialised |
| 1. Design system & content | ✅ Done (awaiting review) | Tokens, fonts, Lucide, Checkered/Button/Card/Badge, `src/content/site.ts`, `/styleguide` |
| 2. All sections (static) | ✅ Done (awaiting review) | 12 sections in `src/components/sections/`; verified 360/768/1440 |
| 3. 3D car viewer | ✅ Done (awaiting review) | `<model-viewer>` in both car stages; CC0 placeholder sedan (13 KB GLB) — `[TBD: replace with Dzire Tour S model]` |
| 4. Driver gallery | ✅ Done (awaiting review) | `npm run drivers` (sharp → AVIF+WebP ×4 widths, EXIF/GPS stripped); grid + `<dialog>` lightbox; 4 neutral placeholders with `[TBD]` captions |
| 5. Motion | ✅ Done (awaiting review) | All 8 §7 moments; 3 motion tiers; no jank at 4× CPU throttle (p95 frame 11 ms, 0 long tasks); success checkmark deferred to Phase 6 |
| 6. Form, SEO, integrations | ✅ Done (awaiting review) | Form validation + wa.me hand-off + plan pre-select; full SEO head, LocalBusiness JSON-LD (schema.org validator: 0 errors, 0 warnings), sitemap, robots, favicon set, manifest |
| 7. QA & polish | ✅ Done (awaiting review) | Lighthouse mobile 96 / 100 / 100 / 100 (median of 3); Playwright pass on nav, CTAs, form, lightbox, 3D fallback, mobile menu; keyboard + SR pass; 0 console errors |
| 8. Handover | ⏳ Not started | |

## Decisions

### Stack (Phase 0) — as recommended by BRIEF §9, no deviation
- **Astro 7** (static output) — zero JS by default; only islands we opt into ship JS. Best fit for slow 4G / low-end Android.
- **Tailwind CSS v4** via `@tailwindcss/vite` — design tokens live as CSS variables in `src/styles/global.css` (`@theme`), no `tailwind.config.js` needed in v4.
- **GSAP + ScrollTrigger + Lenis** — added in Phase 5.
- **`@google/model-viewer`** — added in Phase 3, lazy-loaded.
- **`sharp`** (Phase 4 image pipeline), **`@gltf-transform/cli`** (Phase 3 GLB compression) — added in their phases.
- **Icons:** Lucide (decided now, installed in Phase 1).
- **No React/Framer Motion:** BRIEF §7 motion is fully covered by GSAP + CSS; adding React only for hover states would cost ~45 KB+ on every page. Global CLAUDE.md suggests Framer Motion/R3F/React Bits — BRIEF wins on stack (§0.5) and on performance (§11). Revisit only if the user asks.
- **Hosting:** static `dist/` → Netlify or Vercel (Phase 8).

### Environment
- `registry.npmjs.org` fails TLS handshake on this network (ISP filtering likely); GitHub works. Project `.npmrc` points npm at `https://registry.yarnpkg.com/` (official npm mirror). Global npm config untouched.

## Skills inventory (BRIEF §1)

Format: skill → phase(s) used, or "not relevant".

### UI / visual design
- `frontend-design:frontend-design` → Phases 1, 2, 5 (craft guidance: avoiding template look)
- `ui-pro-magic` → Phases 1, 2 (lock design system before components)
- `ui-ux-pro-max` (plugin: `ui-ux-pro-max`, `design-system`, `ui-styling`, `brand`, `design`) → Phase 1 (tokens, palette contrast, font pairing), Phase 2
- `ui-ux-pro-max: banner-design`, `slides` → not relevant
- `design-consultation` (gstack) → Phase 1 (optional cross-check of design system)
- `design-review` (gstack) → Phases 2, 7 (visual QA)
- `design-html`, `design-shotgun` → not relevant (we build directly in Astro)
- `gsd-ui-phase`, `gsd-ui-review`, `plan-design-review` → Phase 7 (optional audit); overlaps design-review — pick one per phase
- 21st.dev Magic MCP (`mcp__21st__*`, `magic`) → Phase 2 component inspiration only; outputs React, so ported to Astro. `magic` server failed to connect this session.

### Motion / animation
- No dedicated GSAP / Lenis / motion skill installed. → **Gap**: Phase 5 uses GSAP docs via Context7 + `frontend-design` motion guidance.

### 3D / WebGL
- No dedicated three.js / model-viewer skill installed. → **Gap**: Phase 3 uses model-viewer docs via Context7.
- Blender-MCP / TripoSR (global CLAUDE.md) → not relevant unless we must build a Dzire GLB ourselves; would need user approval.

### Website / web app building
- Context7 MCP (`mcp__context7__*`) → all phases (Astro, Tailwind v4, GSAP, model-viewer, sharp, gltf-transform docs)
- `run` → every phase (launch dev server / verify)
- `frontend-design` → Phases 1–2 (above)

### Images / media
- No dedicated image-optimization skill installed. → **Gap**: Phase 4 uses `sharp` docs via Context7.

### Forms / SEO / accessibility / performance
- `benchmark` (gstack, perf regression) → Phase 7
- `cso` / `security-review` / `insecure-defaults` (Trail of Bits) → Phase 6 (form → wa.me URL encoding, no secrets in client)
- No dedicated SEO or a11y skill installed. → **Gap**: Phase 6–7 use best practice + Lighthouse.

### Testing / QA
- Playwright MCP → Phase 7 (navigation, CTAs, form, lightbox, fallback). Failed to connect this session; retry later.
- Chrome DevTools MCP → Phases 3, 5, 7 (WebGL-disabled fallback, CPU throttling, console errors, Lighthouse). Failed to connect this session; retry later.
- `qa`, `qa-only` (gstack) → Phase 7
- `browse` / `browser-use` → not used for own-site QA (Playwright preferred per global CLAUDE.md)
- `superpowers: verification-before-completion` → every phase (build must pass before reporting done)
- `superpowers: test-driven-development` → Phase 6 (form validation + wa.me message builder only)
- `webapp-testing` → not installed (Playwright MCP covers it)

### Workflow / review / git
- `ponytail` → always on
- `commit-commands:commit` → end of every phase
- `review`, `code-review`, `simplify`, `pr-review-toolkit:*` → end of Phases 2, 5, 6, 7
- `superpowers: brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `requesting-code-review`, `receiving-code-review`, `finishing-a-development-branch`, `using-git-worktrees`, `systematic-debugging` → only if a phase is large enough / a bug is reported; Antigravity already sequences phases, so mostly not needed
- `document-generate`, `document-release` → Phase 8 (README, TBD.md)
- `make-pdf` → Phase 8 (optional printable handover)
- `ship`, `land-and-deploy`, `setup-deploy`, `canary` → Phase 8 only if user wants us to deploy
- `antigravity-plan`, `antigravity-review`, `antigravity-sync` → any phase, to sync with the orchestrator
- `task-observer` → end of session
- `gsd-*` (≈70 skills) → not relevant: overlaps with Antigravity's phase orchestration (global CLAUDE.md: don't stack GSD + GStack + Superpowers)
- `graphify`, `lean-ctx`, `claude-mem` (all its skills) → passive / not needed for a codebase this small
- `obsidian-second-brain` + its commands → not relevant
- `diagram` → not relevant

### Not relevant (other domains)
- Unity: `unity-kit` (21 skills), `unity-coding-skills` (10 skills)
- iOS: `ios-clean`, `ios-design-review`, `ios-fix`, `ios-qa`, `ios-sync`
- LSPs: `clangd`, `csharp`, `gopls`, `jdtls`, `kotlin`, `lua`, `php`, `pyright`, `ruby`, `rust-analyzer`, `swift` (`typescript-lsp` → passive, useful)
- `agent-sdk-dev`, `claude-api`, `mcp-server-dev`, `mcp-tunnels`, `plugin-dev`, `skill-creator`, `hookify`, `claude-code-setup`, `update-config`, `keybindings-help`, `fewer-permission-prompts`
- `code-modernization:*`, `claude-security` (full-repo scan; overkill for a static site), `variant-analysis`
- `cwc-makers`, `math-olympiad`, `playground`, `example-plugin`, `project-artifact`, `dataviz`
- `codex`, `benchmark-models`, `pair-agent`, `setup-gbrain`, `sync-gbrain`, `setup-browser-cookies`, `scrape`, `skillify`, `connect-chrome`, `open-gstack-browser`
- `office-hours`, `plan-ceo-review`, `plan-devex-review`, `devex-review`, `plan-tune`, `retro`, `health`, `learn`, `landing-report`
- `careful`, `guard`, `freeze`, `unfreeze`, `context-save`, `context-restore`, `investigate`, `loop`, `schedule`, `ralph-loop`
- `desktop-qa-automation`, Windows-MCP → not relevant
- Supabase / Sentry / Vercel MCPs → dormant (no backend). Vercel/Sentry need auth; Supabase failed to connect.

### MCP connection status this session
- Connected: context7, 21st, browser-use, claude.ai Docs, lean-ctx
- Failed to connect: playwright, chrome-devtools, magic, github, supabase (timeouts) — retry before Phase 3/7
- Needs auth: sentry, vercel

### Design system (Phase 1)
- **Colors** (`src/styles/global.css` `@theme`, Tailwind default palette disabled via `--color-*: initial`): royal `#0B3D91`, royal-deep `#072A66`, royal-tint `#E7EEFA`, taxi `#FFD400`, white, ink `#121826`, ink-muted `#4B5568`, mist `#C8D5EE` (muted text on blue).
- **Contrast:** 15 allowed text/background pairs, all ≥ 4.5:1 (lowest: ink-muted on royal-tint 6.43). `/styleguide` parses `global.css` and **throws at build** if any pair falls below AA. Taxi yellow on white (1.43:1) is never used for text.
- **Fonts:** Anton (display, uppercase) + Inter variable 400–700 via Astro's built-in Fonts API (fontsource provider): self-hosted, preloaded, `font-display: swap`, metric-matched fallbacks. No font npm packages. Hindi/Kannada will need Noto Sans Devanagari/Kannada when those locales land.
- **Icons:** `@lucide/astro` (tree-shaken per icon). Lucide has no brand icons, so WhatsApp uses `MessageCircle` (no logos, per §11).
- **Signature details:** badges styled as Indian commercial yellow number plates; `rounded-plate` 6px for buttons/badges vs `rounded-card` 1rem for containers; blue-tinted shadows; yellow focus ring on `data-surface="dark"`, royal on light.
- **Content:** `src/content/site.ts` — locale-independent data (phones, plans, `mostPopularPlan` flag, gallery) + `en` copy object typed as `Copy`; `hi`/`kn` must satisfy the same type. Strings that vary by word order are functions.
- `reference/pamphlet.jpg` still missing — Phase 1 used BRIEF §4 hex codes/descriptions instead.

### Sections (Phase 2)
- One component per section in `src/components/sections/`, assembled in `src/pages/index.astro`. All copy from `site.ts`.
- **Header:** fixed; transparent over hero, solid `royal-deep` + shrink after 8px scroll (tiny script). Mobile menu uses the native **Popover API** (Esc / outside-tap close for free); closes on link tap.
- **Mobile bar + WhatsApp button:** bar `< md` with Call Now; round WhatsApp button sits inside the bar's footprint (bar has right padding for it), floats bottom-right on `md+`. Footer bottom padding clears both. Automated check: no overlap with footer links or form submit at 360/768/1440.
- **WhatsApp links:** `whatsappHref()` in `site.ts`. While `contact.whatsapp` is `[TBD]`, links go to `https://wa.me/?text=…` (opens WhatsApp with the message; driver picks the contact). Setting the number in one place fixes every link.
- **Car placeholder:** `CarStage.astro` = brief's light gradient stage + an SVG line-art white sedan (three-box, not hatchback). Replaced by `<model-viewer>` in Phase 3.
- **FAQ:** native `<details name="faq">` (exclusive accordion, zero JS).
- **Form:** markup + native validation (`pattern="[6-9][0-9]{9}"`). WhatsApp hand-off, custom errors and plan pre-select (`data-plan` hooks already on Enquire buttons) are Phase 6.
- **Deferred by phase:** 3D viewer (3), image pipeline + lightbox (4), marquee/counters/all motion (5).
- Gotcha: `Button`/`Badge` merge caller classes after their own, but Tailwind resolves conflicting utilities by stylesheet order, not class order — wrap the component instead of overriding `display`/margins (hit on header Call Now `hidden`).

### 3D car viewer (Phase 3)
- **Component:** `src/components/CarStage.astro` (Hero with `eager`, and Our Car). Model + poster paths: `carModel` in `site.ts`.
- **Load order:** poster `<img>` renders instantly (hero: `fetchpriority=high`). The `model-viewer` JS (~285 KB gzip, includes three.js) is a lazy chunk, `import()`ed only when a stage is within 300px of the viewport **and** WebGL2 exists. Each viewer has `loading="lazy"`, so the Our Car one waits until visible. Poster fades out on `load`.
- **Fallback:** no WebGL2 → JS never downloads, poster stays. GLB/JS load error → `data-state="error"`, viewer removed, poster stays. Verified in Playwright (WebGL stubbed out; GLB routed to 404).
- **Behaviour = native model-viewer attributes:** `auto-rotate` 25°/s, pauses on interaction, resumes after `auto-rotate-delay=3000`; `camera-controls`, `disable-pan`, polar limits 40°–88° (no under-floor view), default zoom limits; `environment-image="neutral"`, `exposure=0.8` (white body washed out on the pale stage at 1.0), soft contact shadow. Measured: 801.6° → 826.8° in 1 s; frozen 2 s after a drag; rotating again ~3.5 s after.
- **Hint chip** "Drag to rotate 360°" shows once the model is ready, fades on the first `camera-change` with `source === 'user-interaction'`. model-viewer's hand prompt is off.
- **AR:** `ar ar-modes="webxr scene-viewer quick-look"` + "View in your space" button in the `ar-button` slot (model-viewer only shows it where AR can launch). iOS Quick Look uses model-viewer's auto-generated USDZ.
- **Reduced motion:** `auto-rotate` removed before model-viewer upgrades (verified). Scroll-linked rotation + low-end-device checks are Phase 5.
- **Loader:** royal progress bar (`role="progressbar"`, `aria-valuenow`) driven by model-viewer's `progress` event; hidden on ready/error.
- **Compression:** `npm run models:compress -- <in.glb> <out.glb>` = `gltf-transform optimize --compress draco --texture-compress webp --texture-size 2048`. Placeholder: 187 KB → 13 KB.
  - **Draco over Meshopt:** model-viewer 4.3 has a working Draco default (decoder from Google's gstatic CDN, fetched only for Draco files). Meshopt has no default decoder location, and setting one needs a script-tag hack. If a CSP/offline need appears: self-host `three/examples/jsm/libs/draco/gltf/` and set `dracoDecoderLocation`.
- **Build warning:** `chunkSizeWarningLimit: 1100` in `astro.config.mjs` — the only >500 KB chunk is the lazy model-viewer bundle (comment in config).
- **Placeholder model:** Kenney "Car Kit" `sedan.glb` (CC0, kenney.nl), fetched via GitHub mirror `Arslan12216775/kenney_car-kit` (kenney.nl TLS is blocked on this network). Body-paint swatches in its palette texture recoloured red → white with a one-off script (not kept). Uncompressed source: `assets/models/placeholder-sedan.glb`. Three-box sedan (not a hatchback, §11), but low-poly/toy-like.
- **Hotspots on the model:** skipped (optional in brief). Positions would be wrong on the placeholder; the Features list covers them. Add with the real model.
- **Swapping in the real Dzire Tour S:** source at `assets/models/dzire-tour-s.glb` → `npm run models:compress -- assets/models/dzire-tour-s.glb public/models/dzire-tour-s.glb` → set `carModel.src` → regenerate the poster: stage at 1200×900, in the console `el = document.querySelector('model-viewer'); el.removeAttribute('auto-rotate'); el.resetTurntableRotation()`, then save `await el.toBlob({ mimeType: 'image/webp', qualityArgument: 0.85 })` over `public/models/dzire-poster.webp`. Re-check exposure/framing.

### Driver gallery (Phase 4)
- **Pipeline:** `npm run drivers` = `scripts/drivers.mjs`. Every photo in `assets/drivers-original/` → `public/drivers/<name>-{320,640,960,1280}.{avif,webp}` (AVIF q50, WebP q75). `.rotate()` bakes in EXIF orientation; sharp drops all metadata by default, and the script **re-reads each output and throws if EXIF/XMP/IPTC is present**. `public/drivers/` is wiped and rebuilt each run so removed photos don't stay online. Widths live in `site.ts` (`driverPhotoWidths`) and are shared by the script (Node 24 type stripping imports `.ts` directly) and the component. `sharp` is now a direct devDependency (it was only transitive via Astro).
- **Privacy:** `assets/drivers-original/*` is gitignored (originals carry GPS); only stripped outputs are committed. Exception: `placeholder-*.jpg`, which are generated.
- **Placeholders:** 4 neutral brand-tint silhouettes (no text, so nothing to translate) with `[TBD]` captions and alt "Photo coming soon". Each placeholder original contains fake camera + GPS EXIF, and #2 is stored sideways with Orientation 6. Verified: outputs have no EXIF, no camera strings, and #2 comes out upright at 640×800.
- **Grid:** `<picture>` AVIF → WebP, `srcset` at 4 widths, `sizes` matched to the 2/4-column grid, lazy. Each card is a `<button>` whose name is the image alt. **Build fails with a clear message** if a `gallery` entry has no generated photo (forgot `npm run drivers`).
- **Lightbox:** native `<dialog>` + `showModal()` gives a focus trap, Esc to close, and focus return. It clones the grid's `<picture>` and caption (no duplicated data) with `sizes="100vw"`. ←/→ keys, prev/next buttons, wrap-around, one-finger swipe ≥50px (pinch ignored), tap on the empty area closes, page scroll locked while open, caption `aria-live`.
- **Verified (Playwright):** 360 touch: tap opens, swipe left/right navigates, Esc closes. 1440 keyboard: Enter opens, focus lands on Close, arrows wrap, Esc returns focus to the card. Adding a photo plus one `gallery` entry showed a 5th card with the correct alt/caption/quote (test reverted). No horizontal scroll, no page errors, `astro check` and build clean.
- **Deferred to Phase 5 (§7):** counter count-up, staggered reveal, hover zoom + caption slide-up, shared-element expand into the lightbox.

### Motion (Phase 5)
- **Skills:** no GSAP/Lenis/motion skill is installed (gap noted in Phase 0). Used Context7 (Lenis docs) and `frontend-design` craft guidance; checked GSAP/Lenis/model-viewer source where behaviour mattered.
- **Deps:** `gsap` 3.15 (core + ScrollTrigger, ~44 KB gzip) and `lenis` 1.3 (~5 KB gzip). Both are deferred module scripts and never block render.
- **Three tiers** in `html[data-motion]`, set by an inline `<head>` script before first paint (`Base.astro`):
  - `reduced` = `prefers-reduced-motion`: no movement at all. No wipe, words, float, auto-rotate, orbit, tilt, marquee, pulse, reveals or view transition. Counters show final values.
  - `lite` = `hardwareConcurrency <= 4` or Save-Data: CSS load moments, marquee, road dashes and reveals at smaller distances. No Lenis, float, tilt or scroll-linked 3D.
  - `full` = everything.
  - **QA override:** `?motion=full|lite|reduced`. DevTools CPU throttling doesn't change `hardwareConcurrency`, so throttled profiles still get `full` unless forced.
- **Structure:** `src/scripts/motion.ts` registers ScrollTrigger and exports `tier`, `onceVisible()` and `countUp()`. Lenis is created in `Base.astro` next to the ScrollTrigger import (one clock: `gsap.ticker` drives `lenis.raf`). Each section keeps its own `<script>`, as in earlier phases.
- **Load moments are pure CSS** (`global.css`): the checkered wipe (600 ms), the word-by-word headline and the ₹10,000 stamp. They run at first paint with no wait for JS, and the hero still shows if JS fails. Everything settles by **890 ms** (measured).
- **Scroll-linked orbit:** `CarStage orbit={[from, to]}`. Hero 0→90° (side), Our Car 90→180° (rear), scrubbed across each stage's pass through the viewport. model-viewer's auto-rotate turns the **scene yaw**, not the camera, so the scroll-driven `camera-orbit` stacks on top of it without fighting. Full tier only.
- **Lenis + anchors:** Lenis writes with `behavior: "instant"`, so CSS `scroll-behavior: smooth` stays for anchor links. Native fragment navigation keeps `scroll-padding-top` and the skip link's focus move, so Lenis's `anchors` option isn't used. Touch stays native (Lenis default). `prevent` skips `dialog` and `[popover]`.
- **Gotchas found in testing:**
  - (1) A ScrollTrigger with `once: true` **throws** in `refresh()` if the page loads already past its end, and a batch never fires `onEnter` if its whole range is jumped over. The symptom was a reload mid-page leaving the gallery at opacity 0. Fixed with `onceVisible()` (`end: 'max'`, one call per element), used for every reveal and counter.
  - (2) Pseudo-elements can't go inside `:is()`.
  - (3) Tailwind v4 `translate-*`/`scale-*` use the individual `translate`/`scale` properties, so `Button`'s `transition-[transform]` never animated its press state. Fixed. This is also why CSS hover lift and GSAP's tilt (`transform`) stack on plan cards.
- **Lightbox expand** uses the native View Transitions API (grid photo ↔ lightbox photo, 350 ms). Without the API, or in reduced motion, it just opens and closes. Esc, backdrop tap and Close all animate.
- **Call pulse** (hero, header, mobile bar): a `::after` ring every 4 s until the visitor's first tap, click or key press anywhere on the page.
- **Counters:** `driversOnRoad` is `[TBD]`, so that counter stays static. It counts up automatically once it's a number. The screen-reader text is a separate `sr-only` copy, so readers never hear "0+".
- **Verified (Playwright, built site):**
  - All moments at 1440. Reload mid-page and deep link `#contact` leave nothing hidden.
  - 360 mobile with touch, 4× CPU and slow 4G: FCP 1.0 s; scrolling the whole page gave p95 frame 11 ms, 0 frames > 50 ms, 0 long tasks.
  - Reduced: zero CSS animations, no Lenis, auto-rotate off, lightbox works.
  - Lite: no Lenis, float, tilt or orbit.
  - No horizontal scroll; no page errors; `astro check` and build clean.
- **Deferred:** the success checkmark animation belongs to the form success state, which Phase 6 builds.

### Form, SEO, integrations (Phase 6)
- **Skills:** no dedicated SEO/forms skill installed (gap noted in Phase 0). TDD for the form logic (`npm test`, Node's built-in `node:test`, no new deps). Security pass on the hand-off: user text only ever goes through `encodeURIComponent` into a `wa.me` query; JSON-LD escapes `<`; no secrets in the client.
- **Form logic:** `src/scripts/enquiry.ts` (no DOM): `parseMobile`, `validateEnquiry`, `enquiryMessage`, `submitEnquiry`. **To plug in a backend or email service, change `submitEnquiry()` only.** `Enquiry.astro` just wires it to the DOM.
- **Mobile rule:** strips spaces/dashes and a `+91` / `91` / `0` prefix, then requires 10 digits starting 6–9; also rejects one repeated digit (`9999999999`). `maxlength` removed so pasted `+91 98765 43210` isn't cut off. Without JS, native `required` + `pattern` still apply.
- **Errors:** custom messages from `t.form.errors`, shown under each field (`aria-invalid` + `aria-describedby`; groups described on the `<fieldset>`), focus moves to the first bad field, errors clear live once fixed. New token `danger` `#B3261E` (on white only), added to the styleguide AA check.
- **Hand-off:** `window.open(wa.me…)` in the submit handler (user gesture → not pop-up blocked). Success panel replaces the form: stamped checkmark (same keyframes as ₹10,000, off in reduced motion), focus on its heading, **Open WhatsApp again** (in case the pop-up was blocked or WhatsApp was closed) and **Edit my details** (values kept).
- **Plan pre-select:** any `[data-plan]` click (plan cards' Enquire) checks that plan in the form and re-shows the form if the success panel was up.
- **SEO head (`Base.astro`):** title, description, canonical, Open Graph (incl. image size/alt, `en_IN`), Twitter `summary_large_image`, theme-color, icons, manifest. `noindex` prop used by `/styleguide` (it gets no canonical and isn't in the sitemap).
- **og:image** `public/og-image.jpg` 1200×630 JPEG = car poster on the brand stage. JPEG, not the WebP poster, because every share preview (WhatsApp included) accepts it.
- **JSON-LD** `LocalBusiness` in `index.astro`, built from `site.ts`: name, description, slogan, url, image, telephone, both phones as `ContactPoint`s, `PostalAddress` with `streetAddress: [TBD]` + `addressCountry: IN`. Email is added automatically once it isn't `[TBD]`. Validated on validator.schema.org: 0 errors, 0 warnings. (Google's LocalBusiness rich result will want a real street/locality/postcode — `[TBD]`.)
- **sitemap.xml / robots.txt / manifest.webmanifest** are Astro endpoints (no `@astrojs/sitemap` dependency for a one-page site).
- **Domain `[TBD]`:** `site` in `astro.config.mjs` = `process.env.SITE_URL`, falling back to the reserved `https://drivermitrataxi.example`. Set `SITE_URL` in the host's build settings before going live, or canonical/OG/sitemap point at the placeholder.
- **Icons `[TBD: logo]`:** `npm run icons` (`scripts/icons.mjs`, sharp) writes favicon.svg, favicon.ico (PNG-in-ICO 32px), apple-touch-icon 180, icon-192/512, maskable-512 and og-image.jpg. Motif = checkered taxi tile on royal until the client's logo arrives. Re-run after regenerating the car poster.
- **Verified (Playwright, built site, 360px):** empty submit → 5 errors, focus on Name; `12345`, `5876543210`, `9999999999`, `98765432101` all blocked (nothing opened, error shown, `aria-invalid`); Enquire on the 4-year card → plan 4 checked; `+91 98765 43210` accepted; opened `https://wa.me/?text=…` decodes to the exact expected message; success panel shown and focused; Edit keeps values. No page errors, no horizontal scroll. `npm test` 4/4, `astro check` 0/0/0, build clean.

### QA & polish (Phase 7)
- **Skills/tools:** Playwright MCP (functional + keyboard runs), Lighthouse 12 CLI (Performance isn't in the DevTools MCP audit), `frontend-design` / BRIEF §4 for the visual review. No dedicated a11y/SEO skill (gap from Phase 0).
- **Lighthouse mobile** (built site, `astro preview`, default simulated slow 4G + 4× CPU, 3 runs): **Performance 96, Accessibility 100, Best Practices 100, SEO 100**. FCP 1.36 s, LCP 2.26 s, TBT ~175 ms, CLS 0, SI 1.4 s.
  - Before fixes: Performance 59–71 (TBT ~1.7 s, LCP up to 3.8 s), Accessibility 99.
- **Fix 1: model-viewer waits for the first interaction** (`CarStage.astro`). The ~285 KB three.js bundle used to load as soon as the hero was on screen, costing ~4 s of main-thread work at 4× CPU and delaying the poster's LCP paint. It now waits for the first `pointerdown/pointermove/touchstart/wheel/keydown/scroll` **and** proximity (the facade pattern). The poster is the same car, so nothing looks different. On a real visit the upgrade happens on the first scroll, touch or mouse move. Lighthouse never interacts, so its score shows the poster-only page (the honest first-load cost). Verified: no model-viewer/GLB request before input; after input the hero reaches `ready` and auto-rotates at 25°/s once `auto-rotate-delay` (3 s) passes.
- **Fix 2: heading order.** The key points were `h3` right after the hero `h1`. They are now `h2` with the same `text-h3` style.
- **Fix 3: skip link.** `<main id="main" tabindex="-1">`, so "Skip to main content" moves real focus (and the screen-reader cursor) to main, not just the sequential-focus start point.
- **Playwright functional (built site):** 360 touch: menu opens, link closes it and lands on `#plans`, Esc closes; every `#` anchor has a target; all `tel:` = `+918296611117` / `+919060772111`; WhatsApp links `wa.me`, `_blank` + `noopener`; Call + WhatsApp visible mid-page (sticky bar); plan 5 Enquire pre-selects plan 5; empty submit shows 4 errors, focus on Name; `12345` blocked with `aria-invalid`; `+91 98765 43210` opens WhatsApp with the expected text; success panel shown; no overlap between the sticky bar / WhatsApp button and the submit button or footer links; lightbox tap-open, real CDP swipe left/right, ←/→ with wrap, Esc close. No-WebGL: both posters visible, model-viewer/GLB never requested, 0 errors. GLB 404: `data-state="error"`, poster stays. No horizontal scroll.
- **Keyboard pass (360 + 1440):** skip link is the first stop, visible on focus, focuses `<main>`. Tab order follows reading order. Every stop has a visible ring (yellow on dark, royal on light) and scrolls into view. 3D viewer: focus ring + arrow keys rotate. Lightbox: focus trap, Esc returns focus. Form: labels on all fields, `+91` prefix in the mobile label, radio groups in `<fieldset>`/`<legend>`, errors linked by `aria-describedby`.
- **Screen-reader pass (accessibility tree):** landmarks banner / main / contentinfo / Main + Footer nav; one `h1`, no skipped levels; icon-only buttons (menu, close, prev/next, floating WhatsApp) all named; decorative icons, the marquee and the hint chip `aria-hidden`; counter reads "[TBD]+ drivers on the road", never "0+".
- **Visual review vs §4 at 360 / 768 / 1440:** royal/taxi/white/ink tokens only, Anton + Inter, checkered motif only at the hero edge, timeline road and footer edge, Lucide line icons throughout, no logos, no gradient blobs. No overflow; 360 first screen shows the headline, ₹10,000 stamp, both CTAs and the sticky Call/WhatsApp bar. The `₹` fallback glyph sits fine next to Anton; no change needed.
- **Console:** 0 errors and 0 warnings on load at every width and tier. model-viewer 4.3.1 (latest) still prints debug `console.log`s (`[$updateSource] called!`, `IntersectionObserver fired!`). They now appear only after the first interaction. Not errors. Removing them would need a custom build plugin, and dropping all console output would also hide real errors, so they stay until upstream removes them.
- **Not automated:** no committed Playwright suite (would add `@playwright/test`, ~100 MB of browsers, for a one-page site). Scenarios above are reproducible via the Playwright MCP. AR still needs a real phone.

## Open issues
- `reference/pamphlet.jpg` is **missing** from the project. Needed in Phase 1 for brand color/energy reference.
- **`[TBD: replace with Dzire Tour S model]`** — `public/models/dzire-tour-s.glb` not provided. The site uses a CC0 low-poly white sedan placeholder (`public/models/placeholder-sedan.glb`, 13 KB) and a poster rendered from it. Needed from client: a white Dzire Tour S GLB (or approval to buy a licensed one). Swap steps under "3D car viewer (Phase 3)".
- AR ("View in your space") untested on a real Android/iOS phone — Phase 7 device check.
- All BRIEF §10 items remain `[TBD]`.
- **Domain `[TBD]`**: set `SITE_URL` on the host. **Logo `[TBD]`**: replace the checkered icon via `scripts/icons.mjs`. **Address `[TBD]`**: JSON-LD needs street, locality, postcode for Google's local rich result.
- **Driver photos + consent `[TBD]`**: the gallery shows 4 neutral placeholders. `driversOnRoad` count `[TBD]`. Alt text pattern says "his" (BRIEF §8). Make it gender-aware if any driver is not male.
- **WhatsApp number `[TBD]`**: is 8296611117 or 9060772111 on WhatsApp? Until confirmed, WhatsApp buttons open WhatsApp without a pre-set recipient.
- model-viewer 4.3.1 debug `console.log`s: logs, not errors, only after first interaction (Phase 7). Drop when upstream releases a clean version.
- `₹` glyph is not in Anton's latin subset; renders from the fallback font. Reviewed in Phase 7: looks fine.
