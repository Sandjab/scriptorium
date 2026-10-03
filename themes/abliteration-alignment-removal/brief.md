# Brief — Retirer l'alignement par les poids : direction de refus et ablitération

L'angle directeur : **ce que l'alignement d'un modèle à poids ouverts devient quand on touche aux
poids ou aux activations** — le refus porté par une direction du flux résiduel, son ablation
(« abliteration », mot-valise ablation + obliteration ; « oblitération » n'est pas un terme
établi), le retrait par fine-tuning, et ce que cela révèle de la PROFONDEUR de l'alignement. Le
fil rouge : masquer n'est pas effacer — l'alignement recouvre une capacité sans la retirer.

## Cadrage
Document de référence best-of, en français, public ingénieur ML/sécurité. Gap vérifié par
LECTURE (2026-10-03) : `llm-safety-jailbreaks` ne couvre que les attaques par la requête (BEB
borné aux poids figés) ; `mechanistic-interpretability` cite Rogue Scalpel et Goodfire sans la
direction de refus d'Arditi et al. ni l'orthogonalisation des poids ; `model-editing-unlearning`
porte le même motif « masquer ≠ effacer » pour le savoir désappris. Fine-tuning malveillant :
absent du corpus.

⚠️ **Sujet à double usage** : décrire mécanismes et mesures publiés, sans recette opératoire
(pas de procédure pas-à-pas, pas d'hyperparamètres d'attaque, pas de pointeurs vers des modèles
ou scripts prêts à l'emploi).

## Périmètre à couvrir
1. **Le résultat fondateur** : le refus est médié par une seule direction (Arditi et al. 2024) —
   l'ablater supprime le refus, l'ajouter le provoque ; différence de moyennes.
2. **L'ablitération** : orthogonalisation des poids contre cette direction, modèles
   « abliterated » publiés en open-weights, coût mesuré en capacités.
3. **Variantes et limites** : refus multidimensionnel ou non, concepts/cônes de refus,
   généralisation hors distribution.
4. **Retrait par fine-tuning** : quelques exemples nuisibles, voire bénins, suffisent (Qi et al.
   2023, « shadow alignment »), LoRA.
5. **Profondeur de l'alignement** : alignement superficiel (quelques premiers tokens) vs profond.
6. **Défenses** : résistance à la modification des poids (tamper-resistance, TAR…), et leur
   évaluation adaptative (attaques qui les cassent).
7. **L'enjeu de publication des poids ouverts**.
8. **Limites**.

## Délimitations strictes
- `llm-safety-jailbreaks` : toutes les attaques par la requête — le citer en contrepoint.
- `mechanistic-interpretability` : l'outillage (SAE, steering, probing) — citer Rogue Scalpel et
  Goodfire sans les refaire.
- `model-editing-unlearning` : l'oubli voulu et la récupération du savoir désappris — même motif,
  le dire.
- `rlhf-dpo` : la mécanique de l'alignement lui-même.
- `lora` : la mécanique des adaptateurs.
- `continual-learning-catastrophic-forgetting` : l'oubli des CAPACITÉS sous l'alignement
  (alignment tax) — ici le sens inverse, l'alignement perdu sous le fine-tuning.

Domaine : llm-agents-generation (voisin de llm-safety-jailbreaks), à trancher par /arrange.
