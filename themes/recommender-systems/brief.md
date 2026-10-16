# Brief — recommender-systems

Systèmes de recommandation et filtrage collaboratif : prédire les préférences à grande échelle.
Couvrir, comme piliers distincts : (1) le filtrage collaboratif par voisinage (user-based, item-based,
similarités) ; (2) la factorisation matricielle (SVD-like du Netflix Prize, termes de biais, ALS,
régularisation) ; (3) le feedback implicite (Hu, Koren & Volinsky : confiance vs préférence) et le
ranking par paires (BPR, échantillonnage de négatifs) ; (4) les modèles neuronaux et séquentiels
(NCF et sa remise en cause par Rendle et al. 2020, SASRec/BERT4Rec) ; (5) l'architecture industrielle
en deux étages : retrieval par two-tower (biais d'échantillonnage in-batch, correction logQ) puis
ranking (YouTube DNN, Wide & Deep, DLRM) ; (6) le démarrage à froid (contenu, side information) ;
(7) l'évaluation top-N (Recall@K, hit rate, MAP) et ses pièges hors-ligne : métriques échantillonnées
(Krichene & Rendle), fuites temporelles, baselines mal réglées et crise de reproductibilité
(Ferrari Dacrema et al. 2019), écart hors-ligne / en ligne ; (8) biais et boucles de rétroaction
(biais de popularité, de position, d'exposition ; débiaisement par IPS).

Positionnement : grand domaine applicatif absent du corpus. Public : ingénieur ML.

## Délimitations (vérifiées par LECTURE de la prose des voisins le 2026-10-16)

- **`approximate-nearest-neighbor`** traite HNSW, ScaNN/MIPS comme primitive de la recommandation,
  NSG chez Taobao. Ici le retrieval two-tower ne fait que renvoyer à l'ANN pour l'index.
- **`text-embeddings`** cite Annoy/Voyager chez Spotify (vecteurs de factorisation matricielle) et
  Levy & Goldberg (SGNS = factorisation implicite de PMI). Citer, ne pas refaire.
- **`variational-autoencoders`** a un paragraphe sur Mult-VAE (Liang et al., WWW 2018) ; ici une
  famille parmi d'autres, renvoyer pour le mécanisme VAE.
- **`graph-neural-networks`** traite PinSage (3 Md de nœuds) ; ici citer comme recommandation par
  graphe, ne pas refaire (LightGCN éventuellement).
- **`knowledge-graph-embeddings-link-prediction`** cite le graphe d'items Taobao (lignée DeepWalk).
- **`learning-to-rank`** et **`evaluation-ir-jugements-pertinence`** définissent NDCG et
  l'ordonnancement supervisé générique (RankNet, LambdaRank) : ne pas redéfinir le NDCG ; ici, ce que
  l'évaluation top-N de la recommandation a de propre (feedback implicite, métriques échantillonnées).
- **`multi-armed-bandits`** (candidat non fait) : exploration/exploitation hors périmètre, une
  mention suffit.
