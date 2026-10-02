# Brief — generalisation-double-descent-grokking

Pourquoi les réseaux surparamétrés généralisent : les phénomènes et ce qu'on en comprend. Couvrir :
l'énigme fondatrice (Zhang et al. 2017 : mémoriser des labels aléatoires sans perdre la capacité de
généraliser) ; la double descente (Belkin et al. 2019, Nakkiran et al. : double descente en taille de
modèle, en époques, en données — et le rôle du bruit de label) ; le grokking (Power et al. 2022 :
généralisation longtemps après l'ajustement, et ses explications par la norme des poids et les
circuits) ; l'hypothèse du ticket de loterie (Frankle & Carbin) comme phénomène de généralisation ;
les minima plats et SAM ; le biais implicite de SGD et la régularisation implicite ; le benign
overfitting en régression linéaire ; et ce que ces résultats disent — et ne disent pas — de la
pratique (early stopping, taille de modèle, régularisation).

Positionnement : le corpus a les briques éparses sans le fil (gap jugé « le plus net du domaine »
au backlog du 2026-09-01). Public : ingénieur ML.

## Délimitations

Vérifiées par LECTURE de la prose le 2026-10-02 :

- **`ensemble-learning`** garde le biais-variance classique, la convergence des forêts (Breiman,
  Th. 1.2) et l'énigme d'AdaBoost résolue par les marges (Schapire et al. 1998 : l'erreur de test
  baisse encore après une erreur d'entraînement nulle, contre la prédiction de la théorie VC).
  Le citer comme PRÉCÉDENT de l'énigme d'interpolation, ne pas refaire.
- **`optimizers-adam`** garde le débat adaptatif contre SGD sur la généralisation (Wilson et al.
  2017, la réponse d'AdamW, AlgoPerf). Y RENVOYER ; ici, le biais implicite de SGD comme mécanisme
  de généralisation, pas la comparaison d'optimiseurs.

Reprises de l'audit du backlog (2026-09-01), non relues ce jour :

- **`scaling-laws`** garde les lois de puissance et l'émergence (la double descente n'y est qu'une
  incise, comme forme que BNSL sait représenter).
- **`mechanistic-interpretability`** garde les circuits : le citer pour l'explication du grokking.
- **`lora`** tient le NTK en propriété théorique : citer, ne pas re-dériver.
- **`quantization`** (minima plats au service du QAT) et **`normalization-layers`** (SAM entre
  parenthèses) : simples mentions.
- Le ticket de loterie est ICI comme phénomène ; le candidat `pruning-sparsity` le tiendra comme
  méthode.
