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

**Ajout du 2026-07-23** (corpus à 56 monographies) : +1 candidat `multi-agent-orchestration`, issu
d'une veille sur le buzz « graph engineering » (terme né le 18 juillet 2026 — tweet de Steinberger
puis « Loop Engineering Is Dead » de Husain 4 h 30 plus tard). Le buzzword lui-même est écarté comme
sujet (trop jeune pour la règle des ≥ 2 sources indépendantes, corpus primaire = tweets et
Substacks) ; le sujet de fond — topologies, frameworks et modes d'échec des systèmes multi-agents —
est retenu en priorité moyenne. L'acception « context/knowledge graphs pour agents » est déjà
couverte (agentic-memory, knowledge-graph-construction, retrieval-augmented-generation).

**Passe d'enrichissement du 2026-08-06** (corpus à 65 thèmes, backlog à 0 candidat « haute ») : veille
web sur les tendances 2026 — bibliométrie arXiv H1 2026 (long-horizon planning +510 %, agentic
workflows ×2,3, synthetic data −24 %, state space models −20 %), revue LLM 2026 de Raschka
(« long-context efficiency is king », hybrides sparse+linéaire), post-training (GRPO/DAPO/RLVR),
sécurité des agents (OWASP 2026), SWE-bench Pro, SLM embarqués, génération vidéo. Sept candidats
retenus, quatre sujets à la mode **écartés** parce que déjà couverts. Vérification de gap par
LECTURE de la prose des voisins (greps de localisation, puis lecture des sections concernées) —
trois trouvailles ont décidé des verdicts : (1) `transformer-attention` **exclut explicitement**
les attentions linéaires et parcimonieuses de son périmètre (« FlashAttention n'est pas
sous-quadratique… le ranger parmi les attentions linéaires ou parcimonieuses confond une
optimisation IO-aware avec une approximation algorithmique »), et n'aborde l'attention sink que
côté interprétation ; (2) `calibration-classifieurs` **ne mentionne jamais les LLM** — la
calibration y est traitée sur classifieurs, la couverture conforme sur ensembles de prédiction ;
(3) `agentic-ai` traite déjà tool poisoning, CVE MCP et confused deputy, ce qui réduit fortement
l'angle « sécurité des agents ».

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

### Attention parcimonieuse & long contexte — `sparse-attention-long-context` → `deep-learning-foundations`
**Verdict : gap réel (ajout 2026-08-06).** `transformer-attention` pose le mur quadratique puis
traite l'attention EXACTE (FlashAttention 1/2/3, MQA/GQA/MLA) et **écarte nommément** les familles
linéaire et parcimonieuse ; il n'aborde l'attention sink que sous l'angle « l'attention n'est pas
une explication ». `state-space-models` couvre l'attention linéaire par la dualité SSD et les
hybrides attention+SSM (MambaFormer, Samba, Jamba). `context-engineering` cite BigBird/Longformer
en deux phrases, au titre du coût. Personne ne traite la parcimonie comme design d'architecture —
or c'est la direction dominante de 2026 (efficacité du long contexte pour les harnesses d'agents).

> Attention parcimonieuse (sparse attention) et efficacité du long contexte : réduire le calcul de
> l'attention, pas seulement ses accès mémoire. Couvrir les motifs statiques fondateurs (attention
> locale à fenêtre glissante, tokens globaux, aléatoire : Longformer, BigBird, et la longueur de
> chemin qu'ils préservent), le streaming par tokens-puits (StreamingLLM et la mécanique de
> l'attention sink), la sélection dynamique de KV à l'inférence (éviction et budget par tête, sparse
> prefill), l'attention parcimonieuse NATIVE entraînée de bout en bout (NSA de DeepSeek, MoBA,
> InfLLM-v2), les hybrides parcimonieux+linéaires de 2026 et leurs ratios de couches, et
> l'arbitrage mesuré : ce que la parcimonie coûte en rappel exact et en raisonnement. Public :
> ingénieur ML. ⚠️ Délimitations strictes : transformer-attention couvre l'attention exacte et son
> optimisation IO-aware (FlashAttention) ainsi que MQA/GQA/MLA — NE PAS les re-dériver, et
> reprendre sa distinction exact/approché comme point de départ ; state-space-models couvre
> l'attention linéaire (dualité SSD) et les hybrides attention+SSM — ici la parcimonie, pas la
> récurrence ; llm-inference-serving couvre le KV cache côté système (PagedAttention, préfixes) ;
> context-engineering couvre le context rot côté usage. Domaine : deep-learning-foundations.

### Détection d'hallucinations & incertitude des LLM — `hallucination-detection-uncertainty` → `llm-agents-generation`
**Verdict : gap réel (ajout 2026-08-06).** `calibration-classifieurs` ne parle QUE de classifieurs
(zéro occurrence de « LLM ») ; `retrieval-augmented-generation` borne le risque du pipeline RAG
(C-RAG conforme, Merlin-Arthur, SGI, théorème d'impossibilité) mais côté ancrage, pas côté
détection en génération libre ; `llm-evaluation` traite le juge-LLM et ses biais. Semantic entropy,
SelfCheckGPT, FActScore, confiance verbalisée : 0 occurrence dans le corpus.

> Détecter les hallucinations et estimer l'incertitude d'un LLM : savoir quand la réponse ne vaut
> rien. Couvrir la typologie (confabulation vs erreur de connaissance, incertitude aléatoire vs
> épistémique), l'entropie sémantique (regroupement par équivalence de sens plutôt que par
> séquence de tokens, et les sondes qui l'approchent depuis les états cachés en une seule
> génération), les méthodes par échantillonnage et cohérence (SelfCheckGPT, auto-consistance), les
> signaux internes et déclarés (probabilité de séquence, p(true), confiance verbalisée et sa
> sur-confiance), la vérification factuelle décomposée (FActScore et les métriques par atome), la
> décision qui en découle — abstention, escalade, déférence à un humain — et l'évaluation
> (TruthfulQA, HaluEval, jeux dédiés, et le piège de mesurer un détecteur sur des hallucinations
> fabriquées). Public : ingénieur ML. Délimitations : calibration-classifieurs couvre la calibration
> et la prédiction conforme sur classifieurs (les citer comme socle, ne pas re-dériver ECE ni la
> couverture conforme) ; retrieval-augmented-generation couvre l'ancrage documentaire et ses
> garanties formelles (C-RAG, SGI) — ici le cas sans corpus de référence ; llm-evaluation couvre
> le juge-LLM. Domaine : llm-agents-generation.

---

## Priorité moyenne

Candidats à angle neuf ; chaque entrée porte son prompt riche, prêt à lancer.

(`world-models` : FAIT le 2026-07-10, retiré du backlog.)

(`multi-agent-orchestration` : FAIT le 2026-07-24, retiré du backlog — 17e run /leanmonograph
GREEN après backstop [1 correction dure : blurb MetaGPT « ICLR 2025 »→« ICLR 2024 (oral) »],
classé dans llm-agents-generation après agent-harness-engineering. Ajouté puis fabriqué dans la
foulée de la veille « graph engineering » du 2026-07-23.)

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

(`variational-autoencoders` : FAIT le 2026-07-19, retiré du backlog — 16e run /leanmonograph
GREEN direct, classé dans deep-learning-foundations avant diffusion-models.)

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

(`generative-adversarial-networks` : FAIT le 2026-08-05, retiré du backlog — 25e run
/leanmonograph GREEN direct, backstop propre, classé dans deep-learning-foundations entre
variational-autoencoders et diffusion-models. Gap re-vérifié par lecture avant lancement :
les voisins génératifs publiés depuis le classement du candidat ne citaient les GAN qu'en
contrepoint. Premier run dont le tldr naît des règles de résumé du 2026-08-04.)

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

(`multimodal-vlm` : FAIT le 2026-07-25, retiré du backlog — 19e run /leanmonograph GREEN direct
[backstop 100 % propre, 0 correction], classé dans llm-agents-generation entre
agentic-rl-environments et llm-evaluation. Section modality-gap écartée par l'audit (4 rejets
dont 2 réfutés-jury) : le modality gap de CLIP n'est couvert par aucun claim retenu — angle
résiduel si un candidat « géométrie des espaces d'embedding multimodaux » émerge un jour.
Les candidats document-ai et vision-language-action peuvent désormais se délimiter contre
cette monographie publiée.)

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

(`graph-neural-networks` : FAIT le 2026-07-24, retiré du backlog — 18e run /leanmonograph GREEN
après backstop [2 hedges single-source + sigle workshop RLR→R2L], classé dans
deep-learning-foundations après state-space-models. Section pooling-graphes écartée par l'audit
(3 claims single-source) : le pooling n'est couvert que par un paragraphe DiffPool — angle
résiduel si un candidat « pooling/expressivité avancée » émerge un jour.)

(`streaming-quantiles-sampling` : FAIT le 2026-08-05, retiré du backlog — 26e run /leanmonograph
GREEN après backstop [1 correction dure : divergence INTERNE au document sur la variante mergeable
de KLL, `log²log(1/δε)` dans une section contre `log²log(1/δ)` dans une autre — les deux formes
existent dans l'article original mais pour des problèmes différents (Tableau 1 : un quantile vs
tous les quantiles), et la phrase fautive comparait deux régimes], classé dans
probabilistic-structures-hashing après count-min-sketch, en clôture du bloc des sketches de flux.

Gap re-vérifié par LECTURE avant lancement (5e fois payante) : quatre délimitations absentes du
prompt d'origine ont été ajoutées au brief — (1) `count-min-sketch` traite EN PROFONDEUR les range
queries par décomposition dyadique, la voie « par les fréquences » vers les requêtes de rang ;
(2) la fusionnabilité est déjà exposée des deux côtés (linéarité CMS, PFMERGE), seul le versant
résumés-de-rang était neuf ; (3) `ensemble-learning` NOMME le « weighted quantile sketch » de
XGBoost sans l'expliquer — pont applicatif devenu une section entière ; (4) deux homonymies à
écarter, le *quantile forecasting* de `time-series-forecasting` et le quantile conforme de
`calibration-classifieurs`. Le document écarte explicitement les deux homonymies dès sa première
section.

**Premier run à 0 rejet sur 26** — non par laxisme : les 13 claims `corrected` sont des
contestables que le council a AMENDÉS, plusieurs en inversant le sens. D'où une leçon de backstop :
`lint.py` ne traque que les claims REJETÉS, donc une prose qui garderait la version d'origine d'un
claim corrigé serait invisible au lint. Vérifiés un par un ici, tous rendus dans leur version
amendée.)

(`llm-inference-serving` : FAIT le 2026-07-17/18, retiré du backlog — 14e run /leanmonograph
GREEN après resume, classé dans llm-agents-generation après decoding-sampling ; section
prefix-radix-caching complétée manuellement. Débloque le candidat `model-routing-cascades`.)

(`pretraining-data-curation` : FAIT le 2026-08-01, retiré du backlog — 24e run /leanmonograph
GREEN après backstop, classé dans **deep-learning-foundations** (et non llm-agents-generation
comme prévu ici : le voisin réel est `scaling-laws`, qui traite le data-constrained ET le data
pruning, et vit dans ce domaine) — inséré avant scaling-laws dans le portail. Deux corrections
d'audit du backlog relevées AVANT lancement, par greps : (1) `scaling-laws` traite aussi le
**data pruning** de Sorscher et al. (pas seulement le régime data-constrained) ; (2)
`llm-evaluation` traite déjà la **contamination des benchmarks côté évaluation** — le thème s'est
donc recentré sur la décontamination côté corpus.

**Ce run a mis au jour un défaut de la garantie « ≥ 2 sources indépendantes ».** `collectSources`
dédoublonnait les sources par URL : `arxiv.org/abs/X` et `arxiv.org/html/X` comptaient pour deux,
de même qu'un préprint et ses actes de conférence, ou un papier et le blog de ses auteurs. Cinq
claims du thème portaient une mention « 2 sources indépendantes » inexacte. Corrigé dans les trois
workflows (dédoublonnage par travail : identifiant arXiv/DOI + titre dépouillé de son suffixe
d'édition). **Reste ouvert : ≥ 39 claims sur 28 thèmes du corpus publié sont dans ce cas** — audit
non lancé.)

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

(`event-extraction-temporal` : FAIT le 2026-07-27, retiré du backlog — 21e run /leanmonograph
GREEN après backstop [1 correction : sur-hedge du Build retiré, « 5 349 mentions ACE 2005 »
corroboré par MAVEN], classé dans information-retrieval-representation après relation-extraction.)

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

(`agent-evaluation-observability` : FAIT le 2026-07-18, retiré du backlog — 15e run /leanmonograph
GREEN direct, classé dans llm-agents-generation après llm-evaluation.)

(`diffusion-language-models` : FAIT le 2026-07-30, retiré du backlog — 23e run /leanmonograph
GREEN après backstop [1 correction dure : chiffre FIM Mercury 84,8 % vs Codestral 82,5 %, rejeté
single-source mais affirmé nu — angle mort NOUVEAU du lint : les mêmes pivots vivaient dans les
`examples` d'un claim retenu (claim:21, confirmé sur le débit/arena, pas sur le FIM), donc exclus
comme « non distinctifs » ; les `examples` d'un claim retenu peuvent blanchir les pivots d'un
claim rejeté], classé dans llm-agents-generation entre decoding-sampling et llm-inference-serving.
Gap re-vérifié par greps avant lancement : une seule occurrence corpus, clause d'exclusion dans
diffusion-models.)

(`gpu-kernels-compilers` : FAIT le 2026-07-28, retiré du backlog — 22e run /leanmonograph
GREEN après backstop [2 corrections], classé dans deep-learning-foundations après
distributed-training-parallelism. Deux leçons. **Le SUR-HEDGE se confirme comme classe, pas
comme accident** (2e occurrence consécutive après le 21e run) : le Build a hedgé « source unique »
la filiation Halide de TVM/nvFuser/NNC que l'Audit-prose avait délibérément laissée nue — or
l'article TVM, présent dans la bibliographie du document, revendique lui-même cette filiation.
**Nouvelle variante de l'ASYMÉTRIE DE TRAITEMENT** (7e angle mort) : elle peut vivre à
l'intérieur d'une section retenue, entre deux paragraphes voisins issus du même claim rejeté —
le lint reste aveugle quand les pivots sont reformulés (« 1 134 » pour un pivot « 1100 ») ou
écrits en toutes lettres (« soixante-dix » pour « 70 »), cumul des angles morts 11e et 7e.
Deux corrections d'audit du backlog au passage : « Roofline » n'apparaissait nulle part dans le
corpus, seule l'**intensité arithmétique** y était traitée ; et l'homonymie *Triton Inference
Server* / **langage Triton** n'avait pas été relevée.)

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

(`document-ai` : FAIT le 2026-07-27, retiré du backlog — 20e run /leanmonograph GREEN après
backstop [1 correction : réserve single-source sur GriTS], classé dans
information-retrieval-representation à la charnière entre le bloc recherche et le bloc
structuration (parcours du portail : juste après retrieval-augmented-generation). Section
metriques-anls-teds-grits écartée par l'audit (4 rejets, dont 1 réfuté-jury : ANLS n'est PAS une
similarité continue, elle a un seuil dur τ = 0,5) — la prose et le widget ANLS portent bien la
réfutation, mais le rejet GriTS, single-source équivalent aux 4 rejets hedgés de knowledge.json,
était affirmé nu : **confirmation que les rejets d'une section écartée échappent au lint** (leçon
du 18e run, re-vérifiée ici). Premier run réel de `/arrange` étendu : proposition d'insertion bien
calibrée.)

### Génération de code par LLM — `llm-code-generation` → `llm-agents-generation`
**Verdict : gap réel mais ⚠️ frontière à caler (ajout 2026-08-06).** Le corpus n'a AUCUN thème
code-centré : le code y apparaît toujours comme *application* d'autre chose — `agentic-ai` a une
section « Applications : code, science et entreprise » (Claude Code, ChatDev, taux de succès),
`agent-harness-engineering` traite les harnesses de code (SWE-agent, OpenHands, Aider),
`agent-evaluation-observability` dissèque SWE-bench comme benchmark d'agents, `ia-productivite-esn`
mesure les effets organisationnels, `agentic-rl-environments` fabrique des environnements
vérifiables. Le modèle qui écrit du code — sa lignée, ses formats d'entraînement, ses garanties —
n'est traité nulle part. Sujet au sommet de la visibilité 2026 (leaderboards SWE-bench Pro).

> La génération de code par modèle de langage : ce que le modèle apprend et ce qu'on peut en
> garantir. Couvrir la lignée d'évaluation (Codex et HumanEval, MBPP, puis le basculement vers les
> tâches de dépôt réel : SWE-bench, sa variante Verified, Pro, et les pipelines de collecte
> automatisée type SWE-rebench), les formats d'entraînement propres au code (fill-in-the-middle et
> l'infilling, contexte au niveau du dépôt, dépendances inter-fichiers), les tests comme oracle et
> comme récompense vérifiable (exécution, pass@k et ce qu'il masque, solver-verifier), la
> correction et la réparation de programmes (patch, itération sur l'échec de test), la sécurité du
> code produit (vulnérabilités générées, dépendances hallucinées) et la contamination des
> benchmarks. Public : ingénieur ML/logiciel. ⚠️ Délimitations strictes : agent-harness-engineering
> couvre la BOUCLE et l'outillage (ne pas re-traiter les harnesses) ; agent-evaluation-observability
> couvre SWE-bench comme instrument d'évaluation d'AGENTS et l'écart de harness — s'appuyer dessus
> plutôt que le refaire ; agentic-rl-environments couvre le RLVR et ses environnements ;
> ia-productivite-esn couvre l'effet sur les organisations ; reasoning-test-time-compute couvre le
> raisonnement générique. L'angle propre : le code comme modalité d'entraînement et d'évaluation.
> Domaine : llm-agents-generation.

### Édition de connaissances & désapprentissage — `model-editing-unlearning` → `deep-learning-foundations`
**Verdict : gap réel (ajout 2026-08-06).** `mechanistic-interpretability` couvre le steering par
features de SAE et l'intervention causale, et ne cite MEMIT que dans un blurb bibliographique ;
« unlearning », « désapprentissage », « droit à l'oubli », TOFU : 0 occurrence dans le corpus.
`lora` traite l'adaptation, pas la suppression ciblée. Sujet porté en 2026 par la conformité
(effacement sur demande) autant que par la sûreté (retirer une capacité dangereuse).

> Éditer et faire oublier un modèle entraîné : modifier une connaissance sans tout ré-entraîner.
> Couvrir la localisation-puis-édition (ROME et l'hypothèse des MLP comme mémoires associatives,
> MEMIT pour l'édition massive, les méta-apprenants type MEND), les critères d'une bonne édition
> (efficacité, généralisation aux paraphrases, localité/spécificité) et leurs échecs mesurés (effets
> de ricochet sur les faits liés, dégradation après éditions séquentielles), puis le désapprentissage
> machine (ascension de gradient et ses instabilités, NPO, RMU ; désapprentissage exact vs
> approché), ses benchmarks (TOFU, WMDP, MUSE), ses attaques (réapprentissage, extraction résiduelle,
> désapprentissage « superficiel » qui masque sans effacer) et le cadre réglementaire du droit à
> l'effacement. Public : ingénieur ML / conformité. Délimitations : mechanistic-interpretability
> couvre le steering et l'activation patching (les citer : localiser n'est pas éditer) ; lora couvre
> l'adaptation par adaptateurs (un support d'édition, pas son objectif) ; privacy-preserving-ml
> (candidat) couvre la confidentialité différentielle et la mémorisation — se délimiter
> mutuellement : ici on retire après coup ce qui a été appris. Domaine : deep-learning-foundations.

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
> citer comme descendance continue) ; variational-autoencoders (FAIT) couvre l'ELBO — se
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

### Petits modèles & inférence embarquée — `small-language-models-edge` → `llm-agents-generation`
**Verdict : partiel (ajout 2026-08-06).** Les briques existent séparément — `quantization` (PTQ,
formats FP8/FP4), `knowledge-distillation` (fabriquer de petits modèles), `llm-inference-serving`
(servir côté datacenter) — mais le déploiement local est absent : « NPU » = 0 occurrence, et
« on-device » n'apparaît que dans `multimodal-vlm`. Tendance industrielle nette en 2026 (SLM au
bord, arbitrage local/cloud) mais valeur de référence moindre : beaucoup de produit, peu de théorie.
⚠️ **Verdict renversé** : la passe du 2026-07-09 avait écarté ce sujet d'un mot (« croise
llm-inference-serving »). La lecture montre que `llm-inference-serving` traite le serving en
datacenter (batching continu, PagedAttention, SLO) et jamais l'appareil — le recouvrement portait
sur la compression, pas sur le déploiement local. Priorité basse tout de même : sujet de produit.

> Petits modèles de langage et inférence embarquée : faire tourner un LLM sur l'appareil. Couvrir
> ce qui fait un « petit » modèle utile (budget de paramètres vs budget de tokens, MoE à faible
> activation, distillation et données curées), les contraintes matérielles du bord (NPU et TOPS,
> bande passante mémoire comme goulot réel, énergie et enveloppe thermique), les runtimes
> (llama.cpp/GGUF, MLX, ONNX Runtime, exécution mobile), les compromis de qualité mesurés à
> quantification agressive, et l'architecture hybride bord/cloud (ce qu'on garde local, ce qu'on
> escalade, et pourquoi — latence, coût, confidentialité). Public : ingénieur ML/produit.
> Délimitations : quantization couvre les méthodes de compression (GPTQ/AWQ, FP4) et
> knowledge-distillation la fabrication d'élèves — les citer sans re-dériver ;
> llm-inference-serving couvre le serving à l'échelle (batching continu, PagedAttention) ;
> model-routing-cascades (candidat) couvre l'arbitrage qualité/coût par requête. Domaine :
> llm-agents-generation (à trancher par /arrange).

### Génération vidéo — `video-generation-models` → `deep-learning-foundations`
**Verdict : partiel, ⚠️ angle réduit (ajout 2026-08-06).** `diffusion-models` a une section
« Au-delà de l'image : audio, vidéo » et couvre latent diffusion, DDIM/DPM-Solver, guidage,
consistency models ; `world-models` traite « Générer des mondes : de Sora à Genie 3 » côté
simulation. Reste l'angle proprement vidéo — tokenizer spatio-temporel, cohérence, audio joint,
évaluation — mais il faut le tenir serré pour ne pas refaire les deux voisins.

> Modèles de génération vidéo : produire des séquences cohérentes dans le temps. Couvrir la
> compression spatio-temporelle (VAE 3D, tokenisation en patches d'espace-temps) et pourquoi elle
> commande tout le reste, l'architecture DiT appliquée à la vidéo, la cohérence temporelle et
> l'identité des objets d'un plan à l'autre, le conditionnement (texte, image de départ, trajectoire
> de caméra), la génération audio-vidéo synchronisée, le coût d'inférence et les stratégies
> d'accélération, et l'évaluation (VBench et les axes qu'il décompose, ce que les préférences
> humaines mesurent réellement). Public : ingénieur ML. ⚠️ Délimitations strictes :
> diffusion-models couvre le cadre diffusion complet, y compris sa section audio/vidéo — NE PAS le
> re-dériver ; world-models couvre Sora et Genie 3 comme simulateurs de mondes et la physical AI ;
> generative-adversarial-networks couvre la lignée GAN. L'angle propre : la vidéo comme problème de
> représentation spatio-temporelle. Domaine : deep-learning-foundations.

### Sécurité des agents outillés — `agent-tool-security` → `llm-agents-generation`
**Verdict : partiel, ⚠️ chevauchement fort (ajout 2026-08-06).** À ne lancer que si l'angle
« défense en profondeur » tient sans redite : `llm-safety-jailbreaks` a une section entière
« Prompt injection directe et indirecte » (Greshake, taxonomie OWASP, cinq classes d'impact) et une
sur les défenses au niveau du modèle ; `agentic-ai` traite déjà tool poisoning, rug pull, CVE MCP
et confused deputy. Reste non couvert : les défenses ARCHITECTURALES et leur évaluation —
AgentDojo, « lethal trifecta », séparation de privilèges, capacités et flux d'information : 0
occurrence.

> Sécuriser un agent qui agit : quand l'injection ne trompe plus un texte mais déclenche une action.
> Couvrir la conjonction dangereuse (accès à des données privées + exposition à du contenu non
> fiable + capacité d'exfiltrer), les patterns de défense architecturaux (dual-LLM et séparation
> quarantaine/privilège, action-selector, plan-then-execute, systèmes à capacités et contrôle de
> flux d'information), le confinement d'exécution (permissions, bac à sable, approbation humaine
> sur action irréversible), l'identité et la délégation entre agents, et l'évaluation adaptative
> (AgentDojo et les bancs d'attaque, pourquoi une défense évaluée sur attaques fixes surestime sa
> protection). Public : ingénieur ML/sécurité. ⚠️ Délimitations strictes : llm-safety-jailbreaks
> couvre jailbreaks, injection directe/indirecte et défenses côté modèle (classificateurs,
> alignement) — NE PAS les re-traiter ; agentic-ai couvre MCP/A2A et leurs vulnérabilités connues ;
> agent-harness-engineering couvre le design d'outils côté fiabilité. L'angle propre : contenir les
> conséquences plutôt qu'empêcher la tromperie. Domaine : llm-agents-generation.

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

Écartés lors de la passe du 2026-08-06, malgré leur visibilité dans la veille 2026 :

- **Post-training RL moderne (GRPO, DAPO, et le zoo des variantes)** → `rlhf-dpo` (section « GRPO et
  le RL pour le raisonnement », plus le zoo offline IPO/KTO/ORPO/SimPO) et `agentic-rl-environments`
  (section « GRPO et ses descendants : les algorithmes du RLVR », dont DAPO). Le sujet le plus cité
  des revues post-training 2026 est déjà traité deux fois, sous deux angles complémentaires.
- **Deep research agents / agents de recherche** → réparti et couvert : `recursive-language-models`
  traite le deep research multi-documents comme cas d'usage central (BrowseComp-Plus),
  `retrieval-augmented-generation` a « RAG actif, correctif et adaptatif »,
  `multi-agent-orchestration` les topologies de délégation, `agent-evaluation-observability` les
  environnements exécutables et la contamination. Angle résiduel trop mince : la génération de
  rapports longs sourcés et son évaluation par rubriques.
- **Données synthétiques & self-play** → `pretraining-data-curation` (section « Réécrire plutôt que
  jeter », Nemotron-CC/WRAP, et le model collapse), `knowledge-distillation` (traces de raisonnement
  pour fabriquer de petits LLM), `rlhf-dpo` (RLAIF et Constitutional AI),
  `agentic-rl-environments` (fabriquer des environnements vérifiables à l'échelle). À noter : la
  bibliométrie H1 2026 donne le sujet en recul (−24 %).
- **Planification à horizon long** (le topic le plus en croissance de H1 2026, +510 %) →
  `agentic-ai` (fiabilité à horizon long, meltdown de Vending-Bench, pass^k de τ²-bench),
  `recursive-language-models` (section « Récursion, agents et raisonnement long-horizon »),
  `agentic-memory` et `world-models` (planification en imagination). Le buzz nomme un phénomène
  que le corpus traite déjà par ses mécanismes.
