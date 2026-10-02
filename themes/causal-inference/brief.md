# Brief — Inférence causale pour l'ingénieur ML : estimer des effets, pas des corrélations

L'angle directeur est l'**identification avant l'estimation** : un estimateur, aussi flexible
soit-il (forêt, réseau, DML), n'estime un effet causal que sous des hypothèses d'identification
qu'aucune donnée observationnelle ne teste entièrement. Le document dit, pour chaque méthode,
quelle hypothèse elle achète et comment on la met à l'épreuve.

## Cadrage
Document de référence best-of, en français, niveau ingénieur ML / data. Il pose le socle que
plusieurs thèmes du corpus utilisent sans l'expliquer.

## Périmètre à couvrir
- **Résultats potentiels** (Neyman-Rubin) : ATE/ATT/CATE, ignorabilité (non-confusion),
  positivité/recouvrement, SUTVA ; l'essai randomisé comme référence.
- **Graphes causaux** (Pearl) : DAG, confondants, colliders, médiateurs, critère backdoor,
  do-calcul ; le lien entre les deux cadres.
- **Estimation sous non-confusion** : appariement et scores de propension, IPW, estimateurs
  doublement robustes (AIPW), diagnostics d'équilibre et de recouvrement.
- **Stratégies quasi-expérimentales** : différence de différences (tendances parallèles et ses
  versions récentes à adoption échelonnée), variables instrumentales (LATE), régression sur
  discontinuité, contrôle synthétique.
- **ML pour l'effet** : double/debiased machine learning (orthogonalité, cross-fitting),
  méta-learners S/T/X/R/DR, forêts causales, modélisation d'uplift et son évaluation (Qini).
- **Pièges et robustesse** : biais de sélection et de collider, confondants non observés,
  analyses de sensibilité (E-value, Rosenbaum, bornes), tests placebo, falsification.

## Délimitations strictes
- `time-series-forecasting` garde CausalImpact/BSTS : le citer en pont, ne pas le redériver.
- `learning-to-rank` garde l'IPS sur les clics (LTR non biaisé) : le citer comme application.
- `ia-emploi-marche-du-travail` et `ia-productivite-esn` gardent leurs études d'effets de l'IA :
  ne pas les rediscuter, au plus un renvoi.
- La mécanique des tests A/B en ligne (CUPED, peeking, tests séquentiels) relève du candidat
  `ab-testing-experimentation-en-ligne` ; les bandits relèvent de `multi-armed-bandits`.
- La causalité de Granger (séries temporelles) n'est PAS de l'inférence causale au sens de ce
  document : le dire en une phrase, sans plus.

Domaine : `classical-ml-time-series`.
