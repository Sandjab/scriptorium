# Backlog des thèmes candidats

Sujets candidats pour de futures monographies du scriptorium, identifiés par **analyse de
couverture du corpus** : pour chaque sujet, on vérifie qu'il n'est pas déjà traité (en thème *ou*
comme contenu substantiel) en scannant les `themes/*/knowledge.json` (claims) et les titres de
sections des `manifest.json`. Chaque candidat porte un **prompt riche** prêt à coller derrière
`/frugalmonograph`, qui encode le périmètre *et* les délimitations anti-doublon.

- **Fabrication** : `/frugalmonograph « <prompt riche> »` puis `/arrange <slug>` (classe le thème
  dans un domaine de `tools/taxonomy.json`).
- **Domaine** = celui de `tools/taxonomy.json` (source de vérité). Un thème = un seul domaine.
- **Sujets déjà couverts** : voir les thèmes listés dans `tools/taxonomy.json`.

> ⚠️ **Méthode de vérification** : utiliser une alternation regex correcte (`grep -E 'a|b|c'`,
> **pas** `grep -E 'a\|b\|c'` — en ERE, `\|` est un pipe *littéral* et ne trouve jamais rien).
> Une première passe avec ce bug avait faussement déclaré « 0 fait » plusieurs sujets en réalité
> couverts (tokenization, gradient boosting) ; voir « Écartés » plus bas.

---

## ⭐ Prochains coups recommandés

### Raisonnement à l'inférence & test-time compute — `reasoning-test-time-compute` → `llm-agents-generation`
Le versant *inférence* du raisonnement est un gap. ⚠️ Le versant *entraînement* (RL pour le
raisonnement) est déjà couvert par `rlhf-dpo` (section « GRPO et le RL pour le raisonnement » :
GRPO, DeepSeek-R1, RLVR, DAPO).

> Raisonnement à l'inférence et test-time compute : améliorer la qualité d'un LLM en dépensant
> plus de calcul au moment de répondre, plutôt qu'en grossissant le modèle. Couvrir le
> chain-of-thought (CoT) comme méthode et ses variantes structurées (self-consistency,
> tree-of-thought, graph-of-thought), l'échantillonnage best-of-N et les vérificateurs / Process
> Reward Models (PRM), les lois d'échelle du test-time compute (qualité vs budget d'inférence), et
> le décodage des modèles de raisonnement (o1/o3, traces longues). Positionnement : le versant
> INFÉRENCE du raisonnement. Public : ingénieur ML. Délimitations strictes : NE PAS re-traiter le
> RL-pour-raisonnement (déjà dans rlhf-dpo, section « GRPO et le RL pour le raisonnement ») ni la
> récursion long-horizon (recursive-language-models) — se centrer sur le compute à l'inférence et
> les méthodes de prompting/recherche au décodage. Domaine : llm-agents-generation.

### Décodage & sampling — `decoding-sampling` → `llm-agents-generation`
L'étape de génération elle-même. Adjacences : le *constrained decoding* est dans
`structured-extraction-llm`, la mécanique du KV cache dans `state-space-models` — le neuf ici =
stratégies de sampling + décodage spéculatif.

> Décodage et sampling pour la génération de texte par LLM autoregressifs : comment, à
> l'inférence, on transforme les logits en tokens. Couvrir les stratégies déterministes (greedy,
> beam search) et stochastiques (température, top-k, top-p/nucleus, min-p, typical sampling), les
> pénalités de répétition et le contrastive search/decoding ; le rôle central du KV cache
> (mécanique, coût mémoire O(L·D), goulot d'inférence) ; et le décodage spéculatif (draft model +
> vérification, Medusa, EAGLE, lookahead decoding) comme principal levier de latence.
> Positionnement : l'étape de génération elle-même — absente du corpus alors que l'entraînement
> (rlhf-dpo) et l'architecture (transformer-attention) sont couverts. Public : ingénieur ML.
> Délimitations : ne pas re-couvrir l'attention/les transformers ni l'entraînement RLHF ; le
> décodage contraint/structuré seulement en bref (couvert par structured-extraction-llm) ; la
> mécanique du KV cache déjà esquissée dans state-space-models (la rappeler sans la re-dériver) ;
> quantification hors périmètre (quantization). Domaine : llm-agents-generation.

---

## Fondations du deep learning

### Scaling laws (Chinchilla, compute-optimal) — `scaling-laws`
Vrai gap : seule mention = `ia-productivite-esn` (section « plafonds : Amdahl, hallucinations,
lois d'échelle », contexte productivité — pas les lois d'entraînement compute-optimales).

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
Mentions éparses seulement (diffusion-models, hybrid-search-reranking, tabular — 1 claim chacune,
aucune section dédiée). Complète le triptyque de compression avec `quantization` et `lora`.

> Distillation de connaissances (knowledge distillation) : transférer la capacité d'un modèle
> enseignant (grand) vers un élève (petit) pour compresser à moindre perte. Couvrir la formulation
> de Hinton (soft targets, température, KL sur les logits), la distillation de features/attention
> (DistilBERT, TinyBERT), la distillation au niveau séquence pour le génératif, la self-distillation
> et la born-again, et l'usage moderne pour fabriquer de petits LLM (distillation de traces de
> raisonnement, données synthétiques par l'enseignant). Positionnement : complète le triptyque de
> compression avec quantization (précision numérique) et lora (PEFT). Public : ingénieur ML.
> Délimitations : quantization et lora sont des thèmes distincts (ne traiter que le transfert
> enseignant→élève) ; la distillation de raisonnement n'est qu'un cas d'usage, à relier au candidat
> reasoning-test-time-compute sans le re-couvrir. Domaine : deep-learning-foundations.

### Optimiseurs (Adam / AdamW) — `optimizers-adam`
Mentions éparses (backpropagation, lora, prompt-optimization…), aucune section dédiée. La règle de
mise à jour : backpropagation calcule les gradients, les optimiseurs les consomment.

> Optimiseurs adaptatifs pour l'entraînement de réseaux profonds, centrés sur Adam et AdamW : que
> faire du gradient une fois calculé. Couvrir le rappel SGD + momentum et le besoin d'adaptativité,
> la lignée AdaGrad → RMSProp → Adam (moments d'ordre 1 et 2 avec correction de biais), puis AdamW
> (weight decay découplé, et pourquoi il diffère de la régularisation L2), les schedules de learning
> rate (warmup, cosine) et un survol des variantes modernes (Lion, Adafactor, Sophia, Shampoo/Muon).
> Positionnement : la règle de mise à jour — manque fondamental du corpus. Public : ingénieur ML.
> Délimitations : backpropagation couvre le calcul du gradient — ne pas le re-dériver ;
> normalization-layers est un thème distinct. Domaine : deep-learning-foundations.

### RoPE (Rotary Position Embedding) — `rotary-position-embedding`
`transformer-attention` effleure l'encodage positionnel (2 claims), sans traitement dédié de RoPE
ni de l'extension de contexte. Central pour le contexte long.

> Le Rotary Position Embedding (RoPE) et l'encodage positionnel dans les transformers : injecter
> l'ordre des tokens dans une attention invariante par permutation. Couvrir le besoin d'information
> positionnelle (positionnel absolu sinusoïdal vs appris vs relatif), le mécanisme RoPE (rotation
> par sous-espaces 2D, position relative émergeant du produit scalaire, matrice de rotation), ses
> propriétés (décroissance longue portée, extrapolation) et l'extension de contexte (Position
> Interpolation, NTK-aware scaling, YaRN, dynamic NTK) ; ALiBi comme alternative et point de
> comparaison. Positionnement : composant fondamental des transformers modernes, central pour le
> contexte long. Public : ingénieur ML. Délimitations : transformer-attention couvre l'attention
> elle-même — ne citer l'attention que comme mécanisme hôte ; ne pas empiéter sur
> state-space-models (autre voie au long contexte), juste contraster. Domaine :
> deep-learning-foundations.

---

## Structures probabilistes & hachage

### MinHash + LSH — `minhash-lsh`
Le sketch de similarité d'ensembles. ⚠️ Le LSH est déjà traité comme *contenu* dans la
monographie ANN (`approximate-nearest-neighbor`, 1 section) — ne pas en faire un doublon ; centrer
sur MinHash/Jaccard et la dédup.

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
Cité dans `bloom-filters` (3 claims) comme alternative, sans traitement dédié. Complète la famille
AMQ en ajoutant la suppression.

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

Identifiés mais pas encore retenus comme candidats actifs. ⚠️ Plusieurs sont partiellement
couverts comme contenu — à re-vérifier avant fabrication :

- **Learned sparse retrieval (SPLADE)** ou **ColBERT / late interaction** → `information-retrieval-representation`
  — ⚠️ déjà esquissés dans `hybrid-search-reranking` (1 section + 3 claims) ; n'en faire un thème
  que si l'angle dédié est assez riche.
- **Streaming quantiles (t-digest / KLL)** → `probabilistic-structures-hashing` (complète les sketches de flux ; quasi 0 couverture).
- **Reservoir sampling** → `probabilistic-structures-hashing` (échantillonnage de flux ; 0 couverture ; sujet « petit »).
- **SVM / méthodes à noyau** → `classical-ml-time-series` (0 couverture ; manque classique).
- **Gaussian processes** → `classical-ml-time-series` (effleuré dans tabular/time-series).
- **Graph neural networks (GNN)** → `deep-learning-foundations`
  (⚠️ délimiter vs `knowledge-graph-construction` : construire un KG ≠ apprendre sur graphe).

---

## Écartés après re-vérification (déjà couverts en profondeur)

- **Tokenization (BPE / SentencePiece / byte-level)** — couvert par **`text-embeddings`** :
  3 sections dédiées (« Découper le texte… BPE », « BPE, WordPiece, Unigram, SentencePiece… »,
  « Ce que coûte une tokenisation optimale… ») + 16 claims (BPE glouton, byte-level GPT-2,
  WordPiece, SentencePiece/▁, glitch tokens, tiktoken). Pas un nouveau thème.
- **Gradient boosting (XGBoost / LightGBM / CatBoost)** — couvert par **`ensemble-learning`** :
  2 sections dédiées (« Gradient boosting et XGBoost », « Variantes modernes : LightGBM, CatBoost,
  HistGradientBoosting ») + 15 claims. Pas un nouveau thème.
