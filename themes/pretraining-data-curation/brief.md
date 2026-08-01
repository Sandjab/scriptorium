# Curation des données de pré-entraînement des LLM

**Slug** : `pretraining-data-curation` · **Domaine visé** : `llm-agents-generation` (à trancher par `/arrange`)
**Verdict backlog** : gap réel, angle neuf net — le pipeline de données lui-même n'est traité nulle part.

## Sujet

Curation des données de pré-entraînement des LLM : ce qui entre dans le modèle. Couvrir le
pipeline (extraction depuis Common Crawl, détection de langue, filtres heuristiques puis filtres
par modèle), la déduplication exacte et approximative et ses effets (mémorisation, qualité), les
mélanges de domaines et leur optimisation (DoReMi, données synthétiques), la contamination des
benchmarks, la généalogie des corpus ouverts (C4, The Pile, RefinedWeb, FineWeb et sa démarche
d'ablations systématiques, Dolma) et les questions de licence/PII.

Public : ingénieur ML.

## Délimitations

Vérifiées par greps ciblés sur les `knowledge.json`/`manifest.json` publiés le 2026-07-31
(63 thèmes), avec lecture du contexte de chaque mention.

- **`scaling-laws`** couvre le régime *data-constrained* (Muennighoff et al. 2023 : ~4 epochs
  de répétition à perte négligeable, gains jusqu'à ~16 epochs puis effondrement) **ET le
  *data pruning*** (Sorscher et al. : élagage battant la loi de puissance vers une décroissance
  exponentielle, ResNets sur CIFAR-10/SVHN/ImageNet ; l'élagage aléatoire reste sur la loi de
  puissance) — **les citer en pont, ne PAS les re-dériver**. L'angle neuf est le pipeline
  amont, pas l'allocation calcul/données ni la théorie de l'élagage.
- **`llm-evaluation`** traite déjà la **contamination des benchmarks côté évaluation**
  (contamination sémantique — instances paraphrasées ou traduites —, audits empiriques sur
  des benchmarks de question-réponse, distorsion des leaderboards). Ici : se centrer sur la
  **détection et la décontamination côté corpus** (n-grammes, chevauchement train/test,
  protocoles de décontamination des corpus publiés) et citer `llm-evaluation` pour le versant
  mesure.
- **`minhash-dedup`** (candidat non fait) porte la mécanique MinHash/LSH — **un pont suffit** :
  ici la déduplication est traitée par ses *effets* (mémorisation, qualité, exact vs approché
  à l'échelle du corpus), pas par son algorithmique.
- **`text-embeddings`** couvre la tokenization (BPE, byte-level, SentencePiece) et les vecteurs
  GloVe entraînés sur Common Crawl — la citer sans re-dériver.
- **`document-ai`** mentionne le parsing de 2,1 M de PDF issus de Common Crawl (outil de
  conversion) — voisin périphérique, pas un recouvrement.
- **`privacy-preserving-ml`** (candidat non fait) porterait DP-SGD et la mémorisation côté
  protection — ici la PII est traitée comme contrainte de curation (filtrage, licences), pas
  comme mécanisme de garantie formelle.

## Couverture vérifiée nulle (greps du 2026-07-31)

`RefinedWeb`, `FineWeb`, `DoReMi`, `Dolma`, `MinHash` : 0 occurrence dans le corpus publié.
`C4` comme corpus de pré-entraînement : 1 mention incidente (URL suivies pour un jeu
multimodal) — les autres matches sont des arbres de décision C4.5 et des couleurs hex.
`Common Crawl` : 3 mentions périphériques, aucune sur l'extraction WARC/WET ou le pipeline.
