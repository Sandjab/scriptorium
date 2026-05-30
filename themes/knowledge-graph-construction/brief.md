# brief — knowledge-graph-construction

## Sujet (tel que fourni)

> J'ai un corpus de textes. Je voudrais en extraire des FAITS et des RELATIONS
> TYPÉES entre ces faits et stocker tout cela de manière persistante et navigable.
> Quelle est l'état de l'art sur le sujet ?

## Cadrage

État de l'art de la **construction de graphes de connaissances à partir de texte**
(text-to-knowledge-graph) — le pipeline complet qui répond à la demande :

1. **Extraction de faits** : reconnaissance d'entités (NER), liage d'entités
   (entity linking), résolution de coréférence.
2. **Relations typées** : extraction de relations supervisée / distante, OpenIE,
   approches récentes à base de LLM (extraction de triplets, schémas/ontologies).
3. **Stockage persistant & navigable** : modèles RDF vs property graph, triple
   stores, bases de graphes (Neo4j…), interrogation (SPARQL / Cypher), GraphRAG.

Angle « état de l'art » : situer les familles d'approches, leurs compromis, et
ce qui est établi vs contesté en 2024-2025.
