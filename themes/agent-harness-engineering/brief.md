# Brief — agent-harness-engineering

**Sujet** : Ingénierie du harness et de la boucle agentique (harness & loop engineering).

**Prompt riche** (source : `docs/candidate-themes.md`, priorité haute, ajouté le 2026-07-09) :

> Ingénierie du harness et de la boucle agentique (harness & loop engineering) : construire le
> runtime qui transforme un modèle en agent fiable. Couvrir l'équation agent = modèle + harness et
> la répartition des responsabilités (ce que le harness retire au modèle : validation,
> autorisation, exécution, journalisation), les patterns de boucle (ReAct de base, plan-execute,
> réflexion/vérification, bounded execution, circuit breaker, conditions d'arrêt), la conception
> d'outils (granularité, schémas, messages d'erreur actionnables), l'orchestration (sous-agents,
> parallélisme, files de tâches), le contrôle d'exécution (sandboxing, permissions, déterminisme et
> rejouabilité) et la boucle de feedback (tests, linters, vérificateurs comme signal de
> correction). Positionnement : discipline émergente 2026 (harness engineering, loop engineering),
> très demandée. Public : ingénieur ML/agents. Délimitations : self-improving-harness couvre
> l'anatomie du harness et son AUTO-optimisation (citer, ne pas re-dériver) ; agentic-ai couvre
> ReAct, le tool use et MCP/A2A (les citer) ; la composition du contexte relève du candidat
> context-engineering (un pont suffit) — se centrer sur la conception délibérée du harness et de la
> boucle par l'ingénieur. Domaine : llm-agents-generation.

**Cadrage** : verdict backlog = partiel (angle neuf net) — l'ingénierie *manuelle* du harness et
de la boucle n'est posée nulle part dans le corpus ; `self-improving-harness` (anatomie,
auto-optimisation RHO/RSI) et `agentic-ai` (ReAct, tool use, MCP/A2A) sont les voisins à citer
sans re-dériver.
