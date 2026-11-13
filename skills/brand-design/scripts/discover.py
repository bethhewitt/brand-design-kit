#!/usr/bin/env python3
"""List brand-relevant files in the current repo, grouped by kind.

Usage (from the repo root):
  python3 discover.py                 # human-readable listing
  python3 discover.py --json          # machine-readable
  python3 discover.py --check-cache   # is .brand-design/brand-block.css fresh?
"""
import json
import os
import re
import sys

SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next", ".nuxt", ".svelte-kit",
    "coverage", "vendor", ".venv", "venv", "__pycache__", ".turbo", ".cache",
    ".parcel-cache", "target", ".brand-design", "brand-output", ".idea", ".vscode",
}
MAX_PER_KIND = 30
MAX_CSS_BYTES = 400_000

DOC_RE = re.compile(r"^(design|brand|brand[-_ ]?guidelines?|style[-_ ]?guide|identity)\.(md|mdx|txt|pdf)$", re.I)
TOKEN_RE = re.compile(r"(^tokens?\.(css|scss|json|js|ts)$)|(\.tokens\.json$)|(^design[-_]tokens\.(json|css)$)|(^theme\.(ts|js|json|css)$)|(^tailwind\.config\.(js|cjs|mjs|ts)$)", re.I)
STYLE_RE = re.compile(r"\.(css|scss|sass|less)$", re.I)
LOGO_RE = re.compile(r"(logo|wordmark|logomark|brandmark|monogram|favicon)[^/]*\.(svg|png|jpe?g|webp|ico)$", re.I)
FONT_RE = re.compile(r"\.(woff2?|ttf|otf)$", re.I)
VOICE_RE = re.compile(r"(tone|voice|copy|messaging|writing)[-_ ]?(guide|guidelines)?\.(md|mdx|txt|pdf)$", re.I)


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        rel_dir = os.path.relpath(dirpath, root)
        in_brand_dir = any(p.lower() in {"brand", "branding", "brand-assets", "identity"} for p in rel_dir.split(os.sep))
        for f in filenames:
            yield os.path.normpath(os.path.join(rel_dir, f)), f, in_brand_dir


def css_signals(path):
    try:
        if os.path.getsize(path) > MAX_CSS_BYTES:
            return None
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return None
    root_vars = 0
    for block in re.findall(r":root[^{]*\{([^}]*)\}", text):
        root_vars += len(re.findall(r"--[\w-]+\s*:", block))
    theme = "@theme" in text
    font_face = text.count("@font-face")
    if root_vars >= 4 or theme or font_face:
        return {"root_vars": root_vars, "tailwind_theme": theme, "font_face": font_face}
    return None


def scan(root="."):
    kinds = {"docs": [], "tokens": [], "styles": [], "logos": [], "fonts": [], "voice": [], "brand_dir": []}
    for rel, name, in_brand_dir in walk(root):
        if DOC_RE.search(name):
            kinds["docs"].append(rel)
        elif TOKEN_RE.search(name):
            kinds["tokens"].append(rel)
        elif VOICE_RE.search(name):
            kinds["voice"].append(rel)
        elif LOGO_RE.search(name):
            kinds["logos"].append(rel)
        elif FONT_RE.search(name):
            kinds["fonts"].append(rel)
        elif STYLE_RE.search(name) and (sig := css_signals(os.path.join(root, rel))):
            kinds["styles"].append({"path": rel, **sig})
        elif in_brand_dir:
            kinds["brand_dir"].append(rel)
    kinds["styles"].sort(key=lambda s: -(s["root_vars"] + 20 * s["tailwind_theme"] + 5 * s["font_face"]))
    for k in kinds:
        kinds[k] = kinds[k][:MAX_PER_KIND]
    return kinds


def check_cache(root="."):
    cache = os.path.join(root, ".brand-design", "brand-block.css")
    if not os.path.exists(cache):
        return {"status": "missing"}
    text = open(cache, encoding="utf-8", errors="ignore").read()
    header = text.split(":root", 1)[0]
    sources = re.findall(r"(?:Source|Sources|source)s?:\s*(.+)", header)
    paths = []
    for line in sources:
        paths += [p.strip() for p in re.split(r"[,+]", line) if p.strip() and "(" not in p]
    cache_mtime = os.path.getmtime(cache)
    changed, missing = [], []
    for p in paths:
        full = os.path.join(root, p)
        if not os.path.exists(full):
            missing.append(p)
        elif os.path.getmtime(full) > cache_mtime:
            changed.append(p)
    status = "stale" if (changed or missing or not paths) else "fresh"
    return {"status": status, "sources": paths, "changed": changed, "missing": missing,
            "note": "" if paths else "cache header lists no sources; rediscover"}


def main():
    args = sys.argv[1:]
    if "--check-cache" in args:
        print(json.dumps(check_cache(), indent=2))
        return
    result = scan()
    if "--json" in args:
        print(json.dumps(result, indent=2))
        return
    labels = {
        "docs": "1. Written brand docs", "tokens": "2. Token / theme files",
        "styles": "3. Stylesheets with brand signals", "logos": "4a. Logos",
        "fonts": "4b. Font files", "voice": "5. Voice / copy guides",
        "brand_dir": "Other files in brand folders",
    }
    empty = True
    for k, label in labels.items():
        items = result[k]
        if not items:
            continue
        empty = False
        print(f"\n{label}")
        for it in items:
            if isinstance(it, dict):
                bits = [f"{it['root_vars']} :root vars"]
                if it["tailwind_theme"]:
                    bits.append("@theme")
                if it["font_face"]:
                    bits.append(f"{it['font_face']} @font-face")
                print(f"  {it['path']}  ({', '.join(bits)})")
            else:
                print(f"  {it}")
    if empty:
        print("No brand files found. Follow 'When nothing is found' in references/brand-discovery.md.")


if __name__ == "__main__":
    main()
