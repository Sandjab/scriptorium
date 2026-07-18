# Brief — llm-inference-serving

## Sujet
Serving d'inférence LLM : servir des milliers de requêtes concurrentes sur un parc de GPU —
ordonnancement, mémoire et SLO du système de serving.

## Cadrage
- **Public** : ingénieur ML / infra.
- **Angle** : le SYSTÈME de serving (ordonnancement, gestion mémoire, SLO), pas l'algorithme d'attention
  ni la compression.
- **Couvrir** :
  - Les deux phases **prefill / decode** et leurs régimes (compute-bound vs memory-bound).
  - **Continuous batching** (Orca).
  - **PagedAttention** et la gestion du KV cache comme mémoire paginée (vLLM).
  - **Prefix / radix caching** (SGLang).
  - **Chunked prefill** et **désagrégation prefill/decode**.
  - Métriques de service : **TTFT, TPOT, goodput, SLO**.
  - **Routage / autoscaling** multi-modèles.

## Délimitations (thèmes voisins — citer, ne pas re-dériver)
- `transformer-attention` : FlashAttention et MQA/GQA/MLA.
- `decoding-sampling` : speculative decoding et échantillonnage.
- `quantization` : compression des poids/activations.

## Domaine
`llm-agents-generation`.
