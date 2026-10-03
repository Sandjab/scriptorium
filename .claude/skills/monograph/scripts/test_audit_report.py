"""Tests du générateur déterministe du rapport d'audit (leanmonograph/scripts/audit_report.py).

Lancer :  python3 -m pytest .claude/skills/monograph/scripts/test_audit_report.py

CE QUE CES TESTS PROTÈGENT, ET POURQUOI

  Un script Workflow n'a aucun accès au système de fichiers : `audit-report.json` était écrit
  par un AGENT priant de recopier ~100 ko verbatim. Sur les gros thèmes la copie échoue, et en
  silence — au 75e run (computer-use-gui-agents), `write:audit-report.json` a rendu
  `{written: false}` sans erreur, et le thème a failli être commité sans son rapport (5e
  occurrence de la classe, cf. mémoire frugalmonograph-audit-report-token-limit). Le rapport est
  une transformation déterministe des checkpoints : du code le calcule, l'agent l'exécute.

  Trois propriétés tiennent la valeur du rapport :
    1. les ids `claim:N` sont ceux de knowledge.json — numérotés sur les seules sections
       VIVANTES, dans l'ordre du plan ; un claim d'une section élaguée n'a pas d'id ;
    2. le rapport décrit l'état FINAL : une correction faite après le council (ré-audit,
       backstop) apparaît, alors que l'ancien rapport figeait le vote des jurés ;
    3. un désaccord entre checkpoints et knowledge.json fait ÉCHOUER le script (exit 1) au
       lieu d'écrire un rapport aux ids décalés.
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE.parent.parent / "leanmonograph" / "scripts" / "audit_report.py"


def _tally(holds):
    return {"kind": "established", "corroborated": sum(holds), "refuted": len(holds) - sum(holds),
            "corrected": 0,
            "jurors": [{"lens": "soutien", "holds": h, "corrected": False} for h in holds]}


def _ac(sec, stmt, audit):
    return {"sectionId": sec, "statement": stmt, "original_statement": stmt + " (orig)",
            "audit": audit, "note": "council", "sources": [{"url": "u"}],
            "tally": _tally([audit != "rejected", True])}


def _theme(tmp_path, knowledge_claims=None):
    ck = tmp_path / ".leanmonograph"
    ck.mkdir()
    outline = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    (ck / "research.json").write_text(json.dumps({"arch": {"title": "T", "outline": outline}}))
    secs = {
        "a": [_ac("a", "A1", "confirmed"), _ac("a", "A2", "rejected")],
        "b": [_ac("b", "B1", "rejected"), _ac("b", "B2", "rejected")],   # élaguée
        "c": [_ac("c", "C1", "corrected"), _ac("c", "C2", "confirmed")],
    }
    for sid, claims in secs.items():
        (ck / f"sec-{sid}.json").write_text(json.dumps(
            {"section": {"id": sid, "heading": sid, "kind": "normal"}, "claims": claims}))
    (tmp_path / "manifest.json").write_text(json.dumps({"slug": "t", "elements": [
        {"type": "section", "id": "a"}, {"type": "section", "id": "c"}]}))
    if knowledge_claims is None:
        knowledge_claims = [
            {"id": "claim:1", "statement": "A1", "audit": "confirmed", "sources": ["src:1", "src:2"], "audit_note": "n"},
            {"id": "claim:2", "statement": "A2", "audit": "rejected", "sources": ["src:1"], "audit_note": "n"},
            # Corrigé APRÈS le council (backstop) : le rapport doit le refléter.
            {"id": "claim:3", "statement": "C1 corrigé au backstop", "audit": "corrected",
             "sources": ["src:1", "src:2", "src:3"], "audit_note": "n | backstop"},
            {"id": "claim:4", "statement": "C2", "audit": "confirmed", "sources": ["src:1", "src:2"], "audit_note": "n"},
        ]
    (tmp_path / "knowledge.json").write_text(json.dumps(
        {"theme": {"slug": "t", "title": "T"}, "sources": [], "claims": knowledge_claims}))
    return tmp_path


def _run(theme):
    return subprocess.run([sys.executable, str(SCRIPT), str(theme)], capture_output=True, text=True)


def test_ids_sur_sections_vivantes_et_section_elaguee_sans_id(tmp_path):
    t = _theme(tmp_path)
    assert _run(t).returncode == 0
    rep = json.loads((t / "audit-report.json").read_text())
    by_stmt = {c["original_statement"]: c for c in rep["claims"]}
    assert by_stmt["A1 (orig)"]["id"] == "claim:1"
    assert by_stmt["C1 (orig)"]["id"] == "claim:3"          # b élaguée : la numérotation la saute
    assert by_stmt["B1 (orig)"]["id"] is None
    assert by_stmt["B1 (orig)"]["section_retained"] is False
    assert by_stmt["B1 (orig)"]["retained"] is False
    assert rep["summary"] == {"sections_total": 3, "sections_retained": 2, "claims_total": 6,
                              "confirmed": 2, "corrected": 1, "rejected": 3, "retained": 3}


def test_rapport_decrit_l_etat_final_pas_le_vote(tmp_path):
    t = _theme(tmp_path)
    _run(t)
    rep = json.loads((t / "audit-report.json").read_text())
    c3 = next(c for c in rep["claims"] if c["id"] == "claim:3")
    assert c3["statement"] == "C1 corrigé au backstop"
    assert c3["n_sources"] == 3
    assert c3["jurors"], "les verdicts des jurés restent ceux du council"
    md = (t / "audit-report.md").read_text()
    assert "C1 corrigé au backstop" in md
    assert "**2 confirmed**, 1 corrected, 3 rejected" in md


def test_desaccord_avec_knowledge_echoue_bruyamment(tmp_path):
    """Un claim de trop ou de moins décalerait tous les ids suivants : refuser d'écrire."""
    t = _theme(tmp_path, knowledge_claims=[
        {"id": "claim:1", "statement": "A1", "audit": "confirmed", "sources": [], "audit_note": ""}])
    p = _run(t)
    assert p.returncode == 1
    assert "knowledge.json" in p.stderr
    assert not (t / "audit-report.json").exists()
