#!/usr/bin/env python3
"""Mechanical QA for brand-design output. Judgement calls live in
references/qa-checklist.md; this script only catches what a regex can.

Usage:
  python3 check.py <file.html> [more.html ...]   # P0/P1 checks; exit 1 on any P0
  python3 check.py --brand <tokens.css> [more.css]  # contrast check; follows @import
"""
import os
import re
import sys

AI_INDIGO = {"#6366f1", "#4f46e5", "#4338ca", "#3730a3", "#8b5cf6", "#7c3aed", "#a855f7"}
PLACEHOLDER_CDNS = ("unsplash.com", "placehold.co", "placeholder.com", "picsum.photos", "placekitten.com", "via.placeholder")
FILLER = re.compile(r"lorem ipsum|dolor sit amet|feature (one|two|three)\b|placeholder text|sample content|your (headline|text) here", re.I)
LEFTOVER = re.compile(r"\[REPLACE[^\]]*\]|REPLACE_WITH_REAL_URL|https?://example\.com", re.I)
NEEDS_INPUT = re.compile(r"\[[A-Z][A-Z /]+[:—][^\]]*\]")
# Bracketed template copy such as [Entry title] or [Real price] from assets/layouts.md.
UNFILLED = re.compile(r"\[[A-Z][^\]\n<>{}]{1,80}\]")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")
ICON_SLOTS = re.compile(r"<(h[1-6]|button|li|a)\b[^>]*>(.*?)</\1>|class=\"[^\"]*icon[^\"]*\"[^>]*>(.*?)<", re.I | re.S)
HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


def root_blocks(text):
    return re.findall(r":root[^{]*\{[^}]*\}", text)


def check_html(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    p0, p1, info = [], [], []
    roots = root_blocks(text)
    root_text = "".join(roots)
    outside = text
    for block in roots:
        outside = outside.replace(block, "")

    if not re.search(r"--accent\s*:", root_text):
        p0.append("No brand block: no --accent defined in a :root rule")
    brand_accent = (re.search(r"--accent\s*:\s*(#[0-9a-fA-F]{6})", root_text) or [None, ""])[1].lower()
    for h in sorted({h.lower() for h in HEX.findall(outside)} & AI_INDIGO):
        if h != brand_accent:
            p0.append(f"Default AI indigo/violet {h} used outside the brand block")
    if FILLER.search(text):
        p0.append(f"Filler copy: '{FILLER.search(text).group(0)}'")
    for m in set(LEFTOVER.findall(text)):
        p0.append(f"Template leftover: {m}")
    if re.search(r'href="#"', text):
        p0.append('Dead link: href="#" (use a real URL or remove the CTA)')
    for m in ICON_SLOTS.finditer(text):
        inner = m.group(2) or m.group(3) or ""
        found = EMOJI.findall(re.sub(r"<[^>]+>", "", inner))
        if found:
            p0.append(f"Emoji used as icon/heading decoration: {''.join(found)}")
            break
    if re.search(r"text-transform\s*:\s*uppercase", text, re.I):
        p1.append("text-transform: uppercase found (all-caps eyebrows/labels read as a template; use sentence case)")
    for cdn in PLACEHOLDER_CDNS:
        if cdn in text:
            p1.append(f"External placeholder image host: {cdn}")
    raw_hex = len(HEX.findall(re.sub(r"<svg.*?</svg>", "", outside, flags=re.S)))
    if raw_hex > 12:
        p1.append(f"{raw_hex} raw hex colours outside :root (tokens not honoured; aim for under 12)")
    # Stylesheet rules are fine; ad-hoc inline accent styling is where overuse creeps in.
    inline_accent = sum(s.count("var(--accent)") for s in re.findall(r'style="([^"]*)"', text))
    if inline_accent > 3:
        p1.append(f"var(--accent) used in {inline_accent} inline styles; check visible accent use stays to about 2 per screen/frame")
    needs = set(NEEDS_INPUT.findall(text))
    for m in sorted(needs):
        info.append(f"Needs user input: {m}")
    visible = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.S | re.I)
    unfilled = sorted(set(UNFILLED.findall(visible)) - needs - set(LEFTOVER.findall(text)))
    if unfilled:
        info.append("Unfilled template text (fill or remove before hand-over): " + ", ".join(unfilled[:8]))

    print(f"\n{path}")
    for label, items in (("P0", p0), ("P1", p1), ("INFO", info)):
        for i in items:
            print(f"  {label}  {i}")
    if not (p0 or p1 or info):
        print("  OK  no mechanical issues found")
    return bool(p0)


# ── contrast ────────────────────────────────────────────────────────────
def parse_tokens(text):
    tokens = {}
    for block in root_blocks(text):
        for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block):
            tokens[name] = value.strip()
    return tokens


def resolve(tokens, name, depth=0):
    v = tokens.get(name)
    if v is None or depth > 8:
        return None
    m = re.fullmatch(r"var\((--[\w-]+)\)", v)
    if m:
        return resolve(tokens, m.group(1), depth + 1)
    m = HEX.fullmatch(v)
    return v if m else None


def lum(hexv):
    hexv = hexv.lstrip("#")
    if len(hexv) == 3:
        hexv = "".join(c * 2 for c in hexv)
    rgb = [int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def load_tokens(path, seen=None):
    """Tokens from a CSS file, following local @import so aliases like
    `--accent: var(--brand-pine)` resolve into the file that defines them."""
    seen = seen if seen is not None else set()
    path = os.path.abspath(path)
    if path in seen or not os.path.exists(path):
        return {}
    seen.add(path)
    text = open(path, encoding="utf-8", errors="ignore").read()
    tokens = {}
    for ref in re.findall(r"""@import\s+(?:url\()?["']([^"')]+)["']""", text):
        if not re.match(r"https?:", ref):
            tokens.update(load_tokens(os.path.join(os.path.dirname(path), ref), seen))
    tokens.update(parse_tokens(text))
    return tokens


def check_brand(paths):
    tokens = {}
    for p in paths:  # later files override earlier ones
        tokens.update(load_tokens(p))
    path = ", ".join(paths)
    pairs = [("--fg", "--bg", 4.5, "body text"), ("--fg", "--surface", 4.5, "text on cards"),
             ("--muted", "--bg", 4.5, "secondary text"), ("--accent-on", "--accent", 4.5, "button label"),
             ("--accent", "--bg", 3.0, "accent as large text / UI")]
    failed = False
    print(f"\n{path}")
    for fg, bg, need, label in pairs:
        a, b = resolve(tokens, fg), resolve(tokens, bg)
        if not (a and b):
            print(f"  SKIP {fg} on {bg} ({label}): not resolvable to a hex value "
                  f"(missing, or computed e.g. color-mix; pass the file defining it as another --brand argument)")
            continue
        r = ratio(a, b)
        ok = r >= need
        failed |= not ok
        print(f"  {'OK  ' if ok else 'FAIL'} {fg} on {bg} ({label}): {r:.2f}:1, needs {need}:1")
    return failed


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "--brand":
        sys.exit(1 if check_brand(args[1:]) else 0)
    bad = [check_html(p) for p in args]
    sys.exit(1 if any(bad) else 0)


if __name__ == "__main__":
    main()
