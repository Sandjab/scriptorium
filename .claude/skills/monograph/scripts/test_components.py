# test_components.py
import components as C

def test_section_renders_id_heading_prose():
    el = {"type":"section","id":"intro","heading":"Intro","level":3,"prose":"<p>hi</p>"}
    out = C.render_section(el)
    assert '<section id="intro">' in out
    assert "<h3>Intro</h3>" in out
    assert "<p>hi</p>" in out

def test_glossary_escapes_and_lists_terms():
    gloss = [{"term":"A & B","definition":"d<x>","see_also":"C"}]
    out = C.render_glossary(gloss)
    assert "A &amp; B" in out
    assert "d&lt;x&gt;" in out
    assert "→ C" in out

def test_toc_builds_anchor_links_from_sections_only():
    manifest = {"elements":[
        {"type":"section","id":"a","heading":"Alpha"},
        {"type":"widget","ref":"w"},
        {"type":"section","id":"b","heading":"Beta"}]}
    out = C.render_toc(manifest)
    assert '<a href="#a">Alpha</a>' in out
    assert '<a href="#b">Beta</a>' in out
    assert out.count("<a ") == 2          # seules les 2 sections → 2 liens (le widget exclu)
    assert "#w" not in out                # le ref du widget ne fuit pas dans la TOC

def test_pointers_renders_cards_with_badge_link_and_escaped_blurb():
    el = {"type":"pointers","title":"Pour aller plus loin","items":[
        {"name":"neo4j <graphrag>","url":"https://example.org/x","kind":"package","blurb":"d<x> & y"}]}
    out = C.render_pointers(el)
    assert '<section id="pointers">' in out          # section équilibrée (structural_checks)
    assert "<h3>Pour aller plus loin</h3>" in out
    assert 'href="https://example.org/x"' in out      # lien rendu
    assert "neo4j &lt;graphrag&gt;" in out             # nom échappé via esc()
    assert "package" in out                            # badge kind
    assert "d&lt;x&gt; &amp; y" in out                 # blurb échappé via esc()

def test_pointers_empty_items_still_balanced_section():
    out = C.render_pointers({"type":"pointers","items":[]})
    assert out.count("<section") == out.count("</section>")   # 1/1, jamais déséquilibré
    assert "Pour aller plus loin" in out               # titre par défaut
