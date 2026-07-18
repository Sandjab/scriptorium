# Brief — variational-autoencoders

## Sujet

Autoencodeurs et VAE : apprendre des représentations latentes et générer par inférence
variationnelle. Couvrir l'autoencodeur (encodeur/décodeur, goulot, reconstruction), le débruitage
(denoising autoencoder), puis le Variational Autoencoder (Kingma & Welling 2013 : borne ELBO,
reconstruction + KL au prior, reparameterization trick), les variantes (β-VAE et le
désenchevêtrement, VQ-VAE et le codebook discret), et le lien avec les modèles latents génératifs.

## Positionnement

Brique fondamentale qui sous-tend la diffusion latente. Public : ingénieur ML.

## Délimitations

- `diffusion-models` s'appuie sur un autoencodeur (régularisation KL/VQ) sans traiter le VAE en
  tant que tel — ne le citer que comme usage aval.
- `clustering-dimensionality-reduction` couvre PCA/UMAP — se centrer ici sur le cadre génératif
  probabiliste et l'inférence variationnelle.

## Domaine cible (arrange)

`deep-learning-foundations`
