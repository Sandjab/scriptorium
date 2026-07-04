---
name: leanmonograph
description: Use when asked to produce a "monographie"/monograph for a subject in this scriptorium repo with the LEAN pipeline — verify-first/write-once variant of /monograph (prose written AFTER the council, section-batched jurors, deterministic lint), same guarantees, fewer tokens, more readable prose. Triggered by /leanmonograph <sujet>.
---

# leanmonograph — monographie vérifiée, pipeline « vérifier d'abord, écrire une fois »

Variante **lean** de [`/monograph`](../monograph/SKILL.md). **Même produit** (un dossier de
thème peuplé + **un** document HTML « best-of », `build.py` déterministe) et **mêmes garanties
non négociables** — mais deux renversements d'architecture qui changent le coût ET la lisibilité.

`build.py`, le template et la charte sont **réutilisés** depuis `monograph` (aucune duplication).
Le profil de modèles est celui de `frugalmonograph` (recherche/vérification en Sonnet, jugement
structurant en Opus). Pour la spec du document, des widgets et de la charte : `monograph/SKILL.md`.

## Ce que le pipeline lean change (vs monograph/frugalmonograph)

| Levier | monograph / frugal | /leanmonograph |
|---|---|---|
| Ordre prose/vérification | prose à Extract (AVANT council) puis passes correctives (Réconcilie, Style-prose) | **prose APRÈS le council**, depuis les claims finaux — la dérive « prose pré-council » disparaît par construction ; Réconcilie et Style-prose n'existent plus |
| Council | 2-3 jurés **par claim** (~2 agents/claim, mêmes papiers re-fetchés par chaque juré) | **2 jurés par SECTION** (lentilles soutien / réfutation, ≤4 claims en une passe, fetchs amortis) **+ 1 juré dédié par claim `contestable`** (source primaire) |
| Voix de la prose | 1 agent par section, sans vue d'ensemble | **auteur unique** en tranches séquentielles (charte de voix, fil rouge du Plan, récapitulatif inter-tranches) + **relecture de continuité** (éditions ponctuelles appliquées en code) |
| Claims rejetés | pouvaient rester affirmés dans la prose (pattern connu) | l'auteur **ne les voit jamais** + `lint.py` les traque dans le rendu (adjudication par le build) |
| Faits prose-only | fact-check post-build manuel | **`lint.py --pre`** (chiffres absents de knowledge.json) + agent **Audit-prose** qui les vérifie à la source AVANT l'assemblage |
| Style | fan-out sur manifest/tldr/glossary + widgets | **widgets uniquement** (la prose naît stylée et relue) |

**Inchangé et non négociable** : tout fait `confirmed` s'appuie sur **≥ 2 sources indépendantes**
(seuil en code, `decideAudit`/`collectSources` **identiques** à monograph) ; `build.py` échoue
bruyamment ; plafonds `MAX_SECTIONS=9` / `MAX_CLAIMS_PER_SECTION=4` conservés.
Nuance council : un claim `contestable` a **3 verdicts** (soutien, réfutation, source primaire)
— `confirmed` à la majorité 2/3, comme le monograph complet (frugal exigeait 2/2).

## Déroulé (ce que TU fais quand /leanmonograph est invoqué)

Identique à `/monograph`, au **scriptPath** près.

1. **Sujet** = le texte passé à `/leanmonograph` (ou demande-le s'il manque).
2. **Slug** : terme canonique court en kebab-case ascii (cf. `/monograph`). ⚠️ Pour **comparer**
   lean vs frugal/monograph sur un même sujet, prends un slug **distinct** (sinon même
   `themes/<slug>/` et même `dist/`, ils s'écrasent).
3. **Scaffold** : `mkdir -p themes/<slug>/widgets` + `themes/<slug>/brief.md` (sujet + cadrage).
4. **Annonce le coût AVANT de lancer** (voir « Coût ») et laisse confirmer.
5. **Lance le Workflow** :
   - `scriptPath` : `.claude/skills/leanmonograph/workflow.js`
   - `args` : `{ "subject": "<sujet>", "slug": "<slug>", "themeDir": "<abs>/themes/<slug>" }`
   - (texte seul : `"widget": false`.) **Note le `runId`**. 1er lancement **sans** `resume` ;
     relance après interruption **avec** `"resume": true`.
6. **Rapporte** : `dist/<slug>.html`, le bilan d'audit (`confirmed`/`corrected`/`rejected`,
   ≥2 sources vérifié), les widgets retenus, et le **bilan lint** (`lint_flags`/`lint_fixed`
   du retour de build + `checked/fixed/hedged` de l'Audit-prose). Rapport d'audit annexe :
   `themes/<slug>/audit-report.json` + `.md` (mêmes champs que frugal — comparables).
   Si `build.success` est faux, **remonte l'erreur** — ne déclare pas un succès.

## Coût (ordre de grandeur — à annoncer avant de lancer)

Le fan-out Verify passe de ~2 agents/claim à **2 agents/section + 1 par contestable** :

```
6 (Sweep) + 1 (Plan) + N≤9 (Extract) + N×2 + Σ(contestables) (Verify) + ~1 (pointeurs)
  + ⌈N/3⌉ (prose, séquentiel) + 1 (tldr/glossaire) + 1 (relecture) + 1 (audit-prose)
  + 1 (widget-plan) + Σ_widgets(codeur + critic [+ re-code] + style) + 2 (Compose/Build) + I/O
```

Attendu ~60-70 agents (vs ~130 en frugal pour 36 claims) ; cible **~3,5-5 M tokens** (vs ~8 M),
**à valider par comparaison réelle** sur un thème (juger aux TOKENS, pas au nombre d'agents).
La prose est séquentielle (⌈N/3⌉ tranches Opus l'une après l'autre) — le mur d'horloge reste
dominé par Verify/Widgets qui, eux, sont parallèles.

## Reprise après interruption (rate-limit)

Checkpoints dans **`themes/<slug>/.leanmonograph/`** (isolés de `/monograph` et
`/frugalmonograph`) : `research.json` (après Plan), `sec-<id>.json` (par section auditée —
notes + claims audités), `prose.json` (après relecture de continuité), `widgets.json`.
Relance avec **`args.resume = true`** (mêmes `subject`/`slug`/`themeDir`) : saute Sweep+Plan,
ne re-vérifie que les sections sans checkpoint, saute Author/Relecture si `prose.json` existe,
saute la phase visuelle si `widgets.json` existe. Le chargement est **granulaire** (un loader
par section) : pas de plafond de sortie 32k comme le loader monolithique de frugal.
Un run **frais** (sans `resume`) ignore et réécrit tout checkpoint.

## Lint déterministe (`scripts/lint.py`)

Frontière code/jugement : le **code détecte**, le **modèle adjuge**.

- `lint.py <themeDir> --pre` (avant Compose, corpus = sections_draft/tldr/glossary) et
  `lint.py <themeDir>` (post, corpus = manifest/tldr/glossary **+ le texte visible des
  `widgets/*.html`** — `<script>`/`<style>` retirés ; les widgets ne comptent que pour
  `rejected_flags`, jamais pour `novel_numbers`, et ne sont vus qu'en mode post).
- `rejected_flags` : pivots (chiffres + noms propres distinctifs) des claims **rejetés** trouvés
  dans le texte visible, avec `hedged` (marqueur de réserve à ±350 c. d'un hit). Exit 2 si ≥1
  non hedgé → l'agent (Audit-prose ou Build) lit le contexte et adjuge : affirmation → corriger ;
  critique/réfutation/biblio → OK.
- `novel_numbers` : chiffres significatifs absents de `knowledge.json` = faits prose-only à
  vérifier à la source (l'Audit-prose les traite AVANT le build).

Testé sur le fixture réel `entity-linking-disambiguation` (5 rejets, hedges) : GREEN sur le
thème corrigé, RED (exit 2) quand on retire un hedge.

## Garanties (portées par `workflow.js` + `build.py` + `lint.py`)

- `knowledge.json` assemblé en JS depuis les verdicts ; le manifeste référence par id.
- Seuil **≥ 2 sources indépendantes** pour `confirmed` = règle en code, inchangée.
- L'auteur de prose ne reçoit **que** les claims retenus + les notes sourcées, avec interdiction
  d'introduire un fait précis de mémoire ; le lint + l'Audit-prose ferment la boucle.
- `build.py` échoue bruyamment (référence manquante, balise déséquilibrée, `file:///`, jeton
  non substitué).

## Itérer

`workflow.js` et `scripts/lint.py` sont dans CE dossier (modèles, plafonds, `PROSE_CHUNK`,
lentilles, charte `VOICE`). La rigueur/charte **partagée** (build.py, template) vit dans
`monograph`. Pas de modes top-up (`superwidgetOnly`/`figuresOnly`) ici : pour retrofitter un
thème existant, utiliser `/monograph` ou `/frugalmonograph`.
