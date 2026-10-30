# Diagnostic des défauts de la vidéo générée — brief

**Slug** : `generated-video-artifact-detection` · **Domaine visé** : `deep-learning-foundations` ou `llm-agents-generation` (à trancher par /arrange) · **Public** : ingénieur ML.

## Sujet
Diagnostiquer une vidéo générée par IA : détecter, localiser et expliquer ses défauts (difformités, mouvements irréalistes, violations physiques) — et ce que valent les modèles qui s'en chargent.

## Piliers à couvrir (à comparer au plan avant l'Extract)
1. Typologie des défauts : anatomie et difformités, permanence et identité des objets, violations physiques et mouvements irréalistes, scintillement temporel, texte.
2. Du score global (FVD) aux axes décomposés (VBench) : ce que chaque axe mesure réellement.
3. Les bancs de plausibilité physique (pistes à confirmer : VideoPhy, PhyGenBench, Physics-IQ).
4. Le VLM comme juge de vidéo : juge-t-il le mouvement ou des images isolées ? Accord avec les annotateurs humains.
5. La localisation spatio-temporelle des artefacts (où et quand le défaut apparaît).
6. Ces juges comme récompense pour post-entraîner le générateur (modèles de récompense vidéo, préférences) et l'effet Goodhart.
7. Limites et idées reçues ; écosystème.

## Prudence
- Littérature jeune, dominée par les préprints : un banc est souvent mesuré par l'équipe qui le publie, sur ses propres modèles — indépendance par TRAVAIL, pas par URL.
- Les classements de générateurs vieillissent en quelques mois : toujours dater un score et nommer la version du modèle évalué.
- Un accord juge↔humain n'a de sens qu'avec son protocole (qui annote, combien, quelle métrique d'accord).

## Délimitations (vérifiées par LECTURE le 2026-10-30)
- `world-models` garde la question « le générateur apprend-il la physique ? » (Kang et al., ICML 2025, généralisation « case-based ») et Sora/Genie 3 comme simulateurs : en partir — ici, la question est de savoir si un modèle VOIT la violation.
- `diffusion-models` garde l'architecture de la diffusion vidéo (factorisation espace-temps, Imagen Video, DiT de Sora) : ne pas re-dériver.
- `multimodal-vlm` garde l'architecture des VLM et l'hallucination visuelle sur image ; `llm-evaluation` garde les biais du juge en général (verbosité, auto-préférence) : citer, rester sur ce que la vidéo ajoute.
- Candidat `video-generation-models` : la fabrication de la vidéo (lui a cédé son volet évaluation).
- Candidat `media-provenance-c2pa` : la détection synthétique/réel et la provenance — citer le recouvrement des signaux, ne pas le refaire.
