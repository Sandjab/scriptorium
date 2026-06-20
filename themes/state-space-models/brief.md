# Brief — State Space Models (SSM) & Mamba

**Sujet (tel que fourni)**

State Space Models (SSM) et Mamba pour la modélisation de séquences en deep learning : les
modèles à espace d'états comme alternative sub-quadratique à l'attention. Couvrir le principe
(représentation état-continu (A, B, C, D), discrétisation par le pas Δ, dualité récurrence
linéaire ↔ convolution longue), la lignée canonique HiPPO → S4 (paramétrisation structurée
diagonale / DPLR) → S5, puis la rupture Mamba / S6 (sélectivité dépendante de l'entrée, scan
parallèle « hardware-aware ») et Mamba-2 (formulation SSD, pont théorique avec l'attention
linéaire). Positionnement clé : complexité linéaire en longueur de séquence et inférence
récurrente à coût mémoire constant par token, vs le coût quadratique de l'attention ; forces
et limites mesurées (rappel associatif / copie in-context, contexte long), architectures
hybrides attention+SSM (ex. Jamba). Public visé : ingénieur ML.

**Cadrage**

- Domaine taxonomique pressenti : `deep-learning-foundations` (à confirmer via `/arrange`).
- Délimitations : ne pas reprendre en détail les transformers ni l'attention (déjà couverts
  dans le corpus) — les citer seulement comme point de comparaison ; rester sur les SSM de
  séquençage en deep learning ; ne convoquer les SSM linéaires classiques (filtre de Kalman,
  séries temporelles) que pour la filiation conceptuelle, sans en faire le cœur du document.
