# Brief — mechanistic-interpretability

## Sujet (prompt riche, backlog rang-1 haute priorité)

Interprétabilité mécaniste des transformers : ouvrir la boîte noire au niveau des circuits.
Couvrir le cadre features/circuits (le transformer vu comme flux résiduel que têtes et MLP lisent
et écrivent), les têtes d'induction et leur lien à l'in-context learning, la superposition et
l'hypothèse de représentation linéaire des features, les sparse autoencoders (SAE) pour extraire
des features monosémantiques et leurs limites, les techniques d'intervention causale (activation
patching, ablations, logit lens), et les critiques (illusions d'interprétabilité, fidélité des
explications, généralisation des circuits). Public : ingénieur ML / recherche appliquée.

## Cadrage / délimitations

- `transformer-attention` couvre la mécanique de l'attention → s'y appuyer sans la re-dériver.
- `ensemble-learning` effleure la feature importance du ML classique → NE PAS traiter SHAP/LIME
  ni l'explicabilité post-hoc classique.
- Se centrer sur les mécanismes internes des transformers (circuits, features, superposition, SAE,
  interventions causales).

## Domaine

`deep-learning-foundations` (à confirmer par `/arrange`).

## Verdict backlog

Gap réel (haute) — 0 occurrence dans les 41 monographies ; sujet à forte demande de référence.
