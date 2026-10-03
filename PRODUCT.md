# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML + CSS + vanilla JS, no framework, no build step (`index.html`, `styles.css`, `main.js`, `assets/`). Published on GitHub Pages from `main` (`rodrigoapr01/gp-method`). Confirmed in the original brief.

## Product

GP METHOD is the online coaching program of Giorgia Piras, a personal trainer in Rome and founder of Weal House. It is sold in 6-week cycles (Assess, Build, Perform, Review) and works on three axes: Shape (muscle building and proportions), Strength (strength and progressions), Performance (running, conditioning, Hybrid/HYROX).

Positioning line, as given: "Non devi scegliere tra estetica e performance."

## Users

Two profiles, both confirmed by the client team (2026-10-04):

- Women who already train on their own and want a structured program: they fit **Essential** (personalized program, self-guided).
- Women who want to be followed by Giorgia: they fit **Coaching** (recommended) and **Elite** (limited places, the closest to 1:1).

Most arrive from Instagram (@lapiras93) on a phone. The page has to make three things clear within seconds: it is online coaching, there are three levels, and you start by writing on WhatsApp.

## Offer (fixed facts — do not change without the client)

| Level | Price | Badge | Primary action |
| --- | --- | --- | --- |
| Essential | €149 / 6 settimane | — | "Inizia con Essential" |
| Coaching | €249 / 6 settimane | Consigliato | "Scegli Coaching" |
| Elite | €399 / 6 settimane | Posti limitati | "Candidati a Elite" |

The detailed contents of each level are the lists in `index.html` ("Cosa include"). The scope note on nutrition ("nell'ambito delle competenze di un personal trainer") is a professional limit and must stay.

## Conversion

The only action is WhatsApp. One number, held in a single constant in `main.js`; each button sends a pre-filled message naming its level.

## Voice

Italian, second person singular, short and plain. No invented numbers, testimonials, results or promises. Internal notes (best seller, launch prices, retention) never go on the site. Copy changes need the client's approval.

## Assets

- Logo set in `assets/brand/` (circle, GP monogram, wordmark; SVG + PNG; mockup).
- One portrait of Giorgia (`assets/giorgia-src.png`, not committed). **Open:** the client will supply a better hero image; the hero is built so files can be swapped without code changes.

## Accessibility

WCAG 2.1 AA: contrast, visible focus, DOM order matching visual order on desktop, touch targets ≥ 44px, no motion under `prefers-reduced-motion`.

## Off-limits

Do not touch: `giorgia-piras` (lapiras.it, live), `giorgia-piras-v2`, `giorgia-piras-loghi`, `nuaestheticstudio`, any domain or DNS.
