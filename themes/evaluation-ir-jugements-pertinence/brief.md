# Brief — Évaluer la recherche d'information : jugements de pertinence et méthodologie de mesure

D'où viennent les jugements de pertinence, et ce que les métriques supposent. L'angle directeur
est la **méthodologie de mesure** : un nDCG@10 n'a de sens que rapporté à la collection de test,
aux qrels et à leur incomplétude, au modèle d'utilisateur de la métrique et à la variance entre
requêtes.

## Cadrage
Document de référence best-of, en français, niveau ingénieur ML / recherche. Il pose le socle que
six thèmes du domaine `information-retrieval-representation` invoquent sans le poser.

## Périmètre à couvrir
- Le paradigme de **Cranfield** et les collections de test : TREC, MS MARCO et ses jugements
  clairsemés, BEIR.
- La construction des **qrels par pooling** et l'incomplétude : bpref, condensed lists, ce que
  « non jugé » veut dire.
- **Accord inter-juges** (Voorhees) et stabilité des classements de systèmes.
- Les **métriques** (précision/rappel, MAP, nDCG, MRR, ERR) lues par leurs hypothèses sur
  l'utilisateur.
- **Tests de significativité** et taille des jeux de requêtes.
- **Évaluation en ligne** (interleaving, clics et leurs biais) en contrepoint.
- Le débat 2024-2026 sur les **LLM comme juges de pertinence** : Thomas et al. (Bing),
  Faggioli et al., UMBRELA / TREC RAG, les objections de Soboroff (« Don't Use LLMs to Make
  Relevance Judgments ») et de Clarke & Dietz (circularité, biais).

## Délimitations strictes
- `learning-to-rank` garde les formules DCG/NDCG/MAP/MRR, leur platitude et le biais de pooling
  LETOR : les citer, ne pas les re-dériver.
- `llm-evaluation` garde les biais génériques des juges LLM.
- `hybrid-search-reranking` garde BEIR comme résultat.

Domaine : `information-retrieval-representation`.
