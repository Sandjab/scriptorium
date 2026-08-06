# Brief — streaming-quantiles-sampling

Sketches de flux pour quantiles et échantillonnage : résumer un flux de données en mémoire
bornée. Couvrir l'estimation de quantiles approchés (Greenwald-Khanna et la garantie ε,
t-digest et les centroïdes à compression variable, KLL et son optimalité), et
l'échantillonnage en flux (reservoir sampling : Algorithm R, échantillonnage pondéré A-Res,
échantillonnage distribué), avec les garanties d'erreur (rang vs valeur, ε-approximation) et
la fusionnabilité (mergeable summaries) pour le calcul distribué.
Positionnement : complète la famille des sketches de flux du domaine
probabilistic-structures-hashing. Public : ingénieur ML/data.

Délimitations (re-vérifiées par LECTURE de la prose des voisins le 2026-08-05) :
- `count-min-sketch` traite EN PROFONDEUR les fréquences, les heavy hitters et les **range
  queries par décomposition dyadique** (≤ 2 log n plages, une esquisse par niveau, Théorème 6
  de l'article original) — c'est la voie « par les fréquences » vers les requêtes de rang.
  NE PAS la re-dériver : la citer comme approche concurrente, et se centrer sur les résumés
  de quantiles fondés sur des comparaisons (GK, KLL, t-digest).
- Le blurb bibliographique de `count-min-sketch` mentionne les « quantiles » parmi les
  applications de l'article Cormode-Muthukrishnan — mention en biblio, aucun traitement en
  prose : le sujet est bien un gap.
- La **fusionnabilité** est déjà exposée des deux côtés : linéarité du CMS (fusion par
  addition cellule à cellule, `CMS.MERGE`) et mergeability de HLL (`PFMERGE` en O(m),
  merge en domaine compressé de HyperLogLogLog/UltraLogLog/ExaLogLog). Les citer ; l'angle
  neuf est ce qui est spécifique aux résumés de rang (mergeable summaries d'Agarwal et al.,
  fusion de KLL/GK, et ce que t-digest garantit ou non à la fusion).
- `hyperloglog` couvre la cardinalité distincte et ses régimes d'estimation — voisin de
  famille, pas de recouvrement.
- **Pont applicatif à citer** : `ensemble-learning` NOMME le « weighted quantile sketch »
  de XGBoost dans une énumération de techniques de passage à l'échelle, sans jamais
  l'expliquer — son mécanisme (quantiles pondérés pour le split finding) appartient à CE
  document.
- **Homonymies à écarter explicitement** (elles ne sont PAS le sujet) : le *quantile
  forecasting* de `time-series-forecasting` (MQ-RNN/MQ-CNN, TFT, quantiles 0,1/0,5/0,9 =
  prédiction probabiliste) et le quantile empirique conforme de `calibration-classifieurs`
  (⌈(n+1)(1−α)⌉/n, calcul exact hors flux).
