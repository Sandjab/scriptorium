# Backlog des thèmes candidats

Sujets candidats pour de futures monographies du scriptorium, issus d'une **analyse de couverture
en profondeur** : un agent-lecteur par monographie a **lu le texte rédigé** (`manifest.json` =
prose + `knowledge.json` = faits) des 32 monographies et produit un inventaire détaillé des sujets
traités ; un agent de synthèse en a dérivé la carte de couverture, un verdict par candidat et les
gaps réels. (Cette passe corrige une analyse antérieure faussée par un `grep -E 'a\|b\|c'` —
en ERE, `\|` est un pipe *littéral* ; ne jamais l'utiliser.)

- **Fabrication** : `/frugalmonograph « <prompt riche> »` puis `/arrange <slug>`.
- **Domaine** = celui de `tools/taxonomy.json` (source de vérité). Un thème = un seul domaine.
- **Verdicts** : `gap réel` (rien de substantiel) · `partiel` (effleuré/adjacent ailleurs, angle
  neuf à cibler) · `écarté` (déjà couvert en profondeur).

---

## Priorité haute — gaps réels, forte valeur de référence

### Raisonnement à l'inférence & test-time compute — `reasoning-test-time-compute` → `llm-agents-generation`
**Verdict : gap réel.** `rlhf-dpo` traite le RL d'*entraînement* (GRPO, RLVR, DeepSeek-R1) ;
`agentic-ai` n'a qu'une mention « CoT vs ToT ». Le versant *inférence* est absent.

> Raisonnement à l'inférence et test-time compute : améliorer la qualité d'un LLM en dépensant
> plus de calcul au moment de répondre, plutôt qu'en grossissant le modèle. Couvrir le
> chain-of-thought (CoT) comme méthode et ses variantes structurées (self-consistency,
> tree-of-thought, graph-of-thought), l'échantillonnage best-of-N et les vérificateurs / Process
> Reward Models (PRM), les lois d'échelle du test-time compute (qualité vs budget d'inférence), et
> le décodage des modèles de raisonnement (o1/o3, traces longues). Positionnement : le versant
> INFÉRENCE du raisonnement. Public : ingénieur ML. Délimitations strictes : NE PAS re-traiter le
> RL-pour-raisonnement (déjà dans rlhf-dpo, section « GRPO et le RL pour le raisonnement ») ni la
> récursion long-horizon (recursive-language-models). Domaine : llm-agents-generation.

### Décodage & sampling — `decoding-sampling` → `llm-agents-generation`
**Verdict : gap réel.** `transformer-attention` couvre la mécanique du KV cache (PagedAttention,
GQA, MLA) mais **pas** les stratégies de décodage ; `diffusion-models` traite l'échantillonnage de
diffusion (hors-sujet).

> Décodage et sampling pour la génération de texte par LLM autoregressifs : comment, à
> l'inférence, on transforme les logits en tokens. Couvrir les stratégies déterministes (greedy,
> beam search) et stochastiques (température, top-k, top-p/nucleus, min-p, typical sampling), les
> pénalités de répétition et le contrastive search/decoding ; le rôle du KV cache (et son coût
> mémoire O(L·D)) ; et le décodage spéculatif (draft model + vérification, Medusa, EAGLE,
> lookahead) comme principal levier de latence. Positionnement : l'étape de génération elle-même.
> Public : ingénieur ML. Délimitations : la mécanique du KV cache et l'attention efficace sont déjà
> dans transformer-attention (rappeler sans re-dériver) ; le décodage contraint est dans
> structured-extraction-llm ; l'inférence récurrente des SSM dans state-space-models (contraste).
> Domaine : llm-agents-generation.

### Scaling laws (Chinchilla, compute-optimal) — `scaling-laws` → `deep-learning-foundations`
**Verdict : gap réel.** Seule mention : `ia-productivite-esn` cite Kaplan/Chinchilla dans un cadre
de plafonds de productivité, pas la frontière compute-optimale.

> Lois d'échelle (scaling laws) du deep learning : comment la perte décroît avec les paramètres,
> les données et le compute, et comment allouer un budget de calcul de façon compute-optimale.
> Couvrir les lois en loi de puissance (Kaplan et al. 2020), la révision Chinchilla (Hoffmann et
> al. 2022 : ~20 tokens/paramètre), le compromis taille-modèle vs données à budget FLOPs fixe, les
> lois aval (transfert, inférence) et leurs limites (qualité des données, plafonds, émergence
> contestée). Public : ingénieur ML / décideur technique. Délimitations : ne pas re-dériver
> l'architecture transformer ni l'optimisation ; rester sur la relation empirique perte↔(N, D, C).
> Domaine : deep-learning-foundations.

### Knowledge distillation — `knowledge-distillation` → `deep-learning-foundations`
**Verdict : gap réel.** Dispersée comme sous-élément (distillation Switch sparse→dense, consistency
distillation en diffusion, R1→petits modèles…) mais **jamais traitée en propre**.

> Distillation de connaissances : transférer la capacité d'un modèle enseignant (grand) vers un
> élève (petit). Couvrir la formulation de Hinton (soft targets, température, KL sur les logits),
> la distillation de features/attention (DistilBERT, TinyBERT), la distillation au niveau séquence
> pour le génératif, la self-distillation et la born-again, et l'usage moderne pour fabriquer de
> petits LLM (distillation de traces de raisonnement, données synthétiques). Positionnement :
> complète le triptyque de compression avec quantization et lora. Public : ingénieur ML.
> Délimitations : quantization et lora sont des thèmes distincts ; ne traiter que le transfert
> enseignant→élève. Domaine : deep-learning-foundations.

### Réseaux convolutifs : de LeNet à ConvNeXt — `convolutional-networks` → `deep-learning-foundations`
**Verdict : nouveau gap (haute).** Pilier toujours dominant en vision ; aucun thème dédié.

> Réseaux de neurones convolutifs (CNN), de LeNet à ConvNeXt : l'architecture qui domine encore la
> vision. Couvrir la mécanique convolutive (convolution discrète, partage de poids, champ
> réceptif, stride, padding, dilatation), le pooling et l'invariance par translation, la généalogie
> des architectures (LeNet → AlexNet → VGG → Inception → ResNet/connexions résiduelles → DenseNet →
> EfficientNet/compound scaling → ConvNeXt), les convolutions séparables en profondeur (MobileNet)
> et la comparaison avec les Vision Transformers. Public : ingénieur ML. Délimitations :
> backpropagation effleure LeNet (partage de poids), normalization-layers cite ResNet/ConvNeXt
> comme cas d'usage de BN/LN, transformer-attention couvre les ViT — se centrer sur la mécanique
> convolutive et l'évolution des architectures. Domaine : deep-learning-foundations.

### Apprentissage contrastif & auto-supervisé — `contrastive-self-supervised` → `deep-learning-foundations`
**Verdict : nouveau gap (haute).** Socle du pré-entraînement sans labels ; seulement cité en
passant (InfoNCE/CLIP dans text-embeddings, CLIP comme conditionneur en diffusion).

> Apprentissage contrastif et auto-supervisé : apprendre des représentations sans labels. Couvrir
> le cadre contrastif (InfoNCE, paires positives/négatives, augmentations, température), les
> méthodes phares (SimCLR, MoCo et sa file de négatifs, BYOL et SwAV sans négatifs, Barlow Twins,
> DINO/auto-distillation), le problème du collapse et comment l'éviter, et l'alignement multimodal
> texte-image (CLIP). Positionnement : socle des modèles de fondation. Public : ingénieur ML.
> Délimitations : text-embeddings ne cite InfoNCE/CLIP qu'en passant ; se centrer sur l'objectif
> contrastif et le self-supervised visuel/multimodal. Domaine : deep-learning-foundations.

### Learning to rank — `learning-to-rank` → `information-retrieval-representation`
**Verdict : nouveau gap (haute).** Cœur algorithmique de l'IR, seulement cité comme baseline.

> Learning to rank (LTR) : apprendre à ordonner pour la recherche et la recommandation. Couvrir les
> trois familles de pertes (pointwise ; pairwise — RankNet ; listwise — ListNet,
> LambdaRank/LambdaMART), l'optimisation directe des métriques de rang (NDCG, MAP, MRR) malgré leur
> non-différentiabilité (le gradient λ de LambdaRank), les features de ranking, les jeux
> LETOR/MSLR, et l'usage en reranking. Public : ingénieur ML/IR. Délimitations :
> hybrid-search-reranking compare RRF aux LTR et traite les cross-encoders neuronaux ;
> ensemble-learning couvre les arbres boostés (socle de LambdaMART) — se centrer sur les algorithmes
> LTR et les métriques de rang. Domaine : information-retrieval-representation.

---

## Priorité moyenne

Candidats à angle neuf (les prompts riches des deux premiers existent ; les autres se rédigeront à
la demande).

### Optimiseurs (Adam / AdamW) — `optimizers-adam` → `deep-learning-foundations`
**Verdict : partiel (~60 % neuf).** `backpropagation` traite Adam de base (Kingma & Ba) comme étape
post-gradient ; AdamW (weight decay découplé), schedules warmup/cosine, AdaGrad/RMSProp en propre et
Lion/Adafactor/Sophia/Muon sont absents.

> Optimiseurs adaptatifs pour l'entraînement de réseaux profonds, centrés sur Adam et AdamW : que
> faire du gradient une fois calculé. Couvrir SGD + momentum, la lignée AdaGrad → RMSProp → Adam
> (moments d'ordre 1 et 2, correction de biais), AdamW (weight decay découplé vs L2), les schedules
> de learning rate (warmup, cosine) et les variantes modernes (Lion, Adafactor, Sophia, Muon).
> Délimitations : backpropagation couvre le calcul du gradient (ne pas le re-dériver) et l'esquisse
> d'Adam — l'angle neuf est le paysage des optimiseurs et AdamW. Domaine : deep-learning-foundations.

### RoPE / encodage positionnel — `rotary-position-embedding` → `deep-learning-foundations`
**Verdict : partiel.** `transformer-attention` a une section « encodage positionnel sinusoïdal »
(absolu) ; RoPE, l'encodage relatif, l'extension de contexte (PI/NTK/YaRN) et ALiBi sont absents.

> Le Rotary Position Embedding (RoPE) et l'encodage positionnel dans les transformers. Couvrir le
> besoin d'information positionnelle (absolu sinusoïdal vs appris vs relatif), le mécanisme RoPE
> (rotation par sous-espaces 2D, position relative émergeant du produit scalaire), ses propriétés
> (décroissance longue portée, extrapolation) et l'extension de contexte (Position Interpolation,
> NTK-aware, YaRN, dynamic NTK) ; ALiBi en comparaison. Délimitations : transformer-attention couvre
> l'attention et le PE absolu sinusoïdal — partir de là, se centrer sur RoPE/relatif/extension de
> contexte. Domaine : deep-learning-foundations.

### Autres candidats — priorité moyenne (prompts riches à la demande)

| Sujet | slug | Domaine | Verdict / angle | Délimitation principale |
|---|---|---|---|---|
| Autoencodeurs & VAE | `variational-autoencoders` | deep-learning-foundations | nouveau gap | diffusion-models s'appuie sur un autoencodeur sans traiter le VAE en propre ; cadre génératif probabiliste + inférence variationnelle (ELBO, reparam, β-VAE, VQ-VAE) |
| Systèmes de recommandation | `recommender-systems` | information-retrieval-representation | nouveau gap | ANN/embeddings n'effleurent que l'indexation ; factorisation matricielle/ALS, BPR, two-tower, éval top-N |
| GAN | `generative-adversarial-networks` | deep-learning-foundations | nouveau gap | seul thème génératif = diffusion-models ; jeu min-max, mode collapse, WGAN, StyleGAN |
| Régression régularisée & GLM | `regression-reguliere` | classical-ml-time-series | nouveau gap | lasso/elastic net éparpillés (Sparse PCA) ; régression linéaire/logistique, ridge/lasso/elastic net, GLM |
| Sécurité LLM & jailbreaks | `llm-safety-jailbreaks` | llm-agents-generation | nouveau gap | attaques ponctuelles dispersées (MCP, MINJA, PoisonedRAG) ; taxonomie attaques/défenses au niveau modèle |
| Vision-Language Models (VLM) | `multimodal-vlm` | llm-agents-generation | nouveau gap | ViT (transformer-attention), conditionnement (diffusion) ; architecture VLM, alignement vision-langage, VQA |
| SVM / méthodes à noyau | `svm-kernel-methods` | classical-ml-time-series | gap réel | kernel trick effleuré (Kernel PCA, noyaux GP) ; marge maximale, hinge loss, dualité, SMO |
| Graph neural networks | `graph-neural-networks` | deep-learning-foundations | gap réel | ⚠️ knowledge-graph-construction = *extraction* de graphes (≠ apprendre dessus) ; GCN/GraphSAGE/GAT/message passing |
| Sketches en flux : quantiles & sampling | `streaming-quantiles-sampling` | probabilistic-structures-hashing | gap réel | complète count-min-sketch/hyperloglog ; t-digest/KLL/Greenwald-Khanna + reservoir sampling (Algorithm R, A-Res) fusionnés |

---

## Priorité basse / marginale

| Sujet | slug | Domaine | Verdict | Note |
|---|---|---|---|---|
| MinHash & déduplication | `minhash-dedup` | probabilistic-structures-hashing | partiel | ⚠️ LSH a déjà une section dédiée dans `approximate-nearest-neighbor` ; recibler sur MinHash/Jaccard, min-wise independence, amplification par bandes pour similarity-join et **dédup de corpus**, SimHash |
| Cuckoo filter | `cuckoo-filter` | probabilistic-structures-hashing | partiel (marginal) | déjà traité en plusieurs claims dans `bloom-filters` (Fan et al. 2014, seuils Bloom/cuckoo/xor) ; ne reste que partial-key cuckoo hashing, semi-sorting, vs quotient/xor filter |
| Gaussian processes (général) | `gaussian-processes` | classical-ml-time-series | partiel | `time-series-forecasting` a une section GP orientée prévision ; angle neuf = régression/classification bayésienne + optimisation bayésienne |
| Calibration des classifieurs | `calibration-classifieurs` | classical-ml-time-series | nouveau gap | Platt/isotonic/temperature scaling, reliability diagrams, ECE/MCE, conformal prediction comme pont |

---

## Écartés — déjà couverts en profondeur (vérifié dans le texte)

- **Tokenization (BPE / SentencePiece / byte-level)** → `text-embeddings` (sections dédiées BPE,
  byte-level GPT-2, WordPiece/Unigram/SentencePiece, APX-complétude, glitch tokens).
- **Gradient boosting (XGBoost / LightGBM / CatBoost)** → `ensemble-learning` (sections Friedman 2001
  + XGBoost Newton boosting + LightGBM/CatBoost/HistGradientBoosting) ; appliqué dans `time-series-forecasting`.
- **SPLADE / learned sparse retrieval** → `hybrid-search-reranking` (section dédiée v1/v2/v3,
  régulariseur FLOPS) ; aussi dans `retrieval-augmented-generation` et `bm25-inverted-index`.
- **ColBERT / late interaction** → `hybrid-search-reranking` (« Late interaction — ColBERT v2 et
  MaxSim ») et `retrieval-augmented-generation` (compression résiduelle PLAID).
