# Brief — sparse-attention-long-context

Attention parcimonieuse (sparse attention) et efficacité du long contexte : réduire le CALCUL de
l'attention, pas seulement ses accès mémoire. Couvrir les motifs statiques fondateurs (attention
locale à fenêtre glissante, tokens globaux, motifs aléatoires : Longformer, BigBird, et la
longueur de chemin qu'ils préservent là où l'attention purement locale la dégrade), le streaming
par tokens-puits (StreamingLLM et la mécanique de l'attention sink qui l'explique), la parcimonie
DYNAMIQUE à l'inférence (sélection et éviction de tokens du KV cache, budget par tête, prefill
parcimonieux), la parcimonie NATIVE entraînée de bout en bout (NSA de DeepSeek, MoBA, InfLLM-v2 —
et pourquoi entraîner la parcimonie plutôt que l'appliquer après coup change l'alignement
entraînement/inférence), les hybrides parcimonieux + linéaires de 2026 et leurs ratios de couches,
et l'arbitrage mesuré : ce que la parcimonie coûte en rappel exact, en récupération et en
raisonnement, et ce que « plus rapide » veut dire selon qu'on compte les FLOPs, les accès mémoire
ou le débit réel sur une puce donnée.

Positionnement : la direction dominante de l'architecture 2026 (l'efficacité du long contexte
comme condition des harnesses d'agents), et un gap net du corpus — personne n'y traite la
parcimonie comme design d'architecture. Public : ingénieur ML.

## Délimitations (re-vérifiées par LECTURE de la prose des voisins le 2026-08-06)

- **`transformer-attention` est le point de départ, pas le terrain.** Il pose le mur quadratique
  (O(n²·d) vs O(n·d²), longueur de chemin O(1)), traite l'attention EXACTE (FlashAttention 1/2/3,
  tiling, softmax en ligne, MQA/GQA/MLA) et **exclut nommément le sujet de son périmètre** : « Le
  ranger [FlashAttention] parmi les attentions linéaires ou parcimonieuses (qui, elles, modifient
  le calcul) confond une optimisation IO-aware avec une approximation algorithmique. » REPRENDRE
  cette distinction exact/approché comme charnière d'ouverture, NE PAS re-dériver FlashAttention
  ni les variantes de KV head.
- **L'attention sink est déjà là, mais sous un autre angle.** `transformer-attention` l'explique
  comme preuve que les poids d'attention ne sont pas une explication (le softmax somme à 1 sans
  option d'abstention, le budget reflue sur les premiers tokens) et cite StreamingLLM (Xiao et al.,
  ICLR 2024) et Gu et al. (ICLR 2025) en bibliographie, sans les traiter. L'angle propre ici : le
  sink comme CONTRAINTE DE DESIGN d'un motif parcimonieux de streaming.
- **`state-space-models` tient la voie récurrente/linéaire.** Il couvre l'attention linéaire par la
  dualité SSD de Mamba-2, le goulot du rappel associatif multi-requêtes, et les hybrides
  attention+SSM en profondeur (MambaFormer, Samba, Jamba et son ratio 1:7 attention/Mamba). Ici :
  la parcimonie, pas la récurrence. Les hybrides parcimonieux+linéaires de 2026 se présentent en
  se délimitant explicitement de ces hybrides-là.
- **`context-engineering` tient l'usage.** Il cite BigBird et Longformer en deux phrases (au titre
  du compromis coût/longueur de chemin de Vaswani et al.), et traite le context rot, « Lost in the
  Middle » et le softmax crowding. Les citer comme motivation empirique ; ne pas refaire le context
  rot.
- **`llm-inference-serving` tient le serving.** Prefill/decode, continuous batching, chunked
  prefill, prefix et radix caching (réutiliser le KV d'un préfixe PARTAGÉ), SLO. ⚠️ Ne pas
  confondre : réutiliser un préfixe partagé entre requêtes ≠ sélectionner ou évincer des tokens
  DANS l'attention d'une même séquence. Citer la frontière explicitement.
- `recursive-language-models` contourne la fenêtre par la récursion et un REPL (le long contexte
  comme environnement externe) — approche concurrente à citer, pas à traiter.
- L'extension de contexte par l'encodage positionnel (Position Interpolation, YaRN, NTK) relève du
  candidat `rotary-position-embedding`, NON FAIT : ne pas l'annexer.

## Homonymies à écarter explicitement (« sparse » veut dire cinq choses dans ce corpus)

1. **MoE sparsely-gated** — `mixture-of-experts` en fait son titre : la parcimonie y est celle des
   EXPERTS activés par token (k parmi N), pas celle du motif d'attention. C'est l'homonymie la plus
   dangereuse du thème : à écarter dès la première section.
2. **Sparse autoencoders** — `mechanistic-interpretability` : parcimonie des FEATURES apprises pour
   la monosémanticité.
3. **Learned sparse retrieval** — SPLADE dans `hybrid-search-reranking` et
   `retrieval-augmented-generation` : vecteurs creux sur le vocabulaire, régulariseur FLOPS.
4. **Pruning / élagage de POIDS** — `quantization`, `knowledge-distillation`, `lora` : supprimer des
   paramètres, pas des liens d'attention.
5. **Élagage de listes inversées** — `bm25-inverted-index` (WAND, Block-Max) : sauter des documents
   au parcours d'un index.

## Risque connu du sujet (à surveiller au council)

Le cœur de l'actualité (NSA, MoBA, InfLLM-v2, hybrides 2026) est une littérature **très jeune**,
souvent portée par un seul rapport technique de laboratoire. Le seuil « ≥ 2 sources indépendantes »
produira mécaniquement des rejets single-source, comme sur `agent-harness-engineering` (2 sections
écartées). Traiter les motifs fondateurs (Longformer, BigBird, StreamingLLM) et l'analyse des
compromis comme le socle corroborable, et les systèmes de 2026 comme illustration attribuée.
