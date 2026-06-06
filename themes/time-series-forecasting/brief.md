# Brief — time-series-forecasting

**Cadrage** : panorama vérifié des méthodes de prévision sur séries temporelles, des
statistiques classiques aux foundation models zero-shot. Document de référence best-of :
familles de méthodes, ce que chacune apporte, quand elle gagne, et les frameworks qui les
packagent.

---

## Sujet tel que fourni

Statistiques classiques

ARIMA / SARIMA / SARIMAX — autorégressifs avec différenciation, saisonnalité et variables exogènes. Référence historique.
ETS (Exponential Smoothing) — Holt-Winters et variantes, état-espace selon Hyndman.
Theta — décomposition simple, souvent imbattable sur séries courtes (gagnante M3).
VAR / VECM — multivarié, cointégration.

Décomposition / structurel

Prophet (Meta) — modèle additif : trend + saisonnalités Fourier + holidays + changepoints. Robuste aux trous, peu de tuning.
NeuralProphet — réécriture PyTorch avec composantes AR et lagged regressors.
TBATS / BATS — saisonnalités multiples et complexes (intra-day + intra-week + annuel).
STL + ARIMA — décomposition Loess puis ARIMA sur le résidu.
BSTS (Bayesian Structural Time Series) — composantes en état-espace, inférence MCMC. CausalImpact de Google s'appuie dessus.

Machine learning tabulaire

Régressions (linéaire, ridge, lasso) sur features lag/rolling/calendaires.
Gradient boosting (XGBoost, LightGBM, CatBoost) — dominent les compétitions Kaggle de forecasting depuis M5.
Random Forest / Extra Trees — moins courants, peu d'extrapolation.

Deep learning spécialisé

DeepAR (Amazon) — RNN probabiliste, sorties paramétriques.
N-BEATS / N-HiTS — empilement de blocs MLP, pure feed-forward, top performers académiques.
TFT (Temporal Fusion Transformer) — attention multi-head + gating, interprétable.
Informer / Autoformer / FEDformer / PatchTST — variantes transformer long-horizon.
TSMixer (Google) — pur MLP-mixer, compétitif avec les transformers.
DLinear / NLinear — rappels que parfois une linéaire bat les transformers (papier "Are Transformers Effective for TSF?").

Foundation models (zero-shot)

TimeGPT (Nixtla) — propriétaire, API.
Chronos (Amazon) — basé sur T5, tokenisation des valeurs.
Moirai (Salesforce) — multi-fréquence.
TimesFM (Google) — decoder-only, 200M params.
Lag-Llama — open-source, Llama-style.
TabPFN-TS — extension TabPFN aux séries.

Bayésien / probabiliste

Filtre de Kalman — état-espace linéaire-gaussien.
GP (Gaussian Processes) — kernels périodiques, incertitude native, scaling limité.
PyMC / Stan / NumPyro — modèles hiérarchiques sur mesure.

Méthodes hybrides / ensemble

ES-RNN (Smyl) — gagnant M4, exponential smoothing × LSTM.
MQ-CNN / MQ-RNN — quantile forecasting.
Stacking / blending — combinaison pondérée, souvent la vraie meilleure pratique en prod.

Cas particuliers

Croston / SBA / TSB — séries intermittentes (demande sporadique, spare parts).
Hidden Markov Models — régimes discrets.
Change point detection (Bayesian Online, PELT) — pas du forecasting strict mais souvent en amont.

Frameworks qui packagent tout ça

statsforecast / mlforecast / neuralforecast (Nixtla) — API uniforme, très rapide.
GluonTS / PyTorch Forecasting / Darts — couvrent classiques + DL.
sktime — interface unifiée style scikit-learn.
