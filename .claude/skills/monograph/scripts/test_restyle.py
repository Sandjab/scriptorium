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


# ── Contrôle des noms propres (ajouté après le premier lot de la rétro-passe) ─────────────
def test_une_attribution_perdue_fait_echouer_le_check(tmp_path):
    """`check` comptait les chiffres et restait aveugle à une attribution : un agent l'a
    signalé après avoir réécrit un document entier. Perdre « Finkel et Manning » en gardant
    tous les nombres produirait un texte exact et non attribuable."""
    prose = "<p>Le gain de 16,5 points est établi par Finkel et Manning.</p>"
    theme, before = _theme(tmp_path, prose)
    p = _patch(theme, {"0.0": "Le gain de 16,5 points est établi par les auteurs."})
    _run("apply", theme, p)
    code, out = _run("check", theme, before)
    assert "À ADJUGER" in out and "Finkel" in out and "Manning" in out
    # signalé, jamais bloquant : le code ne sait pas distinguer une répétition devenue
    # inutile d'une attribution remplacée par un pronom — c'est au rédacteur d'adjuger.
    assert code == 0


def test_un_nom_repete_apres_decoupage_ne_fait_pas_echouer_le_check(tmp_path):
    """Couper une phrase oblige souvent à remplacer un pronom par le nom : l'attribution
    devient plus explicite, jamais moins. Seules les PERTES sont fautives."""
    prose = "<p>Le système CAW-coref atteint 88,2 points, ce qui le place en tête.</p>"
    theme, before = _theme(tmp_path, prose)
    p = _patch(theme, {"0.0": "Le système CAW-coref atteint 88,2 points. "
                              "Ce score place CAW-coref en tête."})
    _run("apply", theme, p)
    code, out = _run("check", theme, before)
    assert code == 0, out


def test_une_majuscule_de_debut_de_phrase_nest_pas_une_attribution(tmp_path):
    """Un mot ordinaire promu en tête de phrase par le découpage (« Réciproquement »,
    « Chacun ») ne doit pas être compté comme un nom propre — sinon le contrôle crie à
    chaque coupe."""
    prose = "<p>Le modèle progresse, réciproquement la base recule de 3 points.</p>"
    theme, before = _theme(tmp_path, prose)
    p = _patch(theme, {"0.0": "Le modèle progresse. Réciproquement, la base recule de "
                              "3 points."})
    _run("apply", theme, p)
    assert _run("check", theme, before)[0] == 0


def test_snapshot_emporte_tout_ce_que_le_lint_lit(tmp_path):
    """Deux fausses alertes dans la même journée : un témoin sans tldr.json, puis un témoin
    sans widgets/. Le lint en mode post les lit tous les deux — un témoin incomplet mesure
    autre chose que le document."""
    import subprocess
    theme = tmp_path / "themes" / "t"
    (theme / "widgets").mkdir(parents=True)
    for name in ("manifest.json", "knowledge.json", "tldr.json", "glossary.json"):
        (theme / name).write_text('{"elements": []}', encoding="utf-8")
    (theme / "widgets" / "w.html").write_text("<div>widget</div>", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "x"], cwd=tmp_path, check=True)
    dest = tmp_path / "temoin"
    subprocess.run([sys.executable, str(RESTYLE), "snapshot", "themes/t", str(dest)],
                   cwd=tmp_path, check=True, capture_output=True)
    noms = {p.name for p in dest.iterdir()}
    assert {"manifest.json", "knowledge.json", "tldr.json", "glossary.json",
            "widgets"} <= noms, noms
    assert (dest / "widgets" / "w.html").exists()


def test_un_sigle_apparu_est_signale(tmp_path):
    """Sens inverse du contrôle d'attributions, proposé par un agent de la passe : un nom
    PERDU peut être une répétition devenue inutile, mais un sigle APPARU ne peut pas être un
    artefact de découpage — c'est un fait ajouté."""
    prose = "<p>Le modèle atteint 88,2 points sur le jeu de test.</p>"
    theme, before = _theme(tmp_path, prose)
    p = _patch(theme, {"0.0": "Le modèle atteint 88,2 points sur OntoNotes."})
    _run("apply", theme, p)
    code, out = _run("check", theme, before)
    assert "APPARUS" in out and "OntoNotes" in out
    assert code == 0        # signalé, pas bloquant


def test_un_nom_deplace_dune_section_a_lautre_nest_pas_signale(tmp_path):
    """Comparaison sur le document ENTIER : une réécriture déplace légitimement une mention
    d'une section à l'autre, et la signaler à chaque fois rendrait le contrôle inaudible."""
    (tmp_path / "manifest.json").write_text(json.dumps(
        {"meta": {}, "elements": [
            {"type": "section", "id": "a", "prose": "<p>BLINK atteint 88,2 points.</p>"},
            {"type": "section", "id": "b", "prose": "<p>Le score reste stable à 3 %.</p>"}]},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    before = tmp_path / "avant.json"
    before.write_text((tmp_path / "manifest.json").read_text(encoding="utf-8"),
                      encoding="utf-8")
    p = _patch(tmp_path, {"1.0": "Le score de BLINK reste stable à 3 %."})
    _run("apply", tmp_path, p)
    code, out = _run("check", tmp_path, before)
    assert "APPARUS" not in out, out


def test_les_phrases_se_comptent_paragraphe_par_paragraphe(tmp_path):
    """Même défaut que dans le lint : sans frontière de paragraphe, une intro finissant par
    « : », une formule et la suite ne font qu'une phrase — et la mesure ment."""
    prose = ("<p>Trois variantes se distinguent :</p>"
             "<p>L(θ) = −log σ(β log π(y|x))</p>"
             "<p>Chacune modifie un terme de cette perte.</p>")
    assert restyle.sentence_lengths(prose) == [5, 6, 7]
