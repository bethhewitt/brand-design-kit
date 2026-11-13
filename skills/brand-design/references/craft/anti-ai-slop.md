# Anti-AI-slop rules

Concrete, checkable rules that separate "designed by someone who has shipped
work" from "default LLM output". Rules marked **(checked)** are flagged by
`scripts/check.py`; the rest are judgement calls for you and the reviewer.

> Adapted from [refero_skill](https://github.com/referodesign/refero_skill)
> (MIT, © 2026 Refero) via the craft rules in
> [OpenDesign](https://github.com/nexu-io/open-design) (Apache-2.0), and modified.
> See THIRD_PARTY_NOTICES.md at the package root.

## The seven cardinal sins (P0 — must fix)

1. **Default Tailwind indigo/violet as accent** **(checked)** — `#6366f1`,
   `#4f46e5`, `#4338ca`, `#3730a3`, `#8b5cf6`, `#7c3aed`, `#a855f7`. The brand
   provides `--accent`; use it. Exception: the brand's own tokens genuinely
   bind one of these as `--accent`. Then it is the brand, not a default.
2. **Two-stop "trust" gradient on the hero** — purple→blue, blue→cyan,
   indigo→pink. A flat surface plus intentional type beats it every time.
3. **Emoji as icons** **(checked)** — `✨ 🚀 🎯 ⚡ 🔥 💡` and friends inside
   headings, buttons, list items or icon slots. Use 1.5–2px-stroke monoline
   SVG with `currentColor`, or the brand's own icon set if the repo has one.
4. **Generic sans on display text when the brand binds a display face** —
   h1/h2 use `var(--font-display)`, never a hardcoded Inter / Roboto /
   `system-ui`.
5. **Rounded card with a coloured left-border accent** — the canonical "AI
   dashboard tile". Drop the radius or drop the border.
6. **Invented metrics** — "10× faster", "99.9% uptime", "3× more productive".
   Use a number the user or the repo supplied, or a labelled placeholder such
   as `[STAT: needs source]`.
7. **Filler copy** **(checked)** — `lorem ipsum`, `feature one / two / three`,
   `placeholder text`, `sample content`. An empty section is a composition
   problem, not a reason to invent words.

## Soft tells (P1 — should fix)

- **The stock "Hero → Features → Pricing → FAQ → CTA" skeleton** with no
  variation. Add at least one unexpected section: a full-bleed quote, pricing
  framed against the status quo, an inline product moment.
- **External placeholder image CDNs** **(checked)** — `unsplash.com`,
  `placehold.co`, `picsum.photos`, `placekitten.com`. Use real brand imagery
  from the repo, or a tinted `.ph-img` block labelled with what goes there.
- **More than ~12 raw hex values outside `:root`** **(checked)** — tokens were
  not honoured.
- **All-caps eyebrow labels** **(checked)**: a small, letter-spaced uppercase
  label above a headline or in a frame's corner ("CASE STUDY", "WHAT WE
  DO"). It is the most recognisable template tell. Use sentence case at
  normal tracking, and only where the label tells the reader something.
  Avoid `text-transform: uppercase` entirely unless the brand's own guidelines
  require it.
- **Half-height marker band behind display type**: a block of accent colour
  covering the lower half of a headline word. It reads as neither a
  highlight nor an underline. Commit to one: a full highlight behind the
  whole word, or a clean underline about a tenth of the font size thick,
  below the baseline, breaking around descenders.
- **`var(--accent)` used everywhere.** Cap visible accent uses at about two per
  screen or frame.

## Polish tells (P2 — nice to fix)

- Decorative blob / wave SVG backgrounds with no meaning.
- Perfectly symmetric layout with no tension. Alternating density (one tight
  section, one breathing section) reads as intentional.

## How to add soul without breaking the rules

Aim for **~80% proven patterns + ~20% distinctive choice**. Put the 20% in:

- One bold visual move: a type choice, a single colour decision, an
  unexpected proportion.
- Voice and microcopy, in the brand's own tone. "Start tracking" beats
  "Get started".
- One detail only someone who knows the product would add.

If someone outside the project can tell which brand an asset belongs to from
a screenshot, it has soul. If not, it's a template.
