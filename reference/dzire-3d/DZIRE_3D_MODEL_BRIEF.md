# Dzire 3D Model — Build Brief for Claude Code

> **Goal:** produce `public/models/dzire-tour-s.glb`, a clean, web-ready 3D model of the **white 4th-generation Maruti Suzuki Dzire** (the car Driver Mitra gives its drivers). It's shown in the auto-rotating 360° viewer on the Driver Mitra Taxi website (see `BRIEF.md` Section 6).
>
> **Where this pack lives:** the user downloads it as `dzire-3d-reference-pack.zip` into their **Downloads** folder (Windows: `%USERPROFILE%\Downloads\`, macOS/Linux: `~/Downloads/`). Extract it into the project at `reference/dzire-3d/`, without an extra nested folder. All paths below are relative to `reference/dzire-3d/`. If the zip isn't in Downloads, ask the user where it is before continuing.
>
> **Read every file in this pack before you start:**
> - `photos/` — 9 real photos of the exact car, taken at the dealership. **These are the primary reference.** Where photos and brochure disagree, the photos win.
> - `brochure/dzire-4th-gen-brochure.pdf` — official Maruti Suzuki brochure. Use it for **dimensions, specs, and close-up details** (tail lamp, wheel, roof). Its red car is a top variant (alloys, LED lamps, sunroof). **Do not copy those parts.**
> - `brochure/dzire-4th-gen-brochure-text.txt` — the brochure text, already extracted.
> - `specs.json` — the measurements and colors below, in machine-readable form.

---

## 1. What car exactly

- **Model:** Maruti Suzuki Dzire, 4th generation (launched November 2024), 4-door compact sedan, right-hand drive (India).
- **Trim seen in the photos:** a mid/base variant (it looks like **VXI-level** trim). Evidence: R14 steel wheels with full wheel covers, halogen projector headlamps with no LED DRL strip, body-coloured door handles and mirrors, no fog lamps, no sunroof, a 7-inch (17.78 cm) touchscreen inside. Driver Mitra's commercial Tour S cars are fleet versions of this car, so **model the car in the photos, not the brochure's top variant.**
- **Colour:** **Arctic White**, a solid (non-metallic) white with a glossy clear coat. The whole body is white; trims are gloss/matte black as listed below.

### Do NOT include (top-variant features from the brochure)
Electric sunroof · two-tone or precision-cut alloy wheels · LED "Crystal Vision" headlamps · Sleek Line LED DRL strip · LED fog lamps · chrome belt-line garnish · auto-fold mirror indicators · 360° cameras.

---

## 2. Real dimensions (build to these, in metres, 1 unit = 1 m)

| Item | Value | Source |
|---|---|---|
| Overall length | **3.995 m** | Brochure |
| Overall width (body, excl. mirrors) | **1.735 m** | Brochure |
| Overall height (incl. shark fin) | **1.525 m** | Brochure |
| Wheelbase | **2.450 m** | Brochure |
| Ground clearance (unladen) | **0.163 m** | Brochure |
| Tyre | **165/80 R14** → outer diameter ≈ **0.620 m**, width ≈ **0.165 m** | Brochure + calculation |
| Wheel rim | 14 in (≈ 0.356 m) steel, covered by a full wheel cover | Brochure + photos |
| Front / rear track | ≈ **1.52 m** each | **Estimate**: not in brochure; tune so tyres sit flush with arches in photos 05/06 |
| Front overhang | ≈ **0.73 m** | **Estimate** from photo 03/04 proportions |
| Rear overhang | ≈ **0.82 m** | **Estimate** from photo 03/04 proportions (length − wheelbase − front overhang) |

Origin: put (0,0,0) on the ground, centred under the car's midpoint. Car faces **+Z** (glTF forward), Y up. Wheels touch Y = 0.

---

## 3. Component-by-component breakdown

Each part below names the photo(s) where it's best visible. Model each as a **separate, named mesh/object** (names in `code font`). This lets the website animate or highlight parts later.

### 3.1 Overall body shape — `Body`
- Compact three-box sedan. A short, steep **hood**, a **fast-raked windscreen**, a smoothly arched **roofline** that flows into a **short, upright boot**. *(03, 04)*
- **Shoulder character line:** a crisp crease runs from the top of the headlamp, along both doors, just under the window line, and ends at the top of the tail lamp. *(03, 04)*
- **Lower door crease:** a softer second line about 15–20 cm above the sill, rising slightly toward the rear. *(03, 04)*
- **Wheel arches:** body-coloured, gently flared, no black cladding. *(03, 04)*
- **Sills:** body-coloured, plain. *(03, 04)*
- **Fuel lid:** small rounded-square flap on the **left rear quarter panel**, just behind the rear door. *(04)*
- **Panel gaps:** shallow dark grooves for hood, 4 doors, boot lid, and fuel lid. Do this with bevelled cuts or normal-map lines, not real gaps.
- Material: `Paint_ArcticWhite`.

### 3.2 Front — `Front_*`  *(05, 06, 07, 08, 02)*
- **Front fascia is wide and flat-faced.** Headlamps and grille read as one continuous dark horizontal band across the full width.
- `Front_UpperBar`: a **gloss-black horizontal bar** joining both headlamps across the full width, directly under the hood edge. A **thin red accent line** runs along its lower edge, between the two headlamps. *(06, 09: clearly visible)*
- `Front_Logo`: a chrome emblem centred on the upper bar. **Keep it a generic chrome badge shape (see Section 6).**
- `Front_Grille`: a large **trapezoid gloss-black lower grille**, wider at the bottom, with **4–5 thick horizontal slats** and a dark mesh behind. It takes up most of the bumper height. *(05, 08)*
- `Front_Plate`: white number plate centred on the grille. **Text: "DRIVER MITRA"** (see Section 6).
- `Headlamp_L` / `Headlamp_R`: **swept-back, slim, angular** units that wrap into the fenders. Inside each: a **round projector lens** on the outer side, plus an amber/clear reflector section on the inner side. Use a smoked clear outer lens. *(06, 07: lit)*
- `Front_CornerInserts`: **black boomerang/triangle-shaped inserts** at the lower outer corners of the bumper. There are no fog lamps; they're plain black. *(05, 08)*
- `Front_Bumper`: body-coloured, with a slim lip at the bottom and parking sensor dots optional.
- **Hood:** clamshell-style. The shut line sits just above the black upper bar. Two subtle creases converge toward the logo. *(05)*

### 3.3 Side — `Side_*`  *(03, 04, 02)*
- `Glass_Side`: 4 side windows plus a small fixed **rear quarter glass** in the C-pillar. The window line rises slightly toward the rear.
- `Pillars_Black`: **B-pillar is gloss black.** The A and C pillars are body-coloured; the C-pillar has a black window surround. *(03, 04)*
- `Window_Trim`: the beltline trim under the windows is **black** (not chrome on this trim).
- `Door_Handles`: 4 **body-coloured pull handles**, set into the shoulder line. *(03, 04)*
- `Mirror_L` / `Mirror_R`: **body-coloured** mirror caps on black triangular bases mounted on the doors. *(02, 03, 04)*
- **Doors:** 4 doors. The front door is longer than the rear door. The rear door has a curved cutout around the rear wheel arch.

### 3.4 Wheels and tyres — `Wheel_FL`, `Wheel_FR`, `Wheel_RL`, `Wheel_RR`  *(03, 04)*
- **Each wheel is a separate object with its pivot at the hub centre**, so the website can spin them.
- **Tyre:** black rubber, 165/80 R14. Sidewall text may be faint embossed noise; no brand names.
- **Wheel cover:** **silver-grey plastic full wheel cover** with **about 10 twisted/curved spokes** in a turbine pattern and a small dark centre cap. *(03, 04: clearly visible)*
- Brake disc visible behind the front wheels; drum at the rear (hidden by covers, so low detail is fine).

### 3.5 Roof — `Roof_*`  *(01, 03, 04)*
- **Solid white roof, no sunroof.**
- `Roof_SharkFin`: a small **white shark-fin antenna** at the rear of the roof. *(01: clearly visible)*
- No roof rails.

### 3.6 Rear — `Rear_*`  *(01; tail lamp close-up on brochure page 2)*
- `TailLamp_L` / `TailLamp_R`: **wrap-around tail lamps** with a **smoked dark-red lens**. Inside: the **"3D Trinity" signature of three stacked horizontal light bars**, slightly angled. Make it emissive red so it glows on the website.
- `Rear_Garnish`: a **gloss-black horizontal bar across the boot lid** connecting the two tail lamps, with a **thin chrome strip** along its edge. *(01)*
- `Rear_Spoiler`: the **aero boot lip spoiler**, a small lip integrated into the top edge of the boot lid. *(01)*
- `Rear_Badges`: a model-name script on the left of the boot and a centred logo above the garnish. **Make both generic (see Section 6).**
- `Rear_Plate`: number plate recess in the boot lid, below the garnish, with a white plate reading **"DRIVER MITRA"**.
- `Rear_Bumper`: body-coloured, with a **horizontal crease and lower diffuser-style line**, plus **4 small reverse-parking sensor dots**. *(01)*
- `Glass_Rear`: rear windscreen with a few thin **defogger lines** and an **LED high-mount stop lamp** at its top edge.

### 3.7 Glass — `Glass_Front`, `Glass_Rear`, `Glass_Side`
- Tinted dark glass, glossy, **partly transparent** so a simple interior is faintly visible.
- Two black **wiper arms** at the bottom of the windscreen. *(05, 08)*

### 3.8 Interior (simplified, low-poly) — `Interior_*`  *(09)*
Seen only through glass, so keep it light:
- **Dual-tone dashboard:** black upper and **beige lower** section, with a satin-silver strip between them.
- A **freestanding 7-inch touchscreen** at the top centre of the dash.
- A **3-spoke black steering wheel** on the **right side (RHD)**.
- **Beige fabric seats:** 2 front seats and a rear bench, with headrests.
- A 5-speed manual gear lever.
- Black floor and door trims with beige inserts.

---

## 4. Materials (PBR, metallic-roughness for glTF)

| Material | Base colour | Metallic | Roughness | Notes |
|---|---|---|---|---|
| `Paint_ArcticWhite` | `#F2F3F0` | 0.0 | 0.25 | Add **clearcoat 1.0, clearcoat roughness 0.05** (KHR_materials_clearcoat). Solid white; **not** metallic or pearl. |
| `Plastic_GlossBlack` | `#0A0A0B` | 0.0 | 0.15 | Upper bar, garnish, B-pillar |
| `Plastic_MatteBlack` | `#151517` | 0.0 | 0.7 | Grille slats, inserts, mirror bases, wiper arms |
| `Chrome` | `#E8E8E8` | 1.0 | 0.08 | Badges, garnish strip |
| `Accent_Red` | `#B5121B` | 0.0 | 0.3 | Thin front grille line |
| `Glass_Tinted` | `#1A2228`, alpha 0.35 | 0.0 | 0.05 | Use KHR_materials_transmission if available; otherwise alpha blend |
| `Lens_Headlamp` | `#FFFFFF`, alpha 0.2 | 0.0 | 0.02 | Clear outer cover |
| `Lamp_Projector` | `#D8DDE3` | 1.0 | 0.1 | Projector bowl |
| `TailLamp_Lens` | `#3A0508`, alpha 0.6 | 0.0 | 0.1 | Smoked red |
| `TailLamp_Emissive` | `#FF1A1A`, emissive strength 2–3 | 0.0 | 0.4 | Trinity light bars |
| `WheelCover_Silver` | `#9EA3A8` | 0.3 | 0.45 | Turbine-spoke cover |
| `Tyre_Rubber` | `#1B1B1B` | 0.0 | 0.9 | |
| `Interior_Black` / `Interior_Beige` | `#1E1E1E` / `#CFC3AE` | 0.0 | 0.8 | Low detail |
| `Plate_White` | `#FFFFFF` + black text | 0.0 | 0.5 | "DRIVER MITRA" |

---

## 5. How to build it (process for Claude Code)

A realistic car can't be generated in one shot. Build it step by step and **check against the photos after every step.**

1. **Tooling:** use **Blender driven by Python** (`pip install bpy` for headless Blender, or the Blender CLI `blender -b -P build_car.py`). Write the whole model as a **reproducible script** at `tools/model/build_car.py`, so any change is just a re-run. If Blender can't be installed, fall back to procedural three.js geometry exported with `GLTFExporter`, and say so in `PROGRESS.md`.
2. **Blueprint first:** use photos `03-side-profile-right.jpg` and `05-front-straight-lights-off.jpg` as background reference planes, scaled so the wheelbase in photo 03 measures exactly 2.450 m. Trace the side silhouette, roofline, window line, and wheel-arch positions.
3. **Block-out:** build the main body from a low-poly cage using subdivision surface + edge creases for the shoulder line and the panel edges. Then cut in the window openings. Check proportions against **Section 2**.
4. **Add parts** in this order: wheels → glass → front fascia → headlamps → rear lamps + garnish → mirrors + handles → roof fin → interior → badges/plates.
5. **Compare after each step:** render the model from the **same camera angles as photos 01, 02, 03, 04 and 05** (same height, same perspective) and put each render **side by side with its photo** in `tools/model/compare/`. Fix any proportion that is visibly off before moving on. **Do at least 3 compare-and-fix rounds.**
6. **Apply all modifiers**, triangulate cleanly, and check normals point outward. Merge parts that will never move separately, but **keep each wheel, both headlamps, both tail lamps, and the glass separate**.
7. **Export** `public/models/dzire-tour-s.glb` (glTF 2.0 binary, +Y up), then optimise with `gltf-transform`:
   `npx @gltf-transform/cli optimize in.glb public/models/dzire-tour-s.glb --compress draco --texture-compress webp`
8. **Poster image:** render a clean **front-left three-quarter view** (like photo 02) on a transparent background at 1600×1000 and save it as `public/models/dzire-poster.webp`. The website shows it while the 3D model loads.

### Targets
- **Triangles:** 60k–120k total (smooth enough on desktop, still light for budget phones).
- **File size:** **under 3 MB** after compression (5 MB hard limit).
- **Textures:** 1024 px max, WebP. Prefer flat colours + normal maps over big textures.
- Loads and renders correctly in `<model-viewer>`, in three.js, and in Google's online glTF viewer. Zero validator errors (`npx gltf-validator`).

---

## 6. Branding and legal rules

- **Number plates read "DRIVER MITRA"** (black text on white), front and rear. This brands the car for the client.
- **Don't recreate the Suzuki "S" logo or the "DZIRE" wordmark exactly.** They're Maruti Suzuki trademarks. Use a **generic chrome oval/badge shape** in their place. Mentioning "Maruti Suzuki Dzire" in website text is fine.
- **Don't use the brochure images on the website.** They're Maruti Suzuki's copyrighted marketing material, for modelling reference only.
- Photo `01-rear-three-quarter-left.jpg` shows a dealership staff member in the background. **Don't publish that photo as-is** anywhere on the site.

---

## 7. Gaps in the reference (use the brochure or best judgement, and note it)

The photos don't show:
- **A straight-on rear view:** use photo 01 plus brochure page 2 (tail lamp close-up, rear three-quarter).
- **A top view:** use brochure pages 1–2, **minus the sunroof** (the roof here is solid white).
- **A close-up of the wheel cover:** use photos 03/04.

List every assumption you make in `PROGRESS.md` under "3D model assumptions", so they can be checked against new photos later.

---

## 8. Acceptance checklist

- [ ] Dimensions match Section 2 within ±2 %.
- [ ] Side-by-side renders vs photos 01–05 look like **the same car**: same stance, fascia, window shape, wheel position.
- [ ] Body is **Arctic White** gloss; black trims, red grille line, smoked tail lamps all correct.
- [ ] **No** sunroof, alloys, LED DRLs or fog lamps.
- [ ] Number plates read **DRIVER MITRA**; no exact Suzuki/Dzire logos.
- [ ] 4 wheels are separate objects that spin about their hub axis.
- [ ] GLB is under 3 MB, has 0 validator errors, and loads in `<model-viewer>` with auto-rotate.
- [ ] `dzire-poster.webp` exported.
- [ ] `tools/model/build_car.py` regenerates the model from scratch with one command.
