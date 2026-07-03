# Brief — convolutional-networks

**Sujet** : Réseaux de neurones convolutifs (CNN), de LeNet à ConvNeXt : l'architecture qui
domine encore la vision.

**Cadrage** (issu de `docs/candidate-themes.md`, priorité haute, gap réel) :

Couvrir la mécanique convolutive (convolution discrète, partage de poids, champ réceptif,
stride, padding, dilatation), le pooling et l'invariance par translation, la généalogie des
architectures (LeNet → AlexNet → VGG → Inception → ResNet/connexions résiduelles → DenseNet →
EfficientNet/compound scaling → ConvNeXt), les convolutions séparables en profondeur (MobileNet)
et la comparaison avec les Vision Transformers.

**Public** : ingénieur ML.

**Délimitations** :
- `backpropagation` effleure LeNet (partage de poids) — le citer sans re-dériver.
- `normalization-layers` cite ResNet/ConvNeXt comme cas d'usage de BN/LN — s'y référer.
- `transformer-attention` couvre les ViT — la comparaison CNN vs ViT se fait d'ici, sans
  re-dériver l'attention.
- Se centrer sur la mécanique convolutive et l'évolution des architectures.

**Domaine** (taxonomy) : deep-learning-foundations.

**Pipeline** : /leanmonograph (vérifier d'abord, écrire une fois).
