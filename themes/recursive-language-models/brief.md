# Recursive Language Models (RLM)

**Sujet** : Recursive Language Models — paradigme d'inférence où un modèle de langage,
piloté dans un environnement (REPL / boucle d'outils), décompose et **s'appelle
récursivement** sur des sous-parties de son propre contexte plutôt que de tout ingérer en
un seul passage. Vise à dépasser la dégradation des longs contextes (« context rot ») et à
traiter des entrées quasi illimitées à coût d'inférence borné par appel.

**Cadrage** :
- Origine et définition : RLM comme stratégie d'inférence (root LM dans un REPL Python qui
  manipule le contexte comme une variable/environnement, et lance des sous-appels LM/RLM).
- Distinguer RLM de notions voisines : agents récursifs, chunking/RAG, map-reduce sur
  contexte, recursion of thought, scaffolds long-context.
- Mécanique : décomposition récursive, profondeur, gestion du sous-contexte, agrégation.
- Évaluation : bénéfices sur tâches long-contexte (p. ex. OOLONG, benchmarks « needle »),
  coût/latence, limites et conditions d'échec.
- Théorie : ce que la récursion change vs un seul long forward pass ; rapport au
  « context rot » et aux plafonds de la fenêtre de contexte.
