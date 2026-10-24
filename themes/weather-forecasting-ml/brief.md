# Prévision météorologique par apprentissage — brief

**Slug** : `weather-forecasting-ml` · **Domaine visé** : nouveau `ai-for-science` (si un 3e thème, avec `protein-structure-prediction`) sinon `deep-learning-foundations` — à trancher par /arrange · **Public** : ingénieur ML.

## Sujet
La prévision météorologique apprise : des réanalyses aux modèles opérationnels. Ce que les modèles appris savent faire face à la prévision numérique physique, comment on les évalue, et où ils échouent.

## Piliers à couvrir (à comparer au plan avant l'Extract)
1. Le problème : réanalyse ERA5 comme donnée d'entraînement, prévision numérique physique (IFS de l'ECMWF) comme référence, échéances et variables.
2. Les architectures déterministes : Pangu-Weather (Nature 2023), GraphCast (Science 2023, GNN sur maillage icosaédrique), FourCastNet.
3. Le probabiliste et les ensembles : GenCast (diffusion, Nature), prévision d'ensemble.
4. Le passage en opérationnel à l'ECMWF : AIFS déterministe, AIFS ENS (dates du backlog À VÉRIFIER en source primaire : 25 février 2025, 1er juillet 2025, ENS v2 le 12 mai 2026).
5. L'évaluation : WeatherBench 2, CRPS, RMSE/ACC, scores auto-déclarés par chaque labo.
6. Les limites : lissage, extrêmes, robustesse hors du climat d'entraînement.
7. La cohabitation physique/IA (position de l'ECMWF).
8. Limites et idées reçues ; écosystème.

## Prudence
- Les chiffres de skill sont souvent auto-déclarés par le labo qui publie le modèle : indépendance par TRAVAIL, pas par URL ; un communiqué ECMWF relève de `document-source`.
- Résolutions et échéances divergent selon les sources : ne jamais comparer deux scores sans comparer le protocole (résolution, année de test, référence).

## Délimitations
- `graph-neural-networks` garde le message passing générique (citer sans refaire).
- `diffusion-models` garde le mécanisme de diffusion.
- `time-series-forecasting` garde la prévision de séries.
- `generative-adversarial-networks` garde DGMR (nowcasting radar) ; `calibration-classifieurs` l'héritage du score de Brier.
