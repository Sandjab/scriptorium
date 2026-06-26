# Brief — reasoning-test-time-compute

**Sujet.** Raisonnement à l'inférence et test-time compute : améliorer la qualité d'un LLM en
dépensant plus de calcul au moment de répondre, plutôt qu'en grossissant le modèle. Couvrir le
chain-of-thought (CoT) comme méthode et ses variantes structurées (self-consistency, tree-of-thought,
graph-of-thought), l'échantillonnage best-of-N et les vérificateurs / Process Reward Models (PRM),
les lois d'échelle du test-time compute (qualité vs budget d'inférence), et le décodage des modèles
de raisonnement (o1/o3, traces longues).

**Positionnement.** Le versant INFÉRENCE du raisonnement. Public : ingénieur ML.
Domaine taxonomique : `llm-agents-generation`.

**Délimitations strictes.**
- NE PAS re-traiter le RL-pour-raisonnement — déjà dans `rlhf-dpo` (section « GRPO et le RL pour le
  raisonnement »). Le citer comme voisin (versant ENTRAÎNEMENT), pas le re-dériver.
- NE PAS re-traiter la récursion long-horizon — déjà dans `recursive-language-models`.
