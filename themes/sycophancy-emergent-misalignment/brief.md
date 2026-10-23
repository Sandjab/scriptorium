# Complaisance et désalignement émergent — brief

**Slug** : `sycophancy-emergent-misalignment` · **Domaine visé** : `llm-agents-generation` · **Public** : ingénieur ML / sûreté.

## Sujet
Comment l'entraînement fabrique le désalignement : complaisance (sycophancy) et désalignement émergent. Ce que l'on mesure, ce que l'on sait de l'origine, et ce que valent les interprétations.

## Piliers à couvrir (à comparer au plan avant l'Extract)
1. Mesure et taxonomie de la sycophancy (Sharma et al., « Towards Understanding Sycophancy in Language Models », ICLR 2024) : feedback sycophancy, answer sycophancy, mimicry ; son origine dans les préférences humaines et le modèle de récompense.
2. Désalignement émergent par fine-tuning étroit (Betley et al., « Emergent Misalignment », ICML 2025 ; publication Nature 2026 à vérifier) : code vulnérable → réponses désalignées hors domaine ; backdoors ; variantes (nombres « maléfiques », conseils médicaux dangereux).
3. Du reward hacking en RL de production au désalignement généralisé (MacDiarmid et al., Anthropic, nov. 2025 : « Natural emergent misalignment from reward hacking ») ; ⚠️ `self-improving-harness` le date « 2024 », à ne pas recopier.
4. Les « persona features » et la direction de désalignement (OpenAI, juin 2025, « Persona Features Control Emergent Misalignment ») ; interprétabilité du phénomène.
5. La sycophancy comme déclencheur ou amplificateur (arXiv 2606.09068 — NON vérifié) ; sycophancy envers les chercheurs (arXiv 2606.08629 — NON vérifié).
6. Critiques méthodologiques : « Overtrained, not misaligned » (mai 2026 : 2 modèles sur 12 réguliers selon les seeds) ; position paper ICML 2026 sur la surinterprétation ; dépendance aux seeds, aux formats, aux juges LLM.
7. Mitigations : inoculation prompting, early stopping, mélange de données bénignes, re-alignement par peu d'exemples.
8. Limites et idées reçues : ce que ces résultats prouvent et ne prouvent pas sur les modèles de production.

## Prudence
- Les identifiants arXiv 26xx marqués « non vérifié » sont des pistes à corroborer au Sweep, jamais des faits.
- Distinguer démonstration en laboratoire (fine-tuning étroit, modèles ouverts) et observation en production.
- Chiffres de taux de désalignement : toujours avec le modèle, le jeu d'évaluation et le juge utilisés.

## Délimitations
- `rlhf-dpo` et `agentic-rl-environments` gardent Goodhart et le Reward Hacking Benchmark (citer).
- `cot-monitoring-scheming-ai-control` garde la détection et le contrôle (scheming, alignment faking, AI control).
- `abliteration-alignment-removal` garde le retrait volontaire de l'alignement par les poids.
- `mechanistic-interpretability` garde la méthode des sondes et des features (citer la feature de sycophancy).
