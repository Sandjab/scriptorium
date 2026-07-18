# Brief — Évaluation & observabilité des agents

## Sujet

Évaluation et observabilité des agents LLM : mesurer et déboguer des systèmes multi-tours non
déterministes. Couvrir les benchmarks agentiques (SWE-bench et sa vérification, τ-bench et la
fiabilité pass^k, GAIA, WebArena/OSWorld) et leurs pièges (contamination, écarts de harness entre
laboratoires), l'évaluation de trajectoires (succès final vs qualité des étapes, juges de
trajectoire, simulation d'utilisateur), l'observabilité en production (traces structurées, spans,
coût/latence par étape, clustering d'échecs) et la boucle trace → dataset → éval (AgentOps).

## Public

Ingénieur ML/agents.

## Délimitations

- `llm-evaluation` couvre l'évaluation des MODÈLES, les juges LLM et l'accord juge/humain :
  la citer, ne pas re-dériver le juge LLM.
- `agentic-ai` cite SWE-bench/GAIA comme état de l'art mesuré : le citer.
- Se centrer sur l'évaluation des SYSTÈMES agents et leur observabilité.

## Domaine cible (taxonomie)

llm-agents-generation
