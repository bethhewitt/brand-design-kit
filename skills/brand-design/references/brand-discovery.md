# Brand discovery

Goal: find the brand that lives in the current repository and turn it into a
**brand block** (see `brand-contract.md`), plus notes on how the brand
actually looks in finished work.

Written brand docs describe intent. Finished, approved work shows practice,
and the two often drift: a DESIGN.md can be accurate on every hex value and
still miss which colours take the area, what colour the type is, or the
components that make the brand recognisable. Tokens alone can't tell you
what the brand looks like. Read both, and look at the work. Every value must trace to a file in
the repo, a URL the user gave, or the user's own answer. Never fall back to
"what looks nice".

## 1. Check the cache first

If `.brand-design/brand-block.css` exists at the repo root, read it. Its
header comment lists the source files it came from. Run
`python3 <brand-design>/scripts/discover.py --check-cache`. If it reports
**fresh**, reuse the block and tell the user in one line which sources it came
from. Fresh only covers the tokens: if `brand-notes.md` has no
`## Observed in finished work` section (the check reports
`"observed": "missing"`), do step 3 before designing anyway. If it reports **stale**, or the user says the brand changed, rediscover.

## 2. Scan the repo

Run `python3 <brand-design>/scripts/discover.py` from the repo root. It lists
candidate files grouped by kind, skipping `node_modules`, `.git` and build
output. Then read the candidates in this priority order. Higher sources win
when they conflict:

| Priority | Kind | Typical files |
|---|---|---|
| 1 | Written brand docs | `DESIGN.md`, `BRAND.md`, `brand-guidelines.*`, `style-guide.*`, anything under `brand/` or `docs/brand/` |
| 2 | Token files | `tokens.css`, `design-tokens.json`, `*.tokens.json`, `theme.(ts\|js\|json)`, Tailwind `@theme` blocks, `tailwind.config.*` `theme.extend` |
| 3 | App styles | `:root` custom properties in global CSS/SCSS (`globals.css`, `variables.css`, `_variables.scss`) |
| 4 | Assets | logos (`*logo*.svg/png`, `wordmark*`, `favicon.svg`), font files (`.woff2/.woff/.ttf/.otf`) and `@font-face` rules, brand photography |
| 5 | Voice | tone or copy guidelines, the README intro, existing marketing copy |

Read PDFs of brand guidelines too if the repo has them. Use the pdf skill if
one is available.

## 3. Study the finished work

Do this whenever the notes lack an observed section, and whenever the user
says an asset doesn't look like their brand.

1. **Find it.** `discover.py` lists *finished work*: exported images and PDFs
   other than logo files (social posts, covers, carousels, decks, emails,
   ads), grouped by folder, newest first. It also lists *design boards*:
   HTML or image artboards and design source files in brand folders. Also
   check what the user's instructions (CLAUDE.md, README) point to.
2. **Choose 4 to 8 pieces**, preferring the newest work and a spread of
   formats. Only use work the user made or approved. Skip anything this
   skill produced (`brand-output/`, or drafts from earlier sessions) unless
   the user says it was approved. If you can't tell what's approved, ask.
3. **Look at them as images.** Downscale large files first (for example
   `sips -Z 600` on macOS) and open them with the image reader. Render
   design boards with `render.sh` if they're HTML. Don't infer the look
   from file names or from the docs.
4. **Write down what you see** under `## Observed in finished work` in
   `.brand-design/brand-notes.md`, citing the files:
   - **Colour proportions:** which colours take the area (grounds, panels)
     and which only appear as type or small accents. How many colours one
     piece uses, and whether pairings rotate.
   - **Type colour:** what colour headings are, and what colour body copy is.
   - **Type behaviour:** weights, case, mixed weights in one line, how big
     the biggest thing is compared with everything else.
   - **Signature components:** panels, frames, offsets, stickers, icons,
     sign-offs, image treatment, anything you'd point to and say "that's
     them".
   - **Never seen:** things the docs allow that the work never does.
5. **Compare with the written docs.** List every place the work and the
   docs disagree (for example "DESIGN.md: secondary colour for buttons
   only; every campaign ad uses it as the full background"). Show the user the list and ask which wins. Don't
   silently trust the docs because a file says it is the source of truth.
   Record the answer in the notes, and offer to update the brand docs so
   they stop disagreeing.

## 4. Map to the contract

- Bind each required token from the highest-priority source that states it.
- Derive the rest using the defaults in `brand-contract.md`, and mark them
  `/* derived */` in the block.
- Copy the brand's do's and don'ts, voice notes and logo rules into
  `.brand-design/brand-notes.md`. Sub-skills read that file for anything a
  token can't express.
- Check contrast: `python3 <brand-design>/scripts/check.py --brand .brand-design/brand-block.css`.
  If `--muted` or `--accent-on` fail, adjust the **derived** token only and
  say so. Never silently change a stated brand colour.

## 5. Confirm, then cache

Show the user a compact summary before the first asset in a repo, or after a
rediscovery:

```
Brand: Acme (from brand/DESIGN.md, src/styles/tokens.css)
Colours: bg #f7f5f0 · fg #1d1b18 · accent #0f5c4d · accent-2 #d98a3d
Type: Fraunces (display) / Inter (body). Font files found in public/fonts
Logo: public/brand/logo.svg (+ logo-white.svg)
Derived: muted, border, accent-on
Conflicts: tailwind.config says accent #0e5a4b, DESIGN.md says #0f5c4d → used DESIGN.md
In practice (4 ads in marketing/campaigns/, 2 decks): white grounds, accent on
  buttons and links only; photography full-bleed; square-cornered tiles
Docs vs work: DESIGN.md says 12px rounded cards; every piece uses square tiles → which wins?
```

On confirmation, write `.brand-design/brand-block.css` (with a header comment
listing every source path) and `.brand-design/brand-notes.md`. Suggest adding
`.brand-design/` to git so the team shares one resolved brand.

## 6. When nothing is found

Say so plainly, then ask which route the user wants:

1. **Extract from a website.** The user gives a URL. Fetch the page and its
   stylesheets (WebFetch, or `curl`). Frequency-rank colour literals and
   custom properties, read the `font-family` stacks on `body` and `h1`, and
   find the logo (`<link rel=icon>`, header `<img>`/`<svg>`). If browser
   tools are available, measure computed styles on the live page instead of
   guessing from CSS. Look at the live pages as step 3 does, then continue
   at step 4.
2. **Create a brand file.** Ask a short set of questions (name, primary
   colour, secondary colour, fonts, logo file, 3 words for the tone, any
   don'ts). Write `DESIGN.md` and `tokens.css` at the repo root from
   `assets/DESIGN.template.md` and `assets/tokens.template.css`. Then
   continue at step 4.
3. **Go unbranded.** Use the neutral block in `assets/web-seed.html` and
   label the output as unbranded in the file name and your reply.
