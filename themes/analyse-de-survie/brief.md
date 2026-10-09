# Brief — Analyse de survie : prédire quand, avec des observations qu'on n'a pas vues finir

L'angle directeur est la **censure** : une partie des durées n'est observée qu'à moitié (le client
n'a pas encore résilié, la machine n'est pas encore tombée en panne, le patient est perdu de vue).
Chaque méthode du document se lit comme une façon d'utiliser cette information partielle sans la
jeter ni la traiter comme un événement. Le document dit aussi ce qu'un hazard ratio affirme et ce
qu'il n'affirme pas.

## Cadrage
Document de référence best-of, en français, niveau ingénieur ML / data. Double usage : référence ML
(churn, panne, délai de conversion) ET clé de lecture des hazard ratios que les thèmes santé du
corpus citent sans en expliquer la méthode.

## Périmètre à couvrir
- **Censure** : à droite, à gauche, par intervalle ; troncature à gauche ; censure informative ou
  non informative ; pourquoi une régression ordinaire ou une classification binaire se trompent
  (on jette les censurés, ou on les compte comme non-événements).
- **Grandeurs de base** : fonction de survie, fonction de risque instantané (hazard), risque cumulé.
- **Non paramétrique** : estimateur de Kaplan-Meier, Nelson-Aalen, test du log-rank.
- **Modèle de Cox** : risques proportionnels, vraisemblance partielle, ce que signifie un hazard
  ratio et ce qu'il ne dit pas (relatif vs absolu, non-proportionnalité, résidus de Schoenfeld,
  critique de Hernán « The Hazards of Hazard Ratios »), alternatives (RMST, modèles AFT
  paramétriques — Weibull, log-normal).
- **Risques concurrents** : incidence cumulée (Aalen-Johansen), hazard spécifique vs
  sous-distribution de Fine-Gray, pourquoi 1 − Kaplan-Meier surestime en présence de risques
  concurrents.
- **Métriques** : C-index de Harrell et d'Uno, AUC dépendante du temps, Brier score dynamique et
  integrated Brier score (pondération IPCW), calibration dans le temps.
- **Versions ML** : random survival forests, gradient boosting de survie, DeepSurv, DeepHit,
  modèles à temps discret ; bibliothèques (lifelines, scikit-survival, pycox).
- **Pièges** : fuite temporelle (variables connues après l'origine), biais du temps immortel,
  choix de l'origine du temps, covariables dépendantes du temps.
- **Applications hors médecine** : churn, maintenance prédictive, délai de conversion.

## Délimitations strictes
- `calibration-classifieurs` garde le Brier statique binaire et la couverture conforme : les citer,
  ne pas les redériver.
- `ensemble-learning` garde le boosting et les forêts en général : ne traiter ici que leur
  adaptation à la censure.
- `time-series-forecasting` ne touche jamais aux données censurées : frontière nette (et « Cox »
  y est Box-Cox, sans rapport).
- `causal-inference` garde l'identification d'effets et la censure vue comme collider dans un DAG
  (Hernán & Robins, ch. 8) : y renvoyer ; ne pas refaire l'IPW causal ni l'émulation d'essai cible
  au-delà d'un renvoi.
- Les thèmes santé gardent leurs essais (SELECT, REDUCE-IT, TRAVERSE…) : ne pas en rediscuter les
  résultats, au plus les citer comme exemples de lecture d'un HR.

Domaine : `classical-ml-time-series`.
