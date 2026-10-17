# Transformers bouclés et profondeur récurrente — brief

**Slug** : `looped-transformers-recurrent-depth` · **Domaine visé** : `deep-learning-foundations` (ou `llm-agents-generation`, à trancher par /arrange) · **Public** : ingénieur ML.

## Sujet
Transformers bouclés : réappliquer les mêmes blocs pour gagner de la profondeur sans ajouter de paramètres. Ce que le bouclage apporte à l'échelle d'un LLM pré-entraîné, ce qu'il coûte, et ce qui relève de la rumeur.

## Piliers à couvrir (à comparer au plan avant l'Extract)
1. Le principe : poids partagés entre itérations, profondeur effective contre nombre de paramètres ; le coût en FLOPs et en KV cache n'est PAS réduit par le partage de poids.
2. La lignée : Universal Transformers (2018) et ACT — renvoi vers `recursive-language-models`, sans refaire.
3. Recurrent depth et raisonnement latent à l'échelle : Geiping et al. 2025 (Huginn, arXiv 2502.05171).
4. Mixture-of-Recursions : routage du nombre de passes par token (arXiv 2507.10524).
5. Ouro (ByteDance, arXiv 2510.25741) : sorties anticipées, efficacité paramétrique, « boucler aide le raisonnement sans stocker plus de connaissances ».
6. Profondeur logique virtuelle (arXiv 2506.18233). Nanbeige4.2 et lois d'échelle des MoE bouclés (SMELT) : NON vérifiés.
7. Lien supposé avec le raisonnement caché et la monitorabilité (renvoi vers `cot-monitoring-scheming-ai-control`).
8. Limites et idées reçues.

## Prudence
- La rumeur « Astra » (bouclage supposé d'un modèle OpenAI ; The Information, 1er sept. 2026 ; billet de Raschka du 9 sept.) n'est PAS confirmée par OpenAI : la présenter comme rumeur, jamais comme fait.
- Distinguer résultat publié et extrapolation ; ne pas confondre efficacité en paramètres et efficacité en calcul.

## Délimitations
- `recursive-language-models` garde UT, ACT, HRM/TRM, Coconut (citer sans refaire).
- `reasoning-test-time-compute` garde le scaling par tokens de pensée.
- `mixture-of-experts` garde le routage par experts.
- `cot-monitoring-scheming-ai-control` garde la monitorabilité.
