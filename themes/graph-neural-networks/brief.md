# Brief — graph-neural-networks

## Sujet

Graph neural networks (GNN) : apprendre sur des données structurées en graphe.

## Cadrage

Couvrir le cadre du message passing (agrégation de voisinage, mise à jour, lecture), les
architectures de référence (GCN spectral/spatial, GraphSAGE et l'échantillonnage de voisinage,
GAT et l'attention sur arêtes, GIN et le pouvoir expressif lié au test de Weisfeiler-Lehman),
le pooling de graphes, les tâches (classification de nœuds/graphes, prédiction de liens), et
les pièges (oversmoothing, oversquashing, passage à l'échelle).

- **Positionnement** : famille d'architectures absente d'un corpus 100 % séquence/transformer.
- **Public** : ingénieur ML.
- **Délimitations** : ⚠️ `knowledge-graph-construction` traite l'EXTRACTION de graphes depuis
  le texte ; GraphRAG (`retrieval-augmented-generation`) et les knowledge graphs
  (`agentic-memory`) utilisent des graphes sans message passing — se centrer sur
  l'apprentissage de représentations sur graphes.
- **Domaine** : deep-learning-foundations.

## Provenance

Candidat du backlog (`docs/candidate-themes.md`, priorité moyenne, verdict « gap réel »),
lancé le 2026-07-24 via /leanmonograph (18e run).
