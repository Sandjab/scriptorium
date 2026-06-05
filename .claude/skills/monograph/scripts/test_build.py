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
