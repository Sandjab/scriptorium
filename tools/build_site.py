#!/usr/bin/env python3
"""build_site.py — assemble _site/ pour publication GitHub Pages.

Scanne themes/<slug>/dist/*.html (documents autonomes, CSS + polices inline),
les copie sous _site/<slug>/ et génère _site/index.html : une page d'accueil
navigable qui liste chaque thème et ses documents.

Frontière jugement / code (cf. CLAUDE.md) : ce script ne fait qu'assembler de
façon déterministe. Aucun contenu éditorial n'est inventé ici ; les libellés
sont dérivés mécaniquement des <title> et des noms de fichiers.

Échoue bruyamment si aucun document n'est trouvé.
"""
from __future__ import annotations

import datetime as _dt
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "themes"
SITE_DIR = ROOT / "_site"
TAXONOMY_PATH = Path(__file__).resolve().parent / "taxonomy.json"

# Suffixe de variante (triptyque) -> libellé affiché.
VARIANTS = {
    "pedagogique": "Pédagogique",
    "publication": "Publication",
    "reference": "Référence",
}

# Thème legacy (APO hand-built, gelé) : toujours rendu en dernier, marqué d'un bandeau.
LEGACY_SLUG = "automatic-prompt-optimization"
LEGACY_NOTE = (
    "Édition historique construite à la main (triptyque à 3 éditions), antérieure au "
    "pipeline /monograph — conservée gelée comme golden de référence pour la charte."
)

_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def extract_title(path: Path) -> str:
    """Titre lisible d'un document = contenu de sa balise <title>."""
    m = _TITLE_RE.search(path.read_text(encoding="utf-8", errors="replace"))
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else path.stem


def theme_label(slug: str) -> str:
    """Nom de thème lisible dérivé du slug kebab-case."""
    return slug.replace("-", " ").title()


def collect(themes_dir: Path):
    """[(slug, label, [(href, link_label, full_title), ...]), ...], trié alpha."""
    themes = []
    for theme_dir in sorted(
        (p for p in themes_dir.iterdir() if p.is_dir()), key=lambda p: p.name
    ):
        dist = theme_dir / "dist"
        if not dist.is_dir():
            continue
        docs = []
        for html_file in sorted(dist.glob("*.html")):
            stem = html_file.stem
            variant = stem.rsplit("-", 1)[-1] if "-" in stem else ""
            title = extract_title(html_file)
            link_label = VARIANTS.get(variant, title)
            href = f"{theme_dir.name}/{html_file.name}"
            docs.append((href, link_label, title))
        if docs:
            themes.append((theme_dir.name, theme_label(theme_dir.name), docs))
    return themes


def load_taxonomy(taxonomy_path: Path) -> list[dict]:
    """Lit taxonomy.json, valide la structure ; échoue bruyamment sinon."""
    if not taxonomy_path.is_file():
        raise SystemExit(f"build_site: taxonomy.json manquant : {taxonomy_path}")
    data = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    domains = data.get("domains")
    if not isinstance(domains, list) or not domains:
        raise SystemExit("build_site: 'domains' doit être une liste non vide")
    ids = set()
    for d in domains:
        for key in ("id", "label", "blurb", "themes"):
            if key not in d:
                raise SystemExit(f"build_site: domaine sans clé '{key}': {d!r}")
        if not isinstance(d["themes"], list) or not d["themes"]:
            raise SystemExit(f"build_site: domaine '{d['id']}': 'themes' liste non vide requise")
        if d["id"] in ids:
            raise SystemExit(f"build_site: id de domaine dupliqué : {d['id']}")
        ids.add(d["id"])
    return domains


def group_by_domain(collected, domains, legacy_slug):
    """Croise les thèmes publiés et la taxonomie -> sections ordonnées.

    Retourne une liste de dicts :
      {"kind":"domain","id","label","blurb","themes":[(slug,label,docs),...]}
      {"kind":"unclassified","themes":[...]}   (seulement si non vide)
      {"kind":"legacy","theme":(slug,label,docs)}  (seulement si publié)
    Échoue bruyamment : slug classé sans dist, slug dans 2 domaines, domaine vide,
    slug legacy classé dans un domaine.
    """
    by_slug = {slug: (label, docs) for slug, label, docs in collected}
    seen = set()
    sections = []
    for dom in domains:
        entries = []
        for slug in sorted(dom["themes"]):
            if slug == legacy_slug:
                raise SystemExit(f"build_site: legacy '{slug}' ne doit pas être classé")
            if slug not in by_slug:
                raise SystemExit(
                    f"build_site: thème '{slug}' (domaine '{dom['id']}') sans dist/"
                )
            if slug in seen:
                raise SystemExit(f"build_site: thème '{slug}' classé dans plusieurs domaines")
            seen.add(slug)
            label, docs = by_slug[slug]
            entries.append((slug, label, docs))
        if not entries:
            raise SystemExit(f"build_site: domaine '{dom['id']}' vide")
        sections.append(
            {"kind": "domain", "id": dom["id"], "label": dom["label"],
             "blurb": dom["blurb"], "themes": entries}
        )
    unclassified = sorted(
        s for s in by_slug if s not in seen and s != legacy_slug
    )
    if unclassified:
        sections.append(
            {"kind": "unclassified",
             "themes": [(s, *by_slug[s]) for s in unclassified]}
        )
    if legacy_slug in by_slug:
        label, docs = by_slug[legacy_slug]
        sections.append({"kind": "legacy", "theme": (legacy_slug, label, docs)})
    return sections


def render_index(sections, n_themes, n_docs) -> str:
    """Page d'accueil groupée par domaine — esthétique alignée sur charte.css."""
    e = html.escape
    built = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def render_link(href, lbl, title):
        inner = f'<span class="doc">{e(lbl)}</span>'
        if lbl != title:
            inner += f'<span class="ttl">{e(title)}</span>'
        return f'          <li><a href="{e(href)}">{inner}</a></li>'

    def render_card(slug, label, docs, *, legacy=False):
        links = "\n".join(render_link(*d) for d in docs)
        if legacy:
            return (
                f'        <article class="card legacy">\n'
                f'          <p class="badge-legacy">Legacy</p>\n'
                f'          <h2>{e(label)}</h2>\n'
                f'          <ul>\n{links}\n          </ul>\n'
                f'          <p class="legacy-note">{e(LEGACY_NOTE)}</p>\n'
                f'        </article>'
            )
        return (
            f'        <article class="card">\n'
            f'          <h2>{e(label)}</h2>\n'
            f'          <ul>\n{links}\n          </ul>\n'
            f'        </article>'
        )

    blocks = []
    for sec in sections:
        if sec["kind"] == "legacy":
            slug, label, docs = sec["theme"]
            cards = render_card(slug, label, docs, legacy=True)
            head = '      <h2 class="dhead">Legacy</h2>'
            blurb = ""
        elif sec["kind"] == "unclassified":
            cards = "\n".join(render_card(s, l, d) for s, l, d in sec["themes"])
            head = '      <h2 class="dhead">À classer</h2>'
            blurb = ('      <p class="dblurb">Thèmes publiés pas encore rangés dans '
                     'un domaine (lancer <code>/arrange</code>).</p>')
        else:  # domain
            cards = "\n".join(render_card(s, l, d) for s, l, d in sec["themes"])
            head = f'      <h2 class="dhead">{e(sec["label"])}</h2>'
            blurb = f'      <p class="dblurb">{e(sec["blurb"])}</p>'
        blurb_line = (blurb + "\n") if blurb else ""
        blocks.append(
            f'    <section class="domain">\n{head}\n{blurb_line}'
            f'      <div class="cards">\n{cards}\n      </div>\n    </section>'
        )
    sections_html = "\n".join(blocks)

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Scriptorium — monographies vérifiées</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&family=Spectral:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{{
    --paper:#F4F6FA; --card:#FFFFFF;
    --ink:#15202E; --ink-soft:#43536A; --ink-faint:#7A889B;
    --blue:#23537F; --blue-deep:#142E49; --blue-bright:#2C77B6; --blue-wash:#E7EEF6;
    --bordeaux:#7C2A38; --bordeaux-bright:#9B3443; --bordeaux-wash:#F3E3E6;
    --line:#D7DFE9; --maxw:1100px;
  }}
  *{{box-sizing:border-box;}}
  body{{margin:0;background:var(--paper);color:var(--ink);
    font-family:"Spectral",Georgia,serif;font-size:17px;line-height:1.62;
    -webkit-font-smoothing:antialiased;}}
  h1,h2,.kicker,.doc,.meta span,nav{{font-family:"Archivo",system-ui,sans-serif;}}
  .ttl{{font-family:"Spectral",Georgia,serif;}}

  header.top{{background:linear-gradient(165deg,var(--blue-deep),#0E2236 70%);
    color:#EAF1F8;padding:64px 28px 52px;border-bottom:3px solid var(--bordeaux);}}
  .top-in{{max-width:var(--maxw);margin:0 auto;}}
  .kicker{{font-family:"JetBrains Mono",monospace;font-size:12.5px;letter-spacing:.22em;
    text-transform:uppercase;color:#9DC2E0;margin:0 0 16px;}}
  header.top h1{{font-size:clamp(30px,4.6vw,52px);line-height:1.05;margin:0;
    font-weight:800;letter-spacing:-.01em;}}
  header.top .lede{{font-size:18px;max-width:680px;margin:18px 0 0;color:#C7D7E6;line-height:1.55;}}
  .meta{{margin-top:26px;display:flex;flex-wrap:wrap;gap:10px;}}
  .meta span{{font-size:11.5px;letter-spacing:.04em;border:1px solid rgba(157,194,224,.35);
    color:#B7CFE4;padding:5px 11px;border-radius:2px;font-family:"JetBrains Mono",monospace;}}

  main{{max-width:var(--maxw);margin:0 auto;padding:48px 28px 100px;}}
  .domain{{margin:0 0 46px;}}
  .dhead{{font-size:14px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--bordeaux);margin:0 0 4px;font-weight:700;}}
  .dblurb{{margin:0 0 18px;color:var(--ink-soft);font-size:15px;
    border-bottom:1px solid var(--line);padding-bottom:14px;}}
  .dblurb code{{font-family:"JetBrains Mono",monospace;font-size:13px;color:var(--blue);}}
  .cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:24px;}}
  .card{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--blue);
    border-radius:7px;padding:22px 24px;box-shadow:0 1px 2px rgba(20,46,73,.04);}}
  .card h2{{font-size:19px;margin:0 0 14px;color:var(--blue-deep);font-weight:800;
    letter-spacing:-.005em;}}
  .card ul{{list-style:none;margin:0;padding:0;}}
  .card li{{margin:0 0 4px;}}
  .card a{{display:flex;flex-direction:column;gap:2px;text-decoration:none;
    padding:9px 11px;border-radius:5px;border:1px solid transparent;transition:.15s;}}
  .card a:hover{{background:var(--blue-wash);border-color:var(--line);}}
  .doc{{font-size:14px;font-weight:700;color:var(--bordeaux);letter-spacing:.01em;}}
  .ttl{{font-size:14px;color:var(--ink-soft);line-height:1.4;}}

  .card.legacy{{border-left-color:var(--bordeaux);border-color:var(--bordeaux-bright);}}
  .badge-legacy{{margin:-22px -24px 14px;padding:7px 24px;background:var(--bordeaux);
    color:#fff;font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.22em;
    text-transform:uppercase;border-radius:7px 7px 0 0;}}
  .legacy-note{{margin:16px 0 0;padding-top:13px;border-top:1px solid var(--line);
    font-size:12.5px;line-height:1.5;color:var(--ink-faint);font-style:italic;}}

  footer{{max-width:var(--maxw);margin:0 auto;padding:0 28px 60px;
    color:var(--ink-faint);font-family:"JetBrains Mono",monospace;font-size:12px;
    border-top:1px solid var(--line);padding-top:22px;}}
  footer a{{color:var(--blue-bright);text-decoration:none;}}
</style>
</head>
<body>
  <header class="top">
    <div class="top-in">
      <p class="kicker">Scriptorium · fabrique de monographies</p>
      <h1>Monographies vérifiées</h1>
      <p class="lede">Documents de référence uniques, un par thème : chaque fait
        confirmé s'appuie sur au moins deux sources indépendantes.</p>
      <div class="meta">
        <span>{n_themes} thèmes</span>
        <span>{n_docs} documents</span>
      </div>
    </div>
  </header>
  <main>
{sections_html}
  </main>
  <footer>
    Généré le {built} · <a href="https://github.com/Sandjab/scriptorium">github.com/Sandjab/scriptorium</a>
  </footer>
</body>
</html>
'''


def main() -> int:
    themes = collect()
    if not themes:
        sys.exit(f"build_site: aucun document trouvé sous {THEMES_DIR}/*/dist/*.html")

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    n_docs = 0
    for slug, _, docs in themes:
        (SITE_DIR / slug).mkdir(parents=True, exist_ok=True)
        for href, *_ in docs:
            src = THEMES_DIR / slug / "dist" / Path(href).name
            shutil.copy2(src, SITE_DIR / href)
            n_docs += 1

    (SITE_DIR / "index.html").write_text(render_index(themes), encoding="utf-8")

    print(f"build_site: {len(themes)} thèmes, {n_docs} documents -> {SITE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
