---
name: quifaitquoi
description: >-
  Use when asked which MODEL and which REASONING EFFORT each agent of a skill or
  multi-agent workflow should use — i.e. a per-agent (model × effort) tiering table with
  MINIMAL / OPTIMAL / MAXIMAL configs. Accepts the target by NAME or by PATH. Triggers:
  "/quifaitquoi <nom-ou-chemin>", "qui fait quoi", "quel modèle/effort pour les agents de
  <skill/workflow>", "tiering model x effort", "model effort par rôle d'agent".
---

# quifaitquoi — tiering (modèle × effort) par rôle d'agent

<!-- Skill garé temporairement dans ce repo (scriptorium est dédié aux monographies ;
     on le déplacera plus tard). Hors périmètre métier du repo, c'est assumé. -->

Produit, pour **chaque rôle d'agent** d'un skill ou d'un workflow multi-agents, la combinaison
**(modèle · effort de raisonnement)** minimale / optimale / maximale. Exécution **mono-appel** :
tu résous la cible, tu lis les fichiers qui définissent les agents, puis tu appliques le prompt
d'analyse ci-dessous et tu rends le tableau. (Pas d'orchestration multi-agents en v1.)

## 1. Cible

La **cible** est l'argument passé à `/quifaitquoi` : un **nom** OU un **chemin**.
Si aucun argument n'est fourni, **demande** lequel analyser (nom ou chemin) avant de continuer.

## 2. Résolution de la cible (déterministe)

**a) Ça ressemble à un chemin** si l'argument contient `/`, finit par `.js`/`.md`/`.py`, ou
correspond à un fichier/dossier existant (vérifie avec `ls`).
- Dossier → lis les fichiers qui définissent des agents *dans* ce dossier.
- Fichier → lis-le ; s'il vit dans un dossier de skill, lis aussi le `SKILL.md` voisin.

**b) Sinon c'est un nom** → cherche dans CET ORDRE, et arrête-toi au premier qui matche :
1. `.claude/skills/<nom>/` (repo courant)
2. `.claude/workflows/<nom>.js` (repo courant)
3. `~/.claude/skills/<nom>/`
4. caches de plugins : `~/.claude/plugins/**/skills/<nom>/` (glob)

- **Plusieurs candidats** (homonymes à des emplacements différents) → **liste-les et demande** lequel.
- **Aucun candidat** → dis-le franchement et demande un chemin explicite.

**c) Fichiers à lire INTÉGRALEMENT** (ceux qui portent la définition et les *prompts* des agents) :
`SKILL.md`, tout `*.js` de workflow (ex. `workflow.js`), `agents/*.md`, et tout script référencé
qui contient des prompts d'agents (suis les renvois depuis le workflow / le SKILL.md). Utilise
`Read`/`Grep`/`Glob`. Ne te fie pas aux intitulés : lis le code réel.

## 3. Garde-fou « pas multi-agents »

Si, après lecture, la cible n'a **pas** de structure multi-agents (un seul prompt ; aucun
`agent()`/`parallel()`/`pipeline()`, aucun `agents/*.md`, aucun fan-out) → **dis-le explicitement**
et ne fabrique pas un tableau artificiel : au plus **une ligne** décrivant l'unique rôle.
**N'invente jamais de rôles** pour remplir un tableau.

## 4. Analyse — applique ce prompt aux fichiers lus

> Le bloc ci-dessous EST l'analyse à exécuter. « L'entrée » = les fichiers que tu viens de lire
> à l'étape 2. L'échelle de modèles est un défaut : **adapte-la** si l'utilisateur nomme d'autres
> modèles (ou une autre stack).

### Rôle
Tu es ingénieur LLM. Tu disposes du code (ou des définitions d'agents) d'un SKILL ou WORKFLOW
MULTI-AGENTS (les fichiers lus à l'étape 2). Produis un tableau de tiering recommandant, pour
CHAQUE rôle d'agent, la combinaison (modèle · effort de raisonnement) MINIMALE / OPTIMALE / MAXIMALE.

### Échelle de modèles (du moins au plus capable/coûteux — ADAPTE à la stack visée)
- "Haiku 4.5"  : rapide/économique. Fort en transformations mécaniques, écritures verbatim,
                 extraction simple, sorties structurées courtes, résumé direct. Faible en
                 raisonnement multi-étapes, vérification adversariale, code interactif correct.
- "Sonnet 4.6" : raisonnement général solide, bon codage, excellent suivi d'instructions, à
                 coût bien moindre qu'Opus. Bon défaut pour rédaction/codage/revue/synthèse.
- "Opus 4.8"   : meilleur raisonnement profond, jugement adversarial, code le plus difficile.
                 Coût le plus élevé et plus lourd (pression de rate-limit).

### Échelle d'effort (raisonnement/thinking par appel)
none < low < medium < high. L'effort se règle sur la PROFONDEUR DE RAISONNEMENT exigée par la
tâche, PAS sur son importance. L'effort SUBSTITUE PARTIELLEMENT au tier : un cran de modèle
économisé peut se rattraper par +1 d'effort, surtout sur le raisonnement adversarial et le code.

### Définitions (à appliquer STRICTEMENT et de façon COHÉRENTE entre rôles)
- min     = la config la PLUS BASSE encore ACCEPTABLE : sortie correcte, conforme au schéma,
            sans dégradation qui casserait une GARANTIE du pipeline.
- optimal = meilleur rapport qualité/coût : la config où monter d'un cran n'apporte plus
            assez de qualité pour CETTE tâche précise.
- max     = plafond utile : la config au-dessus de laquelle AUCUN gain n'est atteignable.
Une cellule = "Modèle · effort" (ex. "Sonnet 4.6 · high"). Les trois peuvent être identiques.
Sois honnête : ni Opus·high partout par prudence, ni Haiku·none partout par économie.

### Méthode
1. ÉNUMÈRE EXHAUSTIVEMENT chaque rôle d'agent DISTINCT (repère-les par leurs appels/labels
   dans le code), sa MULTIPLICITÉ (×1, ×N, ×beaucoup) et signale ceux qui DOMINENT le coût.
   N'invente aucun rôle ; ne fusionne pas deux rôles distincts.
2. Pour CHAQUE rôle, ANCRE ton jugement dans l'ARCHITECTURE RÉELLE lue dans le code, pas dans
   l'intitulé. Réponds en interne à :
   - difficulté cognitive réelle (transcription mécanique ? recherche web + fidélité de source ?
     raisonnement adversarial ? code interactif ? jugement éditorial ? synthèse fidèle ?) ;
   - RISQUE D'ERREUR SILENCIEUSE : une mauvaise sortie passe-t-elle le schéma SANS déclencher
     d'échec ? (si oui, remonte le plancher) ;
   - FILETS DE RATTRAPAGE EN AVAL : vote/quorum, re-critique, étape déterministe qui échoue
     bruyamment, seuils, dédup. S'ils couvrent ce rôle → le plancher peut descendre. S'il n'y
     en a AUCUN (sortie jamais re-vérifiée ni exécutée) → remonte le plancher ;
   - la sortie est-elle exécutée/vérifiée plus loin, ou part-elle telle quelle en production ?
3. PONDÈRE PAR LA MULTIPLICITÉ : un rôle ×beaucoup qui domine le coût mérite l'optimal le plus
   réfléchi — c'est le levier coût/latence principal.
4. NORMALISE LA CALIBRATION : « acceptable » doit avoir le MÊME sens partout ; corrige toute
   incohérence entre rôles de difficulté comparable.

### Sortie
1. Un tableau Markdown :
   | Rôle | Multiplicité | Min (modèle·effort) | Optimal (modèle·effort) | Max (modèle·effort) | Justification |
   La justification = 1 phrase liant difficulté réelle + risque silencieux + filet aval.
2. PROFIL CIBLE actionnable : quelle config (modèle·effort) câbler par rôle pour maximiser
   qualité/coût sur l'ensemble, en partant de l'état actuel (souvent : tout au même tier).
3. LEVIER N°1 coût/latence (indice : le rôle qui domine le coût).
4. RÉSERVES : précise que l'analyse est A PRIORI, sans éval empirique ; nomme les 1-2 frontières
   les plus incertaines (typiquement les rôles de raisonnement dur et de code) à valider par un
   run comparatif réel (tier × effort) avant de figer.
