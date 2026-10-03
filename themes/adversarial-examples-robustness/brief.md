# Brief — Exemples adverses et robustesse des réseaux

L'angle directeur : **une perturbation que l'œil ne voit pas et qui change la sortie** — ce
qu'elle révèle des réseaux, comment on l'attaque, comment on s'en défend, et comment on
mesure honnêtement une défense. Le fil rouge : une robustesse se prouve contre l'attaque la
plus forte qui connaît la défense, jamais contre l'attaque d'hier.

## Cadrage
Document de référence best-of, en français, public ingénieur ML / sécurité. Audit de
couverture par lecture (2026-10-03) : `convolutional-networks` referme son § « pièges » sur un
paragraphe (Szegedy 2013, transfert, FGSM de Goodfellow) ; PGD, C&W, attaques physiques,
entraînement adverse et son coût, défenses certifiées, gradients obfusqués, ImageNet-C et le
débat « features non robustes » sont absents du corpus.

## Périmètre à couvrir
1. **Le phénomène** : Szegedy et al. (2013), l'explication linéaire de Goodfellow et al.
   (2014), la transférabilité entre modèles.
2. **Attaques en boîte blanche** : FGSM, PGD (Madry et al.), Carlini-Wagner ; normes L∞/L2/L0
   et budget ε.
3. **Attaques en boîte noire** : par transfert (modèle substitut), par requêtes (estimation de
   gradient, attaques par décision).
4. **Attaques physiques** : patchs adverses, lunettes, panneaux routiers.
5. **Entraînement adverse** et son coût : exactitude propre sacrifiée, compromis
   exactitude/robustesse (TRADES), robust overfitting.
6. **Course aux défenses cassées** : gradients obfusqués (Athalye, Carlini, Wagner 2018),
   évaluation adaptative, AutoAttack et RobustBench comme protocole.
7. **Défenses certifiées** : randomized smoothing (Cohen et al.), bornes par relaxation
   (IBP, CROWN) — ce qu'elles garantissent et à quel rayon.
8. **Corruptions naturelles** comme problème distinct : ImageNet-C, décalage de distribution.
9. **Le débat « features non robustes »** (Ilyas et al. 2019) et ses réponses.
10. **Limites**.

## Délimitations strictes
- `llm-safety-jailbreaks` : texte discret (GCG, transfert côté texte, attaques adaptatives
  contre les défenses de LLM) — le citer pour marquer la frontière continu/discret.
- `quantization` : vérification formelle des QNN — citer.
- `mechanistic-interpretability` : superposition et vulnérabilité adverse (modèle jouet),
  SAE manipulables — citer, ne pas refaire.
- `convolutional-networks` : paragraphe historique Szegedy/FGSM — partir de là.
- `generative-adversarial-networks` : « adverse » au sens de l'entraînement GAN, sans rapport —
  lever l'homonymie en une phrase si utile.
