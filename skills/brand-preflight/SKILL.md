---
name: brand-preflight
description: Use first, before brand-design or any brand-* asset skill (one-pager, report, social post, email graphic, landing page), whenever an on-brand asset is requested in a repository. Audits whether the repo has a DESIGN.md with enough material to design from (colours, fonts, logo, voice, do's and don'ts) and stops to fix gaps before any design work starts. Also use when asked "is our DESIGN.md good enough", "check our design file" or "are we ready to make on-brand assets".
---

# Brand preflight

The first job in every brand task: check that this repository has a
`DESIGN.md` with enough real material to design from. Design work built on a
thin or half-filled `DESIGN.md` ends up guessing, and guessing is how assets
go off brand. This skill runs **before** `brand-design` and its asset skills,
and nothing else starts until it has a verdict.

`<preflight>` below means this skill's base directory. `<brand-design>`
means the sibling `../brand-design/` directory.

## 1. Run the check

From the repo root:

```bash
python3 <preflight>/scripts/preflight.py
```

It finds `DESIGN.md` (root first, then `docs/`, `brand/`, `design/`), reads
it against the ten sections of `<brand-design>/assets/DESIGN.template.md`
and gives one verdict:

| Verdict | Means |
|---|---|
| **READY** | All essentials stated, every section has real content |
| **GAPS** | Essentials stated; some supporting sections thin, missing or still template text |
| **INADEQUATE** | A `DESIGN.md` exists but an essential is missing |
| **MISSING** | No `DESIGN.md` in the repo |

**Essentials** (without these you can't design on brand):

- **Colour:** at least two real colour values, with an accent or primary
  role named.
- **Type:** at least one named font family.
- **Logo:** a logo file path in `DESIGN.md` that exists in the repo.

**Important** (design can go ahead, but the result will be weaker): visual
theme, voice and tone, do's and don'ts, and a font source (font files, a
Google Fonts link or a licence note).

Unfilled `[template brackets]`, `TODO` and `TBD` don't count as content.

**Then read `DESIGN.md` yourself.** The script works from headings and
patterns. Correct it where it's plainly wrong (a colour section under an
odd heading, fonts named in prose rather than a table) and say what you
corrected. Never upgrade a verdict because content "is probably somewhere
else". If it isn't in `DESIGN.md`, it's a gap.

If Python isn't available, do the same check by hand: find `DESIGN.md`, walk
the ten sections and the three essentials above, and give the same verdict.

## 2. Skip if nothing changed

If the output says **"Unchanged since the last preflight"** and the verdict
was READY or GAPS, say so in one line ("DESIGN.md unchanged since <date>,
still GAPS: no component or layout rules") and go straight to step 4. Don't
re-ask questions the user already answered for this same file.

## 3. Report and decide

Show the user a short report in plain language. Lead with the verdict, then
what's there, then what's missing:

```
DESIGN.md check: GAPS (brand/DESIGN.md)

Ready to use
  ✔ Colours  paper #f7f5f0, ink #1d1b18, pine #0f5c4d (accent)
  ✔ Fonts    Fraunces (headlines), Inter (body), Google Fonts
  ✔ Logo     public/brand/logo.svg, logo-white.svg

Missing or thin
  ✘ Component styling, layout, depth, responsive: not written yet
  ◐ Logo & imagery: names mark.svg, which isn't in the repo
```

Then act on the verdict:

- **READY:** say so in one line and continue.
- **GAPS:** list the gaps and ask (AskUserQuestion, or a plain question):
  1. **Carry on.** Design now; the gaps are filled from the repo's other
     files where possible, otherwise from neutral defaults marked as derived.
  2. **Fill the gaps first.** Follow `<brand-design>/references/brand-audit.md`
     to complete `DESIGN.md`, then return to the original request.
- **INADEQUATE:** don't start the asset. Say which essentials are missing
  and ask:
  1. **Fix DESIGN.md now** (recommended). Follow
     `<brand-design>/references/brand-audit.md`: it pulls what's in the
     repo's token files, stylesheets and logos into `DESIGN.md` and asks
     you for the rest.
  2. **Use the repo's other files instead.** Carry on with brand discovery
     from tokens and stylesheets, and say plainly in the handover that
     `DESIGN.md` didn't cover the essentials.
- **MISSING:** say there's no `DESIGN.md`. If the script listed other brand
  docs (`BRAND.md`, a style guide) or token files, offer to build `DESIGN.md`
  from them via `brand-audit.md`. Otherwise offer the three routes in
  `<brand-design>/references/brand-discovery.md` §6 (extract from a website,
  create brand files, go unbranded).

Never fill a gap yourself with a value that "looks right". Every value comes
from a file in the repo, a URL the user gave, or the user's answer.

## 4. Record and hand on

Once the user has decided (or the verdict was READY), record the result so
the next task in this repo can skip the check:

```bash
python3 <preflight>/scripts/preflight.py --save
```

This writes `.brand-design/preflight.json`. If `DESIGN.md` was rewritten in
step 3, run it after the rewrite so it records the new file.

Then carry on with what the user asked for:

- An asset → the matching `brand-*` skill, which runs `brand-design` from
  core step 1. Pass on the verdict and any gaps the user chose to live with
  so they appear in the handover.
- Only the check ("is our DESIGN.md good enough?") → stop after the report
  and the user's decision.

## Common mistakes

- Starting brand discovery or layout before the verdict.
- Counting template text (`[Two or three sentences…]`) as content.
- Treating a logo path as fine without checking the file exists.
- Quietly filling a missing essential with a guess instead of asking.
- Re-running the full report every task when `DESIGN.md` hasn't changed.
