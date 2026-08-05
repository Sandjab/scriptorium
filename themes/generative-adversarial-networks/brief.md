# Brief — generative-adversarial-networks

Réseaux antagonistes génératifs (GAN) : générer par un jeu à deux joueurs. Couvrir la
formulation min-max (générateur vs discriminateur, l'objectif de Goodfellow 2014 et son
interprétation en divergence de Jensen-Shannon), les pathologies d'entraînement
(instabilité, mode collapse, vanishing gradients) et leurs remèdes (Wasserstein GAN,
gradient penalty WGAN-GP, spectral normalization), les architectures marquantes (DCGAN,
conditional GAN, StyleGAN, CycleGAN), et l'évaluation (FID, Inception Score).
Positionnement : paradigme génératif historique majeur, contrepoint de la diffusion.
Public : ingénieur ML.

Délimitations (re-vérifiées par lecture le 2026-08-04) :
- `diffusion-models` couvre le génératif par score/diffusion et emploie déjà FID/IS —
  se centrer sur l'entraînement adversarial et ses pathologies.
- `variational-autoencoders` (publié depuis le classement du candidat) traite VQGAN et
  l'entraînement adversarial d'autoencodeurs (discriminateur par patch, perte perceptuelle),
  et cite InfoGAN comme baseline de disentanglement : les CITER sans re-dériver.
- Le mode collapse est NOMMÉ dans variational-autoencoders sans y être expliqué :
  son explication mécanistique appartient à CE document.

Domaine pressenti : deep-learning-foundations (source de vérité : tools/taxonomy.json via /arrange).
