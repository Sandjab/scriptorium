"""Tests du contrôle des CO-AUTEURS de lint.py (check 5, leanmonograph/scripts/lint.py).

Lancer :  python3 -m pytest .claude/skills/monograph/scripts/test_lint_shared_authors.py

CE QUE CES TESTS PROTÈGENT, ET POURQUOI

  Le seuil « ≥ 2 sources indépendantes » est tenu en code par `docKeys`/`collectSources`, qui
  reconnaissent un même travail à un identifiant (arXiv, DOI) ou à un titre commun. Au 84e run
  (weather-forecasting-ml), une dizaine de claims RETENUS sont passés sur deux « sources » qui
  n'en faisaient qu'une :

    - le préprint arXiv de GenCast (« GenCast: Diffusion-based ensemble forecasting… ») et sa
      version Nature lue sur PMC (« Probabilistic weather forecasting with machine learning ») :
      ni identifiant ni titre communs — même Semantic Scholar les tient pour deux articles ;
    - GraphCast et GenCast, deux articles distincts de la même équipe ;
    - WeatherBench 2, qui partage des auteurs avec GraphCast, GenCast et l'ECMWF.

  Ce que ces cas ont en commun, et que le code peut mesurer : des AUTEURS communs. Deux travaux
  qui partagent un auteur ne se corroborent pas. Le contrôle résout donc les identifiants des
  sources (Semantic Scholar, un seul appel groupé) et compare leurs listes d'auteurs.

  Il tient les mêmes deux bords que le contrôle de rang :
    - on SIGNALE toute paire de sources co-signées d'un claim retenu (le modèle adjuge) ;
    - on ne BLOQUE que le cas dur : un claim CONFIRMÉ dont les sources, regroupées par auteurs
      communs, ne forment plus deux travaux indépendants, hors document-source déclaré.
  Une source sans identifiant (blog, page institutionnelle) compte comme un travail à part :
  le code ne sait pas, il ne bloque pas sur ce qu'il ne sait pas.

  Le réseau peut manquer (quota, 429) : le contrôle le DIT dans sa sortie et ne bloque pas —
  un contrôle muet sur son propre échec passerait pour un thème propre.

  Deux auteurs sont la même personne s'ils partagent leur authorId Semantic Scholar OU leur
  nom complet (sans accents, casse ni trait d'union) — jamais sur « nom + initiale » : à la mise
  au point, cette clé a BLOQUÉ deux claims justes du corpus sur un « Zhu R. » commun à deux
  personnes distinctes. Et jamais sur l'authorId seul : Semantic Scholar scinde des profils
  (« Jia-Heng Liu » sous deux identifiants), ce qui aurait masqué de vrais co-auteurs.

  Les tests n'appellent jamais le réseau : LINT_AUTHORS_FIXTURE pointe un JSON
  {identifiant Semantic Scholar: [{name, authorId}]}, ou {"__error__": "..."} pour simuler une
  panne.
"""
import importlib.util
import json
import os
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
LINT = HERE.parent.parent / "leanmonograph" / "scripts" / "lint.py"


def _load_lint():
    spec = importlib.util.spec_from_file_location("lean_lint", LINT)
    assert spec is not None and spec.loader is not None, f"lint.py introuvable : {LINT}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lint = _load_lint()


# ── Identifiants : ce que le code sait résoudre, et ce qu'il laisse inconnu ──────────────
@pytest.mark.parametrize("url,expected", [
    ("https://arxiv.org/abs/2312.15796", "ArXiv:2312.15796"),
    ("https://arxiv.org/html/2312.15796v1", "ArXiv:2312.15796"),     # la version ne change pas le travail
    ("https://arxiv.org/pdf/2212.12794v2", "ArXiv:2212.12794"),
    ("https://ar5iv.labs.arxiv.org/html/2308.15560", "ArXiv:2308.15560"),
    ("https://pmc.ncbi.nlm.nih.gov/articles/PMC11666454/", "PMCID:11666454"),
    ("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11666454/", "PMCID:11666454"),
    ("https://pubmed.ncbi.nlm.nih.gov/39633054/", "PMID:39633054"),
    ("https://doi.org/10.1038/s41586-024-08252-9", "DOI:10.1038/s41586-024-08252-9"),
    ("https://journals.sagepub.com/doi/pdf/10.1177/0269881120953994", "DOI:10.1177/0269881120953994"),
])
def test_identifiants_resolus(url, expected):
    assert lint.source_s2_id(url) == expected


@pytest.mark.parametrize("url", [
    "https://deepmind.google/discover/blog/gencast-predicts-weather/",
    "https://www.ecmwf.int/node/29308",
    "https://gmd.copernicus.org/articles/18/5781/2025/",
    "",
])
def test_sources_sans_identifiant_restent_inconnues(url):
    assert lint.source_s2_id(url) is None


def same(a, b):
    return bool(lint.author_identities(a) & lint.author_identities(b))


def test_meme_identifiant_meme_personne_malgre_la_graphie():
    assert same({"name": "Zied Ben Bouallègue", "authorId": "2068"},
                {"name": "Z. Ben Bouallegue", "authorId": "2068"})


def test_profil_scinde_reconnu_par_le_nom_complet():
    """Semantic Scholar scinde des profils : Ouro et SMELT ont « Jia-Heng Liu » sous deux
    authorId différents, et « Wenhao Huang » / « Wen-Hao Huang ». L'authorId seul raterait ces
    co-auteurs réels (82e run : SMELT et Ouro ne sont pas indépendants)."""
    assert same({"name": "Jia-Heng Liu", "authorId": "2182423032"},
                {"name": "Jia-Heng Liu", "authorId": "2294523552"})
    assert same({"name": "Wenhao Huang", "authorId": "2322836499"},
                {"name": "Wen-Hao Huang", "authorId": "2284758950"})
    assert same({"name": "Zied Ben Bouallègue"}, {"name": "zied ben  BOUALLEGUE"})


def test_homonymes_nom_initiale_ne_sont_pas_confondus():
    """Faux positif trouvé à la mise au point, sur le corpus réel (looped-transformers) : Ouro
    (Rui-Jie Zhu) et Virtual Logic Depth (Ruike Zhu) partagent « Zhu R. » mais pas l'auteur.
    Une clé nom + initiale BLOQUAIT deux claims justes."""
    assert not same({"name": "Rui-Jie Zhu", "authorId": "2303806694"},
                    {"name": "Ruike Zhu", "authorId": "2371012303"})
    # l'initiale seule ne suffit jamais à identifier une personne
    assert not same({"name": "R. Zhu", "authorId": "1"}, {"name": "Rui-Jie Zhu", "authorId": "2"})
    assert not same({"name": "R. Zhu"}, {"name": "R. Zhu"})
    # une abréviation de deux lettres reste une abréviation (« Th. » = Thomas ? Theodor ?)
    assert not same({"name": "Th. Ewalds"}, {"name": "Th. Ewalds"})


# ── Le check complet, sur un thème minimal écrit sur disque ───────────────────────────────
PREPRINT = {"id": "src:1", "title": "GenCast preprint", "url": "https://arxiv.org/html/2312.15796v1"}
NATURE = {"id": "src:2", "title": "GenCast, Nature version", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11666454/"}
OLIVETTI = {"id": "src:3", "title": "Do data-driven models beat…", "url": "https://doi.org/10.5194/gmd-17-7915-2024"}
BLOG = {"id": "src:4", "title": "DeepMind blog", "url": "https://deepmind.google/discover/blog/gencast/"}

def _a(name, aid):
    return {"name": name, "authorId": aid}


AUTEURS = {
    "ArXiv:2312.15796": [_a("Ilan Price", "1"), _a("Alvaro Sanchez-Gonzalez", "2"),
                         _a("Remi Lam", "3"), _a("Matthew Willson", "4")],
    "PMCID:11666454": [_a("Ilan Price", "1"), _a("A. Sanchez-Gonzalez", "2"),
                       _a("Ferran Alet", "5"), _a("Matthew Willson", "4")],
    "DOI:10.5194/gmd-17-7915-2024": [_a("Leonardo Olivetti", "6"), _a("Gabriele Messori", "7")],
}


def _theme(tmp_path, claims, sources):
    (tmp_path / "knowledge.json").write_text(
        json.dumps({"theme": "t", "sources": sources, "claims": claims}, ensure_ascii=False),
        encoding="utf-8")
    (tmp_path / "manifest.json").write_text(
        json.dumps({"meta": {}, "elements": []}, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def _run(theme, fixture):
    fx = theme / "auteurs.json"
    fx.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
    env = dict(os.environ, LINT_AUTHORS_FIXTURE=str(fx))
    p = subprocess.run([sys.executable, str(LINT), str(theme)],
                       capture_output=True, text=True, env=env)
    return p.returncode, json.loads(p.stdout)


def _claim(sources, audit="confirmed", note="Confirmé : 2/2 jurés, 2 sources indépendantes."):
    return {"id": "claim:1", "audit": audit, "statement": "x", "sources": sources, "audit_note": note}


def test_preprint_et_version_publiee_bloquent(tmp_path):
    """Le cas exact du 84e run : arXiv v1 + Nature sur PMC, comptés pour deux sources."""
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:2"])], [PREPRINT, NATURE]), AUTEURS)
    assert out["authors_check"] == "ok"
    assert len(out["shared_author_sources"]) == 1
    entry = out["shared_author_sources"][0]
    assert entry["blocking"] is True
    assert entry["independent_works"] == 1
    assert out["shared_author_blocking"] == 1
    assert code == 2


def test_sources_aux_auteurs_disjoints_ne_sont_pas_signalees(tmp_path):
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:3"])], [PREPRINT, OLIVETTI]), AUTEURS)
    assert out["shared_author_sources"] == []
    assert code == 0


def test_source_sans_identifiant_compte_pour_un_travail_a_part(tmp_path):
    """Le code ne sait pas qui signe un billet de blog : il ne bloque pas sur ce qu'il ignore.
    (Article + blog des mêmes auteurs reste un angle mort, à la charge des jurés.)"""
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:4"])], [PREPRINT, BLOG]), AUTEURS)
    assert out["shared_author_sources"] == []
    assert code == 0


def test_paire_cosignee_avec_une_troisieme_source_independante_est_signalee_sans_bloquer(tmp_path):
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:2", "src:3"])],
                            [PREPRINT, NATURE, OLIVETTI]), AUTEURS)
    entry = out["shared_author_sources"][0]
    assert entry["independent_works"] == 2
    assert entry["blocking"] is False
    assert {tuple(sorted(p["sources"])) for p in entry["pairs"]} == {("src:1", "src:2")}
    assert code == 0


def test_claim_corrige_est_signale_sans_bloquer(tmp_path):
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:2"], audit="corrected")],
                            [PREPRINT, NATURE]), AUTEURS)
    assert out["shared_author_sources"][0]["blocking"] is False
    assert code == 0


def test_document_source_declare_ne_bloque_pas(tmp_path):
    note = "Confirmé sur lecture directe (règle document-source) : SA SOURCE EST UNIQUE PAR NATURE"
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:2"], note=note)],
                            [PREPRINT, NATURE]), AUTEURS)
    assert out["shared_author_sources"][0]["blocking"] is False
    assert code == 0


def test_claim_rejete_nest_pas_examine(tmp_path):
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:2"], audit="rejected")],
                            [PREPRINT, NATURE]), AUTEURS)
    assert out["shared_author_sources"] == []
    assert code == 0


def test_panne_du_resolveur_est_dite_et_ne_bloque_pas(tmp_path):
    """Un 429 de Semantic Scholar ne doit ni faire planter le lint, ni passer pour un thème propre."""
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:2"])], [PREPRINT, NATURE]),
                     {"__error__": "HTTP 429"})
    assert out.get("error") is None, out
    assert out["authors_check"].startswith("indisponible")
    assert "429" in out["authors_check"]
    assert out["shared_author_sources"] == []
    assert code == 0


def test_homonymes_dans_le_check_complet_ne_bloquent_pas(tmp_path):
    """Le cas réel de looped-transformers, de bout en bout : un seul « Zhu R. » commun, deux
    personnes distinctes — rien à signaler."""
    ouro = {"id": "src:1", "title": "Ouro", "url": "https://arxiv.org/abs/2510.25741"}
    vld = {"id": "src:2", "title": "VLD", "url": "https://arxiv.org/abs/2506.18233"}
    fx = {"ArXiv:2510.25741": [_a("Rui-Jie Zhu", "2303806694"), _a("Wei Huang", "11")],
          "ArXiv:2506.18233": [_a("Ruike Zhu", "2371012303"), _a("Hanwen Zhang", "12")]}
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:2"])], [ouro, vld]), fx)
    assert out["shared_author_sources"] == []
    assert code == 0


def test_profil_scinde_dans_le_check_complet_bloque(tmp_path):
    """Ouro et SMELT, de bout en bout : aucun authorId commun, mais le même « Jia-Heng Liu »."""
    ouro = {"id": "src:1", "title": "Ouro", "url": "https://arxiv.org/abs/2510.25741"}
    smelt = {"id": "src:2", "title": "SMELT", "url": "https://arxiv.org/abs/2609.01343"}
    fx = {"ArXiv:2510.25741": [_a("Jia-Heng Liu", "2182423032"), _a("Rui-Jie Zhu", "2303806694")],
          "ArXiv:2609.01343": [_a("Jia-Heng Liu", "2294523552"), _a("Shaowen Wang", "2310497362")]}
    code, out = _run(_theme(tmp_path, [_claim(["src:1", "src:2"])], [ouro, smelt]), fx)
    assert out["shared_author_sources"][0]["pairs"][0]["shared_authors"] == ["Jia-Heng Liu"]
    assert out["shared_author_blocking"] == 1
    assert code == 2


def test_source_donnee_en_objet_est_examinee(tmp_path):
    """Un claim réparé à la main porte ses sources en objets {title, url} (27e run)."""
    claim = _claim([{"title": "p", "url": PREPRINT["url"]}, {"title": "n", "url": NATURE["url"]}])
    code, out = _run(_theme(tmp_path, [claim], []), AUTEURS)
    assert out["shared_author_sources"][0]["blocking"] is True
    assert code == 2
