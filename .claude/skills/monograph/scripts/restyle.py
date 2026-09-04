#!/usr/bin/env python3
"""restyle.py — outillage de la passe de style, à faits constants.

Usage :
  restyle.py snapshot <themeDir> <dest>            témoin COMPLET de la version committée
  restyle.py dump  <themeDir> [id-de-section ...]   paragraphes réécrivables, avec leur clé
  restyle.py apply <themeDir> <patch.json>          {"<elem>.<par>": "<nouveau contenu>"}
  restyle.py check <themeDir> <manifest-avant.json> compare les invariants et les mesures

POURQUOI CET OUTIL EXISTE

  Réécrire de la prose pour la rendre lisible, c'est toucher au texte publié d'un corpus dont
  la valeur entière tient à l'exactitude. La seule chose qui rend l'opération sûre n'est pas
  la vigilance de celui qui écrit — elle se fatigue, et un agent en réécrit des milliers de
  mots — mais un contrôle déterministe passé à CHAQUE lot :

    1. le multiensemble des NOMBRES est inchangé, élément par élément ;
    2. le multiensemble des nombres ÉCRITS EN TOUTES LETTRES l'est aussi — angle mort connu
       du lint, et le seul écart qu'ait produit le pilote (« deux doses » ajouté en
       reformulant, fait pourtant déductible : reformulé plutôt qu'absorbé) ;
    3. `id`, `type` et `claims` de chaque élément sont inchangés — la prose est une vue des
       faits, jamais leur source.

    4. les NOMS PROPRES et sigles ne disparaissent pas — un contrôle ajouté après que la
       passe a montré que `check` comptait bien les chiffres mais restait aveugle à une
       attribution perdue. Ne sont comparés que les tokens capitalisés hors début de phrase
       (un « Réciproquement » ouvrant une phrase neuve n'est pas une attribution), et seules
       les PERTES sont fautives : un nom répété là où un pronom a été coupé rend
       l'attribution plus explicite, jamais moins.

  Ce que l'outil ne vérifie PAS, et qui reste au jugement : qu'une réserve déplacée reste à
  moins de 350 caractères du chiffre qu'elle qualifie (au-delà, `HEDGE_RE` de lint.py ne la
  voit plus). D'où la règle : après chaque document, relancer lint.py et comparer son rapport
  à celui d'avant — il doit être identique.

  ⚠️ Le témoin se construit avec `snapshot`, jamais à la main. Le lint en mode post lit
  manifest + tldr + glossary + LES WIDGETS ; un témoin auquel il manque `tldr.json` ou
  `widgets/` mesure autre chose que le document et fabrique une régression imaginaire. Les
  deux cas se sont produits dans la même journée, sur scaling-laws puis sur
  entity-linking-disambiguation, et ont chacun coûté une fausse alerte.

  Les figures et les tableaux sont préservés verbatim : `apply` ne remplace que le contenu
  des <p> hors <figure>/<table>, jamais leurs légendes ni leurs libellés SVG.
"""
import collections
import html
import json
import pathlib
import re
import statistics
import sys

FIG_RE = re.compile(r"<figure.*?</figure>|<table.*?</table>", re.S)
TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")
PAR_RE = re.compile(r"<p>(.*?)</p>", re.S)
SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀÉÈÊÎÔÙ«])")
NUM_RE = re.compile(r"\d[\d  .,]*\d|\d")
WORDNUM_RE = re.compile(
    r"\b(deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze"
    r"|seize|vingt|trente|quarante|cinquante|soixante|cent|cents|mille|millions?|milliards?"
    r"|tiers|quarts?|moitié|dizaines?|centaines?|milliers?|demi)\b", re.I)


def manifest_path(theme):
    return pathlib.Path(theme) / "manifest.json"


def load(theme):
    return json.loads(manifest_path(theme).read_text(encoding="utf-8"))


def split_prose(prose):
    """(squelette à jetons, paragraphes, figures) — les figures ne sont jamais touchées."""
    figs = []

    def keep(m):
        figs.append(m.group(0))
        return f"\x00FIG{len(figs) - 1}\x00"

    body = FIG_RE.sub(keep, prose)
    return body, PAR_RE.findall(body), figs


def rebuild(body, pars, figs):
    it = iter(pars)
    out = PAR_RE.sub(lambda m: "<p>" + next(it) + "</p>", body)
    for i, f in enumerate(figs):
        out = out.replace(f"\x00FIG{i}\x00", f)
    return out


def strip_tags(s):
    return html.unescape(TAG_RE.sub(" ", s))


def numbers(prose):
    return collections.Counter(NUM_RE.findall(strip_tags(prose).replace(" ", " ")))


def wordnums(prose):
    return collections.Counter(w.lower() for w in WORDNUM_RE.findall(strip_tags(prose)))


def sentence_lengths(prose):
    txt = re.sub(r"\s+", " ", strip_tags(FIG_RE.sub(" ", prose)))
    return [len(s.split()) for s in SENT_RE.split(txt) if len(s.strip()) > 2]


PROPER_RE = re.compile(r"[A-ZÀ-ÖØ-Þ][\w'’\-]*|[A-Z]{2,}")
ELISION_RE = re.compile(r"^[A-ZÀ-ÖØ-Þ]['’]")


def _canon_proper(tok):
    """« L'EPA » et « EPA » sont le même nom : découper une phrase déplace sans cesse
    l'article élidé, et sans cette normalisation le contrôle criait à la perte sur les
    quatre premiers documents de la passe (EPA 10 → 7, alors que L'EPA passait 0 → 3)."""
    return ELISION_RE.sub("", tok)


def _plain_text(prose):
    return re.sub(r"\s+", " ", strip_tags(FIG_RE.sub(" ", prose)))


def proper_lexicon(prose):
    """Le VOCABULAIRE des noms propres, établi sur la version d'AVANT.

    Un token capitalisé n'est un nom propre que si le texte le montre ailleurs qu'en tête
    de phrase — « Réciproquement » n'y apparaît jamais, « Wikidata » si. Déterminer ce
    vocabulaire une fois, puis compter ses occurrences PARTOUT dans les deux versions, évite
    le faux positif qui a fait échouer la première version de ce contrôle : le découpage
    promeut sans cesse un nom propre en tête de phrase (« … et l'EPA monte » → « L'EPA
    monte. »), et un filtre positionnel appliqué aux deux textes le comptait comme perdu.
    Les sigles et les noms à majuscule interne (mGENRE, CAW-coref) entrent d'office."""
    txt = _plain_text(prose)
    lex = set()
    for m in PROPER_RE.finditer(txt):
        tok = _canon_proper(m.group(0))
        if re.search(r"[A-Z]{2,}", tok) or re.search(r"\w[A-Z]", tok):
            lex.add(tok)
            continue
        before = txt[:m.start()].rstrip()
        if before and before[-1] not in ".!?:»" and not before.endswith("—"):
            lex.add(tok)
    return lex


STRONG_RE = re.compile(r"[A-Z]{2,}|\w[A-Z]")


def strong_names(prose):
    """Tokens qui SONT des noms propres par leur seule forme : sigles (NER, MUC) et noms à
    majuscule interne (mGENRE, CAW-coref, GPT-4). Un tel token apparu de nulle part n'est
    pas un artefact de découpage — c'est un fait inventé."""
    return {t for t in (_canon_proper(x) for x in PROPER_RE.findall(_plain_text(prose)))
            if STRONG_RE.search(t)}


def proper_nouns(prose, lexicon):
    """Occurrences des noms du lexique, sans aucun filtre de position."""
    toks = (_canon_proper(t) for t in PROPER_RE.findall(_plain_text(prose)))
    return collections.Counter(t for t in toks if t in lexicon)


def cmd_snapshot(theme, dest):
    """Témoin de la version COMMITTÉE, avec tout ce que le lint lit en mode post."""
    import shutil
    import subprocess
    theme = pathlib.Path(theme)
    dest = pathlib.Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(["git", "show", f"HEAD:{theme}/manifest.json"],
                          capture_output=True, text=True)
    if head.returncode != 0:
        raise SystemExit(f"[restyle] git show a échoué : {head.stderr.strip()}")
    (dest / "manifest.json").write_text(head.stdout, encoding="utf-8")
    for name in ("knowledge.json", "tldr.json", "glossary.json"):
        if (theme / name).exists():
            shutil.copy(theme / name, dest / name)
    if (theme / "widgets").is_dir():
        shutil.copytree(theme / "widgets", dest / "widgets", dirs_exist_ok=True)
    print(f"[restyle] témoin écrit dans {dest} "
          f"({', '.join(sorted(p.name for p in dest.iterdir()))})")


def cmd_dump(theme, wanted):
    for i, el in enumerate(load(theme)["elements"]):
        if not el.get("prose") or (wanted and el.get("id") not in wanted):
            continue
        _, pars, _ = split_prose(el["prose"])
        print(f"\n@@@@@@ ÉLÉMENT {i} — {el.get('id')} ({len(pars)} §)")
        for j, par in enumerate(pars):
            print(f"\n--- {i}.{j} ---\n{par}")


def cmd_apply(theme, patch_path):
    patch = json.loads(pathlib.Path(patch_path).read_text(encoding="utf-8"))
    m = load(theme)
    for key, new in patch.items():
        i, j = (int(x) for x in key.split("."))
        el = m["elements"][i]
        body, pars, figs = split_prose(el["prose"])
        if j >= len(pars):
            raise SystemExit(f"[restyle] {key} hors bornes ({len(pars)} paragraphes)")
        pars[j] = new
        el["prose"] = rebuild(body, pars, figs)
    # L'indentation du manifeste varie d'un thème à l'autre : la relire plutôt que
    # réécrire tout le fichier, pour que le diff ne porte que sur la prose.
    raw = manifest_path(theme).read_text(encoding="utf-8")
    second = raw.split("\n")[1] if "\n" in raw else "  x"
    indent = len(second) - len(second.lstrip()) or 2
    manifest_path(theme).write_text(
        json.dumps(m, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
    print(f"[restyle] {len(patch)} paragraphes remplacés")


def measure(doc):
    lens = [n for el in doc["elements"] if el.get("prose")
            for n in sentence_lengths(el["prose"])]
    words = sum(len(strip_tags(FIG_RE.sub(" ", el["prose"])).split())
                for el in doc["elements"] if el.get("prose"))
    if not lens:
        return None
    return (words, statistics.mean(lens), statistics.median(lens),
            100.0 * sum(1 for x in lens if x > 45) / len(lens), max(lens))


def cmd_check(theme, before_path):
    before = json.loads(pathlib.Path(before_path).read_text(encoding="utf-8"))
    after = load(theme)
    ok = True
    for i, (b, a) in enumerate(zip(before["elements"], after["elements"])):
        if not b.get("prose"):
            continue
        for label, fn in (("nombres", numbers), ("nombres en toutes lettres", wordnums)):
            nb, na = fn(b["prose"]), fn(a["prose"])
            if nb != na:
                ok = False
                print(f"[restyle] ÉCART — élément {i} ({a.get('id')}) : {label}")
                for k in sorted(set(nb) | set(na)):
                    if nb[k] != na[k]:
                        print(f"    « {k} » : {nb[k]} → {na[k]}")
        lex = proper_lexicon(b["prose"])
        pb, pa = proper_nouns(b["prose"], lex), proper_nouns(a["prose"], lex)
        perdus = {k: (pb[k], pa[k]) for k in pb if pa[k] < pb[k]}
        if perdus:
            # SIGNALÉ, jamais bloquant : une occurrence de moins peut être une répétition
            # devenue inutile (« Sur le DHA, … le statut en DHA ») comme une attribution
            # remplacée par un pronom, ce que la passe s'interdit. Le code ne sait pas
            # trancher ; bloquer pousserait à réinjecter des noms pour faire taire l'outil.
            print(f"[restyle] À ADJUGER — élément {i} ({a.get('id')}) : noms propres en "
                  f"baisse (répétition supprimée = OK ; attribution remplacée par un "
                  f"pronom = à réparer)")
            for k, (x, y) in sorted(perdus.items()):
                print(f"    « {k} » : {x} → {y}")
        for k in ("id", "type", "claims"):
            if b.get(k) != a.get(k):
                ok = False
                print(f"[restyle] ÉCART — élément {i} : {k} modifié")
    # Sens inverse, proposé par un agent de la passe : un nom propre PERDU peut être une
    # répétition devenue inutile, mais un nom propre APPARU ne peut pas être un artefact de
    # découpage. Comparé sur le document ENTIER, car une réécriture déplace légitimement une
    # mention d'une section à l'autre.
    avant_forts = set().union(*(strong_names(e["prose"]) for e in before["elements"]
                                if e.get("prose")), set())
    apres_forts = set().union(*(strong_names(e["prose"]) for e in after["elements"]
                                if e.get("prose")), set())
    inventes = sorted(apres_forts - avant_forts)
    if inventes:
        print("[restyle] À ADJUGER — sigles ou noms propres APPARUS (un nom qui n'était "
              "pas là est un fait ajouté, sauf graphie changée) :")
        for t in inventes:
            print(f"    « {t} »")
    print("✅ nombres et références identiques" if ok else "❌ écart détecté")
    for label, doc in (("avant", before), ("après", after)):
        m = measure(doc)
        if m:
            print(f"  {label} : {m[0]:5d} mots · {m[1]:5.1f} mots/phrase · "
                  f"médiane {m[2]:4.0f} · {m[3]:5.1f} % >45 · max {m[4]}")
    return 0 if ok else 2


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 1
    cmd, theme = sys.argv[1], sys.argv[2]
    if cmd == "snapshot":
        cmd_snapshot(theme, sys.argv[3])
        return 0
    if cmd == "dump":
        cmd_dump(theme, set(sys.argv[3:]))
        return 0
    if cmd == "apply":
        cmd_apply(theme, sys.argv[3])
        return 0
    if cmd == "check":
        return cmd_check(theme, sys.argv[3])
    print(__doc__, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
