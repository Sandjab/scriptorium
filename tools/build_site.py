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
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "themes"
SITE_DIR = ROOT / "_site"

# Suffixe de variante (triptyque) -> libellé affiché.
VARIANTS = {
    "pedagogique": "Pédagogique",
    "publication": "Publication",
    "reference": "Référence",
}

_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def extract_title(path: Path) -> str:
    """Titre lisible d'un document = contenu de sa balise <title>."""
    m = _TITLE_RE.search(path.read_text(encoding="utf-8", errors="replace"))
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else path.stem


def theme_label(slug: str) -> str:
    """Nom de thème lisible dérivé du slug kebab-case."""
    return slug.replace("-", " ").title()


def collect():
    """[(slug, label, [(href, link_label, full_title), ...]), ...] trié."""
    themes = []
    for theme_dir in sorted(p for p in THEMES_DIR.iterdir() if p.is_dir()):
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


def render_index(themes) -> str:
    """Page d'accueil — esthétique alignée sur charte.css (tokens, polices)."""
    e = html.escape
    n_docs = sum(len(docs) for _, _, docs in themes)
    built = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def render_link(href, lbl, title):
        # Doc unique : lbl == title -> une seule ligne (pas de sous-titre redondant).
        inner = f'<span class="doc">{e(lbl)}</span>'
        if lbl != title:
            inner += f'<span class="ttl">{e(title)}</span>'
        return f'        <li><a href="{e(href)}">{inner}</a></li>'

    cards = []
    for _, label, docs in themes:
        links = "\n".join(render_link(*d) for d in docs)
        cards.append(
            f'''      <article class="card">
        <h2>{e(label)}</h2>
        <ul>
{links}
        </ul>
      </article>'''
        )
    cards_html = "\n".join(cards)

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

  main{{max-width:var(--maxw);margin:0 auto;padding:48px 28px 100px;
    display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:24px;}}
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
        <span>{len(themes)} thèmes</span>
        <span>{n_docs} documents</span>
      </div>
    </div>
  </header>
  <main>
{cards_html}
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
