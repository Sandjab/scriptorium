# Bandits multi-bras (multi-armed bandits) — brief

**Slug** : `multi-armed-bandits` · **Domaine visé** : `classical-ml-time-series` · **Public** : ingénieur ML/data.

## Sujet
Décider en ligne sous incertitude. Cadre : récompense, regret, dilemme exploration / exploitation.

## Piliers à couvrir (à comparer au plan avant l'Extract)
1. Cadre : bandit stochastique sans état, regret (pseudo-regret, regret espéré), exploration vs exploitation.
2. Algorithmes de référence : ε-greedy, UCB1 et l'optimisme face à l'incertitude, Thompson sampling et sa lecture bayésienne.
3. Garanties : bornes de regret logarithmiques, borne inférieure de Lai-Robbins.
4. Bandits contextuels : LinUCB, bandits neuronaux.
5. Extensions pratiques : non-stationnarité, feedback retardé, contraintes de budget.
6. Applications : A/B testing adaptatif, allocation de trafic, recommandation, sélection de prompts ou de modèles.

## Délimitations
- Le RL complet (états, transitions) relève de `reinforcement-learning-fundamentals` : ici, cadre sans état et garanties de regret.
- `recommender-systems` traite les modèles de préférence et renvoie explicitement l'exploration (cold start, feedback loops) aux bandits : on reprend ce fil sans refaire la recommandation.
- `ab-testing-experimentation-en-ligne` (candidat) traitera l'expérimentation à horizon fixe : ici, seulement la version adaptative et son coût inférentiel.
