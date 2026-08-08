#!/usr/bin/env python3
"""build_site.py — assemble _site/ pour publication GitHub Pages.

Scanne themes/<slug>/dist/*.html (documents autonomes, CSS + polices inline),
les copie sous _site/<slug>/ et génère la navigation : _site/index.html, hub
des méta-domaines, et _site/<meta-id>.html, qui liste les thèmes d'un
méta-domaine groupés par domaine.

Frontière jugement / code (cf. CLAUDE.md) : ce script ne fait qu'assembler de
façon déterministe. Aucun contenu éditorial n'est inventé ici ; les libellés
sont dérivés mécaniquement des <title> et des noms de fichiers.

Une seule exception à la copie conforme : si le méta-domaine d'un thème porte une
'notice' (bandeau de non-conseil médical), la copie publiée est RÉÉCRITE pour
l'insérer avant </main>. Le texte vient de taxonomy.json, jamais du script ; les
sources sous themes/<slug>/dist/ ne sont pas touchées.

Échoue bruyamment si aucun document n'est trouvé.
"""
from __future__ import annotations

import datetime as _dt
import html
import json
import re
import shutil
from pathlib import Path

import portal
from portal import PALETTE_CSS

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "themes"
SITE_DIR = ROOT / "_site"
TAXONOMY_PATH = Path(__file__).resolve().parent / "taxonomy.json"
PORTALS_DIR = portal.PORTALS_DIR

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

# L'id d'un méta-domaine devient un nom de fichier à la racine du site
# (_site/<id>.html) : il doit être kebab-case, et 'index' est pris par le hub.
_META_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_META_ID_RESERVE = "index"

# Ancre d'injection de la notice : fin de la colonne de prose. Après </body> le
# bandeau tomberait derrière le colophon et hors de la grille .wrap de charte.css.
NOTICE_ANCHOR = "</main>"


def extract_title(path: Path) -> str:
    """Titre lisible d'un document = contenu de sa balise <title>.

    Déséchappé : le <title> source porte des entités HTML ('&amp;'), et tout
    affichage les ré-échappe — sans ce unescape, un '&' s'afficherait '&amp;'.
    """
    m = _TITLE_RE.search(path.read_text(encoding="utf-8", errors="replace"))
    if not m:
        return path.stem
    return html.unescape(re.sub(r"\s+", " ", m.group(1)).strip())


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
    """Lit taxonomy.json v2 (méta-domaines), valide ; échoue bruyamment sinon.

    Retourne la liste ordonnée des méta-domaines, chacun portant ses domaines.
    """
    if not taxonomy_path.is_file():
        raise SystemExit(f"build_site: taxonomy.json manquant : {taxonomy_path}")
    data = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    if data.get("version") != 2:
        raise SystemExit(f"build_site: {taxonomy_path}: version {data.get('version')!r}, "
                         "version 2 requise (méta-domaines ; cf. "
                         "docs/2026-08-07-meta-domaines-sante-design.md)")
    metas = data.get("meta_domains")
    if not isinstance(metas, list) or not metas:
        raise SystemExit("build_site: 'meta_domains' doit être une liste non vide")
    meta_ids, domain_ids = set(), set()
    for i, m in enumerate(metas):
        for key in ("id", "label", "blurb", "domains"):
            if key not in m:
                raise SystemExit(f"build_site: méta-domaine #{i} "
                                 f"('{m.get('id', '?')}') sans clé '{key}'")
        if m["id"] in meta_ids:
            raise SystemExit(f"build_site: id de méta-domaine dupliqué : {m['id']}")
        meta_ids.add(m["id"])
        if m["id"] == _META_ID_RESERVE:
            raise SystemExit(f"build_site: id de méta-domaine réservé : "
                             f"'{_META_ID_RESERVE}' est le hub du site")
        if not isinstance(m["id"], str) or not _META_ID_RE.match(m["id"]):
            raise SystemExit(f"build_site: id de méta-domaine invalide : {m['id']!r} "
                             "(kebab-case attendu ; il devient un nom de fichier "
                             "à la racine du site)")
        if "notice" in m and (not isinstance(m["notice"], str) or not m["notice"].strip()):
            raise SystemExit(f"build_site: méta-domaine '{m['id']}': 'notice' doit être "
                             "une chaîne non vide si présente")
        if not isinstance(m["domains"], list) or not m["domains"]:
            raise SystemExit(f"build_site: méta-domaine '{m['id']}': "
                             "'domains' liste non vide requise")
        for j, d in enumerate(m["domains"]):
            for key in ("id", "label", "blurb", "themes"):
                if key not in d:
                    raise SystemExit(f"build_site: domaine #{j} ('{d.get('id', '?')}') "
                                     f"du méta-domaine '{m['id']}' sans clé '{key}'")
            if not isinstance(d["themes"], list) or not d["themes"]:
                raise SystemExit(f"build_site: domaine '{d['id']}': "
                                 "'themes' liste non vide requise")
            if d["id"] in domain_ids:
                raise SystemExit(f"build_site: id de domaine dupliqué : {d['id']}")
            domain_ids.add(d["id"])
    return metas


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


def write_portals(sections, themes_dir: Path, portals_dir: Path, site_dir: Path,
                  built: str, meta_by_domain: dict) -> set[str]:
    """Écrit _site/domaines/<id>.html pour chaque domaine ayant un portail.

    L'existence de tools/portals/<id>.json déclare que le domaine en a un.
    `meta_by_domain` associe chaque id de domaine à son méta-domaine, pour que le
    fil d'Ariane du portail passe par la page méta au lieu de sauter au hub.
    Échoue bruyamment sur un portail orphelin (fichier ne correspondant à aucun
    domaine), qui serait sinon ignoré en silence après un renommage de domaine.
    """
    domain_ids = {sec["id"] for sec in sections if sec["kind"] == "domain"}
    if portals_dir.is_dir():
        for path in sorted(portals_dir.glob("*.json")):
            if path.stem not in domain_ids:
                raise SystemExit(
                    f"build_site: portail orphelin '{path.name}' "
                    f"(aucun domaine '{path.stem}' dans la taxonomie)"
                )

    rendered = set()
    for sec in sections:
        if sec["kind"] != "domain":
            continue
        path = portal.portal_path(sec["id"], portals_dir)
        if not path.exists():
            continue
        data = portal.load_portal(path, sec["id"], [s for s, _, _ in sec["themes"]])
        meta = meta_by_domain.get(sec["id"])
        if meta is None:
            raise SystemExit(
                f"build_site: domaine '{sec['id']}' rattaché à aucun méta-domaine "
                "(fil d'Ariane du portail impossible à construire)"
            )
        out = portal.render(sec, data, sec["themes"], themes_dir, built, meta)
        (site_dir / "domaines").mkdir(parents=True, exist_ok=True)
        (site_dir / "domaines" / f"{sec['id']}.html").write_text(out, encoding="utf-8")
        rendered.add(sec["id"])
    return rendered


PAGE_CSS = PALETTE_CSS + """  *{box-sizing:border-box;}
  body{margin:0;background:var(--paper);color:var(--ink);
    font-family:"Spectral",Georgia,serif;font-size:17px;line-height:1.62;
    -webkit-font-smoothing:antialiased;}
  h1,h2,.kicker,.doc,.meta span,nav{font-family:"Archivo",system-ui,sans-serif;}
  .ttl{font-family:"Spectral",Georgia,serif;}

  header.top{background:linear-gradient(165deg,var(--blue-deep),#0E2236 70%);
    color:#EAF1F8;padding:64px 28px 52px;border-bottom:3px solid var(--bordeaux);}
  .top-in{max-width:var(--maxw);margin:0 auto;}
  .kicker{font-family:"JetBrains Mono",monospace;font-size:12.5px;letter-spacing:.22em;
    text-transform:uppercase;color:#9DC2E0;margin:0 0 16px;}
  header.top h1{font-size:clamp(30px,4.6vw,52px);line-height:1.05;margin:0;
    font-weight:800;letter-spacing:-.01em;}
  header.top .lede{font-size:18px;max-width:680px;margin:18px 0 0;color:#C7D7E6;line-height:1.55;}
  .meta{margin-top:26px;display:flex;flex-wrap:wrap;gap:10px;}
  .meta span{font-size:11.5px;letter-spacing:.04em;border:1px solid rgba(157,194,224,.35);
    color:#B7CFE4;padding:5px 11px;border-radius:2px;font-family:"JetBrains Mono",monospace;}

  main{max-width:var(--maxw);margin:0 auto;padding:48px 28px 100px;}
  .domain{margin:0 0 46px;}
  .dhead{font-size:14px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--bordeaux);margin:0 0 4px;font-weight:700;}
  .dblurb{margin:0 0 18px;color:var(--ink-soft);font-size:15px;
    border-bottom:1px solid var(--line);padding-bottom:14px;}
  .dblurb code{font-family:"JetBrains Mono",monospace;font-size:13px;color:var(--blue);}
  .dportal{font-family:"Archivo",system-ui,sans-serif;font-size:13.5px;font-weight:700;
    color:var(--blue-bright);text-decoration:none;margin-left:14px;white-space:nowrap;}
  .dportal:hover{color:var(--bordeaux);}
  .cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:24px;}
  .card{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--blue);
    border-radius:7px;padding:22px 24px;box-shadow:0 1px 2px rgba(20,46,73,.04);}
  .card h2{font-size:19px;margin:0 0 14px;color:var(--blue-deep);font-weight:800;
    letter-spacing:-.005em;}
  .card ul{list-style:none;margin:0;padding:0;}
  .card li{margin:0 0 4px;}
  .card a{display:flex;flex-direction:column;gap:2px;text-decoration:none;
    padding:9px 11px;border-radius:5px;border:1px solid transparent;transition:.15s;}
  .card a:hover{background:var(--blue-wash);border-color:var(--line);}
  .doc{font-size:14px;font-weight:700;color:var(--bordeaux);letter-spacing:.01em;}
  .ttl{font-size:14px;color:var(--ink-soft);line-height:1.4;}

  .card.legacy{border-left-color:var(--bordeaux);border-color:var(--bordeaux-bright);}
  .badge-legacy{margin:-22px -24px 14px;padding:7px 24px;background:var(--bordeaux);
    color:#fff;font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.22em;
    text-transform:uppercase;border-radius:7px 7px 0 0;}
  .legacy-note{margin:16px 0 0;padding-top:13px;border-top:1px solid var(--line);
    font-size:12.5px;line-height:1.5;color:var(--ink-faint);font-style:italic;}

  footer{max-width:var(--maxw);margin:0 auto;padding:0 28px 60px;
    color:var(--ink-faint);font-family:"JetBrains Mono",monospace;font-size:12px;
    border-top:1px solid var(--line);padding-top:22px;}
  footer a{color:var(--blue-bright);text-decoration:none;}
  .card.meta h2 a{color:var(--blue-deep);text-decoration:none;}
  .card.meta h2 a:hover{color:var(--bordeaux);}
  .mblurb{margin:0 0 10px;color:var(--ink-soft);font-size:14.5px;line-height:1.5;}
  .mstats{margin:0;font-family:"JetBrains Mono",monospace;font-size:12px;
    color:var(--ink-faint);}
  .notice-sante{max-width:var(--maxw);margin:18px auto 0;padding:12px 16px;
    border:1px solid var(--bordeaux-bright);border-radius:6px;font-size:14px;
    line-height:1.5;color:#C7D7E6;
    background:color-mix(in srgb, var(--bordeaux) 18%, transparent);}
  .kicker a{color:#9DC2E0;text-decoration:none;border-bottom:1px solid rgba(157,194,224,.4);}
"""


def render_sections(sections, portals=()) -> str:
    """Rend les sections (domaine / à classer / legacy) en HTML.

    `portals` = ids des domaines disposant d'un portail (lien « Parcourir »).
    """
    e = html.escape

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
            blurb = f'      <p class="dblurb">{e(sec["blurb"])}'
            if sec["id"] in portals:
                blurb += (f'<a class="dportal" href="domaines/{e(sec["id"])}.html">'
                          f'Parcourir le domaine &rarr;</a>')
            blurb += '</p>'
        blurb_line = (blurb + "\n") if blurb else ""
        blocks.append(
            f'    <section class="domain">\n{head}\n{blurb_line}'
            f'      <div class="cards">\n{cards}\n      </div>\n    </section>'
        )
    return "\n".join(blocks)


def _shell(page_title: str, header_inner: str, main_html: str) -> str:
    """Squelette HTML commun au hub et aux pages de méta-domaine."""
    e = html.escape
    built = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(page_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&family=Spectral:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{PAGE_CSS}</style>
</head>
<body>
  <header class="top">
    <div class="top-in">
{header_inner}
    </div>
  </header>
  <main>
{main_html}
  </main>
  <footer>
    Généré le {built} · <a href="https://github.com/Sandjab/scriptorium">github.com/Sandjab/scriptorium</a>
  </footer>
</body>
</html>
'''


def render_meta_page(meta, sections, portals=()) -> str:
    """Page d'un méta-domaine : l'ancienne home, ciblée sur ses domaines."""
    e = html.escape
    n_domains = sum(1 for s in sections if s["kind"] == "domain")
    n_themes = sum(len(s["themes"]) for s in sections if s["kind"] == "domain")
    notice = (f'\n      <aside class="notice-sante">{e(meta["notice"])}</aside>'
              if meta.get("notice") else "")
    header = f'''      <p class="kicker"><a href="index.html">Scriptorium</a> · fabrique de monographies</p>
      <h1>{e(meta["label"])}</h1>
      <p class="lede">{e(meta["blurb"])}</p>{notice}
      <div class="meta">
        <span>{n_domains} domaines</span>
        <span>{n_themes} thèmes</span>
      </div>'''
    return _shell(f'Scriptorium — {meta["label"]}', header,
                  render_sections(sections, portals))


def render_hub(metas, tail_sections, n_themes, n_docs) -> str:
    """Home hub : une carte par méta-domaine + buckets À classer / Legacy."""
    e = html.escape
    cards = "\n".join(
        f'''        <article class="card meta">
          <h2><a href="{e(m["id"])}.html">{e(m["label"])} &rarr;</a></h2>
          <p class="mblurb">{e(m["blurb"])}</p>
          <p class="mstats">{m["n_domains"]} domaines · {m["n_themes"]} thèmes</p>
        </article>''' for m in metas)
    body = (f'    <section class="domain">\n'
            f'      <h2 class="dhead">Méta-domaines</h2>\n'
            f'      <div class="cards">\n{cards}\n      </div>\n    </section>')
    if tail_sections:
        body += "\n" + render_sections(tail_sections)
    header = f'''      <p class="kicker">Scriptorium · fabrique de monographies</p>
      <h1>Monographies vérifiées</h1>
      <p class="lede">Documents de référence uniques, un par thème : chaque fait
        confirmé s'appuie sur au moins deux sources indépendantes.</p>
      <div class="meta">
        <span>{n_themes} thèmes</span>
        <span>{n_docs} documents</span>
      </div>'''
    return _shell("Scriptorium — monographies vérifiées", header, body)


def main(themes_dir: Path = THEMES_DIR, taxonomy_path: Path = TAXONOMY_PATH,
         site_dir: Path = SITE_DIR, portals_dir: Path = PORTALS_DIR) -> int:
    collected = collect(themes_dir)
    if not collected:
        raise SystemExit(f"build_site: aucun document sous {themes_dir}/*/dist/*.html")
    metas = load_taxonomy(taxonomy_path)
    all_domains = [d for m in metas for d in m["domains"]]
    sections = group_by_domain(collected, all_domains, LEGACY_SLUG)

    n_themes = len(collected)
    n_docs = sum(len(docs) for _, _, docs in collected)

    # notice éventuelle d'un méta-domaine -> ses slugs (bandeau santé)
    notice_by_slug = {}
    for m in metas:
        if m.get("notice"):
            for d in m["domains"]:
                for slug in d["themes"]:
                    notice_by_slug[slug] = m["notice"]

    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)
    for slug, _, docs in collected:
        (site_dir / slug).mkdir(parents=True, exist_ok=True)
        for href, *_ in docs:
            src = themes_dir / slug / "dist" / Path(href).name
            if slug in notice_by_slug:
                # `callout` vient de charte.css, inlinée dans chaque dist/ : elle
                # porte l'apparence (et suit le mode sombre). `notice-sante-doc`
                # ne sert qu'à identifier le bandeau.
                aside = ('<aside class="notice-sante-doc callout">'
                         + html.escape(notice_by_slug[slug]) + '</aside>')
                content = src.read_text(encoding="utf-8")
                n = content.count(NOTICE_ANCHOR)
                if n != 1:
                    raise SystemExit(
                        f"build_site: {n} balise(s) {NOTICE_ANCHOR} dans {src}, "
                        "exactement une requise pour ancrer la notice")
                (site_dir / href).write_text(
                    content.replace(NOTICE_ANCHOR, aside + "\n" + NOTICE_ANCHOR),
                    encoding="utf-8")
            else:
                shutil.copy2(src, site_dir / href)

    built = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    meta_by_domain = {d["id"]: {"id": m["id"], "label": m["label"]}
                      for m in metas for d in m["domains"]}
    portals = write_portals(sections, themes_dir, portals_dir, site_dir, built,
                            meta_by_domain)

    domain_secs = {s["id"]: s for s in sections if s["kind"] == "domain"}
    tail = [s for s in sections if s["kind"] in ("unclassified", "legacy")]
    hub_metas = []
    for m in metas:
        m_secs = [domain_secs[d["id"]] for d in m["domains"]]
        (site_dir / f"{m['id']}.html").write_text(
            render_meta_page(m, m_secs, portals), encoding="utf-8")
        hub_metas.append({
            "id": m["id"], "label": m["label"], "blurb": m["blurb"],
            "n_domains": len(m_secs),
            "n_themes": sum(len(s["themes"]) for s in m_secs),
        })

    (site_dir / "index.html").write_text(
        render_hub(hub_metas, tail, n_themes, n_docs), encoding="utf-8")
    print(f"build_site: {len(metas)} méta-domaines, {n_themes} thèmes, "
          f"{n_docs} documents, {len(portals)} portails -> {site_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
