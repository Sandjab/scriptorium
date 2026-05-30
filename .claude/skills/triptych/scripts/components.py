# components.py — rendus déterministes (aucun I/O, aucun jugement)
import html

def esc(t): return html.escape(t or "", quote=False)

def render_section(el):
    lvl = el.get("level", 3)
    return (f'<section id="{el["id"]}">\n<h{lvl}>{esc(el["heading"])}</h{lvl}>\n'
            f'{el.get("prose","")}\n</section>')

def render_abstract(tldr):
    bullets = "".join(f"<li>{esc(x)}</li>" for x in tldr.get("part1",[]) + tldr.get("part2",[]))
    return ('<div class="xwrap"><div class="xabstract"><div class="xk">Résumé</div>'
            f'<p class="xthese">{esc(tldr["these"])}</p><ul>{bullets}</ul></div></div>')

def render_tldr(tldr, key, title):
    lis = "".join(f"<li>{esc(x)}</li>" for x in tldr[key])
    return f'<div class="xtldr"><div class="xk">En bref — {esc(title)}</div><ul>{lis}</ul></div>'

def render_glossary(gloss):
    cards = []
    for t in gloss:
        see = f'<p class="gt-see">→ {esc(t["see_also"])}</p>' if t.get("see_also") else ""
        cards.append(f'<div class="gterm"><span class="gt-name">{esc(t["term"])}</span>'
                     f'<p class="gt-def">{esc(t["definition"])}</p>{see}</div>')
    return ('<section id="glossaire"><h3>Glossaire</h3>'
            '<div class="gloss-grid">' + "\n".join(cards) + "</div></section>")

def render_exercise(el):
    return (f'<details class="ex"><summary>Vérifie ta compréhension'
            f'<span class="cnt">Partie {esc(el["part"])}</span></summary><div class="exbody">'
            f'<p><b>Question.</b> {el.get("question","")}</p>'
            f'<div class="eg b"><span class="egk">Réponse</span>{el.get("answer","")}</div>'
            f'</div></details>')

def render_onramp(el):
    steps = "".join(el.get("steps", []))
    return ('<div class="xwrap"><div class="xabstract" style="border-left-color:var(--blue-deep);">'
            '<div class="xk">Commence ici · parcours de lecture</div>'
            f'<ul class="xpath">{steps}</ul></div></div>')

def render_widget(el, widgets):
    return widgets[el["ref"]]

def render_callout(el):
    kind = el.get("kind", "callout")
    return f'<div class="{kind}"><div class="ct">{esc(el["title"])}</div>{el.get("body","")}</div>'

def render_biblio(el):
    items = "".join(f'<div><a href="{e["href"]}">{esc(e["label"])}</a></div>'
                    for e in el.get("entries", []))
    return f'<section id="biblio"><h3>Bibliographie &amp; repos</h3>{items}</section>'

def render_toc(manifest):
    return "\n".join(f'<a href="#{el["id"]}">{esc(el["heading"])}</a>'
                     for el in manifest["elements"] if el.get("type") == "section")

RENDERERS = {
    "section":  lambda el, ctx: render_section(el),
    "abstract": lambda el, ctx: render_abstract(ctx["tldr"]),
    "tldr":     lambda el, ctx: render_tldr(ctx["tldr"], el["key"], el["title"]),
    "glossary": lambda el, ctx: render_glossary(ctx["glossary"]),
    "exercise": lambda el, ctx: render_exercise(el),
    "onramp":   lambda el, ctx: render_onramp(el),
    "widget":   lambda el, ctx: render_widget(el, ctx["widgets"]),
    "callout":  lambda el, ctx: render_callout(el),
    "biblio":   lambda el, ctx: render_biblio(el),
}
