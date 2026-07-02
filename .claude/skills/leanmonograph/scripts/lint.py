#!/usr/bin/env python3
"""Lint déterministe leanmonograph — frontière code/jugement : le CODE détecte les candidats,
le MODÈLE adjuge la posture (affirmé vs critiqué) des flags.

Usage : lint.py <themeDir> [--pre]

Corpus de texte visible :
  - mode post (défaut) : manifest.json + tldr.json + glossary.json
  - mode --pre         : sections_draft.json + tldr.json + glossary.json

Vérifications :
  1. rejected_flags : pivots (chiffres + noms propres distinctifs) des claims REJETÉS
     présents dans le corpus. Chaque flag porte hedged=true si un marqueur de réserve
     (« source unique », « auto-rapporté », « non corroboré »…) figure dans la même unité
     de texte — un flag non hedgé doit être ADJUGÉ par un agent (affirmation → corriger ;
     critique/réfutation du contenu rejeté → OK).
  2. novel_numbers : chiffres significatifs du corpus absents de knowledge.json
     (candidats « faits prose-only » à vérifier en source).

Sortie : JSON sur stdout. Exit 2 s'il existe ≥1 rejected_flag non hedgé, 0 sinon,
1 sur erreur d'usage/fichier.
"""
import json
import pathlib
import re
import sys

HEDGE_RE = re.compile(
    r"(source unique|auto-rapport|non corrobor|non reproduit|non v[ée]rifi"
    r"|sans source ind[ée]pendante|chiffre[s]? non corrobor)", re.I)

# Clés JSON dont la valeur n'est pas du texte visible (identifiants, liens, ancrages).
NON_TEXT_KEYS = {"url", "href", "id", "ref", "slug", "kind", "type", "angle_key",
                 "after_section_id", "anchor", "audit", "edition"}

# Mots capitalisés fréquents en tête de phrase française / vocabulaire générique :
# jamais des pivots distinctifs.
STOP_CAPS = {
    "Le", "La", "Les", "Un", "Une", "Des", "Selon", "Mais", "Pour", "Dans", "Cette",
    "Ces", "Ce", "Cet", "Il", "Elle", "Ils", "Elles", "On", "En", "Au", "Aux", "Par",
    "Avec", "Sans", "Sur", "Sous", "Entre", "Table", "Figure", "Section", "Enfin",
    "Ainsi", "Alors", "Depuis", "Après", "Avant", "Deux", "Trois", "Quatre", "Leur",
    "Leurs", "Nous", "Vous", "Tout", "Toute", "Tous", "Toutes", "Rien", "Plus",
}

NUM_RE = re.compile(r"\d+(?:[   ]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?")
CAPS_RE = re.compile(r"\b[A-Z][A-Za-zÀ-ÿ0-9&-]{3,}\b")
TAG_RE = re.compile(r"<[^>]*>")


def norm_text(s):
    return s.replace(" ", " ").replace(" ", " ")


def strip_tags(s):
    return TAG_RE.sub(" ", s)


def canon_num(raw):
    """« 24 000 » → « 24000 » ; « 87,4 » → « 87.4 »."""
    return raw.replace(" ", "").replace(" ", "").replace(" ", "").replace(",", ".")


def walk_strings(obj, path=""):
    """(chemin, texte) pour chaque chaîne de texte visible d'un JSON."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and k in NON_TEXT_KEYS:
                continue
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield (path, obj)


def significant(canon):
    """Chiffre porteur d'un fait : décimal, ou entier ≥ 100 (années comprises)."""
    if "." in canon:
        return True
    try:
        return int(canon) >= 100
    except ValueError:
        return False


def load(theme, name):
    p = theme / name
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    argv = [a for a in sys.argv[1:] if a != "--pre"]
    pre = "--pre" in sys.argv
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 1
    theme = pathlib.Path(argv[0])
    kb = load(theme, "knowledge.json")
    if kb is None:
        print(json.dumps({"error": "knowledge.json introuvable"}))
        return 1

    corpus_files = (["sections_draft.json"] if pre else ["manifest.json"]) + [
        "tldr.json", "glossary.json"]
    corpus = []  # (fichier, chemin, texte nettoyé)
    for name in corpus_files:
        data = load(theme, name)
        if data is None:
            continue
        for path, s in walk_strings(data):
            corpus.append((name, path, norm_text(strip_tags(s))))

    claims = kb.get("claims", [])
    kept = [c for c in claims if c.get("audit") in ("confirmed", "corrected")]
    rejected = [c for c in claims if c.get("audit") == "rejected"]

    # Univers « connu » : tout chiffre présent quelque part dans knowledge.json.
    known_nums = set()
    for _, _, s in [("kb", p, norm_text(t)) for p, t in walk_strings(kb)]:
        for m in NUM_RE.finditer(s):
            known_nums.add(canon_num(m.group(0)))

    # Vocabulaire des claims retenus : un pivot de claim rejeté qui y figure n'est pas distinctif.
    kept_text = norm_text(" ".join(
        (c.get("statement", "") + " " + " ".join(c.get("examples", []))) for c in kept))
    kept_nums = {canon_num(m.group(0)) for m in NUM_RE.finditer(kept_text)}
    kept_caps = set(CAPS_RE.findall(kept_text))

    # 1. Pivots des claims rejetés dans le corpus.
    rejected_flags = []
    for c in rejected:
        stmt = norm_text(c.get("statement", ""))
        piv_nums = [m.group(0) for m in NUM_RE.finditer(stmt)
                    if canon_num(m.group(0)) not in kept_nums]
        piv_caps = [w for w in CAPS_RE.findall(stmt)
                    if w not in STOP_CAPS and w not in kept_caps]
        pivots = list(dict.fromkeys(piv_nums + piv_caps))
        if not pivots:
            continue
        for fname, path, text in corpus:
            hits, positions = [], []
            for p in pivots:
                m = re.search(r"(?<![\w,.])" + re.escape(p) + r"(?![\w])", text)
                if m:
                    hits.append(p)
                    positions.append(m.start())
            # ≥2 pivots distincts, ou 1 seul pivot déjà très distinctif (≥4 caractères).
            if len(hits) >= 2 or any(len(h) >= 4 for h in hits):
                # Hedge requis PRÈS d'un hit (fenêtre ±350 c.) — un hedge ailleurs dans la
                # même section (p. ex. celui d'un AUTRE claim rejeté) ne couvre pas celui-ci.
                hedged = any(HEDGE_RE.search(text[max(0, i - 350):i + 350])
                             for i in positions)
                i = positions[0]
                rejected_flags.append({
                    "claim": c.get("id"), "file": fname, "path": path, "pivots": hits,
                    "hedged": hedged,
                    "context": text[max(0, i - 120):i + 160].strip(),
                })

    # 2. Chiffres significatifs du corpus absents de knowledge.json.
    novel, seen = [], set()
    for fname, path, text in corpus:
        for m in NUM_RE.finditer(text):
            canon = canon_num(m.group(0))
            if not significant(canon) or canon in known_nums or canon in seen:
                continue
            seen.add(canon)
            i = m.start()
            novel.append({"value": m.group(0), "file": fname, "path": path,
                          "context": text[max(0, i - 100):i + 120].strip()})

    unhedged = [f for f in rejected_flags if not f["hedged"]]
    print(json.dumps({
        "mode": "pre" if pre else "post",
        "rejected_flags": rejected_flags,
        "unhedged_count": len(unhedged),
        "novel_numbers": novel,
    }, ensure_ascii=False, indent=1))
    return 2 if unhedged else 0


if __name__ == "__main__":
    sys.exit(main())
