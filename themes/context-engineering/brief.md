# Brief — context-engineering

## Sujet

Context engineering : composer délibérément tout ce que le modèle voit à chaque appel.

## Cadrage

Couvrir :
- la fenêtre de contexte comme ressource rare (budget d'attention, context rot — dégradation
  mesurable quand le contexte s'allonge) ;
- les composants du contexte (system prompt, définitions d'outils, exemples, historique, données
  récupérées, mémoire) ;
- les stratégies de gestion (compaction/résumé, prise de notes structurée, chargement
  juste-à-temps vs pré-chargement, masquage et chargement dynamique d'outils) ;
- l'architecture des contextes multi-agents (isolation par sous-agent, transfert de contexte) ;
- l'évaluation (needle-in-a-haystack et ses limites, benchmarks long contexte).

Positionnement : successeur revendiqué du prompt engineering, discipline centrale 2026.

Public : ingénieur ML/agents.

## Délimitations

- `agentic-memory` couvre la mémoire persistante inter-sessions (la citer) ;
- `prompt-optimization` couvre l'optimisation AUTOMATIQUE des prompts ;
- `recursive-language-models` couvre le context rot et la compaction côté RLM (les citer sans
  re-dériver) ;
- `retrieval-augmented-generation` couvre la récupération ;
- se centrer sur la composition et l'économie du contexte à l'inférence.

Domaine cible : `llm-agents-generation`.
