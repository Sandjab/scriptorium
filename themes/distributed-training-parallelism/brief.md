# Brief — Entraînement distribué & parallélisme

**Slug** : `distributed-training-parallelism` · **Domaine cible** : deep-learning-foundations

## Sujet

Entraînement distribué des réseaux profonds : faire tenir et accélérer l'entraînement sur une
grappe de GPU.

## Cadrage

Couvrir :
- **Data parallelism** : all-reduce, gradient accumulation, ZeRO-1/2/3 et FSDP
  (partitionnement des états d'optimiseur, gradients et paramètres).
- **Tensor parallelism** : Megatron-LM, découpe des matmuls et communications associées.
- **Pipeline parallelism** : micro-batches, bulles, schedules 1F1B.
- **Sequence/context parallelism**.
- **Précision mixte** (FP16/BF16, loss scaling) et **activation checkpointing**.
- **Mesure d'efficacité** : MFU, scaling faible vs fort, choix d'une topologie 3D.

**Public** : ingénieur ML/infra.

## Délimitations (thèmes existants à citer, pas à refaire)

- `mixture-of-experts` couvre l'expert parallelism (le citer).
- `scaling-laws` couvre l'allocation compute-optimale du budget.
- `quantization` couvre les formats numériques à l'inférence.
- `lora` couvre la mémoire du fine-tuning.

Se centrer sur **les stratégies de partitionnement et la mémoire d'entraînement**.
