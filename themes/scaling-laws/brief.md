# Brief — scaling-laws

Lois d'échelle (scaling laws) du deep learning : comment la perte décroît avec les paramètres,
les données et le compute, et comment allouer un budget de calcul de façon compute-optimale.
Couvrir les lois en loi de puissance (Kaplan et al. 2020), la révision Chinchilla (Hoffmann et
al. 2022 : ~20 tokens/paramètre), le compromis taille-modèle vs données à budget FLOPs fixe, les
lois aval (transfert, inférence) et leurs limites (qualité des données, plafonds, émergence
contestée). Public : ingénieur ML / décideur technique. Délimitations : ne pas re-dériver
l'architecture transformer ni l'optimisation ; rester sur la relation empirique perte↔(N, D, C).

Domaine : deep-learning-foundations.
