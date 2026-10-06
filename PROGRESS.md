# PROGRESS — Driver Mitra Taxi

## Phase status

| Phase | Status | Notes |
|---|---|---|
| 0. Setup & skill discovery | ✅ Done (awaiting review) | Astro scaffolded, Tailwind wired, dev server runs, git initialised |
| 1. Design system & content | ✅ Done (awaiting review) | Tokens, fonts, Lucide, Checkered/Button/Card/Badge, `src/content/site.ts`, `/styleguide` |
| 2. All sections (static) | ⏳ Not started | |
| 3. 3D car viewer | ⏳ Not started | |
| 4. Driver gallery | ⏳ Not started | |
| 5. Motion | ⏳ Not started | |
| 6. Form, SEO, integrations | ⏳ Not started | |
| 7. QA & polish | ⏳ Not started | |
| 8. Handover | ⏳ Not started | |

## Decisions

### Stack (Phase 0) — as recommended by BRIEF §9, no deviation
- **Astro 7** (static output) — zero JS by default; only islands we opt into ship JS. Best fit for slow 4G / low-end Android.
- **Tailwind CSS v4** via `@tailwindcss/vite` — design tokens live as CSS variables in `src/styles/global.css` (`@theme`), no `tailwind.config.js` needed in v4.
- **GSAP + ScrollTrigger + Lenis** — added in Phase 5 (not installed yet; no deps "for later").
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

## Open issues
- `reference/pamphlet.jpg` is **missing** from the project. Needed in Phase 1 for brand color/energy reference.
- `[TBD: replace with Dzire Tour S model]` — `public/models/dzire-tour-s.glb` not provided yet (Phase 3).
- All BRIEF §10 items remain `[TBD]`.
