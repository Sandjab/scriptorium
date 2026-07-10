# Brief — reinforcement-learning-fundamentals

## Sujet

Apprentissage par renforcement (reinforcement learning) : les fondamentaux, du MDP à PPO.

## Cadrage

Couvrir :
- le cadre (processus de décision markovien, récompense et retour, politique, fonctions de
  valeur, équations de Bellman) ;
- les méthodes par valeur (TD-learning, Q-learning, DQN et ses stabilisateurs — replay buffer,
  target network) ;
- les méthodes par politique (REINFORCE, baseline et réduction de variance, acteur-critique,
  avantage et GAE) ;
- les régions de confiance (TRPO → PPO et son clipping) ;
- le dilemme exploration/exploitation (on-policy vs off-policy).

Public : ingénieur ML.

## Délimitations

- `rlhf-dpo` couvre PPO appliqué au RLHF (reward model, pénalité KL, DPO) — le citer comme
  débouché ;
- `reasoning-test-time-compute` couvre le RL du raisonnement (GRPO, PAV) — le citer comme
  débouché ;
- `agentic-rl-environments` (FAIT) couvre le RL agentique et les récompenses vérifiables — ce
  thème pose le socle MDP/Bellman qu'il présuppose, le citer comme débouché ;
- les bandits sans état relèvent du candidat `multi-armed-bandits` (un pont suffit).

Ce thème pose le socle que les débouchés présupposent.

Domaine cible : `deep-learning-foundations`.
