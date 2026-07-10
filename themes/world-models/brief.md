# Brief — world-models

## Sujet

World models : apprendre un modèle du monde pour prédire, planifier et générer.

## Cadrage

Couvrir :
- la lignée fondatrice (Ha & Schmidhuber 2018 : VAE + RNN + contrôleur, apprendre dans le rêve) ;
- le RL basé modèle (Dreamer v1–v3 et l'imagination latente, MuZero et la planification avec
  modèle appris) ;
- les architectures prédictives auto-supervisées (JEPA/V-JEPA : prédire en espace latent plutôt
  qu'en pixels) ;
- les modèles de monde génératifs interactifs (Genie : la vidéo comme environnement jouable) ;
- le débat pixels vs latents, avec le lien vers les agents incarnés.

Positionnement : direction de recherche majeure 2026, contrepoint au paradigme LLM — Dreamer,
MuZero, JEPA, Genie = 0 occurrence dans le corpus.

Public : ingénieur ML.

## Délimitations

- `diffusion-models` couvre la génération par diffusion (le citer) ;
- le VAE en propre relève du candidat `variational-autoencoders` ;
- le RL sans modèle relève de la monographie `reinforcement-learning-fundamentals` (FAITE — des
  ponts suffisent) ;
- `agentic-ai` couvre les agents incarnés côté LLM ;
- se centrer sur l'apprentissage du modèle de dynamique et son usage pour planifier et générer.

Domaine cible : `deep-learning-foundations`.
