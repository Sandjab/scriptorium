# Brief — optimizers-adam

Optimiseurs pour l'entraînement de réseaux profonds, centrés sur Adam et AdamW : que faire du
gradient une fois calculé. Couvrir : SGD et momentum (Polyak, Nesterov) comme point de départ ; la
lignée des méthodes adaptatives AdaGrad → RMSProp → Adam (moments d'ordre 1 et 2, correction de
biais) ; le défaut de convergence d'Adam et AMSGrad (Reddi et al.) ; AdamW (weight decay découplé
vs régularisation L2, Loshchilov & Hutter) et pourquoi la différence n'existe qu'avec un optimiseur
adaptatif ; les schedules de learning rate (warmup, cosine, warmup-stable-decay) et le rôle de
ε et des β ; le débat adaptatif vs SGD sur la généralisation (Wilson et al. 2017) ; les variantes
modernes — Adafactor (mémoire factorisée), LAMB/LARS (grands batchs), Lion (recherche
symbolique), Sophia (second ordre diagonal), Shampoo/SOAP et Muon (orthogonalisation) — confrontées
aux comparaisons contrôlées qui en mesurent le gain réel (benchmarks d'optimiseurs, AlgoPerf).

Positionnement : AdamW est l'optimiseur par défaut de quasiment tout LLM, et le corpus n'en
explique ni le découplage du weight decay ni le paysage des successeurs. Public : ingénieur ML.

## Délimitations (vérifiées par LECTURE de la prose des voisins le 2026-09-25)

- **`backpropagation`** pose en un paragraphe Adam de base (Kingma & Ba 2014, momentum + RMSProp,
  β₁ = 0,9, β₂ = 0,999, ε = 10⁻⁸) et les conditions de Robbins-Monro sur le pas ; il sépare
  nettement calcul du gradient et mise à jour. Partir de là : ne pas re-dériver le gradient ni
  refaire Robbins-Monro, y renvoyer.
- **`distributed-training-parallelism`** chiffre la mémoire des états d'Adam (16Ψ octets en
  précision mixte, 12Ψ d'états fp32, partitionnement ZeRO). Y RENVOYER ; ici, seulement ce que ce
  coût mémoire motive (Adafactor, optimiseurs 8 bits, états réduits de Lion/Muon).
- **`normalization-layers`** explique pourquoi le warmup est structurellement nécessaire en
  Post-LN et facultatif en Pre-LN (Xiong et al. 2020). Y renvoyer ; ici, le warmup du point de
  vue de l'optimiseur (variance des moments en début d'entraînement, RAdam).
- **`scaling-laws`** mentionne la durée du warmup et la décroissance cosinus comme causes de
  l'écart Kaplan/Chinchilla (Porian et al. 2024). Citer, ne pas refaire.
