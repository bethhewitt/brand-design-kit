#!/usr/bin/env node
// Render a brand-design HTML file to PNG or PDF with headless Chromium.
// Invoke through render.sh, which installs the Playwright runtime on first use.
//
//   render.sh <in.html> <out.png|out.pdf> [options]
//
// Options:
//   --width N --height N   viewport in CSS px (default 1280x800)
//   --scale N              device pixel ratio for PNG (default 2)
//   --selector CSS         PNG: export each matching element as its own file
//                          (out-01.png, out-02.png ...). Use for carousels and size packs.
//   --full-page            PNG: capture the whole scrollable page
//   --format A4|Letter     PDF: force a paper size (default: the CSS @page size)
//   --wait MS              extra wait before capture (default 300)

const path = require('path');
const fs = require('fs');

const runtime = process.env.BD_RUNTIME;
const { chromium } = require(path.join(runtime, 'node_modules', 'playwright'));

function parse(argv) {
  const [input, output, ...rest] = argv;
  const o = { input, output, width: 1280, height: 800, scale: 2, wait: 300 };
  for (let i = 0; i < rest.length; i++) {
    const k = rest[i];
    if (k === '--full-page') o.fullPage = true;
    else if (k.startsWith('--')) o[k.slice(2).replace(/-(\w)/g, (_, c) => c.toUpperCase())] = rest[++i];
  }
  ['width', 'height', 'scale', 'wait'].forEach((k) => (o[k] = Number(o[k])));
  if (!o.input || !o.output) {
    console.error('usage: render.sh <in.html> <out.png|out.pdf> [--width N --height N --scale N --selector CSS --full-page --format A4 --wait MS]');
    process.exit(2);
  }
  return o;
}

(async () => {
  const o = parse(process.argv.slice(2));
  const inPath = path.resolve(o.input);
  const outPath = path.resolve(o.output);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  const isPdf = outPath.toLowerCase().endsWith('.pdf');

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: o.width, height: o.height },
    deviceScaleFactor: isPdf ? 1 : o.scale,
  });
  const failed = [];
  page.on('requestfailed', (r) => failed.push(r.url()));
  await page.goto('file://' + inPath, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(o.wait);

  const fontReport = await page.evaluate(() =>
    [...document.fonts].filter((f) => f.status !== 'loaded' && f.status !== 'unloaded').map((f) => `${f.family} (${f.status})`)
  );

  // Fixed-size containers (.page for print, .frame for social/email) must not overflow.
  const overflow = await page.evaluate(() =>
    [...document.querySelectorAll('.page, .frame')]
      .map((el, i) => ({ i: i + 1, cls: el.classList.contains('page') ? 'page' : 'frame', dh: el.scrollHeight - el.clientHeight, dw: el.scrollWidth - el.clientWidth }))
      .filter((r) => r.dh > 1 || r.dw > 1)
      .map((r) => `${r.cls} ${r.i} overflows by ${Math.max(r.dh, 0)}px vertically, ${Math.max(r.dw, 0)}px horizontally`)
  );

  const written = [];
  if (isPdf) {
    const opts = { path: outPath, printBackground: true };
    if (o.format) opts.format = o.format;
    else opts.preferCSSPageSize = true;
    await page.pdf(opts);
    written.push(outPath);
  } else if (o.selector) {
    const els = await page.$$(o.selector);
    if (!els.length) throw new Error(`selector matched nothing: ${o.selector}`);
    const base = outPath.replace(/\.png$/i, '');
    for (let i = 0; i < els.length; i++) {
      const file = `${base}-${String(i + 1).padStart(2, '0')}.png`;
      await els[i].screenshot({ path: file });
      written.push(file);
    }
  } else {
    await page.screenshot({ path: outPath, fullPage: !!o.fullPage });
    written.push(outPath);
  }
  await browser.close();

  written.forEach((f) => console.log('wrote ' + f));
  if (failed.length) console.warn('WARN failed to load: ' + [...new Set(failed)].join(', '));
  if (fontReport.length) console.warn('WARN fonts not loaded: ' + fontReport.join(', '));
  overflow.forEach((m) => console.warn('WARN ' + m + ' (content is clipped — shorten or re-lay out)'));
})().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
