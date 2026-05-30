# scriptorium

Fabrique de documents multi-thèmes. Chaque thème est transformé en un **triptyque**
d'éditions HTML autonomes partageant une charte graphique commune :

- **référence** — superset dense, tous les widgets ; consultation experte ;
- **publication** — abstract + widgets phares ; lecture suivie ;
- **pédagogique** — on-ramp, tooltips, exercices ; apprentissage.

## Structure

```
themes/<slug>/            un dossier par thème (slug kebab-case, sans accents)
  knowledge.json          base de faits vérifiée (source de vérité)
  glossary.json · tldr.json
  widgets/                widgets interactifs du thème
  editions/               3 manifestes-vues (reference/publication/pedagogique)
  dist/                   les 3 HTML générés
.claude/skills/triptych/  le skill local qui produit un triptyque
```

## Produire un triptyque

Dans Claude Code, invoque le skill local avec un sujet (d'une phrase à une page) :

```
/triptych <sujet>
```

Le skill effectue une recherche approfondie, vérifie chaque fait contre **≥ 2 sources
indépendantes** (passe adversariale/council), construit la base de faits, puis assemble
les 3 éditions de façon déterministe. Le modèle juge ; le code assemble.

## Thèmes

- **automatic-prompt-optimization** — premier thème : panorama des approches d'APO +
  contrat d'architecture. Les 3 éditions sont dans `themes/automatic-prompt-optimization/dist/`.
  Cette édition a été construite à la main (avant le skill) ; son pipeline d'origine est
  conservé, gelé, sous `themes/automatic-prompt-optimization/legacy/`.

## Statut

- Phase 0 — restructure & migration : ✅
- Phase 1 — générateur déterministe (`build.py` + charte) : en construction
- Phase 2 — workflow deep-research du skill `triptych` : à venir
