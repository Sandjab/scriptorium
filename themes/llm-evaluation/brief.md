# brief — llm-evaluation

**Sujet**
L'évaluation des LLM, avec le paradigme **LLM-as-judge** au cœur : comment mesurer la qualité
des sorties d'un modèle de langage quand il n'y a pas de réponse de référence unique. Couvrir
(1) le **paysage de l'évaluation** — benchmarks (MMLU, MT-Bench, Chatbot Arena/Elo), limites des
métriques classiques (BLEU/ROUGE/exact-match) sur la génération ouverte, contamination des jeux
de test ; (2) **LLM-as-judge** comme méthode dominante — *pointwise* vs *pairwise*, G-Eval,
rubriques, panels de juges (PoLL / *jury*), accord juge↔humain ; (3) les **biais et failles du
juge** — biais de position, biais de verbosité, *self-preference* (auto-préférence), sensibilité
au format, non-transitivité — et les **parades** (permutation, calibration, ancrage par rubrique,
multi-juges) ; (4) la **fiabilité statistique** (intervalles de confiance, corrélation de Spearman
avec le jugement humain, reproductibilité).

**Cadrage**
- Cœur = la *méthodologie de mesure* : LLM-as-judge, ses biais documentés et les protocoles qui
  les atténuent ; benchmarks et métriques traités comme le décor qui justifie le recours au juge.
- **Frontière à surveiller en revue** :
  - `rlhf-dpo` couvre le *reward model* Bradley-Terry — un juge de préférences pour
    **l'entraînement/l'alignement**. NE PAS re-dériver RLHF ; ici le juge sert à **évaluer**, pas
    à optimiser des poids (mentionner le lien reward-model↔juge, sans refaire l'alignement).
  - `self-improving-harness` traite Goodhart / *reward hacking* dans des boucles d'auto-amélioration —
    ne pas re-dériver le self-improvement ; le *gaming* du juge est ici un **biais d'évaluation**.
  - `prompt-optimization` / `automatic-prompt-optimization` **utilisent** un signal d'évaluation —
    ne pas re-expliquer l'optimisation de prompts ; le juge est le **fournisseur du signal**.
  - `agentic-ai` cite des benchmarks d'agents (GAIA, SWE-bench, τ-bench) — ce sont des
    **applications** ; rester sur la méthodologie de jugement, pas le palmarès des agents.
- **Trou pressenti** (à confirmer par le Sweep) : aucun thème du corpus ne traite l'évaluation
  comme discipline ; LLM-as-judge, ses biais (position/verbosité/self-preference), Chatbot Arena/Elo,
  G-Eval, MT-Bench, PoLL et l'accord juge↔humain sont absents — alors que le pipeline du scriptorium
  lui-même (council de jurés vérifiant les faits) est une instance de jugement multi-agents.
