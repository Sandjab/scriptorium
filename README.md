# scriptorium

Fabrique de documents multi-thèmes. Chaque thème est transformé en une **monographie**
partageant une charte graphique commune.

Un document unique : abstract, sections vérifiées, widgets démonstratifs, exercices, biblio, pointeurs, glossaire.

## Structure

```
themes/<slug>/            un dossier par thème (slug kebab-case, sans accents)
  knowledge.json          base de faits vérifiée (source de vérité)
  glossary.json · tldr.json
  widgets/                widgets interactifs du thème
  manifest.json           manifeste-vue du document
  dist/                   le HTML généré
.claude/skills/monograph/  le skill local qui produit une monographie
```

## Produire une monographie

Dans Claude Code, invoque le skill local avec un sujet (d'une phrase à une page) :

```
/monograph <sujet>
```

Le skill effectue une recherche approfondie, vérifie chaque fait contre **≥ 2 sources
indépendantes** (passe adversariale/council), construit la base de faits, puis assemble
le document de façon déterministe. Le modèle juge ; le code assemble.

## Thèmes

- **automatic-prompt-optimization** — premier thème : panorama des approches d'APO +
  contrat d'architecture. Le document est dans `themes/automatic-prompt-optimization/dist/`.
  Cette édition a été construite à la main (avant le skill) ; son pipeline d'origine est
  conservé, gelé, sous `themes/automatic-prompt-optimization/legacy/`.
- **bloom-filters** — premier thème **généré par `/monograph`** : panorama vérifié des filtres
  de Bloom (principe, garanties, variantes, limites). 16 faits audités (10 confirmés, 6 corrigés)
  appuyés sur 46 sources. Le document est dans `themes/bloom-filters/dist/`.

## Statut

- Phase 0 — restructure & migration : ✅
- Phase 1 — générateur déterministe (`.claude/skills/monograph/` : charte + `build.py`, 8 tests) : ✅
- Phase 2 — workflow deep-research + `SKILL.md` du skill `monograph` : ✅
  (validé sur `bloom-filters` : `SKILL.md` + `workflow.js` embarqué, 6 phases
  Sweep→Plan→Extract→Verify→Author→Compose→Build)
