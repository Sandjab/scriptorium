# Tabular foundation models

Sujet : les *tabular foundation models* (TFM) — modèles de fondation pré-entraînés pour la
prédiction sur données tabulaires, dont **TabPFN** (Prior-data Fitted Network) et sa v2,
capables de **prédiction in-context** (un seul passage avant, sans entraînement par jeu de
données) sur de petits jeux tabulaires.

Cadrage : panorama vérifié pour lecteur informé. Couvrir —
- le problème historique du ML tabulaire (là où le **gradient boosting**, XGBoost/LightGBM, a
  longtemps dominé le deep learning) et pourquoi le tabulaire résistait au DL ;
- le principe **PFN / in-context learning** : pré-entraînement bayésien sur des jeux synthétiques
  tirés d'un *prior*, inférence = approximation du posterior prédictif en un forward ;
- **TabPFN** (Hollmann et al.) et **TabPFN v2** (Nature 2025), capacités/limites (taille des jeux,
  nombre de features/classes, régression) ;
- l'écosystème et les concurrents (autres TFM, approches ICL tabulaires, AutoML), les benchmarks
  (vs gradient boosting), le passage à l'échelle, la calibration, les angles morts.

Frontière : modèles pour TABLES (lignes/colonnes hétérogènes), pas séries temporelles ni vision.
Domaine pressenti = ML classique & séries temporelles (terrain du ML tabulaire) — le TFM y est
l'évolution neuronale/foundation de ce terrain (tension blurb « hors deep learning » à arbitrer).
