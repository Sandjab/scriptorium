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

**Passe d'enrichissement du 2026-09-01** (corpus à 89 thèmes / 91 documents) : revue des 2
méta-domaines et de leurs 12 domaines, à la demande. Point de départ : **quatre domaines n'avaient
plus aucun candidat** (`ai-organizations`, `pharmacologie-metabolique`, `fonction-sexuelle`, et
`performance-cognitive` hors une entrée basse), et `ai-organizations` reste le seul domaine sans
portail. 47 idées soumises à 12 agents-lecteurs (un par domaine), chacun tenu à la règle du projet —
grep pour LOCALISER, verdict pris sur la prose LUE, citations verbatim à l'appui —, plus un 13e
agent chargé du balayage corpus de l'heuristique du renvoi (« traité ailleurs », « relève de »,
« dossier distinct »… : 159 occurrences brutes, ≈ 55 renvois de sujet, chaque cible ouverte et lue).
Bilan : **33 gaps réels, 7 partiels, 7 écartés** ; 36 candidats ajoutés ci-dessous, 1 remonté de
priorité. Cinq constats ont décidé des verdicts :

1. **Le balayage des renvois a pris cinq fois, dont trois cibles qui existent mais ne disent pas ce
   qui est promis.** (A1) `diffusion-language-models` renvoie la génération parallèle masquée à « la
   monographie consacrée au décodage » — `decoding-sampling` n'a aucune occurrence de « non
   autorégressif » ni de « Mask-Predict » ; (A2) `pretraining-data-curation` renvoie « de combien un
   score publié s'en trouve faussé » à `llm-evaluation`, qui est une monographie LLM-as-a-judge où
   la contamination tient en trois phrases ; (A3) le même document écrit que « la mécanique des
   signatures, MinHash et LSH, relève d'un autre document » — **aucun document du corpus ne
   contient MinHash** : `minhash-dedup`, classé « marginal » ici, est remonté en priorité moyenne ;
   (A4) `nootropiques-stimulants-prescrits` renvoie le contenu réel des gélules hors circuit à
   « d'autres monographies de ce corpus » qui ne traitent aucun stimulant contrefait ; (A5)
   l'écosystème de `masse-maigre-sous-glp1` décrit faussement `proteines-besoins-timing` (« ne
   couvre pas le déficit marqué » — il a une section entière dessus ; c'est le déficit
   *pharmacologiquement induit* qui manque, et la section `proteines-et-entrainement` du même
   document le dit correctement). ⚠️ **Réparations locales à faire, hors backlog** : A5 (une phrase
   dans `manifest.json`), et la phrase périmée de `nootropiques-panorama` sur les oméga-3 (« aucun
   autre document de ce corpus ne les traite », faux depuis le 48e run). Non faites ce jour.
2. **Le corpus désigne lui-même ses gaps, plus souvent par l'objet nommé que par le renvoi.**
   `incretines-glp1` nomme le piège « traiter la perte de poids comme le seul résultat de la
   classe » puis n'en traite qu'un contre-exemple (SELECT) ; `testosterone-homme-age` nomme trois
   fois le désir sexuel sans jamais rapporter le Sexual Function Trial ; `hyperloglog` et
   `count-min-sketch` écrivent chacun que leurs garanties supposent « une hypothèse rarement
   explicitée » sur la fonction de hachage, qu'aucun thème ne pose ; `creatine` et
   `cafeine-ergogene` citent la liste du Groupe A de l'AIS, dont le jus de betterave est le seul
   membre sans candidat ; `structured-extraction-llm` annonce la « conversion langage naturel vers
   requêtes structurées » et ne la développe jamais ; `convolutional-networks` nomme Szegedy et la
   FGSM en deux phrases de clôture et passe.
3. **Le méta santé est masculin par construction.** Sur 20 thèmes, aucun n'a la femme pour sujet ;
   elle n'apparaît qu'en population d'essai (Chapuy, l'essai osseux du collagène, « 46 femmes en
   déficit de 750 kcal/j ») ou en exclusion de sécurité (grossesse, contraceptifs). Ménopause, THM,
   WHI : jamais traités ; désir féminin : jamais nommé. Deux candidats en découlent
   (`desir-sexuel-hypoactif`, `disponibilite-energetique-reds`) et une tête de file de domaine neuf
   (`menopause-hormonotherapie`).
4. **Sept « écartés » le sont sur lecture, pas sur intuition** (liste en fin de la section
   « Écartés ») : le décodage contraint (chaque point du brief est dans `structured-extraction-llm`,
   XGrammar et le « 75,99 % → 49,25 % » compris), la nicotine (substance 10 des 25 du panorama,
   section dédiée), les expériences de terrain hors code (`ia-productivite-esn` expose
   Brynjolfsson/Li/Raymond, Noy & Zhang et Dell'Acqua avec leurs chiffres), les suppléments
   anti-sarcopénie (HMB, leucine, oméga-3 dans `reste-du-rayon`), le pipeline GLP-1 (section
   `pipeline-retatrutide` de 18 000 caractères).
5. **Deux erreurs de ce backlog corrigées par la lecture** : `count-min-sketch` ne traite PAS les
   heavy hitters déterministes (Misra-Gries et SpaceSaving ne sont qu'une phrase de
   `streaming-quantiles-sampling`), contrairement à ce que supposait l'idée soumise ; et
   « `llm-evaluation` traite déjà la contamination des benchmarks côté évaluation » (passe du
   2026-08-01) était trop généreux — trois phrases de limites, aucune mesure.

**Têtes de file de cette passe** — IA : `ia-competences-deskilling-apprentissage` (FAIT le
2026-09-02 ; il a ouvert `ai-organizations`, et **plus aucun domaine n'est sans portail** — la règle
du 2026-08-27 n'a donc plus d'objet pour l'instant) ; santé : `glp1-hors-poids`,
`desir-sexuel-hypoactif`, `osteoporose-pharmacologie` (table d'ordre de lancement révisée dans la
section santé). ⚠️ Les pistes chiffrées des prompts ajoutés ci-dessous viennent de la mémoire du
rédacteur et des rapports de lecture, **sans balayage web** : à corroborer en source primaire au
Sweep, jamais des faits ; si une piste ne se corrobore pas, la retirer.

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

(`ia-competences-deskilling-apprentissage` : FAIT le 2026-09-02, retiré du backlog — 50e run
/leanmonograph. **Ouvre le portail `ai-organizations`**, le dernier domaine qui n'en avait pas.
11 sections, 43 claims (12 confirmés / 24 corrigés / 7 rejetés), 72 sources, 2 widgets.
Arrêt au garde-fou d'élagage puis réparation : le contrôle d'acceptation a sorti FAUX sur
**10 claims `confirmed` ne reposant que sur une source recevable** — reprises de presse,
miroirs et blogs comptés comme corroboration. Ont été rattrapés en réparation : une fourchette
chiffrée FABRIQUÉE autour d'un chiffre unique et écrite en toutes lettres, le signe d'une
métrique inversé dans un claim retenu, la thèse d'un papier de référence retournée deux fois,
et un conseil organisationnel faux — « mentorat par les seniors » là où la preuve porte sur la
compétence du collègue, pas sur son rang.)

(`ia-emploi-marche-du-travail` : FAIT le 2026-09-02, retiré du backlog — 51e run /leanmonograph.
3e thème d'`ai-organizations`. 10 sections, 39 claims (18 confirmés / 15 corrigés / 6 rejetés),
55 sources, 4 widgets. **Le brief du backlog était partiellement faux et a été corrigé avant
lancement** : il demandait de couvrir les projections macro (Acemoglu vs Goldman), or
`ia-productivite-esn` les tient déjà en profondeur, figure comprise — périmètre resserré en amont,
sur la construction des indices et les effets réalisés. 6e arrêt au garde-fou d'élagage, réparé en
RÉ-GRAINANT au phénomène (Atalay et al. 2020, corpus disjoint et critiques de l'instrument d'ALM),
pas en cherchant un miroir du chiffre. **Découverte transversale** : Autor-Levy-Murnane existe en
deux versions aux chiffres DIFFÉRENTS — « thirty to forty percent » et « more than half » au NBER
w8337 (2001), « 60 percent » et « almost half » au QJE 118(4) (2003), dénominateur compris. Les
claims les citaient fusionnées sous « w8337 / QJE 2003 », ce qui rendait le désaccord entre jurés
insoluble : chaque juré lisait un document différent et les deux avaient raison. 4e occurrence du
trou d'acceptation, sur 4 claims `confirmed` corroborés par des **reprises de presse du papier
décrit** (TIME, Fortune, Yahoo — cette dernière syndication mot pour mot de Fortune, donc la même
source comptée deux fois) ; ré-adjugés par 2 jurés indépendants → 1 réparé au seuil avec trois
travaux distincts, 2 en exception `document-source` déclarée, 1 déclassé en `corrected`. L'agent
Build a de nouveau eu raison de REFUSER de déclarer l'exception à la place des jurés.)
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

(`llm-watermarking-detection` : FAIT le 2026-08-31, retiré du backlog — 49e run /leanmonograph,
GREEN après un ré-audit manuel de l'appareil de preuve, classé dans llm-agents-generation **en
CLÔTURE du portail** (20e du parcours, après llm-inference-serving : le bloc decoding-sampling →
diffusion-language-models → llm-inference-serving est un triangle tenu par trois arêtes, l'ouvrir
au milieu l'aurait cassé ; le lien mécanique au sampling passe par une arête, sans adjacence).
11/11 sections, 44 claims 32✓/10corr/2rej, 61 sources, 5 widgets ; 8,48M tok / 119 agents /
~2 h 55 en deux lancements.

Gap re-vérifié par LECTURE avant lancement, et la lecture a payé une 6e fois : le backlog ne
signalait pas que **trois résultats d'impossibilité distincts vivent déjà dans le corpus**, que
rien ne distingue au grep — BEB et le Defense Trilemma dans `llm-safety-jailbreaks` (l'alignement
et les défenses enveloppantes), Karbasi et al. dans `hallucination-detection-uncertainty`
(la détection d'hallucination), et celui qui appartient à ce thème (la borne de détectabilité).
Les fondre aurait été la redite la plus coûteuse possible. Délimitation portée par `args.subject`,
tenue par le document.

**5e déclenchement du garde-fou d'élagage — et la réparation qu'il prescrit était fausse aux trois
quarts.** Sur 9 rejets `refuted:0 / corroborated:2` (les deux jurés tiennent l'énoncé, rejet au
SEUL seuil de sources), « cherche la 2e source » n'était la bonne réponse que pour 2 d'entre eux.
Les trois issues de [[elagage-reparation-prescrite-est-une-hypothese]] se sont réparties ainsi :
- **réparer (2)** : la spike entropy et le régime basse entropie sont corroborés par Lu et al.
  (ACL 2024, arXiv:2403.13485), équipe CUHK/Tsinghua sans lien avec l'UMD — même formule, même
  lecture des extrêmes, vérifié verbatim ;
- **regrainer (7)** : 6 résultats empiriques réellement mono-source (DIPPER 70,3 → 4,6 %, les
  800 tokens après paraphrase, le 61,22 % TOEFL et son mécanisme, la borne d'AUROC) + 1 vrai rejet
  de fond dont les 3 jurés fournissaient la correction (γ=0,25 n'est PAS le point Pareto-optimal :
  le papier écrit « a small green list, γ=.1 is pareto-optimal ») ;
- **accepter (2)** : le 1,6 % du Tableau 2 et la défense par retrieval restent rejetés, aucune
  corroboration n'existe et l'exception document-source ne couvre pas un résultat empirique.

**Leçon neuve, et c'est la plus utile du run : le regrain produit de MEILLEURS claims que les
originaux.** Remonter l'énoncé au niveau du phénomène et faire descendre le chiffre en `example`
attribué ne dégrade pas le fait — il le rend plus vrai et plus intéressant. Trois prises :
(1) « la paraphrase dégrade la détection sans l'effacer » est porté par DEUX travaux indépendants
(Krishna/UMass mesure la chute, Kirchenbauer/UMD le seuil de tokens qui la rattrape) là où chacun
seul était mono-source ; (2) le biais des détecteurs contre les non-natifs, regrainé, réunit les
deux versants du même mécanisme — Liang et al. montrent qu'un texte de non-natif retouché revient
du côté « humain », Wang et al. (JAAD International 2025, corpus tout autre) qu'un texte humain
poli bascule du côté « machine » ; (3) la borne d'AUROC, qui n'était qu'une dérivation
arithmétique en anglais, porte désormais le DÉBAT — Chakraborty et al. (ICML 2024) reprennent
l'inégalité à leur équation (13) pour la juger « too conservative ». **Une réfutation publiée est
la forme la plus forte d'indépendance** : elle ne reprend pas le résultat sur parole, elle le
ré-analyse. Corollaire de méthode : sur un rejet au seuil, chercher qui CONTESTE le résultat vaut
mieux que chercher qui le répète.

⚠️ **3e occurrence de [[acceptance-ignore-le-rang-des-sources]], et la plus large : 14 claims
`confirmed` reposaient sur UNE seule source de rang réel**, la corroboration affichée étant un
wiki de cours, un blog, un résumé auto-généré ou une reprise de presse du travail même que
l'énoncé décrit. `build.success` est sorti FAUX à cause d'eux — le contrôle a fonctionné. À
saluer : l'agent Build a REFUSÉ de déclarer l'exception document-source à leur place, au motif
juste (« la doctrine exige que TOUS les jurés aient qualifié l'énoncé de document_source,
condition invérifiable a posteriori ; l'écrire quand même fabriquerait une conformité »).
Réparés à la main : le survey de Liu et al. (ACM Computing Surveys) corrobore 5 claims KGW d'un
coup en redonnant verbatim la formule du z-score ; la publication primaire dans *Nature* manquait
à l'appareil du claim SynthID principal ; exception document-source déclarée pour le règlement
européen et l'annonce d'OpenAI. **Défauts résiduels assumés, écrits dans les `audit_note`** :
claim:4 et claim:26 gardent une seule source de rang réel (aucune corroboration trouvée dans un
passage vérifiable — les abstracts n'y suffisent pas, et rattacher une source non lue aurait été
pire) ; les 3 claims du règlement citent artificialintelligenceact.eu, reproduction fidèle mais
NON officielle (EUR-Lex tronque à la récupération, je n'ai pas rattaché d'URL non vérifiée) ;
claim:28 et claim:32 sont un quasi-doublon anglais/français sur le classifieur d'OpenAI.

**Défaut de widget trouvé par la revue visuelle, invisible au lint** : la charte pose
`th{background:var(--blue-deep);color:#E7F0F8}` ; le widget `synopsis-tatouage-attaque-verdict`
écrasait la COULEUR des `th` (`--stav-faint`) **sans écraser leur FOND**, d'où une encre gris-bleu
sur bleu profond à **2,48:1**. Corrigé en retirant la déclaration `color` du widget — la charte
gouverne, conformément à « charte = source unique ». Après correction : **0 violation en clair
comme en sombre**. Piège de MESURE re-confirmé au passage ([[charte-blue-deep-double-role]]) : un
`bgOf` qui ne remonte pas le premier arrêt des dégradés fabrique 4 faux positifs sur le bandeau de
titre (encre claire sur dégradé sombre, lue comme encre claire sur fond de page clair).)

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

### Provenance des médias synthétiques — `media-provenance-c2pa` → domaine à trancher
**Verdict : gap réel (ajout 2026-08-31, sorti du 49e run).** Trouvé par la variante faible de
l'heuristique de gap — un objet NOMMÉ puis écarté : `llm-watermarking-detection` consacre une
section au « contrepoint image », y décrit C2PA et les Content Credentials, et s'arrête là parce
que son brief bornait le texte. Couverture du reste du corpus vérifiée **par lecture** (pas au
grep) : `diffusion-models`, `multimodal-vlm`, `world-models` et `generative-adversarial-networks`
comptent **0 phrase de prose** sur la provenance, l'authenticité ou le filigrane — les quatre
monographies qui enseignent à FABRIQUER des images ne disent rien de savoir d'où elles viennent.
Le seul « deepfake » du corpus hors le nouveau thème est un **libellé de lien bibliographique**
dans `generative-adversarial-networks`. Le règlement européen, lui, traite image, audio et vidéo
au même article que le texte.

> La provenance des médias synthétiques : prouver d'où vient une image, un son, une vidéo.
> Couvrir la voie des métadonnées signées (C2PA et les Content Credentials : manifeste
> d'assertions signées cryptographiquement, chaîne de confiance, liaison au contenu par hachage)
> et sa fragilité pratique (dépouillement au ré-upload, recadrage, captures d'écran — ce qu'une
> signature détachée ne survit pas), la voie du filigrane robuste (watermarking d'image dans
> l'espace latent ou fréquentiel, SynthID Image, compromis imperceptibilité/robustesse aux
> transformations géométriques et à la recompression), la détection passive de deepfakes et sa
> course à l'armement (artefacts de génération, généralisation hors distribution, effondrement
> des détecteurs sur des générateurs inédits), et le versant réglementaire côté image/vidéo.
> Public : ingénieur ML / sécurité. ⚠️ Délimitations : `llm-watermarking-detection` couvre le
> TEXTE en propre et pose déjà C2PA comme contrepoint — PARTIR de cette section, ne pas la
> refaire, et reprendre d'elle la distinction marquage-à-la-source / détection-après-coup, qui
> structure aussi ce sujet ; `diffusion-models` et `generative-adversarial-networks` couvrent la
> génération d'images ; `world-models` la simulation. L'angle propre : ce qui accompagne le
> média, pas ce qui le produit. Domaine à trancher par /arrange — `llm-agents-generation` par
> continuité avec le thème texte, ou `deep-learning-foundations` par continuité avec les modèles
> génératifs d'image.

### MinHash & déduplication — `minhash-dedup` → `probabilistic-structures-hashing`
**Verdict : partiel — REMONTÉ de « basse » à « moyenne » le 2026-09-01.** Le corpus le réclame :
`pretraining-data-curation` (section `deduplication-effets`) écrit « La mécanique des signatures,
MinHash et LSH (Locality-Sensitive Hashing), relève d'un autre document ; on la tient ici pour
acquise » — et **aucun des 89 thèmes ne contient « MinHash »** (`approximate-nearest-neighbor`
tient le LSH côté vecteurs ; `consistent-hashing` nomme un « min-hash rapide » pour l'écarter).
C'est l'heuristique du renvoi cassé, la plus fiable du corpus. ⚠️ La théorie LSH a déjà une section dédiée dans
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

### Généralisation en surparamétrisation — `generalisation-double-descent-grokking` → `deep-learning-foundations`
**Verdict : gap réel — le plus net du domaine (ajout 2026-09-01).** Le corpus a les briques
éparses sans le fil : la double descente en une incise de `scaling-laws` (« où la perte remonte puis
redescend avec l'échelle », comme forme que BNSL sait représenter), les minima plats en une phrase de
`quantization` au service du QAT, SAM entre parenthèses dans `normalization-layers`, et le seul
traitement de fond de l'énigme d'interpolation dans `ensemble-learning` — pour le boosting (« l'erreur
de test d'AdaBoost continue de baisser après que l'erreur d'entraînement a atteint zéro […] La théorie
VC prédit l'inverse », résolu par les marges de Schapire). Grokking, ticket de loterie, Belkin,
Nakkiran, benign overfitting, « labels aléatoires » : 0 occurrence.

> Pourquoi les réseaux surparamétrés généralisent : les phénomènes et ce qu'on en comprend. Couvrir
> l'énigme fondatrice (Zhang et al. 2017 : mémoriser des labels aléatoires sans perdre la capacité de
> généraliser), la double descente (Belkin et al. 2019, Nakkiran et al. : double descente en taille de
> modèle, en époques, en données — et le rôle du bruit de label), le grokking (Power et al. 2022 :
> généralisation longtemps après l'ajustement, et ses explications par la norme des poids et les
> circuits), l'hypothèse du ticket de loterie (Frankle & Carbin) comme phénomène de généralisation,
> les minima plats et SAM, le biais implicite de SGD et la régularisation implicite, le benign
> overfitting en régression linéaire, et ce que ces résultats disent — et ne disent pas — de la
> pratique (early stopping, taille de modèle, régularisation). Public : ingénieur ML. Délimitations :
> `scaling-laws` garde les lois de puissance et l'émergence ; `ensemble-learning` garde
> biais-variance classique et les marges du boosting (les citer comme précédent) ;
> `mechanistic-interpretability` garde les circuits (le citer pour le grokking) ; `lora` tient déjà
> le NTK en propriété théorique. Le ticket de loterie est ICI comme phénomène ; le candidat
> `pruning-sparsity` le tient comme méthode. Domaine : deep-learning-foundations.

### Détection et segmentation d'objets — `object-detection-segmentation` → `deep-learning-foundations`
**Verdict : gap réel (ajout 2026-09-01).** Les détecteurs apparaissent six fois en boîte noire, jamais
ouverts : Faster R-CNN comme extracteur de régions dans `document-ai` (« caractéristiques de région
extraites par Faster R-CNN »), RT-DETR sous Docling, « Table Transformer, deux réseaux fondés sur
DETR », RetinaNet et « têtes de détection R-CNN » dans `normalization-layers` (un bug de BN qui fait
tomber « de 39,1 AP à 2,1 AP »), YOLO pour le BN folding, U-Net comme backbone de diffusion, et une
seule trace de SAM (« ViTDet, dérivé de SAM »), jamais expliquée. COCO et ADE20K ne sont que des
bancs dans `convolutional-networks`. Appariement hongrois, NMS, mAP comme construction : absents.

> Détection et segmentation d'objets : localiser, pas seulement classer. Couvrir la lignée à deux
> étages (R-CNN → Fast → Faster : proposition de régions, RPN, ancres, RoIPool/RoIAlign), les
> détecteurs à un étage (YOLO et ses versions, SSD, RetinaNet et la focal loss), la suppression des
> non-maxima et ses pièges, DETR (requêtes d'objets, appariement hongrois, convergence lente) et ses
> descendants, la segmentation sémantique (FCN, U-Net), d'instance (Mask R-CNN) et panoptique, les
> modèles promptables (Segment Anything, SAM 2), les métriques (AP/mAP à seuils d'IoU, mIoU, PQ) et
> ce qu'elles masquent, les jeux (COCO, ADE20K) et leurs biais. Public : ingénieur ML/vision.
> Délimitations : `convolutional-networks` garde le backbone et ConvNeXt/ViT ; `document-ai` garde
> l'analyse de mise en page (le citer : c'est un client) ; `multimodal-vlm` garde le grounding par
> VLM ; `contrastive-self-supervised` garde DINO. Domaine : deep-learning-foundations.

### Exemples adverses et robustesse — `adversarial-examples-robustness` → `deep-learning-foundations`
**Verdict : gap réel — objet nommé puis lâché (ajout 2026-09-01).** `convolutional-networks` referme
`pieges-idees-recues` sur deux phrases : « Szegedy et ses coauteurs montrent dès 2013 qu'une
perturbation imperceptible […] fait basculer la classification » ; « Goodfellow, Shlens et Szegedy
[…] en tirent la FGSM […] et proposent l'entraînement adverse comme défense » — et c'est tout.
`llm-safety-jailbreaks` appelle le sujet sans qu'il existe (« les optimiseurs discrets y sont plus
faibles que dans le domaine continu de l'image ») ; `quantization` traite la robustesse locale L∞
mais pour des QNN vérifiées par ILP. PGD, randomized smoothing, ImageNet-C, Ilyas : 0 occurrence.

> Les exemples adverses et la robustesse des réseaux : une perturbation que l'œil ne voit pas et qui
> change la sortie. Couvrir le phénomène (Szegedy, l'explication linéaire de Goodfellow), les attaques
> en boîte blanche (FGSM, PGD de Madry, C&W) et en boîte noire (transférabilité, requêtes), les
> attaques physiques (patchs, lunettes, panneaux), l'entraînement adverse et son coût en exactitude
> propre (robust overfitting, compromis exactitude/robustesse), les défenses certifiées (randomized
> smoothing de Cohen et al., bornes par relaxation) contre la course aux défenses cassées (obfuscated
> gradients, Athalye et al.), la robustesse aux corruptions naturelles (ImageNet-C) comme problème
> distinct, et le débat « features non robustes » (Ilyas et al.). Public : ingénieur ML/sécurité.
> Délimitations strictes : `llm-safety-jailbreaks` garde le texte discret (GCG, transfert côté texte)
> — le citer pour marquer la frontière continu/discret ; `quantization` garde la vérification
> formelle des QNN ; `mechanistic-interpretability` garde les SAE manipulables. Domaine :
> deep-learning-foundations.

### Apprentissage continu et oubli catastrophique — `continual-learning-catastrophic-forgetting` → `deep-learning-foundations`
**Verdict : gap réel (ajout 2026-09-01).** Le symptôme est mesuré, la discipline absente : `lora`
(section `limites-et-idees-recues`) rapporte le « domain forgetting — un modèle fine-tuné sur Alpaca
perd ses capacités arithmétiques » et les intruder dimensions corrélées « avec l'oubli du
pré-entraînement : ρ = 0,971 » ; `mixture-of-experts` note que geler les couches non-MoE « réduit le
risque d'oubli catastrophique » ; `agentic-memory` cite SWE-Bench-CL avec « forgetting, forward
transfer et backward transfer » sans les définir. EWC, replay, incrémental par classe, Kirkpatrick :
0 occurrence. « Continual Harness » dans `self-improving-harness` est un homonyme.

> Apprendre sans oublier : l'apprentissage continu et l'oubli catastrophique. Couvrir le phénomène
> (McCloskey & Cohen, le dilemme stabilité-plasticité), les scénarios (incrémental par tâche, par
> domaine, par classe — et pourquoi le dernier est le plus dur), les familles de méthodes
> (régularisation : EWC, SI ; rejeu : experience replay, generative replay ; isolation de paramètres ;
> distillation anti-oubli : LwF), les métriques (exactitude moyenne, backward/forward transfer) et
> les pièges d'évaluation (task-ID connu ou non), puis le cas des LLM : l'oubli au fine-tuning,
> l'alignment tax comme oubli, le pré-entraînement continu et les stratégies de rejeu de données.
> Public : ingénieur ML. Délimitations : `lora` garde la mécanique des adaptateurs (citer ses
> mesures d'oubli comme point de départ) ; `knowledge-distillation` garde la distillation comme
> technique (LwF l'emploie, le dire) ; `rlhf-dpo` garde l'over-optimization ; le candidat
> `model-editing-unlearning` traite l'oubli VOULU — se délimiter mutuellement. Domaine :
> deep-learning-foundations.

### Mathématiques formelles par LLM — `llm-formal-math-theorem-proving` → `llm-agents-generation`
**Verdict : gap réel (ajout 2026-09-01).** Le seul « Lean » du corpus est incident (le Defense
Trilemma « est vérifié mécaniquement en Lean 4 avec Mathlib », dans `llm-safety-jailbreaks`).
AlphaProof, AlphaGeometry, miniF2F, PutnamBench, DeepSeek-Prover, autoformalisation : 0 occurrence.
Les voisins tiennent la vérification informelle et posent la motivation sans la suite :
`reasoning-test-time-compute` traite les vérificateurs APPRIS (« un verifier de 6 milliards de
paramètres atteint environ 92 % sur GSM8K ») et écrit que « les méthodes verifier-free […] sont
asymptotiquement sous-optimales par rapport aux méthodes verifier-based » ; `agentic-rl-environments`
s'en tient à la « boîte de réponse en mathématiques ». Ce thème = le vérificateur formel, oracle parfait.

> Les LLM et la démonstration formelle : quand le vérificateur est un assistant de preuve. Couvrir
> l'assistant de preuve comme oracle (Lean/Mathlib, Isabelle, Coq : ce qu'une preuve vérifiée garantit
> et ce qu'elle ne garantit pas — l'énoncé formalisé peut être faux), l'autoformalisation (du langage
> naturel à l'énoncé formel, et ses erreurs silencieuses), la recherche de preuve guidée par le
> vérificateur (recherche arborescente, best-first, expert iteration), les systèmes (AlphaProof et le
> résultat IMO 2024, AlphaGeometry, DeepSeek-Prover, Kimina, Goedel-Prover), le RL à récompense
> binaire prouvée, les benchmarks (miniF2F, PutnamBench, ProofNet) et leurs fuites, la distinction
> entre résoudre un problème d'olympiade et produire des mathématiques nouvelles, et les usages
> (vérification de code, bibliothèques formelles). Public : ingénieur ML. Délimitations strictes :
> `reasoning-test-time-compute` garde les vérificateurs appris et le best-of-N (partir de sa thèse
> verifier-based) ; `agentic-rl-environments` garde le RLVR par boîte de réponse ; `llm-evaluation`
> garde les juges. L'angle propre : l'oracle exact et ce qu'il change à l'entraînement. Domaine :
> llm-agents-generation (portail clos à 20 : /arrange tranchera l'insertion, comme au 49e run).

### Agents d'interface graphique — `computer-use-gui-agents` → `llm-agents-generation`
**Verdict : partiel, gap net sur la mécanique (ajout 2026-09-01).** Les SCORES et la CONSTRUCTION des
benchmarks sont couverts : `agentic-ai` donne la trajectoire OSWorld (« le meilleur agent atteint
12,24 % contre 72,36 % pour les humains […] Agent S3 […] atteint 72,6 % »), WebArena, CUA
« 38,1 % sur OSWorld » ; `agent-evaluation-observability` détaille les vérifications de WebArena et les
« 134 fonctions d'évaluation » d'OSWorld. Mais les deux désignent la cause d'échec sans la traiter :
« les échecs tiennent d'abord au grounding GUI (l'ancrage des intentions dans les bons éléments
d'interface) », « Un agent peut produire un plan parfaitement correct et échouer à cliquer au bon
endroit ». `multimodal-vlm` s'arrête au seuil (« l'agent incarné relève du thème agentic-ai : on
s'arrête »). Set-of-Mark, Mind2Web, arbre d'accessibilité, ScreenSpot, OmniParser : 0 occurrence.

> Les agents qui pilotent une interface graphique : percevoir un écran, choisir une action, vérifier.
> Couvrir l'ancrage visuel (grounding) comme problème central — coordonnées vs marques (Set-of-Mark),
> capture d'écran vs arbre d'accessibilité vs DOM, parseurs d'écran (OmniParser) et modèles de
> grounding (UGround, SeeClick) avec leurs benchmarks (ScreenSpot) —, la conception de l'espace
> d'actions (clic/texte/raccourcis vs code exécuté : CoAct), la boucle perception-action et la
> vérification d'état, les benchmarks web et bureau (Mind2Web, WebArena, OSWorld, WebVoyager) lus
> par leur méthode plutôt que par leurs scores, le RL sur GUI, et les modes d'échec (boucles, actions
> irréversibles, injection par le contenu de la page). Public : ingénieur ML. ⚠️ Délimitations
> strictes : `agentic-ai` garde les scores et la chronologie (les citer, ne pas les redériver) ;
> `agent-evaluation-observability` garde la construction des environnements exécutables ;
> `multimodal-vlm` garde l'architecture VLM ; `agent-harness-engineering` garde la boucle
> générique ; le candidat `vision-language-action` tient la robotique (voisin, pas doublon) ; le
> candidat `agent-tool-security` tient la défense architecturale. L'angle propre : le grounding et
> l'espace d'actions. Domaine : llm-agents-generation.

### Contamination des benchmarks — `benchmark-contamination` → `llm-agents-generation`
**Verdict : gap réel — renvoi cassé A2 (ajout 2026-09-01).** `pretraining-data-curation` écrit :
« Savoir de combien un score publié s'en trouve faussé relève de la mesure, et le document consacré à
l'évaluation des LLM traite ce versant. » Lecture de `llm-evaluation` : une monographie LLM-as-a-judge
(8 sections : modes de jugement, biais de verbosité, auto-préférence, accord juge-humain) où la
contamination tient en trois phrases de « Limites, pièges » concluant que « sa quantification précise
reste inaccessible ». Ce backlog affirmait le 2026-08-01 que ce versant était couvert : il ne l'est
pas. `pretraining-data-curation` tient la décontamination CÔTÉ CORPUS (n-grammes, seuils) ;
`agent-evaluation-observability` tient la contamination des benchmarks d'AGENTS (SWE-bench).

> La contamination des benchmarks : quand le modèle a vu le test. Couvrir les voies de contamination
> (pré-entraînement, fine-tuning sur données synthétiques, rejeu par les utilisateurs), les méthodes
> de détection (chevauchement n-gramme et ses angles morts, détection par vraisemblance ou
> mémorisation — Sainz et al., Golchin & Surdeanu, « Time Travel in LLMs »), la MESURE de
> l'inflation des scores (paires benchmark / version rafraîchie : GSM8K vs GSM1k, MMLU vs variantes
> récentes ; ce que les écarts disent), les réponses de conception (benchmarks dynamiques et datés,
> LiveBench, jeux privés et le problème de confiance, canaries), la saturation et le cycle de vie
> d'un benchmark, et les leaderboards comme incitation. Public : ingénieur ML. ⚠️ Délimitations
> strictes : `pretraining-data-curation` garde la décontamination côté corpus (partir de sa section,
> ne pas la refaire) ; `llm-evaluation` garde le juge ; `agent-evaluation-observability` garde
> SWE-bench et l'écart de harness ; `scaling-laws` garde l'émergence. L'angle propre : mesurer de
> combien, et concevoir contre. Domaine : llm-agents-generation (portail clos : /arrange tranchera).

### Évaluation de la recherche d'information — `evaluation-ir-jugements-pertinence` → `information-retrieval-representation`
**Verdict : partiel, gap large — le socle que six thèmes invoquent sans le poser (ajout
2026-09-01).** Couvert : les formules de DCG/NDCG/MAP/MRR et leur platitude dans `learning-to-rank`
(« leur gradient par rapport aux scores est nul presque partout »), et le biais de pooling comme
artefact des jeux LETOR seulement (« traite comme non pertinents les documents jamais jugés par le
pooling de TREC »). Le corpus cite des dizaines de nDCG@10 sur BEIR/MS MARCO/TREC-DL sans jamais
dire d'où viennent les qrels ; `hybrid-search-reranking` suppose que « quelques dizaines de jugements
de pertinence suffisent », `bm25-inverted-index` renvoie « sur des corpus sans annotations de
pertinence » à des proxys. Cranfield, qrels, bpref, Voorhees, tests de significativité, le débat
LLM-juge de pertinence (Thomas et al./Bing, Faggioli et al., Clarke & Soboroff, UMBRELA) :
0 occurrence — `llm-evaluation` ne traite le juge que pour la génération.

> Évaluer un système de recherche : d'où viennent les jugements, et ce que les métriques supposent.
> Couvrir le paradigme de Cranfield et les collections de test (TREC, MS MARCO et ses jugements
> clairsemés, BEIR), la construction des qrels par pooling et l'incomplétude (bpref, condensed lists,
> et ce que « non jugé » veut dire), l'accord inter-juges (Voorhees) et la stabilité des classements
> de systèmes, les métriques (précision/rappel, MAP, nDCG, MRR, ERR) lues par leurs hypothèses sur
> l'utilisateur, les tests de significativité et la taille des jeux de requêtes, l'évaluation en
> ligne (interleaving, clics et leurs biais) en contrepoint, et le débat 2024-2026 sur les LLM comme
> juges de pertinence (Thomas et al., Faggioli et al., UMBRELA/TREC RAG, l'objection de Clarke &
> Soboroff : circularité et biais). Public : ingénieur ML/recherche. ⚠️ Délimitations strictes :
> `learning-to-rank` garde les formules et le biais LETOR (les citer, ne pas les re-dériver) ;
> `llm-evaluation` garde les biais génériques des juges ; `hybrid-search-reranking` garde BEIR
> comme résultat. L'angle propre : la méthodologie de mesure. Domaine :
> information-retrieval-representation.

### Du langage naturel à la requête structurée — `text-to-sql-semantic-parsing` → `information-retrieval-representation`
**Verdict : gap réel — objet nommé puis laissé (ajout 2026-09-01).** `structured-extraction-llm`
annonce « Trois cas d'usage […] chatbots équipés d'outils externes, conversion langage naturel vers
requêtes structurées, et extraction de données structurées depuis du texte libre. Ce troisième cas
révèle d'emblée la nature du contrat… » — le deuxième n'est jamais développé.
`knowledge-graph-construction` traite les LANGAGES (SPARQL 1.1, GQL ISO/IEC 39075:2024) sans jamais
la génération depuis le langage naturel. Text-to-SQL, Spider, BIRD, schema linking : 0 occurrence.

> Du langage naturel à la requête exécutable : text-to-SQL et parsing sémantique. Couvrir la tâche et
> ses benchmarks (Spider et l'évaluation par correspondance exacte vs exécution, BIRD et les bases
> réalistes, Spider 2.0 et les flux d'entreprise), le schema linking comme cœur du problème (colonnes
> ambiguës, valeurs, jointures implicites), les approches (encodeur-décodeur contraint par la
> grammaire, LLM avec schéma dans le contexte, décomposition, exécution comme oracle et
> auto-correction), les erreurs typiques (requête plausible et fausse, agrégations, NULL), la
> sécurité (injection, droits), l'évaluation (exécution vs sémantique, plusieurs requêtes
> correctes), et l'extension aux graphes (text-to-SPARQL/Cypher). Public : ingénieur ML/data.
> Délimitations : `structured-extraction-llm` garde le schéma JSON en sortie (ici un PROGRAMME
> exécutable) ; `knowledge-graph-construction` garde les langages de graphe ; `agentic-ai` garde
> l'agent qui appelle une base (cas d'usage à citer, pas l'objet). Domaine :
> information-retrieval-representation.

### Plongements de graphes de connaissances — `knowledge-graph-embeddings-link-prediction` → `information-retrieval-representation`
**Verdict : gap réel (ajout 2026-09-01).** Seule trace : `graph-neural-networks` nomme « la prédiction
de liens (link prediction) » comme catégorie OGB (« ogbl-collab, ogbl-citation2 […] Hits@K, MRR ») sans
un mot sur les graphes multi-relationnels. `knowledge-graph-construction` pose l'incomplétude (« un
graphe nécessairement incomplet […] traiter à tort tout fait non encore consigné comme faux ») sans
jamais la traiter comme problème d'inférence. TransE, RotatE, ComplEx, DistMult : 0 occurrence.

> Plonger un graphe de connaissances pour le compléter : les modèles de prédiction de liens et ce
> qu'ils garantissent. Couvrir la tâche (triplets manquants, monde ouvert), les modèles
> translationnels (TransE et ses limites sur les relations 1-N, TransH/R), bilinéaires (DistMult,
> ComplEx et la symétrie), rotationnels (RotatE), et la comparaison avec les GNN relationnels
> (R-GCN, CompGCN), l'entraînement par échantillonnage négatif, le protocole d'évaluation (MRR,
> Hits@k, filtré vs brut) et ses controverses vérifiables (fuite par relations inverses dans FB15k,
> Toutanova & Chen ; « old dog new tricks » de Ruffinelli et al. ; Sun et al. 2020 sur les
> protocoles), l'usage en aval (complétion, recommandation, question-réponse) et les limites
> (entités inédites, échelle). Public : ingénieur ML. Délimitations : `knowledge-graph-construction`
> garde la construction (ici on COMPLÈTE) ; `graph-neural-networks` garde le message passing (citer
> R-GCN) ; `entity-linking-disambiguation` garde le liage. Domaine :
> information-retrieval-representation, entre knowledge-graph-construction et le reste de la chaîne.

### Fonctions de hachage et hachage universel — `fonctions-de-hachage-universelles` → `probabilistic-structures-hashing`
**Verdict : gap réel — désigné deux fois par le corpus (ajout 2026-09-01).** Les six thèmes du domaine
consomment l'hypothèse sans la traiter, et deux le disent : `hyperloglog` (« Sous toutes ces garanties
se cache une hypothèse rarement explicitée dans les guides d'utilisation : les bornes d'erreur de HLL
supposent un hash function qui distribue ses sorties de façon uniforme […] un idéal que peu de
fonctions pratiques satisfont rigoureusement ») et `count-min-sketch` (« les garanties supposent des
hash functions tirées uniformément au hasard et gardées secrètes — une hypothèse souvent ignorée en
déploiement »). Seule trace de k-indépendance : « une famille pairwise independent » en une phrase.
Fonctions concrètes seulement nommées (MurmurHash2, MD5 tronqué, « PRF à clef »). Carter-Wegman,
tabulation, xxHash, SipHash, HashDoS : 0 occurrence. Le fournisseur des six clients.

> Les fonctions de hachage elles-mêmes : ce que « suffisamment aléatoire » veut dire, et ce que ça
> coûte. Couvrir le hachage universel (Carter & Wegman), la k-indépendance et ce que chaque structure
> exige réellement (2-indépendance pour Count-Min, davantage pour les estimateurs de cardinalité, le
> hachage par tabulation de Pătraşcu & Thorup comme compromis), les familles pratiques et leurs
> garanties absentes (MurmurHash, xxHash, CityHash, wyhash : vitesse, qualité empirique, SMHasher),
> le hachage à clef et l'adversaire (HashDoS de 2011, SipHash, pourquoi les langages ont changé
> leur hachage par défaut), la différence avec le hachage cryptographique (résistance aux
> collisions vs uniformité), et les pièges (hachage de flottants, de chaînes, dépendance à
> l'endianness, graines). Public : ingénieur ML/systèmes. Délimitations : les six thèmes du domaine
> sont les CLIENTS (citer leurs hypothèses, ne pas redériver leurs structures) ;
> `approximate-nearest-neighbor` garde le LSH ; `minimal-perfect-hashing` garde la construction
> MPHF. Domaine : probabilistic-structures-hashing — en ouverture du parcours, c'est le socle.

### Structures de données succinctes — `structures-succinctes` → `probabilistic-structures-hashing`
**Verdict : gap réel (ajout 2026-09-01).** Trois objets nommés puis laissés : `bm25-inverted-index`
traite Elias-Fano en un paragraphe comme code de postings (« au plus ⌈log2(U/n)⌉ + 2 bits par
élément […] accès aléatoire en temps constant ») sans la mécanique rank/select qui le fonde ;
`minimal-perfect-hashing` nomme « CacheLineEF » et « les index fondés sur la BWT (Burrows-Wheeler
Transform) » comme repoussoir de SSHash, jamais expliqués ; `pretraining-data-curation` nomme « suffix
array (table des suffixes) » sans le décrire. Rank/select, wavelet tree, FM-index, arbres succincts :
0 occurrence. Thème long (≈ 12 sections) : vérifier le quota WebSearch avant.

> Les structures de données succinctes : tenir dans l'espace de l'information elle-même, sans
> renoncer aux requêtes. Couvrir la borne (espace proche de la borne d'entropie, plus o(n)), les
> bitvecteurs avec rank/select en temps constant (Jacobson, structures à deux niveaux, variantes
> pratiques), Elias-Fano comme structure et non comme code, les wavelet trees (rank/select sur
> alphabet, applications aux index), la transformée de Burrows-Wheeler et le FM-index (recherche de
> motif en temps proportionnel au motif, backward search), tables et arbres de suffixes compressés,
> arbres succincts (LOUDS, parenthèses équilibrées), les bibliothèques (SDSL) et les usages (index
> de recherche, génomique : alignement de lectures), et les compromis réels (constantes, cache).
> Public : ingénieur systèmes/ML. Délimitations : `bm25-inverted-index` garde Elias-Fano comme
> code de postings et PForDelta (le citer, ne pas refaire la compression d'index) ;
> `minimal-perfect-hashing` garde les MPHF ; le candidat `bitmaps-compresses-roaring` tient les
> bitmaps. Domaine : probabilistic-structures-hashing.

### Analyse de survie — `analyse-de-survie` → `classical-ml-time-series`
**Verdict : gap réel — le plus net du domaine (ajout 2026-09-01).** Tous les hits du grep sont des
faux amis vérifiés en lecture : « Cox » est Box-Cox dans `time-series-forecasting`, « churn » est le
code churn d'`ia-productivite-esn`, « hazard » désigne les hazard ratios cités sans méthode par les
thèmes santé (SELECT, REDUCE-IT, TRAVERSE…). `calibration-classifieurs` traite le Brier statique
binaire, pas le Brier dynamique ; `ensemble-learning` nomme « l'analyse de l'abandon dans les cours
en ligne massifs » comme usage de XGBoost et passe. Valeur double : référence ML (churn, panne, délai
de conversion) ET clé de lecture des HR pour les 20 thèmes santé qui les citent.

> L'analyse de survie : prédire quand, avec des observations qu'on n'a pas vues finir. Couvrir la
> censure (à droite, par intervalle, informative ou non) et pourquoi la régression ordinaire se
> trompe, l'estimateur de Kaplan-Meier et le test du log-rank, le modèle de Cox (risques
> proportionnels, vraisemblance partielle, ce que signifie un hazard ratio et ce qu'il ne dit pas :
> absolu vs relatif, non-proportionnalité), les risques concurrents (Fine-Gray, incidence cumulée),
> les métriques (C-index, Brier dynamique, calibration dans le temps), les versions ML (random
> survival forests, gradient boosting de survie, DeepSurv, modèles à temps discret) et leurs
> pièges (fuite temporelle, biais du temps immortel), et les applications hors médecine (churn,
> maintenance prédictive, délai de conversion). Public : ingénieur ML/data. Délimitations :
> `calibration-classifieurs` garde le Brier statique et la couverture conforme (les citer) ;
> `ensemble-learning` garde le boosting ; `time-series-forecasting` ne touche jamais aux données
> censurées — frontière nette ; le candidat `causal-inference` garde l'identification d'effets.
> Domaine : classical-ml-time-series.

### Explicabilité post-hoc — `explicabilite-shap-lime` → `classical-ml-time-series`
**Verdict : partiel, gap large (ajout 2026-09-01).** Couvert (à citer, ne pas refaire) : le biais MDI
et la comparaison permutation / drop-column sur variables corrélées dans `ensemble-learning`
(section `importance-variables`, Strobl 2007/2008), les Variable Selection Networks du TFT dans
`time-series-forecasting`. `mechanistic-interpretability` pose lui-même la frontière : Olah forge le
terme « pour distinguer cette démarche […] des méthodes alors dominantes de l'IA interprétable : les
saliency maps ». SHAP, Shapley, TreeSHAP, LIME, PDP, ICE, Rashomon : 0 occurrence.

> Expliquer un modèle tabulaire après coup : ce qu'une explication garantit, et ce qu'elle ne
> garantit pas. Couvrir les valeurs de Shapley (axiomes, coût exponentiel) et SHAP (KernelSHAP,
> TreeSHAP, interventionnel vs observationnel et le débat sur les variables corrélées), LIME et son
> instabilité, l'importance par permutation et ses pièges (déjà posés pour les forêts — partir de
> là), PDP/ICE et l'extrapolation hors support, les explications contrefactuelles, l'ensemble de
> Rashomon (plusieurs modèles également bons, explications différentes), les attaques sur les
> explications et la fidélité, et l'usage réglementaire (droit à l'explication) contre ce que la
> méthode permet. Public : ingénieur ML/data. Délimitations strictes : `ensemble-learning` garde
> l'importance des variables des forêts (citer, une phrase) ; `mechanistic-interpretability` garde
> les réseaux et les circuits (l'opposition post-hoc/mécanistique est le point de départ) ;
> `tabular-foundation-models` garde TabPFN. Domaine : classical-ml-time-series.

### Expérimentation en ligne et tests A/B — `ab-testing-experimentation-en-ligne` → `classical-ml-time-series`
**Verdict : gap réel — objet nommé puis lâché (ajout 2026-09-01).** `time-series-forecasting` cite en
fin de phrase « (détection d'anomalies, expérimentation bayésienne, A/B testing séquentiel) » et n'y
revient pas ; `hyperloglog` traite un coin précis (tests A/A sur comptes distincts estimés, « 43,86 %
[…] unsuitable for use in A/B testing ») ; `learning-to-rank` nomme l'interleaving et rapporte des
gains d'A/B sans méthodologie ; CausalImpact dans `time-series-forecasting` est le complément exact
(« quand un essai contrôlé randomisé est impossible »). Peeking, tests séquentiels, CUPED, MDE, delta
method : 0 occurrence. ⚠️ Deux frontières à écrire dans le brief contre les candidats
`causal-inference` et `multi-armed-bandits`.

> Les statistiques de l'expérimentation en ligne : décider à partir d'un test A/B sans se tromper
> sur ce qu'il prouve. Couvrir le plan (randomisation par unité, puissance et effet minimal
> détectable, durée), le problème du « peeking » et ses remèdes (tests séquentiels, mSPRT, p-values
> toujours valides de Johari et al., approches bayésiennes), la réduction de variance (CUPED,
> stratification), les métriques de ratio et la delta method, les interférences et effets de
> réseau (violation de SUTVA, randomisation par grappes, marchés à deux faces), les tests A/A et la
> validation de la plateforme, les pièges (multiplicité, effet de nouveauté, biais de survie,
> métriques de garde) et les plateformes d'expérimentation. Public : ingénieur ML/data.
> ⚠️ Délimitations strictes : ce thème traite l'expérience RANDOMISÉE À ALLOCATION FIXE —
> l'allocation adaptative relève de `multi-armed-bandits` (candidat) ; l'identification d'effets
> sans randomisation (propension, DiD, IV, DML, effets hétérogènes) relève de `causal-inference`
> (candidat) ; `time-series-forecasting` garde CausalImpact (le citer en contrepoint) ;
> `hyperloglog` garde son cas de comptage. Domaine : classical-ml-time-series.

---

## Priorité basse / marginale

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

### Élagage et parcimonie — `pruning-sparsity` → `deep-learning-foundations`
**Verdict : gap réel avec un chevauchement à borner (ajout 2026-09-01).** `knowledge-distillation`
couvre le pruning structuré RÉPARÉ par distillation (Llama 3.2 « réduit par un pruning structuré en une
passe », Minitron « width-pruned », « depth-pruned »), sous l'angle réparation ; `sparse-attention-long-context`
cite Deep Compression en une phrase pour l'EXCLURE de son périmètre ; `quantization` frôle la lignée
OBS/OBD via GPTQ. 2:4, SparseGPT, Wanda, magnitude pruning, sparsité d'activation : 0 occurrence.

> L'élagage des réseaux : retirer des poids sans perdre le modèle. Couvrir le magnitude pruning et
> le cycle train-prune-retrain, structuré vs non structuré et pourquoi le matériel décide (2:4 des
> Tensor Cores), la lignée OBD/OBS et ses héritiers one-shot pour les LLM (SparseGPT, Wanda), le
> ticket de loterie comme MÉTHODE (le candidat `generalisation-double-descent-grokking` le tient
> comme phénomène — trancher avant de lancer), la sparsité d'activation, et l'évaluation honnête
> (accélération réelle vs paramètres retirés). Délimitations : `knowledge-distillation` garde la
> réparation post-pruning (Minitron : citer, ne pas refaire) ; `mixture-of-experts` garde la
> parcimonie d'experts ; `sparse-attention-long-context` garde le motif d'attention ; `quantization`
> garde la précision. Domaine : deep-learning-foundations.

### Deep learning bayésien et incertitude — `bayesian-deep-learning-uncertainty` → `deep-learning-foundations`
**Verdict : partiel — le plus exposé au chevauchement (ajout 2026-09-01).** La dichotomie est posée
en un paragraphe de `hallucination-detection-uncertainty` (« l'incertitude épistémique — ce que le
modèle ignore, par opposition à l'incertitude aléatoire […] un ensemble de modèles entraînés
indépendamment ; l'option est jugée "prohibitivement coûteuse" pour les LLM ») ; `calibration-classifieurs`
tient le post-hoc et le conformal ; `tabular-foundation-models` tient l'inférence bayésienne AMORTIE.
MC dropout, deep ensembles (Lakshminarayanan), Laplace, SWAG, BNN variationnel, détection OOD :
0 occurrence (« Laplace » = transformée dans `state-space-models`).

> Quantifier l'incertitude d'un réseau : les méthodes bayésiennes et leurs approximations. Couvrir
> la décomposition épistémique/aléatoire, les BNN par inférence variationnelle (Bayes by Backprop),
> MC dropout (Gal & Ghahramani) et sa critique, les deep ensembles et le débat « ensembles ≈
> Bayes ? », Laplace/SWAG/SWA, la détection hors distribution (softmax, ODIN, Mahalanobis) et ses
> benchmarks, l'évaluation (log-vraisemblance, calibration sous décalage) et le coût. Délimitations
> strictes (quatre frontières) : `hallucination-detection-uncertainty` garde l'UQ des LLM en boîte
> noire ; `calibration-classifieurs` garde le post-hoc et le conformal ; `variational-autoencoders`
> garde l'ELBO génératif ; `tabular-foundation-models` garde l'inférence amortie ; `ensemble-learning`
> garde bagging/boosting (les deep ensembles y renvoient). Domaine : deep-learning-foundations.

### Génération non autorégressive de texte — `non-autoregressive-generation` → `deep-learning-foundations` (ou regrain)
**Verdict : gap réel — renvoi cassé A1 (ajout 2026-09-01).** `diffusion-language-models` écrit : « la
génération parallèle masquée existe aussi de ce côté-là, et la monographie consacrée au décodage la
traite — le pont existe dans les deux sens, nous n'y revenons pas. » `decoding-sampling` lu en entier :
du greedy au décodage spéculatif (Medusa, EAGLE, lookahead) ; le seul « masque » est le masque causal
arborescent de Medusa ; « non autorégressif », « Mask-Predict », « CMLM » : 0 occurrence. Valeur de
référence 2026 modeste (le versant diffusion discrète est déjà tenu) : **alternative recevable, un
regrain d'une section de `decoding-sampling`** qui répare le renvoi à moindre coût.

> La génération non autorégressive de texte : produire plusieurs tokens à la fois. Couvrir le
> problème de multimodalité (Gu et al. 2018 : sorties incohérentes quand les positions décident
> indépendamment), Mask-Predict/CMLM et le raffinement itératif, le décodage par blocs et les
> compromis latence/qualité mesurés (traduction automatique), la distillation séquentielle comme
> béquille, et les ponts vers la diffusion discrète et le décodage spéculatif. Délimitations
> strictes : `diffusion-language-models` garde la diffusion masquée (le citer comme descendance) ;
> `decoding-sampling` garde le spéculatif (accélérer un modèle autorégressif ≠ changer la
> factorisation). Domaine : deep-learning-foundations, ou section ajoutée à decoding-sampling.

### LLM multilingues et langues peu dotées — `llm-multilingue-basses-ressources` → domaine à trancher
**Verdict : gap réel sur le cœur, périphérie déjà occupée (ajout 2026-09-01).** Fragments à citer :
« surcoût d'API pour les langues non anglaises (plus de tokens par mot) » en une proposition de
`text-embeddings`, jamais quantifiée ; le jailbreak par langues peu dotées traité à fond dans
`llm-safety-jailbreaks` (« 79 % sur AdvBench […] culmine en zoulou ») ; l'identification de langue
comme plus grosse coupe du pipeline dans `pretraining-data-curation` ; « La dégradation s'accentue
sur les entrées non-anglaises » dans `quantization`. `llm-evaluation` ne contient RIEN de multilingue.
Curse of multilinguality, XLM-R, FLORES, prime de tokenisation mesurée : 0 occurrence.

> Les modèles de langage hors anglais : ce que coûte une langue, et ce qu'on lui transfère. Couvrir
> la prime de tokenisation mesurée par langue (Petrov et al. : jusqu'à plusieurs fois plus de tokens
> par phrase, conséquences en coût, contexte et qualité), le transfert inter-langues et la « curse of
> multilinguality » (Conneau et al., XLM-R), le mélange de langues en pré-entraînement et
> l'échantillonnage par température, l'évaluation multilingue (benchmarks traduits et leurs biais
> culturels, Global MMLU, MGSM), les langues à faibles ressources (FLORES-200, NLLB, données
> synthétiques par traduction), et les modèles régionaux. Délimitations : quatre renvois sortants —
> `llm-safety-jailbreaks` (jailbreak multilingue), `pretraining-data-curation` (filtre de langue),
> `quantization` (dégradation), `text-embeddings` (BPE) ; le candidat
> `recherche-multilingue-cross-lingual` tient le versant recherche. Domaine à trancher par /arrange :
> deep-learning-foundations (le sujet est plus « modèle » qu'« agent ») ou llm-agents-generation.

### Recherche inter-langues — `recherche-multilingue-cross-lingual` → `information-retrieval-representation`
**Verdict : gap réel, un seul paragraphe adjacent (ajout 2026-09-01).** `hybrid-search-reranking`
donne BGE-M3 « 70,0 de nDCG@10 sur 18 langues du benchmark MIRACL » — MIRACL y est un chiffre, pas
un objet ; `text-embeddings` n'a aucune section multilingue (fastText « 157 langues », SentencePiece
en passant). mDPR, mContriever, LaBSE, traduction de requête : 0 occurrence. Littérature plus mince
et plus mono-source que les autres candidats IR.

> Retrouver dans une langue ce qui est écrit dans une autre. Couvrir les stratégies (traduire la
> requête, traduire les documents, espace d'embeddings aligné), l'alignement inter-langues
> (LaBSE, mContriever, mE5, BGE-M3) et sa fuite vers l'anglais, les benchmarks (MIRACL, Mr. TyDi,
> CLEF) et ce qu'ils mesurent, le cas des langues peu dotées et la tokenisation, et le reranking
> multilingue. Délimitations : `text-embeddings` garde l'alignement mono-langue ;
> `hybrid-search-reranking` garde BGE-M3 comme résultat ; le candidat
> `llm-multilingue-basses-ressources` tient le versant génération. Domaine :
> information-retrieval-representation.

### Expansion et réécriture de requête — `query-expansion-rewriting` → `information-retrieval-representation`
**Verdict : partiel — la moitié classique entièrement absente, la moitié LLM déjà dans RAG (ajout
2026-09-01).** `retrieval-augmented-generation` tient HyDE (« poussant le nDCG@10 de 44,5 à 61,3 »,
repris sans réserve), RAG-Fusion, RQ-RAG et la réécriture conversationnelle ; `hybrid-search-reranking`
tient l'expansion implicite de SPLADE ; `bm25-inverted-index` pose le vocabulary mismatch. Rocchio,
RM3, pseudo-relevance feedback (une seule mention historique), doc2query, query2doc, PRF dense, et le
résultat « l'expansion nuit aux retrievers forts » : 0 occurrence. **Ne lancer qu'avec un brief qui
interdit de redire HyDE/RAG-Fusion** et centre sur le PRF classique et « quand l'expansion nuit ».

> L'expansion de requête, de Rocchio au LLM : combler l'écart de vocabulaire, et savoir quand ça
> nuit. Couvrir le relevance feedback et le pseudo-relevance feedback (Rocchio, RM3), l'expansion
> côté document (doc2query, docT5query) contre côté requête (query2doc), le PRF sur représentations
> denses (ANCE-PRF, ColBERT-PRF), et le résultat contre-intuitif que l'expansion par LLM dégrade les
> retrievers forts (Weller et al. 2024) — avec ses conditions. Délimitations strictes :
> `retrieval-augmented-generation` garde HyDE, RAG-Fusion, RQ-RAG et les variantes agentiques (les
> citer en une phrase, NE PAS les redérouler) ; `hybrid-search-reranking` garde SPLADE ;
> `bm25-inverted-index` garde le vocabulary mismatch. Domaine : information-retrieval-representation.

### Bitmaps compressés — `bitmaps-compresses-roaring` → `probabilistic-structures-hashing`
**Verdict : gap réel, valeur d'ingénierie (ajout 2026-09-01).** Roaring, bitmap, bitset, WAH, EWAH :
0 occurrence. `bm25-inverted-index` (section `recherche-efficace`) couvre la compression de postings
(d-gap, PForDelta, décodage SIMD, WAND) — jamais la représentation par bitmap ; traces annexes :
l'algèbre OU/ET des filtres de Bloom, le run-length encoding de Redis dans `hyperloglog`.

> Les bitmaps compressés : représenter un ensemble d'entiers par ses bits, et le comprimer sans
> perdre les opérations. Couvrir les bitmaps alignés par mots (WAH, EWAH) et leurs limites, Roaring
> (conteneurs array/bitmap/run, choix par densité, opérations ensemblistes vectorisées), la
> comparaison mesurée avec les listes de postings compressées (quand le bitmap gagne, quand il
> perd), et les usages (Lucene/Elasticsearch, ClickHouse, Druid, index de colonnes). Délimitations :
> `bm25-inverted-index` garde d-gap/PForDelta/WAND (partir de sa section, contraster) ;
> `bloom-filters` garde l'appartenance approchée ; le candidat `structures-succinctes` tient
> rank/select. Domaine : probabilistic-structures-hashing. Run lean.

### Heavy hitters déterministes — `heavy-hitters-deterministes` → `probabilistic-structures-hashing`
**Verdict : gap réel, contrairement à l'attendu, mais étroit (ajout 2026-09-01).** Ce backlog
supposait le sujet couvert par `count-min-sketch` : lu, il traite les heavy hitters par CMS dyadique
(Théorème 6) puis écrit que l'énumération « requiert soit une liste de candidats fournie à l'avance,
soit une structure auxiliaire distincte ; l'énumération native n'est pas prise en charge » — sans la
nommer. Misra-Gries et SpaceSaving n'apparaissent qu'en une phrase de `streaming-quantiles-sampling`
(« isomorphes l'un à l'autre, sont déterministes, pleinement mergeables ») ; Lossy Counting :
0 occurrence. Run court, ou à coupler dans un thème « frequent items ».

> Trouver les éléments fréquents d'un flux sans hasard : Misra-Gries, SpaceSaving, Lossy Counting.
> Couvrir le problème (φ-heavy hitters, garantie déterministe d'erreur ε), Misra-Gries et sa preuve,
> SpaceSaving et son isomorphisme, Lossy Counting, la fusionnabilité (Agarwal et al.), la
> comparaison honnête avec CMS + tas (mémoire, faux positifs, garanties), et les implémentations
> (Frequent Items de DataSketches). Délimitations : `count-min-sketch` garde le sketch et le CMS
> dyadique (partir de sa section « limites ») ; `streaming-quantiles-sampling` garde les quantiles.
> Domaine : probabilistic-structures-hashing.

### Sketching linéaire et feature hashing — `sketching-lineaire-feature-hashing` → `probabilistic-structures-hashing`
**Verdict : partiel — ne lancer qu'en le recentrant (ajout 2026-09-01).** AMS/F2 (deux paragraphes,
« prix Gödel en 2005 ») et Count Sketch (un paragraphe, « borne l'erreur en norme L2 ») sont déjà le
cœur de deux sections de `count-min-sketch` ; le lemme JL et l'optimalité de Larsen-Nelson sont dans
`text-embeddings` ; E2LSH par projection gaussienne dans `approximate-nearest-neighbor`. Absents :
hashing trick / feature hashing (0 hit), JL parcimonieux, sketching pour la régression, moments Fk.

> Les projections aléatoires et le sketching linéaire : réduire la dimension sans regarder les
> données. Couvrir le lemme de Johnson-Lindenstrauss (énoncé, preuve par concentration, JL
> parcimonieux et rapide), le feature hashing (Weinberger et al. : le hashing trick, collisions et
> biais, usage en apprentissage en ligne), les sketches pour l'algèbre linéaire (régression par
> sketch, CountSketch comme projection, subspace embeddings), et les moments de fréquence au-delà
> de F2. ⚠️ Délimitations strictes : `count-min-sketch` tient AMS et Count Sketch (les citer, NE PAS
> les redériver) ; `text-embeddings` tient JL et son optimalité (partir de là) ;
> `approximate-nearest-neighbor` tient E2LSH ; `clustering-dimensionality-reduction` tient PCA.
> Domaine : probabilistic-structures-hashing.

### Tables de hachage dynamiques — `hash-tables-dynamiques` → `probabilistic-structures-hashing`
**Verdict : gap réel — objet écarté B2 (ajout 2026-09-01).** `minimal-perfect-hashing` referme
`limites-et-pieges` sur « Les cas d'usage naturels sont donc les ensembles gelés […] Les ensembles
dynamiques relèvent d'autres structures » — sans cible. Le candidat `cuckoo-filter` est une structure
d'appartenance, pas une table. Chaînage, adressage ouvert, cuckoo hashing, hachage extensible, Robin
Hood : 0 occurrence. Donnerait au domaine son 7e thème, par le contraire de la MPHF.

> Les tables de hachage dynamiques : le contraire de l'ensemble gelé. Couvrir chaînage vs adressage
> ouvert (sondage linéaire et l'effet des caches, Robin Hood), le cuckoo hashing (deux fonctions,
> relocalisation, seuil de charge et ses preuves), le hachage extensible et linéaire (croissance
> sans réhachage global), les tables des langages et bibliothèques (Swiss tables, F14) et leurs
> choix, et les attaques (HashDoS, renvoi au candidat hachage universel). Délimitations :
> `minimal-perfect-hashing` garde l'ensemble gelé (partir de sa clôture) ; le candidat
> `cuckoo-filter` garde l'appartenance approchée avec empreintes ; `consistent-hashing` garde la
> répartition entre nœuds. Domaine : probabilistic-structures-hashing.

### Optimisation des hyperparamètres et AutoML — `optimisation-hyperparametres-automl` → `classical-ml-time-series`
**Verdict : partiel — nommé partout, expliqué nulle part ; recouvrement à arbitrer (ajout
2026-09-01).** µP en un paragraphe de `scaling-laws` (MiniCPM « transférés sans nouveau réglage »),
un grid search exemplaire sur k1/b dans `bm25-inverted-index`, AutoML nommé quatre fois comme
comparateur dans `tabular-foundation-models` (« AutoGluon Extreme (ensemble de 4 heures) ») sans être
défini, hyperparamètres critiques listés par `ensemble-learning` sans méthode de réglage. Bergstra &
Bengio, TPE, Hyperband/ASHA, NAS : 0 occurrence. ⚠️ Le candidat `gaussian-processes` réclame
« l'application phare : l'optimisation bayésienne » — trancher qui la porte AVANT de lancer.

> Régler les hyperparamètres : ce que chaque méthode achète, et à quel prix. Couvrir grid vs random
> search (Bergstra & Bengio : pourquoi l'aléatoire gagne), l'optimisation bayésienne (TPE, SMAC, GP
> avec EI/UCB — en renvoi ou en propre selon l'arbitrage), les méthodes à budget (successive
> halving, Hyperband, ASHA, arrêt précoce), le transfert d'hyperparamètres (µP — citer scaling-laws),
> la recherche d'architecture (NAS et sa crise de reproductibilité), AutoML (AutoGluon, ce qu'un
> « ensemble de 4 heures » signifie) et l'évaluation honnête (validation imbriquée, fuite par
> réglage sur le test). Délimitations : `scaling-laws` garde µP ; `tabular-foundation-models` garde
> TabPFN et cite AutoGluon ; `ensemble-learning` garde le boosting ; `gaussian-processes` (candidat)
> — à arbitrer. Domaine : classical-ml-time-series.

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


Écartés lors de la passe du 2026-09-01, chacun sur lecture de la prose (agents-lecteurs, un par
domaine) :

- **Décodage contraint / sorties structurées** → `structured-extraction-llm` couvre chaque point :
  mécanique et coût (« les logits des tokens invalides sont mis à −∞ », XGrammar « moins de 40 µs par
  token »), effet sur le raisonnement (« 75,99 % en texte libre à 49,25 % sous JSON-mode »),
  JSONSchemaBench à six moteurs, function calling strict ; `decoding-sampling` y délègue
  explicitement. Reste trop mince pour un run : l'alignement grammaire/tokens BPE — une section.
- **Expériences de terrain hors code (support client, rédaction, consultants)** →
  `ia-productivite-esn`, section `distribution-des-gains` (Brynjolfsson/Li/Raymond « +15 % […] le
  quintile inférieur +36 % », Dell'Acqua « 19 points de pourcentage moins susceptibles », Noy &
  Zhang « −40 % de temps, +18 % de qualité »). Un thème doublonnerait une section et demie.
- **Adoption de l'IA en entreprise et ROI** → même document, `paradoxe-adoption-valeur` et
  `projections-futures` (McKinsey « 88 % […] 6 % », NBER « plus de 80 % sans impact », J-curve).
  Ne manquent que MIT NANDA et Census BTOS : une section, pas un thème.
- **Nicotine comme nootropique** → `nootropiques-panorama`, substance 10 des 25, section dédiée
  (Heishman 2010 « g 0,39 », Majdi 2021, Newhouse 2012, financement tabac) : « la nicotine porte le
  meilleur dossier cognitif » hors ordonnance. Rien à ajouter.
- **Sommeil et performance cognitive** → partiel à la frontière du doublon : `cafeine-cognition-vigilance`
  tient privation, travail posté, sieste caféinée et effet en retour sur QUATRE sections. Reste vide :
  hypnotiques, extension de sommeil, dose-réponse de Van Dongen 2003 — et la mélatonine, qui a son
  candidat en `complements-sante`.
- **Exercice physique et cognition** → gap réel (Erickson, Ciria 2023 : 0 occurrence) mais MAL LOGÉ :
  l'exercice est déjà revendiqué par `sarcopenie-exercice-nutrition` et par le candidat
  `graisse-viscerale-homme-age` ; un troisième document sur l'exercice se range mal dans un méta
  découpé par produit. À reprendre si un domaine « exercice » émerge.
- **BCAA / EAA / leucine** → `proteines-besoins-timing` (seuil de leucine « autour de 2,5 g […] et
  3 g chez l'âgé », « leucine trigger » partiellement confirmé, essai Lynch à leucine égalisée) et
  `sarcopenie-exercice-nutrition` (Guo : « aucun effet du supplément seul »). Reste : les BCAA
  vendus seuls — une section de `proteines-besoins-timing`, pas un thème.
- **Suppléments anti-sarcopénie (HMB, créatine de l'âgé, vitamine D + protéines, oméga-3)** →
  `sarcopenie-exercice-nutrition`, sections `reste-du-rayon` (Li 2025 « +0,28 kg », umbrella review,
  DO-HEALTH, VITAL) et `creatine-60-plus`. Au plus un widget.
- **Aphrodisiaques du rayon sexuel (maca, tribulus, yohimbine…)** → les plantes sont absentes, mais
  la moitié forte (l'adultération) est écrite TROIS fois (`inhibiteurs-pde5` : Tucker 2018
  « 776 produits […] 45,5 % » ; `complements-amincissants` ; `nootropiques-panorama` : « instruite
  ailleurs dans ce corpus et n'a pas à être redéroulée »), et le thème PDE5 énonce la thèse : « Une
  plante ne produit pas l'effet ; la molécule, si ». Un run redirait la moitié forte et rejetterait la
  moitié neuve par carence.
- **Pipeline GLP-1 de nouvelle génération** → `incretines-glp1`, section `pipeline-retatrutide`
  (18 000 caractères : rétatrutide et TRIUMPH-1/3/4, orforglipron « approuvé par la FDA le 1er avril
  2026 sous le nom de Foundayo », CagriSema/REDEFINE 1, la règle du communiqué de promoteur). Ne
  manquent que sémaglutide oral 25/50 mg, amycrétine, MariTide, survodutide : un REGRAIN de section,
  pas un run. ⚠️ Objet nommé trois fois et jamais traité : le rétatrutide de contrebande (Santé Canada
  dans `peptides-gris`, alerte ANSM de juillet 2026 dans `testosterone-homme-age`) — à verser dans ce
  regrain ou dans le candidat `medicaments-contrefaits-en-ligne`.
- **Recherche sur documents-images (ColPali)** → différé : `document-ai` a un paragraphe que la prose
  qualifie elle-même de « source unique, non corroborée par une évaluation indépendante » ; sujet
  jeune (2024-2026), risque élevé de rejets par carence. À reprendre comme section d'un thème plus
  large ou quand ViDoRe v2 aura ses répliques.

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

**Ordre de lancement** — mis à jour le 2026-08-30 (nos 1 à 7, 10 et 11 sont FAITS ; restent 8, 9 et 12) :

| # | thème | priorité | domaine |
|---|---|---|---|
| ~~1~~ | ~~`sarcopenie-exercice-nutrition`~~ | FAIT 2026-08-18 | `muscle-vieillissement` (domaine créé) |
| ~~2~~ | ~~`testosterone-homme-age`~~ | FAIT 2026-08-19 | `muscle-vieillissement` (portail ouvert) |
| ~~3~~ | ~~`nootropiques-vegetaux`~~ | FAIT 2026-08-26 | `performance-cognitive` (**portail ouvert**) |
| ~~4~~ | ~~`inhibiteurs-pde5`~~ | FAIT 2026-08-27 | `fonction-sexuelle` (**domaine créé** ; portail ouvert au no 5) |
| ~~5~~ | ~~`ejaculation-precoce`~~ | FAIT 2026-08-29 | `fonction-sexuelle` (**portail ouvert** — chantier du 43e run refermé) |
| ~~6~~ | ~~`cafeine-cognition-vigilance`~~ | FAIT 2026-08-27 | `performance-cognitive` (3e thème du domaine) |
| ~~7~~ | ~~`omega-3`~~ | FAIT 2026-08-30 | `complements-sante` (3e thème, **2e du parcours**) |
| 8 | `acide-alpha-lipoique` | moyenne-haute | `complements-sante` |
| 9 | `beta-alanine-tampons` | moyenne | `nutrition-sportive` |
| ~~10~~ | ~~`microdosage-psychedeliques`~~ | FAIT 2026-08-27 | `performance-cognitive` (4e thème du domaine) |
| ~~11~~ | ~~`nootropiques-panorama`~~ | FAIT 2026-08-28 | `performance-cognitive` (**capstone : REFERME le domaine à 5 thèmes**) |
| 12 | `magnesium`, `hydratation-electrolytes` | basses | — |

**Arbitrage assumé** : les deux thèmes muscle passent devant `nootropiques-vegetaux`, qui était en
tête depuis le 2026-08-15. Ils coûtent plus cher (deux runs au lieu d'un) et laissent
`performance-cognitive` à moitié né **deux tours de plus** — mais ils créent un domaine
**complet, portail inclus**, sur un gap plus large, et leur fil rouge est le mieux mesuré que ce
backlog ait proposé (voir la section du domaine). `nootropiques-vegetaux` garde sa priorité haute
et reste le run le moins cher pour refermer le chantier `performance-cognitive` :
**si le budget ne permet qu'un seul run, le lancer lui.**

⚠️ **Priorité révisée le 2026-08-27, appliquée puis close le 2026-08-29.** `ejaculation-precoce`
était passé en tête parce que le 43e run avait créé `fonction-sexuelle` avec UN seul thème, donc
sans portail — et que l'histoire de `performance-cognitive`, ouvert au 39e run et refermé seulement
au 42e, dit ce que coûte un chantier laissé ouvert. Le 47e run l'a fabriqué et a ouvert le portail :
**la règle reste valable — le 2e thème d'un domaine neuf passe avant la tête de file d'un domaine
déjà complet — mais elle n'a plus de candidat à qui s'appliquer.** Les 12 domaines ont leur portail
à l'exception d'`ai-organizations` (1 seul thème, `ia-productivite-esn`), pour lequel ce backlog ne
propose aucun candidat : l'y appliquer suppose d'abord d'en instruire un.

**Ordre de lancement — RÉVISÉ le 2026-09-01** (candidats de la passe du jour ; les nos 8, 9 et 12
ci-dessus restent valables et sont reclassés dans cette table) :

| # | thème | priorité | domaine | pourquoi en tête |
|---|---|---|---|---|
| 1 | `glp1-hors-poids` | haute | `pharmacologie-metabolique` | le pivot nomme le piège lui-même ; 5 phases 3 publiées (FLOW, STEP-HFpEF, SURMOUNT-OSA, ESSENCE) + 1 échec (EVOKE) : seuil ≥ 2 atteignable |
| 2 | `desir-sexuel-hypoactif` | haute | `fonction-sexuelle` | 3 objets nommés désignent le désir ; corrige l'asymétrie homme/femme ; saga FDA d'école |
| 3 | `osteoporose-pharmacologie` | haute | `muscle-vieillissement` (blurb à élargir à l'os) | la thèse du domaine (le substitut ne prédit pas) écrite 3 fois, jamais éprouvée sur les molécules faites POUR l'os |
| 4 | `nitrates-betterave` | moyenne-haute | `nutrition-sportive` | seul membre du Groupe A de l'AIS sans candidat, nommé 2 fois par le corpus |
| 5 | `melatonine` | moyenne-haute | `complements-sante` | mot absent du corpus ; ouvre la cible « sommeil » qu'aucun domaine ne porte |
| 6 | `acide-alpha-lipoique` | moyenne-haute | `complements-sante` | inchangé (no 8 ci-dessus) |
| 7 | `fer-supplementation` | moyenne | `complements-sante` | miroir exact de `vitamine-d` (seuils contestés) avec un bénéfice réel et un vrai risque |
| 8 | `entrainement-cognitif-commercial` | moyenne | `performance-cognitive` (rouvrir UNE fois) | gap total ; l'amende FTC Lumosity fait pendant au veto sur l'allégation caféine |
| 9 | `medicaments-du-poids-retires` | moyenne | `pharmacologie-metabolique` | 85 % neuf ; le Mediator, angle français absent du corpus |
| 10 | `dysfonction-erectile-hors-pde5` | moyenne | `fonction-sexuelle` | zéro recouvrement ; « quand le comprimé ne suffit pas » |
| 11 | `multivitamines`, `probiotiques` | moyenne | `complements-sante` | grands RCT nommables / littérature par souche (run coûteux) |
| 12 | `disponibilite-energetique-reds` | moyenne | `nutrition-sportive` | corrige le biais masculin ; preuve surtout de consensus |
| 13 | `beta-alanine-tampons`, `medicaments-contrefaits-en-ligne`, `metformine-rapamycine-longevite` | moyenne | voir entrées | — |
| 14 | `menopause-hormonotherapie` | moyenne | **domaine à créer** | tête de file d'un domaine « santé de la femme » |
| 15 | `chutes-fragilite-prevention`, `nad-nmn-precurseurs`, `curcumine`, `glucides-pendant-l-effort`, `magnesium`, `hydratation-electrolytes` | basses | voir entrées | — |

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


### Nitrate alimentaire et jus de betterave — `nitrates-betterave` → `nutrition-sportive`
**Verdict : gap réel — objet nommé deux fois puis laissé (ajout 2026-09-01).** Le nitrate n'apparaît
que dans deux listes : `creatine` (« range la créatine dans le Groupe A de son cadre de classification
ABCD […] aux côtés de la caféine, de la bêta-alanine, du bicarbonate, du jus de betterave et du
glycérol ») et `cafeine-ergogene` (« liste courte, et notable surtout par ce qu'elle exclut »), plus la
créatine-nitrate écartée comme forme commerciale. « Oxyde nitrique » n'existe que comme voie du
sildénafil. Coût en O2, dose, délai, répondeurs, effet réduit chez l'élite : rien. Avec
`beta-alanine-tampons`, il referme la liste du Groupe A. La grille du portail (dose, délai, plafond,
quelle variable produit le gain) s'y applique terme à terme.

> Le nitrate alimentaire (jus de betterave) au tamis des essais : ce qu'il change à l'effort, chez
> qui, à quelle dose. Couvrir la voie nitrate → nitrite → NO (bactéries buccales, et pourquoi le bain
> de bouche antiseptique annule l'effet — piste à corroborer), le résultat fondateur (baisse du coût
> en O2 à intensité fixe, Jones et coll.) et ce qu'il devient sur la performance (contre-la-montre,
> temps jusqu'à épuisement — et l'écart entre les deux critères), la dose et le délai (≈ 6-12 mmol,
> 2-3 h avant ; aigu vs chronique), le plafond et les non-répondeurs (effet réduit ou nul chez
> l'athlète d'endurance élite — VO2max élevé —, et ce que ça dit du mécanisme), les efforts
> intermittents et la force, les positions institutionnelles (consensus du CIO 2018 sur les
> compléments, Groupe A de l'AIS : document-source par nature), la sécurité (nitrates et
> nitrosamines : ce que la littérature alimentaire dit réellement, sans importer la peur des
> charcuteries), et le contenu réel des produits (teneur en nitrate des jus, variabilité). Public :
> lecteur exigeant non spécialiste. Délimitations : `cafeine-ergogene` pose le patron « dose unique,
> horaire, métabolisme du sujet » et `creatine` le patron « remplissage d'une réserve » — situer le
> nitrate entre les deux ; `beta-alanine-tampons` (candidat) tient les tampons. Doctrine de preuve
> santé (`docs/evidence-sante.md`) à recopier intégralement dans le brief. Domaine :
> nutrition-sportive.

### Disponibilité énergétique et RED-S — `disponibilite-energetique-reds` → `nutrition-sportive`
**Verdict : gap réel — et le premier thème santé centré sur la femme (ajout 2026-09-01).** RED-S,
triade, aménorrhée, seuil de disponibilité énergétique : 0 occurrence (le seul « triade » du corpus
est « la triade d'études humaines sur le BPC-157 »). Le voisin le plus proche, `proteines-besoins-timing`
(section `proteines-deficit-energetique`), installe un déficit de 40 % (« Quarante hommes en surpoids
[…] quatre semaines de déficit énergétique marqué ») et enseigne à maigrir en compétition (« 2,3 à
3,1 g/kg de masse maigre par jour ») sans jamais nommer ce qu'une faible disponibilité coûte à l'os,
aux hormones, à la performance. Les populations des 3 thèmes du domaine sont masculines à ≈ 90 %
(caféine : « 612 participants — dont 89 % d'hommes »). Preuve surtout observationnelle et de
consensus : attendre des rejets au seuil, et un seuil (30 kcal/kg de masse maigre) que le consensus
2023 relativise lui-même — à vérifier au Sweep.

> Le déficit énergétique relatif dans le sport (RED-S) : quand l'entraînement coûte plus que
> l'assiette ne rend. Couvrir la disponibilité énergétique comme grandeur (apport moins dépense
> d'exercice, par kg de masse maigre ; comment on la mesure, mal), la triade de l'athlète féminine
> (Loucks) et son extension en RED-S (consensus du CIO 2014, 2018, 2023 — document-source par
> nature ; ce que la version 2023 retire au seuil de 30 kcal/kg), les effets par système
> (aménorrhée hypothalamique et son diagnostic d'exclusion, os et fractures de fatigue, fer,
> immunité, performance — et où la preuve est expérimentale vs observationnelle), l'homme
> (testostérone, os : ce qui est démontré, moins qu'on ne dit), le dépistage (LEAF-Q, IOC REDs
> CAT2 et sa validation), le traitement (remonter l'apport, pas la pilule : ce que les essais
> d'œstrogènes montrent sur l'os), et la frontière avec les troubles du comportement alimentaire.
> Public : lecteur exigeant non spécialiste. Délimitations : `proteines-besoins-timing` tient le
> déficit contrôlé du sujet entraîné (partir de sa section, sans la refaire) ; `vitamine-d` et
> `collagene` tiennent l'os hors contexte énergétique ; `testosterone-homme-age` tient l'axe
> androgénique de l'âgé. ⚠️ Discipline : déclarer explicitement quand la population d'un essai n'est
> pas celle du titre ; ne pas transformer un consensus d'experts en résultat d'essai. Doctrine de
> preuve santé à recopier intégralement dans le brief. Domaine : nutrition-sportive.

- **glucides-pendant-l-effort** (basse, recentré le 2026-09-01) — gap réel mais trop large tel que
  soumis (« périodisation, train-low, cétogène ») : réduire à l'ingestion pendant l'effort (g/h,
  glucose + fructose, rinçage de bouche) et au « train low », en plaçant les études Supernova de
  Burke (LCHF chez les marcheurs élites) comme contre-exemple. Le glycogène n'apparaît que comme
  mécanisme abandonné de la caféine (`cafeine-ergogene` : « l'utilisation du glycogène a chuté de
  28 % chez six sujets et n'a pas bougé chez les six autres »). Chapitre de manuel plus que produit :
  la grille du portail ne s'applique qu'à l'ingestion en g/h.

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
(`omega-3` : **FAIT le 2026-08-30**, retiré du backlog — 48e run /leanmonograph, 20e thème santé,
3e de `complements-sante` où il s'insère **en 2e du parcours**, entre `vitamine-d` et `collagene`.
13/13 sections retenues (plan à 13, aucune troncature), 51 claims **24✓ / 25 corrigés / 2 rejetés**,
109 sources, 4 widgets, ~11 160 mots. Coût **9,39M tok / 118 agents / 3 h 55** — un seul lancement,
aucune reprise, dans la fourchette annoncée (7-10M).

**Le run le plus propre du corpus côté verdicts : 3,9 % de rejets, et les DEUX sont justes.**
Aucun rejet par carence (quota WebSearch à 1000, jamais approché). Les deux rejets tiennent au seuil
de sources avec **contenu vérifié exact par les deux jurés**, et dans les deux cas ce sont les jurés
eux-mêmes qui ont vu le piège : PMC, MDPI et ResearchGate reconnus comme **trois miroirs d'une même
publication** ; et l'exception `document-source` écartée au bon motif sur la revue Cochrane — « un
résultat empirique de méta-analyse n'en relève pas », exactement la borne écrite dans le CLAUDE.md.

**Le second rejet portait le cœur du fil rouge**, et sa récupération en prose est le point à retenir :
la réserve écrite dit « source unique sur ces chiffres, qu'aucune seconde synthèse de même ampleur ne
vient corroborer », puis rend la certitude GRADE juste après (« certitude élevée […] l'on peut s'y
fier »). ⚠️ **La formule générique « source unique, non corroborée » aurait été FAUSSE au fond ici** :
appliquée telle quelle à une revue systématique de 45 essais, elle suggère un résultat fragile là où
la preuve est du plus haut rang. Le hedge doit porter sur la corroboration BIBLIOGRAPHIQUE, jamais
sur la solidité — à surveiller sur tout rejet au seuil frappant une source de rang fort.

**Deux consignes du brief ressortent appliquées dans la prose**, ce qui plaide pour les y remettre :
l'argument du silence (« ASCEND n'a pas publié d'analyse du risque de saignement propre à son bras
oméga-3 ; un paramètre non analysé ne devient pas un paramètre rassurant ») et la lecture des
affiliations, devenue systématique — sponsors des deux essais à haute dose, texte de défense du
comparateur co-signé par le sponsor, association professionnelle du secteur signalée sur DEUX travaux
distincts, auteur actionnaire du vendeur du test d'index. « Le désaccord n'est pas seulement
statistique : il est financé. »

**Deux défauts d'appareil de preuve, non bloquants, laissés tels quels** : (1) un claim compte une
publication PMC et **le communiqué de presse de cette même publication** pour deux sources —
mono-source déguisée, 5e occurrence de [[sources-independence-by-document]], qui passe parce que le
contrôle bloquant ne juge que les `confirmed` et jamais les `corrected` ; (2) un claim s'appuie sur
ASCEND via deux write-ups tiers **sans sa publication primaire**. Piste de code : étendre le blocage
`low_rank_sources` aux `corrected`, et traiter un communiqué comme non indépendant du document qu'il
annonce.

**Visuel** : 2 violations de contraste en thème CLAIR seulement, dans un widget du thème —
`--blue-bright` employé comme encre à 4,42:1, le motif récurrent de la charte. Passé à `--blue`
(7,09 clair / 6,11 sombre) : 0 violation sur 1121 éléments dans les deux thèmes.

⚠️ **Trois PNG écrits À LA RACINE du repo par des agents du run** (`fig-omega3-forest.png`,
`omega3-fig-1.png`, et un troisième sans rapport avec le thème). Le CLAUDE.md prescrit
`.playwright-mcp/`. Non commités.)
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


### Mélatonine — `melatonine` → `complements-sante`
**Verdict : gap réel — mot absent du corpus, ouvre la cible « sommeil » (ajout 2026-09-01).**
« Mélatonine », « décalage horaire », « circadien » : 0 occurrence dans les 89 thèmes. La latence
d'endormissement n'est mesurée qu'une fois, comme dommage de la caféine (« s'allonge de 8,35
minutes », `cafeine-cognition-vigilance`). Le sommeil n'existe dans le corpus que comme stresseur
(privation) ou comme effet indésirable ; aucun document ne traite d'un produit vendu POUR dormir.

> La mélatonine au tamis des essais : une hormone vendue comme somnifère. Couvrir ce qu'elle est
> (chronobiotique, pas hypnotique — et pourquoi la distinction commande tout), l'effet mesuré sur
> l'insomnie (méta-analyses : latence d'endormissement raccourcie de quelques minutes — ≈ 7 min —,
> temps total de sommeil peu changé ; à corroborer), le décalage horaire (Cochrane : là où l'effet
> est le mieux établi), la dose et l'heure (0,5 mg vs 5 mg : plus n'est pas mieux ; l'heure de
> prise décide du sens de l'effet), les formes à libération prolongée (Circadin 2 mg, prescription
> après 55 ans en Europe), enfants et TDAH (usage massif, preuve étroite), la divergence
> réglementaire (complément en vente libre aux États-Unis, médicament ou plafond de dose en Europe
> — en France, avis ANSES 2018 et seuil réglementaire à vérifier), le contenu réel des produits
> (Erland & Saxena 2017 : de −83 % à +478 % de l'étiquette, sérotonine détectée), la sécurité
> (somnolence, interactions, grossesse, surdosages pédiatriques rapportés aux centres antipoison)
> et ce que le marketing « naturel » cache. Public : lecteur exigeant non spécialiste.
> Délimitations : `cafeine-cognition-vigilance` tient la privation de sommeil et la sieste
> (renvoi, ne pas redérouler) ; `complements-amincissants` a posé le patron « contenu réel des
> gélules » (le citer). Doctrine de preuve santé à recopier intégralement dans le brief. Domaine :
> complements-sante.

### Fer et supplémentation — `fer-supplementation` → `complements-sante`
**Verdict : gap réel — miroir de `vitamine-d` (ajout 2026-09-01).** « Ferritine », « hepcidine »,
« anémie », « carence martiale » : 0 occurrence ; « fer » n'apparaît qu'au sens du fer à repasser. Le
corpus n'a aucun thème sur un minéral, et un seul sur une supplémentation conditionnée à un dosage
sanguin contesté — `vitamine-d`, qui démonte exactement ce dispositif (« L'ampleur de l'épidémie est
un artefact de convention, pas une donnée de la nature »). Le fer est le cas inverse : seuils
contestés AUSSI, mais bénéfice fonctionnel réel chez le carencé et vrai risque de surdosage.

> Le fer en supplément : qui en a besoin, à quelle dose, et pourquoi tous les jours est une erreur.
> Couvrir le diagnostic (ferritine et ses seuils contestés — 15, 30, 45 µg/L —, l'inflammation qui
> la fausse, la saturation de la transferrine), la carence sans anémie et la fatigue (essais
> randomisés : ce qui bouge, chez qui — femmes menstruées, sportives), l'hepcidine et la prise un
> jour sur deux (Stoffel et coll., Lancet Haematology : absorption meilleure à dose alternée — à
> corroborer en primaire), les formes orales et leur tolérance, le fer intraveineux (indications,
> hypophosphatémie), l'athlète d'endurance (hémolyse, hepcidine post-effort, RED-S en renvoi), le
> risque (surcharge, hémochromatose, enfants et intoxications), et le contenu réel des produits.
> Public : lecteur exigeant non spécialiste. Délimitations : `vitamine-d` fournit le patron « la
> fabrique du besoin par le seuil » — le citer et CONTRASTER (ici le seuil décide d'un bénéfice
> réel) ; le candidat `disponibilite-energetique-reds` tient le versant sportif. Doctrine de preuve
> santé à recopier intégralement dans le brief. Domaine : complements-sante.

### Multivitamines et antioxydants — `multivitamines` → `complements-sante`
**Verdict : gap réel (ajout 2026-09-01).** Le mot n'apparaît que dans `masse-maigre-sous-glp1`, à
propos de la clause NICE (« Une multivitamine ne se paie qu'en argent »). COSMOS, PHS II, SELECT
vitamine E, ATBC/CARET : 0 occurrence (le « COSMOS » du corpus est un modèle NVIDIA, le « SELECT » un
essai de sémaglutide) ; l'USPSTF est cité par `vitamine-d` pour les fractures, jamais pour sa
recommandation 2022 sur les multivitamines. Le biais de l'utilisateur en bonne santé rejoint
directement le « paradoxe observationnel » de `vitamine-d` (« Associé à tout, cause de presque
rien ») — même méthode, objet neuf, et le seul cas du rayon où un RCT montre un SURRISQUE de cancer.

> Les multivitamines et les antioxydants au tamis des grands essais : le complément le plus vendu, la
> preuve la plus mince. Couvrir le biais de l'utilisateur en bonne santé (pourquoi les cohortes
> disent oui et les essais non), les grands RCT (Physicians' Health Study II : cancer −8 %,
> cardiovasculaire nul ; COSMOS et COSMOS-Mind : le signal cognitif et sa fragilité ; SELECT :
> vitamine E et cancer de la prostate en excès ; ATBC et CARET : bêta-carotène et cancer du poumon
> chez le fumeur, essais arrêtés), la recommandation USPSTF 2022 (« preuve insuffisante », et contre
> le bêta-carotène et la vitamine E — document-source par nature), les populations où une
> supplémentation ciblée est démontrée (grossesse et folates, carence avérée) à distinguer du
> « au cas où », les formulations et doses réelles, et le marché. Public : lecteur exigeant non
> spécialiste. Délimitations : `vitamine-d` et `omega-3` tiennent leurs molécules (VITAL, COSMOS ne
> sont cités ici que pour le bras multivitamine) — renvoyer, ne pas redérouler ; `vitamine-d` fournit
> le patron association vs effet. Doctrine de preuve santé à recopier intégralement dans le brief.
> Domaine : complements-sante.

### Probiotiques — `probiotiques` → `complements-sante`
**Verdict : gap réel (ajout 2026-09-01).** Le mot n'apparaît qu'une fois, dans une liste de
« potentialisateurs » réfutés en bloc par `masse-maigre-sous-glp1` (« probiotiques et fibres
prébiotiques joueraient par le microbiote. Il serait fastidieux, et inutile, de réfuter ces mécanismes
un par un »). Le microbiote n'est traité que comme voie métabolique de la berbérine. Spécificité de
souche, AGA 2020, Cochrane, contenu réel des gélules : rien. Premier « vivant » du domaine, preuve
organisée par souche et non par molécule : run coûteux (beaucoup de claims mono-source par souche).

> Les probiotiques au tamis des essais : une preuve par souche, un marketing par catégorie. Couvrir
> ce qu'est une souche et pourquoi un résultat ne se transporte pas (spécificité, dose en UFC,
> viabilité), la colonisation transitoire (ce que montrent les biopsies), les indications où la
> preuve existe (diarrhée associée aux antibiotiques — Cochrane —, diarrhée infectieuse de
> l'enfant, prévention de l'entérocolite du prématuré, C. difficile, certaines souches dans le
> SII) et celles où elle manque (immunité, humeur, poids), la guideline AGA 2020 (« aucune
> recommandation » hors trois situations — document-source par nature) et sa réception, la
> sécurité (bactériémies chez l'immunodéprimé, le cas Lactobacillus), le contenu réel des produits
> (souches absentes ou non déclarées) et le cadre réglementaire (allégations refusées par l'EFSA,
> le mot « probiotique » lui-même interdit sur l'étiquette en Europe — à vérifier). Public : lecteur
> exigeant non spécialiste. Délimitations : `berberine` tient le microbiote comme voie
> métabolique ; `complements-amincissants` a posé le patron « contenu réel » ; `nootropiques-vegetaux`
> le patron « allégations EFSA comme instrument de lecture ». ⚠️ Prévoir que les claims porteurs
> seront des SYNTHÈSES par indication, les résultats par souche restant en prose attribuée.
> Doctrine de preuve santé à recopier intégralement dans le brief. Domaine : complements-sante.

- **nad-nmn-precurseurs** (basse, ajout 2026-09-01) — NMN, NR, Sinclair : 0 occurrence ; « NAD+ »
  n'existe qu'en ligne d'inventaire d'une alerte ANSM (`testosterone-homme-age`). Le blurb du domaine
  promet « longévité » sans qu'aucun thème ne porte une allégation anti-âge. Contraste de méthode
  fort avec `omega-3` (« un lipide qui bouge dans le bon sens n'est toujours pas un événement
  évité » : ici le NAD sanguin monte sans critère fonctionnel), objet neuf (saga FDA 2022-2025 sur
  le statut de complément du NMN — à vérifier ; marketing d'un chercheur), mais littérature humaine
  mince : run court, beaucoup de « source unique » en prose.
- **curcumine** (basse, ajout 2026-09-01) — curcumine, curcuma, pipérine, PAINS : 0 occurrence. Le
  motif « biodisponibilité quasi nulle, effet pourtant revendiqué » est déjà écrit pour `berberine`
  (« ce n'est pas la dose qui limite l'exposition, c'est l'absorption ») ; ce qui reste de neuf est
  fort mais étroit — le statut de PAINS (Nelson et al. 2017, *J Med Chem*), les formulations
  « biodisponibles », les cas d'hépatotoxicité (Italie, 2019 — à vérifier) et l'adultération au
  plomb. Dernier de sa liste.

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


### Les GLP-1 hors du poids — `glp1-hors-poids` → `pharmacologie-metabolique`
**Verdict : gap réel — HAUTE, désigné par le pivot lui-même (ajout 2026-09-01).** `incretines-glp1`
(14 sections lues) écrit dans `obesite-step-surmount` : « Un dernier déplacement guette, plus
insidieux que le précédent : celui qui consiste à traiter la perte de poids comme le seul résultat de
la classe. » Puis il n'en traite qu'un contre-exemple, SELECT en section entière (HR 0,80, médiation
« un tiers seulement du bénéfice attribuable au tour de taille »), l'HbA1c, et deux mentions de
TRIUMPH. MASH, NASH, FLOW, HFpEF, apnée, EVOKE, SOPK : 0 occurrence dans les 5 thèmes ;
« Alzheimer » n'existe qu'en performance-cognitive, « alcool » qu'à propos de la caféine et des PDE5.
Littérature la plus mûre des candidats du domaine (phases 3 au NEJM), donc compatible avec le seuil
≥ 2 sans forcer. La grille de lecture est déjà écrite dans `signaux-controverses` : « "Aucun signal
observé" ne vaut que si le paramètre concerné a été mesuré. »

> Ce que les agonistes du GLP-1 font hors de la balance : indication autorisée contre effet de
> classe. Couvrir, organe par organe et essai par essai : le foie (MASH — ESSENCE, sémaglutide,
> résolution histologique, AMM 2025 aux États-Unis ; à corroborer), le rein (FLOW : critère composite
> rénal, arrêt anticipé pour efficacité), l'insuffisance cardiaque à fraction préservée
> (STEP-HFpEF : symptômes et poids, pas mortalité — ce que le critère mesure), l'apnée du sommeil
> (SURMOUNT-OSA, tirzépatide, IAH et AMM), le cerveau (EVOKE/EVOKE+ : échec annoncé fin 2025 dans
> l'Alzheimer — l'essai négatif comme résultat central), les addictions (alcool : petits essais et
> cohortes, pas d'AMM), le SOPK (promesse sans essai de taille), l'arthrose (TRIUMPH-4 déjà
> nommé), et ce qui sépare une AMM d'un effet de classe (qui a payé l'essai, quelle molécule, quelle
> dose, quel critère). Sécurité par indication (pancréas, vésicule, gastroparésie, ce que chaque
> essai a mesuré). Fil rouge : le déplacement du poids vers l'organe, et ce que chaque essai n'a
> PAS regardé. Public : lecteur exigeant non spécialiste. ⚠️ Délimitations strictes :
> `incretines-glp1` tient STEP/SURMOUNT/SELECT, l'HbA1c, le pipeline et le compounding — PARTIR de
> sa section « obesite-step-surmount » et de SELECT, ne rien redérouler ; `masse-maigre-sous-glp1`
> tient la composition corporelle ; `berberine` et `complements-amincissants` tiennent les
> substituts. Règle du promoteur (déjà écrite dans l'écosystème d'incretines) : un communiqué compte
> comme la même source que l'essai qu'il annonce. Doctrine de preuve santé à recopier
> intégralement dans le brief. Domaine : pharmacologie-metabolique.

### Les médicaments du poids retirés du marché — `medicaments-du-poids-retires` → `pharmacologie-metabolique`
**Verdict : gap réel à 85 % (ajout 2026-09-01).** `complements-amincissants` porte tout ce qui existe :
la sibutramine en détail (« l'essai SCOUT […] elle augmente de 16 % les événements cardiovasculaires
majeurs […] le produit a quitté les marchés américain et européen en 2010 », et l'adultérant qu'elle
est devenue), l'éphédra en section entière, et le cadre « rail A : sortie a posteriori sur signal de
sécurité » — illustré par un seul cas médicament. Rimonabant, fenfluramine, lorcasérine, orlistat n'y
sont que des noms dans la liste des adultérants ; `microdosage-psychedeliques` tient la mécanique
5-HT2B des valvulopathies comme comparateur. Benfluorex/Mediator : 0 occurrence — l'angle français
absent du corpus.

> L'histoire des médicaments de l'obésité retirés du marché, et ce qu'elle apprend sur la lecture
> d'un essai : fenfluramine et fen-phen (Connolly 1997, valvulopathies, retrait), rimonabant (RIO :
> efficacité réelle, suicidalité, retrait européen 2008, jamais approuvé aux États-Unis), sibutramine
> (SCOUT : en renvoi, déjà écrit), lorcasérine (CAMELLIA-TIMI 61 : sécurité cardiovasculaire
> démontrée PUIS retrait 2020 sur un déséquilibre de cancers — le cas d'école du critère non
> prévu), benfluorex/Mediator (l'affaire française : valvulopathies, décennie de signaux, procès),
> les survivants (orlistat, phentermine : ce qu'ils ont de différent) et la leçon transversale — ce
> qu'un essai de 1 à 2 ans ne peut pas voir, la pharmacovigilance comme second essai, et comment
> lire aujourd'hui SELECT et ses successeurs à la lumière de ces précédents. Public : lecteur
> exigeant non spécialiste. Délimitations : `complements-amincissants` tient la sibutramine et
> l'éphédra (renvoyer, deux phrases) et le cadre réglementaire ; `incretines-glp1` tient la classe
> actuelle (ne pas la juger ici, seulement lui appliquer la grille) ; `microdosage-psychedeliques`
> tient la mécanique 5-HT2B (citer). Doctrine de preuve santé à recopier intégralement dans le
> brief. Domaine : pharmacologie-metabolique.

### Médicaments contrefaits et pharmacies en ligne illégales — `medicaments-contrefaits-en-ligne` → `pharmacologie-metabolique`
**Verdict : gap réel — renvoi cassé A4, objet le plus récurrent du balayage (ajout 2026-09-01).**
`nootropiques-stimulants-prescrits` renvoie « Ce que contiennent réellement les gélules acquises hors
circuit, et par quels canaux elles circulent » à « d'autres monographies de ce corpus » — aucune ne
traite un stimulant contrefait. Cinq documents tiennent chacun leur bout du même objet sans le nommer
comme sujet : `incretines-glp1` (compounding, 7 mentions de contrefaçon), `inhibiteurs-pde5`
(sildénafil contrefait), `testosterone-homme-age` (« Ce qu'il y a vraiment dans le flacon »),
`peptides-gris` (lots « research use only »), et le rétatrutide de contrebande nommé trois fois.
Domaine à confirmer par /arrange : le sujet est transversal, `pharmacologie-metabolique` est le
logement le plus naturel (statut de la molécule, canal de vente : c'est déjà sa frontière interne).

> Les médicaments d'ordonnance hors circuit : ce que contiennent réellement les produits achetés en
> ligne, et par où ils passent. Couvrir la typologie (contrefaçon, préparation magistrale non
> autorisée, produit « research use only », détournement de chaîne légale), les analyses de
> contenu par classe (stimulants d'ordonnance et faux Adderall contenant de la méthamphétamine ;
> GLP-1 : saisies et analyses de stylos contrefaits, insuline à la place du sémaglutide ; PDE5 ;
> testostérone et anabolisants ; peptides), les canaux (pharmacies en ligne illégales, réseaux
> sociaux, télémédecine complaisante — l'étude en client mystère déjà citée pour la
> testostérone), les instruments de mesure (saisies douanières, programmes d'analyse des agences,
> études d'achat test) et leurs biais, le cadre (EMA, FDA, ANSM, LegitScript, la directive
> médicaments falsifiés) et la question du risque réel (cas cliniques documentés vs alarme). Public :
> lecteur exigeant non spécialiste. ⚠️ Délimitations strictes : chaque thème cité tient son
> bout — `incretines-glp1` le compounding des GLP-1, `inhibiteurs-pde5` l'adultération sexuelle
> (Tucker 2018), `complements-amincissants` l'adultération des compléments, `peptides-gris` le
> « research use only », `testosterone-homme-age` le flacon de SARM — PARTIR de leurs sections,
> réunir sans redire ; l'angle propre est le canal et la mesure de ce qui y circule. Doctrine de
> preuve santé à recopier intégralement dans le brief. Domaine : pharmacologie-metabolique (à
> confirmer).

(Écarté le 2026-09-01 : `glp1-pipeline-nouvelle-generation` — déjà couvert par la section
`pipeline-retatrutide` d'`incretines-glp1`, voir « Écartés ». Le candidat
`metformine-rapamycine-longevite`, instruit ici, est logé dans `muscle-vieillissement` : le seul
précédent de fond du corpus est la GH anti-âge de `testosterone-homme-age`.)

---

## `performance-cognitive` — domaine CRÉÉ le 2026-08-15, portail ouvert le 2026-08-26

*(Ce qui suit est la PROPOSITION du 2026-08-15, conservée pour son raisonnement. Le domaine existe
depuis le 39e run ; son portail, ouvert par `nootropiques-vegetaux` au 42e, a mis trois runs à
venir. Les candidats non barrés plus bas restent d'actualité.)*

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

(`cafeine-cognition-vigilance` : **FAIT le 2026-08-27**, retiré du backlog — 44e run
/leanmonograph, 16e thème santé, 3e de `performance-cognitive`. 15/15 sections (plan à 15,
plafond 16, aucune troncature), 60 claims **31✓ / 21 corrigés / 8 rejetés**, 104 sources,
2 widgets + 2 exercices, tableau de verdicts à **21 lignes**, ~14 000 mots. Contraste 0 violation
en clair ET en sombre. Coût **10,26M tok / 133 agents / 2 lancements / ~3 h 45** — dans la
fourchette annoncée (8-11M). ✅ **La consigne de frontière a tenu** : le voisin ergogène n'est
jamais redéroulé, et son acquis métrologique (seuil « gros consommateur » de 190 à 600 mg/j, aucune
méthode validée) est réutilisé comme OUTIL de lecture, ce que le brief autorisait explicitement.

**2e déclenchement du garde-fou d'élagage du corpus, et le plus instructif.** Il a arrêté le run
avant la prose : trois claims tenus par TOUS leurs jurés allaient faire tomber « Ligne de base
effondrée », la moitié du fil rouge où l'effet est réel. Diagnostic réel — **pas celui qu'annonce
le message d'erreur** : les deux jurés avaient confirmé mot pour mot, chiffre par chiffre, en
citant **la même** source. Les claims étaient rédigés comme des paraphrases de papier
(« une méta-analyse trouve X »), donc **mono-sources par construction**. Reformulés pour porter le
FAIT et non le contenu d'un papier, chacun tient sur deux travaux sans aucun lien — Wang et al.
2026 (Harbin Institute of Information Technology) et Irwin et al. 2020 (Griffith University).
→ **Réflexe nouveau** : sur un rejet « seuil de sources » à 0 réfutation, regarder d'abord si
l'énoncé PARLE D'UN PAPIER au lieu de dire un fait — la réparation est éditoriale, pas
bibliographique, et ne contourne pas le seuil.

**Classe d'échec NOUVELLE — le claim qui se rejette lui-même.** Un claim dont le CONTENU est une
mise en garde d'indépendance (« ces deux essais partagent deux auteurs, donc une seule lignée de
preuve ») est condamné par sa propre honnêteté : les jurés, cohérents avec l'énoncé, refusent de
compter comme indépendantes deux sources que le claim déclare liées — d'où `corroborated: 2,
refuted: 0, sources: 0` et rejet au seuil. Ré-adjugé en `corrected` après contrôle en primaire
(Alsene 2003 / Childs 2008, Neuropsychopharmacology, université de Chicago, Deckert et de Wit
communs) : le seuil ≥ 2 protège contre l'affirmation d'un fait empirique non corroboré, or cet
énoncé n'affirme pas l'effet, il affirme l'ÉTAT DE LA LITTÉRATURE. → [[claim-mise-en-garde-se-rejette]]

**Quatre erreurs de fond trouvées en re-vérifiant, aucune vue par les jurés** :
1. une **NOTE de section** attribuait l'essai de 48 h à « Kamimori/Hansen » — **Kamimori n'en est
   pas auteur** (Hansen, Van Dongen et al., Washington State University / DoD BHSAI). L'auteur de
   prose écrit PAR LES NOTES : ré-adjuger un claim n'aurait rien réparé ;
2. **Irwin et al. 2020 publie « response time g=0,86 ; 95 % CI: 0,53-0,83 »** — la valeur ponctuelle
   est HORS de son propre intervalle (coquille de l'article). Chiffre écarté, et le document le dit ;
3. « Irwin et al. **2019** » en bibliographie contre 2020 en prose — corrigé après build, rebuild ;
4. l'Audit-prose a trouvé un « 2025 » pour 2024 (essai Gardiner/Halson) **invisible au lint** parce
   que 2025 existait déjà ailleurs dans `knowledge.json` — nouvelle occurrence de l'angle mort par
   collision numérique.

**Le rejet maintenu l'a été à raison** : l'essai de terrain de 55 h (McLellan & Kamimori) n'a pour
corroboration apparente que PMID 16018347, **de la même équipe (4 co-auteurs communs)**. La prose
l'écrit : « le résultat s'écrit, il ne se compte pas. » Le piège n°3 du brief — « sur deux sources
qui se corroborent trop bien, lire les auteurs » — s'est matérialisé DEUX fois en sens inverses :
pour rejeter à raison, et pour lever une fausse dépendance inventée par une note.

**Ce qui a bien tourné** : l'Audit-prose a tourné AVEC son moteur (24 chiffres vérifiés, `fixed=1`),
les critics ont écarté une figure introduisant un chiffre non sourcé et fait corriger un débordement
mobile, **zéro renvoi cassé** malgré deux voisins non publiés, et le `resume` n'a écrasé aucune des
ré-adjudications manuelles (jetons de traçabilité retrouvés intacts dans `knowledge.json`).

**Angle résiduel** : 4 statements sur 60 sont restés en anglais dans `knowledge.json` — sans effet
sur la prose, française de bout en bout, mais irrégulier au regard du reste du corpus.)
(`microdosage-psychedeliques` : **FAIT le 2026-08-27**, retiré du backlog — 45e run /leanmonograph,
17e thème santé, **4e thème de `performance-cognitive`**. 15/15 sections retenues (plan à 15, aucune
troncature), 58 claims **20 ✓ / 19 corrigés / 19 rejetés** (39 retenus), 70 sources, 3 widgets,
~14 000 mots, contraste 0 violation en clair ET en sombre. Coût **10,14 M tok / 136 agents /
2 lancements / ~4 h 35** — au-dessus de la fourchette annoncée (7-10 M), le ré-audit et la reprise
l'expliquent entièrement.

**3e déclenchement du garde-fou d'élagage — et la première fois que sa réparation prescrite est la
MAUVAISE.** Il signalait 5 rejets décisifs menaçant 3 sections, dont « Sécurité, doses,
interactions », obligatoire en santé. Sa consigne — « ré-audit ciblé pour chercher la 2e source
indépendante » — était ici inapplicable : ces énoncés portent le grain statistique fin d'un essai
unique (`t(26)=2,56, p=,017` ; `111,5 vs 105,35 mmHg`), que **seule la primaire peut porter**. Les
revues tierces confirment ces résultats, mais qualitativement — aucune ne reprend ce niveau de
détail. La 2e source n'existait pas et n'existera pas : les rejets étaient JUSTES.
**La bonne réparation n'était pas de sauver les claims mais de déplacer l'énoncé au grain que
plusieurs travaux portent réellement** — 3 claims de SYNTHÈSE écrits et vérifiés à la main, chacun
corroboré par des équipes distinctes vérifiées auteur par auteur, et le document y a gagné : la
thèse de la rupture d'insu ne repose plus sur un essai mais sur le recensement d'un champ entier.
Les chiffres rejetés restent en prose, attribués et assortis de leur réserve — traitement correct.

⚠️ **À retenir pour tout sujet à littérature JEUNE** (19 rejets sur 58 ici) : le seuil « ≥ 2 sources »
et la règle santé « dose et taille d'effet obligatoires dans le statement » sont en tension frontale.
Plus l'énoncé est précis, moins il est corroborable. Prévoir dès le brief que les claims porteurs
seront des SYNTHÈSES, et les chiffres d'essai, de la prose réservée.

**Six défauts trouvés au backstop, APRÈS `build.success: true`, aucun vu par les jurés ni par le
lint** — dont le plus grave rencontré à ce jour sur le corpus :
1. **`claim:28`, retenu et portant un résultat CENTRAL du fil rouge, reposait sur trois sources de
   RANG NUL** : presse de vulgarisation, organisation de promotion du microdosage, et **un vendeur de
   retraites psychédéliques**. Contenu exact, **appareil de preuve faux** — invisible à la lecture,
   indéfendable si un lecteur ouvre les liens. → [[corrected-claims-escape-source-check]] : le
   contrôle `all_confirmed_have_2plus_sources` ne regarde QUE les `confirmed` ; les 19 `corrected`,
   retenus comme les autres, n'ont **aucun** contrôle de sources en code.
2. `claim:11` : une annonce d'événement comme 2e source → requalifié `document-source`.
3. **Yanakieva daté 2018 en prose, 2019 en bibliographie** (Psychopharmacology vol. 236, 2019).
4. **« Cette même revue de 2024 »** deux phrases après l'avoir datée 2026 — collision numérique.
5. **`src:43`/`src:44` = le même article** sous `/doi/pdf/` et `/doi/` : nouvelle variante du bug
   `normUrl` du 43e run, la normalisation ignore le segment `/pdf/`. **Correctif de code non
   appliqué à ce jour — à faire.**
6. **Trois réserves FAUSSES par excès de prudence** (erreur du 42e run) : une revue systématique et
   un protocole d'essai publié présentés comme « non corroborés » → « source unique par nature ».

**Deux fausses indépendances évitées** en lisant les listes d'auteurs (réflexe du 43e run) :
Szigeti et al. 2023 (*Scientific Reports*), candidat évident comme 2e source, est de la MÊME équipe
d'Imperial College que l'essai eLife 2021 ; et Family et al. 2020 / Yanakieva et al. 2019 analysent
la MÊME cohorte de 48 volontaires âgés. `audit-report.json` régénéré en déterministe après
dépassement des 64k tokens de sortie — **5e occurrence**.)

- **neurostimulation-tdcs** (basse) — vrai gap, excellent matériau de crise de réplication, mais
  c'est un dispositif et non un produit de rayon : moins homogène avec le méta-domaine.

### Panorama du rayon nootropique — `nootropiques-panorama` → `performance-cognitive`
(**FAIT le 2026-08-28**, retiré du backlog — 46e run /leanmonograph, 18e thème santé, 5e et dernier
de `performance-cognitive`. 16/16 sections retenues (plan brut à 16, plafond à 16 : aucune
troncature), 61 claims **31 ✓ / 28 corrigés / 2 rejetés**, 147 sources, 3 widgets, tableau de
verdicts à **25 substances**, ~396 ko de HTML. Coût **~10,8 M tok / 139 agents / 2 lancements /
~3 h 45**, dans la fourchette annoncée. Build exit 0 du premier coup, lint exit 0, contraste
0 violation en clair ET en sombre.

**4e déclenchement du garde-fou d'élagage, et le plus instructif : 5 rejets au seul seuil de
sources, dont AUCUN ne se réparait de la même façon.** La consigne du garde-fou (« cherche la
2e source ») n'était juste que pour 2 d'entre eux :
- **réparables** (la 2e source existait) : Lôo & Poirier — la revue de Starling-Soares,
  Carrera-Bastos & Bettendorff (*J Nutr Metab* 2020) décrit l'essai mot pour mot ; et Cohen 2021 —
  corroboré par Vanhee et al. (*J Xenobiot* 2025, surveillance de 12 laboratoires officiels
  européens et australien, 159 échantillons) et Jędrejko et al. 2023 ;
- **à regrainer** (le grain fin ne pouvait PAS être corroboré) : les deux claims lévétiracétam ;
- **rejet JUSTE** : le noopept, mono-source par nature — vérifié sur 154 notices Europe PMC,
  aucune publication indépendante de l'Institut Zakusov. La réserve « source unique, non
  corroborée » est son traitement correct.

**Le regrain a fait sortir le meilleur fait du document, qu'aucun juré n'avait vu** : l'essai
HOPE4MCI (Mohs et al., *Alz & Dementia TRCI* 2024;10(1):e12446) **a manqué son critère principal**
— CDR-SB −0,10 (IC 95 % −0,85 à 0,58) — et le « déclin ralenti de 40 % » vient d'un sous-groupe
APOE ε4 dont l'IC inclut aussi zéro (−0,45 ; IC 95 % −1,43 à 0,53). Le claim d'origine présentait
Lancaster et al. 2025 comme un « essai croisé INDÉPENDANT » reproduisant ce résultat : or c'est un
ABSTRACT de congrès, et **Arnold Bakker en est co-auteur comme il est auteur de HOPE4MCI** —
fausse indépendance évitée de justesse, 3e occurrence du réflexe « lire les auteurs ».

**Le brief transmettait DEUX erreurs, toutes deux corrigées par le run** (2e fois après le 43e) :
« asthénie fonctionnelle » (absent des deux documents officiels d'Arcalion) et la date de Cohen
(2021, pas 2020 — la date 2020 est celle de la couverture presse). Les deux sont corrigées
ci-dessus dans ce fichier.

⚠️ **6 défauts trouvés au backstop APRÈS un build vert et un lint vert, tous dans l'APPAREIL de
preuve, aucun dans les énoncés** — dont **l'exception `document-source` invoquée sur un MIROIR PR
Newswire du communiqué FDA**, et **deux entrées `nootroo.com`, un VENDEUR de nootropiques, citées
en bibliographie sur l'histoire du terme**. Plus : Wikipédia en 2e source de deux claims (le brief
lui donnait pourtant « zéro valeur de source »), un PDF de revue hébergé sur un blog personnel, et
le **doublon Jędrejko sous `doi.org` et `/doi/abs/`** — nouvelle variante de « même travail compté
deux fois » après `/doi/pdf/` au 45e run et la query string au 43e. Tracés dans `audit-report.md`
sous le jeton `[BACKSTOP-46]`.
→ **Le contrôle d'acceptation du build ne regarde QUE les `confirmed`, et ne juge JAMAIS le RANG
des sources : il valide « 2 sources » sans voir que l'une est un vendeur.** C'est l'angle mort le
plus rentable du corpus.

✅ **Premier run sans perte au `resume`** : les 16 jetons de traçabilité posés avant la relance ont
tous survécu, contre une section perdue par reprise aux 43e et 45e runs.)


### Entraînement cognitif commercial — `entrainement-cognitif-commercial` → `performance-cognitive`
**Verdict : gap réel — le seul qui vaille de rouvrir le domaine, UNE fois (ajout 2026-09-01).**
Lumosity, Cogmed, n-back, Jaeggi, Simons, transfert proche/lointain : 0 occurrence dans les 89
thèmes (« ACTIVE » n'apparaît que pour la forme active de la vitamine D). « Entraînement cognitif »
n'existe que comme cofacteur d'un essai de plante (`nootropiques-vegetaux` : « bacopa combiné à trois
heures hebdomadaires d'entraînement cognitif »). Les 25 substances du panorama sont toutes des
substances ; aucune intervention non pharmacologique n'entre dans sa grille. Pourtant le domaine
emploie déjà la notion sans la nommer (« une taille d'effet ne se transporte pas d'une fenêtre à
l'autre » ; « rattraper un déficit fabriqué en laboratoire n'est pas améliorer un cerveau intact »), et
l'amende FTC de 2016 contre Lumosity fait pendant au veto parlementaire de 2016 sur l'allégation
caféine : un régulateur qui sanctionne la promesse, pas le produit. Autres idées écartées pour le
domaine (exercice, sommeil, nicotine) : voir « Écartés ».

> L'entraînement cognitif vendu au grand public : ce que les essais mesurent quand on s'entraîne
> à un jeu. Couvrir la question du transfert (proche : la tâche entraînée s'améliore, toujours ;
> lointain : l'intelligence fluide, la mémoire au quotidien — rarement, et c'est tout le sujet), le
> n-back et Jaeggi 2008 puis ses réplications manquées, Cogmed et la mémoire de travail, Lumosity
> (l'amende FTC de 2016 et ce que la FTC reprochait exactement — document-source par nature), le
> consensus de Stanford/Max Planck de 2014 contre la lettre des industriels, la revue de Simons et
> coll. 2016 (*Psychological Science in the Public Interest*), l'essai ACTIVE et son suivi à dix ans
> (vitesse de traitement et démence : ce que le résultat dit et ne dit pas), les jeux vidéo
> d'action, le placebo et les attentes (Foroughi 2016 : le recrutement décide de l'effet), la
> personne âgée et la prévention du déclin, et le cadre réglementaire (logiciels « thérapeutiques »
> approuvés, EndeavorRx). Public : lecteur exigeant non spécialiste. Délimitations : les 5 thèmes du
> domaine tiennent les substances — partir de leur thèse commune (l'effet est conditionnel à la
> tâche et à la ligne de base) et la tester sur un objet non pharmacologique ; `creatine` tient le
> versant cognitif de la créatine. Doctrine de preuve santé à recopier intégralement dans le brief.
> Domaine : performance-cognitive (6e thème ; le portail se rouvre pour lui).

---

## `muscle-vieillissement` — domaine CRÉÉ le 2026-08-18, portail ouvert le 2026-08-19

*(Ce qui suit est la PROPOSITION du 2026-08-18, conservée pour son raisonnement. Le plan « deux
thèmes qui créent le domaine ET son portail » a été tenu en deux runs consécutifs — le seul cas du
corpus où un domaine naît complet. `graisse-viscerale-homme-age` reste à confirmer.)*

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


### Pharmacologie de l'ostéoporose — `osteoporose-pharmacologie` → `muscle-vieillissement`
**Verdict : gap réel — HAUTE, la thèse du domaine écrite trois fois et jamais éprouvée sur les
molécules faites pour l'os (ajout 2026-09-01).** Bisphosphonate, alendronate, zolédronate, dénosumab,
tériparatide, romosozumab, fracture atypique : 0 occurrence. Ce qui existe est une thèse sur la DMO
comme substitut, développée sur une hormone, un nutriment et un peptide : `testosterone-homme-age`
(« la testostérone augmente la densité, donc elle solidifie l'os, donc elle évite des fractures. Le
premier maillon est mesuré, et solide. Le dernier est mesuré, et contredit »), `vitamine-d` (« la
variation de densité minérale osseuse […] est jugée sans portée clinique » ; l'ostéoporose diagnostiquée
n'y figure qu'en exclusion USPSTF ; le calcium n'y est que le co-facteur de Chapuy, sans un mot sur son
signal cardiovasculaire), `collagene` (DMO et T-score sur un seul essai, « la même mesure, lue sur deux
échelles »). Ni `sarcopenie-exercice-nutrition` ni `testosterone-homme-age` ne désignent l'ostéoporose
comme un dehors : l'os y est refermé comme preuve interne. Le blurb du domaine (« la masse et la
force ») est à élargir à l'os — « masse, force, densité, fracture : ce que le substitut ne prédit
pas ».

> Les médicaments de l'os au tamis des essais : ce que la densité gagne, ce que la fracture évite.
> Couvrir la DMO comme substitut et ce qu'elle prédit réellement (méta-régressions DMO/fracture :
> une fraction de l'effet), les bisphosphonates (FIT : alendronate, fractures vertébrales vs de
> hanche selon la population ; HORIZON : zolédronate annuel, mortalité après fracture de hanche),
> le dénosumab (FREEDOM, et l'effet rebond à l'arrêt : fractures vertébrales multiples — le
> médicament qu'on ne peut pas arrêter), les anabolisants (tériparatide, romosozumab et ARCH : la
> DMO qui monte le plus et le signal cardiovasculaire), les « drug holidays » et les fractures
> atypiques du fémur (le risque rare qui a vidé les prescriptions — combien de fractures évitées
> par fracture atypique), le calcium et la vitamine D comme adjuvants (et le signal cardiovasculaire
> du calcium, Bolland — controverse à écrire comme telle), l'homme (moins d'essais, mêmes
> molécules), le dépistage (T-score, FRAX, seuils d'intervention) et la question de qui traiter,
> l'observance (moitié des patients arrêtent à un an) et le marché. Fil rouge : le substitut ne
> prédit pas le résultat — ici démontrable dans les deux sens, et molécule par molécule. Public :
> lecteur exigeant non spécialiste. ⚠️ Délimitations strictes : `vitamine-d` tient la vitamine D
> seule et les chutes (renvoyer) ; `collagene` tient l'essai osseux du collagène ;
> `testosterone-homme-age` tient TRAVERSE-fractures (le citer comme précédent du fil rouge) ;
> `sarcopenie-exercice-nutrition` tient l'exercice ; les candidats `chutes-fragilite-prevention` et
> `menopause-hormonotherapie` tiennent respectivement la chute et le THM (l'os sous œstrogènes n'a
> ici droit qu'à un renvoi). Doctrine de preuve santé à recopier intégralement dans le brief.
> Domaine : muscle-vieillissement, blurb à élargir par /arrange.

### Metformine, rapamycine et le marché de la longévité — `metformine-rapamycine-longevite` → `muscle-vieillissement` (à confirmer)
**Verdict : gap réel, domaine à trancher (ajout 2026-09-01 ; instruit côté pharmacologie).** La
metformine n'existe que comme comparateur dans `berberine` (« la berbérine serait aussi efficace que
la metformine. Elle a une source, et pratiquement une seule ») et comme traitement de fond de
SURPASS-2 ; la rapamycine n'est qu'un outil de laboratoire dans `proteines-besoins-timing` (« abolit
complètement la stimulation de la MPS par la leucine », chez le porcelet). TAME, Bannister, MILES,
Konopka, ITP, PEARL, Dog Aging Project : 0 occurrence. Le repositionnement anti-âge est un quatrième
motif pour `pharmacologie-metabolique` ; le seul précédent de fond est la GH anti-âge de
`testosterone-homme-age` (« la GH ne peut pas être recommandée comme thérapie anti-âge »), d'où le
logement ici. ⚠️ Base humaine randomisée mince (MILES, Konopka à quelques dizaines de sujets ; TAME
jamais lancé faute de financement — à vérifier) : attendre des rejets mono-source comme au 45e run,
et prévoir des claims de SYNTHÈSE.

> Deux médicaments repositionnés contre le vieillissement : ce que la souris promet, ce que l'homme
> montre. Couvrir la metformine (Bannister 2014 : « les diabétiques sous metformine vivent plus
> longtemps que les non-diabétiques » — et le biais de temps immortel qui fabrique le résultat ;
> MILES ; l'atténuation des gains de l'exercice chez l'âgé — Konopka 2019 ; TAME, l'essai conçu pour
> faire reconnaître le vieillissement comme indication, et pourquoi il n'a pas eu lieu), la
> rapamycine (mTOR, les données ITP chez la souris et leur robustesse, PEARL 2025 — critère
> principal, effets indésirables —, le Dog Aging Project/TRIAD, l'usage off-label hebdomadaire et
> ses cliniques), le marché de la longévité (protocoles, tests d'« âge biologique », horloges
> épigénétiques comme substituts non validés), et la grille commune : quel critère, chez qui, et ce
> qu'un substitut de vieillissement ne prédit pas. Public : lecteur exigeant non spécialiste.
> Délimitations : `berberine` tient la comparaison berbérine/metformine (renvoyer) ;
> `testosterone-homme-age` tient la GH anti-âge (le citer comme précédent) ; `incretines-glp1` tient
> les GLP-1 ; les candidats `nad-nmn-precurseurs` (compléments) et `glp1-hors-poids` tiennent leurs
> objets. Doctrine de preuve santé à recopier intégralement dans le brief. Domaine :
> muscle-vieillissement (à confirmer par /arrange ; pharmacologie-metabolique en repli).

- **chutes-fragilite-prevention** (basse-moyenne, ajout 2026-09-01) — gap réel mais plus faible : la
  chute n'est traitée que comme CRITÈRE de trois interventions (`vitamine-d` : « réduisent le risque de
  chute de 19 % » puis « la vitamine D seule ne prévient pas les chutes » ; `sarcopenie-exercice-nutrition` :
  SPRINTT, « des chutes plus fréquentes dans le bras multimodal » ; `testosterone-homme-age` : « plus de
  80 % des fractures […] consécutives à des chutes »), jamais comme objet. Phénotype de Fried, index de
  fragilité, Otago, tai-chi, STRIDE, protecteurs de hanche, déprescription : 0 occurrence. Réserve :
  pas un produit de rayon, et chevauchement avec l'ostéoporose sur les fractures — à programmer en
  4e thème du domaine, après `osteoporose-pharmacologie`, pour tenir la dissociation chutes/fractures.

---

## `fonction-sexuelle` — domaine CRÉÉ le 2026-08-27, ✅ portail OUVERT le 2026-08-29

**Ouvert par `inhibiteurs-pde5` au 43e run.** Paramètres retenus, tels que proposés : id
`fonction-sexuelle`, label « Fonction sexuelle », blurb « Ce que les essais démontrent quand on
prétend traiter — ou améliorer — la fonction sexuelle. », classé après `performance-cognitive` et
avant `complements-sante`. 12e domaine du corpus.

✅ **CHANTIER REFERMÉ EN UN SEUL RUN** (le 47e, deux jours après l'ouverture) : `ejaculation-precoce`
a porté le domaine à deux thèmes et `/arrange` a écrit `tools/portals/fonction-sexuelle.json` —
11e portail du corpus. À comparer à `performance-cognitive`, ouvert au 39e run et refermé seulement
au 42e. **`ai-organizations` (1 thème) est désormais le seul domaine sans portail.**

### Éjaculation précoce — `ejaculation-precoce` → `fonction-sexuelle`

(**FAIT le 2026-08-29**, retiré du backlog — 47e run /leanmonograph, 19e thème santé, **REFERME le
domaine `fonction-sexuelle`** et lui ouvre son portail. 14/14 sections retenues (plan à 14, aucune
troncature, `--expect-sections` satisfait du premier coup), 54 claims **24✓ / 21 corrigés / 9
rejetés**, 86 sources, 3 widgets + 2 figures, ~10 800 mots. Coût **8,74M tok / 112 agents / 3 h 58**
— un seul lancement, aucune reprise, dans la fourchette annoncée (8-12M).

**Le run le plus PROPRE du corpus côté pipeline, et c'est le backstop qui a payé.** Aucun rejet par
carence (`search_exhausted` faux sur les 9 — quota WebSearch à 1000 jamais approché), aucune section
sous quota d'élagage, `low_rank_sources` et `foreign_statements` vides, contraste 0 violation en
clair ET en sombre dès le premier build (327 éléments de widgets mesurés).

**Les 9 rejets, tous justes, et deux familles nettes** — à opposer au 43e run (7 faux rejets sur 8) :
1. **Quatre rejets d'énoncé FAUX**, réparés par la prose : `claim:6` décrivait les 118 hommes de
   l'étude coréenne comme « en demande de traitement » quand ils étaient **sains** ; `claim:21`
   parlait de « quatre guidelines » notées AGREE quand l'article n'en note que **trois** (le DSM-5 et
   la CIM-11 ne sont pas des guidelines) ; deux claims tramadol mal formulés à chiffres exacts.
   **L'auteur a écrit la version corrigée depuis les notes** — vérifié dans le HTML final.
2. **Cinq rejets au seuil, contenu vérifié mot pour mot**, tous **récupérés en prose avec la réserve
   « source unique, non corroborée »** : lois lognormale/Gumbel de l'IELT, moyenne géométrique et
   *fold increase*, métriques du PEDT, méta-analyse Zhang 2019, divergence des trois guidelines sur
   l'acide hyaluronique. **Le seuil ≥2 n'a donc rien coûté au document** : il a déplacé ces faits du
   `knowledge.json` vers une prose qui les porte avec leur statut. C'est le traitement prescrit, et
   la première fois qu'on le constate appliqué sur toute une série.

**LE DÉFAUT DE FOND, invisible au council comme au lint** (section sécurité, obligatoire en santé) :
la prose présentait l'analyse cardiovasculaire de la dapoxétine comme *« une analyse de
pharmacovigilance **indépendante** »*. Elle ne l'est pas — **trois de ses quatre auteurs sont
employés et actionnaires de Johnson & Johnson**, le quatrième est son consultant, et J&J a financé
les essais analysés. Pire, la prose citait le « 24,5 % d'événements cardiovasculaires sous 60 mg
quotidiens » **sans la conclusion des auteurs** (« no associated significant cardiovascular adverse
events, except for vasovagal-mediated syncope ») : le lecteur comprenait un risque cardiaque
quintuplé. Corrigé à la main puis rebuild. **Tous les chiffres étaient EXACTS** — seule la lecture
des AFFILIATIONS révélait l'erreur. Réflexe à généraliser : sur un chiffre de sécurité spectaculaire,
lire les affiliations ET la phrase de conclusion des auteurs, pas seulement le tableau de résultats.
La section `dapoxetine`, elle, déclarait correctement son lien industriel — le défaut était isolé.

**Deux défauts d'infrastructure** : (1) `write:audit-report.json` a de nouveau échoué (>64k tokens de
sortie, **4e occurrence**) — régénéré en déterministe, 54/54 claims appariés ; (2) **classe NOUVELLE
— le checkpoint `research.json` écrit PUIS perdu** : `ckptWrite` fait recopier un JSON de 75 Ko
*verbatim* à un agent LLM (`workflow.js:639`), qui a échoué en silence (`ckptWrite` avale l'erreur
par conception). Sans réparation, un `resume` aurait rejoué Sweep+Plan et **régénéré des ids
différents** de ceux des sections déjà auditées — incohérence que `workflow.js:1043` signale
lui-même. Reconstruit depuis `journal.jsonl` en réutilisant les vraies fonctions `normUrl` /
`dedupSources` du workflow. → [[checkpoint-research-perdu-a-l-ecriture]]

**Angle résiduel** : le lint sort en exit 2 sur 7 faux positifs irréductibles, tous `claim:13` sur
les pivots « Diagnostic » / « Tool » — mots communs du nom *Premature Ejaculation Diagnostic Tool* et
de l'expansion *Diagnostic and Statistical Manual*. Vérifiés un par un : aucun ne réaffirme les
statistiques rejetées. Un pivot qui est un mot ordinaire du nom propre qu'il sert à repérer est
structurellement inexploitable.)
**Priorité HAUTE, tête de file du méta santé depuis le 2026-08-27.** Reste à instruire : l'IELT
(délai d'éjaculation intravaginal chronométré), l'un des très rares critères d'efficacité
**objectifs** de tout le méta-domaine ; la dapoxétine et son statut réglementaire réel juridiction
par juridiction ; les ISRS hors AMM ; les anesthésiques topiques. Aucun chevauchement avec les
voisins. À écarter comme 2e thème : tout document centré sur le rayon gris (il redirait
`complements-amincissants` et `peptides-gris`) et tout document sur la libido androgénique
(`testosterone-homme-age` tient l'avis FDA du 20 avril 2026 sur le désir sexuel bas).

⚠️ **Aucune arête vers `testosterone-homme-age`** : il appartient à `muscle-vieillissement`, et
`portal.py` refuse tout slug hors du domaine dans `parcours`, `aretes` et `delimitations`. Le renvoi
n'a qu'une forme légale, une phrase d'`intro` sans slug. `inhibiteurs-pde5` l'a fait ainsi
(« l'axe androgénique […] fait l'objet d'un dossier distinct »), à reprendre tel quel.

(`inhibiteurs-pde5` : **FAIT le 2026-08-27**, retiré du backlog — 43e run /leanmonograph, 15e thème
santé, **crée le domaine `fonction-sexuelle`**. 10/10 sections retenues (plan à 10, aucune
troncature), 40 claims **21✓ / 18 corrigés / 1 rejeté après backstop** (le council avait rendu
19/13/8), 70 sources, 5 widgets, tableau de verdicts à 23 lignes sur 6 substances, ~8 800 mots.
Coût **~9,2M tok / 3 lancements / ~7 h** — dans la fourchette annoncée (8-12M), dont ~1M perdus sur
une reprise arrêtée par le garde-fou d'élagage. Contraste 0 violation en clair et en sombre après
correction d'un widget. Live vérifié par sha256 (double neutralisation).

**Le run le plus instructif du corpus sur la FIABILITÉ DU CODE, pas sur la preuve.** Le council a
rendu **8 rejets dont 7 FAUX**, et aucun ne venait d'un défaut de jugement des jurés :

1. **`normUrl` écrasait trois notices FDA en une seule source** — il supprimait la query string, or
   DailyMed adresse chaque étiquetage par `?setid=`. Sildénafil, tadalafil et vardénafil — trois
   médicaments — ne valaient qu'UNE source. Le seuil ≥2 devenait inatteignable sur les énoncés qui
   COMPARENT des étiquetages, c'est-à-dire exactement la section « Sécurité, doses, interactions »,
   obligatoire en santé. Le même défaut a **re-cassé la réparation manuelle à l'assemblage**.
   → Corrigé dans les **3** workflows + test de frontière `test_source_identity_query_string.mjs`.
2. **Le loader de reprise perdait une section par resume, en silence** — 2 reprises, 2 sections
   ré-auditées et leurs corrections manuelles écrasées. → Atténué (retry + log bruyant).

**Quatre erreurs de fond trouvées en re-vérifiant, aucune vue par les jurés** : l'IIEF est publié
dans *Urology* 1997;49:822-830 (et non *Int J Impot Res*) ; sa publication d'origine annonce
**10 langues**, pas 32 ; le domaine érectile se note **sur 30** et non « de 6 à 30 » (Q15 n'offre
pas de zéro) ; et le repère « 572 produits / 41,6 % » **que ce backlog transmettait** est de Justa
Neves & Caldas 2015 — daté. L'analyse complète (Tucker et al., *JAMA Netw Open* 2018) donne
**776 produits dont 45,5 % de sexuels, PREMIÈRE catégorie devant l'amincissement (40,9 %)**.
**Le pipeline a donc corrigé une erreur de son propre brief**, via un claim `contestable` — c'est
la meilleure justification observée pour la consigne « inclure au moins un claim contestable ».

**Fausse indépendance évitée de justesse** : Tucker et al. 2018 et l'enquête de Sacramento 2023 sont
l'œuvre de la **même équipe** (Food and Drug Branch, California Department of Public Health). Sans
la vérification, le document présentait deux confirmations indépendantes là où il n'y a qu'une
équipe. Ni le council ni le premier passage manuel ne l'avaient vu : c'est sorti en ouvrant la liste
d'auteurs. **Réflexe à garder : sur deux sources qui se corroborent trop bien, lire les auteurs.**

Le seul rejet subsistant est un VRAI rejet : le sildénafil seul n'améliore pas significativement
l'IIEF-5 dans la dysfonction psychogène (p = 0,06) — la prose le réfute au lieu de l'affirmer.

**Angle résiduel** : `complements-amincissants` cite déjà Tucker pour ses 40,9 % d'amincissants sans
instruire le versant sexuel. Les deux moitiés du même tableau vivent désormais dans deux documents
qui ne se renvoient pas l'un à l'autre — une arête à considérer si les deux domaines se rejoignent.)


### Désir sexuel hypoactif — `desir-sexuel-hypoactif` → `fonction-sexuelle`
**Verdict : gap réel — HAUTE, désigné trois fois par le corpus (ajout 2026-09-01).** Flibansérine,
Addyi, brémélanotide, Vyleesi, HSDD, « désir hypoactif », testostérone chez la femme : 0 occurrence
dans les 89 thèmes. Les seules mentions du désir sont des objets nommés puis laissés :
`inhibiteurs-pde5` décrit les domaines de l'IIEF (« le désir sexuel deux » items) sans jamais les
lire ; `testosterone-homme-age` nomme « trois essais principaux — fonction sexuelle, fonction
physique, vitalité » sans rapporter le Sexual Function Trial, puis conclut de l'avis FDA du 20 avril
2026 que « le seul terrain sur lequel le régulateur accepte d'avancer est celui du désir » — en
signalant que « la référence chiffrée qui circule sur l'essai d'appui n'a pas pu être retrouvée en
source primaire ». Le désir FÉMININ n'est ni traité, ni nommé, ni renvoyé. C'est aussi le candidat qui
corrige l'asymétrie du méta (aucun des 20 thèmes santé n'a la femme pour sujet). Deux variantes :
désir féminin en cœur avec une section pont sur le désir masculin laissé ouvert par le thème
testostérone (recommandée) ; ou désir féminin seul, sans contact avec `muscle-vieillissement`.

> Le désir sexuel bas et sa pharmacologie : ce que les essais mesurent quand on prétend traiter
> l'envie. Couvrir la construction du diagnostic (HSDD du DSM-IV au « trouble de l'intérêt/excitation »
> du DSM-5, prévalence selon l'instrument et la détresse), la flibansérine (deux refus FDA puis
> l'approbation de 2015 : l'effet mesuré — environ un demi-événement sexuel satisfaisant de plus par
> mois —, l'interaction avec l'alcool et la contrainte REMS, la campagne « Even the Score » et ce
> qu'elle apprend du lobbying par l'égalité — document-source sur les avis FDA), le brémélanotide
> (2019 : injection à la demande, nausées, taille d'effet), la testostérone chez la femme (le Global
> Consensus Position Statement de 2019 : indication étroite, dose physiologique, ménopause —
> document-source par nature ; les préparations hors AMM), le placebo et l'effet du seul fait de
> mesurer, les instruments (FSFI et ses seuils), puis la section pont — le désir masculin : le
> Sexual Function Trial des Testosterone Trials rapporté enfin (taille d'effet, chez qui), et l'avis
> FDA du 20 avril 2026 sur le désir sexuel bas de l'homme hypogonadique, à instruire en source
> primaire là où le thème testostérone n'a pas pu. Public : lecteur exigeant non spécialiste.
> ⚠️ Délimitations strictes : `inhibiteurs-pde5` tient l'érection (renvoi pour l'IIEF et son domaine
> désir) ; `ejaculation-precoce` tient l'IELT ; `testosterone-homme-age` tient l'axe androgénique de
> l'homme âgé, le muscle et l'os — la section pont ne reprend QUE le critère sexuel, en le citant ;
> aucune arête inter-domaines possible (`portal.py` refuse un slug hors domaine : renvoi dans
> l'`intro` seulement). Doctrine de preuve santé à recopier intégralement dans le brief. Domaine :
> fonction-sexuelle (3e thème).

### Dysfonction érectile au-delà des PDE5 — `dysfonction-erectile-hors-pde5` → `fonction-sexuelle`
**Verdict : gap réel à zéro recouvrement (ajout 2026-09-01).** Ondes de choc, Li-ESWT, PRP, cellules
souches, alprostadil, prothèse, dispositif à vide, traction : 0 occurrence (les « traction » du corpus
sont des « gagné en traction » de thèmes IA ; le seul « PRP » est le Probability Ranking Principle).
`inhibiteurs-pde5` ne quitte jamais ses quatre molécules ; sa section `populations-non-transportables`
ne nomme qu'une alternative, dans un essai isolé (« thérapie cognitivo-comportementale sexuelle
seule »), et ce qui se passe quand le comprimé échoue n'est pas posé. Le patron « régénératif sans
essai humain » est déjà celui de `peptides-gris` (BPC-157 : « presque entièrement animale et
mécanistique ») — précédent de méthode, objets neufs. Suite naturelle du thème PDE5.

> Quand le comprimé ne suffit pas : les traitements de la dysfonction érectile hors inhibiteurs de
> la PDE5, et le marché qui les entoure. Couvrir la 2e ligne établie (alprostadil intracaverneux et
> intra-urétral : efficacité, douleur, abandon ; dispositifs à vide), la 3e ligne (prothèses
> péniennes : satisfaction, infections, révision — le traitement le mieux évalué et le moins
> vendu), puis le rayon « régénératif » : ondes de choc de faible intensité (Li-ESWT : méta-analyses
> d'essais hétérogènes, effet sur l'IIEF vs seuil de différence minimale déjà posé par le thème
> PDE5, position des sociétés savantes — EAU/AUA « expérimental » ou recommandation faible :
> document-source), PRP (« P-shot » : essais de 2021-2023, taille d'effet, ce que vendent les
> cliniques), cellules souches (essais de phase 1, aucun critère d'efficacité robuste), traction et
> extension (Peyronie en renvoi), et la population qui décide de tout : après prostatectomie, diabète
> ancien, échec réel des PDE5 vs mauvais usage. Sécurité et prix. Public : lecteur exigeant non
> spécialiste. ⚠️ Délimitations strictes : `inhibiteurs-pde5` tient les quatre molécules, l'IIEF et sa
> MCID (PARTIR de sa règle IIEF/MCID, ne pas la redériver) et l'adultération ; `peptides-gris` tient le
> patron « littérature animale vendue comme humaine » (le citer) ; `testosterone-homme-age` tient
> l'hypogonadisme. Doctrine de preuve santé à recopier intégralement dans le brief. Domaine :
> fonction-sexuelle.

### Traitement hormonal de la ménopause — `menopause-hormonotherapie` → domaine à CRÉER
**Verdict : gap réel, hors domaine — tête de file d'un domaine « santé de la femme » (ajout
2026-09-01).** WHI, THM, ospémifène, prastérone, œstrogènes vaginaux, syndrome génito-urinaire :
0 occurrence. « Ménopause » ne sert que de qualificatif de population (`collagene` : « 131 femmes
ménopausées » ; `vitamine-d` : USPSTF « chez les femmes ménopausées » ; `creatine` : « +0,37 kg »), et
« œstrogène » n'est que mécanistique (`omega-3`, `testosterone-homme-age` : l'aromatase). Le versant
fonction sexuelle du THM (atrophie, dyspareunie, DHEA vaginale) ne ferait qu'une ou deux sections
d'un thème dont le cœur est cardiovasculaire, osseux et cognitif : ce n'est pas un 3e thème de
`fonction-sexuelle`, c'est le premier d'un domaine que le méta n'a pas — et le constat de la passe
(aucun des 20 thèmes santé n'a la femme pour sujet) plaide pour le créer. ⚠️ Comme pour tout domaine
neuf : il naît avec son premier thème et n'a de portail qu'au 2e — prévoir le 2e candidat
(`disponibilite-energetique-reds` est en nutrition-sportive ; un candidat « contraception hormonale
et ses risques » ou « endométriose » serait à instruire) avant de lancer, pour ne pas rejouer
`performance-cognitive`.

> Le traitement hormonal de la ménopause : vingt ans de peur, et ce que les essais disaient
> vraiment. Couvrir la WHI (2002 : l'arrêt du bras œstro-progestatif, les risques relatifs devenus
> titres, les risques absolus qu'ils cachaient ; le bras œstrogènes seuls et son résultat inverse
> sur le sein), la relecture par l'âge et la fenêtre temporelle (moins de 60 ans / moins de 10 ans
> après la ménopause : ce qui est démontré et ce qui est extrapolé), les bénéfices établis (bouffées
> de chaleur : le seul critère où l'effet est massif ; os et fractures — en renvoi vers
> l'ostéoporose ; syndrome génito-urinaire et œstrogènes locaux, ospémifène, prastérone), les
> risques (sein, thrombose selon la voie — orale vs transdermique —, AVC), le retrait par la FDA de
> l'encadré noir en 2025 (à corroborer en primaire : ce que l'agence a retiré et ce qu'elle a
> gardé), le marché de la « ménopause » (compléments, hormones « bio-identiques » compoundées, tests
> hormonaux inutiles), et les non-hormonaux (fézolinétant, ISRS). Public : lecteur exigeant non
> spécialiste. Délimitations : `collagene` et `vitamine-d` tiennent leurs molécules chez la femme
> ménopausée (renvoyer) ; `testosterone-homme-age` tient l'axe masculin — symétrie à écrire dans
> l'intro, pas en arête ; le candidat `osteoporose-pharmacologie` tient les médicaments de l'os.
> Doctrine de preuve santé à recopier intégralement dans le brief. Domaine : à créer par /arrange
> (« santé de la femme », id et blurb à proposer au premier run).
