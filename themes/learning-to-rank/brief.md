# Brief — learning-to-rank

**Sujet** : Learning to rank (LTR) : apprendre à ordonner pour la recherche et la recommandation.

**Cadrage** : couvrir les trois familles de pertes (pointwise ; pairwise — RankNet ; listwise —
ListNet, LambdaRank/LambdaMART), l'optimisation directe des métriques de rang (NDCG, MAP, MRR)
malgré leur non-différentiabilité (le gradient λ de LambdaRank), les features de ranking, les
jeux LETOR/MSLR, et l'usage en reranking.

**Public** : ingénieur ML/IR.

**Délimitations** :
- `hybrid-search-reranking` compare RRF aux LTR et traite les cross-encoders neuronaux ;
- `ensemble-learning` couvre les arbres boostés (socle de LambdaMART) ;
- → se centrer sur les algorithmes LTR et les métriques de rang.

**Domaine taxonomique pressenti** : information-retrieval-representation.
