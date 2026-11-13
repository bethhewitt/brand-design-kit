#!/usr/bin/env python3
"""List brand-relevant files in the current repo, grouped by kind.

Usage (from the repo root):
  python3 discover.py                 # human-readable listing
  python3 discover.py --json          # machine-readable
  python3 discover.py --check-cache   # is .brand-design/brand-block.css fresh,
                                      # and do the notes record finished work?
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
WORK_RE = re.compile(r"\.(png|jpe?g|webp|gif|pdf)$", re.I)
BOARD_RE = re.compile(r"\.(html?|fig|sketch|xd|af|psd|ai)$", re.I)
WORK_SKIP_RE = re.compile(r"(screenshot|preview|thumb|icon|avatar|favicon|sprite)", re.I)
MAX_WORK_FOLDERS = 15
# folders whose contents are retired or rejected, never examples of the brand
WORK_SKIP_DIRS = {"archive", "archived", "rejected", "rejected-drafts", "old", "_old", "deprecated", "trash"}
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
    kinds = {"docs": [], "tokens": [], "styles": [], "logos": [], "fonts": [], "voice": [],
             "boards": [], "brand_dir": []}
    work = {}  # folder -> [(mtime, rel)]
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
        elif in_brand_dir and BOARD_RE.search(name):
            kinds["boards"].append(rel)
        elif WORK_RE.search(name) and not WORK_SKIP_RE.search(name) and \
                not any(p.lower() in WORK_SKIP_DIRS for p in rel.split(os.sep)):
            # exported images/PDFs count as finished work, inside brand folders too
            try:
                mtime = os.path.getmtime(os.path.join(root, rel))
            except OSError:
                continue
            work.setdefault(os.path.dirname(rel) or ".", []).append((mtime, rel))
        elif in_brand_dir:
            kinds["brand_dir"].append(rel)
    kinds["styles"].sort(key=lambda s: -(s["root_vars"] + 20 * s["tailwind_theme"] + 5 * s["font_face"]))
    for k in kinds:
        kinds[k] = kinds[k][:MAX_PER_KIND]
    # finished work: folders of exported images/PDFs, newest folder first
    folders = []
    for folder, files in work.items():
        files.sort(reverse=True)
        folders.append({"folder": folder, "count": len(files), "newest": files[0][0],
                        "files": [f for _, f in files[:4]]})
    folders.sort(key=lambda f: -f["newest"])
    for f in folders:
        del f["newest"]
    kinds["work"] = folders[:MAX_WORK_FOLDERS]
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
        line = line.split("*/", 1)[0]               # end of a one-line comment
        line = re.sub(r"\([^)]*\)", " ", line)       # drop notes like "(resolved 2026-11-12)"
        for p in re.split(r"[,+;]|\s·\s", line):
            p = p.strip().strip("`'\"")
            if p and p not in paths:
                paths.append(p)
    cache_mtime = os.path.getmtime(cache)
    changed, missing = [], []
    for p in paths:
        full = os.path.join(root, p)
        if not os.path.exists(full):
            missing.append(p)
        elif os.path.getmtime(full) > cache_mtime:
            changed.append(p)
    status = "stale" if (changed or missing or not paths) else "fresh"
    notes_path = os.path.join(root, ".brand-design", "brand-notes.md")
    notes = open(notes_path, encoding="utf-8", errors="ignore").read() if os.path.exists(notes_path) else ""
    observed = "present" if re.search(r"^##\s+Observed in finished work", notes, re.M | re.I) else "missing"
    note = "" if paths else "cache header lists no sources; rediscover"
    if observed == "missing":
        note = (note + "; " if note else "") + \
            "brand-notes.md has no '## Observed in finished work' section: study finished work (brand-discovery step 3) before designing"
    return {"status": status, "observed": observed, "sources": paths, "changed": changed,
            "missing": missing, "note": note}


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
        "boards": "4c. Design boards (look at these)",
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
    if result["work"]:
        empty = False
        print("\n6. Finished work, newest folders first (look at 4-8 approved pieces; see discovery step 3)")
        for f in result["work"]:
            print(f"  {f['folder']}/  ({f['count']} files)")
            for p in f["files"]:
                print(f"    {p}")
    if empty:
        print("No brand files found. Follow 'When nothing is found' in references/brand-discovery.md.")


if __name__ == "__main__":
    main()
