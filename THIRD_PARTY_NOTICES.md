# Third-party notices

The brand-design kit is MIT-licensed (see `LICENSE`). Some files are adapted
from the projects below and stay under those projects' licences. Each adapted
file says so in its header.

## OpenDesign

Source: https://github.com/nexu-io/open-design
Licence: Apache License 2.0 (full text in `LICENSES/Apache-2.0-OpenDesign.txt`)

Modified files in this kit:

- `skills/brand-design/references/craft/accessibility-baseline.md`
- `skills/brand-design/references/craft/anti-ai-slop.md`
- `skills/brand-design/references/craft/color.md`
- `skills/brand-design/references/craft/typography.md`
- `skills/brand-design/references/craft/typography-hierarchy.md`
- `skills/brand-design/references/craft/typography-hierarchy-editorial.md`
- `skills/brand-design/assets/layouts.md`
- `skills/brand-design/assets/web-seed.html`

`skills/brand-design/references/brand-contract.md` follows the shape of
OpenDesign's design-system token schema.

Changes made: rewritten to read the brand-contract tokens, OpenDesign-specific
wiring removed, sample product copy replaced with placeholders, and rules
added (for example, no all-caps labels).

## refero_skill

Source: https://github.com/referodesign/refero_skill
Licence: MIT, Copyright (c) 2026 Refero (full text in `LICENSES/MIT-refero_skill.txt`)

`anti-ai-slop.md`, `color.md` and `typography.md` in
`skills/brand-design/references/craft/` reached OpenDesign from refero_skill
and were modified again here.

## Impeccable

Source: https://github.com/pbakaus/impeccable (Apache License 2.0, Copyright 2025 Paul Bakaus)

Credited, not copied. The "P2 — polish pass" section of
`skills/brand-design/references/qa-checklist.md` follows the order of
Impeccable's audit, polish and harden steps and uses those step names. Its
wording is original to this kit; no Impeccable text or code is included.

## Playwright (installed at run time, not bundled)

`render.sh` installs Playwright and Chromium from npm on first use, into a
per-user cache. Playwright is Apache-2.0 (https://github.com/microsoft/playwright).
