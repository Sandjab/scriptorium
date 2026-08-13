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


def render_widget(el, widgets):
    return widgets[el["ref"]]

def render_callout(el):
    kind = el.get("kind", "callout")
    return f'<div class="{kind}"><div class="ct">{esc(el["title"])}</div>{el.get("body","")}</div>'

def render_biblio(el):
    items = "".join(f'<div><a href="{e["href"]}">{esc(e["label"])}</a></div>'
                    for e in el.get("entries", []))
    return f'<section id="biblio"><h3>Bibliographie &amp; repos</h3>{items}</section>'

def render_pointers(el):
    cards = []
    for p in el.get("items", []):
        kind = esc(p.get("kind", ""))
        badge = f'<span class="xptr-kind">{kind}</span>' if kind else ""
        cards.append(f'<div class="xptr"><a class="xptr-name" href="{p["url"]}">{esc(p["name"])}</a>'
                     f'{badge}<p class="xptr-blurb">{esc(p.get("blurb",""))}</p></div>')
    title = esc(el.get("title", "Pour aller plus loin"))
    return (f'<section id="pointers"><h3>{title}</h3>'
            '<div class="xptr-grid">' + "\n".join(cards) + "</div></section>")

EFFICACY_LEVELS = ("nulle", "faible", "modeste", "bonne", "tres-bonne", "indeterminee")
SAFETY_STATUS = ("autorise", "interdit", "restreint", "pas-avis")
EFFICACY_LABELS = {"nulle": "Nulle", "faible": "Faible", "modeste": "Modeste",
                   "bonne": "Bonne", "tres-bonne": "Très bonne",
                   "indeterminee": "Indéterminée"}

def _efficacy_cell(lvl):
    label = EFFICACY_LABELS[lvl]
    if lvl == "indeterminee":
        return f'<span class="vmeter vm-na">{label}</span>'
    n = EFFICACY_LEVELS.index(lvl)                     # nulle=0 … tres-bonne=4
    bars = "".join(f'<i class="{"on" if i < n else ""}"></i>' for i in range(4))
    return f'<span class="vmeter">{bars}<b>{label}</b></span>'

def render_verdicts(v):
    parts = ['<section id="verdicts" class="verdicts"><h3>Verdicts par indication</h3>']
    for sub in v["substances"]:
        parts.append(f'<h4 class="vd-sub">{esc(sub["label"])}</h4>')
        rows = []
        for r in sub["rows"]:
            ind = esc(r["indication"])
            if r.get("anchor"):
                ind = f'<a href="#{r["anchor"]}">{ind}</a>'
            rows.append(
                f'<tr><td>{ind}</td><td>{_efficacy_cell(r["efficacy"])}</td>'
                f'<td>{esc(r.get("ci") or "—")}</td>'
                f'<td>{esc(r.get("official") or "—")}</td>'
                f'<td>{esc(r.get("note") or "")}</td></tr>')
        parts.append(
            '<div class="tbl-w"><table><thead><tr><th>Indication</th><th>Efficacité</th>'
            '<th>IC / taille d’effet</th><th>Statut officiel</th><th>Note</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")
        saf, adv = sub["safety"], sub["adverse"]
        parts.append(
            f'<p class="vd-safety"><b>Sécurité</b> : '
            f'<span class="vbadge vb-{saf["status"]}">{esc(saf["label"])}</span> · '
            f'<b>Effets indésirables</b> : {esc(adv["text"])}</p>')
    parts.append("</section>")
    return "\n".join(parts)

def render_toc(manifest):
    return "\n".join(f'<a href="#{el["id"]}">{esc(el["heading"])}</a>'
                     for el in manifest["elements"] if el.get("type") == "section")

RENDERERS = {
    "section":  lambda el, ctx: render_section(el),
    "abstract": lambda el, ctx: render_abstract(ctx["tldr"]),
    "glossary": lambda el, ctx: render_glossary(ctx["glossary"]),
    "exercise": lambda el, ctx: render_exercise(el),
    "widget":   lambda el, ctx: render_widget(el, ctx["widgets"]),
    "callout":  lambda el, ctx: render_callout(el),
    "biblio":   lambda el, ctx: render_biblio(el),
    "pointers": lambda el, ctx: render_pointers(el),
    "verdicts": lambda el, ctx: render_verdicts(ctx["verdicts"]),
}
