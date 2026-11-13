#!/usr/bin/env python3
"""Check whether this repo's DESIGN.md holds enough to design on brand.

Usage (from the repo root):
  python3 preflight.py            # human-readable report
  python3 preflight.py --json     # machine-readable
  python3 preflight.py --save     # also record the result in .brand-design/preflight.json

Verdicts:
  READY         every essential is stated; nothing important is missing
  GAPS          essentials are stated; some supporting sections are thin or missing
  INADEQUATE    DESIGN.md exists but at least one essential is missing
  MISSING       no DESIGN.md in the repo

The script is a first pass. It reads structure and obvious values; the skill
still reads the file itself before reporting.
"""
import datetime
import hashlib
import json
import os
import re
import sys

SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next", ".nuxt", ".svelte-kit",
    "coverage", "vendor", ".venv", "venv", "__pycache__", ".turbo", ".cache",
    ".parcel-cache", "target", ".brand-design", "brand-output", ".idea", ".vscode",
}
PREFERRED_DIRS = ["", "docs", "brand", "docs/brand", "design", ".github"]
OTHER_DOC_RE = re.compile(r"^(brand|brand[-_ ]?guidelines?|style[-_ ]?guide|identity)\.(md|mdx|txt|pdf)$", re.I)
LOGO_FILE_RE = re.compile(r"(logo|wordmark|logomark|brandmark|monogram)[^/]*\.(svg|png|jpe?g|webp)$", re.I)
FONT_FILE_RE = re.compile(r"\.(woff2?|ttf|otf)$", re.I)
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
COLOR_FN_RE = re.compile(r"\b(?:rgb|rgba|hsl|hsla|oklch|oklab)\([^)]*\)")
PATH_RE = re.compile(r"[\w./@-]+\.(?:svg|png|jpe?g|webp|woff2?|ttf|otf)\b", re.I)
PLACEHOLDER_RE = re.compile(r"\[(?![^\]]*\]\()[^\]|]*[a-z][^\]|]*\]")  # [bracket text], not [links](...)
TODO_RE = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum)\b", re.I)

# The ten sections of assets/DESIGN.template.md in brand-design, and the
# heading words that count as each. First match wins, in this order.
SECTIONS = [
    ("theme", "Visual theme & atmosphere", r"theme|atmosphere|personality|look and feel|overview"),
    ("colour", "Colour palette & roles", r"colou?r|palette"),
    ("type", "Typography rules", r"typograph|type|font"),
    ("components", "Component styling", r"component|button|card"),
    ("layout", "Layout principles", r"layout|spacing|grid|whitespace"),
    ("depth", "Depth & elevation", r"depth|elevation|shadow"),
    ("dos", "Do's and don'ts", r"\bdo'?s\b|don'?t|rules"),
    ("responsive", "Responsive behaviour", r"responsive|breakpoint|mobile"),
    ("voice", "Voice & tone", r"voice|tone|copy|writing|messaging"),
    ("logo", "Logo & imagery", r"logo|imagery|photograph|illustration"),
]
ESSENTIAL = ["colour", "type", "logo"]
IMPORTANT = ["theme", "voice", "dos"]
MIN_WORDS = 12  # real words a section needs to count as more than a stub


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not (d.startswith(".") and d != ".github")]
        rel_dir = os.path.relpath(dirpath, root)
        for f in filenames:
            yield os.path.normpath(os.path.join(rel_dir, f)), f


def find_docs(root):
    design, others, logos, fonts = [], [], [], []
    for rel, name in walk(root):
        if name.lower() == "design.md":
            design.append(rel)
        elif OTHER_DOC_RE.search(name):
            others.append(rel)
        elif LOGO_FILE_RE.search(name):
            logos.append(rel)
        elif FONT_FILE_RE.search(name):
            fonts.append(rel)

    def rank(p):
        d = os.path.dirname(p).replace(os.sep, "/")
        return (PREFERRED_DIRS.index(d) if d in PREFERRED_DIRS else len(PREFERRED_DIRS), p.count(os.sep), p)

    return sorted(design, key=rank), sorted(others), sorted(logos), sorted(fonts)


def split_sections(text):
    """Return [(heading, body)] for every markdown heading, outside code fences."""
    out, heading, body, fence = [], None, [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            if heading is not None:
                out.append((heading, "\n".join(body)))
            heading, body = m.group(2).strip(), []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        out.append((heading, "\n".join(body)))
    return out


def clean(body):
    """Body text with template placeholders, table scaffolding and comments removed."""
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"^\s*>.*$", " ", body, flags=re.M)  # template blockquote notes
    body = PLACEHOLDER_RE.sub(" ", body)
    body = re.sub(r"^\s*\|?[\s:|-]+\|?\s*$", " ", body, flags=re.M)  # table separators
    return body


def words(body):
    return len(re.findall(r"[A-Za-z]{2,}", clean(body)))


def table_column(body, header_re):
    """Non-empty cells under the first table column whose header matches header_re."""
    lines = [l for l in body.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return []
    cells = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
    head = cells(lines[0])
    idx = next((i for i, h in enumerate(head) if re.search(header_re, h, re.I)), None)
    if idx is None:
        return []
    vals = []
    for l in lines[2:]:
        row = cells(l)
        if idx < len(row):
            v = PLACEHOLDER_RE.sub("", row[idx]).strip()
            if v and not re.fullmatch(r"[-–—\s]*", v):
                vals.append(v)
    return vals


def assess(root, path, logos_in_repo, fonts_in_repo):
    text = open(os.path.join(root, path), encoding="utf-8", errors="ignore").read()
    base = os.path.dirname(path)
    found = {}
    for heading, body in split_sections(text):
        for key, _, pat in SECTIONS:
            if key not in found and re.search(pat, heading, re.I):
                found[key] = {"heading": heading, "body": body}
                break

    report = {}
    for key, label, _ in SECTIONS:
        sec = found.get(key)
        if not sec:
            report[key] = {"label": label, "status": "missing", "notes": []}
            continue
        body = sec["body"]
        n = words(body)
        todos = len(TODO_RE.findall(body))
        placeholders = len(PLACEHOLDER_RE.findall(body))
        status = "complete" if n >= MIN_WORDS and not todos and not placeholders else ("partial" if n else "empty")
        notes = []
        if placeholders:
            notes.append(f"{placeholders} unfilled template placeholder(s)")
        if todos:
            notes.append(f"{todos} TODO/TBD marker(s)")
        report[key] = {"label": label, "status": status, "heading": sec["heading"], "words": n, "notes": notes}

    # Essentials: concrete values, not just a heading.
    colour_body = found.get("colour", {}).get("body", "")
    colours = sorted(set(HEX_RE.findall(clean(colour_body)) + COLOR_FN_RE.findall(clean(colour_body))))
    if not colours:  # some docs list colours outside a colour heading
        colours = sorted(set(HEX_RE.findall(clean(text))))
    accent_named = bool(re.search(r"accent|primary|brand colou?r|main colou?r", clean(colour_body), re.I))
    ess = {}
    ess["colour"] = {
        "ok": len(colours) >= 2 and accent_named,
        "values": colours[:12],
        "detail": (f"{len(colours)} colour value(s)" + ("" if accent_named else "; no accent/primary role named")),
    }

    type_body = found.get("type", {}).get("body", "")
    families = table_column(type_body, r"family|font|typeface")
    if not families:
        families = re.findall(r"(?:family|font|typeface)\s*[:=]\s*['\"]?([A-Z][\w\s-]{1,40}?)['\"]?(?:[,;\n]|$)", clean(type_body))
        families += re.findall(r"['\"]([A-Z][\w -]{1,40})['\"]", clean(type_body))
    families = sorted(set(f.strip() for f in families if f.strip()))
    font_source = bool(fonts_in_repo) or bool(re.search(r"fonts\.googleapis|fonts\.google|@font-face|adobe fonts|typekit|licen[cs]e", text, re.I))
    ess["type"] = {
        "ok": bool(families),
        "values": families[:8],
        "detail": f"{len(families)} font family name(s)" + ("" if font_source else "; no font files, Google Fonts link or licence note"),
        "font_source": font_source,
    }

    logo_body = found.get("logo", {}).get("body", "")
    referenced = sorted(set(m for m in PATH_RE.findall(logo_body) if not FONT_FILE_RE.search(m)))
    exists, missing = [], []
    for ref in referenced:
        candidates = [os.path.normpath(os.path.join(root, base, ref)), os.path.normpath(os.path.join(root, ref.lstrip("/"))),
                      os.path.normpath(os.path.join(root, "public", ref.lstrip("/")))]
        (exists if any(os.path.exists(c) for c in candidates) else missing).append(ref)
    ess["logo"] = {
        "ok": bool(exists),
        "values": exists,
        "missing_files": missing,
        "unreferenced_in_repo": [l for l in logos_in_repo if not any(l.endswith(os.path.normpath(e).lstrip("./")) for e in exists)][:10],
        "detail": (f"{len(exists)} logo file(s) found" if exists else "no logo file path in DESIGN.md that exists in the repo"),
    }

    essential_missing = [k for k in ESSENTIAL if not ess[k]["ok"]]
    important_weak = [k for k in IMPORTANT if report[k]["status"] != "complete"]
    other_weak = [k for k, _, _ in SECTIONS if k not in ESSENTIAL + IMPORTANT and report[k]["status"] != "complete"]
    if not ess["type"]["font_source"]:
        important_weak.append("font_source")

    if essential_missing:
        verdict = "INADEQUATE"
    elif important_weak or other_weak or any(report[k]["status"] != "complete" for k in ESSENTIAL):
        verdict = "GAPS"
    else:
        verdict = "READY"

    return {
        "verdict": verdict,
        "sections": report,
        "essentials": ess,
        "essential_missing": essential_missing,
        "important_weak": important_weak,
        "other_weak": other_weak,
        "sha256": hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest(),
    }


def run(root="."):
    design, others, logos, fonts = find_docs(root)
    result = {"design_md": design[0] if design else None, "other_design_md": design[1:],
              "other_brand_docs": others, "logo_files_in_repo": logos[:20], "font_files_in_repo": fonts[:20]}
    if not design:
        result.update({"verdict": "MISSING"})
    else:
        result.update(assess(root, design[0], logos, fonts))

    prev_path = os.path.join(root, ".brand-design", "preflight.json")
    try:
        prev = json.load(open(prev_path))
        result["previous"] = {"verdict": prev.get("verdict"), "date": prev.get("date"),
                              "unchanged": prev.get("sha256") == result.get("sha256") and prev.get("design_md") == result["design_md"]}
    except (OSError, ValueError):
        result["previous"] = None
    return result


ICON = {"complete": "✔", "partial": "◐", "empty": "◐", "missing": "✘"}


def print_report(r):
    if r["verdict"] == "MISSING":
        print("DESIGN.md preflight: MISSING (no DESIGN.md in this repo)")
        if r["other_brand_docs"]:
            print("Other brand docs found: " + ", ".join(r["other_brand_docs"]))
        if r["logo_files_in_repo"]:
            print("Logo files found: " + ", ".join(r["logo_files_in_repo"][:5]))
        return
    prev = r.get("previous") or {}
    print(f"DESIGN.md preflight: {r['verdict']}  ({r['design_md']})")
    if prev.get("unchanged"):
        print(f"Unchanged since the last preflight on {prev.get('date')} (was {prev.get('verdict')}).")
    if r["other_design_md"]:
        print("Other DESIGN.md files (not read): " + ", ".join(r["other_design_md"]))
    print("\nEssentials")
    for k in ESSENTIAL:
        e = r["essentials"][k]
        vals = ", ".join(e["values"][:6])
        print(f"  {'✔' if e['ok'] else '✘'} {k:<7} {e['detail']}" + (f": {vals}" if vals else ""))
        if k == "logo" and e["missing_files"]:
            print(f"            referenced but not found: {', '.join(e['missing_files'])}")
        if k == "logo" and not e["ok"] and e["unreferenced_in_repo"]:
            print(f"            logo files in the repo DESIGN.md doesn't name: {', '.join(e['unreferenced_in_repo'][:5])}")
    print("\nSections (target: brand-design/assets/DESIGN.template.md)")
    for i, (k, label, _) in enumerate(SECTIONS, 1):
        s = r["sections"][k]
        extra = f"  under \"{s['heading']}\"" if s.get("heading") else ""
        notes = f"  ({'; '.join(s['notes'])})" if s["notes"] else ""
        print(f"  {ICON[s['status']]} {i:>2} {label:<28} {s['status']}{extra}{notes}")


def main():
    args = sys.argv[1:]
    r = run()
    if "--save" in args:
        os.makedirs(".brand-design", exist_ok=True)
        keep = {k: r.get(k) for k in ("verdict", "design_md", "sha256", "essential_missing", "important_weak", "other_weak")}
        keep["date"] = datetime.date.today().isoformat()
        json.dump(keep, open(os.path.join(".brand-design", "preflight.json"), "w"), indent=2)
    if "--json" in args:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print_report(r)


if __name__ == "__main__":
    main()
