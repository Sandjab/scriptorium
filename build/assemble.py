#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble les 3 versions enrichies du document APO a partir de l'original
+ des blocs/widgets/glossaire/tldr produits par le workflow.

Strategie : transformations communes (chirurgicales, ancres assertees) puis
3 variantes (reference / publication / pedagogique). Echoue bruyamment si une
ancre ne matche pas exactement (count != attendu)."""

import json, os, re, html, sys

ROOT = "/Users/jean-paulgavini/Documents/Dev/napo"
B    = os.path.join(ROOT, "build")
ORIG = os.path.join(ROOT, "Auto-amélioration de skill — panorama & décisions.html")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

# ---------- pieces ----------
css2  = read(os.path.join(ROOT, "Auto-amélioration de skill — panorama & décisions_files", "css2"))
blocks = {n: read(os.path.join(B, "blocks", n + ".html"))
          for n in ["axe2-biais-juge","axe2-rubrique-auto","axe3-rl","axe3-trace",
                    "axe4-bandits","familles-rl-row","skillopt-note","part2-rigueur",
                    "part2-cout","biblio-additions"]}
widgets = {n: read(os.path.join(B, "widgets", n + ".html"))
           for n in ["pareto-explorer","reward-hack-demo","family-navigator",
                     "epsilon-calibrator","theme-tooltips"]}
gloss = json.load(open(os.path.join(B, "glossary.fr.json"), encoding="utf-8"))["terms"]
tldr  = json.load(open(os.path.join(B, "tldr.fr.json"), encoding="utf-8"))

base = read(ORIG)

# ---------- helpers : insertion assertee ----------
def repl_lit(s, old, new, n=1):
    c = s.count(old)
    if c != n:
        raise SystemExit("ANCRE LITTERALE absente/multiple (%d!=%d) : %r" % (c, n, old[:90]))
    return s.replace(old, new, 1 if n == 1 else n)

def sub_re(s, pattern, repl, n=1, flags=0):
    out, c = re.subn(pattern, repl, s, flags=flags)
    if c != n:
        raise SystemExit("ANCRE REGEX matchs=%d (attendu %d) : %r" % (c, n, pattern[:90]))
    return out

def esc(t):
    return html.escape(t, quote=False)

# ---------- CSS d'enrichissement (reutilise les tokens existants) ----------
EXTRA_CSS = """
  /* ===== enrichissements (blocs ajoutes) ===== */
  .xwrap{max-width:var(--maxw);margin:0 auto;padding:0 28px;}
  .xabstract{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--bordeaux);
    border-radius:8px;padding:24px 28px;margin:28px 0 0;box-shadow:0 1px 2px rgba(20,46,73,.05);}
  .xabstract .xk{font-family:"Archivo",system-ui,sans-serif;font-size:11px;letter-spacing:.16em;
    text-transform:uppercase;color:var(--bordeaux);font-weight:700;margin:0 0 9px;}
  .xabstract .xthese{font-size:19px;line-height:1.5;color:var(--ink);font-weight:600;margin:0 0 12px;
    font-family:"Spectral",Georgia,serif;}
  .xabstract ul{margin:8px 0 0;padding:0;list-style:none;}
  .xabstract li{position:relative;padding:5px 0 5px 22px;font-size:15px;color:var(--ink-soft);line-height:1.5;}
  .xabstract li::before{content:"\\25B8";position:absolute;left:2px;color:var(--blue-bright);font-weight:700;}
  .xabstract .xpath li::before{content:counter(xp);counter-increment:xp;background:var(--blue-deep);color:#fff;
    width:19px;height:19px;border-radius:50%;font-family:"JetBrains Mono",monospace;font-size:10px;left:0;top:5px;
    display:flex;align-items:center;justify-content:center;}
  .xabstract ul.xpath{counter-reset:xp;}
  .xabstract .xfoot{font-size:13px;color:var(--ink-faint);margin:14px 0 0;line-height:1.5;}
  .xtldr{background:var(--blue-wash);border:1px solid #CFE0EF;border-left:4px solid var(--blue);
    border-radius:6px;padding:14px 20px;margin:16px 0 4px;}
  .xtldr .xk{font-family:"Archivo",system-ui,sans-serif;font-size:11px;letter-spacing:.1em;
    text-transform:uppercase;color:var(--blue);font-weight:700;margin-bottom:7px;}
  .xtldr ul{margin:0;padding-left:19px;}
  .xtldr li{font-size:14px;color:var(--ink-soft);line-height:1.5;margin:4px 0;}
  .gloss-grid{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin:18px 0;}
  @media(max-width:760px){.gloss-grid{grid-template-columns:1fr;}}
  .gterm{background:var(--card);border:1px solid var(--line);border-radius:7px;padding:14px 17px;
    border-left:3px solid var(--blue);}
  .gterm .gt-name{font-family:"Archivo",system-ui,sans-serif;font-weight:700;color:var(--blue-deep);
    font-size:14.5px;display:block;margin-bottom:5px;}
  .gterm .gt-def{font-size:13.5px;color:var(--ink-soft);line-height:1.5;margin:0;}
  .gterm .gt-see{font-family:"JetBrains Mono",monospace;font-size:10.5px;color:var(--ink-faint);
    margin:8px 0 0;}
"""

# ---------- glossaire -> HTML ----------
def glossary_section():
    cards = []
    for t in gloss:
        see = ('<p class="gt-see">→ ' + esc(t["see_also"]) + "</p>") if t.get("see_also") else ""
        cards.append(
            '<div class="gterm"><span class="gt-name">' + esc(t["term"]) + "</span>"
            '<p class="gt-def">' + esc(t["definition"]) + "</p>" + see + "</div>")
    return ('<section id="glossaire">\n<h3>Glossaire</h3>\n'
            '<p class="lead">Les termes-clés du document, définis avec leurs exemples chiffrés. '
            'Les renvois <code>→</code> tissent les notions entre elles.</p>\n'
            '<div class="gloss-grid">\n' + "\n".join(cards) + "\n</div>\n</section>\n")

def tldr_block(key, titre):
    lis = "".join("<li>" + esc(x) + "</li>" for x in tldr[key])
    return ('<div class="xtldr"><div class="xk">En bref — ' + titre + "</div><ul>" + lis + "</ul></div>")

def abstract_block():
    bullets = "".join("<li>" + esc(x) + "</li>" for x in (tldr["part1"] + tldr["part2"]))
    return ('<div class="xwrap"><div class="xabstract">'
            '<div class="xk">Résumé</div>'
            '<p class="xthese">' + esc(tldr["these"]) + "</p>"
            "<ul>" + bullets + "</ul>"
            '<p class="xfoot">Document de travail en deux parties : un panorama des approches d’<em>automatic '
            'prompt optimization</em>, puis le contrat d’architecture retenu. Glossaire complet en annexe.</p>'
            "</div></div>")

def onramp_block():
    these = esc(tldr["these"])
    return ('<div class="xwrap"><div class="xabstract" style="border-left-color:var(--blue-deep);">'
            '<div class="xk">Commence ici · parcours de lecture</div>'
            '<p class="xthese">' + these + "</p>"
            '<ul class="xpath">'
            '<li><strong>La boucle</strong> (§ Le cadre) — run → critique → propose → accept/rollback : tout le reste en découle.</li>'
            '<li><strong>Les 4 axes</strong>, en t’arrêtant sur l’<em>évaluateur</em> (axe 2) — c’est lui qui débloque ou ferme tout l’aval.</li>'
            '<li><strong>Joue avec les widgets</strong> — l’explorateur de Pareto et la démo reward-hacking rendent les deux idées-clés tangibles.</li>'
            '<li><strong>La Partie II</strong> — comment ces choix se figent en un contrat d’architecture agnostique à l’heuristique.</li>'
            "</ul>"
            '<p class="xfoot">Survole les termes soulignés — comme '
            '<span class="theme-gloss" data-def="Dérive où l’optimisation apprend à exploiter les failles du juge plutôt qu’à améliorer la qualité réelle.">reward hacking</span> '
            'ou <span class="theme-gloss" data-def="Ensemble des candidats non dominés : meilleurs sur au moins une instance.">frontière de Pareto</span> '
            '— pour leur définition ; bascule en <strong>mode sombre</strong> via le bouton en haut à droite ; le '
            '<strong>glossaire</strong> complet est en annexe.</p>'
            "</div></div>")

EXO_P1 = ('<details class="ex"><summary>Vérifie ta compréhension<span class="cnt">Partie I</span></summary>'
          '<div class="exbody">'
          '<p><b>Question.</b> Ton évaluateur ne rend qu’un <em>scalaire absolu</em> 0–100. '
          'Quelles familles te sont fermées, et pourquoi ?</p>'
          '<div class="eg b"><span class="egk">Réponse</span>'
          '<p>Le <strong>réflexif-Pareto</strong> (pas de vecteur par-instance → aucune coordonnée de frontière) '
          'et tout opérateur de <strong>gradient dirigé</strong> (pas de feedback textuel → pas de direction de réécriture). '
          'Restent l’évolutionnaire, le tree-search, le bayésien et le RL — mais le scalaire est <span class="hl">dupable</span> '
          '(un préfixe « Analyse rigoureuse : » fait 72→81 à contenu identique), d’où la préférence pour un verdict pairwise.</p></div>'
          "</div></details>")

EXO_P2 = ('<details class="ex"><summary>Vérifie ta compréhension<span class="cnt">Partie II</span></summary>'
          '<div class="exbody">'
          '<p><b>Question.</b> Pourquoi <code>scores_par_instance</code> (vecteur) et <code>est_meilleur</code> (verdict pairwise) '
          'sont-ils <em>tous deux</em> primitifs, alors qu’une implémentation donnée peut calculer l’un à partir de l’autre ?</p>'
          '<div class="eg b"><span class="egk">Réponse</span>'
          '<p>Parce qu’on ne dérive pas un pairwise fiable de deux scores absolus indépendants (l’écart est sous le bruit de '
          'calibration), ni des coordonnées Pareto cardinales d’un simple « gagnant ». Le contrat les exige <strong>séparément</strong> '
          '; ils peuvent même légitimement <span class="hl">se contredire</span> — <code>est_meilleur</code> peut dire A&gt;B alors que '
          'la moyenne de B est supérieure, parce que A gagne là où B s’effondre.</p></div>'
          "</div></details>")

# =================== TRANSFORMATIONS COMMUNES ===================
def build_common():
    s = base

    # 1. CSS d'enrichissement avant </style> (unique dans le head a ce stade)
    s = repl_lit(s, "</style>", EXTRA_CSS + "\n</style>", 1)

    # 2. inline des polices : <link ... css2> -> <style>@font-face...</style>
    s = sub_re(s, r'<link href="\./Auto[^"]*?css2" rel="stylesheet">',
               lambda m: "<style>\n/* polices inlinées (ex-css2) — fichier autonome */\n"
                         + css2 + "\n</style>", 1)

    # 3. liens TOC/refs : file:///...#x -> #x (corrige une nav cassée dans l'original)
    s = s.replace("file:///Users/jean-paulgavini/Downloads/auto-amelioration-skill_1.html#", "#")

    # 3b. retrait du commentaire "saved from url" (fuite chemin local + nom d'utilisateur)
    s = sub_re(s, r"<!-- saved from url=.*?-->\n?", lambda m: "", 1)

    # 4. Option 2.g (rubrique auto) AVANT le callout reward-hacking
    s = sub_re(s, r'(<div class="callout">\s*<div class="ct">Le piège central : reward hacking</div>)',
               lambda m: blocks["axe2-rubrique-auto"] + "\n" + m.group(1), 1)

    # 5. tableau biais du juge + widget reward-hack-demo AVANT "Paramètres transverses"
    s = repl_lit(s, '<p><strong>Paramètres transverses</strong>',
                 blocks["axe2-biais-juge"] + "\n" + widgets["reward-hack-demo"]
                 + '\n<p><strong>Paramètres transverses</strong>', 1)

    # 6. Option 3.e (RL) + note Trace AVANT la note OPRO
    s = sub_re(s, r'(<div class="note">\s*<div class="ct">Variante : génération depuis trajectoire \(OPRO\)</div>)',
               lambda m: blocks["axe3-rl"] + "\n" + blocks["axe3-trace"] + "\n" + m.group(1), 1)

    # 7. note bandits + details AVANT "Règle d'acceptation"
    s = repl_lit(s, "<h4>Règle d'acceptation</h4>",
                 blocks["axe4-bandits"] + "\n<h4>Règle d'acceptation</h4>", 1)

    # 8. ligne RL dans le tableau des familles (avant </tbody> de CE tableau)
    s = sub_re(s, r'(</tbody>\s*</table></div>\s*<details class="ex"><summary>Exemples<span class="cnt">quelle famille)',
               lambda m: blocks["familles-rl-row"] + "\n" + m.group(1), 1)

    # 8b. note SkillOpt (instanciation nommée) en fin de #familles (avant son </section>)
    s = repl_lit(s, "</section>\n\n<!-- ============ PART II ============ -->",
                 blocks["skillopt-note"] + "\n</section>\n\n<!-- ============ PART II ============ -->", 1)

    # 9. widget Pareto en fin de section #d-pareto (avant #d-propre)
    s = repl_lit(s, '<section id="d-propre">',
                 widgets["pareto-explorer"] + '\n\n<section id="d-propre">', 1)

    # 10. nouvelle section #d-rigueur APRES #d-bruit (entre </section> et <section d-cible>)
    s = sub_re(s, r'</section>(\s*)<section id="d-cible">',
               lambda m: "</section>" + m.group(1) + blocks["part2-rigueur"]
                         + "\n\n<section id=\"d-cible\">", 1)

    # 11. bloc cout DANS #consequences (avant son </section>, juste avant <!-- BIBLIO -->)
    s = sub_re(s, r'</section>(\s*)<!-- BIBLIO -->',
               lambda m: blocks["part2-cout"] + "\n</section>" + m.group(1) + "<!-- BIBLIO -->", 1)

    # 12. ajouts bibliographie APRES le groupe "Fondateurs" (APE), avant </section> du biblio
    s = sub_re(s, r'(<a href="#?https?://arxiv\.org/abs/2211\.01910">Zhou et al\. 2022 — APE</a>\s*</div>)(\s*</section>)',
               lambda m: m.group(1) + "\n\n" + blocks["biblio-additions"] + m.group(2), 1)

    # 13. section Glossaire en annexe, juste avant </main>
    s = repl_lit(s, "</main>", glossary_section() + "\n</main>", 1)

    # 14. TOC : entrée Rigueur statistique après "Traitement du bruit"
    s = repl_lit(s, '<a href="#d-bruit" class="sub">Traitement du bruit</a>',
                 '<a href="#d-bruit" class="sub">Traitement du bruit</a>\n'
                 '  <a href="#d-rigueur" class="sub">Rigueur statistique</a>', 1)

    # 15. TOC : entrée Glossaire après Bibliographie
    s = repl_lit(s, '<a href="#biblio">Bibliographie &amp; repos</a>',
                 '<a href="#biblio">Bibliographie &amp; repos</a>\n'
                 '  <a href="#glossaire">Glossaire</a>', 1)

    return s

# =================== VARIANTES ===================
def strip_theme_demo(theme_html):
    # retire le bloc "Mode d'emploi" (details) pour ref/publication
    return re.sub(r"<details class=\"ex\"><summary>Mode d'emploi.*?</details>\s*",
                  "", theme_html, flags=re.S)

def set_kicker(s, label):
    return repl_lit(s, '<p class="kicker">Méthode · Auto-amélioration de skill</p>',
                    '<p class="kicker">Méthode · Auto-amélioration de skill · ' + label + "</p>", 1)

def add_family_nav(s):
    return repl_lit(s, "<!-- ============ PART II ============ -->",
                    widgets["family-navigator"] + "\n\n<!-- ============ PART II ============ -->", 1)

def add_epsilon(s):
    # le widget epsilon en fin de #d-bruit : avant la section #d-rigueur deja inseree
    return repl_lit(s, blocks["part2-rigueur"],
                    widgets["epsilon-calibrator"] + "\n\n" + blocks["part2-rigueur"], 1)

def add_theme(s, full):
    th = widgets["theme-tooltips"] if full else strip_theme_demo(widgets["theme-tooltips"])
    return repl_lit(s, "<footer>", th + "\n\n<footer>", 1)

def add_after_header(s, htmlblock):
    return repl_lit(s, '<div class="wrap">', htmlblock + '\n\n<div class="wrap">', 1)

def add_tldr_notes(s):
    s = repl_lit(s, '<div class="part-band" id="part1"><span class="pk">Partie I</span><h2>Panorama des approches</h2></div>',
                 '<div class="part-band" id="part1"><span class="pk">Partie I</span><h2>Panorama des approches</h2></div>\n'
                 + tldr_block("part1", "Partie I"), 1)
    s = repl_lit(s, '<div class="part-band" id="part2"><span class="pk">Partie II</span><h2>Les choix retenus &amp; leurs conséquences</h2></div>',
                 '<div class="part-band" id="part2"><span class="pk">Partie II</span><h2>Les choix retenus &amp; leurs conséquences</h2></div>\n'
                 + tldr_block("part2", "Partie II"), 1)
    return s

def add_exercises(s):
    # exo Partie I : juste avant PART II ; exo Partie II : avant <!-- BIBLIO -->
    s = repl_lit(s, "<!-- ============ PART II ============ -->",
                 EXO_P1 + "\n\n<!-- ============ PART II ============ -->", 1)
    s = repl_lit(s, "<!-- BIBLIO -->", EXO_P2 + "\n\n<!-- BIBLIO -->", 1)
    return s

def title_suffix(s, suff):
    return repl_lit(s, "<title>Auto-amélioration de skill — panorama &amp; décisions</title>",
                    "<title>Auto-amélioration de skill — " + suff + "</title>", 1)

# ---------- assemblage ----------
def write(name, s):
    p = os.path.join(ROOT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)
    return p, len(s)

results = []

# V1 — REFERENCE (superset dense : tous widgets, tldr compact, pas d'on-ramp)
v1 = build_common()
v1 = title_suffix(v1, "référence")
v1 = set_kicker(v1, "édition référence")
v1 = add_family_nav(v1)
v1 = add_epsilon(v1)
v1 = add_theme(v1, full=False)
v1 = add_tldr_notes(v1)
results.append(write("Auto-amélioration de skill — référence.html", v1))

# V2 — PUBLICATION (abstract, 2 widgets phares, pas family-nav/epsilon)
v2 = build_common()
v2 = title_suffix(v2, "panorama & décisions (édition publication)")
v2 = set_kicker(v2, "édition publication")
v2 = add_theme(v2, full=False)
v2 = add_after_header(v2, abstract_block())
results.append(write("Auto-amélioration de skill — publication.html", v2))

# V3 — PEDAGOGIQUE (on-ramp, tous widgets, tooltips, tldr, exercices)
v3 = build_common()
v3 = title_suffix(v3, "pédagogique")
v3 = set_kicker(v3, "édition pédagogique")
v3 = add_family_nav(v3)
v3 = add_epsilon(v3)
v3 = add_theme(v3, full=True)
v3 = add_after_header(v3, onramp_block())
v3 = add_tldr_notes(v3)
v3 = add_exercises(v3)
results.append(write("Auto-amélioration de skill — pédagogique.html", v3))

# ---------- rapport + verifs simples ----------
print("=== FICHIERS ÉCRITS ===")
for p, n in results:
    print("%7d o  %s" % (n, os.path.basename(p)))

print("\n=== VÉRIFS STRUCTURE (par fichier) ===")
for p, _ in results:
    s = read(p)
    checks = {
        "file:/// résiduels": s.count("file:///"),
        "<section ouverts": len(re.findall(r"<section\b", s)),
        "</section> fermés": s.count("</section>"),
        "<details ouverts": len(re.findall(r"<details\b", s)),
        "</details>": s.count("</details>"),
        "id d-rigueur": s.count('id="d-rigueur"'),
        "id glossaire": s.count('id="glossaire"'),
        "widget pareto": s.count('id="pareto-explorer"'),
        "widget reward-hack": s.count('id="reward-hack-demo"'),
        "widget family-nav": s.count('id="family-navigator"'),
        "widget epsilon": s.count('id="epsilon-calibrator"'),
        "bouton theme": s.count('id="theme_toggle"'),
        "<script>": s.count("<script>"),
        "</script>": s.count("</script>"),
    }
    print("\n# " + os.path.basename(p))
    for k, v in checks.items():
        print("   %-22s %s" % (k, v))
