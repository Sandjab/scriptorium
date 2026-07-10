# Brief — agentic-rl-environments

## Sujet

Reinforcement learning agentique et environnements vérifiables : entraîner des agents LLM par
récompenses vérifiables à l'échelle.

## Cadrage

Couvrir :
- le passage RLHF → RLVR (récompense binaire vérifiable vs reward model appris, et pourquoi cela
  change l'échelle) ;
- la conception d'environnements (gyms d'agents, tâches code/terminal/navigateur, génération de
  tâches synthétiques et leur vérification, l'exemple des computer-use agents) ;
- le RL multi-tours (attribution de crédit sur horizons longs, récompenses de processus vs de
  résultat) ;
- le reward hacking en environnement et ses défenses ;
- l'infrastructure (rollouts asynchrones, sandboxes à l'échelle).

Positionnement : paradigme post-training dominant 2026. Public : ingénieur ML.

## Délimitations

- `rlhf-dpo` couvre PPO/DPO et pose RLVR (le citer) ;
- `reasoning-test-time-compute` couvre le RL du raisonnement — GRPO, PAV (le citer) ;
- le socle MDP/Bellman relève du candidat `reinforcement-learning-fundamentals` (un pont suffit) ;
- se centrer sur les environnements et l'entraînement d'agents multi-tours.

Domaine cible : `llm-agents-generation`.
