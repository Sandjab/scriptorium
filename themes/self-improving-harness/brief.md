# Self-Harness: Harnesses That Improve Themselves

Sujet tel que fourni : **Self-Harness — Harnesses That Improve Themselves**.

Cadrage : panorama vérifié des **harness agentiques qui s'améliorent eux-mêmes** — c.-à-d.
le scaffold/framework autour d'un LLM (prompts, outils, boucle de contrôle, mémoire, workflow
multi-agents) qui se ré-écrit ou s'auto-optimise au lieu d'être figé à la main. Distinguer
clairement les niveaux de « self-improvement » (optimisation de prompts/programmes vs réécriture
du code du harness vs amélioration des poids du modèle) et ce qui est empiriquement démontré vs
spéculatif.

Axes à couvrir (le Plan tranche le périmètre final, plafonds frugaux MAX_SECTIONS=9) :
- Définitions & taxonomie : qu'est-ce qu'un « harness » ; échelle de Schmidhuber (self-referential)
  → réécriture de code (Gödel Agent / Darwin Gödel Machine) → recherche méta-agentique (ADAS) →
  optimisation de programmes/prompts (STOP, DSPy, automatic prompt optimization).
- Mécanismes concrets : boucle propose→évalue→sélectionne, mémoire/skill library (Voyager),
  self-rewarding / self-critique, méta-agent qui code de nouveaux agents.
- Garanties & limites : preuve d'amélioration (Gödel machine theorique), reward hacking,
  effondrement/dérive, coût, sécurité (objective robustness, oversight).
- État empirique 2023-2025 : ce qui est mesuré sur benchmarks (SWE-bench, etc.) vs claims.

Garde-fous : tout `confirmed` ≥ 2 sources indépendantes ; séparer rigoureusement résultat
empirique publié, cadre théorique, et projection. Frontière jugement/code respectée.
