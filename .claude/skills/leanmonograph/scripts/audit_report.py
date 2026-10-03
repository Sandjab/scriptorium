#!/usr/bin/env python3
"""audit_report.py — rapport d'audit d'un thème leanmonograph, calculé par CODE.

Usage : python3 audit_report.py <themeDir>

Écrit <themeDir>/audit-report.json et <themeDir>/audit-report.md. Remplace l'écriture
« verbatim » par un agent, qui échouait en silence au-delà du plafond de sortie (5 occurrences,
dont le 75e run : `{written: false}` sans erreur).

Entrées :
  .leanmonograph/research.json  → ordre des sections (arch.outline) et titre
  .leanmonograph/sec-<id>.json  → claims audités et verdicts des jurés (tally)
  manifest.json                 → sections VIVANTES (après élagage)
  knowledge.json                → état FINAL des claims retenus et rejetés des sections vivantes

Les ids `claim:N` sont attribués comme dans workflow.js : sur les seules sections vivantes,
dans l'ordre du plan puis des claims. Le statut, l'énoncé, la note et le nombre de sources
viennent de knowledge.json — le rapport décrit donc l'état final, ré-audit et backstop compris.
Un désaccord de décompte entre checkpoints et knowledge.json fait sortir en 1, sans rien écrire.
"""
import json
import pathlib
import sys
from typing import NoReturn


def die(msg) -> NoReturn:
    print(f"[audit_report] ÉCHEC : {msg}", file=sys.stderr)
    sys.exit(1)


def load(p):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        die(f"{p} illisible ({e})")


def esc(v):
    return " ".join(str("" if v is None else v).replace("|", "\\|").split())


def num(v):
    return "?" if v is None else v


def build(theme):
    ck = theme / ".leanmonograph"
    research = load(ck / "research.json")
    arch = research.get("arch") or {}
    knowledge = load(theme / "knowledge.json")
    manifest = load(theme / "manifest.json")
    live = {e.get("id") for e in manifest.get("elements", []) if e.get("type") == "section"}

    sections = []
    for o in arch.get("outline", []):
        p = ck / f"sec-{o['id']}.json"
        if p.exists():
            sections.append(load(p))
    if not sections:
        die(f"aucun checkpoint sec-*.json dans {ck}")

    kclaims = knowledge.get("claims", [])
    n_live = sum(len(s.get("claims", [])) for s in sections if s["section"]["id"] in live)
    if n_live != len(kclaims):
        die(f"{n_live} claims dans les sections vivantes des checkpoints, {len(kclaims)} dans "
            f"knowledge.json — les ids seraient décalés, rapport non écrit")

    claims, k = [], 0
    for s in sections:
        sid = s["section"]["id"]
        retained_sec = sid in live
        for ac in s.get("claims", []):
            t = ac.get("tally")
            row = {"id": None, "section": sid, "section_retained": retained_sec,
                   "audit": ac.get("audit"), "kind": t.get("kind") if t else "unknown",
                   "statement": ac.get("statement"),
                   "original_statement": ac.get("original_statement") or ac.get("statement"),
                   "corroborated": t.get("corroborated") if t else None,
                   "refuted": t.get("refuted") if t else None,
                   "corrected": t.get("corrected") if t else None,
                   "n_sources": len(ac.get("sources") or []),
                   "jurors": t.get("jurors", []) if t else [],
                   "audit_note": ac.get("note") or ""}
            if retained_sec:
                f = kclaims[k]
                k += 1
                row.update(id=f.get("id"), audit=f.get("audit"), statement=f.get("statement"),
                           n_sources=len(f.get("sources") or []),
                           audit_note=f.get("audit_note") or "")
            row["retained"] = retained_sec and row["audit"] != "rejected"
            claims.append(row)
    # Ordre des clés identique à workflow.js.
    keys = ["id", "section", "section_retained", "retained", "audit", "kind", "statement",
            "original_statement", "corroborated", "refuted", "corrected", "n_sources",
            "jurors", "audit_note"]
    claims = [{x: c[x] for x in keys} for c in claims]
    count = lambda a: sum(c["audit"] == a for c in claims)
    return {
        "generator": "leanmonograph",
        "theme": knowledge.get("theme") or {"slug": manifest.get("slug"), "title": arch.get("title")},
        "summary": {"sections_total": len(sections),
                    "sections_retained": sum(s["section"]["id"] in live for s in sections),
                    "claims_total": len(claims), "confirmed": count("confirmed"),
                    "corrected": count("corrected"), "rejected": count("rejected"),
                    "retained": sum(c["retained"] for c in claims)},
        "claims": claims,
    }


def render_md(rep):
    s = rep["summary"]
    lines = [
        f"# Rapport d'audit — {esc(rep['theme'].get('title'))} ({rep['generator']})", "",
        f"Thème : `{esc(rep['theme'].get('slug'))}`", "",
        "## Synthèse",
        f"- Sections : {s['sections_retained']}/{s['sections_total']} retenues",
        f"- Claims : {s['claims_total']} audités → **{s['confirmed']} confirmed**, "
        f"{s['corrected']} corrected, {s['rejected']} rejected ; {s['retained']} retenus dans le document",
        "", "Légende jurés : `lentille✓` corrobore · `lentille✗` réfute · `~` propose une correction.", "",
        "## Par claim", "",
        "| id | section | kind | audit | corrob. | réfut. | corrig. | sources | jurés | énoncé |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for c in rep["claims"]:
        jur = " ".join(f"{j.get('lens')}{'✓' if j.get('holds') else '✗'}{'~' if j.get('corrected') else ''}"
                       for j in c["jurors"])
        lines.append(
            f"| {c['id'] or '—'} | {esc(c['section'])} | {c['kind']} | {c['audit']}"
            f"{'' if c['retained'] else ' (non retenu)'} | {num(c['corroborated'])} | {num(c['refuted'])} | "
            f"{num(c['corrected'])} | {c['n_sources']} | {esc(jur)} | {esc(c['statement'])} |")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        die("usage : audit_report.py <themeDir>")
    theme = pathlib.Path(sys.argv[1])
    rep = build(theme)
    (theme / "audit-report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    (theme / "audit-report.md").write_text(render_md(rep), encoding="utf-8")
    s = rep["summary"]
    print(f"[audit_report] écrit audit-report.json/.md — {s['claims_total']} claims "
          f"({s['confirmed']} confirmed, {s['corrected']} corrected, {s['rejected']} rejected), "
          f"{s['sections_retained']}/{s['sections_total']} sections")


if __name__ == "__main__":
    main()
