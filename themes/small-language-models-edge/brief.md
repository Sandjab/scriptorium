# Brief — Petits modèles de langage et inférence embarquée

L'angle directeur : **faire tourner un LLM sur l'appareil est un problème de système**, pas
seulement de modèle. Le document part du budget de l'appareil (mémoire, bande passante,
énergie, thermique) et montre ce qu'il impose au modèle, au runtime et à l'architecture
bord/cloud.

## Cadrage
Document de référence best-of, en français, niveau ingénieur ML / produit. Audit de couverture
par lecture (2026-10-02) : runtimes et hybride bord/cloud absents du corpus, contraintes
matérielles du bord à moitié vides ; « petit modèle utile » et quantification agressive déjà
couverts par quatre monographies — à citer, pas à refaire.

## Périmètre à couvrir
1. **Budget de l'appareil** : capacité et bande passante mémoire comme goulots réels du
   décodage sur téléphone/portable (mémoire unifiée partagée) ; NPU et ce que les TOPS
   mesurent ou non ; énergie par token ; enveloppe thermique et bridage en exécution soutenue.
2. **Ce qui rend un modèle de quelques milliards de paramètres viable sous ce budget** :
   sur-entraînement, distillation, données curées (citer) ; la MoE comme question ouverte sous
   contrainte de capacité mémoire ; capacités annoncées par les éditeurs avec leurs réserves
   de robustesse.
3. **Runtimes et formats** : llama.cpp/GGUF (k-quants), MLX, ONNX Runtime, ExecuTorch,
   exécution mobile — ce que chacun optimise.
4. **Qualité mesurée à quantification agressive (2-4 bits) spécifiquement sur petits modèles**,
   et pourquoi un modèle sur-entraîné se quantifie moins bien.
5. **Architecture hybride bord/cloud** : ce qu'on garde local, ce qu'on escalade, pourquoi
   (latence, coût, confidentialité) ; déploiements documentés (modèles on-device d'Apple +
   Private Cloud Compute, Gemini Nano).
6. **Limites**.

## Délimitations strictes
- `quantization` : méthodes de compression (GPTQ/AWQ, FP4, BitNet) — citer.
- `knowledge-distillation` : fabrication d'élèves (Gemma 2, Llama 3.2, Minitron) — citer.
- `scaling-laws` : Chinchilla, sur-entraînement inference-aware — citer.
- `pretraining-data-curation` : données curées/synthétiques (phi-1) — citer.
- `llm-inference-serving` : prefill/decode, serving datacenter — citer.
- `gpu-kernels-compilers` : roofline — citer.
- `mixture-of-experts` : mémoire résidente des experts — citer.
- `llm-classifieur-decision-typee` : cascades génériques ; `model-routing-cascades`
  (candidat) : arbitrage qualité/coût par requête.
- Toute attribution (auteurs, années, chiffres) se vérifie en source primaire au Sweep ;
  aucune n'est donnée ici comme fait.
