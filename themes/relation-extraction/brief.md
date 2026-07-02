# Brief — relation-extraction

## Sujet

Extraction de relations (relation extraction) : identifier les relations typées entre
entités d'un texte.

## Cadrage

Couvrir :
- **Formulation** : classification de paires de mentions, schémas de relations,
  classe no-relation.
- **Lignée supervisée** : features et chemins de dépendance, CNN/PCNN, marqueurs
  d'entités et R-BERT, matching-the-blanks et le pré-entraînement relationnel.
- **Benchmarks et leurs pièges** : SemEval-2010 Task 8, TACRED et ses ré-annotations
  TACREV/Re-TACRED.
- **Niveau document** : DocRED, raisonnement multi-phrases, preuves/evidence.
- **Extraction jointe entités+relations** : table-filling, span pairs, TPLinker.
- **Évaluation** : micro-F1, biais des classes fréquentes.

## Public

Ingénieur NLP/IR.

## Délimitations

- `knowledge-graph-construction` couvre la supervision distante, OpenIE et REBEL —
  les citer sans re-dériver.
- `structured-extraction-llm` couvre la RE générative par LLM.
- `named-entity-recognition-sequence-labeling` fournit les mentions.
- Se centrer sur le versant discriminatif supervisé et le niveau document.

## Domaine taxonomique pressenti

information-retrieval-representation
