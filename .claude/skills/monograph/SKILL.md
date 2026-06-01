---
name: monograph
description: Use when asked to produce, generate or build a "monographie"/monograph (a single verified reference document) for a subject in this scriptorium repo — turning a topic (a phrase to a page) into a verified HTML document. Triggered by /monograph <sujet>.
---

# monograph — fabriquer une monographie vérifiée

Transforme un **sujet** en un dossier de thème peuplé + **un** document HTML « best-of »,
via une recherche approfondie vérifiée puis un assemblage déterministe (`build.py`).

**Frontière** : le modèle juge (recherche, rédige, vérifie, sélectionne/critique les widgets) ;
le code assemble. La rigueur factuelle n'est pas négociable — tout fait `confirmed` s'appuie
sur **≥ 2 sources indépendantes**.

## Déroulé (ce que TU fais quand /monograph est invoqué)

Le gros du travail est un **Workflow** multi-agents embarqué (`workflow.js`). Comme un script
Workflow n'a pas d'accès disque, le **setup déterministe** t'incombe, puis tu lances le
workflow, puis tu rapportes.

1. **Sujet** = le texte passé à `/monograph` (ou demande-le s'il manque).
2. **Slug** : un terme canonique court en kebab-case ascii (minuscules, accents translittérés,
   non-alphanumérique → `-`, sans articles). Ex. « Les filtres de Bloom » → `bloom-filters`.
   Si le slug est ambigu, propose-le et fais confirmer.
3. **Scaffold** : crée le dossier du thème.
   ```bash
   mkdir -p themes/<slug>/widgets
   ```
   Écris `themes/<slug>/brief.md` : le sujet tel que fourni + 1-2 lignes de cadrage.
4. **Annonce le coût AVANT de lancer** (voir « Coût ») : une ligne — ordre de grandeur en
   agents + tokens — et laisse l'utilisateur confirmer. Le fan-out est massif.
5. **Lance le Workflow** avec le script embarqué et le dossier en **chemin absolu** :
   - `scriptPath` : `.claude/skills/monograph/workflow.js`
   - `args` : `{ "subject": "<sujet>", "slug": "<slug>", "themeDir": "<abs>/themes/<slug>" }`
   - (texte seul, sans widgets : ajoute `"widget": false` ; widgets inclus par défaut.)

   Le workflow exécute : Sweep → Plan → Extract → Verify (council adversarial) →
   Author (écrit `knowledge.json`/`glossary.json`/`tldr.json`) → Widgets (planner →
   codeurs → critic) → Compose (écrit `manifest.json`) → Build (`build.py` → `dist/` + auto-vérifs).

6. **Rapporte** le résultat retourné par le workflow : le document `dist/<slug>.html`, le bilan
   d'audit (`confirmed`/`corrected`/`rejected`, ≥2 sources vérifié) et le bilan widgets
   (retenus). Si `build.success` est faux, **remonte l'erreur** (build.py échoue bruyamment) —
   ne déclare pas un succès.

## Le document (superset best-of)

Un seul HTML, le plus complet : `abstract → [sections + claims ; chaque widget après sa
section] → 1-2 exercises → biblio → pointers → glossary`.

## Widgets — ce qu'on attend (spec)

**Quand** : chaque **concept ou mécanisme clé NON TRIVIAL** du sujet où *montrer > expliquer*
(le montrer aide à visualiser/comprendre, ou rend la compréhension plus simple) mérite **son**
widget. Rien pour le trivial ou le purement déclaratif. Un widget par mécanisme (dédup).

**Quoi** : un widget interactif **autoporteur** qui démontre vraiment le mécanisme (manipulable,
pas décoratif). Aussi complexe que nécessaire, **complexité proportionnée à la valeur
explicative**.

**Contraintes strictes** (sinon `build.py` échoue) : un seul bloc `<div class="widget">…</div>`
+ `<style>` + `<script>` ; AUCUNE ressource externe, AUCUN `file:///`, AUCUN
`alert/confirm/prompt` ; balises `<section>/<details>/<script>` équilibrées ; id/classes
préfixés par le ref. La phase Widgets sélectionne (planner), code (fan-out), puis **relit**
(critic, 1 révision possible).

## Coût (ordre de grandeur — à annoncer avant de lancer)

Le workflow fait du **fan-out massif** sur **deux** étapes : **Verify** (council) et **Widgets**
(codage interactif). Nombre d'agents :

```
6 (Sweep) + 1 (Plan) + N (Extract) + Σ_sections(claims × jurés) + ~1 (pointeurs)
  + 1 (Author) + 1 (widget-plan) + Σ_widgets(1 codeur + 1 critic [+1 re-code]) + 2 (Compose/Build)
```

avec **jurés = 3 si le claim est `contestable`, 2 si `established`** (plafond câblé). Verify
domine toujours (un agent Verify ≈ ~70k tokens). Les widgets ajoutent un **2ᵉ fan-out** : coder
et critiquer du HTML interactif n'est pas gratuit.

Conséquences :
- **Juge la conso aux TOKENS par agent, pas au nombre de fichiers/journaux.**
- Un `resume` après interruption **re-paie le run** (pas de réutilisation de cache fiable
  constatée) — ne relance pas « pour pas cher ».

## Garanties (portées par `workflow.js` + `build.py`)

- Les **faits** (`knowledge.json`) sont assemblés en JS depuis les verdicts vérifiés, pas
  recopiés dans la vue ; le manifeste les **référence par id**.
- Seuil `≥ 2 sources indépendantes` pour `confirmed` = règle en code ; l'**indépendance** des
  sources est jugée par les jurés.
- `build.py` échoue sur référence manquante, type inconnu (dont `tldr`/`onramp`, retirés),
  balise déséquilibrée, `file:///` résiduel ou jeton non substitué.

## Itérer

`workflow.js` est versionné dans ce dossier. Pour ajuster la rigueur, les angles ou la
politique de widgets, édite-le puis relance ; rien à régénérer ailleurs.
