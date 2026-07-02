# Brief — knowledge-distillation

## Sujet

Distillation de connaissances : transférer la capacité d'un modèle enseignant (grand) vers un
élève (petit). Couvrir la formulation de Hinton (soft targets, température, KL sur les logits),
la distillation de features/attention (DistilBERT, TinyBERT), la distillation au niveau séquence
pour le génératif, la self-distillation et la born-again, et l'usage moderne pour fabriquer de
petits LLM (distillation de traces de raisonnement, données synthétiques).

## Positionnement

Complète le triptyque de compression avec quantization et lora.

## Public

Ingénieur ML.

## Délimitations

- `quantization` et `lora` sont des thèmes distincts du corpus : ne pas les re-traiter.
- Ne traiter que le transfert enseignant→élève.

## Domaine pressenti

`deep-learning-foundations`.
