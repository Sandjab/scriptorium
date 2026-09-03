"""Tests du contrôle de RANG DES SOURCES de lint.py (check 4, leanmonograph/scripts/lint.py).

Lancer :  python3 -m pytest .claude/skills/monograph/scripts/test_lint_source_rank.py

CE QUE CES TESTS PROTÈGENT, ET POURQUOI

  Le contrôle d'acceptation du build COMPTE les sources d'un claim confirmé sans jamais juger
  ce qu'elles valent : il valide « 2 sources » sans voir que l'une est un marchand. Deux runs
  l'ont payé —

    45e run : un claim RETENU portant un résultat central reposait sur trois sites de rang nul,
              dont un vendeur de retraites psychédéliques. Contenu exact, appareil faux.
    46e run : claim:4 (« nootrope », étymologie) confirmé « 2/2 jurés, 2 sources indépendantes »
              alors que ses DEUX sources étaient Wiktionary et nootroo.com, un vendeur de
              nootropiques — zéro source de rang réel. Et l'exception `document-source` invoquée
              sur un miroir PR Newswire au lieu du document officiel de l'agence.

  La règle encodée ici tient les DEUX bords, et c'est le point délicat :
    - on SIGNALE largement (un claim corrigé, un claim d'absence ou un claim méthodologique peut
      légitimement citer la presse qu'il décrit — le modèle adjuge) ;
    - on ne BLOQUE que la garantie dure du projet : un claim CONFIRMÉ sans deux sources de rang
      réel, hors exception document-source DÉCLARÉE dans son audit_note.
  Un communiqué publié par l'autorité qui l'émet (fda.gov, ftc.gov, ansm) EST le document
  officiel : le signaler serait un faux positif, et c'en fut un lors de la mise au point.
"""
import importlib.util
import json
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


# ── source_rank : ce que le code classe, et ce qu'il refuse de classer ────────────────────
@pytest.mark.parametrize("url", [
    "https://en.wikipedia.org/wiki/Piracetam",
    "https://en.wiktionary.org/wiki/nootropic",          # 46e run : échappait à la 1re version
    "https://nootroo.com/setting-record-straight-roots-term-nootropic/",  # vendeur, 46e run
    "https://www.healio.com/news/primary-care/20200923/some-dietary-supplements",
    "https://www.prnewswire.com/news-releases/statement-from-deputy-commissioners",
    "https://www.researchgate.net/publication/24032577_Comparative_studies",
    "https://gwern.net/doc/nootropic/1994-review-chemicalstructure-racetams.pdf",
    "https://www.reddit.com/r/nootropics/comments/xyz",
])
def test_sources_de_rang_nul_sont_signalees(url):
    assert lint.source_rank(url) is not None, url


@pytest.mark.parametrize("url", [
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC9415189/",
    "https://pubmed.ncbi.nlm.nih.gov/8061686/",
    "https://doi.org/10.1016/j.phrs.2008.02.004",
    "https://www.cochrane.org/evidence/CD001011",
    "https://www.ncbi.nlm.nih.gov/books/NBK559694/",
    "https://base-donnees-publique.medicaments.gouv.fr/medicament/64384738/extrait",
    "https://examine.com/supplements/piracetam/research/",   # rang MOYEN, pas nul (doctrine santé)
])
def test_sources_recevables_ne_sont_pas_signalees(url):
    assert lint.source_rank(url) is None, url


@pytest.mark.parametrize("url", [
    "https://www.ftc.gov/news-events/news/press-releases/2019/02/ftc-fda-send-warning-letters",
    "https://www.fda.gov/news-events/press-announcements/statement-on-vinpocetine",
])
def test_communique_publie_par_lautorite_est_le_document_officiel(url):
    """Faux positif rencontré à la mise au point : un communiqué d'agence sur le site de
    l'agence est la source, pas une reprise. Seul le même chemin AILLEURS est une reprise."""
    assert lint.source_rank(url) is None, url


def test_reprise_de_communique_hors_site_officiel_est_signalee():
    assert lint.source_rank("https://www.pharmatimes.com/press-release/fda-warns-on-vinpocetine")


# ── Le check complet, sur un thème minimal écrit sur disque ───────────────────────────────
def _theme(tmp_path, claims, sources):
    (tmp_path / "knowledge.json").write_text(
        json.dumps({"theme": "t", "sources": sources, "claims": claims}, ensure_ascii=False),
        encoding="utf-8")
    (tmp_path / "manifest.json").write_text(
        json.dumps({"meta": {}, "elements": []}, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def _run(theme):
    p = subprocess.run([sys.executable, str(LINT), str(theme)],
                       capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout)


VENDEUR = {"id": "src:1", "title": "boutique", "url": "https://nootroo.com/research/x"}
WIKI = {"id": "src:2", "title": "wiki", "url": "https://en.wikipedia.org/wiki/Nootropic"}
REVUE = {"id": "src:3", "title": "revue", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9415189/"}
REVUE2 = {"id": "src:4", "title": "revue 2", "url": "https://doi.org/10.1016/j.phrs.2008.02.004"}
MIROIR = {"id": "src:5", "title": "miroir", "url": "https://www.prnewswire.com/news-releases/z"}


def test_confirme_sur_vendeur_et_wiki_bloque(tmp_path):
    """Le cas exact de claim:4 au 46e run : deux « sources indépendantes », aucune recevable."""
    t = _theme(tmp_path, [{"id": "claim:1", "audit": "confirmed", "statement": "x",
                           "sources": ["src:1", "src:2"], "audit_note": "2/2 jurés"}],
               [VENDEUR, WIKI])
    code, out = _run(t)
    assert out["low_rank_blocking"] == 1
    assert code == 2


def test_confirme_avec_deux_sources_reelles_ne_bloque_pas(tmp_path):
    t = _theme(tmp_path, [{"id": "claim:1", "audit": "confirmed", "statement": "x",
                           "sources": ["src:3", "src:4", "src:2"], "audit_note": ""}],
               [REVUE, REVUE2, WIKI])
    code, out = _run(t)
    assert out["low_rank_blocking"] == 0
    assert code == 0


def test_document_source_declare_ne_bloque_pas(tmp_path):
    """L'exception nommée reste ouverte — mais elle doit être DÉCLARÉE dans l'audit_note."""
    t = _theme(tmp_path, [{"id": "claim:1", "audit": "confirmed", "statement": "x",
                           "sources": ["src:3"],
                           "audit_note": "source unique par nature (document-source)"}],
               [REVUE])
    code, out = _run(t)
    assert out["low_rank_blocking"] == 0
    assert code == 0


def test_document_source_non_declare_sur_un_miroir_bloque(tmp_path):
    """Le cas claim:56 du 46e run : l'exception invoquée sur une republication de presse."""
    t = _theme(tmp_path, [{"id": "claim:1", "audit": "confirmed", "statement": "x",
                           "sources": ["src:5"], "audit_note": "confirmé sur lecture directe"}],
               [MIROIR])
    code, out = _run(t)
    assert out["low_rank_blocking"] == 1
    assert code == 2


def test_claim_corrige_est_signale_mais_ne_bloque_pas(tmp_path):
    """Un claim méthodologique cite légitimement la presse qu'il décrit (claim:51, 46e run) :
    on le SIGNALE pour adjudication, on ne bloque pas — sinon le lint devient un couperet."""
    t = _theme(tmp_path, [{"id": "claim:1", "audit": "corrected", "statement": "x",
                           "sources": ["src:5", "src:2"], "audit_note": ""}],
               [MIROIR, WIKI])
    code, out = _run(t)
    assert len(out["low_rank_sources"]) == 1
    assert out["low_rank_blocking"] == 0
    assert code == 0


def test_claim_rejete_nest_pas_examine(tmp_path):
    """Un claim rejeté ne porte aucun fait du document : son appareil n'a pas à être jugé."""
    t = _theme(tmp_path, [{"id": "claim:1", "audit": "rejected", "statement": "x",
                           "sources": ["src:1"], "audit_note": ""}], [VENDEUR])
    code, out = _run(t)
    assert out["low_rank_sources"] == []
    assert code == 0


def test_une_source_donnee_en_objet_ne_fait_pas_planter_le_lint(tmp_path):
    """27e run : 11 claims ont été écrits À LA MAIN après le council, et portent leur source
    en OBJET ({title, url}) au lieu d'un id — 23 entrées dans le corpus. `by_id.get(dict)`
    levait « unhashable type: dict » : le lint sortait en 1, indiscernable d'une erreur
    d'usage, et le contrôle de rang restait AVEUGLE sur tout le thème. Un contrôle qui
    plante ne contrôle rien."""
    claim = {"id": "claim:1", "audit": "confirmed", "statement": "x",
             "sources": [{"title": "boutique", "url": "https://nootroo.com/research/x"},
                         {"title": "wiki", "url": "https://en.wikipedia.org/wiki/Nootropic"}]}
    code, out = _run(_theme(tmp_path, [claim], []))
    assert out.get("error") is None, out
    assert len(out["low_rank_sources"]) == 1, out["low_rank_sources"]
    entry = out["low_rank_sources"][0]
    assert entry["blocking"] is True
    assert {f["url"] for f in entry["flagged_sources"]} == {
        "https://nootroo.com/research/x", "https://en.wikipedia.org/wiki/Nootropic"}
    assert code == 2


def test_les_deux_formes_de_source_coexistent_dans_un_meme_claim(tmp_path):
    """Le mélange existe en vrai : un claim repris à la main garde ses ids d'origine
    et se voit ajouter une source en objet."""
    claim = {"id": "claim:1", "audit": "confirmed", "statement": "x",
             "sources": ["src:3", {"title": "vendeur", "url": "https://nootroo.com/y"}]}
    code, out = _run(_theme(tmp_path, [claim], [REVUE]))
    assert out.get("error") is None, out
    flagged = out["low_rank_sources"][0]["flagged_sources"]
    assert [f["url"] for f in flagged] == ["https://nootroo.com/y"]
    assert out["low_rank_sources"][0]["sources_of_real_rank"] == 1
