"""Tests du contrôle de STYLE DE PROSE de lint.py (check 5, leanmonograph/scripts/lint.py).

Lancer :  python3 -m pytest .claude/skills/monograph/scripts/test_lint_prose_style.py

CE QUE CES TESTS PROTÈGENT, ET POURQUOI

  Une mesure sur les 90 documents publiés a montré une phrase moyenne à 30 mots, un tiers
  des phrases au-dessus de 35 et une sur six au-dessus de 45 : un régime auquel un document
  se relit mal, sans qu'aucun fait y soit en cause. La cause est structurelle — une phrase
  qui tente de porter à la fois le résultat, son attribution, sa population et sa réserve.
  Sans contrôle chiffré, chaque run reproduit le motif, et la dette repart.

  Deux intentions sont encodées ici, et la seconde compte autant que la première :

  1. Le check MESURE et SIGNALE, section par section, pour que l'agent sache où découper.
  2. Le check NE BLOQUE JAMAIS. La lisibilité n'est pas une question de vérité : un document
     exact mais lourd doit sortir, un document fluide mais faux doit être arrêté. Confondre
     les deux ferait du style un motif de rejet et de la vérité une affaire de forme. C'est
     `test_le_style_ne_bloque_jamais` qui tient cette frontière — s'il tombe un jour parce
     qu'on a ajouté prose_style au code de sortie, c'est le code de sortie qu'il faut
     corriger, pas le test.
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LINT = HERE.parent.parent / "leanmonograph" / "scripts" / "lint.py"


def _load_lint():
    spec = importlib.util.spec_from_file_location("lean_lint_style", LINT)
    assert spec is not None and spec.loader is not None, f"lint.py introuvable : {LINT}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lint = _load_lint()

COURT = ("<p>Le mot ne désigne pas une substance. Il désigne une position. "
         "Trois molécules comptent ici. La première vient des végétaux. "
         "Les deux autres viennent des poissons.</p>")

LONG = ("<p>La conversion emprunte une voie de désaturation-élongation, où des enzymes "
        "appelées désaturases insèrent des doubles liaisons pendant que des élongases "
        "rallongent la chaîne de deux carbones à chaque passage, et l'insertion de la "
        "première double liaison sur l'acide alpha-linolénique, opérée par une enzyme "
        "particulière, en constitue l'étape limitante que toute la suite du dossier "
        "suppose connue du lecteur qui voudrait la vérifier lui-même en primaire.</p>")


# ── La mesure elle-même ───────────────────────────────────────────────────────────────────
def test_les_phrases_sont_comptees_une_a_une():
    assert lint.sentence_lengths(COURT) == [7, 4, 4, 5, 6]


def test_une_figure_ne_compte_pas_comme_de_la_prose():
    """Les légendes et les libellés SVG d'une figure ne sont pas de la prose suivie :
    les compter ferait varier la mesure avec le nombre de figures, pas avec l'écriture."""
    avec_figure = COURT + "<figure><svg><text>un libellé très long qui ne doit rien peser " \
                          "dans la mesure de la prose rédigée</text></svg>" \
                          "<figcaption>une légende</figcaption></figure>"
    assert lint.sentence_lengths(avec_figure) == lint.sentence_lengths(COURT)


# ── Le seuil : ce qui est signalé, ce qui ne l'est pas ────────────────────────────────────
def _theme(tmp_path, prose):
    (tmp_path / "knowledge.json").write_text(
        json.dumps({"theme": "t", "sources": [], "claims": []}, ensure_ascii=False),
        encoding="utf-8")
    (tmp_path / "manifest.json").write_text(
        json.dumps({"meta": {}, "elements": [{"type": "section", "id": "s1", "prose": prose}]},
                   ensure_ascii=False), encoding="utf-8")
    return tmp_path


def _run(theme, *args):
    p = subprocess.run([sys.executable, str(LINT), str(theme), *args],
                       capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout)


def test_une_prose_courte_nest_pas_signalee(tmp_path):
    _, out = _run(_theme(tmp_path, COURT))
    assert out["prose_style"]["sections_over"] == []
    assert out["prose_style"]["median_words"] <= lint.STYLE_MEDIAN_MAX


def test_une_prose_a_phrases_longues_est_signalee_avec_sa_section(tmp_path):
    _, out = _run(_theme(tmp_path, LONG))
    over = out["prose_style"]["sections_over"]
    assert len(over) == 1, over
    assert over[0]["section"] == "s1"
    assert over[0]["median_words"] > lint.STYLE_MEDIAN_MAX
    assert over[0]["longest"] >= 45


def test_le_style_ne_bloque_jamais(tmp_path):
    """La frontière du projet : le style se signale, la vérité seule arrête un run.
    Une prose illisible mais exacte sort avec exit 0."""
    code, out = _run(_theme(tmp_path, LONG))
    assert out["prose_style"]["sections_over"], "le cas de test doit bien être signalé"
    assert out["prose_style"]["blocking"] is False
    assert code == 0


def test_le_mode_pre_lit_le_brouillon_de_sections(tmp_path):
    """Au --pre, le manifeste n'existe pas encore : la mesure doit porter sur
    sections_draft.json, sinon le contrôle arrive trop tard pour servir à l'auteur."""
    (tmp_path / "knowledge.json").write_text(
        json.dumps({"theme": "t", "sources": [], "claims": []}, ensure_ascii=False),
        encoding="utf-8")
    (tmp_path / "sections_draft.json").write_text(
        json.dumps([{"id": "brouillon", "heading": "h", "prose": LONG}], ensure_ascii=False),
        encoding="utf-8")
    code, out = _run(tmp_path, "--pre")
    assert code == 0
    assert [s["section"] for s in out["prose_style"]["sections_over"]] == ["brouillon"]


def test_une_fin_de_paragraphe_est_une_fin_de_phrase(tmp_path):
    """Un paragraphe qui se termine par « : », un bloc de formule sans ponctuation finale
    et le paragraphe suivant se recollaient en une « phrase » de 70 mots qui n'existe pas.
    L'artefact suffisait à maintenir une section de rlhf-dpo au-dessus du seuil alors
    qu'aucune de ses phrases ne dépassait 45 mots."""
    prose = ("<p>Trois variantes se distinguent :</p>"
             "<p>L(θ) = −log σ(β log π(y|x))</p>"
             "<p>Chacune modifie un terme de cette perte, et le choix du terme décide de "
             "la robustesse observée sur les jeux de préférences bruités.</p>")
    _, out = _run(_theme(tmp_path, prose))
    lens = out["prose_style"]
    assert lens["sentences"] == 3, out["prose_style"]
    assert lens["pct_over_45"] == 0.0
