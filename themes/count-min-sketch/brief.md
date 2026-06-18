# Count-Min Sketch

Sujet : le Count-Min Sketch (CMS), structure de données probabiliste compacte pour
estimer les fréquences d'éléments dans un flux (stream) en espace sous-linéaire.

Cadrage : compagnon de fréquence des autres structures probabilistes du scriptorium —
là où HyperLogLog estime la *cardinalité* et le filtre de Bloom l'*appartenance*, le
Count-Min Sketch estime le *compte / la fréquence* (et les heavy hitters). Couvrir le
principe (table de compteurs × fonctions de hachage, estimation par minimum), les
garanties d'erreur (paramètres ε / δ, biais unilatéral de sur-estimation), les
variantes (Count-Mean-Min, conservative update), et les usages réels (flux réseau,
bases de données, NLP).
