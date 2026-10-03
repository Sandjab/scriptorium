# Brief — Agents d'interface graphique : percevoir un écran, agir, vérifier

L'angle directeur : **comment un agent pilote une interface graphique** — l'ancrage visuel
(grounding) comme problème central, l'espace d'actions, la boucle perception-action. Le fil
rouge : un plan correct ne vaut rien si le clic tombe à côté ; le corpus mesure les agents GUI,
ce document explique comment ils fonctionnent.

## Cadrage
Document de référence best-of, en français, public ingénieur ML. Gap vérifié par LECTURE
(2026-10-03, 8 thèmes lus) : `agent-evaluation-observability` pose le constat « les échecs
tiennent d'abord au grounding GUI » sans le mécanisme ; parseurs d'écran et modèles de grounding
(OmniParser, UGround, SeeClick, ScreenSpot) : 0 occurrence ; RL sur GUI réduit à une phrase
(CUA) ; injection visuelle, actions irréversibles, boucles propres à la GUI : absentes.

## Périmètre à couvrir
1. **Ancrage visuel** : coordonnées brutes vs marques (Set-of-Mark) ; capture d'écran vs arbre
   d'accessibilité vs DOM, et ce que chaque représentation perd.
2. **Parseurs d'écran et modèles de grounding** : OmniParser, SeeClick, UGround, CogAgent,
   ShowUI ; benchmarks ScreenSpot (et ScreenSpot-Pro) lus par leur méthode.
3. **Espace d'actions** : clic/saisie/raccourcis vs code exécuté (CoAct-1), et le compromis.
4. **Boucle perception-action et vérification d'état** côté agent.
5. **Benchmarks lus par leur méthode** : Mind2Web (hors ligne, traces), WebVoyager (juge),
   AndroidWorld ; WebArena/OSWorld seulement en renvoi.
6. **RL sur GUI** : DigiRL, UI-TARS, environnements en ligne.
7. **Modes d'échec** : boucles, actions irréversibles, injection par le contenu de l'écran
   (pop-ups, texte adverse visuel).
8. **Limites**.

## Délimitations strictes
- `agentic-ai` garde les scores et la chronologie (OSWorld, WebArena, WebVoyager, CUA, Agent S3,
  CoAct-1 à 60,76 %) — les citer, ne pas les redériver. ⚠️ Le corpus a deux valeurs pour la
  barre humaine OSWorld (72,36 % / 72,4 %) : ne pas propager l'écart.
- `agent-evaluation-observability` garde la construction et la vérification de WebArena et
  OSWorld (812 / 369 tâches, 134 fonctions d'évaluation).
- `multimodal-vlm` garde l'architecture VLM ; `document-ai` garde Pix2Struct.
- `agent-harness-engineering` garde la boucle d'agent générique.
- `agentic-rl-environments` garde le RL agentique générique (POMDP, RLVR).
- `llm-safety-jailbreaks` garde la mécanique de l'injection indirecte (Greshake, EchoLeak) —
  ici seulement sa forme visuelle propre à l'écran.
- Candidats voisins : `vision-language-action` (robotique), `agent-tool-security` (défense
  architecturale).

Domaine : llm-agents-generation, à trancher par /arrange.
