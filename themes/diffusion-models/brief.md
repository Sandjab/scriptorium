# Brief — diffusion-models

## Sujet (tel que fourni)

Les modèles de diffusion génératifs — du bruit à l'échantillon. Panorama grand angle à hauteur
de lecteur informé non-expert : processus forward/reverse et intuition du débruitage ; un chapitre
référence théorique qui creuse le « pourquoi ça marche » — DDPM, score matching, borne
variationnelle, et l'unification DDPM ↔ modèles à score ↔ probability-flow ODE (Song et al.) ;
échantillonnage & accélération (DDIM, solveurs d'EDO type DPM-Solver, distillation / consistency
models) ; guidage (classifier-free guidance) ; latent diffusion (Stable Diffusion) ; applications
au-delà de l'image (audio, vidéo, molécules) ; et le pont vers le flow matching. Une section
approfondit la théorie ; les autres restent panoramiques.

## Cadrage

- **Forme** : panorama grand angle borné (≤ 9 sections), une **seule** section « fondations
  théoriques » descend en profondeur (DDPM ↔ score ↔ probability-flow ODE, Song et al.) ; les
  autres balaient le paysage sans surcharger.
- **Lecteur cible** : informé mais non-expert (connaît les bases du ML/génératif, pas forcément
  les EDS ni le score matching).
- **Axes attendus** : intuition forward/reverse · fondations théoriques (deep) · échantillonnage
  & accélération (DDIM, DPM-Solver, distillation, consistency models) · guidage (classifier-free)
  · latent diffusion (Stable Diffusion) · applications hors image (audio, vidéo, molécules) ·
  pont vers le flow matching.
