# Génération de code par modèle de langage : ce que le modèle apprend et ce qu'on peut en garantir

Candidat du backlog (`docs/candidate-themes.md`, priorité moyenne, ajouté le 2026-08-06),
lancé le 2026-09-19 en 60e run `/leanmonograph`.
Domaine visé : `llm-agents-generation` (`/arrange` tranchera l'insertion).

⚠️ Ce fichier est une TRACE : `workflow.js` ne le lit pas. Le cadrage effectif passe
entièrement par `args.subject`.

## Gap re-vérifié avant lancement (2026-09-19)

Lecture de la prose des sections voisines (pas au grep seul), corpus à 99 thèmes :
- `agent-evaluation-observability` couvre EN PROFONDEUR SWE-bench (2 294 instances, protocole
  FAIL_TO_PASS/PASS_TO_PASS, Verified : 93 annotateurs, 68,3 % écartés, 500 instances ; audit
  OpenAI de février 2026 : 59,4 % de 138 tâches, bascule vers Pro), SWE-Bench Illusion,
  SWE-Bench+ (12,47 % → 3,97 %), et l'estimateur pass@k de Chen et al. (n = 100, dual pass^k).
  → Le brief du backlog demandait « la lignée d'évaluation … SWE-bench, Verified, Pro » et
  « pass@k et ce qu'il masque » : RESSERRÉ — SWE-bench n'est cité qu'en renvoi, pass@k n'est
  repris que pour ce qui est propre au code (échantillonnage chaud, filtrage par tests,
  clustering AlphaCode, best-of-n vs pass@1).
- `pretraining-data-curation` couvre la décontamination par n-grammes (GPT-3/PaLM/GPT-4/Phi-4,
  Gopher, Dolma) ; `benchmark-contamination` est un candidat SÉPARÉ du backlog (renvoi cassé A2).
  → « contamination des benchmarks » RETIRÉE du plan comme section ; mention en renvoi seulement.
- `agentic-ai` (section applications logiciel) : Claude Code, ChatDev, CoAct-1 — usages, pas
  le modèle.
- `agent-harness-engineering` : SWE-agent, OpenHands, Aider = la BOUCLE ; `agentic-rl-environments` :
  RLVR et ses environnements.
- Non couverts nulle part (0 occurrence substantielle) : Codex (2021) et la lignée des modèles de
  code (AlphaCode, CodeGen, StarCoder/The Stack, Code Llama, DeepSeek-Coder, Qwen-Coder),
  fill-in-the-middle/infilling (Bavarian et al.), complétion au niveau du dépôt (RepoCoder,
  CrossCodeEval, RepoBench), tests comme oracle de sélection (CodeT, clustering AlphaCode),
  réparation de programmes (Self-Debug, Reflexion sur code, Defects4J), sécurité du code généré
  (Pearce et al. « Asleep at the keyboard », dépendances hallucinées / slopsquatting), effet du
  code dans le mélange de pré-entraînement sur le raisonnement.

## Délimitations (à tenir dans `args.subject`)

- `agent-evaluation-observability` garde SWE-bench comme instrument et l'écart de harness ;
  `agent-harness-engineering` garde la boucle et l'outillage ; `agentic-rl-environments` garde le
  RLVR ; `pretraining-data-curation` garde la décontamination ; `ia-productivite-esn` garde
  l'effet organisationnel ; `reasoning-test-time-compute` garde le raisonnement générique.
- Angle propre : **le code comme modalité d'entraînement et d'évaluation** — ce que le modèle
  apprend (corpus, formats, contexte de dépôt), comment on sélectionne et répare ses sorties par
  exécution, et ce qu'on peut garantir ou non (sécurité, dépendances inventées).

## Bilan du run (2026-09-19)

- 60e run `/leanmonograph`, 2 lancements (11e arrêt d'élagage au garde-fou : 8 rejets au seul seuil,
  tous réparés AVANT la prose par regrain au phénomène avec un 2e travail distinct contre-lu dans le
  PDF par la session ; 3 mono-sources laissés rejetés à dessein). Reprise `resume` : 11/11 sections
  rechargées, aucune perte.
- 11 sections, 43 claims (25 confirmés / 11 corrigés / 7 rejetés), 61 sources = 61 entrées de
  bibliographie, 6 widgets + 3 figures (9/9 du plan). ≈ 11,1 M tokens, 120 agents workflow
  + 16 agents de session, ~2 h 42 de workflow.
- `build.success:false` mérité (8e occurrence du trou d'acceptation) : claim:2 (Codex-S) confirmé sur
  une reprise Towards Data Science → ré-adjugé par 2 jurés en `corrected` (regrain PanGu-Coder-FT) ;
  claims 25/28 re-sourcés (agrégateurs de rang nul retirés).
- Backstop web (4 agents, 371 faits lus à la source) : 336 exacts / 25 imprécis / 10 FAUX, tous
  contre-lus avant édition. Faux les plus lourds : « le code s'exécute et marche » attribué à Pearce
  et al. (l'étude ne teste PAS la correction fonctionnelle — claim:33 déclassé) ; « CoC interroge
  PyPI/npm » (auto-confirmation par prompt, Li & Gao 2025) ; « 19,3 à 28,9 points » (réductions
  RELATIVES par k, 4 claims + prose + glossaire + widget) ; « 600 fois plus petit que GPT-3-175B »
  (aucun 175B dans le papier Codex) ; EvalPlus « ne touche pas aux solutions de référence » (il les
  ré-implémente) ; LiveCodeBench v1 « > 600 problèmes » (400) ; The Stack v2 « 6 To » (67,5 To bruts).
- Incohérences internes de papiers relevées : Aryabumi §3.1 (code→text « au niveau du texte seul »
  vs corps −21 % sous balanced→text ; 4,1 vs 4,2 % ; 3,6 vs 3,1 %), Codex Fig. 1 (« temperature
  0.8 » vs 37,7 % en greedy §4.5), CodeT v1/v2 (score et RANSAC absents de la v1).
- Hook impeccable : tailles < 11 px relevées sur 6 widgets, 3 interlignes, 1 libellé scindé ;
  exceptions règle par règle dans `.impeccable/config.json`. Contraste sombre mesuré : 0.
