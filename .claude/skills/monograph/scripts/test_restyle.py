"""Tests de restyle.py — l'outillage de la passe de style à faits constants.

Lancer :  python3 -m pytest .claude/skills/monograph/scripts/test_restyle.py

CE QUE CES TESTS PROTÈGENT

  La passe de style réécrit du texte PUBLIÉ. Ce qui la rend sûre n'est pas la vigilance de
  celui qui écrit — elle se fatigue, et un agent en réécrit des milliers de mots — mais un
  contrôle déterministe passé à chaque lot. Ces tests vérifient que le contrôle attrape
  vraiment ce qu'il prétend attraper, et que l'application ne casse pas ce qu'elle ne doit
  pas toucher :

  - un chiffre perdu, ajouté ou modifié FAIT ÉCHOUER le check (exit 2) ;
  - un nombre écrit EN TOUTES LETTRES aussi — c'est l'angle mort du lint, et le seul écart
    qu'ait produit le pilote omega-3 ;
  - une figure et son SVG traversent `apply` verbatim : la prose se réécrit, l'appareil
    graphique jamais ;
  - `claims` ne bouge pas — la prose est une vue des faits, jamais leur source.
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
RESTYLE = HERE / "restyle.py"


def _load():
    spec = importlib.util.spec_from_file_location("restyle", RESTYLE)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


restyle = _load()

FIGURE = ("<figure><svg viewBox='0 0 10 10'><text>42 unités mesurées</text></svg>"
          "<figcaption>une légende de figure</figcaption></figure>")
PROSE = ("<p>Trois essais donnent 21,3 % contre 11,3 %, soit près du double.</p>"
         + FIGURE +
         "<p>La revue Cochrane agrège 45 essais et 143 693 participants.</p>")


def _theme(tmp_path, prose=PROSE):
    (tmp_path / "manifest.json").write_text(json.dumps(
        {"meta": {}, "elements": [
            {"type": "section", "id": "s1", "claims": ["claim:1"], "prose": prose}]},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    before = tmp_path / "avant.json"
    before.write_text((tmp_path / "manifest.json").read_text(encoding="utf-8"),
                      encoding="utf-8")
    return tmp_path, before


def _run(*args):
    p = subprocess.run([sys.executable, str(RESTYLE), *map(str, args)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def _patch(tmp_path, mapping):
    f = tmp_path / "patch.json"
    f.write_text(json.dumps(mapping, ensure_ascii=False), encoding="utf-8")
    return f


# ── Ce qui doit passer ────────────────────────────────────────────────────────────────────
def test_un_decoupage_a_faits_constants_passe(tmp_path):
    theme, before = _theme(tmp_path)
    p = _patch(theme, {"0.0": "Trois essais donnent 21,3 %. C'est contre 11,3 %, "
                              "soit près du double."})
    _run("apply", theme, p)
    code, out = _run("check", theme, before)
    assert code == 0, out
    assert "identiques" in out


def test_la_figure_et_son_svg_traversent_verbatim(tmp_path):
    theme, before = _theme(tmp_path)
    p = _patch(theme, {"0.1": "La revue Cochrane agrège 45 essais. Ils totalisent "
                              "143 693 participants."})
    _run("apply", theme, p)
    after = json.loads((theme / "manifest.json").read_text(encoding="utf-8"))
    assert FIGURE in after["elements"][0]["prose"]
    assert _run("check", theme, before)[0] == 0


# ── Ce qui doit échouer ───────────────────────────────────────────────────────────────────
def test_un_chiffre_modifie_fait_echouer_le_check(tmp_path):
    theme, before = _theme(tmp_path)
    p = _patch(theme, {"0.0": "Trois essais donnent 21,5 % contre 11,3 %."})
    _run("apply", theme, p)
    code, out = _run("check", theme, before)
    assert code == 2 and "nombres" in out


def test_un_chiffre_perdu_fait_echouer_le_check(tmp_path):
    theme, before = _theme(tmp_path)
    p = _patch(theme, {"0.1": "La revue Cochrane agrège 45 essais."})
    _run("apply", theme, p)
    assert _run("check", theme, before)[0] == 2


def test_un_nombre_en_toutes_lettres_ajoute_fait_echouer_le_check(tmp_path):
    """L'angle mort du lint : « deux doses » ajouté en reformulant est invisible à un
    contrôle qui ne regarde que les chiffres. C'est le seul écart qu'ait produit le pilote."""
    theme, before = _theme(tmp_path)
    p = _patch(theme, {"0.0": "Trois essais comparent deux doses : 21,3 % contre 11,3 %."})
    _run("apply", theme, p)
    code, out = _run("check", theme, before)
    assert code == 2 and "toutes lettres" in out


def test_une_reference_de_claim_modifiee_fait_echouer_le_check(tmp_path):
    """La prose est une VUE des faits : elle ne peut jamais changer ce qu'une section cite."""
    theme, before = _theme(tmp_path)
    m = json.loads((theme / "manifest.json").read_text(encoding="utf-8"))
    m["elements"][0]["claims"] = ["claim:2"]
    (theme / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=2),
                                         encoding="utf-8")
    code, out = _run("check", theme, before)
    assert code == 2 and "claims" in out
