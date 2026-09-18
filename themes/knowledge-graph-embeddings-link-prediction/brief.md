# Plongements de graphes de connaissances — compléter un graphe par prédiction de liens

Candidat du backlog (`docs/candidate-themes.md`, priorité moyenne, ajouté le 2026-09-01,
verdict « gap réel » par lecture), lancé le 2026-09-18 en 58e run `/leanmonograph`.
Domaine visé : `information-retrieval-representation` (14 thèmes ; `/arrange` tranchera
l'insertion, attendue après `knowledge-graph-construction`).

⚠️ Ce fichier est une TRACE : `workflow.js` ne le lit pas. Le cadrage effectif passe
entièrement par `args.subject`.

## Gap re-vérifié avant lancement (2026-09-18)

Le verdict du backlog date du 2026-09-01 (lecture des voisins). Depuis, huit thèmes ont été
ajoutés (`git log --since=2026-09-01`), tous santé, `ai-organizations` ou démonstration formelle
— aucun ne touche les graphes de connaissances. `TransE`, `ComplEx`, `RotatE`, `DistMult`,
`CompGCN`, `FB15k`, `WN18` : **0 occurrence** (grep sensible à la casse, frontières de mots)
dans les `manifest.json`/`knowledge.json` publiés. Seules traces, lues en contexte :
- `graph-neural-networks` nomme « la prédiction de liens (link prediction) » comme catégorie
  OGB (ogbl-collab, ogbl-citation2, Hits@K, MRR) sur graphes HOMOGÈNES, et R-GCN comme modèle
  du produit Neptune ML — sans un mot sur les graphes multi-relationnels ni les scores de triplet.
- `knowledge-graph-construction` pose l'hypothèse de monde ouvert (« une arête absente signifie
  "inconnu", jamais "faux" ») sans jamais traiter l'incomplétude comme problème d'inférence.

## Délimitations (du backlog, à tenir dans `args.subject`)

- `knowledge-graph-construction` garde la CONSTRUCTION (schéma, OWA, SPARQL) ; ici on COMPLÈTE.
- `graph-neural-networks` garde le message passing et OGB ; citer R-GCN/CompGCN comme
  comparaison relationnelle, ne pas re-dériver la convolution de graphe.
- `entity-linking-disambiguation` garde le liage de mentions ; `relation-extraction` garde
  l'extraction depuis le texte.
- L'angle propre : **ce qu'un score de triplet garantit et ce qu'il ne garantit pas** — les
  biais d'expressivité par famille (1-N, symétrie, composition), le protocole d'évaluation et
  ses controverses vérifiables (fuite par relations inverses, « old dog new tricks », protocoles
  de rang), les entités inédites et l'échelle.

⚠️ Les pistes du prompt du backlog (Toutanova & Chen, Ruffinelli et al., Sun et al. 2020) ont été
écrites sans balayage web : à corroborer en source primaire au Sweep, jamais des faits.
