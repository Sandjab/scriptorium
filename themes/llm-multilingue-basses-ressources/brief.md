# LLM multilingues et langues peu dotées — brief

**Slug** : `llm-multilingue-basses-ressources` · **Domaine visé** : `deep-learning-foundations` ou `llm-agents-generation` (à trancher par /arrange) · **Public** : ingénieur ML.

## Sujet
Les modèles de langage hors anglais : ce que coûte une langue (en tokens, en capacité, en qualité), et ce qu'un modèle lui transfère depuis les langues riches en données.

## Piliers à couvrir (à comparer au plan avant l'Extract)
1. La prime de tokenisation mesurée par langue (Petrov et al., NeurIPS 2023) : plusieurs fois plus de tokens pour une même phrase, conséquences en coût d'API, en contexte utile et en qualité.
2. Le transfert inter-langues et la « curse of multilinguality » (Conneau et al., XLM-R, ACL 2020) : capacité partagée, interférence entre langues, ce que montrent mBERT et XLM-R.
3. Le mélange de langues au pré-entraînement : échantillonnage par température (exposant α), part non anglaise des corpus des modèles récents.
4. L'évaluation multilingue : benchmarks traduits et leurs biais culturels (Global MMLU), MGSM, écart entre langues d'un même modèle.
5. Les langues peu dotées : FLORES-200 et NLLB (« No Language Left Behind »), données synthétiques par traduction, modèles régionaux et communautaires (Aya…).
6. Limites et idées reçues ; écosystème.

## Prudence
- Les écarts entre langues sont souvent mesurés par l'équipe qui publie le modèle, sur son propre benchmark : indépendance par TRAVAIL, pas par URL.
- Un benchmark traduit ne mesure pas la même chose que l'original : ne jamais comparer deux scores sans dire si le jeu est traduit (et par qui : humain, machine) ou natif.
- La prime de tokenisation dépend du tokeniseur : toujours nommer le tokeniseur derrière un ratio.

## Délimitations (vérifiées par LECTURE le 2026-10-30)
- `text-embeddings` garde la mécanique des tokeniseurs (BPE, WordPiece, Unigram, SentencePiece, optimalité du glouton) ; il ne cite le surcoût des langues non anglaises qu'en une proposition, sans chiffre : citer sans re-dériver.
- `pretraining-data-curation` garde l'identification de langue (lid.176, seuils de C4/CCNet/FineWeb) et le biais dialectal du filtre de C4 ; il note que CCNet a fourni les données de XLM-R.
- `llm-safety-jailbreaks` garde le jailbreak par langues peu dotées (79 % sur AdvBench) : renvoi.
- `quantization` garde la dégradation plus forte hors anglais : renvoi.
- `speech-recognition-asr` garde le multilingue de la PAROLE (Whisper 96 langues, FLEURS, normaliseur et écritures indiques, wav2vec 2.0 à faibles ressources) : le présent thème porte sur le TEXTE.
- `mixture-of-experts` cite GShard comme transformer multilingue ; `model-routing-cascades` note l'absence de langues peu dotées dans les benchmarks de routage.
- Le candidat `recherche-multilingue-cross-lingual` tient le versant recherche d'information (non traité ici).
