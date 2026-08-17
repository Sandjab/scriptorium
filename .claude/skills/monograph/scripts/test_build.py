# test_build.py
import json, pathlib, pytest
import build

def _mk_theme(tmp, elements, claims=None, widgets=None):
    t = pathlib.Path(tmp)
    (t/"widgets").mkdir(parents=True); (t/"dist").mkdir()
    (t/"knowledge.json").write_text(json.dumps({"theme":{"slug":"demo","title":"D"},
        "sources":[], "claims":claims or []}), encoding="utf-8")
    (t/"glossary.json").write_text("[]", encoding="utf-8")
    (t/"tldr.json").write_text(json.dumps({"these":"t","part1":[],"part2":[]}), encoding="utf-8")
    for w in (widgets or {}):
        (t/"widgets"/(w+".html")).write_text(widgets[w], encoding="utf-8")
    (t/"manifest.json").write_text(json.dumps(
        {"slug":"demo",
         "meta":{"title":"D","kicker":"k","h1":"H","lede":"l","meta_chips":[],"footer":"f"},
         "elements":elements}), encoding="utf-8")
    return str(t)

def test_missing_claim_ref_fails_loud(tmp_path):
    theme = _mk_theme(tmp_path, [{"type":"section","id":"a","heading":"A","prose":"<p>x</p>",
                                  "claims":["claim:nope"]}])
    with pytest.raises(SystemExit):
        build.build_theme(theme)

def test_valid_theme_writes_html(tmp_path):
    theme = _mk_theme(tmp_path,
        [{"type":"section","id":"a","heading":"A","prose":"<p>x</p>","claims":["claim:k"]}],
        claims=[{"id":"claim:k","statement":"s","sources":["src:1","src:2"],"audit":"confirmed"}])
    build.build_theme(theme)
    out = (pathlib.Path(theme)/"dist"/"demo.html").read_text(encoding="utf-8")
    assert "file:///" not in out
    assert "--blue" in out
    assert '<section id="a">' in out
    assert "<!--%" not in out

def test_unknown_element_type_fails_loud(tmp_path):
    theme = _mk_theme(tmp_path, [{"type":"bogus","id":"a"}])
    with pytest.raises(SystemExit):
        build.build_theme(theme)

def test_missing_widget_ref_fails_loud(tmp_path):
    theme = _mk_theme(tmp_path, [{"type":"widget","ref":"ghost"}])
    with pytest.raises(SystemExit):
        build.build_theme(theme)

def test_structural_defect_blocks_all_writes(tmp_path):
    # prose injects an unbalanced <section> → structural check must trip BEFORE any file is written
    theme = _mk_theme(tmp_path,
        [{"type":"section","id":"a","heading":"A","prose":"<section>oops"}])
    dist = pathlib.Path(theme)/"dist"
    with pytest.raises(SystemExit):
        build.build_theme(theme)
    assert list(dist.glob("*.html")) == []   # aucune écriture partielle

def test_pointers_element_builds_and_is_structurally_sound(tmp_path):
    theme = _mk_theme(tmp_path, [
        {"type":"section","id":"a","heading":"A","prose":"<p>x</p>","claims":["claim:k"]},
        {"type":"pointers","title":"Pour aller plus loin","items":[
            {"name":"toolX","url":"https://example.org/x","kind":"package","blurb":"fait Y"}]},
    ], claims=[{"id":"claim:k","statement":"s","sources":["src:1","src:2"],"audit":"confirmed"}])
    build.build_theme(theme)
    out = (pathlib.Path(theme)/"dist"/"demo.html").read_text(encoding="utf-8")
    assert '<section id="pointers">' in out
    assert 'href="https://example.org/x"' in out
    assert "toolX" in out
    assert "<!--%" not in out            # aucun jeton résiduel
    assert "file:///" not in out

@pytest.mark.parametrize("removed_type", ["onramp", "tldr"])
def test_removed_renderer_is_unknown_type(tmp_path, removed_type):
    theme = _mk_theme(tmp_path/removed_type, [{"type": removed_type}])
    with pytest.raises(SystemExit):
        build.build_theme(theme)

def test_multiple_widgets_all_inlined_and_validated(tmp_path):
    theme = _mk_theme(tmp_path,
        [{"type":"section","id":"a","heading":"A","prose":"<p>x</p>"},
         {"type":"widget","ref":"w1"},
         {"type":"section","id":"b","heading":"B","prose":"<p>y</p>"},
         {"type":"widget","ref":"w2"}],
        widgets={"w1":'<div class="widget" id="w1">ONE</div>',
                 "w2":'<div class="widget" id="w2">TWO</div>'})
    build.build_theme(theme)
    out = (pathlib.Path(theme)/"dist"/"demo.html").read_text(encoding="utf-8")
    assert "ONE" in out and "TWO" in out
    assert "<!--%" not in out
    assert "file:///" not in out

def test_figures_are_numbered_in_document_order(tmp_path):
    fig = ('<figure class="fig"><svg viewBox="0 0 10 10"></svg>'
           '<figcaption><span class="fcap-k"></span>Légende.</figcaption></figure>')
    theme = _mk_theme(tmp_path, [
        {"type":"section","id":"a","heading":"A","prose": f"<p>x</p>{fig}"},
        {"type":"section","id":"b","heading":"B","prose": f"<p>y</p>{fig}"},
    ])
    build.build_theme(theme)
    out = (pathlib.Path(theme)/"dist"/"demo.html").read_text(encoding="utf-8")
    assert '<span class="fcap-k">Figure 1</span>' in out
    assert '<span class="fcap-k">Figure 2</span>' in out
    assert '<span class="fcap-k"></span>' not in out           # plus aucun gabarit vide
    assert out.index("Figure 1") < out.index("Figure 2")       # ordre du document


def test_figure_with_single_quoted_attrs_is_numbered(tmp_path):
    # Insertion JSON-safe : la figure utilise des apostrophes simples ; la regex les tolère, la sortie reste en ".
    fig = ("<figure class='fig'><svg></svg>"
           "<figcaption><span class='fcap-k'></span>L.</figcaption></figure>")
    theme = _mk_theme(tmp_path, [
        {"type":"section","id":"a","heading":"A","prose": f"<p>x</p>{fig}"},
    ])
    build.build_theme(theme)
    out = (pathlib.Path(theme)/"dist"/"demo.html").read_text(encoding="utf-8")
    assert '<span class="fcap-k">Figure 1</span>' in out         # apostrophes tolérées, sortie en "
    assert "<span class='fcap-k'></span>" not in out             # plus aucun gabarit vide

# --- verdicts ---------------------------------------------------------------

_VCLAIMS = [
    {"id": "claim:ok",  "statement": "s", "sources": ["src:1", "src:2"], "audit": "confirmed"},
    {"id": "claim:fix", "statement": "s", "sources": ["src:1", "src:2"], "audit": "corrected"},
    {"id": "claim:bad", "statement": "s", "sources": ["src:1"],          "audit": "rejected"},
]

def _valid_verdicts():
    return {"theme": "demo", "substances": [{
        "id": "s1", "label": "S1",
        "safety": {"status": "autorise", "label": "OK", "claims": ["claim:fix"]},
        "adverse": {"text": "t", "claims": ["claim:ok"]},
        "rows": [{"indication": "I", "efficacy": "bonne",
                  "claims": ["claim:ok"], "anchor": "sec-a"}]}]}

def _mk_vtheme(tmp, verdicts, with_element=True):
    els = [{"type": "abstract"}]
    if with_element:
        els.append({"type": "verdicts"})
    els.append({"type": "section", "id": "sec-a", "heading": "A", "prose": "<p>x</p>"})
    theme = _mk_theme(tmp, els, claims=_VCLAIMS)
    if verdicts is not None:
        (pathlib.Path(theme) / "verdicts.json").write_text(
            json.dumps(verdicts), encoding="utf-8")
    return theme

def test_verdicts_valid_builds_and_accepts_corrected(tmp_path):
    # safety cite un claim « corrected » : vérifié au même titre que confirmed (sémantique lint.py)
    theme = _mk_vtheme(tmp_path, _valid_verdicts())
    build.build_theme(theme)
    out = (pathlib.Path(theme) / "dist" / "demo.html").read_text(encoding="utf-8")
    assert '<section id="verdicts"' in out

def test_verdicts_row_without_claims_fails(tmp_path):
    v = _valid_verdicts(); v["substances"][0]["rows"][0]["claims"] = []
    with pytest.raises(SystemExit):
        build.build_theme(_mk_vtheme(tmp_path, v))

def test_verdicts_rejected_claim_fails(tmp_path):
    v = _valid_verdicts(); v["substances"][0]["rows"][0]["claims"] = ["claim:bad"]
    with pytest.raises(SystemExit):
        build.build_theme(_mk_vtheme(tmp_path, v))

def test_verdicts_unknown_claim_fails(tmp_path):
    v = _valid_verdicts(); v["substances"][0]["adverse"]["claims"] = ["claim:nope"]
    with pytest.raises(SystemExit):
        build.build_theme(_mk_vtheme(tmp_path, v))

def test_verdicts_efficacy_out_of_enum_fails(tmp_path):
    # ferme la porte aux gradations inventées (« miraculeuse » n'est pas un verdict)
    v = _valid_verdicts(); v["substances"][0]["rows"][0]["efficacy"] = "miraculeuse"
    with pytest.raises(SystemExit):
        build.build_theme(_mk_vtheme(tmp_path, v))

def test_verdicts_safety_status_out_of_enum_fails(tmp_path):
    v = _valid_verdicts(); v["substances"][0]["safety"]["status"] = "douteux"
    with pytest.raises(SystemExit):
        build.build_theme(_mk_vtheme(tmp_path, v))

def test_verdicts_element_without_file_fails(tmp_path):
    with pytest.raises(SystemExit):
        build.build_theme(_mk_vtheme(tmp_path, None))

def test_orphan_verdicts_file_fails(tmp_path):
    # verdicts.json présent sans élément au manifeste : aucun tableau perdu en silence
    with pytest.raises(SystemExit):
        build.build_theme(_mk_vtheme(tmp_path, _valid_verdicts(), with_element=False))

def test_verdicts_unknown_anchor_fails(tmp_path):
    v = _valid_verdicts(); v["substances"][0]["rows"][0]["anchor"] = "ghost"
    with pytest.raises(SystemExit):
        build.build_theme(_mk_vtheme(tmp_path, v))

# ── --expect-sections : le manifeste ÉCRIT est comparé aux sections attendues ──
# Classe d'échec du 39e run (nootropiques-stimulants-prescrits) : Compose omet une
# section, le workflow annonce « 11/11 retenues » (compte calculé sur l'élagage, un
# proxy), le document n'en a que 10 et build.py assemble sans broncher. Le contrôle
# doit vivre ici : seul build.py lit le fichier réellement écrit.

_CLAIM_OK = [{"id": "claim:k", "statement": "s", "sources": ["src:1", "src:2"],
              "audit": "confirmed"}]

def _sec(sid):
    return {"type": "section", "id": sid, "heading": sid.upper(),
            "prose": "<p>x</p>", "claims": ["claim:k"]}

def test_expect_sections_missing_one_fails_loud_before_write(tmp_path):
    theme = _mk_theme(tmp_path, [_sec("a")], claims=_CLAIM_OK)
    with pytest.raises(SystemExit) as e:
        build.build_theme(theme, expect_sections=["a", "b"])
    assert "b" in str(e.value)                                   # l'id manquant est nommé
    assert list((pathlib.Path(theme) / "dist").glob("*.html")) == []   # aucune écriture partielle

def test_expect_sections_unexpected_extra_fails_loud(tmp_path):
    # une section inattendue est le symétrique de l'omission : même arrêt bruyant
    theme = _mk_theme(tmp_path, [_sec("a"), _sec("b")], claims=_CLAIM_OK)
    with pytest.raises(SystemExit) as e:
        build.build_theme(theme, expect_sections=["a"])
    assert "b" in str(e.value)

def test_expect_sections_match_builds(tmp_path):
    theme = _mk_theme(tmp_path, [_sec("a"), _sec("b")], claims=_CLAIM_OK)
    build.build_theme(theme, expect_sections=["a", "b"])
    assert (pathlib.Path(theme) / "dist" / "demo.html").exists()

def test_expect_sections_ignores_non_section_elements(tmp_path):
    # seuls les éléments type=="section" comptent (widget/biblio/verdicts hors champ)
    theme = _mk_theme(tmp_path,
        [_sec("a"), {"type": "biblio", "entries": [{"label": "L", "href": "https://x.test"}]}],
        claims=_CLAIM_OK)
    build.build_theme(theme, expect_sections=["a"])
    assert (pathlib.Path(theme) / "dist" / "demo.html").exists()

def test_expect_sections_cli_flag(tmp_path):
    # le workflow invoque build.py par la LIGNE DE COMMANDE : le flag doit y exister,
    # sinon un agent Build le retirerait « pour faire passer » et le contrôle mourrait
    import subprocess, sys as _sys
    theme = _mk_theme(tmp_path, [_sec("a")], claims=_CLAIM_OK)
    r = subprocess.run([_sys.executable, build.__file__, theme, "--expect-sections", "a,b"],
                       capture_output=True, text=True)
    assert r.returncode != 0
    assert "b" in (r.stderr + r.stdout)
    r2 = subprocess.run([_sys.executable, build.__file__, theme, "--expect-sections", "a"],
                        capture_output=True, text=True)
    assert r2.returncode == 0, r2.stderr
