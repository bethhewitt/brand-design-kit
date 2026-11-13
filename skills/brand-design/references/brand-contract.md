# Brand contract

Every brand, however the repo stores it, is mapped onto one fixed set of CSS
custom properties. Templates only ever read these names, so one template
works for every brand. The resolved set is called the **brand block**: a
single `:root { … }` pasted as the first rule of every asset's `<style>`.

Format adapted from OpenDesign's design-system token schema.

## Tokens

**Required** (always bind these; derive if the brand doesn't state them):

| Token | Role | If the brand doesn't say |
|---|---|---|
| `--bg` | Page / canvas background | Brand's lightest neutral. Avoid pure `#fff` unless the brand uses it |
| `--surface` | Cards, panels, raised areas | `--bg` nudged 2–4% lighter or darker |
| `--fg` | Primary text | Brand's darkest neutral. Avoid pure `#000` unless the brand uses it |
| `--muted` | Secondary text, captions | `--fg` mixed ~45% toward `--bg`; must still pass 4.5:1 on `--bg` |
| `--border` | Hairlines, dividers | `--fg` mixed ~88% toward `--bg` |
| `--accent` | The one brand colour for CTAs, links, focus, one focal element | Brand primary. Never invent one |
| `--accent-on` | Text/icon colour on top of `--accent` | `#fff` or `--fg`, whichever passes 4.5:1 |
| `--font-display` | Headlines | Brand display/heading face plus a fallback chain |
| `--font-body` | Body copy | Brand body face plus a fallback chain |

**Optional** (bind when the brand defines them, otherwise derive or alias):

| Token | Role | Default |
|---|---|---|
| `--surface-warm` | Nested / tinted panels | alias `--surface` |
| `--fg-2` | Sub-headings, strong labels | alias `--fg` |
| `--meta` | Lowest-emphasis text (dates, page numbers) | alias `--muted` |
| `--border-soft` | Row separators | alias `--border` |
| `--accent-hover`, `--accent-active` | Interactive states | `color-mix(in oklab, var(--accent), black 8%)` / `14%` |
| `--accent-2` | Secondary brand colour (charts, illustration only) | omit |
| `--success`, `--warn`, `--danger` | Status | `#16a34a`, `#eab308`, `#dc2626` |
| `--font-mono` | Numbers, labels, code | `ui-monospace, 'SF Mono', Menlo, monospace` |
| `--radius-sm/-md/-lg/-pill` | Corner radii | `6px / 10px / 16px / 9999px` |
| `--container-max` | Web content width | `1120px` |
| `--logo` | Path to the primary logo file (as a CSS string, for reference only) | omit |

Chart series colours: `--accent`, then `--accent-2`, then `--fg-2`, then
`--muted`. Never introduce an unrelated hue for a chart.

## Example brand block

```css
:root {
  /* Source: brand/DESIGN.md + src/styles/tokens.css (resolved 2026-11-12) */
  --bg: #f7f5f0; --surface: #ffffff; --surface-warm: #efebe3;
  --fg: #1d1b18; --fg-2: #35322d; --muted: #6d6860; --meta: #8c867c;
  --border: #e3ded4; --border-soft: #eeeae2;
  --accent: #0f5c4d; --accent-on: #ffffff; --accent-2: #d98a3d;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --success: #16a34a; --warn: #eab308; --danger: #dc2626;
  --font-display: 'Fraunces', Georgia, serif;
  --font-body: 'Inter', -apple-system, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, Menlo, monospace;
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 14px; --radius-pill: 9999px;
  --container-max: 1120px;
}
```

Fonts: when the repo ships font files, add `@font-face` rules above the brand
block that point at them with paths relative to the asset. If the font is a
Google Font, a single `<link>` is fine for web output. For PNG/PDF export the
font must actually load, or the render falls back. Check the render.

## The DESIGN.md format

When a repo has no brand file and the user wants one created, write
`DESIGN.md` at the repo root from `assets/DESIGN.template.md`, plus a matching
`tokens.css` from `assets/tokens.template.css`. The sections:

1. Visual theme & atmosphere
2. Colour palette & roles
3. Typography rules
4. Component styling (buttons, cards, badges, inputs)
5. Layout principles (spacing, grid, whitespace, radii)
6. Depth & elevation
7. Do's and don'ts
8. Responsive behaviour
9. Voice & tone (how the brand writes)
10. Logo & imagery usage
