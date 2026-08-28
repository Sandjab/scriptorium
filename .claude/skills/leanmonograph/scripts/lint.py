#!/usr/bin/env python3
"""Lint déterministe leanmonograph — frontière code/jugement : le CODE détecte les candidats,
le MODÈLE adjuge la posture (affirmé vs critiqué) des flags.

Usage : lint.py <themeDir> [--pre]

Corpus de texte visible :
  - mode post (défaut) : manifest.json + tldr.json + glossary.json + widgets/*.html
                         (texte visible seul, <script>/<style> retirés ; les widgets ne
                         participent qu'au check rejected_flags, pas à novel_numbers)
  - mode --pre         : sections_draft.json + tldr.json + glossary.json
                         (les widgets ne sont pas encore bâtis à ce stade)

Vérifications :
  1. rejected_flags : pivots (chiffres + noms propres distinctifs) des claims REJETÉS
     présents dans le corpus. Chaque flag porte hedged=true si un marqueur de réserve
     (« source unique », « auto-rapporté », « non corroboré »…) figure dans la même unité
     de texte — un flag non hedgé doit être ADJUGÉ par un agent (affirmation → corriger ;
     critique/réfutation du contenu rejeté → OK).
  2. novel_numbers : chiffres significatifs du corpus absents de knowledge.json
     (candidats « faits prose-only » à vérifier en source).
  3. foreign_statements : claims REJETÉS dont le statement n'est pas en français
     (heuristique de mots-outils). Leurs pivots textuels ne peuvent PAS matcher une
     prose française (« universal solver » vs « agent universel ») : le mécanisme
     rejected_flags est aveugle pour eux — l'agent doit adjuger MANUELLEMENT la
     présence du contenu dans la prose (cas world-models claim:12, 4e trou).
  4. low_rank_sources : claims RETENUS dont l'appareil de preuve repose sur des
     sources de rang nul (presse, encyclopédie collaborative, dépôt social, blog,
     vendeur). Le contrôle d'acceptation du build COMPTE les sources sans jamais
     juger ce qu'elles valent : il valide « 2 sources » sans voir que l'une est un
     marchand de compléments. C'est ce trou qui a laissé passer, au 45e run, un
     claim retenu porté par trois sites de rang nul dont un vendeur de retraites,
     et au 46e run deux entrées `nootroo.com` (un vendeur de nootropiques) citées
     en bibliographie sur l'histoire d'un terme, plus l'exception `document-source`
     invoquée sur un miroir PR Newswire au lieu du document officiel.

Sortie : JSON sur stdout. Exit 2 s'il existe ≥1 rejected_flag non hedgé, ≥1
foreign_statement, OU ≥1 claim CONFIRMÉ sans deux sources de rang réel et sans
exception document-source déclarée (tous exigent une adjudication), 0 sinon,
1 sur erreur d'usage/fichier.
"""
import json
import pathlib
import re
import sys

HEDGE_RE = re.compile(
    r"(source unique|auto-rapport|non corrobor|non reproduit|non v[ée]rifi"
    r"|sans source ind[ée]pendante|chiffre[s]? non corrobor)", re.I)

# ── Rang des sources (check 4) ────────────────────────────────────────────────────────────
# Le CODE ne classe QUE ce qui est indiscutablement sans valeur probante par nature : il ne
# tente pas de juger la qualité d'une revue ou d'un éditeur, qui reste au modèle. Une entrée
# signalée ici n'est pas nécessairement fautive — un claim méthodologique peut légitimement
# citer la presse qu'il décrit, un claim d'absence peut s'appuyer sur une recherche déclarée.
# D'où la règle : on SIGNALE tout, on ne BLOQUE que le cas dur (un `confirmed` sans deux
# sources de rang réel, hors exception document-source déclarée).
#
# Volontairement ABSENT de cette liste : examine.com, que la doctrine santé classe en rang
# MOYEN (agrégateur sérieux mais secondaire) et non nul — cf. docs/evidence-sante.md.
LOW_RANK_HOSTS = (
    # encyclopédies collaboratives et bases tertiaires
    "wikipedia.org", "wiktionary.org", "wikiwand.com", "wikidata.org", "drugs.com",
    # presse générale, presse spécialisée grand public, agrégateurs d'actualité
    "healio.com", "statnews.com", "medscape.com", "neurosciencenews.com", "sciencedaily.com",
    "nutraingredients.com", "webmd.com", "healthline.com", "doctissimo.fr", "futura-sciences.com",
    "health.harvard.edu", "sciencealert.com", "theconversation.com",
    # fils de communiqués : republient un texte officiel sans être le document officiel
    "prnewswire.com", "businesswire.com", "eurekalert.org", "globenewswire.com",
    # dépôts sociaux et hébergeurs : une copie d'article n'est pas sa source citable
    "researchgate.net", "academia.edu", "scribd.com", "slideshare.net",
    # blogs et plateformes d'écriture personnelle
    "medium.com", "substack.com", "wordpress.com", "blogspot.", "gwern.net",
    # forums
    "reddit.com", "quora.com", "stackexchange.com",
)
# Marchands : reconnus sur le NOM DE DOMAINE seul (jamais le chemin — « /shop/ » sur un site
# d'agence n'en fait pas un vendeur). C'est la classe qui a produit les deux défauts les plus
# graves du corpus : un appareil de preuve exact dans son contenu, faux dans ses sources.
VENDOR_HINTS = ("nootro", "supplement", "vitamin", "sarms", "peptide", "biohack",
                "bodybuilding", "myprotein", "iherb", "vitacost", ".shop", ".store")
# Communiqué reconnu au chemin — MAIS un communiqué d'AGENCE publié sur le site de l'agence
# EST le document officiel (avis FDA, action conjointe FTC, point presse de l'ANSM) : il est
# recevable, et c'est même la forme sous laquelle beaucoup de décisions réglementaires
# existent. La distinction n'est donc pas « communiqué ou non » mais QUI le publie : sur le
# site de l'autorité, c'est la source ; ailleurs, c'est une reprise.
PRESS_PATH_RE = re.compile(r"/(pressroom|press-room|press-release|news-release|newsroom|"
                           r"press-announcements|communique)", re.I)
OFFICIAL_HOST_RE = re.compile(
    r"(\.gov$|\.gov\.[a-z]{2}$|\.gouv\.fr$|\.europa\.eu$|\.int$|\.canada\.ca$|\.admin\.ch$"
    r"|sante\.fr$|\.who\.int$|\.nih\.gov$|cochrane\.org$)", re.I)
# L'exception document-source doit être DÉCLARÉE dans l'audit_note (cf. decideAudit et les
# trois workflows) : sans déclaration, un confirmed mono-source reste un défaut.
DOC_SOURCE_RE = re.compile(r"(document.source|source unique par nature|par nature)", re.I)


def source_rank(url):
    """Retourne None si la source est recevable comme preuve, sinon la raison du rang nul."""
    u = (url or "").strip().lower()
    if not u:
        return "sans url"
    host = re.sub(r"^https?://", "", u).split("/")[0]
    official = bool(OFFICIAL_HOST_RE.search(host))
    for h in LOW_RANK_HOSTS:
        if h in host:
            return f"rang nul : {h}"
    for v in VENDOR_HINTS:
        if v in host:
            return f"marchand probable : {host}"
    if PRESS_PATH_RE.search(u) and not official:
        return "communiqué de presse (hors site de l'autorité qui l'émet)"
    return None

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

# Mots-outils pour l'heuristique de langue d'un statement (fréquences relatives ;
# un titre anglais cité dans un statement français n'apporte que 2-3 mots-outils EN,
# noyés sous les mots-outils FR de la phrase porteuse).
EN_STOP_WORDS = {
    "the", "of", "and", "with", "that", "this", "these", "those", "is", "are", "was",
    "were", "be", "been", "can", "cannot", "could", "not", "no", "only", "from", "for",
    "to", "in", "on", "by", "as", "an", "it", "its", "their", "which", "show", "shows",
    "shown", "prove", "proves", "proven", "when", "where", "than", "into", "across",
}
FR_STOP_WORDS = {
    "le", "la", "les", "de", "des", "du", "et", "que", "qui", "une", "un", "pour",
    "dans", "sur", "est", "sont", "pas", "ne", "au", "aux", "par", "avec", "ce",
    "cette", "ces", "se", "son", "sa", "ses", "plus", "comme", "entre", "leur",
    "leurs", "vers", "sous", "sans", "dont", "où", "même", "selon", "être", "été",
}


def foreign_statement(stmt):
    """(is_foreign, en, fr) — un statement est « étranger » si les mots-outils anglais
    dominent nettement les français (≥3 EN et EN > FR). Déterministe, sans dépendance."""
    words = re.findall(r"[a-zà-ÿ']+", stmt.lower())
    en = sum(w in EN_STOP_WORDS for w in words)
    fr = sum(w in FR_STOP_WORDS for w in words)
    return (en >= 3 and en > fr, en, fr)

NUM_RE = re.compile(r"\d+(?:[   ]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?")
CAPS_RE = re.compile(r"\b[A-Z][A-Za-zÀ-ÿ0-9&-]{3,}\b")
TAG_RE = re.compile(r"<[^>]*>")
# Blocs non visibles d'un widget HTML : JS/CSS bourrés de nombres (coords SVG, couleurs)
# qui ne sont PAS du texte rendu — à retirer avant strip_tags.
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)


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
    corpus = []  # (fichier, chemin, texte nettoyé) — alimente les DEUX checks
    for name in corpus_files:
        data = load(theme, name)
        if data is None:
            continue
        for path, s in walk_strings(data):
            corpus.append((name, path, norm_text(strip_tags(s))))

    # Widgets (mode post seulement — ils n'existent pas encore au --pre). build.py inline
    # leur HTML verbatim dans le dist ; leurs légendes/notes/labels SVG sont donc du texte
    # VISIBLE, mais absents du manifeste (référencés par `ref`, une clé non-texte). On les
    # scanne UNIQUEMENT pour rejected_flags — leurs nombres jouets (coords, ticks) ne sont
    # pas des faits de prose et pollueraient novel_numbers.
    widget_corpus = []
    if not pre:
        wdir = theme / "widgets"
        if wdir.exists():
            for wp in sorted(wdir.glob("*.html")):
                visible = strip_tags(SCRIPT_STYLE_RE.sub(" ", wp.read_text(encoding="utf-8")))
                widget_corpus.append((f"widgets/{wp.name}", "(texte visible)", norm_text(visible)))

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

    # 1. Pivots des claims rejetés dans le corpus. Comme pour kept_text, les `examples`
    # comptent : les noms propres d'un claim vivent souvent là, pas dans le statement.
    rejected_flags = []
    for c in rejected:
        stmt = norm_text(c.get("statement", "") + " " + " ".join(c.get("examples", [])))
        piv_nums = [m.group(0) for m in NUM_RE.finditer(stmt)
                    if canon_num(m.group(0)) not in kept_nums]
        piv_caps = [w for w in CAPS_RE.findall(stmt)
                    if w not in STOP_CAPS and w not in kept_caps]
        pivots = list(dict.fromkeys(piv_nums + piv_caps))
        if not pivots:
            continue
        for fname, path, text in corpus + widget_corpus:
            hits, positions = [], []
            for p in pivots:
                if any(ch.isdigit() for ch in p):
                    # Matching CANONIQUE : un pivot « 5.1 » (statement en anglais)
                    # doit matcher « 5,1 » dans la prose française, et inversement.
                    target = canon_num(p)
                    m = next((mm for mm in NUM_RE.finditer(text)
                              if canon_num(mm.group(0)) == target), None)
                else:
                    m = re.search(r"(?<![\w,.])" + re.escape(p) + r"(?![\w])", text)
                if m:
                    hits.append(p)
                    positions.append(m.start())
            # ≥2 pivots distincts, ou 1 seul pivot déjà très distinctif : nombre ≥4
            # caractères (« 0,927 », « 2019 ») ou mot ≥6 (« Hariharan ») — les mots
            # courts de titres (« Does », « REST »), fréquents dans les `examples`,
            # et les petits entiers (« 34 ») ne suffisent pas seuls.
            def alone(h):
                if any(ch.isdigit() for ch in h):
                    return len(h) >= 4
                return len(h) >= 6
            if len(hits) >= 2 or any(alone(h) for h in hits):
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

    # 3. Statements de claims rejetés non français : pivots textuels structurellement
    # aveugles (aucun mot anglais ne matchera la prose française) — à adjuger à la main.
    foreign = []
    for c in rejected:
        stmt = c.get("statement", "")
        is_foreign, en, fr = foreign_statement(stmt)
        if is_foreign:
            foreign.append({
                "claim": c.get("id"), "en_stopwords": en, "fr_stopwords": fr,
                "statement_head": stmt[:140],
                "note": "pivots textuels aveugles (statement non français) : vérifier "
                        "manuellement que la prose n'affirme pas ce contenu sans hedge",
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

    # 4. Rang des sources des claims RETENUS. Le seuil ≥2 est tenu en amont par le code du
    # workflow ; ce qu'aucun contrôle ne regardait, c'est ce que VALENT ces sources.
    by_id = {s.get("id"): s for s in kb.get("sources", [])}
    low_rank = []
    for c in kept:
        flagged, strong = [], 0
        for sid in c.get("sources", []):
            src = by_id.get(sid, {})
            reason = source_rank(src.get("url"))
            if reason:
                flagged.append({"id": sid, "url": src.get("url", ""), "reason": reason})
            else:
                strong += 1
        if not flagged or strong >= 2:
            continue
        declared = bool(DOC_SOURCE_RE.search(c.get("audit_note", "") or ""))
        low_rank.append({
            "claim": c.get("id"),
            "audit": c.get("audit"),
            "sources_of_real_rank": strong,
            "document_source_declared": declared,
            # Ne bloque que la garantie DURE du projet : un fait `confirmed` s'appuie sur
            # ≥2 sources indépendantes — et une source de rang nul n'en est pas une.
            "blocking": c.get("audit") == "confirmed" and not declared,
            "flagged_sources": flagged,
            "statement": (c.get("statement", "") or "")[:180],
            "adjudication": "un claim CORRIGÉ, un claim d'absence ou un claim méthodologique "
                            "peut légitimement citer ces sources — vérifier que l'énoncé ne "
                            "REPOSE pas sur elles ; un claim CONFIRMÉ doit être re-sourcé, ou "
                            "déclarer l'exception document-source sur le document OFFICIEL "
                            "(jamais sur un miroir de presse)",
        })
    blocking = [f for f in low_rank if f["blocking"]]

    unhedged = [f for f in rejected_flags if not f["hedged"]]
    print(json.dumps({
        "mode": "pre" if pre else "post",
        "rejected_flags": rejected_flags,
        "unhedged_count": len(unhedged),
        "foreign_statements": foreign,
        "novel_numbers": novel,
        "low_rank_sources": low_rank,
        "low_rank_blocking": len(blocking),
    }, ensure_ascii=False, indent=1))
    return 2 if (unhedged or foreign or blocking) else 0


if __name__ == "__main__":
    sys.exit(main())
