# Surveillance de la chaîne de pensée, scheming et AI control — brief

**Slug** : `cot-monitoring-scheming-ai-control` · **Domaine visé** : `llm-agents-generation` (à trancher par /arrange) · **Public** : ingénieur ML / sûreté.

## Sujet
Surveiller un modèle peut-être adverse : chaîne de pensée, scheming et contrôle. Comment observer et contenir un modèle qui pourrait poursuivre un but caché, et ce que valent les dispositifs actuels.

## Piliers à couvrir (à comparer au plan avant l'Extract)
1. La surveillance du CoT comme dispositif de sûreté : position paper multi-labos (Korbak et al., juil. 2025), notion de monitorabilité, suite « Monitoring Monitorability » d'OpenAI (déc. 2025, métrique g-mean²). MonitorBench (arXiv 2603.28590) : NON vérifié.
2. Fragilité : la pression d'optimisation sur le CoT (pénaliser les « mauvaises pensées ») rend le raisonnement illisible ou dissimulé (obfuscated reward hacking).
3. Scheming en contexte (Apollo Research, 2024) et alignment faking (Greenblatt et al., Anthropic/Redwood, 2024).
4. Sandbagging (van der Weij et al., ICLR 2025 ; modèles verrouillés par mot de passe) et conscience de l'évaluation qui brouille les mesures.
5. Protocoles d'AI control (Greenblatt et al., ICML 2024) : trusted/untrusted monitoring, resampling, editing, évaluations de sabotage ; moniteurs fondés sur les seules actions (arXiv 2605.29601).
6. Passage en production : moniteurs de CoT sur le trafic interne d'agents de code, évaluations de sabotage dans des system cards (ControlConf 2026).
7. Limites et idées reçues : ce que ces évaluations prouvent et ne prouvent pas.

## Prudence
- Toute actualité non sourcée par ≥ 2 sources indépendantes (ex. bouclage supposé d'« Astra » et baisse de monitorabilité de sa system card) est une RUMEUR : ne pas l'affirmer.
- Distinguer démonstration en contexte (scénario construit) et propension spontanée.

## Délimitations
- `reasoning-test-time-compute` garde la FIDÉLITÉ du CoT (citer Arcuschin 2025 sans refaire).
- `mechanistic-interpretability` garde les sondes et circuits.
- `llm-safety-jailbreaks` garde attaque/défense ; `agent-tool-security` (candidat) garde l'injection.
- `sycophancy-emergent-misalignment` (candidat) garde la GENÈSE du désalignement — ici, l'observer et le contenir.
- `abliteration-alignment-removal` garde le retrait de l'alignement par les poids.
