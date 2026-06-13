# brief — rlhf-dpo

**Sujet**
RLHF et DPO : l'alignement des LLM sur les préférences humaines — modèle de récompense
Bradley-Terry, optimisation par renforcement (PPO) vs optimisation directe des préférences
(DPO), variantes (IPO, KTO, ORPO, RLAIF, GRPO), et compromis stabilité / coût /
over-optimization face au fine-tuning supervisé.

**Cadrage**
- RLHF + DPO au cœur (alignement par préférences) ; les variantes (IPO/KTO/ORPO/RLAIF/GRPO)
  traitées comme état de l'art, pas comme panorama dilué.
- Frontière à surveiller en revue : `self-improving-harness` cite RLHF/PPO/GRPO comme outils
  du self-improvement et `prompt-optimization` les évoque — ne PAS re-dériver le
  self-improvement ni l'optimisation de prompts ; rester sur l'alignement par préférences.
- Trou réel confirmé : RLHF/DPO cités en passant (self-improving-harness, prompt-optimization)
  mais jamais expliqués ; Bradley-Terry et « preference optimization » absents du corpus.
