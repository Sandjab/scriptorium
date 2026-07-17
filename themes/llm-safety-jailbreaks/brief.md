# Brief — llm-safety-jailbreaks

## Sujet
Sécurité des LLM : jailbreaks, prompt injection et garde-fous — taxonomie des attaques et des
défenses **au niveau du modèle**.

## Cadrage
- **Public** : ingénieur ML / sécurité.
- **Angle** : taxonomie attaques/défenses au niveau du MODÈLE (pas l'infrastructure agentique ni le RAG).
- **Couvrir** :
  - Attaques : jailbreaks (par rôle/persona, encodage, optimisation type GCG), prompt injection
    directe et indirecte, extraction de prompt système et de données d'entraînement, attaques multi-tours.
  - Red-teaming : manuel et automatisé.
  - Défenses : alignement par refus, classificateurs d'entrée/sortie, guardrails, durcissement du
    system prompt, détection de PII — avec leurs limites (course à l'armement, transférabilité).

## Délimitations (thèmes voisins déjà couverts — citer, ne pas re-dériver)
- `agentic-ai` : surface agentique (MCP, tool poisoning).
- `agentic-memory` : MINJA.
- `retrieval-augmented-generation` : PoisonedRAG / BadRAG.

## Domaine
`llm-agents-generation`.
