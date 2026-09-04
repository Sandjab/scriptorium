#!/usr/bin/env python3
"""restyle.py — outillage de la passe de style, à faits constants.

Usage :
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

  Ce que l'outil ne vérifie PAS, et qui reste au jugement : qu'aucune attribution n'ait été
  perdue, et qu'une réserve déplacée reste à moins de 350 caractères du chiffre qu'elle
  qualifie (au-delà, `HEDGE_RE` de lint.py ne la voit plus). D'où la règle : après chaque
  document, relancer lint.py et comparer son rapport à celui d'avant — il doit être identique.

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
        for k in ("id", "type", "claims"):
            if b.get(k) != a.get(k):
                ok = False
                print(f"[restyle] ÉCART — élément {i} : {k} modifié")
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
