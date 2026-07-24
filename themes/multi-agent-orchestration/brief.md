# Brief — Orchestration multi-agents

**Sujet** : Systèmes multi-agents LLM et leur orchestration : concevoir la topologie qui relie
plusieurs agents.

**Cadrage** : Couvrir les topologies (supervisor, hiérarchique, réseau/swarm, blackboard,
pipeline), les graphes d'état et le checkpointing (LangGraph), les frameworks fondateurs
(AutoGen et la conversation programmable, MetaGPT et les SOP, CAMEL et le role-playing, CrewAI),
la communication inter-agents (mémoire partagée vs passage de messages), les modes d'échec
(taxonomie MAST « Why Do Multi-Agent LLM Systems Fail? », Berkeley 2025 : spécification,
désalignement inter-agents, vérification), le débat mono vs multi-agent (Cognition « Don't Build
Multi-Agents » vs le système de recherche multi-agents d'Anthropic) et l'économie (coût
multiplié, quand la parallélisation paie). Encadré terminologique : « graph engineering »
(juillet 2026) comme étiquette récente de la pratique.

**Public** : ingénieur LLM.

**Délimitations** :
- ⚠️ `agentic-ai` couvre ReAct/tool use, MCP/A2A et les paradigmes — ne pas re-dériver.
- `agent-harness-engineering` couvre le harness mono-agent et pose déjà orchestrator-workers —
  partir de là, se centrer sur les topologies, frameworks et modes d'échec.
- `agent-evaluation-observability` couvre l'évaluation et le tracing des agents.

**Domaine pressenti** : llm-agents-generation.

**Origine** : candidat backlog ajouté le 2026-07-23 (veille « graph engineering »,
`docs/candidate-themes.md`).
