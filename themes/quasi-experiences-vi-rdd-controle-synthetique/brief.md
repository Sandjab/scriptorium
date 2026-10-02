# Brief — Quasi-expériences : variables instrumentales, discontinuité, contrôle synthétique

L'angle directeur est celui du thème parent `causal-inference` : **quelle hypothèse chaque
méthode achète, et comment on la met à l'épreuve**. Les trois stratégies traitées ici
identifient un effet sans supposer la non-confusion ; elles la remplacent par une autre
hypothèse, souvent invérifiable en partie, dont le document dit le prix.

## Cadrage
Document de référence best-of, en français, niveau ingénieur ML / data. Sorti du 68e run :
le plan de `causal-inference` a privilégié le versant ML et laissé ces piliers hors plan
(audit par lecture du document publié).

## Périmètre à couvrir
- **Variables instrumentales** : pertinence, exclusion, indépendance, monotonie ; LATE et
  compliers ; 2SLS ; instruments faibles (diagnostic et inférence robuste) ; hétérogénéité.
- **Régression sur discontinuité** : nette et floue ; estimation locale, choix de fenêtre,
  inférence ; tests de manipulation de la variable de score ; tests de continuité des
  covariables ; validité externe limitée au seuil.
- **Contrôle synthétique** : construction des poids, ajustement pré-traitement, inférence par
  placebo ; variantes récentes.
- **Rapport aux méthodes ML** : DML avec instrument, forêts instrumentales, et ce que le ML
  change (ou ne change pas) aux hypothèses d'identification.

## Délimitations strictes
- `causal-inference` tient le cadre (résultats potentiels, DAG, propension, AIPW, DiD
  échelonnée, DML, méta-learners) : le citer, ne pas le refaire.
- `time-series-forecasting` tient CausalImpact/BSTS : le citer en pont.
- Toute attribution (auteurs, années, chiffres) se vérifie en source primaire au Sweep ;
  aucune n'est donnée ici comme fait.

Domaine : `classical-ml-time-series`.
