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

**Passe d'enrichissement du 2026-08-26** (corpus à 82 thèmes / 84 documents) : deux sujets soumis
explicitement — « perte de graisse abdominale chez l'homme de plus de 50 ans » et « amélioration des
performances sexuelles (Viagra, Cialis) ». Audit de couverture **par lecture** de la prose publiée
des sept voisins santé concernés (`incretines-glp1`, `masse-maigre-sous-glp1`,
`complements-amincissants`, `berberine`, `testosterone-homme-age`, `sarcopenie-exercice-nutrition`,
`peptides-gris`) après localisation, doublé de huit balayages web. Deux candidats ajoutés
(`graisse-viscerale-homme-age` ; `inhibiteurs-pde5`, qui exige un domaine à créer). Trois constats
ont décidé des verdicts :

1. **La graisse abdominale est partout un critère, nulle part un objet.** Tour de taille comme
   médiateur du bénéfice cardiovasculaire dans SELECT (`incretines-glp1` : −7,7 cm, environ un tiers
   du bénéfice MACE lui étant attribuable) ; comme critère secondaire de quatre méta-analyses
   (`berberine` : −1,08 à −3,27 cm) ; comme critère que la L-carnitine ne déplace pas
   (`complements-amincissants`) ; comme critère d'inclusion de T4DM — 1 007 hommes de 50 à 74 ans,
   tour de taille ≥ 95 cm, **exactement la population demandée**, mais pour un critère de diabète
   (`testosterone-homme-age`) ; comme critère principal de la seule AMM du champ, la tésamoréline
   dans la lipodystrophie du VIH (`peptides-gris` : −18 % et −14 % au scanner L4-L5). Et une seule
   mention de la nature viscérale de la perte, en `sarcopenie-exercice-nutrition`, aussitôt qualifiée
   de « source unique, non corroborée ». **« Perte de graisse » : 0 occurrence dans les
   84 documents** ; aucun document du corpus n'a l'exercice pour objet hors entraînement en
   résistance chez l'âgé (0 occurrence de HIIT, de *spot reduction*, d'« androïde »).
2. **`sildénafil`, `tadalafil`, `PDE5` : 0 occurrence dans les 84 documents.** « Érectile » n'existe
   que dans `testosterone-homme-age`, comme critère diagnostique de l'EMAS et dans l'avis FDA du
   20 avril 2026 — et ce document **nomme** le *Sexual Function Trial* des Testosterone Trials dans
   l'architecture de l'essai sans jamais en dérouler les résultats, tout en concluant que « le seul
   terrain sur lequel le régulateur accepte d'avancer est celui du désir ». La frontière est écrite
   d'avance, et le manque désigné de l'intérieur — troisième prise de l'heuristique du renvoi, sous
   sa forme faible : non pas un renvoi cassé, mais un objet nommé puis laissé de côté.
3. **Le motif de rejet du 2026-08-15 ne tient plus.** `objectif : performances sexuelles` avait été
   écarté parce que son profil « redirait `complements-amincissants` et `peptides-gris` » : vrai d'un
   document centré sur le rayon gris, faux d'un document centré sur une classe de médicaments à AMM
   avec vingt-cinq ans de RCT. L'adultération y devient une section, pas le fil rouge.

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

(`sparse-attention-long-context` : FAIT le 2026-08-07, retiré du backlog — 27e run /leanmonograph
GREEN après backstop [1 correction : une plage de mesures tronquée aux deux bouts, « 1,03–1,16× »
pour des gains horloge réels allant de 1,00× à 1,24× — la borne basse, l'absence pure et simple
d'accélération, renforçait pourtant la thèse du passage], classé dans deep-learning-foundations
**entre transformer-attention et state-space-models** : le parcours présentait les SSM comme « la
réponse au coût quadratique », il en montre désormais deux — élaguer le motif ou renoncer à revoir
le passé. 9/9 sections retenues, 35 claims 22✓/12corr/1rej, 77 sources, 4 widgets ;
7,10M tok / 92 agents / 3 h 57.

Le risque annoncé au council — littérature 2026 portée par un seul rapport de laboratoire — **ne
s'est pas matérialisé** : NSA, MoBA et InfLLM-V2 sont chacun corroborés par 2 à 3 sources
indépendantes. Le seul rejet (TidalDecode) est bien single-source, et son `statement` en anglais
en a fait un cas `foreign_statements` — vérifié à la main, la prose l'attribue et le hedge.

**Angle résiduel COMBLÉ le même jour** : le plan comptait 11 entrées pour un plafond de 9, et les
deux sections tombées à l'arbitrage (`cout-en-qualite`, `ecosysteme`) ont été rédigées et ajoutées
à la main. Le manque était réel et visible dans le rendu : la section sur la mesure des
accélérations se terminait par « Elles ne disent rien de ce qu'elle fait perdre, et c'est l'autre
moitié de l'arbitrage » — une transition sans suite, et « The Sparse Frontier » (arXiv:2504.17768)
figurait en bibliographie sans être lue. ⚠️ Les 11 claims ajoutés (claim:36 à claim:46)
**n'ont pas été jugés par le council** : vérifiés à la source, chacun porte dans son `audit_note`
la nature de ses sources, et `audit-report.md` le dit en tête. Document final : **11 sections,
46 claims**. Effet de bord notable : les 6 flags non hedgés du lint sont tombés à 0, « 2025 »
étant devenu non distinctif en entrant dans un claim retenu.

**Leçon pour le skill** : le plafond `MAX_SECTIONS=9` coupe *après* que le Plan a écrit les
transitions — un document peut donc sortir du pipeline en promettant une suite qui n'existe pas.
Sur un plan à plus de 9 entrées, vérifier la dernière phrase de la dernière section retenue.)

(`hallucination-detection-uncertainty` : FAIT le 2026-08-07, retiré du backlog — 28e run
/leanmonograph GREEN après backstop, classé dans llm-agents-generation **entre llm-evaluation et
agent-evaluation-observability** (le juge externe, puis les signaux internes du modèle, puis la
trajectoire). 9/9 sections, 36 claims 19✓/16corr/1rej, 76 sources, 4 widgets (revue visuelle
faite, clair + sombre) ; 7,33M tok / 121 agents / ~3 h 03 en deux runs — le premier s'est arrêté
en Author sur un garde-fou du script : l'agent de la tranche 1 a rendu `sections: []` validé par
le schéma, reprise par checkpoints `resume: true`.

**Correction du backstop — classe d'angle mort NOUVELLE : le faux rejet par jurés à information
asymétrique.** Deux claims (Kadavath P(True)/P(IK), Tian confiance verbalisée) rejetés sur une
égalité 1-1 : les DEUX jurés avaient vérifié le contenu verbatim exact, mais seul le juré soutien
avait trouvé et vérifié une seconde source indépendante (survey Princeton arXiv:2412.05563) — le
juré réfutation n'a compté que les 2 candidates initiales (à raison jugées même travail) et a
rejeté sur le seuil. Conséquence en cascade : la prose portait un hedge FAUX (« source unique,
non corroborée »). Re-vérifiés à la source puis re-adjugés confirmed, hedges retirés (celui du
chiffre −50 % d'ECE, réellement single-source, conservé), re-adjudication tracée en tête
d'audit-report. **Réflexe : sur tout rejet « seuil non atteint » d'un claim established, comparer
les listes de sources des deux jurés avant de croire le rejet.**)

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

---

# Méta-domaine `sante-nutrition` — backlog de lancement (2026-08-07)

Premier méta-domaine hors IA (spec : `docs/2026-08-07-meta-domaines-sante-design.md` ;
doctrine de preuve : `docs/evidence-sante.md`, à recopier dans chaque brief).
Méta-domaine et domaines sont créés dans `tools/taxonomy.json` par `/arrange` au fil
des publications — jamais à vide. Paramètres fixés :

- Méta : id `sante-nutrition`, label « Santé, nutrition & performance humaine »,
  blurb « Ce que disent réellement les essais cliniques et méta-analyses — doses,
  tailles d'effet, sécurité — derrière les promesses des compléments et traitements. »,
  `notice` = texte du bandeau dans `docs/evidence-sante.md`.
- Domaines : `nutrition-sportive` « Nutrition & supplémentation sportive » (blurb
  « Performance, récupération et composition corporelle : ce qui est démontré, à
  quelle dose. ») ; `complements-sante` « Compléments & santé générale » (blurb
  « Les compléments en vente libre à visée santé/longévité, au tamis des essais. ») ;
  `pharmacologie-metabolique` « Pharmacologie métabolique & perte de poids » (blurb
  « La promesse minceur, du médicament efficace au complément inefficace. »).

**PILOTE = `creatine`** : FAIT le 2026-08-08 — la doctrine a tenu (voir l'entrée FAIT
dans `nutrition-sportive`), le méta-domaine et le domaine sont créés.

**Passe d'enrichissement du 2026-08-15** (corpus à 77 thèmes, backlog santé à 4 candidats dont
0 haute) : audit de couverture **par lecture** — balayage de localisation sur la prose des
76 `sections_draft.json`, puis lecture intégrale des sections concernées de
`complements-amincissants`, `incretines-glp1` et `creatine`. Quatre décisions, dont deux
qui tiennent à ce que le corpus dit **de lui-même** :

1. **Un renvoi cassé a décidé du candidat n° 1.** `incretines-glp1` clôt sa section « Ce qui est
   perdu » par : « Ce qui peut limiter cette perte — apports protéiques, entraînement en
   résistance sous déficit énergétique — relève du versant nutritionnel, **traité ailleurs dans ce
   corpus** et non repris ici. » Ce n'est traité nulle part : `proteines-besoins-timing` porte sur
   l'hypertrophie du sujet entraîné, pas sur la préservation musculaire sous −20 % de poids.
   Un renvoi vers un document inexistant est le signal de gap le plus fiable dont ce corpus
   dispose. → `masse-maigre-sous-glp1`, priorité haute — **FAIT le jour même**, voir son entrée
   dans `pharmacologie-metabolique`. ⚠️ L'heuristique reste ouverte pour les autres : balayer le
   corpus sur « traité ailleurs », « relève de », « non repris ici », puis vérifier PAR LECTURE
   que la cible existe.
2. **Le format « une monographie par objectif » est validé mais tenu rare.** Il existe déjà —
   `complements-amincissants` *est* une monographie par objectif — et il est cher : run le plus
   coûteux du corpus (6,86M tok, deux runs, ~4 h 10) et classe d'erreur factuelle nouvelle (fausse
   indépendance par scission de source), parce que multiplier les molécules multiplie les
   attributions à vérifier. Règle retenue : **un objectif ne mérite sa monographie que si aucune
   molécule seule ne le porte ET que le corpus n'a aucune couverture**. Sur les 8 objectifs
   examinés (perte de poids, masse grasse, prise de masse, endurance, résistance, explosivité,
   performances sexuelles, performances intellectuelles), un seul coche les deux.
3. **Nouveau domaine `performance-cognitive`** (section dédiée en fin de fichier) : couverture
   **nulle** vérifiée par lecture — 0 occurrence de `nootrop*`, `modafinil`, `racétam`, `bacopa`,
   `ginkgo`, `rhodiola`, `ashwagandha`, `théanine`, `méthylphénidate` dans les 76 documents, et
   `cafeine-ergogene` ne dit **rien** du versant cognitif (0 occurrence de « cognition »/« cognitif »
   dans ses 12 sections). Le label du méta-domaine promet pourtant déjà « performance **humaine** ».
4. **Écartés** — `objectif : perte de poids / masse grasse` (saturé à 3 documents, 4 avec le
   candidat n° 1) ; `tirzépatide + berbérine / picolinate de chrome` comme monographie de
   potentialisation (**aucun essai n'a randomisé ces combinaisons** : une carte du vide ne remplit
   pas dix sections, et `complements-amincissants` a déjà rendu ce service pour le rayon) ;
   `objectif : endurance / explosivité / prise de masse` (servis par `cafeine-ergogene`,
   `creatine`, `proteines-besoins-timing`). `objectif : performances sexuelles` est un gap réel,
   **non retenu ce tour-ci** : son profil (adultération PDE5, marché gris, contrôle du contenu réel
   des gélules) redirait la méthode de `complements-amincissants` et `peptides-gris`.

**Passe d'enrichissement du 2026-08-18** (corpus à 79 thèmes / 81 documents) : audit ciblé sur
**« la prise de masse maigre chez l'homme de plus de 60 ans »** (exercice, alimentation,
supplémentation, médicaments, marché gris), mené **par lecture intégrale de la prose** de
8 monographies — les 5 du versant nutrition/compléments (`creatine`, `proteines-besoins-timing`,
`vitamine-d`, `cafeine-ergogene`, `collagene`) et les 3 du versant pharmacologique
(`incretines-glp1`, `masse-maigre-sous-glp1`, `peptides-gris`) — doublé de deux balayages web
séparés, l'un sur exercice/protéines/suppléments, l'autre sur médicaments/marché gris. Cinq
décisions :

1. **Gap réel, et le corpus le désigne lui-même comme un dehors.** Le sujet n'existe qu'en
   fragments périphériques, chacun explicitement présenté comme incise ou perspective :
   `proteines-besoins-timing` définit la résistance anabolique en ouverture, donne le seuil de
   leucine relevé chez l'âgé et PROT-AGE dans **un paragraphe de sa section sécurité**, puis écrit
   que « le sujet vieillissant […] relève d'ailleurs d'une dose et d'un seuil qui lui sont
   propres » — il nomme le centre pour l'exclure ; `creatine` relègue le vieillissement en
   « front qui bouge » dans un unique paragraphe d'écosystème et renvoie vers une revue
   **externe** (Candow 2025) ; `vitamine-d` traite chutes et fractures de l'âgé en profondeur et
   ne dit **rien** de la masse ni de la force ; `cafeine-ergogene` n'en dit rien du tout (vérifié
   par lecture ET comptage) ; `collagene` ne couvre que l'os de la **femme** ménopausée. Absents
   du corpus entier : la sarcopénie comme entité clinique, l'entraînement en résistance comme
   intervention, le HMB, la testostérone, la pharmacologie des SARMs.
2. **Deux monographies, pas une — parce que les deux versants n'ont pas le même régime de
   preuve.** Côté exercice/nutrition : littérature mature, méta-analyses multiples et
   concordantes, effets modestes mais affirmables. Côté médicaments : le champ 2024-2026 est fait
   presque entièrement de **communiqués de promoteur non revus par les pairs** (QUALITY, COURAGE,
   EMBRAZE), et le seul essai publié en revue à comité de lecture — BELIEVE, *Nature Medicine*,
   5 mars 2026 — **ne mesure aucun critère fonctionnel**. Fondre les deux produirait un document
   qui hedge tout au même niveau.
3. **Deux moitiés de la pharmacologie musculaire sont DÉJÀ PRISES, ce qui resserre le 2e thème.**
   Les anticorps anti-myostatine/activine sont traités en profondeur par `masse-maigre-sous-glp1`
   (bimagrumab/BELIEVE, apitegromab/EMBRAZE, trévogrumab/COURAGE) ; les sécrétagogues de GH par
   `peptides-gris` (CJC-1295, MK-677, ipamoréline, tésamoréline comme étalon). Ne restent
   réellement libres que **la testostérone, les SARMs, la GH exogène et l'échec réglementaire de
   la pharmacologie sarcopénie**. Une 3e monographie « SARMs & marché gris de la musculation »
   n'est **pas** ouverte ici : elle redirait `peptides-gris`, et ne se justifierait qu'a posteriori
   si l'arbitrage du 2e run sacrifiait ces sections.
4. **Domaine `muscle-vieillissement` à créer — avec une réserve taxonomique explicite** (section
   dédiée en fin de fichier). Les deux thèmes créent le domaine **et son portail d'un seul coup**
   (le portail exige 2 thèmes), ce qui évite le défaut du 39e run où `performance-cognitive` est
   né à moitié.
5. **2e renvoi cassé du corpus, trouvé par la même heuristique et réparé le jour même** :
   `incretines-glp1` promettait « apports protéiques, entraînement en résistance sous déficit
   énergétique […] traité ailleurs dans ce corpus », et son écosystème citait « le thème consacré
   aux protéines et à la masse maigre en déficit calorique » — deux désignations que
   `masse-maigre-sous-glp1` dément frontalement (« la monographie consacrée aux besoins
   protéiques traite du sujet entraîné en surplus ou à l'équilibre énergétique, pas de la
   préservation sous déficit marqué », et la question de l'entraînement y reste ouverte, LEAN-PREP
   n'ayant qu'un protocole publié). Corrigé dans `manifest.json` puis rebuild — voir la note de
   réparation en fin de section `pharmacologie-metabolique`.

**Ordre de lancement** — mis à jour le 2026-08-26 (les 3 premiers sont FAITS) :

| # | thème | priorité | domaine |
|---|---|---|---|
| ~~1~~ | ~~`sarcopenie-exercice-nutrition`~~ | FAIT 2026-08-18 | `muscle-vieillissement` (domaine créé) |
| ~~2~~ | ~~`testosterone-homme-age`~~ | FAIT 2026-08-19 | `muscle-vieillissement` (portail ouvert) |
| ~~3~~ | ~~`nootropiques-vegetaux`~~ | FAIT 2026-08-26 | `performance-cognitive` (**portail ouvert**) |
| 4 | `cafeine-cognition-vigilance` | **haute** (tête de file) | `performance-cognitive` |
| 5 | `omega-3` | moyenne-haute | `complements-sante` |
| 6 | `acide-alpha-lipoique` | moyenne-haute | `complements-sante` |
| 7 | `beta-alanine-tampons` | moyenne | `nutrition-sportive` |
| 8 | `microdosage-psychedeliques` | moyenne | `performance-cognitive` |
| 9 | `nootropiques-panorama` | moyenne | `performance-cognitive` (**capstone : à lancer après les nos 3, 4 et 8**) |
| 10 | `magnesium`, `hydratation-electrolytes` | basses | — |

**Arbitrage assumé** : les deux thèmes muscle passent devant `nootropiques-vegetaux`, qui était en
tête depuis le 2026-08-15. Ils coûtent plus cher (deux runs au lieu d'un) et laissent
`performance-cognitive` à moitié né **deux tours de plus** — mais ils créent un domaine
**complet, portail inclus**, sur un gap plus large, et leur fil rouge est le mieux mesuré que ce
backlog ait proposé (voir la section du domaine). `nootropiques-vegetaux` garde sa priorité haute
et reste le run le moins cher pour refermer le chantier `performance-cognitive` :
**si le budget ne permet qu'un seul run, le lancer lui.**

## `nutrition-sportive`

(`creatine` : FAIT le 2026-08-08, retiré du backlog — 29e run /leanmonograph, **premier
thème hors IA** : GREEN direct, backstop 100 % propre (une première sur un run à 16
corrections). La doctrine de preuve santé, injectée en bloc dans le `subject`, a été
appliquée par le council : mythe de la charge « indispensable » corrigé sur RCT + position
ISSN, plage de rétention d'eau complétée (1-3 kg vs la seule borne 0,5-1 L), hedge sprints
« une seule méta-analyse vérifiée » exact ; l'unique rejet — une inversion arithmétique
« 116 % de moins » sur l'étude de marché Escalante 2022 — est corrigé et hedgé dans la
prose. 9/9 sections, 33 claims 16✓/16corr/1rej, 62 sources, 4 widgets (revue visuelle
faite ; financement industriel et rang mécanistique signalés dans leurs notes) ; 6,05M
tok / 86 agents / 2 h 07 en un seul run. Crée le méta `sante-nutrition` et le domaine
`nutrition-sportive` ; première `notice` réellement injectée dans `_site/`, vérifiée
avant `</main>`, `dist/` propre.)
(`proteines-besoins-timing` : FAIT le 2026-08-08, retiré du backlog — 30e run
/leanmonograph, 2e thème santé : GREEN direct, 9/9 sections, 36 claims 17✓/18corr/1rej,
65 travaux distincts, 3 widgets + 3 figures ; 6,03M tok / 87 agents / 2 h 31 en un seul
run. La doctrine de preuve santé a mordu plus loin que sur `creatine` : conflits d'intérêt
déclarés claim par claim (National Dairy Council et Dymatize sur Morton 2018, Meiji sur
Tagawa, Axiom Foods sur Moon 2020) et repris jusque dans la ligne source des figures ;
divergence des trois seuils (1,3 / 1,5 / 1,62 g/kg/j) discutée frontalement au lieu d'être
lissée. L'unique rejet — comparaison DIAAS athlètes végétariens/omnivores (Ciuris 2019) —
est single-source, hedgé dans la prose. **Backstop : 1 correction dure d'une CLASSE
NOUVELLE, l'ARGUMENT DU SILENCE** : la section sécurité affirmait un bénéfice « sans effet
rénal ou osseux délétère rapporté dans les essais inclus » en s'appuyant sur une
méta-analyse (Kim et al. 2016) qui ne suit QUE la composition corporelle — ni rein ni os
parmi les paramètres mesurés, soit une absence d'examen présentée comme une absence
d'effet. Le fait n'étant porté par aucun claim, et ses nombres étant courts ou en toutes
lettres, il échappait à la fois au council et à `lint.py`. ⚠️ **Réflexe pour les prochains
runs santé : sur toute tournure « sans X rapporté » / « aucun effet observé », vérifier que
le paramètre a été MESURÉ par la source, pas seulement non mentionné.**)
(`cafeine-ergogene` : FAIT le 2026-08-15, retiré du backlog — 37e run /leanmonograph, 9e thème
santé, 3e de `nutrition-sportive` dont il **crée le portail manquant** (parcours en gradation :
effet réel avec plafond → promesse créditée à la mauvaise variable → amplitude fabriquée par le
protocole). 12/12 sections, 47 claims 24✓/19corr/4rej, 82 sources, 3 widgets + 2 figures,
9 536 mots ; 7,30M tok / 104 agents / 3 h 20 en un seul run.

Trois enseignements, dont deux de fond :

1. **CLASSE D'ÉCHEC NOUVELLE — un rejet sur le SEUIL DE SOURCES jette aussi l'énoncé corrigé
   du juré.** `decideAudit` exige `holds+corrected >= 2` PUIS `sources >= 2` ; quand la seconde
   condition tombe, la correction produite par le juré n'est écrite nulle part et meurt dans sa
   `note`. L'auteur, aveugle aux claims rejetés, réécrit alors le fait depuis les NOTES de
   section — sans la correction. Deux erreurs de ce run viennent de là, dont une fausse
   attribution d'auteur (essai croisé de 2020 attribué à Guest alors qu'il est de Carswell et
   coll.) que `lint.py` ne pouvait pas voir : la tournure évitait de NOMMER Guest, et aucun
   chiffre n'était en cause. ⚠️ **Réflexe : après chaque run, lire les notes des jurés des
   claims rejetés en cherchant `holds=false` AVEC une correction — c'est le sous-ensemble le
   plus rentable du backstop.** Correctif de code envisageable, non appliqué : faire remonter
   le `corrected_statement` dans les notes transmises à l'auteur même sur un claim rejeté.
2. **La règle document-source est enfin DANS LE CODE** (commit `fix(council)`), après deux
   applications à la main (berberine, ce run). Branche unanime et fail-closed dans les 3
   workflows, champ `document_source` dans les schémas et prompts, exception écrite dans le
   `CLAUDE.md`, 9 cas × 3 workflows sous test avec mutation vérifiée. Critère de tri retenu :
   « ce document de référence dit X » → exception ; « un seul travail a trouvé X » → rejet
   maintenu et réserve conservée en prose. Sur ce run le partage était 2 contre 4.
3. **Note de mémoire FAUSSE corrigée** : « forcer `data-theme` en JS ne bascule pas les widgets,
   leurs faibles contrastes sont des artefacts » était inexact — tout bascule par `data-theme`
   (0 occurrence de `prefers-color-scheme` dans la charte). La vraie cause des mesures
   aberrantes est de MESURER DANS LE MÊME APPEL JS QUE LA BASCULE, donc en pleine transition
   CSS. Séparer bascule et mesure a fait tomber 19 « violations » à 4 réelles, dont un badge de
   widget à 2,16:1 bien réel. Restent ouverts 2 défauts de la charte partagée :
   `--bordeaux-bright` à 4,37:1 en sombre sur `.fcap-k`/`.xk` (les 77 documents) et la couleur
   de lien à 4,39:1 en clair.)
- **beta-alanine-tampons** (moyenne) — bêta-alanine/carnosine et bicarbonate : tampons
  intracellulaire/extracellulaire, efforts 1-4 min, paresthésies, méta-analyses.
- **hydratation-electrolytes** (basse) — déshydratation et performance (seuils réels vs
  folklore des 2 %), sodium, hyponatrémie d'effort, boissons de l'effort.

## `complements-sante`

(`collagene` : FAIT le 2026-08-12, retiré du backlog — 34e run /leanmonograph, 6e thème
santé : GREEN, 10/10 sections, 37 claims 21✓/9corr/7rej, 72 sources, 3 widgets + figures ;
6,55M tok / 95 agents / 3 h 24 en un seul run. **Crée le domaine `complements-sante`**, classé
entre `nutrition-sportive` et `pharmacologie-metabolique` — le méta santé se lit désormais en
gradation : nutrition de performance → complément en vente libre → médicament sur ordonnance.
Pas de portail : un `parcours` à une seule étape n'oriente personne, il viendra au 2e thème.

Trois enseignements, dont un de doctrine :

1. **Sur une littérature MONO-SOURCE, le seuil « ≥ 2 sources » devient le SEUL mécanisme de
   rejet — et il rejette des faits VRAIS.** Les 7 rejets de ce run portent tous le même motif,
   « 1 source indépendante » ; AUCUN ne porte sur l'exactitude, et six avaient reçu 1 à 3
   confirmations de jurés. En cause : les essais du collagène sont uniques, financés par
   l'ingrédientier, jamais répliqués par une équipe tierce (Praet 2019 sur la tendinopathie,
   l'essai pivot UC-II à 191 sujets). Taux de rejet 19 % contre 3 à 8 % sur les cinq runs
   santé précédents. Le pipeline se rattrape en aval : la prose garde ces essais avec la
   réserve « source unique, non corroborée » posée par le lint sur 5 passages.
   ⚠️ **Attendre le même profil sur `vitamine-d`, `omega-3`, `magnesium` — juger un run santé
   à la NATURE de ses rejets, jamais à leur nombre.**
2. **L'Audit-prose a attrapé une fausse attribution** (la classe d'erreur du 33e run) : une
   phrase citait des masses moléculaires « 500 Da / 15 000-50 000 Da / 3 000-5 000 Da » en les
   attribuant à une page qui ne les contient pas — vérifié par lecture directe de la source,
   valeurs réelles rétablies (>100 000 Da natif, 3 000-8 000 hydrolysat, <3 000 « faible poids
   moléculaire »). Le council avait par ailleurs RETOURNÉ un claim affirmant une « réplication
   indépendante par plusieurs équipes » sur l'UC-II : tous les essais relèvent de la même
   filiation industrielle (InterHealth, racheté par Lonza en 2016).
3. **Deux défauts de la charte PARTAGÉE corrigés, trouvés en revue visuelle** (corpus entier
   rebuildé, 73 documents, diff purement chromatique) : `--ink-faint` était sous AA sur TOUS
   les fonds en thème clair (3,61 sur blanc, 2,91 sur fond teinté) → `#5C697B` / `#8393A6`,
   porté à 4,50-5,58 ; et surtout **le correctif `--blue-deep` du 32e run était PARTIEL** — il
   ne visait que les titres, alors que les termes du glossaire portent la même encre et
   restaient à **1,13:1** en thème sombre depuis toujours (→ 7,52). ⚠️ **Reste ouvert** :
   `.xptr-kind` (badges de pointeurs), blanc sur `--blue-bright` éclairci en sombre, à 2,16 —
   mécanisme différent, un fond éclairci gardant une encre blanche.)
(`vitamine-d` : FAIT le 2026-08-13, retiré du backlog — 35e run /leanmonograph, 7e thème
santé : **GREEN au premier passage**, 10/10 sections, 40 claims 26✓/11corr/3rej, 88 sources,
4 widgets + 3 figures, verdicts 11 indications ; **5,97M tok / 95 agents / 2 h 38 — premier
run santé sous 6M**. **Crée le portail `complements-sante`** (2e thème du domaine), classé
AVANT collagene : la vitamine D est l'étalon méthodologique du rayon (association vs effet,
la fabrique du besoin par le seuil), le collagène l'autre régime de preuve (mono-source).

Profil de rejets inverse de collagene, comme anticipé : 3 rejets seulement (7,5 %), dont
2 mono-source mécaniques et 1 sur-généralisation réelle attrapée par le juré réfutation
(l'OR du sous-groupe croisé de Martineau 2017 attribué aux carencés en général) — la prose
rend d'elle-même la version corrigée, hedgée. Le backstop n'a corrigé AUCUN fait ; ses deux
seules retouches sont visuelles : 2 défauts sombres dans les widgets du thème, dont la
**3e incarnation du double rôle `--blue-deep`** (consommé comme encre par un widget, 1,01:1
sur le bandeau synthèse). ⚠️ `.xptr-kind` de la charte partagée reste à 2,16 en sombre —
défaut ouvert depuis le 34e run, corpus entier.)
- **omega-3** (moyenne) — EPA/DHA : triglycérides (démontré) vs événements cardio
  (REDUCE-IT vs STRENGTH), cognition, doses, oxydation des huiles.
- **magnesium** (basse) — carence réelle vs marketing, formes (citrate, bisglycinate,
  oxyde), sommeil/crampes/anxiété : tri par niveau de preuve.

### Acide alpha-lipoïque — `acide-alpha-lipoique` → `complements-sante`
**Verdict : gap réel (moyenne-haute), mais PAS où on l'attend.** Zéro occurrence dans les
76 documents. Le piège est de le ranger en amincissant : les méta-analyses donnent −1,27 kg
(Kucukgoncu 2017, *Obesity Reviews*) et −0,69 kg / −0,38 kg/m² (Namazi 2018, *Clin Nutr*), soit
exactement l'ordre de grandeur du CLA (−0,35), de la L-carnitine (−1,21) et du picolinate de
chrome (−0,50 à −1,1) **déjà jugés molécule par molécule** dans `complements-amincissants` — un
4e verdict en fraction de kilo n'apprendrait rien, la graduation et le verdict de catégorie sont
posés. L'angle qui vaut le run est ailleurs : c'est le rare complément dont la meilleure preuve
porte sur une **indication clinique étroite** (neuropathie diabétique périphérique), avec une
variable que le corpus n'a jamais traitée — **la voie d'administration décide de l'effet**
(IV vs orale vs séquentielle). Il s'assied à cheval sur la gradation du méta-domaine
(nutrition → complément libre → ordonnance) puisqu'il est délivré sur prescription en Allemagne.

> L'acide alpha-lipoïque (ALA, acide thioctique) : ce que la preuve établit indication par
> indication. Couvrir la neuropathie diabétique périphérique comme dossier principal — lignée
> ALADIN / SYDNEY / NATHAN 1, méta-analyses et network meta-analysis bayésienne comparant voies
> orale, intraveineuse et séquentielle, doses 600–1 800 mg/j, scores TSS/NIS et ce qu'un score
> symptomatique mesure réellement ; la dissociation entre effet aigu IV et effet oral au long
> cours ; la sensibilité à l'insuline et les marqueurs métaboliques ; le poids uniquement pour
> **situer** l'ordre de grandeur contre le seuil réglementaire des 5 %, pas pour refaire le
> verdict du rayon. Sécurité : vérifier le signal de **syndrome insulinique auto-immun**
> (hypoglycémies, allèle HLA-DRB1*04:06, séries japonaises et coréennes) — annoncé comme piste,
> à corroborer ou à écarter au sweep, ne pas l'affirmer sur une source unique. Traiter aussi le
> racémique vs R-énantiomère et le statut réglementaire dissocié (complément ici, médicament sur
> prescription en Allemagne). Délimitations : `complements-amincissants` a rendu le verdict
> minceur du rayon et posé la graduation FDA/GLP-1 — ne pas la refaire ; `vitamine-d` fournit le
> patron « verdict par indication » ; `berberine` le patron « mécanisme cellulaire ≠ effet humain ».
> Domaine : complements-sante.

## `pharmacologie-metabolique`

(`berberine` : FAIT le 2026-08-10, retiré du backlog — 32e run /leanmonograph, 4e thème
santé : GREEN après backstop, 10/10 sections, 40 claims 26✓/11corr/3rej, 69 sources,
3 widgets + 3 figures ; 6,66M tok / 94 agents / 3 h 06 en un seul run.
⚠️ **Classé dans `pharmacologie-metabolique` et NON dans `complements-sante` comme le
prévoyait ce backlog** : le domaine créé la veille par `incretines-glp1` l'annonçait déjà
dans son blurb (« les produits qui promettent de les remplacer ») et dans l'intro de son
portail (« ceux qui promettent de s'en dispenser »). `complements-sante` reste à créer par
le premier thème de santé/longévité (collagene, vitamine-d, omega-3, magnesium)
— créé depuis, par `collagene` le 2026-08-12.

Trois enseignements, dont deux de fond :

1. **2e trou dans la garantie « ≥ 2 sources indépendantes »**, détecté par `build.py` qui a
   refusé de valider : `docKeys` dédoublonne des travaux, mais PAS la répétition du même
   identifiant — deux jurés citant la même page sous deux titres différents produisaient deux
   clés `title:` distinctes, puis un seul `src:` id (`['src:27','src:27']`) sous un
   `audit_note` affirmant « 2 sources indépendantes ». Le même document REJETAIT deux claims
   auto-référentiels (fiches NCCIH) et en CONFIRMAIT deux autres par ce contournement.
   **Règle document-source adoptée** ; correctif appliqué aux 3 workflows (clé d'URL toujours
   posée + dédoublonnage des ids), prouvé par test sur le cas réel et non-régression.
2. **Classe d'erreur factuelle nouvelle — la fausse plage par agrégation de compartiments** :
   « la metformine élève l'AMPK de 63 à 97 % » n'était pas une plage mais deux mesures de
   compartiments différents (63 % en lysat total, 97 % dans les lysosomes), fusionnées.
   Invisible au lint : les deux nombres figurent dans la source. Corrigé en prose ET dans le
   widget, qui portait la même faute.
3. **Défaut de la charte partagée, trouvé en revue visuelle** : `--blue-deep` sert à la fois
   d'encre de titre (`h3`, `.part-band h2`) et de couleur de fond (`th`) ; assombri en thème
   sombre pour son rôle de fond, il rendait tous les titres illisibles (contraste 1,01:1).
   Corrigé dans `charte.css`, **corpus entier rebuildé** (71 documents, diff purement CSS) —
   contraste porté à 8,42:1.)

(`incretines-glp1` : FAIT le 2026-08-08, retiré du backlog — 31e run /leanmonograph,
3e thème santé et premier sur des MÉDICAMENTS SUR ORDONNANCE : GREEN après backstop,
**14/14 sections**, 52 claims 22✓/26corr/4rej, 111 sources, 5 widgets ; run interrompu
puis repris (`resume: true`), 5,25M tok / 68 agents / 3 h 39 pour la seule reprise.
Crée le domaine `pharmacologie-metabolique` et son portail — premier portail hors IA.

Trois leçons, dont deux nouvelles :

1. **La troncature du plan de sections est une décision d'édition prise par du code.**
   `workflow.js` coupait l'outline aux N PREMIÈRES sections *dans l'ordre du plan* :
   ici disparaissaient en silence la section sécurité (pourtant obligatoire par la
   doctrine), le rétatrutide (pourtant dans le titre) et le pivot du fil rouge.
   Contourné par `args.maxSections`, PAS corrigé sur le fond — le prompt de
   l'architecte lui promet un élagage « par matière » qui n'arrive qu'après.
   ⚠️ **Audit ouvert : 46 thèmes publiés sont pile à 9 sections.**
2. **NOUVEAU — le lint est aveugle par CONJONCTION de deux angles morts connus.**
   Il exige 2 pivots retrouvés, ou 1 seul d'au moins 4 caractères. La collision
   numérique (24e run) blanchit assez de pivots pour faire tomber le compte sous 2,
   et ce qui survit est trop court pour valoir seul (12e run). Trois rejets affirmés
   nus dans la prose sont ainsi restés totalement invisibles : « 0,8 » et « 7,1 »
   isolés, « 120 » blanchi. Ni l'un ni l'autre mécanisme seul n'aurait suffi.
3. **NOUVEAU — un quota WebSearch épuisé FABRIQUE des faux rejets.** Le juré soutien
   d'un claim a voté `false` en écrivant lui-même « WebSearch épuisé », « par prudence
   sur l'indépendance, non sur l'exactitude ». La 2e source manquante était citée dans
   la bibliographie du document. Poser `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`
   AVANT le lancement — un run dense en consomme ~300.)
(`complements-amincissants` : FAIT le 2026-08-11, retiré du backlog — 33e run /leanmonograph,
5e thème santé : GREEN après backstop, 10/10 sections, 40 claims 17✓/21corr/2rej, 96 sources,
1 super-widget ; 6,86M tok / 106 agents / ~4 h 10 en DEUX runs. Classé 3e du parcours de
`pharmacologie-metabolique`, après `berberine` : le domaine se lit désormais en gradation
descendante — l'effet établi sur ordonnance, le substitut annoncé, puis le rayon entier où
l'effet devient indiscernable et où la question bascule vers le réglementaire et l'adultération.

Trois enseignements, dont un de fond :

1. **Classe d'erreur factuelle NOUVELLE — la fausse indépendance par scission de source**,
   symétrique exact de la fausse plage par agrégation (32e run). La prose donnait « deux séries
   indépendantes » sur l'hépatotoxicité du thé vert — DILIN à 42 j de latence, et « une revue
   distincte publiée en 2022 par Grajecki » à 72 j / 15-448 j / 35 % / 3 greffes — puis en tirait
   un argument : « deux recrutements différents, pas deux mesures du même échantillon ». C'était
   le MÊME corpus de 40 cas compté deux fois : les chiffres du second bloc sont verbatim
   l'abstract de Hoofnagle et al. 2021 (Hepatology, PMID 32892374), le papier DILIN lui-même,
   et le « 42 jours » vient de la fiche LiverTox qui le résume. Tout le pipeline était aveugle
   par construction : les nombres sont EXACTS, seule leur attribution est fausse — le lint
   compare des valeurs, jamais un couple (valeur, travail), et aucun claim ne portait le fait.
   L'Audit-prose l'a flairé puis classé « hors périmètre » et laissé partir au build. Corrigé à
   la main après vérification aux deux sources. ⚠️ **Réflexe : sur toute prose affirmant
   l'indépendance de deux séries, comparer leurs EFFECTIFS et leurs valeurs secondaires — ici
   35 % / 8 % / 3 greffes étaient identiques des deux côtés. Et un doute d'attribution soulevé
   par l'Audit-prose n'est JAMAIS hors périmètre : c'est plus grave qu'un chiffre faux.**
2. **Le mode d'échec « tranche d'Author vide » a récidivé** (déjà vu au 28e run) : la tranche 1
   a rendu `sections: []` avec un `summary` complet et bien formé, en UN SEUL tour — ni
   rate-limit ni troncature, et le schéma l'accepte puisqu'un tableau vide est valide. Réparé
   par `resume: true` (checkpoints du skill), surtout PAS par `resumeFromRunId` qui aurait
   rejoué la tranche fautive depuis le cache à l'octet près. Coût du premier run non perdu :
   le council entier (40 claims, 97 sources) était en checkpoints. ⚠️ **Le workflow paie
   pourtant les 3 tranches suivantes avant de détecter le trou à l'assemblage — un contrôle
   des ids après chaque tranche supprimerait le gaspillage ET la reprise.**
3. Deux défauts mineurs relevés hors périmètre, non corrigés : `--ink-faint` sur blanc donne
   **3,61:1** en micro-texte (renvois de glossaire, libellés de widget) — sous le seuil AA,
   défaut de la charte partagée donc des 74 documents ; et `build.py:86` imprime `len()`,
   un nombre de CARACTÈRES étiqueté « o » (octets) — 4 726 d'écart sur ce document, soit les
   accents. Enfin, 0 figure ici contre 3 pour `berberine` : document visuellement plus maigre
   que ses voisins.)

(`masse-maigre-sous-glp1` : FAIT le 2026-08-15, retiré du backlog — 38e run /leanmonograph,
10e thème santé, 4e de `pharmacologie-metabolique` : GREEN après backstop, 9/9 sections,
34 claims 22✓/10corr/2rej (20/10/4 au council, avant re-adjudication), 75 sources, 4 widgets +
2 figures, tableau de verdicts à 7 substances, ~7 250 mots ; **6,28M tok / 87 agents / 2 h 24 en
un seul run, 0 erreur d'agent — sous la fourchette annoncée** (6-8M / 3 h-3 h 45). Classé **2e du
parcours**, pas en fin de file : il continue littéralement la section « Ce qui est perdu »
d'`incretines-glp1`, dont il répare le renvoi cassé. Le domaine se lit désormais en deux temps —
l'effet établi puis la composition de cet effet — avant la descente déjà en place. Blurb du
domaine et intro du portail élargis à l'axe qui manquait : ce qu'on prétend AJOUTER au traitement.

Trois enseignements, dont deux de fond :

1. **L'heuristique de gap la plus fiable trouvée à ce jour, et elle est réutilisable** : ce thème
   est né d'un **renvoi vers un document inexistant**. `incretines-glp1` refermait sa section « Ce
   qui est perdu » sur « apports protéiques, entraînement en résistance — relève du versant
   nutritionnel, traité ailleurs dans ce corpus et non repris ici », alors que ce n'était nulle
   part. ⚠️ **Chercher les autres** : balayer le corpus sur « traité ailleurs », « relève de »,
   « non repris ici », puis VÉRIFIER PAR LECTURE que la cible existe.
2. **Les 4 rejets du council portaient TOUS le seuil de sources, AUCUN l'exactitude** — 2 à 3
   jurés tenaient chaque énoncé, zéro ne le réfutait ; les trois passages étaient dans la prose,
   affirmés, dont deux sans attribution. Trois réparations, par ordre de généralité :
   **(a) la seconde source était citée PAR l'article source** (Willoughby 2018, en introduction de
   Look 2025) — ⚠️ réflexe neuf : sur un rejet « 1 source », lire la BIBLIOGRAPHIE de la source
   retenue, le juré cherche sur le web et pas dans les références ; **(b) exception
   document-source ratée par manque d'unanimité** — un juré sur deux avait coché `document_source`,
   l'autre l'avait écrit en prose dans sa note, et la branche fail-closed a refusé de s'ouvrir
   (code correct, c'est le prompt du juré qui laisse la qualification s'exprimer en texte libre) ;
   **(c) un claim composite se répare en le SCINDANT** — la part corroborable devient le claim, la
   part mono-source reste en prose sous attribution explicite à son essai.
   Un 4e rejet est maintenu à raison (énoncé d'exhaustivité, qu'une source unique ne peut établir),
   et un cinquième cas est resté rejeté après trois tentatives infructueuses de second travail :
   attribution en prose plutôt que corroboration fabriquée.
   ⚠️ **`lint.py` était vert et ne prouvait rien** : deux de ces énoncés n'ont ni chiffre ni nom
   propre distinctif, et les pivots du troisième sont blanchis par collision avec des claims
   retenus — la conjonction d'angles morts du 31e run, sur un run par ailleurs impeccable.
3. **Piège de MESURE du contraste, classe nouvelle** : une remontée d'arbre qui ne lit que
   `backgroundColor` rate un bandeau peint en `linear-gradient`, file jusqu'au `body` clair et
   sort un 1,05:1 sur un titre parfaitement lisible. Première mesure : 5 violations dont **4
   fausses**. Après prise en compte du premier arrêt de couleur du dégradé : 1 seule réelle
   (micro-texte de widget à 4,29:1 sur fond teinté), corrigée, puis 0 violation en clair ET en
   sombre. Les 4 widgets du run ne posent aucun fond en dur et portent tous leur règle sombre.

**Bon comportement à reconduire mot pour mot** : les pistes issues de la recherche préliminaire
étaient passées dans `args.subject` comme « à corroborer en source primaire, jamais des faits — si
une piste ne se corrobore pas, la retirer, ne pas la sauver ». La consigne a tenu, et le pipeline a
corrigé une contamination venue du brief : l'essai s'appelle **EMBRAZE**, pas EMBRACE — le document
signale de lui-même que la graphie qui circule dans les reprises est fausse.)

**RÉPARATION du 2026-08-18 — 2e renvoi cassé du corpus, dans `incretines-glp1`.** Le 38e run avait
réparé le premier (une section qui renvoyait vers un document inexistant) ; l'audit du 2026-08-18 a
trouvé le second, dans le **même** document et par la **même** heuristique. Deux passages
promettaient une couverture que le corpus ne fournit pas :

- section « Ce qui est perdu » : « apports protéiques, entraînement en résistance sous déficit
  énergétique — relève du versant nutritionnel, **traité ailleurs dans ce corpus** et non repris
  ici » ;
- section écosystème : « le thème consacré aux protéines et à **la masse maigre en déficit
  calorique** » — désignation d'un thème qui n'existe sous ce nom nulle part.

Les deux sont démentis par `masse-maigre-sous-glp1`, publié **après** : il écrit que
`proteines-besoins-timing` « traite du sujet entraîné en surplus ou à l'équilibre énergétique, pas
de la préservation sous déficit marqué », et conclut que la question de l'entraînement reste
ouverte (LEAN-PREP n'a qu'un protocole publié, pas de résultat). Le renvoi n'était donc pas
seulement périmé, il **sur-vendait** : il annonçait une réponse là où le corpus n'a qu'une question
documentée.

Réparé dans `manifest.json` seul, puis `build.py` + `build_site.py` (95 tests verts, la phrase
fautive absente du `dist/`) : les deux passages nomment désormais le voisin réel **et sa
conclusion négative**. `sections_draft.json` et `.leanmonograph/prose.json` **délibérément non
touchés** — ce sont les artefacts du run d'origine, pas la source du build ; les réécrire
falsifierait la trace du run sans rien changer au document publié.

⚠️ **L'heuristique reste ouverte, et elle a maintenant deux prises sur deux.** Balayer le corpus
sur « traité ailleurs », « relève de », « non repris ici », « traité par ailleurs » — puis vérifier
**par lecture** que la cible existe *et* qu'elle dit ce que le renvoi promet. Le second point est
neuf : ici la cible existait (`proteines-besoins-timing`), c'est son **contenu** qui ne
correspondait pas.

---

## `performance-cognitive` — domaine À CRÉER (proposé le 2026-08-15)

**Verdict : le plus gros trou du méta-domaine santé.** Trois arguments convergents : (1) le label
du méta-domaine promet déjà « Santé, nutrition & **performance humaine** », or la performance y est
exclusivement physique ; (2) couverture nulle vérifiée par lecture (cf. passe du 2026-08-15,
point 3) ; (3) **la méthode est déjà éprouvée dessus** — la section « Cerveau et cognition » de
`creatine` contient en miniature tout ce que ce domaine exige : refus d'allégation par l'EFSA,
double comptage dans les méta-analyses pivots (sous-tests corrélés traités comme observations
indépendantes), effet qui change de signe selon la métrique (temps de réponse vs précision), et
surtout la thèse de **l'effet de circonstances** — le bénéfice n'apparaît que sur cerveau
contraint (privation de sommeil), pas sur sujet sain reposé. Elle sert d'ancrage et de porte
d'entrée, pas de couverture.

- **Paramètres proposés** : id `performance-cognitive`, label « Performance cognitive », blurb
  « Ce que les essais mesurent réellement quand on prétend augmenter l'attention, la mémoire ou
  la vigilance — molécule par molécule, tâche par tâche. » Classé après `nutrition-sportive`
  (performance physique → performance cognitive) et avant `complements-sante`.
- ⚠️ **Ne pas créer le domaine à vide** : il naît avec son premier thème (`/arrange` ne crée jamais
  un domaine vide), et le portail exige un 2e thème — donc **deux runs** pour qu'il existe
  pleinement. Arête à poser dès le 1er thème : `creatine` → section « Cerveau et cognition ».

(`nootropiques-stimulants-prescrits` : **FAIT le 2026-08-15**, retiré du backlog — 39e run
/leanmonograph, 11e thème santé, **crée le domaine `performance-cognitive`**. 11/11 sections,
42 claims 24✓/9corr/9rej, 52 sources, 3 widgets (aucun fond clair en dur). Coût réel **9,3M tok /
~5 h 30 / 130 agents**, très au-dessus de la fourchette : deux réparations post-build en sont la
cause entière. Le fil rouge de `creatine` est bien généralisé — l'effet est *conditionnel* à la
difficulté de la tâche, à la ligne de base et à l'état du cerveau — et la section « Ce qu'on croit
ressentir, ce qu'on mesure » est le meilleur apport du document : l'écart le mieux documenté de
cette littérature n'oppose pas la molécule au placebo mais la performance mesurée à la performance
ressentie.

**Trois classes d'échec nouvelles, toutes découvertes APRÈS un `build.success: true`** — c'est le
vrai rendement de ce run, détaillé en mémoire :
1. **Un faux rejet coûte une SECTION, pas un fait.** L'élagage déterministe coupe toute section
   sous 2 claims retenus (`SECTION_CLAIM_QUOTA`). Un claim que les deux jurés tenaient, rejeté
   faute d'une 2e source, a fait tomber « Quand la complexité de la tâche retourne le verdict » —
   la 1re des trois conditions du fil rouge. Un ré-audit ciblé (1 agent) a trouvé la vraie 2e
   source en lisant le texte intégral d'une primaire citée par la revue, **et corrigé une erreur
   de fond au passage** (le sous-groupe *localise* l'effet, il ne le révèle pas).
   Traces qui trahissent la perte : anaphore sans antécédent, entrée de glossaire orpheline.
2. **Le compte de sections annoncé est un proxy.** Le workflow a rapporté « 11/11 retenues » alors
   que le manifeste écrit par Compose n'en avait que 10. Compter sur le HTML (`<h3>`).
3. **`prose.json` est PRÉ-Audit-prose** : y auditer les rejets fait re-signaler du déjà corrigé
   (j'y ai ajouté une réserve redondante, retirée depuis). Auditer le manifeste ou le dist.

✅ **Portail `performance-cognitive` CRÉÉ le 2026-08-26** par le 2e thème du domaine,
`nootropiques-vegetaux` — voir son entrée ci-dessous. ⚠️ L'arête `creatine` → section « Cerveau et
cognition » **ne peut pas être posée comme arête** : `portal.py` refuse tout slug hors du domaine
dans `parcours`, `aretes` et `delimitations` (lignes 89 et 111), et `creatine` appartient à
`nutrition-sportive`. Un renvoi inter-domaines n'a qu'une forme légale : une phrase de l'`intro`,
sans slug — c'est ce qui a été fait. **À retenir pour tout backlog** : ne plus écrire « arête à
poser » vers un thème d'un autre domaine, le code l'interdit par construction.)

(`nootropiques-vegetaux` : **FAIT le 2026-08-26**, retiré du backlog — 42e run /leanmonograph,
14e thème santé, **2e thème de `performance-cognitive` : il crée le portail du domaine** et referme
le chantier ouvert au 39e run. 11/11 sections retenues (plan à 11 entrées, **aucune troncature** —
le plafond réel est `MAX_SECTIONS=16` depuis le 2026-08-10, le `SKILL.md` du lean annonce encore 9 :
doc périmée, à corriger). 43 claims **21✓ / 21 corrigés / 1 rejeté** après backstop (le council avait
rendu 19/21/3), 93 sources, 3 widgets, ~10 300 mots. Coût **8,0M tok / 101 agents / 3 h 21** — dans
la fourchette annoncée (5-8M, 4-7 h) et **sous l'estimation basse en durée**. Contraste : 0 violation
en clair, 0 réelle en sombre.

**Le fil rouge a tenu sans être forcé** — et c'est le council qui l'a empêché de déraper : le lien
« essais négatifs parce que non financés par Schwabe » a été **corrigé en facteur plausible parmi
d'autres**, aux côtés de la taille d'échantillon, de la durée et de la population. Le garde-fou
« le fil rouge n'est pas une thèse à défendre », écrit dans le brief, s'est révélé opérant.

**Les 3 rejets valaient chacun un traitement différent — c'est le rendement de ce run** :
1. `claim:1` (spécification Ph. Eur. d'EGb 761) — **faux rejet** : l'énoncé décrit une **NORME**,
   `document-source` par nature. Ré-adjugé à la main. Les jurés n'ont pas coché `document_source`
   probablement parce que le claim était **composite** (spécification + constat EMA sur les ≈ 30 %
   du bilan massique) : un claim qui mélange un contenu de document et un énoncé analytique tombe
   dans l'angle mort de l'exception. **Piste pour le skill** : détecter les claims composites avant
   le council, ou demander au juré de qualifier `document_source` par MORCEAU.
2. `claim:8` (enquête du procureur de New York) — **faux rejet par carence** (0 confirmation,
   0 réfutation : le juré n'avait pas retrouvé un communiqué officiel pourtant en ligne).
   Ré-adjugé à la main, document-source également.
3. `claim:17` (méta-analyse BJPsych Open 2025) — **rejet JUSTE**, conservé : résultat empirique
   mono-source, que l'exception ne couvre pas. Chiffres revérifiés exacts, réserve « source unique,
   non corroborée » maintenue en prose. **La leçon n'est donc pas « les rejets sont faux » mais
   qu'ils ne sont pas de la même espèce** — un rejet se juge sur la NATURE de ce qu'il rejette.

**Classe d'erreur nouvelle : la réserve fausse par excès de prudence.** L'Audit-prose a vérifié les
3 claims rejetés, les a trouvés EXACTS en primaire, et — ne pouvant pas ré-adjuger — a ajouté à
chacun « (source unique, non corroborée) ». Sur `claim:17` c'est le traitement correct ; sur les
deux autres, **la réserve était fausse** : elle présentait une norme de pharmacopée et un document
officiel comme des affirmations fragiles. Corrigé en « spécification pharmacopéique / avis d'agence /
communiqué officiel : source unique **par nature** ». **Réflexe** : quand l'Audit-prose hedge un
claim rejeté, vérifier si la bonne réponse n'était pas la ré-adjudication document-source — hedger
un fait réglementaire l'affaiblit à tort.

**Ce qui a bien tourné, et qui avait échoué au 41e run** : l'Audit-prose a tourné **avec** son
moteur de recherche (19 chiffres de prose vérifiés en primaire, `fixed=0`, aucun resté douteux),
et le quota WebSearch n'a pas été épuisé. Vérifications indépendantes au backstop : GEM (523
démences, 277 ginkgo / 246 placebo, HR 1,12 [0,94-1,33] et Alzheimer 1,16 [0,97-1,39]), GuidAge
(2854 participants, HR 0,84), EFSA (4 637 allégations / 341 avis) — **tous exacts**.

**Zéro renvoi cassé**, alors que le risque était maximal (trois voisins du domaine encore non
publiés). L'interdiction explicite dans le `subject` — « verdict autonome ou rien, jamais "traité
ailleurs" » — a tenu de bout en bout : les 2 occurrences de « dans ce corpus » désignent l'une le
corpus d'ESSAIS, l'autre un document réellement publié.)

### Nootropiques végétaux — `nootropiques-vegetaux` → `performance-cognitive`
**Verdict : gap réel (moyenne) — ouvre le portail du domaine.** Le verdict de rayon, format
`complements-amincissants` mais bien moins cher (moins de molécules). Ginkgo est le cas d'école :
deux grands essais négatifs (GEM, GuidAge) contre un marché qui n'a pas bougé. ⚠️ Profil de rejets
attendu **identique à `collagene`** : essais uniques, souvent financés par l'ingrédientier, jamais
répliqués par une équipe tierce — juger le run à la **nature** de ses rejets, jamais à leur nombre.

> Les nootropiques d'origine végétale au tamis des essais : bacopa monnieri, ginkgo biloba,
> rhodiola rosea, ashwagandha (et panax ginseng). Molécule par molécule : ce qui a été mesuré, sur
> quelle population, avec quel comparateur et quelle taille d'effet. Couvrir le contre-exemple du
> ginkgo (grands essais de prévention négatifs vs allégations de rayon), la standardisation des
> extraits — un extrait n'est pas la plante, et deux extraits ne sont pas le même produit —, les
> allégations refusées par l'EFSA comme instrument de lecture, l'adultération et le contenu réel
> des gélules, et la question de l'indépendance des essais (financement par l'ingrédientier).
> Délimitations : `complements-amincissants` donne le patron du verdict de rayon et les outils de
> lecture d'une méta-analyse (I², analyse de sensibilité) ; `collagene` donne le patron de la
> littérature mono-source. Domaine : performance-cognitive.

- **cafeine-cognition-vigilance** (moyenne) — le rehausseur cognitif le plus consommé au monde,
  et `cafeine-ergogene` ne le traite PAS (0 occurrence de « cognition »/« cognitif » dans ses
  12 sections). Vigilance, dette de sommeil, sevrage et effet de restauration (le buveur régulier
  retrouve-t-il seulement sa ligne de base ?), caféine + L-théanine, siestes caféinées.
  ⚠️ **Ne lancer qu'avec la frontière écrite d'avance dans le brief** : pharmacocinétique, CYP1A2,
  habituation et sécurité sont déjà rédigés chez le voisin ergogène.
- **microdosage-psychedeliques** (moyenne) — littérature RCT désormais réelle et majoritairement
  négative une fois l'insu tenu (essais auto-aveuglés à grande échelle) : l'écart promesse/preuve
  est énorme et le sujet très demandé. Exige la doctrine santé au pied de la lettre.
- **neurostimulation-tdcs** (basse) — vrai gap, excellent matériau de crise de réplication, mais
  c'est un dispositif et non un produit de rayon : moins homogène avec le méta-domaine.

### Panorama du rayon nootropique — `nootropiques-panorama` → `performance-cognitive`
**Verdict : candidat de FORMAT, ajouté le 2026-08-19 sur demande explicite.**
**Annoté le 2026-08-26** (question posée : « Arcalion ou Noopept mériteraient-ils une monographie
dédiée ? »). Réponse : **non, et ce bloc est leur place** — corpus revérifié, 0 occurrence de
sulbutiamine, Arcalion, noopept, omberacetam et racétams dans les 82 thèmes (seul faux positif :
*paracétamol* dans `structured-extraction-llm`). Aucune des deux ne porte 9-13 sections vérifiables :
noopept parce que ses données humaines sont de petits essais russes d'un même laboratoire — les
claims d'efficacité tomberaient par carence RÉELLE, pas par prudence ; sulbutiamine parce que son
dossier exploitable tient en ~5-8 études. Les deux enrichissements ci-dessous (SMR et RCT
sulbutiamine ; analyses de contenu réel) sortent de cette vérification. Le document-index du
domaine : lister **TOUT** ce qui est allégué améliorateur des performances cognitives au sens
large — y compris ce que le corpus traite déjà ou prévoit de traiter sous ce même angle, alors
rappelé en quelques lignes (verdict + renvoi), jamais re-déroulé. Inventaire de départ : la page
Wikipédia « Nootrope » (fr) — **valeur d'inventaire uniquement, zéro valeur de source** ; chaque
substance est à instruire en source primaire. Couverture corpus vérifiée le 2026-08-19 par grep de
localisation puis lecture du contexte des 3 seuls documents qui matchaient : hors les rappels
listés dans le prompt, **aucune** des substances n'apparaît nulle part (racétams, donneurs de
choline, Hydergine, lévétiracétam, pitolisant, mémantine, anticholinestérasiques, nicotine,
tyrosine, vasopressine, fluorénol, tolcapone : 0 occurrence).

⚠️ **Deux dérogations assumées, à ne pas laisser passer en silence :**
1. La règle « une monographie par objectif ne se justifie que si aucune molécule seule ne porte
   l'objectif ET que le corpus n'a aucune couverture » n'est **pas** satisfaite — ici le format
   EST la valeur : une carte complète du rayon, graduée par niveau de preuve, dont la profondeur
   par substance est inversement proportionnelle à la couverture ailleurs.
2. Le précédent `complements-amincissants` avertit que multiplier les molécules multiplie les
   attributions à vérifier (run le plus cher du corpus, classe d'erreur « fausse indépendance par
   scission de source »). Tenir le budget par un quota strict : les substances sans donnée humaine
   se traitent en UNE LIGNE du tableau de verdicts, jamais en section.

⚠️ **À lancer en DERNIER des candidats `performance-cognitive`** (après `nootropiques-vegetaux`,
`cafeine-cognition-vigilance`, `microdosage-psychedeliques`) : ce document rappelle les verdicts
de ses voisins, donc chaque voisin manquant au lancement devient soit un renvoi cassé —
l'anti-pattern le mieux documenté du corpus, deux prises sur deux — soit un mini-verdict que la
monographie dédiée devra ensuite contredire ou dupliquer. S'il devait être lancé avant eux :
écrire les entrées concernées comme verdicts autonomes, et **interdire toute formule « traité
ailleurs » ou « couverture à venir »**.

> Le rayon nootropique au complet : tout ce qui est vendu, prescrit ou détourné avec une promesse
> cognitive, en un catalogue raisonné où chaque substance reçoit un verdict gradué par sa
> meilleure preuve. Fil rouge double : (1) le rayon est défini par l'ALLÉGATION, jamais par la
> preuve — le même mot « nootrope » couvre des médicaments à AMM, des molécules de marché gris et
> des composés sans aucune donnée humaine ; (2) l'origine du mot lui-même — Giurgea (UCB) le forge
> en 1972 POUR le piracétam, et les critères qu'il pose (améliorer sans stimuler ni sédater, être
> quasi atoxique) ne sont remplis par à peu près rien de ce que le rayon vend depuis. Structure
> par familles pharmacologiques, PAS par substance (patron `complements-amincissants` : sections
> de famille + super-widget tableau de verdicts couvrant TOUTES les entrées) :
> **racétams** — piracétam en dossier principal (AMM européenne, SMR faible, déconseillé par
> Prescrire, warning letters FDA côté compléments US : même molécule, trois statuts ; Cochrane sur
> le déclin cognitif ; l'essentiel de la littérature porte sur des populations atteintes — 
> l'allégation d'augmentation chez le sujet sain est une extrapolation quasi jamais testée),
> aniracétam, oxiracétam, pramiracétam, néfiracétam, coluracétam, rolziracétam, cébaracétam
> (pour la plupart : une ligne), noopept (littérature russe mono-source — le nommer comme tel),
> et le **lévétiracétam** comme cas inverse fascinant : antiépileptique à part entière (Keppra,
> étiracétam = son racémique) suspecté d'effets cognitifs indésirables à dose pleine, testé à
> BASSE dose dans le MCI amnésique (programme AGB101 / HOPE4MCI) — vérifier l'issue réelle de ces
> essais en primaire.
> **Éveillants et dopaminergiques** — modafinil, armodafinil, méthylphénidate, amphétamines :
> RAPPEL de `nootropiques-stimulants-prescrits` (verdict en deux phrases, renvoi, ne rien
> re-dérouler — son toolkit SMD/domaines/double comptage sert de méthode commune à tout le
> document) ; adrafinil (le précurseur historique, retiré du marché français — instruire le
> pourquoi) ; sulbutiamine (Arcalion : AMM française « asthénie fonctionnelle », service médical
> rendu à vérifier — **aucun avis de la Commission de la transparence retrouvé au 2026-08-26** :
> instruire en primaire (BDPM, HAS) l'hypothèse qu'il n'y en a pas, plutôt que de chercher un
> niveau de SMR ; un RCT réel existe et vaut mieux qu'une ligne — Loo & Poirier, 600 mg/j,
> 8 semaines, multicentrique, double aveugle contre placebo, inhibition psycho-comportementale de
> l'épisode dépressif majeur **sous clomipramine** : population atteinte et add-on, à ne surtout
> pas lire comme une preuve d'augmentation chez le sain ; détournement étudiant) ;
> pitolisant (Wakix, mécanisme histaminergique H3) ;
> fluorénol (données précliniques Cephalon uniquement — une ligne) ; L-Dopa et tolcapone (études
> de mémoire chez le sain : petites, anciennes, à corroborer) ; nicotine — le dossier sérieux du
> lot hors ordonnance : vraie littérature RCT (attention soutenue, amorçage chez le MCI — essai
> de Newhouse), à séparer absolument de la question tabac/vapotage et de la dépendance.
> **Cholinergiques et médicaments Alzheimer détournés** — donépézil, rivastigmine, galantamine
> (= Reminyl), mémantine, tacrine (retirée, hépatotoxicité) : l'angle est le DÉTOURNEMENT chez le
> sujet sain ou « inquiet de sa mémoire » — que montrent les essais chez le non-dément ? ;
> huperzine A — alcaloïde purifié d'une mousse, tranché ICI et non dans `nootropiques-vegetaux`
> (essais chinois, qualité méthodologique à documenter) ; DMAE et centrophénoxine (efficacité non
> démontrée — l'écrire) ; **dihydroergotoxine (Hydergine)** en cas d'école réglementaire : parmi
> les médicaments les plus vendus au monde dans les années 1980, méta-analyses décevantes,
> déremboursements — instruire la trajectoire complète.
> **Peptides et hormones** — semax, selank : `peptides-gris` tient déjà leur versant réglementaire
> (vote 503A) — le rappeler, et instruire ICI leur dossier d'efficacité cognitive (littérature
> russe, mono-source) ; vasopressine et analogues (études de mémoire des années 1980, jamais
> confirmées) ; tyrosine (littérature militaire : stress, froid, privation — l'effet est de
> PRÉSERVATION sous stresseur, pas d'augmentation — bien poser cette distinction).
> **Divers et vitamines** — sunifiram, suritozole (aucune donnée humaine : une ligne chacun,
> assumée comme carte du vide) ; vitamines B et homocystéine (grands essais négatifs — VITACOG et
> suite) ; oméga-3 : selon l'état du backlog au lancement, rappel du thème dédié ou verdict
> autonome. RAPPELS transverses obligatoires : créatine (section « Cerveau et cognition » de
> `creatine` : effet conditionnel à l'état du cerveau), caféine/L-théanine et végétaux
> (bacopa, ginkgo, rhodiola, ashwagandha, ginseng) et microdosage : renvois aux monographies
> dédiées si publiées — sinon verdict autonome sans promesse de couverture. Délimitations
> strictes : ne PAS re-dérouler le 39e run (trois molécules, mesure, usage détourné, régulateur) ;
> ne pas retraiter l'adultération générique (`peptides-gris`, `complements-amincissants` la
> portent) — la citer sur les poudres de racétams du marché gris : **ces analyses de contenu réel
> existent** (vérifié le 2026-08-26), et ce sont les deux meilleures entrées du dossier gris —
> (1) Cohen et al., *Neurology Clinical Practice* 2020, « Five Unapproved Drugs Found in Cognitive
> Enhancement Supplements » : 10 produits analysés, **omberacetam jusqu'à ~40 mg par prise
> recommandée, soit ≈ 4× la dose pharmaceutique typique de 10 mg**, aniracétam ~502 mg, plus
> phénibut, vinpocétine et picamilon détectés sans être déclarés — et des ingrédients déclarés
> non détectés ; (2) Jędrejko et al., *Drug Testing and Analysis* 2023, revue des ingrédients non
> autorisés des compléments « nootropiques » (histoire, pharmacologie, prévalence, réglementations
> internationales, potentiel dopant). ⚠️ **Piège d'indépendance connu du corpus** : le papier
> Cohen est repris par au moins six médias (AAN, Harvard Health, Healio, STAT, Medscape,
> Neuroscience News) — la reprise de presse n'est pas une seconde source ; corroborer par un
> travail distinct, pas par un article qui raconte celui-là. Pilier document-source du même
> dossier : page FDA « Vinpocetine in Dietary Supplements » (ne répond pas à la définition
> d'ingrédient alimentaire ; avertissement grossesse du 2019-06-03), warning letters FDA aux
> vendeurs de piracétam, notice ANSM d'Arcalion. Public : lecteur exigeant non
> spécialiste. Doctrine de preuve santé
> (`docs/evidence-sante.md`) à recopier intégralement dans le brief ; s'attendre à un profil de
> rejets type `collagene` en plus marqué (mono-source russe, essais anciens jamais répliqués) —
> juger le run à la NATURE de ses rejets. Domaine : performance-cognitive.

---

## `muscle-vieillissement` — domaine À CRÉER (proposé le 2026-08-18)

**Verdict : gap réel et large, à couvrir en DEUX thèmes qui créent le domaine et son portail.**
Couverture nulle vérifiée par lecture intégrale de 8 monographies (cf. passe du 2026-08-18) : les
documents existants dessinent les bords du sujet sans jamais en occuper le centre, et deux d'entre
eux le désignent explicitement comme un dehors.

**Le fil rouge — le mieux mesuré que ce backlog ait proposé, et il est commun aux deux thèmes :
la dissociation entre la masse et la fonction.** Toutes les molécules déplacent de façon fiable
le compartiment que le **SDOC (2020) a EXCLU de la définition de la sarcopénie**, précisément
parce que la masse maigre en DXA ne prédisait pas les événements incidents, là où force de
préhension et vitesse de marche les prédisent. L'entraînement en résistance fait exactement
l'inverse : gain de masse négligeable, gain de force et de performance large. Et le
contre-exemple est parfait, à l'intérieur d'une même molécule : la testostérone augmente la
densité minérale osseuse trabéculaire du rachis (TTrials 2017) **et augmente les fractures
cliniques** (TRAVERSE, sous-étude fractures, *NEJM* 2024, HR ≈ 1,43). C'est la thèse
« le substitut ne prédit pas le résultat », déjà installée par `vitamine-d` (association vs effet)
et par `masse-maigre-sous-glp1` (mesurer une masse n'est pas mesurer une fonction) — ici elle est
démontrable **deux fois, dans les deux sens**.

- **Paramètres proposés** : id `muscle-vieillissement`, label « Muscle & vieillissement », blurb
  « Ce que l'exercice, l'assiette et les molécules font réellement à la masse et à la force après
  60 ans — et pourquoi les deux ne bougent presque jamais ensemble. » Position à trancher par
  `/arrange` : après `nutrition-sportive` (performance du sujet entraîné → muscle du sujet
  vieillissant) ou en clôture du méta.
- ⚠️ **Réserve taxonomique à trancher explicitement par `/arrange`, ne pas la laisser passer en
  silence.** Les quatre domaines santé existants sont découpés par **type de produit** (nutrition
  sportive, performance cognitive, compléments libres, pharmacologie métabolique) ; celui-ci le
  serait par **population**, et contiendrait donc à la fois de la nutrition et de l'ordonnance.
  C'est une rupture de principe. L'alternative — `sarcopenie-exercice-nutrition` dans
  `nutrition-sportive`, `testosterone-homme-age` dans un domaine hormonal à créer — éclate un
  sujet dont l'unité est justement le fil rouge ci-dessus. Recommandation : créer le domaine, et
  écrire la rupture dans son blurb plutôt que la masquer.
- **Ne pas créer le domaine à vide** : il naît avec `sarcopenie-exercice-nutrition` et son portail
  n'existe qu'au 2e thème — **deux runs pour qu'il existe pleinement**, comme
  `performance-cognitive`. Arêtes à poser dès le 1er thème : `proteines-besoins-timing` (seuil par
  prise, résistance anabolique), `creatine` (section « front qui bouge » de l'écosystème),
  `vitamine-d` (chutes et fractures), `masse-maigre-sous-glp1` (mesurer une masse n'est pas
  mesurer une fonction).

**Deux pièges communs aux deux briefs, à recopier dans chacun :**

1. **La question porte sur l'HOMME de plus de 60 ans, et la littérature ne coopère pas.** Les
   populations âgées déjà citées dans le corpus sont majoritairement féminines (Chapuy à 84 ans,
   l'essai osseux du collagène chez des femmes ménopausées) ; côté nutrition, les essais mélangent
   les sexes sans stratifier ; côté pharmacologie, ils sont exclusivement masculins mais fortement
   comorbides (dans les TTrials : 62,9 % d'obèses, 71,6 % d'hypertendus). **Traiter l'écart entre
   la population de la question et celle des essais comme une limite à écrire, jamais à lisser.**
2. **Les pistes ci-dessous viennent d'une recherche préliminaire : elles sont À CORROBORER EN
   SOURCE PRIMAIRE, jamais des faits.** Si une piste ne se corrobore pas, la retirer — ne pas la
   sauver. (Consigne reconduite mot pour mot du 38e run, où elle a tenu et où le pipeline a
   corrigé une contamination venue du brief.) Deux pistes sont explicitement **signalées comme
   douteuses** et ne doivent pas être reprises telles quelles : le signal d'insuffisance cardiaque
   de l'essai MK-677 après fracture de hanche (Adunsky 2011, ~6,5 % vs 1,7 %), concordant entre
   sources secondaires mais **non vérifié en primaire** ; et une allégation circulant en 2026
   selon laquelle les recommandations nutritionnelles américaines auraient adopté 1,2-1,6 g/kg/j,
   **issue d'un site secondaire non fiable**.

### Sarcopénie : exercice, protéines et suppléments après 60 ans — `sarcopenie-exercice-nutrition` → `muscle-vieillissement`

(**FAIT le 2026-08-18** — 40e run /leanmonograph, 12e thème santé, **crée le domaine
`muscle-vieillissement`**, classé entre `nutrition-sportive` et `performance-cognitive`.
12/12 sections, 48 claims 24✓/18corr/6rej, 91 sources, 2 widgets (0 fond en dur), ~11 000 mots —
le plus long document santé du corpus. Titre : « Muscle après 60 ans : la masse ne prédit pas la
fonction ». **~8,1M tokens / 111 agents / ~3 h 45 en deux runs** — dans la fourchette annoncée
(7-9,5M / 3h-4h30). Lint exit 0 (4 flags, tous adjugés faux positifs : collisions sur
« Journal of Gerontology », entrées de bibliographie) ; contraste mesuré à 0 violation en clair
ET en sombre ; pas de portail (1 seul thème — il naîtra avec `testosterone-homme-age`).

**Le rendement de ce run est un enseignement de méthode, pas un document de plus.**

1. **Le garde-fou d'élagage du 39e run a servi pour la première fois — et il a payé.** Le
   pipeline s'est arrêté APRÈS le council et AVANT d'écrire la prose, parce qu'une section
   allait tomber sous le quota à cause de rejets suspects. Aucune prose payée pour rien.
2. ⚠️ **MAIS il ne signale que les faux rejets DÉCISIFS.** Le balayage manuel des 12
   checkpoints sur le critère `refuted == 0 && corroborated >= 2` en a trouvé **5**, pas 2 : les
   3 autres vivaient dans des sections qui survivaient — dont deux **pile au quota**, donc
   amputées en silence. **Réflexe à systématiser après tout arrêt sur ce garde-fou : balayer
   TOUS les checkpoints, pas seulement les sections que le message nomme.**
3. ⚠️⚠️ **CLASSE D'ÉCHEC NOUVELLE — le ré-audit d'un faux rejet trouve souvent une ERREUR DE
   FOND, pas seulement une source manquante.** Trois des cinq énoncés étaient INEXACTS :
   (a) l'énoncé sur **OPTIMen** attribuait à l'essai un entraînement en résistance que le
   protocole **INTERDISAIT** (« instructed to avoid vigorous resistance and endurance exercise »,
   avec arrêt de la musculation exigé 12 semaines avant l'inclusion), et taisait le second
   facteur du plan 2×2, la testostérone ; (b) **Lopez 2021** était donné pour « 28 essais
   randomisés » — faux deux fois (1/24 et 3/23 études non randomisées, 6/28 en devis
   intra-sujet) — et appariait une plage de tailles d'effet prise dans DEUX analyses avec une
   plage de p issue de la seule analyse globale ; (c) **Morton 2018** plaçait le plateau de
   1,62 g/kg/j et « 49 études / 1 863 participants » dans la même phrase, alors que le point de
   rupture est estimé sur 42 bras et 723 participants. **Promouvoir un claim sur la seule foi
   d'une 2e source trouvée aurait publié un fait faux avec deux références correctes en
   dessous.** Le ré-audit doit TOUJOURS re-vérifier l'énoncé en source primaire, jamais se
   contenter de chercher la source manquante.
4. **3e incarnation du trou d'indépendance par URL**, sur un claim que le council avait pourtant
   bien traité (il avait retourné l'énoncé) : sa liste comptait le MÊME article du *Journal of
   Nutrition* sous deux URLs (ScienceDirect et le site de la revue) plus un site commercial de
   calculateur de protéines, et son `audit_note` annonçait « 5 sources indépendantes » pour
   3 travaux réels. Dédoublonné à la main.
5. **Deux pièges d'indépendance désamorcés par les ré-audits**, à garder en tête pour les runs
   santé : la meilleure source apparente pour OPTIMen (méta-analyse de Hudson & Campbell) est
   signée par un **co-auteur de l'essai** ; et pour SPRINTT, la seule revue tierce qui cite la
   métrologie fine **en intervertit l'intervalle de confiance** (elle accole l'estimation de
   36 mois à l'intervalle de 24 mois) — la graphie fautive circule dans la littérature
   secondaire, la prose ne l'a pas recopiée.
6. **`write:audit-report.json` a de nouveau échoué sur la limite de 64 000 tokens de sortie**
   (pattern connu) : régénéré en déterministe depuis les checkpoints et `knowledge.json`, avec
   une `regeneration_note` qui déclare les 5 ré-adjudications manuelles.
7. **Bon comportement confirmé** : la consigne « pistes à corroborer, jamais des faits » a encore
   tenu. Mieux, le council a **RETOURNÉ** la piste que le brief signalait comme douteuse — les
   recommandations américaines à 1,2-1,6 g/kg/j sont une cible pratique, l'apport journalier
   recommandé restant à 0,8 g/kg/j — et le document en fait un point de fond.
8. Les 5 claims ré-adjugés portent tous, en tête de leur `audit_note`, la mention « Confirmé
   après RÉ-ADJUDICATION MANUELLE — ceci n'est pas un verdict de council », et la prose attribue
   nommément tout ce qui est resté mono-source (« l'essai rapporte », « les auteurs rapportent »),
   vérifié passage par passage sur `prose.json` avant le build.)

**Verdict d'origine : gap réel (haute) — crée le domaine.** Régime de preuve mature : méta-analyses
multiples et concordantes, effets modestes mais affirmables. C'est le thème qui porte la moitié
« ce qui marche » du fil rouge.

> Gagner ou garder du muscle après 60 ans : ce que l'exercice et l'assiette obtiennent réellement,
> et sur quel critère. Couvrir d'abord le cadre et sa dispute — la sarcopénie et ses définitions
> concurrentes (EWGSOP2 2019 qui place la **force** au centre et fait de la masse une
> confirmation ; GLIS 2024, consensus Delphi mondial dont la définition **opérationnelle** n'est
> toujours pas publiée ; SDOC 2020 qui **exclut** la masse musculaire parce qu'elle ne prédit pas
> les événements incidents) —, puis la résistance anabolique liée à l'âge : établie (méta-analyse
> d'études traceurs), d'ampleur **modeste**, et disputée dans son étiologie (part de l'âge vs part
> de l'inactivité et des épisodes de décharge — l'argument « inevitable or preventable ? »).
> Ensuite l'entraînement en résistance comme **seul levier de première ligne** : gains chiffrés de
> masse (~+1 kg) contre gains de force très supérieurs (méta-analyses Peterson 2011, Borde 2015,
> network meta-analysis *Age and Ageing* 2018), le **renversement récent en faveur du volume BAS**
> (network méta-analyse de ~151 essais chez les ≥ 60 ans), charges lourdes vs légères poussées
> près de l'échec, power training, entraînement sous restriction de flux sanguin (BFR) et sa
> sécurité mal documentée, et surtout la dose réellement tenue — l'adhérence est le verrou, pas la
> physiologie. Puis les protéines : le divorce persistant entre consensus d'experts (PROT-AGE
> 2013, ESPEN 2014 : ≥ 1,0-1,2 g/kg/j) et essais contrôlés d'alimentation négatifs en conditions
> non stressées, le seuil par repas relevé avec l'âge (~0,40 g/kg, ~3 g de leucine), la
> distribution des prises (rationnel aigu fort, RCT au long cours non démonstratifs — un écart
> promesse/preuve à nommer), sources animales vs végétales et l'écart entre traceurs aigus et
> essais chroniques, et la lecture **conditionnelle** qui réconcilie la littérature : le
> supplément protéique n'ajoute que si l'apport de base est insuffisant. Enfin le tri des
> suppléments, verdict par verdict : créatine (le seul bénéfice reproductible, ~+1 kg au-delà de
> l'entraînement, **nul sans entraînement**, avec la controverse 2025 du « wash-in » qui isole la
> part hydrique), HMB (effet réel mais petit, surtout en situation catabolique ; les gains
> historiques spectaculaires jamais répliqués), vitamine D (trois grands essais négatifs sur la
> masse et la sarcopénie, bolus délétères), oméga-3 (effet force minuscule, effet masse non
> démontré, l'essai fondateur jamais répliqué), leucine seule (nulle), collagène (inférieur à
> toute protéine complète à dose égale). Terminer par les interventions multimodales — PROVIDE,
> SPRINTT et sa leçon : le combiné protège la **fonction** plus que la masse. ⚠️ Délimitations
> strictes : `proteines-besoins-timing` couvre le plateau de 1,6 g/kg/j, la fenêtre anabolique et
> le score protéique chez le sujet entraîné en surplus ou à l'équilibre — **partir de là, ne pas
> le re-dériver** ; `creatine` couvre le mécanisme, la charge et la dose (l'angle neuf est la
> population âgée et le conditionnement à l'entraînement) ; `vitamine-d` couvre chutes, fractures
> et la frontière carencé/institutionnalisé — **s'y appuyer, ne pas refaire le dossier**, l'angle
> neuf est le muscle (masse et force), que ce voisin ne traite pas ; `collagene` a déjà rendu son
> verdict et le patron de la littérature mono-source ; `masse-maigre-sous-glp1` couvre la
> préservation sous déficit pharmacologiquement induit — **ici on parle de gagner, pas de moins
> perdre**. Public : lecteur exigeant non spécialiste. Doctrine de preuve santé
> (`docs/evidence-sante.md`) à recopier intégralement dans le brief. Domaine :
> muscle-vieillissement (à créer).

### Testostérone et anabolisants chez l'homme âgé — `testosterone-homme-age` → `muscle-vieillissement`
**Verdict : gap réel (haute) — ouvre le portail du domaine.** Aucune couverture : la testostérone
et la pharmacologie des SARMs sont absentes des 8 documents lus **et ne font l'objet d'aucun
renvoi**. C'est le thème qui porte la moitié « ce qu'on promet » du fil rouge, et son régime de
preuve est l'inverse du précédent : essais rares et anciens du côté publié, communiqués de
promoteur du côté récent.

> La testostérone et ce qu'on vend avec elle à l'homme vieillissant : ce que les essais mesurent,
> et sur quel critère ils échouent. Le dossier principal est la TRT — les Testosterone Trials
> (*NEJM* 2016 : 790 hommes de 65 ans et plus, et le détail qui décide de la lecture, **l'essai
> dédié à la fonction physique manque son critère primaire** pendant que l'agrégat de tous les
> participants devient significatif, pour une différence moyenne de quelques mètres au test de
> marche de 6 minutes, **sous la différence minimale cliniquement importante**), TEAAM (3 ans,
> ~+0,9 kg de masse maigre, force du haut du corps améliorée, **pas celle des jambes**), la
> dose-réponse de Storer 2008 (masse, force et puissance dose-dépendantes ; vitesse de marche et
> TUG **non liés à la dose**, avec l'explication des auteurs : le plateau de la courbe
> force/fonction), et TRAVERSE (2023) pour la sécurité cardiovasculaire — **avec sa sous-étude
> fractures de 2024, le contre-exemple central du document : la densité osseuse monte et les
> fractures aussi**. Puis la combinaison qui déflate la molécule : LITROS et TEX montrent que le
> gain fonctionnel vient **intégralement** du programme d'exercice, la testostérone achetant la
> masse maigre et l'os ; T4DM pour le versant métabolique et sa contrepartie hématologique.
> Ensuite la fabrique de la demande : la prévalence réelle de l'hypogonadisme tardif (EMAS, ~3 %
> à 60-69 ans) contre le volume de prescriptions et sa croissance concentrée sur des tranches
> d'âge **plus jeunes**, la télémédecine directe au consommateur et l'étude en « client mystère »
> (*JAMA Internal Medicine* 2023), et le vocabulaire lui-même (« age-related », « late-onset »,
> « functional ») que l'Endocrine Society critique nommément en 2026. Le versant réglementaire est
> à traiter de première main et il bouge : retrait par la FDA du *boxed warning* cardiovasculaire
> (février 2025) **avec maintien explicite de la Limitation of Use pour l'hypogonadisme lié à
> l'âge**, panel d'experts de décembre 2025, extension d'indication envisagée sur **la libido** —
> pas sur le muscle ; côté français, le SMR d'Androtardyl important **sauf** pour le déficit
> androgénique lié à l'âge. Trois sections pour le reste de la pharmacologie : les SARMs (échec
> réglementaire fondateur d'enobosarm dans les essais POWER, où la masse bouge et la puissance de
> montée d'escalier non ; LGD-4033 à 21 jours chez des sujets **jeunes**, sans aucune mesure de
> force ; RAD-140, le plus vendu du marché gris, avec **zéro donnée humaine de composition
> corporelle** ; hépatotoxicité documentée par séries de cas, suppression de l'axe, baisse du
> HDL ; statut : approuvé nulle part, détention interdite en France par l'arrêté du 18 juin 2024,
> classe S1.2 de l'AMA), la GH exogène chez le sujet âgé sain (méta-analyse de 2007 : ~+2,1 kg de
> masse maigre, ~−2,1 kg de masse grasse, **aucun effet sur la capacité fonctionnelle**, excès
> d'œdèmes, canal carpien et arthralgies — et le régime pénal fédéral américain qui frappe la
> prescription anti-âge indépendamment de toute efficacité), et **l'échec réglementaire de la
> pharmacologie sarcopénie** comme clôture : aucun médicament approuvé, l'avis négatif du CHMP sur
> l'anamoréline (« effet marginal sur la masse maigre et aucun effet prouvé sur la force de
> préhension »), l'approbation japonaise du **même** dossier — divergence doctrinale et non
> scientifique —, l'arrêt définitif de l'azélaprag pour hépatotoxicité (janvier 2025), le critère
> primaire manqué de SARA-INT/BIO101 présenté comme « prometteur » par son promoteur. Finir sur le
> marché gris et le contenu réel des flacons (l'analyse de référence *JAMA* 2017 : ~52 % des
> produits contiennent le SARM annoncé, ~41 % à la bonne dose, ~9 % rien du tout, ~39 % un autre
> médicament non approuvé), et l'alerte ANSM de juillet 2026 avec ses mesures de police sanitaire.
> ⚠️ **Une lacune à écrire comme telle, pas à combler par extrapolation** : aucune donnée de
> prévalence d'usage des SARMs ou des peptides chez les hommes de plus de 60 ans n'a été trouvée,
> et les séries d'hépatotoxicité portent sur des hommes de 24 à 46 ans. ⚠️ **Délimitations
> strictes, deux moitiés sont déjà prises** : `peptides-gris` couvre **les sécrétagogues de GH**
> (CJC-1295, MK-677, ipamoréline, tésamoréline comme étalon d'AMM), la typologie de l'adultération
> et le statut « research use only » — les citer, **ne pas les retraiter** ;
> `masse-maigre-sous-glp1` couvre **les anticorps anti-myostatine/activine** (bimagrumab,
> apitegromab, trévogrumab) et tout le pivot GLP-1 — la frontière est nette : chez lui, empêcher
> une perte pendant un amaigrissement ; ici, **produire un gain chez la personne âgée** ;
> `incretines-glp1` couvre le marché gris du compounding des médicaments approuvés ;
> `complements-amincissants` a posé le patron du verdict de rayon. ⚠️ **Discipline de source
> propre à ce thème** : les trois essais les plus pertinents pour la question (enobosarm chez les
> plus de 60 ans, et les deux essais de préservation sous agoniste) **ne sont connus que par
> communiqués de promoteur** — les nommer comme tels partout, ne jamais les compter comme une
> source de plus que l'essai qu'ils annoncent, et ne pas les laisser porter une section. Public :
> lecteur exigeant non spécialiste. Doctrine de preuve santé (`docs/evidence-sante.md`) à recopier
> intégralement dans le brief. Domaine : muscle-vieillissement.

### Graisse viscérale de l'homme mûr — `graisse-viscerale-homme-age` → `muscle-vieillissement` (à confirmer)
**Verdict : gap réel SOUS CONDITION DE RECENTRAGE, priorité moyenne, ajouté le 2026-08-26 sur
demande explicite** (« perte de graisse abdominale chez le sujet mâle de plus de 50 ans »).

⚠️ **La condition est bloquante, et elle est écrite plus haut dans ce fichier.** La règle du
2026-08-15 dit qu'« un objectif ne mérite sa monographie que si aucune molécule seule ne le porte
ET que le corpus n'a aucune couverture » : la seconde moitié n'est **pas** remplie — quatre
documents couvrent le versant pharmacologique (`incretines-glp1`, `masse-maigre-sous-glp1`,
`berberine`, `complements-amincissants`) et un cinquième la seule AMM du champ (`peptides-gris`).
Formulé « perdre du ventre après 50 ans », ce candidat retombe sous le verdict déjà rendu
`objectif : perte de poids / masse grasse — écarté, saturé`. Il ne passe qu'avec le centre déplacé
là où le corpus est **entièrement vide** : l'exercice comme intervention, le tour de taille comme
instrument de mesure, la physiologie de la distribution. Les molécules y entrent en rappels de deux
phrases avec renvoi, **jamais en sections** — c'est la ligne à écrire dans `args.subject`.

Matière neuve relevée le 2026-08-26 (résultats de recherche, **à instruire en primaire** : rien
ci-dessous n'a valeur de fait vérifié) : méta-analyses en réseau exercice → tissu adipeux viscéral
(84 RCT dans *Obesity Reviews* 2024 ; dose-réponse dans *Int J Obesity* 2021 ; *PLOS One* 2013), et
surtout l'effet **sans perte de poids** (exercice vs régime hypocalorique : effets dissociés sur le
poids et sur le viscéral) — c'est le fil rouge candidat, le compartiment bouge quand la balance ne
bouge pas ; essais sur la bonne tranche d'âge (RESOLVE, 100 participants de 50 à 70 ans ; combiné
−36 % contre −19 % et −21 % pour aérobie ou résistance seuls chez l'âgé obèse) ; le tour de taille
comme « signe vital » (consensus IAS/ICCR 2020, *Nature Reviews Endocrinology* — **pilier
document-source** : une position de groupe de travail, source unique par nature) ; la boucle
hypogonadisme ↔ obésité viscérale par l'aromatase et le shunt testostérone → estradiol, seul
mécanisme qui justifie le mot « homme » du titre ; le ciblage local, consensus négatif d'un
demi-siècle contredit par un RCT 2023 sur **16 hommes** (*Physiological Reports*) — cas d'école
taillé pour ce corpus, à traiter comme mono-source et non comme un renversement.

⚠️ **Trois risques à écrire dans le brief.**
1. **La restriction « > 50 ans » n'a pas sa littérature dédiée sur tout le périmètre** : les
   méta-analyses portent sur des « adultes en surpoids », parfois seulement stratifiées par sexe
   (la résistance réduirait le viscéral chez l'homme et pas chez la femme selon une des synthèses).
   Exiger la déclaration explicite chaque fois que la population de l'essai n'est pas celle du
   titre — sinon extrapolation silencieuse, et le lint ne la verra pas.
2. **Le RCT de ciblage local est le piège du document** : petit effectif, conclusion contraire au
   consensus, titre affirmatif (« spot reduction exists »). Le traiter comme `collagene` traite ses
   mono-sources, jamais comme la réponse à la question.
3. **Aucune « arête à poser » vers un thème d'un autre domaine** : `portal.py` refuse tout slug hors
   du domaine dans `parcours`, `aretes` et `delimitations` (leçon du 42e run). Les renvois vers
   `incretines-glp1`, `berberine` et `peptides-gris` n'ont qu'une forme légale, une phrase d'`intro`
   sans slug — sauf si le domaine retenu est `pharmacologie-metabolique`.

**Domaine : à trancher par `/arrange`, pas ici.** Trois options, aucune parfaite : (a)
`muscle-vieillissement` — le voisinage est le meilleur (`sarcopenie-exercice-nutrition` et
`testosterone-homme-age` sont les deux voisins directs, et T4DM y est déjà instruit sur la
population exacte du titre), au prix d'un blurb à élargir de « la masse et la force » vers la
composition corporelle ; (b) `pharmacologie-metabolique` — logement immédiat et arêtes légales vers
les GLP-1, mais il tire le document vers les molécules, c'est-à-dire vers le doublon qu'on cherche
à éviter ; (c) `nutrition-sportive` — son blurb nomme la composition corporelle, mais « sportive »
cadre mal un homme de 55 ans qui veut perdre du ventre.

> La graisse viscérale de l'homme après 50 ans : ce que l'exercice, la mesure et la physiologie de
> la distribution obtiennent réellement, une fois les médicaments du poids laissés à leurs
> monographies. Fil rouge : **le compartiment bouge quand la balance ne bouge pas** — l'exercice
> sans déficit calorique réduit le tissu adipeux viscéral sans forcément réduire le poids, et
> inversement un amaigrissement peut être compté comme un succès sans que le compartiment à risque
> ait beaucoup changé ; d'où la thèse que le poids est le mauvais critère et que le tour de taille
> est le bon. Structure : ce qu'est le viscéral et en quoi il diffère du sous-cutané (mesure de
> référence au scanner, DXA, et ce que le pèse-personne ne voit pas) ; **le tour de taille comme
> instrument** — protocole de mesure, seuils, et la position du groupe de travail IAS/ICCR qui
> demande sa prise en routine clinique (source unique par nature : la déclarer comme telle) ;
> pourquoi la graisse de l'homme se dépose là — distribution androïde, et la boucle
> hypogonadisme/obésité viscérale par l'aromatase, avec sa direction de causalité discutée ;
> **l'exercice, dose par dose** — aérobie, résistance, HIIT, combiné : ce que les méta-analyses en
> réseau classent, la dose efficace (fréquence, durée, semaines), et l'effet à poids constant ;
> l'âge et le sexe comme modificateurs, avec la discipline de déclaration ci-dessus ; **le ciblage
> local**, un demi-siècle de consensus négatif et le petit essai qui prétend le renverser ; ce que
> l'assiette ajoute (déficit énergétique, alcool, répartition) sans re-dérouler
> `proteines-besoins-timing` ; sécurité, doses, interactions ; et une section de verdicts de rappel
> où chaque molécule reçoit deux phrases et un renvoi. Délimitations strictes : ne PAS re-dérouler
> les agonistes GLP-1 (`incretines-glp1` tient STEP/SURMOUNT/SELECT et la médiation par le tour de
> taille ; `masse-maigre-sous-glp1` tient la contrepartie musculaire), ni le rayon amincissant
> (`complements-amincissants`), ni la berbérine, ni la testostérone chez l'homme âgé
> (`testosterone-homme-age` tient T4DM et l'axe androgénique), ni la tésamoréline
> (`peptides-gris` tient la seule AMM sur le viscéral, dans la lipodystrophie du VIH) : chacun a sa
> monographie, chacun n'a droit qu'à un verdict et un renvoi. Public : lecteur exigeant non
> spécialiste. Doctrine de preuve santé (`docs/evidence-sante.md`) à recopier intégralement dans le
> brief. Domaine : à confirmer (voir ci-dessus).

---

## `fonction-sexuelle` — domaine À CRÉER (proposé le 2026-08-26)

**Verdict : gap réel, et le méta-domaine le réclame par son propre label.** « Santé, nutrition &
performance humaine » couvre aujourd'hui la performance physique (`nutrition-sportive`), le muscle
vieillissant, la cognition, les compléments de santé générale et la pharmacologie métabolique. La
fonction sexuelle n'a aucun logement : ce n'est ni un complément en vente libre, ni un médicament du
poids, ni du muscle, ni de la cognition. C'est le seul champ du méta-domaine où une classe de
médicaments à AMM, massivement prescrite **et** massivement détournée, n'est nommée nulle part —
0 occurrence de `sildénafil`, `tadalafil`, `PDE5` dans les 84 documents.

- **Paramètres proposés** : id `fonction-sexuelle`, label « Fonction sexuelle », blurb « Ce que les
  essais démontrent quand on prétend traiter — ou améliorer — la fonction sexuelle. » Classé après
  `performance-cognitive` (performance physique → cognitive → sexuelle) et avant `complements-sante`.
- ⚠️ **Ne pas le laisser à moitié né.** `/arrange` ne crée jamais un domaine vide, et le portail
  exige un 2e thème : le chantier `performance-cognitive`, ouvert au 39e run, n'a été refermé qu'au
  42e. Le 2e thème est donc à décider **avant** de lancer le premier. Candidat le plus propre :
  **`ejaculation-precoce`** — à instruire, l'IELT (délai d'éjaculation intravaginal chronométré),
  l'un des très rares critères d'efficacité **objectifs** de tout le méta-domaine ; la dapoxétine et
  son statut réglementaire réel juridiction par juridiction ; les ISRS hors AMM ; les anesthésiques
  topiques. Aucun chevauchement avec les voisins. À écarter comme 2e thème : tout document centré
  sur le rayon gris (il redirait `complements-amincissants` et `peptides-gris` — c'est précisément le
  motif de rejet du 2026-08-15) et tout document sur la libido androgénique
  (`testosterone-homme-age` tient déjà l'avis FDA du 20 avril 2026 sur le désir sexuel bas).
- ⚠️ **Aucune arête vers `testosterone-homme-age`** : il appartient à `muscle-vieillissement`, et
  `portal.py` refuse tout slug hors du domaine dans `parcours`, `aretes` et `delimitations`. Le
  renvoi n'a qu'une forme légale, une phrase de l'`intro` sans slug.
- ⚠️ **Publication : thème santé = DOUBLE neutralisation** (cf. mémoire `pages-publication`), et
  sujet intime : la doctrine de preuve santé s'applique au pied de la lettre, sans exception de ton.

### Inhibiteurs de la PDE5 — `inhibiteurs-pde5` → `fonction-sexuelle`
**Verdict : gap réel, priorité HAUTE, ajouté le 2026-08-26 sur demande explicite** (« amélioration
des performances sexuelles : Viagra, Cialis et autres »). Nommé par classe pharmacologique, sur le
patron `incretines-glp1`. C'est le meilleur profil de candidat santé disponible : littérature RCT
massive et ancienne, critère validé et chiffré (IIEF), pilier réglementaire épais, et un écart
promesse/preuve qui se mesure au lieu de se supposer.

**Couverture vérifiée par lecture le 2026-08-26** : nulle. « Érectile » n'apparaît que dans
`testosterone-homme-age`, deux fois et jamais comme objet — dans la définition EMAS de
l'hypogonadisme tardif (trois symptômes sexuels dont la dysfonction érectile, plus une testostérone
< 11 nmol/L : 2,1 % de 2 966 hommes de 40 à 79 ans) et dans l'avis FDA du 20 avril 2026 sur le
désir sexuel bas. Ce même document **nomme** le *Sexual Function Trial* des Testosterone Trials
dans l'architecture de l'essai sans en dérouler un seul résultat, et conclut que « le seul terrain
sur lequel le régulateur accepte d'avancer est celui du désir » — sans instruire ce terrain. La
frontière du nouveau thème est donc déjà écrite par le corpus lui-même.

Matière relevée le 2026-08-26 (résultats de recherche, **à instruire en primaire**) : efficacité
sur l'IIEF, +7 à 10 points au dosage maximal contre placebo, avec des comparatifs par molécule
(sildénafil 9,65 ; tadalafil 8,52 ; vardénafil 7,50) et une méta-analyse en réseau 2026 dans le
*Journal of Sexual Medicine* ; quotidien contre à la demande pour le tadalafil ; **l'usage chez
l'homme sans dysfonction** — 9 % d'un échantillon d'étudiants en médecine à fonction érectile
parfaite déclarent en avoir pris, dont 71 % avec de l'alcool, et des allégations d'usage sportif
dont la preuve d'effet est à peu près nulle ; adultération, où le chiffre se retourne contre le
corpus déjà publié — sur les 572 compléments adultérés signalés par la FDA entre 2007 et 2014,
41,6 % relevaient de la performance sexuelle, **première catégorie**, quand
`complements-amincissants` cite le même travail pour ses 40,9 % d'amincissants et mentionne les
« produits sexuels » sans les instruire ; et 67 % de 102 produits achetés en boutique contenant au
moins un inhibiteur de PDE5 non déclaré.

⚠️ **Deux risques.** (1) Le document doit tenir la distinction soin / augmentation sans la moraliser
ni la dissoudre : la même molécule restaure une fonction chez le patient et ne démontre à peu près
rien chez l'homme sans trouble — c'est le fil rouge, pas un jugement. (2) La section adultération
est **plafonnée à une section** : au-delà, le document redevient celui qu'on a écarté en 2026-08-15.

> Les inhibiteurs de la PDE5 — sildénafil, tadalafil, vardénafil, avanafil — au tamis des essais :
> ce qu'ils démontrent chez l'homme qui a un trouble, ce qu'ils ne démontrent pas chez celui qui
> veut seulement faire mieux. Fil rouge, transposé du 39e run et de sa section « Restaurer ou
> augmenter » : **la ligne de base décide du résultat**. Chez l'homme dont la fonction érectile est
> altérée, l'effet est l'un des mieux établis de toute la pharmacologie du confort — chiffré, dosé,
> répliqué, mesuré par un questionnaire validé. Chez l'homme sans trouble, la littérature qui
> soutiendrait une « amélioration de la performance » est quasi inexistante, alors que l'usage,
> lui, est documenté et mélangé à l'alcool et aux drogues récréatives. Structure : le mécanisme
> (NO/GMPc, spécificité PDE5 et ce que les autres PDE expliquent des effets indésirables — PDE6 et
> les troubles visuels, PDE11 et le tadalafil) ; **mesurer une fonction sexuelle** — l'IIEF et son
> domaine érectile, les questions SEP, ce qu'un score de 7 à 10 points veut dire pour un patient, et
> pourquoi les taux de « réponse » ne se comparent pas d'un essai à l'autre ; molécule par molécule
> et dose par dose, avec les demi-vies et le quotidien contre l'à la demande ; **restaurer ou
> augmenter** : ce qui a été mesuré chez l'homme sans dysfonction, et la prévalence déclarée de
> l'usage récréatif contre la prévalence mesurée (reprendre la méthode du 39e run sur l'écart
> déclaré/mesuré) ; l'écart entre performance ressentie et performance mesurée, s'il existe une
> littérature qui le teste ici ; sécurité — nitrates et contre-indication absolue, hypotension,
> priapisme, NAION et surdité brusque, interactions (alpha-bloquants, inhibiteurs du CYP3A4) ;
> **le régulateur** : AMM, mentions obligatoires, passage en vente libre au Royaume-Uni et ce que
> cette décision a exigé comme dossier ; et **une seule** section sur le rayon gris : compléments
> « naturels » adultérés au sildénafil, contrefaçons, plateformes de télémédecine — sans re-dérouler
> le patron d'adultération déjà écrit ailleurs. Délimitations strictes : ne PAS retraiter l'axe
> androgénique ni l'hypogonadisme tardif (`testosterone-homme-age` tient l'EMAS, les Testosterone
> Trials, T4DM, TRAVERSE et l'avis FDA du 20 avril 2026 sur le désir — le renvoi se fait par une
> phrase d'intro sans slug, `portal.py` interdisant l'arête inter-domaines) ; ne PAS refaire le
> verdict de rayon des compléments (`complements-amincissants`) ni le dossier du marché gris des
> peptides (`peptides-gris`) ; ne PAS traiter la fonction sexuelle féminine ni les troubles du
> désir, qui sont un autre sujet et un autre corpus. S'attendre à un profil de rejets FAIBLE pour
> un thème santé — la littérature est ancienne, industrielle et répliquée — sauf sur deux points où
> il faut au contraire s'attendre au pire : les chiffres d'usage récréatif (enquêtes déclaratives,
> petits échantillons, populations non représentatives) et les allégations sportives. Public :
> lecteur exigeant non spécialiste. Doctrine de preuve santé (`docs/evidence-sante.md`) à recopier
> intégralement dans le brief. Domaine : fonction-sexuelle (à créer par ce thème).
