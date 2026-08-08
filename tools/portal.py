#!/usr/bin/env python3
"""portal.py — rend le portail d'un domaine (page de navigation).

Un portail donne ce qu'aucune monographie ne peut contenir : l'ordre d'entrée dans
un domaine, les arêtes entre ses thèmes, les frontières entre voisins proches.

Frontière jugement / code (cf. CLAUDE.md) : la couche éditoriale (intro, parcours,
arêtes, délimitations) est JUGÉE par /arrange et vit dans tools/portals/<id>.json ;
le corps de la page est DÉRIVÉ mécaniquement (label du thème, thèse de son
tldr.json, liens vers ses documents). Aucun contenu éditorial n'est inventé ici.

Aucun fait vérifiable n'a sa place dans un portail — ni chiffre, ni date, ni
attribution, ni mesure : c'est ce qui l'exempte légitimement du council. Un tel
énoncé est un claim, et sa place est le knowledge.json d'une monographie.

Échoue bruyamment sur toute incohérence entre un portail et sa taxonomie.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

PORTALS_DIR = Path(__file__).resolve().parent / "portals"

# Palette partagée avec build_site.py : foyer unique, pour que la home et les
# portails ne dérivent pas l'un de l'autre.
PALETTE_CSS = """  :root{
    --paper:#F4F6FA; --card:#FFFFFF;
    --ink:#15202E; --ink-soft:#43536A; --ink-faint:#7A889B;
    --blue:#23537F; --blue-deep:#142E49; --blue-bright:#2C77B6; --blue-wash:#E7EEF6;
    --bordeaux:#7C2A38; --bordeaux-bright:#9B3443; --bordeaux-wash:#F3E3E6;
    --line:#D7DFE9; --maxw:1100px;
  }
"""


def portal_path(domain_id: str, portals_dir: Path = PORTALS_DIR) -> Path:
    """Chemin du portail d'un domaine. Son existence déclare que le domaine en a un."""
    return portals_dir / f"{domain_id}.json"


def _require_list_of_dicts(data, key: str, domain_id: str, fields: tuple[str, ...]):
    """Valide data[key] : liste de dicts portant tous les champs attendus, non vides."""
    items = data.get(key, [])
    if not isinstance(items, list):
        raise SystemExit(f"portal: '{domain_id}': '{key}' doit être une liste")
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise SystemExit(f"portal: '{domain_id}': {key}[{i}] doit être un objet")
        for f in fields:
            if not str(item.get(f, "")).strip():
                raise SystemExit(f"portal: '{domain_id}': {key}[{i}] sans '{f}' non vide")
    return items


def load_portal(path: Path, domain_id: str, domain_slugs) -> dict:
    """Charge et valide le portail d'un domaine contre les thèmes de ce domaine.

    Échoue bruyamment : JSON invalide, champ obligatoire manquant, 'domain' qui ne
    correspond pas au fichier, slug hors domaine, doublon dans le parcours, ou
    thème du domaine absent du parcours (un thème publié ne doit jamais devenir
    invisible dans le portail de son domaine).
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"portal: '{domain_id}': JSON invalide ({exc})") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"portal: '{domain_id}': racine JSON attendue = objet")

    if data.get("domain") != domain_id:
        raise SystemExit(
            f"portal: '{domain_id}': champ 'domain' = {data.get('domain')!r}, "
            f"attendu {domain_id!r}"
        )
    if not str(data.get("intro", "")).strip():
        raise SystemExit(f"portal: '{domain_id}': 'intro' non vide requise")

    parcours = _require_list_of_dicts(data, "parcours", domain_id, ("slug", "pourquoi"))
    if not parcours:
        raise SystemExit(f"portal: '{domain_id}': 'parcours' liste non vide requise")

    known = set(domain_slugs)
    seen = set()
    for step in parcours:
        slug = step["slug"]
        if slug not in known:
            raise SystemExit(
                f"portal: '{domain_id}': parcours cite '{slug}', hors du domaine"
            )
        if slug in seen:
            raise SystemExit(f"portal: '{domain_id}': '{slug}' en double dans le parcours")
        seen.add(slug)
    manquants = sorted(known - seen)
    if manquants:
        raise SystemExit(
            f"portal: '{domain_id}': thèmes du domaine absents du parcours : "
            f"{', '.join(manquants)}"
        )

    aretes = _require_list_of_dicts(data, "aretes", domain_id, ("de", "vers", "lien"))
    delims = _require_list_of_dicts(
        data, "delimitations", domain_id, ("a", "b", "frontiere")
    )
    for key, items, fields in (("aretes", aretes, ("de", "vers")),
                               ("delimitations", delims, ("a", "b"))):
        for i, item in enumerate(items):
            for f in fields:
                if item[f] not in known:
                    raise SystemExit(
                        f"portal: '{domain_id}': {key}[{i}].{f} = '{item[f]}', "
                        f"hors du domaine"
                    )

    return {"domain": domain_id, "intro": data["intro"].strip(),
            "parcours": parcours, "aretes": aretes, "delimitations": delims}


def thesis_of(themes_dir: Path, slug: str) -> str:
    """Thèse d'un thème, lue dans themes/<slug>/tldr.json (déjà vérifiée à la source).

    Dérivée, jamais stockée dans le portail : une monographie mise à jour rafraîchit
    son portail au build suivant. Échoue bruyamment si elle manque.
    """
    path = themes_dir / slug / "tldr.json"
    if not path.exists():
        raise SystemExit(f"portal: thème '{slug}' sans {path.name} (thèse indisponible)")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"portal: thème '{slug}': tldr.json invalide ({exc})") from exc
    these = str(data.get("these", "")).strip() if isinstance(data, dict) else ""
    if not these:
        raise SystemExit(f"portal: thème '{slug}': 'these' vide dans tldr.json")
    return these


_SOUS_TITRE_RE = re.compile(r"\s*[:—]\s*")


def short_title(title: str) -> str:
    """Nom court d'un thème : le titre de sa monographie privé de son sous-titre.

    Dérivé, comme le reste : « Décodage et sampling : des logits aux tokens » se
    cite « Décodage et sampling » dans une arête, là où le titre complet noierait
    la relation qu'on veut montrer. Les deux séparateurs employés dans le corpus
    sont le deux-points et le tiret cadratin.
    """
    court = _SOUS_TITRE_RE.split(title, maxsplit=1)[0].strip()
    return court or title.strip()


PORTAL_CSS = PALETTE_CSS + """  *{box-sizing:border-box;}
  body{margin:0;background:var(--paper);color:var(--ink);
    font-family:"Spectral",Georgia,serif;font-size:17px;line-height:1.62;
    -webkit-font-smoothing:antialiased;}
  h1,h2,h3,.kicker,.meta span,.step-n,.why,.edge b,.delim b{
    font-family:"Archivo",system-ui,sans-serif;}

  header.top{background:linear-gradient(165deg,var(--blue-deep),#0E2236 70%);
    color:#EAF1F8;padding:64px 28px 52px;border-bottom:3px solid var(--bordeaux);}
  .top-in{max-width:var(--maxw);margin:0 auto;}
  .kicker{font-family:"JetBrains Mono",monospace;font-size:12.5px;letter-spacing:.22em;
    text-transform:uppercase;color:#9DC2E0;margin:0 0 16px;}
  .kicker a{color:#9DC2E0;text-decoration:none;border-bottom:1px solid rgba(157,194,224,.4);}
  header.top h1{font-size:clamp(30px,4.6vw,52px);line-height:1.05;margin:0;
    font-weight:800;letter-spacing:-.01em;}
  header.top .lede{font-size:18px;max-width:720px;margin:18px 0 0;color:#C7D7E6;
    line-height:1.55;}
  .meta{margin-top:26px;display:flex;flex-wrap:wrap;gap:10px;}
  .meta span{font-size:11.5px;letter-spacing:.04em;border:1px solid rgba(157,194,224,.35);
    color:#B7CFE4;padding:5px 11px;border-radius:2px;font-family:"JetBrains Mono",monospace;}

  main{max-width:var(--maxw);margin:0 auto;padding:48px 28px 100px;}
  .block{margin:0 0 52px;}
  .dhead{font-size:14px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--bordeaux);margin:0 0 4px;font-weight:700;}
  .dblurb{margin:0 0 22px;color:var(--ink-soft);font-size:15px;
    border-bottom:1px solid var(--line);padding-bottom:14px;}

  ol.steps{list-style:none;margin:0;padding:0;counter-reset:step;}
  .step{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--blue);
    border-radius:7px;padding:20px 24px;margin:0 0 14px;
    box-shadow:0 1px 2px rgba(20,46,73,.04);}
  .step-n{counter-increment:step;font-family:"JetBrains Mono",monospace;font-size:11.5px;
    letter-spacing:.18em;color:var(--ink-faint);margin:0 0 6px;}
  .step-n::before{content:counter(step,decimal-leading-zero);}
  .step h3{margin:0 0 8px;font-size:19px;font-weight:800;letter-spacing:-.005em;}
  .step h3 a{color:var(--blue-deep);text-decoration:none;
    border-bottom:2px solid var(--blue-wash);}
  .step h3 a:hover{border-bottom-color:var(--blue-bright);}
  .step h3 a + a{margin-left:12px;font-size:14px;color:var(--bordeaux);}
  .why{margin:0 0 8px;font-size:14.5px;color:var(--blue);font-weight:600;}
  .these{margin:0;font-size:15px;color:var(--ink-soft);line-height:1.55;
    padding-top:10px;border-top:1px solid var(--line);}

  ul.edges,ul.delims{list-style:none;margin:0;padding:0;}
  .edge,.delim{background:var(--card);border:1px solid var(--line);border-radius:6px;
    padding:14px 18px;margin:0 0 10px;font-size:15px;color:var(--ink-soft);}
  .edge{border-left:3px solid var(--blue-bright);}
  .delim{border-left:3px solid var(--bordeaux-bright);}
  .edge b,.delim b{color:var(--blue-deep);font-weight:700;font-size:14px;}
  .arrow{font-family:"JetBrains Mono",monospace;color:var(--ink-faint);padding:0 6px;}

  footer{max-width:var(--maxw);margin:0 auto;padding:0 28px 60px;
    color:var(--ink-faint);font-family:"JetBrains Mono",monospace;font-size:12px;
    border-top:1px solid var(--line);padding-top:22px;}
  footer a{color:var(--blue-bright);text-decoration:none;}
"""


def render(domain: dict, data: dict, entries, themes_dir: Path, built: str,
           meta: dict) -> str:
    """HTML du portail. `entries` = [(slug, label, docs)] du domaine, docs = [(href, lbl, titre)].

    Les hrefs collectés sont relatifs à la racine du site ; la page vit dans
    domaines/, d'où le préfixe '../'.

    `meta` = {"id", "label"} du méta-domaine qui contient ce domaine. Obligatoire :
    le fil d'Ariane traverse les deux étages de la taxonomie (hub -> méta -> domaine),
    et un défaut optionnel rétablirait en silence le saut de niveau qu'on corrige ici.
    """
    e = html.escape
    by_slug = {slug: (label, docs) for slug, label, docs in entries}

    def nom_court(slug: str) -> str:
        docs = by_slug[slug][1]
        return short_title(docs[0][2])

    steps = []
    for step in data["parcours"]:
        slug = step["slug"]
        docs = by_slug[slug][1]
        links = " ".join(
            f'<a href="../{e(href)}">{e(titre if i == 0 else lbl)}</a>'
            for i, (href, lbl, titre) in enumerate(docs)
        )
        steps.append(
            f'      <li class="step">\n'
            f'        <p class="step-n"></p>\n'
            f'        <h3>{links}</h3>\n'
            f'        <p class="why">{e(step["pourquoi"])}</p>\n'
            f'        <p class="these">{e(thesis_of(themes_dir, slug))}</p>\n'
            f'      </li>'
        )
    steps_html = "\n".join(steps)

    def block(title, blurb, body):
        return (f'    <section class="block">\n'
                f'      <h2 class="dhead">{e(title)}</h2>\n'
                f'      <p class="dblurb">{e(blurb)}</p>\n'
                f'{body}\n    </section>')

    blocks = [block(
        "Parcours de lecture",
        "Un ordre d'entrée dans le domaine : chaque étape dit pourquoi elle vient là, "
        "puis reprend la thèse de sa monographie.",
        f'      <ol class="steps">\n{steps_html}\n      </ol>',
    )]

    if data["aretes"]:
        items = "\n".join(
            f'        <li class="edge"><b>{e(nom_court(a["de"]))}</b>'
            f'<span class="arrow">&rarr;</span>'
            f'<b>{e(nom_court(a["vers"]))}</b> — {e(a["lien"])}</li>'
            for a in data["aretes"]
        )
        blocks.append(block(
            "Ce qui relie les thèmes",
            "Les dépendances de lecture que chaque monographie, prise isolément, ne dit pas.",
            f'      <ul class="edges">\n{items}\n      </ul>',
        ))

    if data["delimitations"]:
        items = "\n".join(
            f'        <li class="delim"><b>{e(nom_court(d["a"]))}</b>'
            f'<span class="arrow">|</span>'
            f'<b>{e(nom_court(d["b"]))}</b> — {e(d["frontiere"])}</li>'
            for d in data["delimitations"]
        )
        blocks.append(block(
            "Frontières entre voisins",
            "Deux thèmes proches se recouvrent en surface : voici ce qui les sépare.",
            f'      <ul class="delims">\n{items}\n      </ul>',
        ))

    n = len(data["parcours"])
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(domain["label"])} — portail de domaine</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&family=Spectral:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{PORTAL_CSS}</style>
</head>
<body>
  <header class="top">
    <div class="top-in">
      <p class="kicker"><a href="../index.html">Scriptorium</a> · <a href="../{e(meta["id"])}.html">{e(meta["label"])}</a> · portail de domaine</p>
      <h1>{e(domain["label"])}</h1>
      <p class="lede">{e(data["intro"])}</p>
      <div class="meta">
        <span>{n} monographies</span>
        <span>parcours de lecture</span>
      </div>
    </div>
  </header>
  <main>
{chr(10).join(blocks)}
  </main>
  <footer>
    Généré le {built} · <a href="../index.html">retour à l'accueil</a>
  </footer>
</body>
</html>
'''
