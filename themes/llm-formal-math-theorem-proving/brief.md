# Mathématiques formelles par LLM — l'assistant de preuve comme oracle

Candidat du backlog (`docs/candidate-themes.md`, priorité moyenne, ajouté le 2026-09-01,
verdict « gap réel » par lecture), lancé le 2026-09-17 en 57e run `/leanmonograph`.
Domaine visé : `llm-agents-generation` (portail clos à 20 : `/arrange` tranchera l'insertion,
comme au 49e run).

⚠️ Ce fichier est une TRACE : `workflow.js` ne le lit pas. Le cadrage effectif passe
entièrement par `args.subject`.

## Gap re-vérifié avant lancement (2026-09-17)

Le verdict du backlog date du 2026-09-01 (lecture des voisins). Depuis, sept thèmes ont été
ajoutés (`git log --since=2026-09-01`), tous santé ou `ai-organizations` — aucun ne touche la
démonstration formelle. `AlphaProof`, `miniF2F`, `PutnamBench`, `DeepSeek-Prover`,
`autoformalis`, `Isabelle` : **0 occurrence** dans les `manifest.json`/`knowledge.json` publiés ;
`Mathlib` n'apparaît que dans `llm-safety-jailbreaks` (le Defense Trilemma « vérifié
mécaniquement en Lean 4 avec Mathlib » — mention incidente déjà relevée par le backlog).

## Délimitations (du backlog, à tenir dans `args.subject`)

- `reasoning-test-time-compute` garde les vérificateurs APPRIS et le best-of-N (thèse
  « verifier-based asymptotiquement supérieur » : partir de là, ne pas re-dériver).
- `agentic-rl-environments` garde le RLVR par boîte de réponse.
- `llm-evaluation` garde les juges.
- L'angle propre : **l'oracle exact et ce qu'il change à l'entraînement** — ce qu'une preuve
  vérifiée garantit et ce qu'elle ne garantit pas (l'énoncé formalisé peut être faux).

⚠️ Les pistes chiffrées du prompt du backlog (IMO 2024, taux miniF2F…) ont été écrites sans
balayage web : à corroborer en source primaire au Sweep, jamais des faits.
