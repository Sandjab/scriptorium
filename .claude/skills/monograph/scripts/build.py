#!/usr/bin/env python3
# build.py — assembleur déterministe. Usage: build.py <theme_dir>
import json, re, sys, pathlib
import components as C

TPL = pathlib.Path(__file__).resolve().parent.parent / "template"
EDITIONS = ["reference", "publication", "pedagogique"]

def die(msg): raise SystemExit(f"[build] ÉCHEC : {msg}")
def read(p): return pathlib.Path(p).read_text(encoding="utf-8")

def load_widgets(theme):
    d = pathlib.Path(theme) / "widgets"
    return {p.stem: p.read_text(encoding="utf-8") for p in d.glob("*.html")} if d.exists() else {}

REQUIRED_META = ("title", "kicker", "h1", "lede")

def validate_manifest(manifest):
    for k in ("slug", "meta", "elements"):
        if k not in manifest:
            die(f"clé de manifeste manquante : {k}")
    for k in REQUIRED_META:
        if k not in manifest["meta"]:
            die(f"clé meta manquante : {k}")

def validate_refs(manifest, kb, widgets):
    claim_ids = {c["id"] for c in kb.get("claims", [])}
    for el in manifest["elements"]:
        if el.get("type") not in C.RENDERERS:
            die(f"type d'élément inconnu : {el.get('type')}")
        for cid in el.get("claims", []):
            if cid not in claim_ids:
                die(f"référence de fait inconnue : {cid} (élément {el.get('id', el['type'])})")
        if el["type"] == "widget" and el["ref"] not in widgets:
            die(f"widget inconnu : {el['ref']}")

def structural_checks(htmls):
    for name, s in htmls.items():
        if "file:///" in s: die(f"{name} : file:/// résiduel")
        for tag in ("section", "details", "script"):
            o, c = len(re.findall(rf"<{tag}\b", s)), s.count(f"</{tag}>")
            if o != c: die(f"{name} : <{tag}> déséquilibré ({o} ouverts / {c} fermés)")
        for tok in re.findall(r"<!--%[A-Z_]+%-->", s):
            die(f"{name} : jeton non substitué {tok}")

def render_edition(manifest, ctx):
    body = "\n".join(C.RENDERERS[el["type"]](el, ctx) for el in manifest["elements"])
    meta = manifest["meta"]
    chips = "".join(f"<span>{C.esc(x)}</span>" for x in meta.get("meta_chips", []))
    repl = {"TITLE": C.esc(meta["title"]), "FONTS": ctx["fonts"], "CHARTE": ctx["charte"],
            "KICKER": C.esc(meta["kicker"]), "H1": meta["h1"], "LEDE": meta["lede"],
            "META": chips, "TOC": C.render_toc(manifest), "MAIN": body,
            "THEME_LAYER": ctx["theme_layer"], "FOOTER": C.esc(meta.get("footer",""))}
    out = ctx["base"]
    for k, v in repl.items():
        out = out.replace(f"<!--%{k}%-->", v)
    return out

def build_theme(theme):
    theme = pathlib.Path(theme)
    kb = json.loads(read(theme/"knowledge.json"))
    ctx = {"fonts": read(TPL/"fonts.css"), "charte": read(TPL/"charte.css"),
           "base": read(TPL/"base.html"), "theme_layer": read(TPL/"theme-layer.html"),
           "glossary": json.loads(read(theme/"glossary.json")),
           "tldr": json.loads(read(theme/"tldr.json")),
           "widgets": load_widgets(theme), "kb": kb}
    htmls = {}
    for ed in EDITIONS:
        mp = theme/"editions"/f"{ed}.manifest.json"
        if not mp.exists():
            continue
        manifest = json.loads(read(mp))
        validate_manifest(manifest)
        validate_refs(manifest, kb, ctx["widgets"])
        htmls[f"{manifest['slug']}-{ed}.html"] = render_edition(manifest, ctx)
    if not htmls:
        die(f"aucun manifeste d'édition dans {theme}/editions/")
    structural_checks(htmls)
    (theme/"dist").mkdir(exist_ok=True)
    for name, html in htmls.items():
        (theme/"dist"/name).write_text(html, encoding="utf-8")
        print(f"[build] écrit dist/{name} ({len(html)} o)")

if __name__ == "__main__":
    if len(sys.argv) != 2: die("usage: build.py <theme_dir>")
    build_theme(sys.argv[1])
