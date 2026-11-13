# Web prototype layouts

> Modified from OpenDesign's web-prototype layouts
> ([nexu-io/open-design](https://github.com/nexu-io/open-design), Apache-2.0).
> Sample copy replaced with placeholders. See THIRD_PARTY_NOTICES.md.

**8 paste-ready section skeletons.** Drop into `<main id="content">` of `assets/web-seed.html`. Don't write sections from scratch. Pick the closest layout, paste, swap copy.

## Pre-flight (do this once before pasting anything)

1. **Read `assets/web-seed.html`** through the end of the `<style>` block. Every class used below must exist there. If one is missing, add it to `<style>` rather than inlining it on each section.
2. **Pick a section list before writing copy.** Default rhythms:
   - **Landing**: 1 hero → 2 features → 3 stat-row OR quote → 4 split → 6 cta-strip → footer
   - **Marketing / editorial**: 1 hero-center → 7 log-list → 4 split → 6 cta-strip
   - **Pricing / docs**: 1 hero-center → table-driven → 6 cta-strip
3. **One accent per screen, used at most twice.** The hero eyebrow and the primary button already use it; budget any third usage carefully.

## Class inventory (all defined in `web-seed.html`)

> `section` `container` `hero` `hero-center` `hero-split` `hero-cta` `eyebrow` `lead` `h1` `h2` `h3` `meta` `num` `btn` `btn-primary` `btn-secondary` `btn-ghost` `btn-arrow` `card` `card-flat` `card-rule` `feature` `feature-mark` `stat` `stat-num` `stat-label` `stat-unit` `quote` `quote-mark` `quote-author` `pill` `tag` `field` `input` `textarea` `ds-table` `num-col` `ph-img` `content-img` `square` `portrait` `wide` `rule` `rule-strong` `grid-2` `grid-3` `grid-4` `grid-2-1` `grid-1-2` `row` `row-between` `stack` `log-row` `pull` `topnav` `pagefoot`

If you reach for a class not on this list, define it in `<style>` first or use `style="…"` inline. Never invent a global class on a `<section>` that isn't backed by CSS.

---

## Layout 1: Hero, centered

Use when the page leads with a thesis sentence (most landings, most marketing pages). An optional sentence-case label (never all caps), one h1 (≤14 words), one lead sentence, two CTAs.

```html
<section class="section hero">
  <div class="container hero-center">
    <p class="eyebrow">Context label (optional)</p>
    <h1>One sharp sentence about what this is.</h1>
    <p class="lead">One concrete-value subhead: what changes for the reader.</p>
    <div class="hero-cta">
      <button class="btn btn-primary">Primary action</button>
      <button class="btn btn-secondary">Secondary</button>
    </div>
  </div>
</section>
```

## Layout 2: Hero, split (text + visual)

Use when there is a real product visual (product UI, screenshot, photograph). Left half copy, right half a `ph-img` scaffold. During Step 3, replace the entire scaffold with the acquired project-local image using `<img class="content-img" width="[intrinsic width]" height="[intrinsic height]">`. Do not transfer the scaffold's `wide` class or 16:9 ratio to the real image. Retain the scaffold only as a labeled fallback when acquisition genuinely fails.

```html
<section class="section">
  <div class="container hero-split">
    <div>
      <p class="eyebrow">Role label (optional)</p>
      <h1>Headline that names the change.</h1>
      <p class="lead" style="margin-top: 20px;">A short subhead. Concrete, not corporate. Two sentences max.</p>
      <div class="hero-cta" style="margin-top: 28px;">
        <button class="btn btn-primary">Primary action</button>
        <button class="btn btn-ghost btn-arrow">Read the story</button>
      </div>
    </div>
    <div class="ph-img wide" aria-label="Hero visual placeholder">[ Hero visual · 16:9 ]</div>
  </div>
</section>
```

## Layout 3: Feature triplet

Three feature cells. Lead with a small `<h2>` framing the row. Don't put an icon on every heading. One tasteful mark per cell, monoline.

```html
<section class="section">
  <div class="container stack" style="gap: 56px;">
    <div style="max-width: 36ch;">
      <p class="eyebrow">What's different</p>
      <h2>Three things you'll notice in the first ten minutes.</h2>
    </div>
    <div class="grid-3">
      <div class="feature card-flat">
        <div class="feature-mark">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3v18M3 12h18"/></svg>
        </div>
        <h3>Specific feature one</h3>
        <p>Two-sentence description that names the user value, not the technology.</p>
      </div>
      <div class="feature card-flat">
        <div class="feature-mark">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/></svg>
        </div>
        <h3>Specific feature two</h3>
        <p>Two-sentence description that names the user value, not the technology.</p>
      </div>
      <div class="feature card-flat">
        <div class="feature-mark">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7h16M4 12h10M4 17h16"/></svg>
        </div>
        <h3>Specific feature three</h3>
        <p>Two-sentence description that names the user value, not the technology.</p>
      </div>
    </div>
  </div>
</section>
```

## Layout 4: Stat row (data billboard)

Use when there are real numbers. Three stats max; four feels like a brochure. **Don't invent metrics.** If you don't have a number, use a different layout.

```html
<section class="section">
  <div class="container">
    <p class="eyebrow" style="margin-bottom: 40px;">[LABEL: e.g. By the numbers, with year]</p>
    <div class="grid-3">
      <div class="stat">
        <div class="stat-num num">[STAT: needs source]</div>
        <p class="stat-label">[What the number measures, and where it comes from.]</p>
      </div>
      <div class="stat">
        <div class="stat-num num">[STAT: needs source]</div>
        <p class="stat-label">[What the number measures, and where it comes from.]</p>
      </div>
      <div class="stat">
        <div class="stat-num num">[STAT: needs source]<span class="stat-unit">[unit]</span></div>
        <p class="stat-label">[What the number measures, and where it comes from.]</p>
      </div>
    </div>
  </div>
</section>
```

## Layout 5: Pull quote (testimonial)

A single decisive quote with attribution. Use sparingly: one per page, never two in a row.

```html
<section class="section">
  <div class="container" style="max-width: 800px;">
    <div class="quote-mark">"</div>
    <blockquote class="quote">[QUOTE: needs source. A real customer quote, word for word.]</blockquote>
    <p class="quote-author">[NAME: needs source], [Role] at [Company]</p>
  </div>
</section>
```

## Layout 6: CTA strip (closing)

End the page on one decisive ask. Centered, generous whitespace, one primary button. No secondary unless the page has zero other buttons.

```html
<section class="section" style="text-align: center;">
  <div class="container" style="max-width: 600px;">
    <h2>[Closing line: the one thing to do next]</h2>
    <p class="lead" style="margin: 16px auto 32px;">[One supporting sentence. Real terms or prices only.]</p>
    <a class="btn btn-primary" href="[URL]">[Action, e.g. Book a call]</a>
  </div>
</section>
```

## Layout 7: Log list (changelog / blog index / posts)

Editorial layout for a list of dated entries. Date in mono on the left, title + dek in the middle, optional pull stat on the right. Borders on top, never around; boxes feel like a brochure.

```html
<section class="section">
  <div class="container">
    <div class="row-between" style="margin-bottom: 32px;">
      <h2>Recent changes</h2>
      <a class="btn btn-ghost btn-arrow" href="[URL]">View all</a>
    </div>
    <div>
      <article class="log-row">
        <span class="meta">[Date]</span>
        <div>
          <h3>[Entry title]</h3>
          <p style="margin: 4px 0 0; color: var(--muted); font-size: 14px;">[One-line summary of the entry.]</p>
        </div>
        <span class="pull meta">[Category]</span>
      </article>
      <article class="log-row">
        <span class="meta">[Date]</span>
        <div>
          <h3>[Entry title]</h3>
          <p style="margin: 4px 0 0; color: var(--muted); font-size: 14px;">[One-line summary of the entry.]</p>
        </div>
        <span class="pull meta">[Category]</span>
      </article>
    </div>
  </div>
</section>
```

## Layout 8: Comparison table (pricing, plan matrix, before/after)

Hairline borders, mono numerics, one column highlighted via an accent border. Don't put the whole row in surface-color; that screams "table".

```html
<section class="section">
  <div class="container">
    <div style="text-align: center; max-width: 36ch; margin: 0 auto 56px;">
      <p class="eyebrow">Pricing</p>
      <h2>[Heading that frames the comparison]</h2>
    </div>
    <table class="ds-table">
      <thead>
        <tr>
          <th>Feature</th>
          <th class="num-col">[Option 1]</th>
          <th class="num-col">[Option 2]</th>
          <th class="num-col">[Option 3]</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>[Feature or inclusion]</td><td class="num-col">✓</td><td class="num-col">✓</td><td class="num-col">✓</td></tr>
        <tr><td>[Feature or inclusion]</td><td class="num-col">–</td><td class="num-col">✓</td><td class="num-col">✓</td></tr>
        <tr><td>[Feature or inclusion]</td><td class="num-col">–</td><td class="num-col">–</td><td class="num-col">✓</td></tr>
        <tr style="border-top: 1px solid var(--fg);">
          <td><strong>[Price line]</strong></td>
          <td class="num-col"><strong>[Real price]</strong></td>
          <td class="num-col"><strong>[Real price]</strong></td>
          <td class="num-col"><strong>[Real price]</strong></td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
```

---

## Section rhythm: when in doubt

For a 5-section landing:
1. Hero (Layout 1 or 2)
2. Features (Layout 3)
3. Stats *or* quote (Layout 4 or 5)
4. Split detail (custom, using `grid-2-1` / `grid-1-2`)
5. CTA + footer (Layout 6)

For a 4-section docs/marketing index:
1. Hero center (Layout 1)
2. Log list (Layout 7)
3. CTA + footer (Layout 6)

Two stat rows in a row, two quote blocks in a row, two feature triplets in a row: all visual fatigue. Alternate.
