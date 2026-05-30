# test_build.py
import json, pathlib, pytest
import build

def _mk_theme(tmp, elements, claims=None, widgets=None):
    t = pathlib.Path(tmp)
    (t/"editions").mkdir(parents=True); (t/"widgets").mkdir(); (t/"dist").mkdir()
    (t/"knowledge.json").write_text(json.dumps({"theme":{"slug":"demo","title":"D"},
        "sources":[], "claims":claims or []}), encoding="utf-8")
    (t/"glossary.json").write_text("[]", encoding="utf-8")
    (t/"tldr.json").write_text(json.dumps({"these":"t","part1":[],"part2":[]}), encoding="utf-8")
    for w in (widgets or {}):
        (t/"widgets"/(w+".html")).write_text(widgets[w], encoding="utf-8")
    (t/"editions"/"reference.manifest.json").write_text(json.dumps(
        {"edition":"reference","slug":"demo",
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
    out = (pathlib.Path(theme)/"dist"/"demo-reference.html").read_text(encoding="utf-8")
    assert "file:///" not in out
    assert "--blue" in out
    assert '<section id="a">' in out
    assert "<!--%" not in out
