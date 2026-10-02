# Brief — benchmark-contamination

Candidat du backlog (`docs/candidate-themes.md`, « Contamination des benchmarks », gap réel —
renvoi cassé A2, ajout 2026-09-01), lancé le 2026-10-02 en 66e run `/leanmonograph`.
Domaine visé : `llm-agents-generation` (`/arrange` tranchera l'insertion).

⚠️ Ce fichier est une TRACE : `workflow.js` ne le lit pas. Le cadrage effectif passe
entièrement par `args.subject`.

## Sujet (= args.subject)

La contamination des benchmarks de LLM : quand le modèle a vu le test, et de combien le score
publié s'en trouve faussé. Couvrir : les voies de contamination (pré-entraînement sur le web,
fine-tuning et données synthétiques qui paraphrasent le test, rejeu des benchmarks via les API et
les utilisateurs) ; les méthodes de détection boîte noire et grise (complétion guidée et quiz de
mémorisation — Sainz et al. 2023, Golchin & Surdeanu « Time Travel in LLMs » —, tests par
vraisemblance et permutation d'ordre, et leurs angles morts) ; la MESURE de l'inflation des scores
par paires benchmark / version rafraîchie ou perturbée (GSM8K vs GSM1k, GSM-Symbolic, MMLU vs
MMLU-Redux/variantes, découpes avant/après date de coupure) et ce que les écarts disent — ou ne
disent pas — de la contamination par rapport à la difficulté ou à la fragilité ; les réponses de
conception (benchmarks dynamiques et datés — LiveBench, LiveCodeBench —, jeux privés ou
held-out et le problème de confiance, chaînes canary et leur respect réel) ; la saturation et le
cycle de vie d'un benchmark ; Goodhart et l'incitation des classements. Public : ingénieur ML.
Angle propre : MESURER de combien, et CONCEVOIR contre.

## Délimitations (vérifiées par LECTURE de la prose le 2026-10-02)

- `pretraining-data-curation` garde la décontamination CÔTÉ CORPUS (seuils n-grammes GPT-3,
  PaLM, GPT-4, Phi-4 ; LLM decontaminator de LMSYS ; WIMBD ; Dolma), la mémorisation et
  l'extractibilité (Kandpal, Carlini). Partir de sa thèse « chevauchement détecté ≠ inflation
  réelle » pour la MESURER ; ne pas refaire les seuils. C'est le renvoi cassé que ce thème répare.
- `agent-evaluation-observability` garde SWE-bench (SWE-Bench Illusion, audit de Verified,
  SWE-Bench+, SWE-bench Pro) et présente déjà Min-K% Prob : citer comme cas d'école, ne pas
  re-chiffrer.
- `llm-evaluation` garde le juge, Chatbot Arena et The Leaderboard Illusion (paragraphe chiffré) :
  y renvoyer ; ici, l'incitation générale (Goodhart, cycle de vie), pas les chiffres d'Arena.
- `llm-code-generation` n'a LiveCodeBench qu'en trois phrases et renvoie explicitement la
  contamination à « un traitement séparé » : on peut développer LiveCodeBench comme benchmark daté.
- `llm-formal-math-theorem-proving` garde la saturation de PutnamBench : citer.
- `scaling-laws` garde l'émergence (« mirage » de Schaeffer et al.).
- Absents du corpus (vérifié) : GSM1k, GSM-Symbolic, LiveBench, Sainz et al., Golchin & Surdeanu,
  canaries, MMLU-Redux/MMLU-Pro.
