# Brief — calibration-classifieurs

**Sujet.** Calibration des classifieurs probabilistes : faire en sorte que les
probabilités prédites reflètent les fréquences réelles. Couvrir le diagnostic
(reliability diagrams, ECE/MCE, Brier score), les méthodes post-hoc (Platt scaling,
isotonic regression, temperature scaling pour les réseaux profonds), la mauvaise
calibration des réseaux modernes, et la prédiction conforme (conformal prediction)
comme garantie de couverture distribution-free, en pont.

**Public.** Ingénieur ML.

**Cadrage / délimitations.**
- `llm-evaluation` traite l'accord juge/humain au sens psychométrique (kappa, alt-test) —
  hors périmètre ici.
- C-RAG / conformal risk control en contexte RAG — hors périmètre.
- Se centrer sur la **calibration de probabilités de classification** ; la prédiction
  conforme est introduite en pont (garantie de couverture distribution-free), pas comme
  sujet principal.

**Domaine taxonomique.** classical-ml-time-series.
