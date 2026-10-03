"""Tests du contrôle de LANGUE des claims RETENUS de lint.py (leanmonograph/scripts/lint.py).

Lancer :  python3 -m pytest .claude/skills/monograph/scripts/test_lint_foreign_kept.py

CE QUE CES TESTS PROTÈGENT, ET POURQUOI

  knowledge.json est la source de vérité d'un thème français. Quand un juré propose une
  correction, `decideAudit` reprend son `corrected_statement` tel quel — et les jurés écrivent
  souvent en anglais. Au 75e run (computer-use-gui-agents), trois claims `corrected` RETENUS
  (claim:16, 20, 51) sont arrivés jusqu'au commit avec un énoncé anglais ; au 44e run, quatre.
  Le lint ne regardait la langue que des claims REJETÉS (où elle aveugle `rejected_flags`) :
  pour les retenus, aucun contrôle ne voyait rien, et la reprise manuelle les a trouvés par
  hasard en régénérant le rapport d'audit.

  La règle encodée : un claim retenu (confirmed ou corrected) dont l'énoncé n'est pas en
  français BLOQUE (exit 2), sous une clé distincte de `foreign_statements`, parce que le geste
  de réparation diffère — traduire l'énoncé dans knowledge.json, pas adjuger la prose.
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LINT = HERE.parent.parent / "leanmonograph" / "scripts" / "lint.py"

SRC = [{"id": "src:1", "title": "a", "url": "https://arxiv.org/abs/2401.00001"},
       {"id": "src:2", "title": "b", "url": "https://arxiv.org/abs/2402.00002"}]
# Énoncé réel du 75e run (claim:20), recopié du juré.
EN = ("UGround (10M elements, slight LLaVA adaptation) and OS-Atlas (13M elements) rely on "
      "large-scale grounding data, and ScreenSpot-Pro reports that the best existing grounding "
      "model reaches only 18.9% on professional high-resolution interfaces.")
FR = ("UGround (10 M d'éléments) et OS-Atlas (13 M d'éléments) misent sur des données de "
      "grounding à grande échelle, et ScreenSpot-Pro rapporte que le meilleur modèle n'atteint "
      "que 18,9 % sur des interfaces professionnelles.")


def _run(tmp_path, claims):
    (tmp_path / "knowledge.json").write_text(
        json.dumps({"theme": "t", "sources": SRC, "claims": claims}, ensure_ascii=False),
        encoding="utf-8")
    (tmp_path / "manifest.json").write_text(
        json.dumps({"meta": {}, "elements": []}, ensure_ascii=False), encoding="utf-8")
    p = subprocess.run([sys.executable, str(LINT), str(tmp_path)],
                       capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout)


def _claim(audit, stmt, cid="claim:1"):
    return {"id": cid, "audit": audit, "statement": stmt,
            "sources": ["src:1", "src:2"], "audit_note": "2/2 jurés"}


def test_corrige_retenu_en_anglais_bloque(tmp_path):
    """Le cas exact du 75e run : la correction du juré, recopiée en anglais, est retenue."""
    code, out = _run(tmp_path, [_claim("corrected", EN)])
    assert [f["claim"] for f in out["foreign_kept_statements"]] == ["claim:1"]
    assert code == 2


def test_confirme_retenu_en_anglais_bloque_aussi(tmp_path):
    code, out = _run(tmp_path, [_claim("confirmed", EN)])
    assert len(out["foreign_kept_statements"]) == 1
    assert code == 2


def test_retenu_en_francais_passe(tmp_path):
    """Un énoncé français qui cite des noms propres anglais (UGround, ScreenSpot-Pro) n'est
    pas étranger : le contrôle compte les mots-outils, pas les noms."""
    code, out = _run(tmp_path, [_claim("corrected", FR)])
    assert out["foreign_kept_statements"] == []
    assert code == 0


def test_rejete_en_anglais_reste_dans_sa_cle_propre(tmp_path):
    """Les deux clés ne se mélangent pas : un rejet anglais appelle une adjudication de la
    prose (foreign_statements), pas une traduction de knowledge.json."""
    code, out = _run(tmp_path, [_claim("rejected", EN)])
    assert out["foreign_kept_statements"] == []
    assert len(out["foreign_statements"]) == 1
    assert code == 2
