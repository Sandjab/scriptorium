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

### Autoencodeurs & VAE — `variational-autoencoders` → `deep-learning-foundations`
**Verdict : nouveau gap.** `diffusion-models` s'appuie sur un autoencodeur (latent diffusion) sans
traiter le VAE en propre ; `clustering-dimensionality-reduction` couvre la réduction linéaire (PCA).

> Autoencodeurs et VAE : apprendre des représentations latentes et générer par inférence
> variationnelle. Couvrir l'autoencodeur (encodeur/décodeur, goulot, reconstruction), le débruitage
> (denoising autoencoder), puis le Variational Autoencoder (Kingma & Welling 2013 : borne ELBO,
> reconstruction + KL au prior, reparameterization trick), les variantes (β-VAE et le
> désenchevêtrement, VQ-VAE et le codebook discret), et le lien avec les modèles latents génératifs.
> Positionnement : brique fondamentale qui sous-tend la diffusion latente. Public : ingénieur ML.
> Délimitations : diffusion-models s'appuie sur un autoencodeur (régularisation KL/VQ) sans traiter
> le VAE en tant que tel (ne le citer que comme usage aval) ; clustering-dimensionality-reduction
> couvre PCA/UMAP — se centrer sur le cadre génératif probabiliste et l'inférence variationnelle.
> Domaine : deep-learning-foundations.

### Systèmes de recommandation — `recommender-systems` → `information-retrieval-representation`
**Verdict : nouveau gap.** `approximate-nearest-neighbor`/`text-embeddings` n'effleurent que
l'indexation/similarité.

> Systèmes de recommandation et filtrage collaboratif : prédire les préférences à grande échelle.
> Couvrir le filtrage collaboratif (voisinage user/item), la factorisation matricielle (SVD-like,
> ALS, termes de biais), le feedback implicite et le ranking par paires (BPR), l'architecture
> two-tower (retrieval + ranking) des systèmes industriels, le démarrage à froid et l'évaluation
> top-N (Recall@K, NDCG, hit rate, pièges de l'évaluation hors-ligne). Positionnement : grand
> domaine applicatif absent. Public : ingénieur ML. Délimitations : ANN et text-embeddings
> n'effleurent que l'indexation/similarité (Annoy/Voyager, arbitraire du cosinus de Steck et al.) —
> se centrer sur les modèles de préférence et l'évaluation ; learning-to-rank (candidat distinct)
> traite l'ordonnancement supervisé générique. Domaine : information-retrieval-representation.

### Réseaux antagonistes génératifs (GAN) — `generative-adversarial-networks` → `deep-learning-foundations`
**Verdict : nouveau gap.** `diffusion-models` est le seul thème génératif.

> Réseaux antagonistes génératifs (GAN) : générer par un jeu à deux joueurs. Couvrir la formulation
> min-max (générateur vs discriminateur, l'objectif de Goodfellow 2014 et son interprétation en
> divergence de Jensen-Shannon), les pathologies d'entraînement (instabilité, mode collapse,
> vanishing gradients) et leurs remèdes (Wasserstein GAN, gradient penalty WGAN-GP, spectral
> normalization), les architectures marquantes (DCGAN, conditional GAN, StyleGAN, CycleGAN), et
> l'évaluation (FID, Inception Score). Positionnement : paradigme génératif historique majeur,
> contrepoint de la diffusion. Public : ingénieur ML. Délimitations : diffusion-models couvre le
> génératif par score/diffusion (FID/IS) — se centrer sur l'entraînement adversarial et ses
> pathologies. Domaine : deep-learning-foundations.

### Régression régularisée & GLM — `regression-reguliere` → `classical-ml-time-series`
**Verdict : nouveau gap.** Éparpillé (lasso/elastic net dans Sparse PCA, biais-variance dans
ensemble-learning, régression logistique/BIM dans bm25).

> Régression régularisée et modèles linéaires généralisés (GLM) : la brique de base du ML
> supervisé. Couvrir la régression linéaire (moindres carrés, hypothèses) et logistique, la
> régularisation (ridge/L2, lasso/L1 et la parcimonie, elastic net), le compromis biais-variance et
> la sélection de variables, le cadre GLM (familles exponentielles, fonction de lien, déviance), et
> l'optimisation (équations normales, descente de coordonnées, IRLS). Positionnement : socle du ML
> classique, actuellement éparpillé. Public : ingénieur ML/data. Délimitations :
> clustering-dimensionality-reduction utilise lasso/elastic net (Sparse PCA) et ensemble-learning le
> biais-variance (les citer sans re-dériver) ; bm25-inverted-index mentionne la régression
> logistique (BIM) en contexte IR — se centrer sur la régression supervisée et la régularisation en
> propre. Domaine : classical-ml-time-series.

### Sécurité LLM & jailbreaks — `llm-safety-jailbreaks` → `llm-agents-generation`
**Verdict : nouveau gap.** Attaques ponctuelles dispersées (MCP/tool poisoning, MINJA,
PoisonedRAG/BadRAG, refus).

> Sécurité des LLM : jailbreaks, prompt injection et garde-fous. Couvrir la taxonomie des attaques
> au niveau du modèle (jailbreaks par rôle/encodage/optimisation type GCG, prompt injection directe
> et indirecte, extraction de prompt système et de données d'entraînement, attaques multi-tours), le
> red-teaming (manuel et automatisé), et les défenses (alignement par refus, classificateurs
> d'entrée/sortie, guardrails, durcissement du system prompt, détection de PII) avec leurs limites
> (course à l'armement, transférabilité). Positionnement : très demandé, aujourd'hui dispersé.
> Public : ingénieur ML / sécurité. Délimitations : agentic-ai couvre la surface agentique (MCP,
> tool poisoning), agentic-memory le MINJA, RAG le PoisonedRAG/BadRAG — se centrer sur la taxonomie
> attaques/défenses au niveau du MODÈLE, pas sur l'infrastructure agentique ni le RAG. Domaine :
> llm-agents-generation.

### Vision-Language Models (VLM) — `multimodal-vlm` → `llm-agents-generation`
**Verdict : nouveau gap.** ViT (transformer-attention) et conditionnement cross-attention
(diffusion) seulement.

> Vision-Language Models (VLM) et fusion multimodale : aligner image et texte dans un même modèle.
> Couvrir l'alignement contrastif (CLIP en rappel), les architectures de fusion (encodeur visuel +
> LLM via projection/Q-Former — BLIP-2 ; cross-attention — Flamingo ; tokens visuels en entrée —
> LLaVA), l'instruction-tuning multimodal, le traitement de la résolution/des patchs, et les
> benchmarks (VQA, captioning, hallucination visuelle). Positionnement : pertinence croissante,
> absent en tant que thème cohérent. Public : ingénieur ML. Délimitations : transformer-attention
> couvre le ViT, diffusion-models le conditionnement (génération d'images), agentic-ai l'agent
> incarné (PaLM-E) — se centrer sur l'architecture VLM et l'alignement vision→langage pour la
> compréhension ; le contrastif/CLIP est approfondi par contrastive-self-supervised (le citer).
> Domaine : llm-agents-generation.

### SVM / méthodes à noyau — `svm-kernel-methods` → `classical-ml-time-series`
**Verdict : gap réel.** Le kernel trick n'est effleuré que via Kernel PCA et les noyaux GP.

> Machines à vecteurs de support (SVM) et méthodes à noyau : classer par marge maximale. Couvrir le
> classifieur à marge maximale (hyperplan séparateur, vecteurs de support), la formulation duale et
> le kernel trick (noyaux linéaire, polynomial, RBF/gaussien, théorème de Mercer, RKHS), le
> soft-margin et la hinge loss (paramètre C), l'optimisation (SMO), la régression (SVR) et le
> panorama des méthodes à noyau. Positionnement : pilier du ML classique. Public : ingénieur ML.
> Délimitations : clustering-dimensionality-reduction couvre le kernel trick côté Kernel PCA
> (noyaux RBF/poly, matrice de Gram) et time-series-forecasting les noyaux GP (les citer sans
> re-dériver) — se centrer sur la marge maximale, la dualité, la hinge loss et SMO. Domaine :
> classical-ml-time-series.

### Graph neural networks (GNN) — `graph-neural-networks` → `deep-learning-foundations`
**Verdict : gap réel.** ⚠️ `knowledge-graph-construction` traite l'*extraction* de graphes (≠
apprendre dessus) ; GraphRAG/agentic-memory utilisent des graphes sans message passing.

> Graph neural networks (GNN) : apprendre sur des données structurées en graphe. Couvrir le cadre du
> message passing (agrégation de voisinage, mise à jour, lecture), les architectures de référence
> (GCN spectral/spatial, GraphSAGE et l'échantillonnage de voisinage, GAT et l'attention sur arêtes,
> GIN et le pouvoir expressif lié au test de Weisfeiler-Lehman), le pooling de graphes, les tâches
> (classification de nœuds/graphes, prédiction de liens), et les pièges (oversmoothing,
> oversquashing, passage à l'échelle). Positionnement : famille d'architectures absente d'un corpus
> 100 % séquence/transformer. Public : ingénieur ML. Délimitations : ⚠️ knowledge-graph-construction
> traite l'EXTRACTION de graphes depuis le texte ; GraphRAG (RAG) et les knowledge graphs
> (agentic-memory) utilisent des graphes sans message passing — se centrer sur l'apprentissage de
> représentations sur graphes. Domaine : deep-learning-foundations.

### Sketches en flux : quantiles & échantillonnage — `streaming-quantiles-sampling` → `probabilistic-structures-hashing`
**Verdict : gap réel.** Complète `count-min-sketch` (fréquences) et `hyperloglog` (cardinalité).

> Sketches de flux pour quantiles et échantillonnage : résumer un flux de données en mémoire bornée.
> Couvrir l'estimation de quantiles approchés (Greenwald-Khanna et la garantie ε, t-digest et les
> centroïdes à compression variable, KLL et son optimalité), et l'échantillonnage en flux (reservoir
> sampling : Algorithm R, échantillonnage pondéré A-Res, échantillonnage distribué), avec les
> garanties d'erreur et la fusionnabilité (mergeable summaries) pour le calcul distribué.
> Positionnement : complète la famille des sketches de flux du domaine. Public : ingénieur ML/data.
> Délimitations : count-min-sketch et hyperloglog couvrent d'autres sketches en flux (fréquences,
> cardinalité) — les citer comme voisins ; se centrer sur quantiles et échantillonnage. Domaine :
> probabilistic-structures-hashing.

---

## Priorité basse / marginale

### MinHash & déduplication — `minhash-dedup` → `probabilistic-structures-hashing`
**Verdict : partiel.** ⚠️ La théorie LSH a déjà une section dédiée dans
`approximate-nearest-neighbor` (et ALSH/MIPS dans `text-embeddings`) → recibler sur MinHash/dedup.

> MinHash et déduplication par similarité d'ensembles : estimer la similarité de Jaccard et trouver
> les quasi-doublons à grande échelle. Couvrir le MinHash (min-wise independent permutations,
> estimateur non biaisé de Jaccard et sa variance, b-bit minwise), l'amplification par bandes (LSH
> banding pour le similarity-join, courbe en S, réglage bandes×lignes), SimHash pour le cosinus, et
> l'application phare : la déduplication de gros corpus (dont les jeux d'entraînement LLM, MinHash-LSH
> à l'échelle). Public : ingénieur ML/data. ⚠️ Délimitations strictes : la THÉORIE LSH a déjà une
> section dédiée dans approximate-nearest-neighbor (familles (r,cr,p1,p2), E2LSH, exposant ρ) et
> text-embeddings traite l'ALSH pour le MIPS — NE PAS re-dériver le cadre LSH générique ; se centrer
> sur MinHash/Jaccard, la min-wise independence et la déduplication comme killer app. Domaine :
> probabilistic-structures-hashing.

### Cuckoo filter — `cuckoo-filter` → `probabilistic-structures-hashing`
**Verdict : partiel (marginal).** ⚠️ `bloom-filters` traite **déjà** le Cuckoo filter (Fan et al.
2014) en plusieurs claims — ce thème n'a de sens que s'il va nettement plus loin, sinon enrichir
`bloom-filters` plutôt qu'un thème séparé.

> Le Cuckoo filter : test d'appartenance approximatif avec suppression. Couvrir le cuckoo hashing
> (deux fonctions de hachage, relocalisation, facteur de charge), le partial-key cuckoo hashing qui
> ne stocke que des empreintes (fingerprints), les opérations insert/lookup/delete, l'analyse du
> taux de faux positifs et de l'occupation, l'optimisation semi-sorting, et la comparaison fine avec
> les alternatives (counting Bloom, quotient filter, xor filter). Public : ingénieur ML/systèmes.
> ⚠️ Délimitations : bloom-filters traite DÉJÀ le Cuckoo filter (suppression, seuils comparatifs
> Bloom/cuckoo/xor) — ne lancer ce thème que s'il approfondit nettement (partial-key cuckoo hashing
> détaillé, semi-sorting, analyse vs quotient/xor) ; sinon enrichir bloom-filters. Domaine :
> probabilistic-structures-hashing.

### Gaussian processes (général) — `gaussian-processes` → `classical-ml-time-series`
**Verdict : partiel.** `time-series-forecasting` a une section GP orientée prévision ; l'angle neuf
= régression/classification bayésienne générale + optimisation bayésienne.

> Processus gaussiens (GP) : régression et classification bayésiennes non paramétriques avec
> quantification d'incertitude. Couvrir la définition (distribution sur fonctions, moyenne + noyau de
> covariance), la régression GP (postérieure analytique, choix/combinaison de noyaux
> RBF/Matérn/périodique, apprentissage des hyperparamètres par vraisemblance marginale), le coût
> O(n³) et les approximations (inducing points, SVGP), la classification GP (Laplace/EP), et
> l'application phare : l'optimisation bayésienne (fonctions d'acquisition EI/UCB). Public : ingénieur
> ML. Délimitations : time-series-forecasting a déjà une section GP orientée prévision (noyau
> périodique/Matérn, O(n³), état-espace/SDE, inducing points/SVGP) — la citer ; l'angle neuf = la
> régression/classification bayésienne générale et l'optimisation bayésienne. Domaine :
> classical-ml-time-series.

### Calibration des classifieurs — `calibration-classifieurs` → `classical-ml-time-series`
**Verdict : nouveau gap.** Totalement absent (llm-evaluation traite l'accord juge/humain, pas la
calibration probabiliste).

> Calibration des classifieurs probabilistes : faire en sorte que les probabilités prédites reflètent
> les fréquences réelles. Couvrir le diagnostic (reliability diagrams, ECE/MCE, Brier score), les
> méthodes post-hoc (Platt scaling, isotonic regression, temperature scaling pour les réseaux
> profonds), la mauvaise calibration des réseaux modernes, et la prédiction conforme (conformal
> prediction) comme garantie de couverture distribution-free, en pont. Public : ingénieur ML.
> Délimitations : llm-evaluation traite l'accord juge/humain au sens psychométrique (kappa, alt-test)
> et C-RAG le conformal risk control en contexte RAG — se centrer sur la calibration de probabilités
> de classification. Domaine : classical-ml-time-series.

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
