# Brief — multimodal-vlm

**Sujet** : Vision-Language Models (VLM) et fusion multimodale : aligner image et texte dans un
même modèle.

**Cadrage** : couvrir l'alignement contrastif (CLIP en rappel), les architectures de fusion
(encodeur visuel + LLM via projection/Q-Former — BLIP-2 ; cross-attention — Flamingo ; tokens
visuels en entrée — LLaVA), l'instruction-tuning multimodal, le traitement de la résolution/des
patchs, et les benchmarks (VQA, captioning, hallucination visuelle).

**Positionnement** : pertinence croissante, absent du corpus en tant que thème cohérent.

**Public** : ingénieur ML.

**Délimitations** :
- `transformer-attention` couvre le ViT — ne pas re-dériver.
- `diffusion-models` couvre le conditionnement (génération d'images).
- `agentic-ai` couvre l'agent incarné (PaLM-E).
- `contrastive-self-supervised` approfondit le contrastif/CLIP — le citer.
- Se centrer sur l'architecture VLM et l'alignement vision→langage pour la **compréhension**.

**Domaine** : llm-agents-generation.
