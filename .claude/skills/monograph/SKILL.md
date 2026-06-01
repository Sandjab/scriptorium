---
name: triptych
description: Use when asked to produce, generate or build a "triptyque"/triptych for a subject in this scriptorium repo — turning a topic (a phrase to a page) into a verified, multi-edition HTML document (référence / publication / pédagogique). Triggered by /triptych <sujet>.
---

# triptych — fabriquer un triptyque vérifié

Transforme un **sujet** en un dossier de thème peuplé + 3 éditions HTML, via une
recherche approfondie vérifiée puis un assemblage déterministe (`build.py`).

**Frontière** : le modèle juge (recherche, rédige, vérifie) ; le code assemble. La
rigueur factuelle n'est pas négociable — tout fait `confirmed` s'appuie sur **≥ 2
sources indépendantes**.

## Déroulé (ce que TU fais quand /triptych est invoqué)

Le gros du travail est un **Workflow** multi-agents embarqué (`workflow.js`). Comme un
script Workflow n'a pas d'accès disque, le **setup déterministe** t'incombe, puis tu
lances le workflow, puis tu rapportes.

1. **Sujet** = le texte passé à `/triptych` (ou demande-le s'il manque).
2. **Slug** : un terme canonique court en kebab-case ascii (minuscules, accents
   translittérés, non-alphanumérique → `-`, sans articles). Ex. « Les filtres de Bloom »
   → `bloom-filters`. Si le slug est ambigu, propose-le et fais confirmer.
3. **Scaffold** : crée le dossier du thème.
   ```bash
   mkdir -p themes/<slug>/editions themes/<slug>/widgets
   ```
   Écris `themes/<slug>/brief.md` : le sujet tel que fourni + 1-2 lignes de cadrage.
4. **Annonce le coût AVANT de lancer** (voir « Coût » plus bas) : une ligne — ordre de
   grandeur en agents + tokens — et laisse l'utilisateur confirmer. Le fan-out est massif.
5. **Lance le Workflow** avec le script embarqué et le dossier en **chemin absolu** :
   - `scriptPath` : `.claude/skills/triptych/workflow.js`
   - `args` : `{ "subject": "<sujet>", "slug": "<slug>", "themeDir": "<abs>/themes/<slug>" }`
   - (texte seul : ajoute `"widget": false` ; widget inclus par défaut.)

   Le workflow exécute : Sweep → Plan → Extract → Verify (council adversarial) →
   Author (écrit `knowledge.json`/`glossary.json`/`tldr.json`/widget) → Compose (écrit
   les 3 `editions/*.manifest.json`) → Build (`build.py` → `dist/` + auto-vérifs).

6. **Rapporte** le résultat retourné par le workflow : les 3 HTML de `dist/`, et le
   bilan d'audit (`confirmed`/`corrected`/`rejected`, ≥2 sources vérifié). Si `build.success`
   est faux, **remonte l'erreur** (build.py échoue bruyamment) — ne déclare pas un succès.

## Coût (ordre de grandeur — à annoncer avant de lancer)

Le workflow fait du **fan-out massif** ; **Verify domine** le total. Nombre d'agents :

```
6 (Sweep) + 1 (Plan) + N (Extract) + Σ_sections(claims × jurés) + ~1 (pointeurs) + 3 (Author/Compose/Build)
```

avec `N` = sections (4-9) et **jurés = 3 si le claim est `contestable`, 2 si `established`**
(plafond câblé dans `workflow.js`). Pour un sujet riche (N≈7, ~3 claims/section dont 1
contestable) ≈ **55-70 agents**, dont l'essentiel en Verify. Un agent Verify (WebSearch +
WebFetch) a été observé à **~70k tokens** → la note se compte en **millions de tokens de
sortie**, pas en « quelques appels ».

Conséquences :
- **Juge la conso aux TOKENS par agent, pas au nombre de fichiers/journaux.**
- Un `resume` après interruption **re-paie le run** (pas de réutilisation de cache fiable
  constatée) — ne relance pas « pour pas cher ».

## Garanties (portées par `workflow.js` + `build.py`)

- Les **faits** (`knowledge.json`) sont assemblés en JS depuis les verdicts vérifiés, pas
  recopiés dans les vues ; les manifestes les **référencent par id**.
- Seuil `≥ 2 sources indépendantes` pour `confirmed` = règle en code ; l'**indépendance**
  des sources est jugée par les jurés.
- `build.py` échoue sur référence manquante, type inconnu, balise déséquilibrée,
  `file:///` résiduel ou jeton non substitué.

## Itérer

`workflow.js` est versionné dans ce dossier. Pour ajuster la rigueur, le nombre d'angles
ou la politique d'édition, édite-le puis relance ; rien à régénérer ailleurs.
