# Brief — Édition de connaissances et désapprentissage

L'angle directeur : **retirer ou modifier après coup ce qu'un modèle a appris, sans tout
ré-entraîner** — et mesurer si c'est vraiment fait. Le fil rouge : une édition ou un oubli
qui « réussit » au test direct peut masquer sans effacer.

## Cadrage
Document de référence best-of, en français, public ingénieur ML / conformité. Audit de
couverture par lecture (2026-10-02) : critères et échecs de l'édition, désapprentissage
machine, benchmarks (TOFU, WMDP, MUSE) et droit à l'effacement absents du corpus ; la
localisation (ROME comme test causal) et l'extraction de données d'entraînement déjà
couvertes par des voisins — à citer, pas à refaire.

## Périmètre à couvrir
1. **Édition par localisation puis modification** comme TECHNIQUE : MLP vus comme mémoires
   clé-valeur, mise à jour de rang un (ROME), édition massive (MEMIT), méta-apprenants (MEND) ;
   alternatives sans toucher aux poids (citer RAG en une phrase).
2. **Critères d'une bonne édition** (efficacité, généralisation aux paraphrases,
   localité/spécificité ; CounterFact, zsRE) et **échecs mesurés** : effets de ricochet sur
   les faits liés, dégradation après éditions séquentielles.
3. **Désapprentissage machine** : exact (ré-entraînement, SISA) vs approché ; ascension de
   gradient et ses instabilités, NPO, RMU.
4. **Benchmarks** : TOFU, WMDP, MUSE — ce que chacun mesure (oubli, utilité conservée,
   confidentialité) ; extraction et inférence d'appartenance comme outils d'évaluation.
5. **Attaques et oubli superficiel** : réapprentissage rapide, information résiduelle
   récupérable, désapprentissage qui masque sans effacer.
6. **Cadre réglementaire** : droit à l'effacement (RGPD art. 17) appliqué aux modèles
   entraînés, et ce que la technique permet ou non d'en garantir.
7. **Limites**.

## Délimitations strictes
- `mechanistic-interpretability` : causal tracing, ROME/MEMIT comme test de localisation,
  « localiser n'est pas éditer » (Hase et al. 2023), illusion d'interprétabilité de Makelov,
  steering — citer, ne pas refaire.
- `llm-safety-jailbreaks` : extraction de données d'entraînement, « le RLHF recouvre sans
  effacer », défenses par refus — citer.
- `pretraining-data-curation` : déduplication comme prévention en amont, lois de mémorisation
  — citer (« ne pas apprendre » vs « oublier »).
- `benchmark-contamination` : inférence d'appartenance et ses limites — citer.
- `lora` : oubli catastrophique SUBI à l'ajustement fin — le distinguer de l'oubli VOULU.
- `rlhf-dpo` : forme de DPO — y renvoyer si NPO est présenté.
- `llm-watermarking-detection` : règlement IA art. 50 — autre texte que le RGPD art. 17.
- `privacy-preserving-ml` (candidat) : confidentialité différentielle et mémorisation.
