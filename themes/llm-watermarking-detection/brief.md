# Tatouage et détection du texte généré par LLM

Candidat du backlog (`docs/candidate-themes.md`, priorité moyenne, ajouté le 2026-07-17),
lancé le 2026-08-31 en 49e run `/leanmonograph`. Domaine visé : `llm-agents-generation`.

⚠️ Ce fichier est une TRACE : `workflow.js` ne le lit pas. Le cadrage effectif passe
entièrement par `args.subject` (vérifié : aucune lecture de `brief.md` dans le workflow).

## Gap re-vérifié par lecture avant lancement (2026-08-31)

Corpus à 88 thèmes / 90 documents. `watermark`, `tatouag`, `Kirchenbauer`, `DetectGPT`,
`SynthID`, `C2PA`, `liste verte` : **0 occurrence** dans les `manifest.json` et
`knowledge.json` publiés. Le gap du backlog tient — il a même grandi (le verdict datait
d'un corpus à 45 thèmes).

La lecture des voisins a sorti un piège absent du backlog : **trois résultats
d'impossibilité distincts vivent déjà dans le corpus**, et rien ne les distingue au grep.

1. `llm-safety-jailbreaks` § « Garanties et impossibilités » — BEB (Wolf et al.) borne
   l'ALIGNEMENT à poids figés ; le Defense Trilemma (Bhatt et al., avril 2026, préprint,
   déjà hedgé « source unique » dans ce document) borne les défenses enveloppantes.
2. `hallucination-detection-uncertainty` — Karbasi et al. (ICML 2025) sur l'impossibilité
   de la détection automatisée d'HALLUCINATION.
3. Celui qui appartient à ce thème — la borne de DÉTECTABILITÉ du texte machine
   (Sadasivan et al., AUROC borné par la distance en variation totale). À vérifier au
   sweep comme tout le reste, pas à affirmer sur la foi de ce brief.

Fondre ces trois-là produirait la redite la plus coûteuse que ce thème puisse commettre.

## Autres délimitations vérifiées

- `decoding-sampling` : logits, temperature/top-k/top-p, min-p, pénalités, décodage
  spéculatif. Le watermarking par biais de logits **est** une modification du sampling —
  partir de là, ne pas re-dériver.
- `hallucination-detection-uncertainty` : détecte le FAUX, pas la MACHINE. Homonymie de
  « détection » à écarter dès la première section (précédent : `streaming-quantiles-sampling`
  écarte ses deux homonymies en ouverture).
- `pretraining-data-curation` : données synthétiques comme matière volontaire,
  décontamination par n-grammes contre les jeux de test. Le filtrage du texte machine dans
  un crawl est un pont applicatif, pas le centre.
