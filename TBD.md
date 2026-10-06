# Still to confirm: what we need from Driver Mitra

The site is built, but the items below show as **[TBD]** (or as a placeholder) until the business gives us the real information. We won't guess any of these.

Once you have an answer, most items are a single text change in `src/content/site.ts`. The README explains how ([section 3](README.md#3-change-words-phone-numbers-and-other-details)). Items marked 🛠 need a small developer task as well.

## 1. Must-have before going live

| # | What's needed | Where it shows on the site | Where to put it |
|---|---|---|---|
| 1 | **Daily rent for each plan** (3, 4 and 5 years) | Plans section: "Daily rent: ₹[TBD]" | `plans` → `dailyRent` ([README §4](README.md#4-change-prices-daily-rent)) |
| 2 | **WhatsApp number**: is it 8296611117, 9060772111, or a different one? | Every WhatsApp button, the enquiry form, Contact section. Until it's set, WhatsApp opens without a contact chosen, so the driver has to pick one. | `contact.whatsapp`, e.g. `'918296611117'` |
| 3 | **Is the ₹10,000 refundable, and what does it cover?** | FAQ: "Is the ₹10,000 refundable?" | `faq` → 1st answer |
| 4 | **Documents and eligibility** (licence, badge, ID, address proof, age, experience…) | FAQ: "What documents do I need?" | `faq` → 2nd answer |
| 5 | **What the daily rent includes** (insurance, permit, maintenance?) | FAQ: "What does the daily rent include?" | `faq` → 3rd answer |
| 6 | **Who pays for maintenance and insurance**, plus the insurance provider and what it covers | FAQ: "Who pays for maintenance and insurance?" | `faq` → 4th answer |
| 7 | **When the car is transferred to the driver's name** | FAQ: "When does the car transfer to my name?" | `faq` → 5th answer |
| 8 | **Can drivers choose any app (Ola, Uber, others)?** Please confirm the exact wording. | FAQ: "Can I choose which app to work with?" | `faq` → 6th answer |
| 9 | **Domain name** (e.g. drivermitrataxi.in): please buy it, or tell us which one you own | Google results, WhatsApp/Facebook link previews, sitemap. Until it's set they point at a placeholder address. | Set `SITE_URL` on Netlify/Vercel ([README §7](README.md#7-put-the-site-online-netlify-or-vercel)) |

## 2. Contact details

| # | What's needed | Where it shows | Where to put it |
|---|---|---|---|
| 10 | **Office address** (street, area, city, PIN code) | Contact section. Google also needs it to show the business on Maps/local search. | `contact.address` |
| 11 | **Email address** | Contact section, Google business info | `contact.email` |
| 12 | 🛠 **Google Maps location** (a Maps share link to the office) | Contact section: a "Map coming soon" box for now | A developer adds the map embed (about 10 minutes) once the address is final |
| 13 | **Cities served** | Not on the site yet. Please list them; we'll add them to the page and to Google's business info. | 🛠 Developer adds |

## 3. Photos, logo and the 3D car

| # | What's needed | Where it shows | How |
|---|---|---|---|
| 14 | **Driver handover photos, each with the driver's consent**, plus each driver's name, city, plan and handover month | "Happy Drivers, New Cars" gallery: four grey placeholders for now | [README §5](README.md#5-add-a-driver-photo). Only drivers who have agreed to appear. |
| 15 | **Number of drivers on the road** (a real count) | "[TBD]+ drivers on the road" | `driversOnRoad`, e.g. `'250'` |
| 16 | **Are all drivers in the photos men?** The photo description for blind users currently says "receiving **his** Dzire Tour S". | Hidden image descriptions in the gallery | 🛠 If any driver isn't a man, a developer makes the wording neutral (one line) |
| 17 | **3D model of the white Dzire Tour S sedan** (`.glb` file), or approval to buy a licensed one | Hero and "Our Car" section: a simple stand-in sedan for now | [README §6](README.md#6-replace-the-3d-car-model) |
| 18 | **Real photos of the car** | The still image visitors see before the 3D car loads, and the link preview on WhatsApp/Facebook. Both are rendered from the stand-in model now. | Comes from the real 3D model (item 17); [README §6](README.md#6-replace-the-3d-car-model), step 5 |
| 19 | **Car specifications**: fuel type, seating, mileage, boot space | "Our Car" → Specifications | `car` → `specs` |
| 20 | **Feature details**: spacious boot, CNG option, rear seats | "Our Car" → Features | `car` → `hotspots` → `detail` |
| 21 | 🛠 **Logo file** (SVG or large PNG) | Browser tab icon, phone home-screen icon, link previews. A checkered taxi pattern is used for now. | A developer updates `scripts/icons.mjs` and runs `npm run icons` |

## 4. Optional

| # | What's needed | Where it shows | Where to put it |
|---|---|---|---|
| 22 | **Which plan to mark "Most Popular"** (3, 4 or 5 years) | Yellow badge on that plan card. No badge is shown until you choose. | `mostPopularPlan` ([README §4](README.md#4-change-prices-daily-rent)) |
| 23 | 🛠 **Hindi and Kannada text** | Site is English-only for now. It's already set up for both languages. | Translations needed, then a developer adds them (`hi` / `kn` in `site.ts`, plus fonts) |

---

**For developers:** every `[TBD]` value comes from the `TBD` constant in `src/content/site.ts`. The other markers are `// [TBD: domain]` in `astro.config.mjs` and `// [TBD: logo]` in `scripts/icons.mjs`. The styleguide page (`src/pages/styleguide.astro`) also shows a `[TBD]` badge, but that page is for design reference only. To re-audit, run `grep -rn "TBD" src scripts astro.config.mjs`.
