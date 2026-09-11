#!/usr/bin/env python3
"""Lint déterministe du CONTRASTE EN THÈME SOMBRE — frontière code/jugement : le CODE mesure
le contraste réel de chaque texte dans un navigateur, le MODÈLE adjuge la réparation.

Usage : lint_contraste_sombre.py <themeDir...> [--seuil 3.0] [--base-url URL] [--limite N]

  lint_contraste_sombre.py themes/backpropagation          # un thème, après son build
  lint_contraste_sombre.py themes/*/                       # balayage du corpus (~2 s/document)

CE QUE CE LINT PROTÈGE, ET POURQUOI

  Un widget embarque son CSS propre mais hérite des variables de la charte. Dès qu'un auteur
  mélange les deux registres — un jeton pour l'encre, une valeur littérale pour le fond — le
  thème sombre casse le couple : l'encre bascule, le fond non. Mesuré le 2026-09-11 sur les
  93 documents de thème : 77 portaient au moins un texte sous 3:1, 2 872 occurrences.

  Aucune relecture ne l'attrape : on regarde le document qu'on vient d'écrire, dont les widgets
  sont récents et corrects, jamais les soixante autres. Seule une MESURE le voit, parce que le
  défaut ne vit ni dans le CSS (qui est syntaxiquement correct) ni dans le HTML, mais dans la
  composition des deux au moment du rendu.

  Le lint ne lit donc PAS les sources : il ouvre le document bâti, force `data-theme="dark"`,
  et relève pour chaque texte visible sa couleur et le fond effectivement peint derrière lui
  (en remontant les ancêtres jusqu'au premier fond opaque). C'est la seule mesure qui ne
  puisse pas mentir — un grep sur `background:#F...` rate le fond posé par JS, et compte pour
  fautif un fond littéral que son auteur a correctement doublé d'une règle sombre.

TROIS FAMILLES, TROIS RÉPARATIONS DIFFÉRENTES — d'où la classification

  Les familles sont déduites de `template/charte.css` (source unique des jetons), jamais
  d'une table recopiée ici : le fond mesuré est comparé aux valeurs sombres des jetons, et
  pour un jeton reconnu c'est l'ÉCART entre sa valeur diurne et sa valeur nocturne qui tranche.

  1. `fond_clair_en_dur`  — le fond n'est aucun jeton et il est clair. Le widget a écrit une
     valeur littérale sans règle `html[data-theme="dark"]`. Réparation : donner au couple sa
     règle sombre, ou tirer fond ET encre des jetons.
  2. `miroir`             — le fond EST un jeton, mais un jeton qui s'ÉCLAIRCIT en sombre
     (`--blue` passe de #23537F à #6FA8D8). Une encre blanche en dur n'y tient plus.
     Réparation : un jeton `--<prefix>-onbright` (#fff en clair, encre sombre en sombre).
     ⚠️ Cette famille-là est INVISIBLE à l'heuristique statique : ces widgets ont souvent
     déjà des règles `data-theme`, donc un grep les tient pour traités.
  3. `encre_en_dur`       — le fond est un jeton sombre, donc correct : c'est l'ENCRE qui est
     littérale et claire-sur-clair. Le symétrique du cas 1.

  `autre` reste pour ce qui n'entre dans aucune : un fond sombre non-jeton. À adjuger à la main.

Sortie : JSON sur stdout — un objet par document, ses occurrences triées par contraste
croissant, et un décompte par famille. Exit 2 s'il existe ≥1 occurrence sous le seuil
(toutes exigent une adjudication), 0 sinon, 1 sur erreur d'usage/fichier/navigateur.

DÉPENDANCE : `agent-browser` (CLI). Le lint ouvre le document en `file://` — les widgets sont
inlinés par build.py, aucune requête réseau n'est nécessaire. Un document servi en HTTP se
mesure avec `--base-url` (démarrer le serveur avec serve.sh, jamais un http.server ad hoc).
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
from typing import NoReturn

HERE = pathlib.Path(__file__).resolve().parent
CHARTE = HERE.parent / "template" / "charte.css"
SESSION = "lint-contraste-sombre"

# Collecteur injecté dans la page : il ne JUGE rien, il relève. Tout le verdict est calculé en
# Python, donc testable sans navigateur. Renvoie [{encre, fond, ou, fondDe, texte}, ...].
SONDE = r"""
(() => {
  const px = c => {
    const m = String(c).match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const hex = c => '#' + [c.r, c.g, c.b]
    .map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  // Le fond EFFECTIF : le premier ancêtre qui peint vraiment quelque chose d'opaque.
  const fondEffectif = el => {
    let n = el;
    while (n && n.nodeType === 1) {
      const c = px(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0.5) return { c, n };
      n = n.parentElement;
    }
    return { c: px(getComputedStyle(document.documentElement).backgroundColor)
                || { r: 255, g: 255, b: 255, a: 1 }, n: null };
  };
  const nomme = el => el ? (el.tagName.toLowerCase()
    + (el.classList.length ? '.' + [...el.classList].join('.') : '')) : 'racine';
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    // Seul le texte porté EN PROPRE compte : sinon un conteneur hérite du verdict de ses enfants.
    const texte = [...el.childNodes]
      .filter(n => n.nodeType === 3).map(n => n.textContent.trim()).filter(Boolean).join(' ');
    if (!texte) continue;
    const box = el.getBoundingClientRect();
    if (!box.width || !box.height) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) === 0) continue;
    const encre = px(cs.color);
    if (!encre || encre.a < 0.5) continue;
    const fond = fondEffectif(el);
    out.push({ encre: hex(encre), fond: hex(fond.c),
               ou: nomme(el), fondDe: nomme(fond.n), texte: texte.slice(0, 60) });
  }
  return JSON.stringify(out);
})()
"""


def die(msg) -> NoReturn:
    raise SystemExit(f"[contraste] ÉCHEC : {msg}")


# --- mesure pure (testable sans navigateur) ---------------------------------

def luminance(h):
    """Luminance relative WCAG d'un `#rrggbb`."""
    h = h.lstrip("#")
    if len(h) != 6:
        die(f"couleur illisible : {h}")
    canaux = []
    for i in (0, 2, 4):
        v = int(h[i:i + 2], 16) / 255
        canaux.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * canaux[0] + 0.7152 * canaux[1] + 0.0722 * canaux[2]


def contraste(a, b):
    """Rapport de contraste WCAG entre deux `#rrggbb` — 1.0 (identiques) à 21.0 (noir/blanc)."""
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _declarations(bloc):
    """Custom properties d'un bloc CSS : {'--blue': '#23537f', ...}. Seules les couleurs
    littérales sont retenues — `--maxw:1240px` n'a rien à faire dans une comparaison de fonds."""
    out = {}
    for d in bloc.split(";"):
        if ":" not in d:
            continue
        nom, val = (x.strip() for x in d.split(":", 1))
        if nom.startswith("--") and re.fullmatch(r"#[0-9A-Fa-f]{6}", val):
            out[nom] = val.lower()
    return out


def jetons_charte(css):
    """{'--blue': ('#23537f', '#6fa8d8'), ...} — valeur CLAIRE et valeur SOMBRE de chaque jeton.

    Lues dans charte.css, jamais recopiées ici : la charte est la source unique, et une table
    locale divergerait au premier ajustement de palette — le lint classerait alors des jetons
    en « fond codé en dur » et enverrait réparer ce qui va bien.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)  # sinon un commentaire colle au 1er jeton du bloc

    def bloc(selecteur):
        i = css.find(selecteur)
        if i < 0:
            die(f"bloc {selecteur} introuvable dans la charte")
        return css[css.index("{", i) + 1:css.index("}", i)]

    clair = _declarations(bloc(":root"))
    sombre = _declarations(bloc('html[data-theme="dark"]'))
    jetons = {nom: (clair[nom], val) for nom, val in sombre.items() if nom in clair}
    if not jetons:
        die("aucun jeton lu dans la charte")
    return jetons


def famille(fond, jetons, clair=0.5):
    """Classe une occurrence par MÉCANISME, parce que la réparation diffère (cf. docstring).

    Le miroir ne se reconnaît pas à une luminance absolue mais à un ÉCART : `--blue` sombre
    (#6FA8D8) n'est pas « clair » dans l'absolu, il est plus clair que sa valeur diurne — et
    c'est cela, et rien d'autre, qui fait lâcher une encre blanche écrite en dur par-dessus.
    """
    f = fond.lower()
    for jour, nuit in jetons.values():
        if nuit == f:
            return "miroir" if luminance(nuit) > luminance(jour) else "encre_en_dur"
    return "fond_clair_en_dur" if luminance(f) > clair else "autre"


def analyse(records, jetons, seuil):
    """Occurrences sous le seuil, la pire d'abord. Le reste est tu : un lint qui liste ce qui
    va bien ne se lit plus."""
    fautes = []
    for r in records:
        ratio = contraste(r["encre"], r["fond"])
        if ratio >= seuil:
            continue
        fautes.append({"contraste": round(ratio, 2), "famille": famille(r["fond"], jetons),
                       "encre": r["encre"], "fond": r["fond"],
                       "ou": r["ou"], "fondDe": r["fondDe"], "texte": r["texte"]})
    fautes.sort(key=lambda f: f["contraste"])
    return fautes


# --- pilotage du navigateur -------------------------------------------------

def _browser(args, entree=None):
    p = subprocess.run(["agent-browser", "--session", SESSION, *args],
                       input=entree, capture_output=True, text=True)
    if p.returncode != 0:
        die(f"agent-browser {args[0]} : {p.stderr.strip() or p.stdout.strip()}")
    return p.stdout


def _dans_la_page(js):
    """Exécute un fragment JS dans la page et renvoie sa valeur (chaîne)."""
    brut = _browser(["eval", "--stdin", "--json"], entree=js)
    try:
        env = json.loads(brut.strip().splitlines()[-1])
    except (ValueError, IndexError):
        die(f"réponse d'agent-browser illisible : {brut.strip()[:200]}")
    if not env.get("success"):
        die(f"exécution refusée dans la page : {env.get('error')}")
    return env["data"]["result"]


def releve(url):
    """Ouvre, bascule en sombre, PUIS mesure — en deux appels séparés : un seul appel lirait
    des valeurs en pleine transition CSS."""
    _browser(["open", url])
    _dans_la_page("document.documentElement.setAttribute('data-theme','dark')")
    return json.loads(_dans_la_page(SONDE))


def documents(theme_dir):
    d = pathlib.Path(theme_dir) / "dist"
    if not d.is_dir():
        die(f"pas de dist/ dans {theme_dir} — bâtir le thème d'abord")
    htmls = sorted(d.glob("*.html"))
    if not htmls:
        die(f"aucun HTML bâti dans {d}")
    return htmls


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("themes", nargs="+", help="dossiers de thème (themes/<slug>)")
    ap.add_argument("--seuil", type=float, default=3.0,
                    help="rapport de contraste sous lequel une occurrence est relevée (défaut 3.0)")
    ap.add_argument("--base-url", default=None,
                    help="servir en HTTP au lieu de file: (racine correspondant à themes/)")
    ap.add_argument("--limite", type=int, default=40,
                    help="occurrences détaillées conservées par document (défaut 40)")
    a = ap.parse_args()

    jetons = jetons_charte(CHARTE.read_text(encoding="utf-8"))
    rapport, total = [], 0
    try:
        for t in a.themes:
            for html in documents(t.rstrip("/")):
                if a.base_url:
                    url = f"{a.base_url.rstrip('/')}/{html.parent.parent.name}/{html.name}"
                else:
                    url = html.resolve().as_uri()
                fautes = analyse(releve(url), jetons, a.seuil)
                total += len(fautes)
                par_famille = {}
                for f in fautes:
                    par_famille[f["famille"]] = par_famille.get(f["famille"], 0) + 1
                rapport.append({"document": str(html), "occurrences": len(fautes),
                                "familles": par_famille, "detail": fautes[:a.limite]})
    finally:
        subprocess.run(["agent-browser", "--session", SESSION, "close"],
                       capture_output=True, text=True)

    familles = {}
    for d in rapport:
        for k, v in d["familles"].items():
            familles[k] = familles.get(k, 0) + v
    json.dump({"seuil": a.seuil, "documents": len(rapport),
               "documents_fautifs": sum(1 for d in rapport if d["occurrences"]),
               "occurrences": total, "familles": familles, "par_document": rapport},
              sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 2 if total else 0


if __name__ == "__main__":
    sys.exit(main())
