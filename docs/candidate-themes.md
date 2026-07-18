# Backlog des thèmes candidats

Sujets candidats pour de futures monographies du scriptorium, issus d'une **analyse de couverture
en profondeur** : un agent-lecteur par monographie a **lu le texte rédigé** (`manifest.json` =
prose + `knowledge.json` = faits) des 32 monographies et produit un inventaire détaillé des sujets
traités ; un agent de synthèse en a dérivé la carte de couverture, un verdict par candidat et les
gaps réels. (Cette passe corrige une analyse antérieure faussée par un `grep -E 'a\|b\|c'` —
en ERE, `\|` est un pipe *littéral* ; ne jamais l'utiliser.)

**Passe d'enrichissement du 2026-07-02** (corpus à 41 monographies) : retrait des 5 candidats
devenus FAITS depuis la refonte (scaling-laws, named-entity-recognition-sequence-labeling,
entity-linking-disambiguation, coreference-resolution, calibration-classifieurs ;
knowledge-distillation déjà retiré) et ajout de 15 candidats, dont 3 issus d'un audit ciblé de la
chaîne d'extraction d'information (le « pôle NER » : 5 maillons FAITS depuis relation-extraction, mais
événements/temporel et supervision faible absents). Vérification de couverture par greps
ciblés (frontières de mots, casse respectée pour les sigles) sur les `knowledge.json`/`manifest.json`
publiés, puis lecture du contexte de chaque mention — méthode plus légère que la passe initiale par
agents-lecteurs, suffisante pour trancher gap/partiel/écarté.

**Passe d'enrichissement du 2026-07-09** (corpus à 45 monographies) : ajout de 5 candidats issus
d'un balayage des tendances 2026 (harness/loop engineering, context engineering, RLVR et
environnements d'agents, évaluation/observabilité des agents, world models), chacun vérifié par
greps ciblés sur le corpus publié : `self-improving-harness` couvre déjà l'anatomie du harness et
son auto-optimisation, `agentic-ai` la boucle ReAct/tool use et MCP/A2A, `recursive-language-models`
le context rot et la compaction, `rlhf-dpo` pose RLVR — les nouveaux candidats se délimitent contre
ces acquis. (`agent-harness-engineering` : FAIT le 2026-07-10, retiré du backlog.)

**Passe d'enrichissement du 2026-07-17** (corpus à 52 monographies) : ajout de 8 candidats après
épuisement de la priorité haute — nouvelles modalités (texte par diffusion, audio, document image,
action robotique), couche systèmes (kernels/compilation, routage multi-modèles) et provenance
(watermarking). Chacun vérifié par greps ciblés sur les `knowledge.json`/`manifest.json` publiés
puis lecture du contexte des mentions. Deux pièges de délimitation relevés : le flow matching est
déjà traité EN PROFONDEUR par `diffusion-models` (le candidat flows se recentre sur la
vraisemblance exacte), et le candidat `llm-inference-serving` inclut déjà le routage infra (le
candidat routage se recentre sur l'arbitrage qualité/coût par requête).

- **Fabrication** : `/leanmonograph « <prompt riche> »` (défaut depuis le test GREEN du 2026-07-02 ;
  `/frugalmonograph` en repli) puis `/arrange <slug>`.
- **Domaine** = celui de `tools/taxonomy.json` (source de vérité). Un thème = un seul domaine.
- **Verdicts** : `gap réel` (rien de substantiel) · `partiel` (effleuré/adjacent ailleurs, angle
  neuf à cibler) · `écarté` (déjà couvert en profondeur).

---

## Priorité haute — gaps réels, forte valeur de référence

(`contrastive-self-supervised` : FAIT le 2026-07-10, retiré du backlog.)
(`agentic-rl-environments` : FAIT le 2026-07-10, retiré du backlog.)
(`reinforcement-learning-fundamentals` : FAIT le 2026-07-10, retiré du backlog.)
(`context-engineering` : FAIT le 2026-07-11, retiré du backlog.)
(`distributed-training-parallelism` : FAIT le 2026-07-11, retiré du backlog.)

---

## Priorité moyenne

Candidats à angle neuf ; chaque entrée porte son prompt riche, prêt à lancer.

(`world-models` : FAIT le 2026-07-10, retiré du backlog.)

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
> se centrer sur les modèles de préférence et l'évaluation ; learning-to-rank (FAIT)
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

(`llm-safety-jailbreaks` : FAIT le 2026-07-17, retiré du backlog — 13e run /leanmonograph GREEN,
classé dans llm-agents-generation après llm-evaluation.)

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

(`llm-inference-serving` : FAIT le 2026-07-17/18, retiré du backlog — 14e run /leanmonograph
GREEN après resume, classé dans llm-agents-generation après decoding-sampling ; section
prefix-radix-caching complétée manuellement. Débloque le candidat `model-routing-cascades`.)

### Curation des données de pré-entraînement — `pretraining-data-curation` → `llm-agents-generation`
**Verdict : gap réel (angle neuf net).** `scaling-laws` traite le régime data-constrained
(Muennighoff) côté allocation ; le pipeline de données lui-même (filtrage, déduplication, mélanges)
n'est traité nulle part.

> Curation des données de pré-entraînement des LLM : ce qui entre dans le modèle. Couvrir le
> pipeline (extraction depuis Common Crawl, détection de langue, filtres heuristiques puis filtres
> par modèle), la déduplication exacte et approximative et ses effets (mémorisation, qualité), les
> mélanges de domaines et leur optimisation (DoReMi, données synthétiques), la contamination des
> benchmarks, la généalogie des corpus ouverts (C4, The Pile, RefinedWeb, FineWeb et sa démarche
> d'ablations systématiques) et les questions de licence/PII. Public : ingénieur ML. Délimitations :
> scaling-laws couvre le régime data-constrained et les lois d'échelle (le citer) ; la mécanique
> MinHash/LSH de la déduplication relève du candidat minhash-dedup (un pont suffit) ;
> text-embeddings couvre la tokenization — se centrer sur le pipeline de curation et ses ablations.
> Domaine : llm-agents-generation.

### Inférence causale — `causal-inference` → `classical-ml-time-series`
**Verdict : gap réel.** `time-series-forecasting` cite CausalImpact (séries structurelles
bayésiennes) ; `llm-evaluation` emploie « causal » au sens expérimental sans cadre formel ;
potential outcomes, do-calculus, propensity scores = 0 occurrence.

> Inférence causale pour l'ingénieur ML : estimer des effets, pas des corrélations. Couvrir le
> cadre des résultats potentiels (Rubin : ATE/ATT, ignorabilité, SUTVA), les graphes causaux
> (Pearl : DAG, confondants et colliders, critère backdoor, do-calcul), les méthodes d'estimation
> (appariement et scores de propension, IPW, différence de différences, variables instrumentales,
> régression sur discontinuité), le double/debiased machine learning et les méta-learners
> (S/T/X-learner, modélisation d'uplift), et les pièges (biais de sélection, confondants non
> observés, tests placebo et de robustesse). Public : ingénieur ML/data. Délimitations :
> time-series-forecasting couvre CausalImpact (le citer en pont) ; ia-productivite-esn discute
> d'effets de l'IA sans méthodologie causale — se centrer sur l'identification et l'estimation
> d'effets. Domaine : classical-ml-time-series.

### Bandits multi-bras — `multi-armed-bandits` → `classical-ml-time-series`
**Verdict : gap réel.** Aucune occurrence substantielle (les matches « Thompson » du corpus sont
des noms d'auteurs).

> Bandits multi-bras (multi-armed bandits) : décider en ligne sous incertitude. Couvrir le cadre
> (récompense, regret, exploration vs exploitation), les algorithmes de référence (ε-greedy, UCB1
> et le principe d'optimisme face à l'incertitude, Thompson sampling et sa lecture bayésienne), les
> garanties (bornes de regret logarithmiques, borne inférieure de Lai-Robbins), les bandits
> contextuels (LinUCB, bandits neuronaux), les extensions pratiques (non-stationnarité, feedback
> retardé, contraintes de budget) et les applications (A/B testing adaptatif, allocation de trafic,
> recommandation, sélection de prompts ou de modèles). Public : ingénieur ML/data. Délimitations :
> le RL complet (états et transitions) relève de la monographie reinforcement-learning-fundamentals (FAITE) ;
> recommender-systems (candidat) traite les modèles de préférence — se centrer sur le cadre sans
> état et les garanties de regret. Domaine : classical-ml-time-series.

### Extraction d'événements & information temporelle — `event-extraction-temporal` → `information-retrieval-representation`
**Verdict : gap réel (audience plus étroite que la RE).** ACE 2005 n'est cité que comme benchmark
ICL dans `structured-extraction-llm` ; TIMEX seulement comme catégorie MUC historique dans le thème
NER. Triggers/arguments, coréférence d'événements, TimeML = 0 occurrence.

> Extraction d'événements et d'information temporelle : qui a fait quoi, à qui, et quand. Couvrir
> le schéma ACE (triggers, arguments, types d'événements), la détection de triggers et l'étiquetage
> d'arguments (par classification, par question-réponse, par génération), la coréférence
> d'événements, l'extraction temporelle (TimeML et TIMEX3, normalisation des expressions
> temporelles, relations temporelles et TempEval) et la construction de chronologies (timelines),
> avec les benchmarks (ACE 2005, MAVEN, TimeBank). Public : ingénieur NLP. Délimitations :
> structured-extraction-llm cite l'event extraction comme benchmark des LLM extracteurs (le
> citer) ; named-entity-recognition-sequence-labeling détecte les entités qui servent d'arguments ;
> la RE binaire entité-entité relève de la monographie relation-extraction (FAITE) — se centrer sur les
> structures événementielles et le temps. Domaine : information-retrieval-representation.

### Supervision faible & apprentissage actif — `weak-supervision-active-learning` → `classical-ml-time-series`
**Verdict : gap réel.** Seule la supervision distante (cas particulier pour la RE) est traitée
dans `knowledge-graph-construction` ; Snorkel, labeling functions, active learning = 0 occurrence
dans le corpus alors que c'est le goulot pratique de tout projet supervisé.

> Supervision faible et apprentissage actif : obtenir des jeux d'étiquettes quand l'annotation est
> chère. Couvrir la supervision faible programmatique (labeling functions, agrégation de labels
> bruités et modèle génératif de Snorkel, data programming), la supervision distante et son
> débruitage, l'apprentissage actif (échantillonnage par incertitude, query-by-committee,
> diversité/core-sets, le batch mode et ses pièges d'évaluation), la qualité d'annotation (accord
> inter-annotateurs, gold vs silver) et l'annotation par LLM comme supervision faible moderne.
> Public : ingénieur ML/data. Délimitations : knowledge-graph-construction couvre la supervision
> distante pour la RE (la citer comme cas particulier) ; llm-evaluation couvre l'accord juge/humain
> psychométrique (kappa) — se centrer sur la fabrication et l'économie des étiquettes. Domaine :
> classical-ml-time-series (à trancher par /arrange).

### Détection d'anomalies — `anomaly-detection` → `classical-ml-time-series`
**Verdict : gap réel.** Seulement nommée comme cas d'usage (heavy hitters de `count-min-sketch`,
contrainte applicative dans `time-series-forecasting`) ; aucune méthode traitée.

> Détection d'anomalies : repérer le rare et l'aberrant, avec ou sans labels. Couvrir la typologie
> (anomalies ponctuelles, contextuelles, collectives ; outlier vs novelty detection), les méthodes
> statistiques robustes (z-score, MAD), par voisinage et densité (k-NN, LOF), par isolation
> (Isolation Forest et sa variante étendue), à une classe (one-class SVM, SVDD), par reconstruction
> (PCA, autoencodeurs), l'évaluation sans vérité terrain fiable (taux de contamination, PR-AUC vs
> ROC-AUC, benchmarks ADBench) et un pont vers les séries temporelles. Public : ingénieur ML/data.
> Délimitations : count-min-sketch couvre les heavy hitters en flux et time-series-forecasting
> nomme la détection d'anomalies comme contrainte (les citer) ; clustering-dimensionality-reduction
> couvre DBSCAN/HDBSCAN et PCA en propre (s'y référer sans re-dériver) — se centrer sur les modèles
> de score d'anomalie et leur évaluation. Domaine : classical-ml-time-series.

### Évaluation & observabilité des agents — `agent-evaluation-observability` → `llm-agents-generation`
**Verdict : partiel.** `llm-evaluation` couvre l'évaluation des MODÈLES (benchmarks, juges LLM,
psychométrie) ; SWE-bench/GAIA ne sont cités que comme résultats d'état de l'art (`agentic-ai`,
`self-improving-harness`) ; τ-bench, traces, simulation d'utilisateur = 0 occurrence.

> Évaluation et observabilité des agents LLM : mesurer et déboguer des systèmes multi-tours non
> déterministes. Couvrir les benchmarks agentiques (SWE-bench et sa vérification, τ-bench et la
> fiabilité pass^k, GAIA, WebArena/OSWorld) et leurs pièges (contamination, écarts de harness entre
> laboratoires), l'évaluation de trajectoires (succès final vs qualité des étapes, juges de
> trajectoire, simulation d'utilisateur), l'observabilité en production (traces structurées, spans,
> coût/latence par étape, clustering d'échecs) et la boucle trace → dataset → éval (AgentOps).
> Public : ingénieur ML/agents. Délimitations : llm-evaluation couvre l'évaluation des modèles, les
> juges LLM et l'accord juge/humain (la citer, ne pas re-dériver le juge LLM) ; agentic-ai cite
> SWE-bench/GAIA comme état de l'art mesuré (le citer) — se centrer sur l'évaluation des SYSTÈMES
> agents et leur observabilité. Domaine : llm-agents-generation.

### Modèles de langage à diffusion — `diffusion-language-models` → `llm-agents-generation`
**Verdict : gap réel (ajout 2026-07-17).** `diffusion-models` couvre la diffusion continue
(images/audio) et le flow matching ; `decoding-sampling` cite une source sur la génération
parallèle des masked diffusion LMs comme contrepoint de l'autorégressif ; le paradigme lui-même
(D3PM, diffusion masquée, LLaDA, Mercury) = 0 occurrence.

> Modèles de langage à diffusion (diffusion discrète/masquée) : générer du texte sans factorisation
> autorégressive. Couvrir la diffusion sur espaces discrets (D3PM, état absorbant), le score
> entropy (SEDD), la diffusion masquée simplifiée et son passage à l'échelle (LLaDA), les modèles
> déployés (Mercury d'Inception Labs, Gemini Diffusion), le compromis parallélisme/qualité (nombre
> d'étapes vs tokens par étape, ordre de génération, remasking), le lien avec l'infilling et
> l'édition, et les pièges d'évaluation (vraisemblance vs qualité perçue, vitesse réelle).
> Public : ingénieur ML. Délimitations : diffusion-models couvre le cadre continu, l'ELBO et le
> flow matching (le citer, ne pas re-dériver) ; decoding-sampling couvre le décodage autorégressif
> et cite la génération parallèle masquée (le citer en pont) — se centrer sur le paradigme
> diffusion pour le texte. Domaine : llm-agents-generation.

### Kernels GPU & compilation ML — `gpu-kernels-compilers` → `deep-learning-foundations`
**Verdict : gap réel (ajout 2026-07-17).** Triton n'apparaît que via Liger Kernel
(`normalization-layers`) et les noyaux AQLM (`quantization`, blurb) ; XLA via GShard (blurb MoE) ;
torch.compile, fusion d'opérateurs, CUDA Graphs = 0 occurrence. La couche kernels/compilation
n'est traitée nulle part en propre.

> Kernels GPU et compilation pour le deep learning : pourquoi le même modèle va 3× plus vite bien
> programmé. Couvrir le modèle d'exécution GPU (SM, warps, hiérarchie mémoire, coalescing,
> occupancy), l'intensité arithmétique et le Roofline appliqué aux kernels, l'écriture de kernels
> en Triton (tiling, mémoire partagée, autotuning) face à CUDA, la fusion d'opérateurs et ce
> qu'elle économise, la pile torch.compile (TorchDynamo, AOTAutograd, TorchInductor, graph
> breaks), CUDA Graphs contre l'overhead de lancement, et le paysage des compilateurs (XLA, TVM).
> Public : ingénieur ML/infra. Délimitations : transformer-attention couvre FlashAttention comme
> algorithme (le citer comme exemple canonique de kernel IO-aware, ne pas re-dériver) ;
> decoding-sampling couvre le Roofline du décodage et distributed-training-parallelism le MFU et
> le recouvrement calcul/communication (les citer) ; normalization-layers cite Liger Kernel — se
> centrer sur la couche kernels/compilation elle-même. Domaine : deep-learning-foundations.

### Vision-Language-Action — `vision-language-action` → `llm-agents-generation`
**Verdict : partiel (ajout 2026-07-17).** `agentic-ai` a une section « robotique et agents
incarnés » (RT-1, planification par LLM, PaLM-E) et `world-models` couvre la physical AI côté
simulation (Cosmos, GAIA-2) ; RT-2, OpenVLA, π0, la tokenisation d'actions = 0 occurrence.

> Modèles vision-langage-action (VLA) : des politiques robotiques généralistes fondées sur des
> backbones vision-langage. Couvrir le geste fondateur RT-2 (les actions comme tokens de texte,
> co-fine-tuning web + données robot, transfert sémantique), les VLA ouverts (OpenVLA, Octo), les
> têtes d'action continues (diffusion policy, flow matching — π0), les données et la
> cross-embodiment (Open X-Embodiment), l'évaluation (taux de succès réel vs simulation,
> généralisation aux objets/instructions inédits) et les contraintes de déploiement (fréquence de
> contrôle, latence, sécurité). Public : ingénieur ML. Délimitations : agentic-ai couvre le LLM
> planificateur et RT-1 (partir de là, le citer) ; world-models couvre simulateurs et génération
> vidéo pour la physical AI ; le candidat multimodal-vlm couvre l'architecture VLM de
> compréhension — se centrer sur la génération d'actions. Domaine : llm-agents-generation.

### Watermarking & détection de texte généré — `llm-watermarking-detection` → `llm-agents-generation`
**Verdict : gap réel (ajout 2026-07-17).** Watermark, Kirchenbauer, DetectGPT, SynthID =
0 occurrence dans le corpus.

> Tatouage (watermarking) et détection du texte généré par LLM : établir la provenance. Couvrir le
> watermarking par biais de logits (Kirchenbauer et al. : listes verte/rouge, test statistique z,
> compromis détectabilité/distorsion), les schémas cryptographiques indistinguables (Aaronson,
> Christ-Gunn-Zamir), SynthID-Text et le déploiement à l'échelle, la robustesse (paraphrase,
> traduction, attaques de suppression et de spoofing), la détection post-hoc sans tatouage
> (perplexité, DetectGPT/Fast-DetectGPT, classifieurs entraînés) et ses taux d'erreur — notamment
> sur les locuteurs non natifs —, et les limites fondamentales (résultats d'impossibilité).
> Public : ingénieur ML / sécurité. Délimitations : decoding-sampling couvre l'échantillonnage et
> les logits (le citer : le watermarking est une modification du sampling) ; le candidat
> llm-safety-jailbreaks couvre attaques/défenses du modèle — se centrer sur provenance et
> détection. Domaine : llm-agents-generation.

### Document AI — `document-ai` → `information-retrieval-representation`
**Verdict : gap réel (ajout 2026-07-17).** Le corpus traite l'extraction sur texte propre
(`structured-extraction-llm` ; `relation-extraction` niveau document = DocRED, du texte) mais
jamais le document image : OCR, LayoutLM, DocVQA, Donut = 0 occurrence.

> Compréhension de documents (Document AI) : du pixel au contenu structuré. Couvrir l'OCR neuronal
> (détection + reconnaissance, modèles séquence type TrOCR), les modèles texte + layout + image
> (lignée LayoutLM v1→v3 et ses pré-entraînements), les approches sans OCR (Donut, Pix2Struct) et
> les VLM généralistes appliqués au document, les tâches et benchmarks (classification,
> extraction clé-valeur — FUNSD, reconnaissance de tables, DocVQA), le parsing de PDF pour les
> pipelines RAG, et l'évaluation (ANLS, TEDS, pièges des benchmarks saturés). Public : ingénieur
> ML/data. Délimitations : structured-extraction-llm couvre l'extraction depuis le TEXTE (la citer
> comme aval de l'OCR) ; relation-extraction traite le niveau document sur texte propre ; le
> candidat multimodal-vlm couvre l'architecture VLM générique — se centrer sur la modalité
> document/layout. Domaine : information-retrieval-representation.

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

### Topic modeling — `topic-modeling` → `information-retrieval-representation`
**Verdict : gap réel (valeur de référence moindre en 2026).** LDA, Dirichlet, BERTopic :
0 occurrence dans le corpus ; sujet net mais en retrait face aux embeddings pour l'audience visée.

> Topic modeling : découvrir les thèmes latents d'un corpus. Couvrir la lignée (LSA/pLSA → LDA), le
> modèle génératif LDA et son inférence (variationnelle, Gibbs sampling effondré), le choix du
> nombre de topics et les métriques de cohérence (C_v, NPMI, et leurs pièges), les variantes
> (topics corrélés, dynamiques, supervisés), et les approches neuronales par embeddings (Top2Vec,
> BERTopic : réduction + clustering + c-TF-IDF), avec un regard critique sur l'évaluation humaine
> des topics. Public : ingénieur ML/data. Délimitations : clustering-dimensionality-reduction
> couvre UMAP/HDBSCAN en propre et text-embeddings les représentations (les citer sans re-dériver)
> — se centrer sur les modèles thématiques et leur évaluation. Domaine :
> information-retrieval-representation.

### Reconnaissance vocale (ASR) — `speech-recognition-asr` → `deep-learning-foundations`
**Verdict : gap réel (modalité entièrement absente).** Whisper n'apparaît que comme cas d'usage de
compression (`quantization`, WER PTQ 2 bits) ; CTC, wav2vec, Conformer = 0 occurrence. Adéquation à
l'audience ML-engineering correcte mais moins centrale que les candidats texte/vision.

> Reconnaissance vocale automatique (ASR) neuronale : du signal au texte. Couvrir le front-end
> (spectrogrammes log-mel), l'alignement sans segmentation (CTC et son forward-backward,
> RNN-Transducer pour le streaming), les encodeurs (Conformer), le pré-entraînement auto-supervisé
> audio (wav2vec 2.0, HuBERT), l'approche weakly-supervised à grande échelle (Whisper), le décodage
> (beam search, fusion avec un modèle de langue) et l'évaluation (WER et ses pièges, multilinguisme,
> robustesse au bruit). Public : ingénieur ML. Délimitations : quantization cite Whisper comme cas
> de compression (le citer) ; le self-supervised contrastif visuel relève du candidat
> contrastive-self-supervised — se centrer sur la modalité parole. Domaine :
> deep-learning-foundations.

### Fusion de modèles — `model-merging` → `deep-learning-foundations`
**Verdict : gap réel (étroit).** Seul `lora` mentionne une fusion — celle des adaptateurs dans les
poids (merge_and_unload), qui n'est pas la fusion inter-modèles.

> Fusion de modèles (model merging) : combiner plusieurs modèles entraînés sans ré-entraînement.
> Couvrir les model soups (moyenne de poids de fine-tunings), l'arithmétique de tâches (task
> vectors : addition, négation), les méthodes de résolution d'interférences (TIES, DARE), le SLERP,
> la condition sous-jacente (connectivité de mode linéaire, alignement de permutations), les
> applications (multi-tâche, désapprentissage, recyclage de checkpoints) et les limites (modèles de
> bases différentes, échelle). Public : ingénieur ML. Délimitations : lora couvre la fusion
> d'adaptateurs dans le modèle de base (la citer, c'est un cas dégénéré) ; ensemble-learning couvre
> l'agrégation de PRÉDICTIONS, pas de poids — se centrer sur la fusion dans l'espace des paramètres.
> Domaine : deep-learning-foundations.

### ML préservant la confidentialité — `privacy-preserving-ml` → `deep-learning-foundations`
**Verdict : gap réel (audience à confirmer).** `count-min-sketch` est le seul thème à effleurer la
confidentialité ; DP-SGD, apprentissage fédéré, attaques par membership inference = 0 occurrence.

> Machine learning préservant la confidentialité : entraîner sans exposer les données. Couvrir la
> confidentialité différentielle (définition (ε, δ), mécanismes de base, composition), DP-SGD
> (clipping par exemple, bruit, comptabilité des moments) et son coût en utilité, les attaques
> (membership inference, extraction de données mémorisées), l'apprentissage fédéré (FedAvg,
> hétérogénéité des clients, agrégation sécurisée) et sa combinaison avec la DP. Public : ingénieur
> ML. Délimitations : count-min-sketch effleure les sketches privés (le citer) ; la mémorisation
> des LLM croise le candidat pretraining-data-curation (déduplication) — se centrer sur les
> mécanismes de protection et leurs garanties. Domaine : deep-learning-foundations (à trancher par
> /arrange).

### Synthèse vocale & codecs audio neuronaux — `speech-synthesis-tts` → `deep-learning-foundations`
**Verdict : gap réel (ajout 2026-07-17 ; modalité absente, audience comparable au candidat ASR).**
Seul `diffusion-models` touche l'audio, via DiffWave comme vocoder (MOS 4,44 sur LJSpeech).

> Synthèse vocale neuronale (TTS) et codecs audio : du texte à la parole. Couvrir la lignée
> acoustique (Tacotron 2 : mel + vocoder ; FastSpeech non autorégressif et le contrôle
> durée/prosodie), les vocoders (WaveNet, HiFi-GAN, DiffWave), les codecs audio neuronaux
> (SoundStream, EnCodec, quantification vectorielle résiduelle RVQ) et le TTS comme modèle de
> langage sur tokens audio (VALL-E), le zero-shot/voice cloning et ses risques d'usage, et
> l'évaluation (MOS et ses pièges, WER de resynthèse, similarité de locuteur). Public : ingénieur
> ML. Délimitations : diffusion-models couvre DiffWave côté diffusion (le citer) ; le candidat
> speech-recognition-asr couvre la direction inverse (parole→texte, se délimiter mutuellement) —
> se centrer sur la synthèse et les codecs. Domaine : deep-learning-foundations.

### Normalizing flows — `normalizing-flows` → `deep-learning-foundations`
**Verdict : partiel (ajout 2026-07-17 ; ⚠️ angle réduit).** `diffusion-models` couvre DÉJÀ en
profondeur le flow matching, rectified flow et les stochastic interpolants (claims dédiés,
théorèmes de Lipman et al.) — l'angle restant = les flots discrets à vraisemblance exacte, valeur
de référence 2026 moindre.

> Normalizing flows classiques : modéliser une densité par transformations inversibles. Couvrir le
> cadre (changement de variable, log-déterminant du jacobien, vraisemblance exacte), les couplages
> (NICE, RealNVP, Glow et ses convolutions 1×1 inversibles), les flots autorégressifs (MAF/IAF et
> le compromis échantillonnage/densité), les flots continus (Neural ODE, FFJORD), et les
> applications où la vraisemblance exacte compte (inférence par simulation, détection d'anomalies,
> postérieurs variationnels). Public : ingénieur ML. ⚠️ Délimitations strictes : diffusion-models
> couvre le flow matching/rectified flow/stochastic interpolants (NE PAS les re-dériver ; les
> citer comme descendance continue) ; le candidat variational-autoencoders couvre l'ELBO — se
> centrer sur les architectures inversibles et l'estimation de densité exacte. Domaine :
> deep-learning-foundations.

### Routage multi-modèles & cascades — `model-routing-cascades` → `llm-agents-generation`
**Verdict : gap réel mais ⚠️ frontière à caler (ajout 2026-07-17).** RouteLLM, FrugalGPT,
cascades = 0 occurrence ; MAIS `llm-inference-serving` (FAIT le 2026-07-18) traite déjà « le
routage/autoscaling multi-modèles » côté infra (section routage-autoscaling-multimodeles :
routage prefix-cache-aware et load-aware). Dépendance levée — caler la frontière sur l'arbitrage
qualité/coût par requête, en délimitant contre la section routage de llm-inference-serving.

> Routage multi-modèles et cascades de LLM : servir chaque requête au moindre coût à qualité
> maintenue. Couvrir les cascades (FrugalGPT : petit modèle d'abord, escalade sur score de
> confiance), les routeurs appris sur données de préférences (RouteLLM : classifieurs, matrix
> factorization, généralisation à des paires de modèles inédites), le choix statique vs dynamique
> (benchmarks par requête, prédicteurs de difficulté), les métriques (courbes coût-qualité, APGR,
> % d'appels au grand modèle), et le routage en production (fallbacks, dégradation contrôlée,
> multi-fournisseurs). Public : ingénieur ML/infra. ⚠️ Délimitations : llm-inference-serving
> (candidat) couvre le versant infra du routage (autoscaling, SLO) — ici l'arbitrage qualité/coût
> par requête ; decoding-sampling couvre le speculative decoding (accélération intra-modèle, le
> citer en contrepoint) ; ensemble-learning couvre l'agrégation de prédictions (tous les modèles
> répondent) vs le routage (un seul répond). Domaine : llm-agents-generation.

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
- **Attention efficace / FlashAttention / KV cache (MQA, GQA, MLA)** → `transformer-attention`
  (FlashAttention traité comme attention EXACTE, FA-2/FA-3 sur H100 ; MQA/GQA en production,
  MLA −93,3 % de KV cache) ; le speculative decoding est dans `decoding-sampling`. Le versant
  SYSTÈME est désormais traité par `llm-inference-serving` (FAIT le 2026-07-18).
- **Embeddings statiques (word2vec, GloVe, fastText)** → `text-embeddings` (lignée historique
  couverte au sein du thème embeddings).
