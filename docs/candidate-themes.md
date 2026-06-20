# Backlog des thèmes candidats

Sujets candidats pour de futures monographies du scriptorium, identifiés par **analyse de
couverture du corpus** (gaps par domaine + adjacence). Chaque candidat porte un **prompt riche**
prêt à coller derrière `/frugalmonograph`, qui encode le périmètre *et* les délimitations
anti-doublon propres au corpus actuel.

- **Fabrication** : `/frugalmonograph « <prompt riche> »` puis `/arrange <slug>` (classe le thème
  dans un domaine de `tools/taxonomy.json`).
- **Domaine** = celui de `tools/taxonomy.json` (source de vérité). Un thème = un seul domaine.
- **Sujets déjà couverts** : voir les thèmes listés dans `tools/taxonomy.json`.

---

## ⭐ Prochains coups recommandés

Les deux gaps LLM les plus structurants ; tous deux prolongent `state-space-models` côté
inférence/génération.

### Reasoning & test-time compute — `reasoning-test-time-compute` → `llm-agents-generation`
Sans doute le plus gros trou de 2026 (0 fait dans le corpus).

> Raisonnement des LLM et calcul à l'inférence (test-time compute) : améliorer la qualité non par
> plus de paramètres mais par plus de calcul au moment de répondre. Couvrir le chain-of-thought
> (CoT) et ses variantes (self-consistency, tree/graph-of-thought), la montée des modèles de
> raisonnement (o1/o3, DeepSeek-R1) entraînés par RL à produire de longues chaînes, le rapport
> entraînement-RL ↔ inférence, les lois d'échelle du test-time compute (best-of-N,
> vérificateurs/PRM, recherche guidée) et la distillation de traces de raisonnement.
> Positionnement : déplacement de paradigme majeur (2024-2026) totalement absent du corpus.
> Public : ingénieur ML. Délimitations : rlhf-dpo couvre l'alignement par préférences — ici le RL
> spécifiquement pour le raisonnement et le calcul à l'inférence ; ne pas empiéter sur
> self-improving-harness (boucles d'auto-amélioration) ni recursive-language-models (les citer
> comme adjacents). Domaine : llm-agents-generation.

### Décodage & sampling — `decoding-sampling` → `llm-agents-generation`
L'étape de génération elle-même, absente alors que l'entraînement et l'architecture sont couverts.

> Décodage et sampling pour la génération de texte par LLM autoregressifs : comment, à
> l'inférence, on transforme les logits en tokens. Couvrir les stratégies déterministes (greedy,
> beam search) et stochastiques (température, top-k, top-p/nucleus, min-p, typical sampling), les
> pénalités de répétition et le contrastive search/decoding ; le rôle central du KV cache
> (mécanique, coût mémoire O(L·D), goulot d'inférence) ; et le décodage spéculatif (draft model +
> vérification, Medusa, EAGLE, lookahead decoding) comme principal levier de latence.
> Positionnement : l'étape de génération elle-même — absente du corpus alors que l'entraînement
> (rlhf-dpo) et l'architecture (transformer-attention) sont couverts. Public : ingénieur ML.
> Délimitations : ne pas re-couvrir l'attention/les transformers ni l'entraînement RLHF ; le
> décodage contraint/structuré seulement en bref (couvert par structured-extraction-llm) ;
> quantification hors périmètre (quantization) ; l'inférence récurrente des SSM
> (state-space-models) citée comme contraste seulement.

---

## Fondations du deep learning

### Tokenization (BPE / SentencePiece / byte-level) — `tokenization`
L'étage d'entrée de tout LLM, seulement effleuré dans le corpus.

> Tokenization pour les LLM : comment le texte brut devient une séquence d'entiers que le modèle
> consomme. Couvrir le problème (vocabulaire fini vs texte ouvert ; mot↔sous-mot↔caractère↔octet),
> l'algorithme BPE (Byte-Pair Encoding : fusions gloutonnes, entraînement du vocabulaire),
> WordPiece (critère par vraisemblance), Unigram LM / SentencePiece, et le byte-level BPE
> (GPT-2/-4, fallback octet sans <UNK>) ; les enjeux pratiques : taille de vocabulaire vs longueur
> de séquence, tokens spéciaux, fertilité par langue (biais multilingue), traitement des
> espaces/chiffres, et les pièges (glitch tokens, tokenisation des nombres et du code).
> Positionnement : l'étage d'entrée de tout LLM, qui conditionne coût, contexte et performance —
> absent du corpus. Public : ingénieur ML. Délimitations : text-embeddings couvre le passage
> token→vecteur — ne traiter ici que la SEGMENTATION (texte→tokens), pas les embeddings ni
> l'attention. Domaine : deep-learning-foundations.

### Scaling laws (Chinchilla, compute-optimal) — `scaling-laws`
Cadre quantitatif qui gouverne toute décision de budget d'entraînement (0 couverture).

> Lois d'échelle (scaling laws) du deep learning : comment la perte décroît avec les paramètres,
> les données et le compute, et comment allouer un budget de calcul de façon compute-optimale.
> Couvrir les lois en loi de puissance (Kaplan et al. 2020), la révision Chinchilla (Hoffmann et
> al. 2022 : ~20 tokens/paramètre, modèles « sous-entraînés »), le compromis taille-modèle vs
> données à budget FLOPs fixe, les lois pour le transfert/fine-tuning et l'inférence, et leurs
> limites (qualité des données, plafonds, émergence contestée). Positionnement : cadre quantitatif
> absent du corpus alors qu'il gouverne tout. Public : ingénieur ML / décideur technique.
> Délimitations : ne pas re-dériver l'architecture transformer ni l'optimisation
> (backpropagation/optimiseurs) ; rester sur la relation empirique perte↔(N, D, C) et ses
> conséquences d'allocation. Domaine : deep-learning-foundations.

### Knowledge distillation — `knowledge-distillation`
Complète le triptyque de compression avec `quantization` (précision) et `lora` (PEFT).

> Distillation de connaissances (knowledge distillation) : transférer la capacité d'un modèle
> enseignant (grand) vers un élève (petit) pour compresser à moindre perte. Couvrir la formulation
> de Hinton (soft targets, température, KL sur les logits), la distillation de features/attention
> (DistilBERT, TinyBERT), la distillation au niveau séquence pour le génératif, la self-distillation
> et la born-again, et l'usage moderne pour fabriquer de petits LLM (distillation de traces de
> raisonnement, données synthétiques par l'enseignant). Positionnement : complète le triptyque de
> compression avec quantization (précision numérique) et lora (PEFT) — 0 couverture. Public :
> ingénieur ML. Délimitations : quantization et lora sont des thèmes distincts (ne traiter que le
> transfert enseignant→élève) ; la distillation de raisonnement n'est qu'un cas d'usage, à relier
> au candidat reasoning-test-time-compute sans le re-couvrir. Domaine : deep-learning-foundations.

### Optimiseurs (Adam / AdamW) — `optimizers-adam`
La règle de mise à jour : backpropagation calcule les gradients, les optimiseurs les consomment.

> Optimiseurs adaptatifs pour l'entraînement de réseaux profonds, centrés sur Adam et AdamW : que
> faire du gradient une fois calculé. Couvrir le rappel SGD + momentum et le besoin d'adaptativité,
> la lignée AdaGrad → RMSProp → Adam (moments d'ordre 1 et 2 avec correction de biais), puis AdamW
> (weight decay découplé, et pourquoi il diffère de la régularisation L2), les schedules de learning
> rate (warmup, cosine) et un survol des variantes modernes (Lion, Adafactor, Sophia, Shampoo/Muon).
> Positionnement : la règle de mise à jour — manque fondamental du corpus (backpropagation calcule
> les gradients ; les optimiseurs les consomment). Public : ingénieur ML. Délimitations :
> backpropagation couvre le calcul du gradient — ne pas le re-dériver ; normalization-layers est un
> thème distinct. Domaine : deep-learning-foundations.

### RoPE (Rotary Position Embedding) — `rotary-position-embedding`
Encodage positionnel des transformers, central pour le contexte long ; absent du corpus.

> Le Rotary Position Embedding (RoPE) et l'encodage positionnel dans les transformers : injecter
> l'ordre des tokens dans une attention invariante par permutation. Couvrir le besoin d'information
> positionnelle (positionnel absolu sinusoïdal vs appris vs relatif), le mécanisme RoPE (rotation
> par sous-espaces 2D, position relative émergeant du produit scalaire, matrice de rotation), ses
> propriétés (décroissance longue portée, extrapolation) et l'extension de contexte (Position
> Interpolation, NTK-aware scaling, YaRN, dynamic NTK) ; ALiBi comme alternative et point de
> comparaison. Positionnement : composant fondamental des transformers modernes, absent du corpus
> et central pour le contexte long. Public : ingénieur ML. Délimitations : transformer-attention
> couvre l'attention elle-même — ne citer l'attention que comme mécanisme hôte ; ne pas empiéter
> sur state-space-models (autre voie au long contexte), juste contraster. Domaine :
> deep-learning-foundations.

---

## ML classique & séries temporelles

### Gradient boosting (GBDT) — `gradient-boosting`
Le cheval de bataille du ML tabulaire ; rééquilibre un domaine maigre.

> Gradient boosting sur arbres de décision (GBDT) : XGBoost, LightGBM, CatBoost. Couvrir le principe
> du boosting comme descente de gradient fonctionnelle (Friedman, modèle additif d'apprenants
> faibles), la régularisation (shrinkage, sous-échantillonnage lignes/colonnes), puis les trois
> implémentations de référence : XGBoost (boosting de second ordre/Newton, split sparsity-aware,
> weighted quantile sketch), LightGBM (histogrammes, GOSS, EFB, croissance leaf-wise), CatBoost
> (ordered boosting, traitement natif du catégoriel). Positionnement : le cheval de bataille du ML
> tabulaire, qui domine encore le deep learning sur données tabulaires ; enrichit le domaine maigre.
> Public : ingénieur ML. Délimitations : ensemble-learning couvre déjà bagging/boosting/stacking au
> niveau conceptuel — ici, approfondissement spécifique des GBDT (ne pas re-traiter les random
> forests en détail) ; tabular-foundation-models cité comme comparaison seulement. Domaine :
> classical-ml-time-series.

---

## Structures probabilistes & hachage

### MinHash + LSH — `minhash-lsh`
Le sketch de similarité d'ensembles. ⚠️ Le LSH est déjà traité comme *contenu* dans la
monographie ANN — ne pas en faire un doublon.

> MinHash et Locality-Sensitive Hashing (LSH) : estimer la similarité d'ensembles et trouver des
> quasi-doublons à grande échelle. Couvrir la similarité de Jaccard, le MinHash (min-wise hashing,
> estimateur non biaisé et bornes d'erreur), l'amplification LSH (construction AND/OR par bandes,
> courbe en S probabilité de collision vs similarité), les familles LSH (MinHash pour Jaccard,
> SimHash pour le cosinus, p-stable pour l'euclidien) ; application phare : déduplication de corpus
> (dont jeux d'entraînement LLM) et détection de near-duplicates. Positionnement : le sketch de
> similarité d'ensembles, aux côtés de count-min-sketch, hyperloglog et bloom-filters. Public :
> ingénieur ML/data. ⚠️ Délimitations strictes : le LSH est déjà traité comme contenu dans la
> monographie ANN (approximate-nearest-neighbor) — ne PAS en faire un doublon ; centrer sur
> MinHash/Jaccard et la théorie LSH comme structure probabiliste autonome, avec la dédup comme
> killer app, et renvoyer à ANN pour la recherche vectorielle sans la re-dériver. Domaine :
> probabilistic-structures-hashing.

### Cuckoo filter — `cuckoo-filter`
Complète la famille AMQ aux côtés de `bloom-filters` (ajoute la suppression).

> Le Cuckoo filter : alternative moderne au filtre de Bloom pour le test d'appartenance approximatif
> avec suppression. Couvrir le rappel du cuckoo hashing, le stockage d'empreintes (fingerprints) et
> le partial-key cuckoo hashing (deux buckets candidats, relocalisation d'empreinte), les opérations
> insert/lookup/delete, le taux de faux positifs et l'efficacité spatiale comparée à Bloom (quand le
> Cuckoo filter gagne, en-dessous de ~3 % de FPR), le facteur de charge et l'optimisation
> semi-sorting. Positionnement : complète la famille AMQ (approximate membership query) aux côtés de
> bloom-filters, en ajoutant la suppression et une meilleure localité. Public : ingénieur
> ML/systèmes. Délimitations : bloom-filters est un thème distinct — ne traiter Bloom (et counting
> Bloom, quotient filter) que comme référence de comparaison, sans le re-dériver. Domaine :
> probabilistic-structures-hashing.

---

## Tier 2 — non priorisés (en réserve)

Identifiés mais pas encore retenus comme candidats actifs :

- **Learned sparse retrieval (SPLADE)** ou **ColBERT / late interaction** → `information-retrieval-representation`
  (pont entre `bm25-inverted-index` lexical et `text-embeddings` dense ; ⚠️ délimiter vs `hybrid-search-reranking`).
- **Streaming quantiles (t-digest / KLL)** → `probabilistic-structures-hashing` (complète les sketches de flux).
- **Reservoir sampling** → `probabilistic-structures-hashing` (échantillonnage de flux ; sujet « petit »).
- **SVM / méthodes à noyau** ou **Gaussian processes** → `classical-ml-time-series` (manques classiques).
- **Graph neural networks (GNN)** → `deep-learning-foundations`
  (⚠️ délimiter vs `knowledge-graph-construction` : construire un KG ≠ apprendre sur graphe).
