# Brief — Normalisation dans les réseaux profonds

**Sujet** : normalisation dans les réseaux profonds (BatchNorm, LayerNorm, RMSNorm).

**Cadrage** : brique fondamentale présupposée par tous les transformers du corpus mais jamais
traitée en propre. Couvrir le problème que résout la normalisation (stabilité/vitesse
d'entraînement, internal covariate shift et son débat), les trois grandes familles —
Batch Normalization (Ioffe & Szegedy 2015), Layer Normalization (Ba, Kiros & Hinton 2016),
RMSNorm (Zhang & Sennrich 2019) — leurs formulations exactes (statistiques calculées, paramètres
appris γ/β, ε), leurs différences (dépendance au batch, comportement train vs inference,
running statistics de BatchNorm), et le placement dans les architectures modernes
(Pre-LN vs Post-LN dans les transformers, pourquoi LayerNorm/RMSNorm dominent les LLM,
adoption de RMSNorm par LLaMA/T5/Gemma). Domaine taxonomique pressenti : `deep-learning-foundations`.
