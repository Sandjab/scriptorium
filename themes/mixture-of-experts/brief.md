# Brief — Mixture of Experts (MoE)

Mixture of Experts (MoE) dans les réseaux de neurones : la couche sparsely-gated qui remplace
le FFN dense par N experts + un routeur appris, pour DÉCOUPLER capacité (paramètres totaux) et
calcul (FLOPs actifs par token).

## Cadrage
Document de référence best-of, en français, niveau technique. L'angle directeur est le
découplage **capacité ≠ calcul** (sparsité conditionnelle) ; tout le reste s'y rattache.
Le document s'insère dans la famille « fondations deep learning » du scriptorium, à côté de
`transformer-attention` et `quantization` — qu'il suppose connus et auxquels il renvoie plutôt
que de les ré-exposer.

## Périmètre à couvrir
- Principe : MoE sparsely-gated (Shazeer et al. 2017), conditional computation, sparsité.
- Routing / gating : top-k gating (top-1 Switch, top-2 GShard/Mixtral), softmax/noisy gating,
  token-choice vs expert-choice routing.
- Équilibrage de charge : auxiliary load-balancing loss, capacity factor, token dropping,
  collapse / sur-spécialisation des experts.
- Systèmes & passage à l'échelle : expert parallelism, communication all-to-all, empreinte
  mémoire (tous les experts résidents) vs coût de calcul réduit.
- Instances réelles à corroborer (≥2 sources indépendantes par fait) : GShard, Switch
  Transformer, GLaM, Mixtral 8x7B, DeepSeek-V2/V3 (fine-grained + shared experts), Qwen-MoE.
- Trade-offs et limites : instabilités d'entraînement, fine-tuning, coût mémoire au service.

## Frontières (ne pas ré-exposer ; renvoyer aux thèmes voisins)
- Architecture Transformer et attention → supposées connues (thème `transformer-attention`).
- Compression post-hoc (PTQ/QAT) → hors sujet, sauf mention de la quantization de MoE au
  déploiement (thème `quantization`).
- DISTINGUER explicitement MoE d'un ensemble classique (bagging/boosting) : routing conditionnel
  sparse appris de bout en bout, PAS une agrégation de tous les modèles (contraste avec le thème
  `ensemble-learning`).
