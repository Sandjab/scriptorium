# Brief — Modèles de langage à diffusion

**Slug** : `diffusion-language-models` · **Domaine cible** : `llm-agents-generation`

## Sujet

Modèles de langage à diffusion (diffusion discrète/masquée) : générer du texte sans factorisation
autorégressive. Couvrir la diffusion sur espaces discrets (D3PM, état absorbant), le score
entropy (SEDD), la diffusion masquée simplifiée et son passage à l'échelle (LLaDA), les modèles
déployés (Mercury d'Inception Labs, Gemini Diffusion), le compromis parallélisme/qualité (nombre
d'étapes vs tokens par étape, ordre de génération, remasking), le lien avec l'infilling et
l'édition, et les pièges d'évaluation (vraisemblance vs qualité perçue, vitesse réelle).

**Public** : ingénieur ML.

## Délimitations

- `diffusion-models` couvre le cadre continu, l'ELBO et le flow matching — le citer, ne pas
  re-dériver.
- `decoding-sampling` couvre le décodage autorégressif et cite la génération parallèle masquée —
  le citer en pont.
- Se centrer sur le paradigme diffusion pour le texte.

## Vérification du gap (2026-07-30)

Greps ciblés (D3PM, LLaDA, SEDD, Mercury, Gemini Diffusion, diffusion masquée/discrète, masked
diffusion) sur les `knowledge.json`/`manifest.json` du corpus (62 thèmes) : une seule occurrence,
clause d'exclusion dans `themes/diffusion-models/knowledge.json`. Gap réel confirmé.
