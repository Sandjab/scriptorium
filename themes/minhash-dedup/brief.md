# MinHash et déduplication par similarité d'ensembles

Candidat du backlog (`docs/candidate-themes.md`, priorité moyenne, remonté de « basse » le
2026-09-01 sur renvoi cassé), lancé le 2026-09-18 en 59e run `/leanmonograph`.
Domaine visé : `probabilistic-structures-hashing` (6 thèmes ; `/arrange` tranchera l'insertion).

⚠️ Ce fichier est une TRACE : `workflow.js` ne le lit pas. Le cadrage effectif passe
entièrement par `args.subject`.

## Gap re-vérifié avant lancement (2026-09-18)

Neuf thèmes ajoutés depuis le verdict du 2026-09-01, aucun ne touche le hachage. Lecture du
contexte de chaque mention (pas au grep seul) :
- `pretraining-data-curation` : MinHash n'y est qu'un NOM d'outil (FineWeb −44 % par dump,
  SlimPajama 13-grammes à Jaccard ≥ 0,8, MassiveText, datatrove) ; la section
  `deduplication-effets` écrit « la mécanique des signatures, MinHash et LSH, relève d'un autre
  document ; on la tient ici pour acquise ». C'est LE renvoi cassé que ce thème répare.
- `approximate-nearest-neighbor` : section « LSH : le socle théorique » (530 mots) — famille
  (r, cr, p₁, p₂), exposant ρ, E2LSH. À citer, ne pas re-dériver.
- `bloom-filters`, `bm25-inverted-index` : Broder n'y apparaît que pour Summary Cache et WAND.
- `SimHash`, `b-bit`, `min-wise`, `minwise` : 0 occurrence dans le corpus.

## Délimitations (à tenir dans `args.subject`)

- `approximate-nearest-neighbor` garde le cadre LSH générique et les vecteurs denses ;
  `text-embeddings` garde ALSH/MIPS ; `pretraining-data-curation` garde les EFFETS de la
  déduplication sur les modèles (mémorisation, ablations FineWeb). Ici : la MÉCANIQUE des
  signatures et ce qu'elle garantit.
- Angle propre : **ce qu'une signature MinHash estime, avec quelle variance, et ce que
  l'amplification par bandes fait à la courbe de rappel** — min-wise independence et ses
  approximations (k-wise, permutations linéaires), b-bit minwise, one-permutation hashing,
  banding et courbe en S, SimHash pour le cosinus, la déduplication de corpus comme application
  phare (Broder 1997 → LLM), et les faux-doublons/faux-uniques en production.

⚠️ Les pistes du prompt du backlog ont été écrites sans balayage web : à corroborer en source
primaire au Sweep, jamais des faits.
