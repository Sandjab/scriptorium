---
name: frugalmonograph
description: Use when asked to produce a "monographie"/monograph for a subject in this scriptorium repo AT REDUCED COST — the frugal variant of /monograph. Same verified pipeline (single best-of HTML reference document), but cheaper models on research/verification, a 2-juror council and hard caps. Triggered by /frugalmonograph <sujet>.
---

# frugalmonograph — monographie vérifiée, à coût réduit

Variante **frugale** de [`/monograph`](../monograph/SKILL.md). **Même produit** (un dossier de
thème peuplé + **un** document HTML « best-of », recherche vérifiée → assemblage déterministe
`build.py`) et **mêmes garanties non négociables** — seul le **profil de coût** change.

Pour la spec complète du document, des widgets et de la charte, voir le SKILL.md de `monograph` :
ce skill ne réécrit que ce qui lui est propre. `build.py`, le template et la charte sont
**réutilisés** depuis `monograph` (aucune duplication ; le workflow pointe déjà
`.claude/skills/monograph/scripts/build.py`).

## Ce que le profil frugal change (vs /monograph)

| Levier | /monograph | /frugalmonograph |
|---|---|---|
| Modèle Sweep / Extract / Verify / pointeurs | hérité (Opus) | **Sonnet** (`M_RESEARCH`) |
| Modèle écritures & checkpoints (I/O) | hérité (Opus) | **Sonnet** (`M_IO`) |
| Modèle Plan / Author / Widgets / Compose / Build | Opus | **Opus (inchangé)** — jugement structurant |
| Council par claim | 2 jurés (`established`) / **3** (`contestable`) | **2 jurés** dans tous les cas |
| Verify : recherche web | recherche libre | **part d'abord des `candidate_sources`**, web en secours |
| Plafonds | aucun | **MAX_SECTIONS=9**, **MAX_CLAIMS_PER_SECTION=4** (garde-fous) |

**Inchangé et non négociable** : tout fait `confirmed` s'appuie sur **≥ 2 sources indépendantes**
(seuil en code, `decideAudit`/`collectSources` identiques) ; `build.py` échoue bruyamment.
Le council `contestable` réduit à 2 lentilles = `[réfutation, source primaire]`.

## Déroulé (ce que TU fais quand /frugalmonograph est invoqué)

Identique à `/monograph`, au **scriptPath** près. Le gros du travail est un **Workflow**
multi-agents (`workflow.js` de CE dossier).

1. **Sujet** = le texte passé à `/frugalmonograph` (ou demande-le s'il manque).
2. **Slug** : terme canonique court en kebab-case ascii (cf. `/monograph` pour la règle).
   ⚠️ Si tu veux **comparer** frugal vs monograph sur un même sujet, prends un slug **distinct**
   (ex. `bloom-filters-frugal`) : sinon les deux écrivent le **même** `themes/<slug>/` et le même
   `dist/<slug>.html`, et s'écrasent.
3. **Scaffold** :
   ```bash
   mkdir -p themes/<slug>/widgets
   ```
   Écris `themes/<slug>/brief.md` : le sujet tel que fourni + 1-2 lignes de cadrage.
4. **Annonce le coût AVANT de lancer** (voir « Coût ») et laisse confirmer.
5. **Lance le Workflow** avec le script de CE dossier et le dossier en **chemin absolu** :
   - `scriptPath` : `.claude/skills/frugalmonograph/workflow.js`
   - `args` : `{ "subject": "<sujet>", "slug": "<slug>", "themeDir": "<abs>/themes/<slug>" }`
   - (texte seul, sans widgets : ajoute `"widget": false`.)
   - **Note le `runId`** retourné. Premier lancement : **sans** `resume`. Relance après
     interruption : ajoute `"resume": true` (voir « Reprise »).
6. **Rapporte** : `dist/<slug>.html`, le bilan d'audit (`confirmed`/`corrected`/`rejected`,
   ≥2 sources vérifié) et les widgets retenus. Le workflow écrit aussi un **rapport d'audit
   annexe** — `themes/<slug>/audit-report.json` (réexploitable) + `audit-report.md` (lisible) :
   par claim, combien de jurés corroborent / réfutent / corrigent, l'audit final, et s'il a été
   retenu (utile pour **comparer frugal vs monograph**). Si `build.success` est faux,
   **remonte l'erreur** — ne déclare pas un succès.

## Coût (ordre de grandeur — à annoncer avant de lancer)

Même structure de fan-out que `/monograph` (Verify et Widgets dominent), mais **moins cher par
agent** : la recherche et la vérification (~90 % du volume d'appels) tournent en **Sonnet**, le
council est à **2 jurés** partout, et chaque juré **réutilise d'abord les sources déjà trouvées**.
Nombre d'agents :

```
6 (Sweep) + 1 (Plan) + N≤9 (Extract) + Σ_sections(claims≤4 × 2 jurés) + ~1 (pointeurs)
  + 1 (Author) + 1 (widget-plan) + Σ_widgets(1 codeur + 1 critic [+1 re-code]) + 2 (Compose/Build)
```

- **Juge la conso aux TOKENS par agent, pas au nombre de fichiers/journaux.** (Pas de chiffre
  absolu garanti ici : le coût par agent web varie selon les fetch.)
- Les phases **Widgets / Author / Compose / Build restent en Opus** : coder/critiquer du HTML
  interactif et rédiger glossaire/manifeste n'est pas dégradé pour économiser.
- Après une interruption (rate-limit), **NE relance JAMAIS un run frais** (re-paie tout) :
  **reprends** — voir ci-dessous.

## Reprise après interruption (rate-limit)

Identique à `/monograph`, mais les checkpoints vivent dans **`themes/<slug>/.frugalmonograph/`**
(isolés de `/monograph` : pas de collision si les deux ont tourné sur un même thème).

- **Reprise disque** (survit à `/clear` et au changement de session) : relance le Workflow avec
  **`args.resume = true`** (mêmes `subject`/`slug`/`themeDir`). Le workflow relit
  `research.json` (après Plan), les `sec-<id>.json` (sections auditées), `widgets.json`, et ne
  re-paie que le travail réellement inachevé. Un run **FRAIS** (sans `resume`) les **ignore et
  réécrit** : l'intention fraîche-vs-reprise est portée par `args.resume`, jamais devinée.
- **Reprise moteur** (même session) : `resumeFromRunId: "<runId>"` — historiquement peu fiable,
  d'où la reprise disque.

(Réflexe : 1er lancement sans `resume` ; toute relance après échec **avec** `resume:true`.)

## Garanties (portées par `workflow.js` + `build.py`)

- Les **faits** (`knowledge.json`) sont assemblés en JS depuis les verdicts vérifiés, référencés
  par id dans le manifeste — jamais recopiés.
- Seuil **`≥ 2 sources indépendantes`** pour `confirmed` = règle en code ; l'**indépendance** des
  sources est jugée par les jurés. **Le profil frugal ne touche pas ce seuil.**
- `build.py` échoue sur référence manquante, type inconnu, balise déséquilibrée, `file:///`
  résiduel ou jeton non substitué.

## Itérer

`workflow.js` est dans CE dossier. Pour ajuster le profil frugal (modèles `M_RESEARCH`/`M_IO`,
plafonds `MAX_SECTIONS`/`MAX_CLAIMS_PER_SECTION`, lentilles du council), édite-le puis relance.
Pour changer la rigueur/charte **partagée**, c'est dans `monograph` (build.py, template).
