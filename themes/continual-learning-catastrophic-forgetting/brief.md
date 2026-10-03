# Brief — Apprentissage continu et oubli catastrophique

L'angle directeur : **apprendre une tâche nouvelle sans détruire les anciennes** — pourquoi un
réseau entraîné par descente de gradient écrase ce qu'il savait, quelles familles de méthodes
résistent, et comment on mesure honnêtement qu'il a « retenu ». Le fil rouge : le dilemme
stabilité-plasticité, et un protocole d'évaluation qui décide souvent du verdict plus que la
méthode.

## Cadrage
Document de référence best-of, en français, public ingénieur ML. Audit de couverture par
lecture (2026-09-01, re-vérifié 2026-10-03) : `lora` mesure le domain forgetting et la
corrélation intruder dimensions / oubli ; `mixture-of-experts` évoque le gel de couches contre
l'oubli ; `agentic-memory` cite SWE-Bench-CL sans définir les métriques ;
`model-editing-unlearning` se délimite de l'oubli catastrophique sans le traiter. EWC, SI,
rejeu, incrémental par classe, LwF, métriques BWT/FWT : absents du corpus.

## Périmètre à couvrir
1. **Le phénomène** : McCloskey & Cohen (1989), Ratcliff (1990), French (1999) ; le dilemme
   stabilité-plasticité ; pourquoi le gradient partagé écrase.
2. **Les scénarios** : incrémental par tâche, par domaine, par classe (van de Ven & Tolias) —
   et pourquoi l'incrémental par classe est le plus dur.
3. **Régularisation** : EWC (Kirkpatrick et al. 2017, information de Fisher), SI, MAS.
4. **Rejeu** : experience replay, GEM/A-GEM, iCaRL, rejeu génératif (Shin et al.).
5. **Isolation de paramètres / architecture** : Progressive Networks, PackNet, masques.
6. **Distillation anti-oubli** : LwF (Li & Hoiem) — l'employer sans refaire la distillation.
7. **Métriques** : exactitude moyenne, backward/forward transfer (Lopez-Paz & Ranzato).
8. **Pièges d'évaluation** : task-ID connu ou non, frontières de tâches, mémoire et calcul non
   comptés, baselines de rejeu simples qui battent des méthodes sophistiquées.
9. **Le cas des LLM** : oubli au fine-tuning, alignment tax comme oubli, pré-entraînement
   continu (rejeu de données, re-warming du taux d'apprentissage).
10. **Limites**.

## Délimitations strictes
- `lora` : mécanique des adaptateurs — citer ses mesures d'oubli comme point de départ.
- `knowledge-distillation` : la distillation comme technique — LwF l'emploie, le dire.
- `rlhf-dpo` : over-optimization — ne pas refaire.
- `model-editing-unlearning` : l'oubli VOULU (édition, désapprentissage) — se délimiter
  mutuellement.
- `mixture-of-experts`, `agentic-memory` : citer, ne pas refaire.

Domaine : deep-learning-foundations.
