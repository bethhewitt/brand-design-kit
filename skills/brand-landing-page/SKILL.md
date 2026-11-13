---
name: brand-landing-page
description: Use when asked for an on-brand landing page, campaign page, product or feature page, waitlist or pre-launch page, event page, or marketing web page for the brand in the current repository.
---

# Brand landing page

A landing page exists to get one action from one audience. Every section
either moves the reader toward that action or removes a reason not to take
it.

**First:** run `brand-preflight` (the DESIGN.md check) if it hasn't run in
this task. Then read `../brand-design/SKILL.md` and complete core steps 1–3.
Paths below are relative to `../brand-design/`.

## Step 2 — ask every time

**Output** (single choice):
- Single self-contained HTML file (CSS inline, easy to host or hand over)
- HTML plus review screenshots (desktop 1440 and mobile 390 full-page PNGs)
- Built into this repo's web app, using its existing framework, components
  and styles. Only offer this when the repo is a web app. Inspect its routes
  and components first and follow its conventions instead of the seed.

**Content to request if missing:** the single conversion goal (sign up,
book a demo, buy, download, join the waitlist) plus a real destination URL
or form endpoint; the audience; the offer; available proof (customer
quotes, logos, numbers with sources); and must-have sections.

## Structure

Above the fold must answer **what it is, who it's for, why it matters, and
what to do**: an optional sentence-case label (never an all-caps eyebrow), a headline of 12 words or fewer, one supporting
sentence, the primary CTA, and a real product or brand visual.

Then choose 3–5 sections from `assets/layouts.md` (Layouts 2–8). Start from
a rhythm and change at least one section so the page doesn't read as the
stock "hero → features → pricing → FAQ → CTA" template:

- Features → stat row or quote → split detail → CTA strip (default)
- Problem statement → how it works (numbered steps) → proof → CTA
- Waitlist: hero with inline email capture → 3 reasons → closing capture

Conversion rules (from the Laws of UX):
- **One primary action**, repeated at the top, middle and end with the same
  label. Secondary actions are visually quieter. (Von Restorff, Hick)
- Keep plan/option counts to 3 or fewer per row. (Choice overload)
- CTAs and controls are at least 44×44px with generous spacing. (Fitts)
- Proof sits next to the claim it supports. (Proximity)

## Build

- Copy `assets/web-seed.html`, replace its first `:root` with the brand block,
  and paste sections from `assets/layouts.md`. Use only classes defined in the
  seed. Use inline styles for one-offs.
- Real links only. If there is no destination, remove the CTA rather than
  pointing at `#`.
- Forms: labelled inputs, a visible focus state, a clear success and error
  message, and the form `action` set to the user's endpoint or left
  clearly marked for wiring.
- Semantic landmarks (`header`, `main`, `footer`), one `h1`, alt text on
  every meaningful image, and `prefers-reduced-motion` respected for any
  motion.
- Meta: `<title>`, meta description, and Open Graph title, description and
  image (use a social graphic from `brand-social-post` if one exists).

Craft files: `typography.md`, `typography-hierarchy.md`, `color.md`,
`anti-ai-slop.md`, `accessibility-baseline.md`.

## Export

```bash
bash ../brand-design/scripts/render.sh index.html review-desktop.png --width 1440 --full-page --scale 1
bash ../brand-design/scripts/render.sh index.html review-mobile.png --width 390 --height 844 --full-page --scale 2
```

## Task-specific checks

- At 390px: no horizontal scroll, the CTA is visible without scrolling far,
  and grids have stacked.
- The page passes the 5-second test: from the desktop screenshot's first
  screen alone, someone can say what's offered and what to click.
- Every claim on the page is sourced from the user or repo.
