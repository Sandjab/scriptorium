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
   - **Note le `runId`** retourné (utile pour une reprise même-session). Premier lancement : **sans**
     `resume`. Relance après interruption : ajoute `"resume": true` (voir « Reprise après interruption »).

   Le workflow exécute : Sweep → Plan → Extract → Verify (council adversarial) →
   Author (écrit `knowledge.json`/`glossary.json`/`tldr.json`) → Widgets (planner →
   codeurs → critic) → Compose (écrit `manifest.json`) → Build (`build.py` → `dist/` + auto-vérifs).

6. **Rapporte** le résultat retourné par le workflow : le document `dist/<slug>.html`, le bilan
   d'audit (`confirmed`/`corrected`/`rejected`, ≥2 sources vérifié) et le bilan widgets
   (retenus). Le workflow écrit aussi un **rapport d'audit annexe** —
   `themes/<slug>/audit-report.json` + `audit-report.md` : par claim, combien de jurés
   corroborent / réfutent / corrigent, l'audit final, et s'il a été retenu. Si `build.success`
   est faux, **remonte l'erreur** (build.py échoue bruyamment) — ne déclare pas un succès.

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

**Deux registres (`kind`)** : `probe` (illustre **un** mécanisme isolé) et `process` (**super-widget
synoptique** : un **processus de bout en bout** assemblé sur une instance jouet — itératif
*avant→arrière→mise à jour→jusqu'à convergence*, ou pipeline ≥3 étapes chaînées). Le planner tague
chaque widget ; le super-widget reste un `{"type":"widget"}` ordinaire (charte/`build.py` inchangés).
**Pas de plafond** : la rubrique stricte « vrai processus, jamais un mécanisme isolé » est le seul frein.

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
- Après une interruption (rate-limit), **NE relance JAMAIS un run frais** (re-paie tout) :
  **reprends** — voir « Reprise après interruption ».

## Reprise après interruption (rate-limit)

Le fan-out massif se fait régulièrement **rate-limiter côté serveur** (`Rate limited` /
`temporarily limiting requests` — **not your usage limit**). Symptôme TROMPEUR : avalanche de
« completed without calling StructuredOutput » + `knowledge.json` vide. Ce **n'est pas un bug** :
un agent rate-limité n'appelle jamais `StructuredOutput`. **NE relance pas un run frais** (re-paie
tout, plusieurs M tokens). Deux mécanismes de reprise, **complémentaires** :

1. **Reprise moteur (même session)** — réutilise le cache des agents déjà terminés. Garde le
   **`runId`** affiché au lancement du Workflow. Si `/workflows` indique « paused » ou si des agents
   ont été rate-limités : `TaskStop` le run, puis relance
   `Workflow({ scriptPath: ".claude/skills/monograph/workflow.js", resumeFromRunId: "<runId>", args })`
   avec les **mêmes args**. ⚠️ **Same-session uniquement**, et **historiquement peu fiable** (souvent
   re-payé en pratique) — d'où le mécanisme 2. Un `/clear` ou une nouvelle session **détruit** ce cache.

2. **Reprise disque (survit à `/clear` et au changement de session)** — relance le Workflow avec
   **`args.resume = true`** (mêmes `subject`/`slug`/`themeDir`). Le workflow écrit, au fil de l'eau, des
   checkpoints **incrémentaux** dans `themes/<slug>/.monograph/` : `research.json` (après Plan), un
   `sec-<id>.json` par section auditée (pendant Verify), `widgets.json` (après Widgets). Une reprise
   **saute Sweep+Plan**, **ne re-vérifie QUE les sections sans checkpoint**, et **saute Widgets** si déjà
   fait — elle ne re-paie donc que le travail réellement inachevé (couvre une tempête de rate-limit
   *pendant* Verify, même après `/clear`).

Un run **FRAIS** (sans `args.resume`) **ignore et réécrit** tout checkpoint existant : l'intention
« fraîche vs reprise » est portée par `args.resume`, jamais devinée. (Réflexe : 1er lancement sans
`resume` ; toute relance après échec **avec** `resume:true`.)

## Retrofit : ajouter un super-widget à un article existant

Pour équiper un thème **déjà construit** sans tout régénérer : relance le Workflow avec
`args.superwidgetOnly = true` (mêmes `subject`/`slug`/`themeDir`). Le mode **top-up** lit les
fichiers persistés (`sections_draft.json`, `knowledge.json`, `manifest.json`), exécute **seulement**
planner-process → codeur → critic → **insertion chirurgicale** dans `manifest.json` → `build.py`.
**Aucune re-vérification factuelle** ; le planner décide la pertinence par thème (peut rendre 0,
le thème est alors laissé tel quel). N'a **pas** besoin de `.monograph/`.

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
