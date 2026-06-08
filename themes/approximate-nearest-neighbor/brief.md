# Recherche approchée de plus proches voisins (ANN)

**Sujet (tel que fourni)** : Approximate Nearest Neighbor search (HNSW, IVF, PQ, etc).

## Cadrage

Panorama vérifié de la **recherche approchée de plus proches voisins** (Approximate Nearest
Neighbor search, ANN) : le problème de retrouver, dans un grand ensemble de vecteurs de haute
dimension, les points les plus proches d'une requête — non plus exactement (k-NN exact, coûteux
en haute dimension à cause de la *curse of dimensionality*) mais de façon **approchée**, en
échangeant un peu de *recall* contre des gains massifs de latence et de mémoire. Couvrir :
la formulation du problème et le compromis recall / latence / mémoire ; les grandes familles
d'index — **graphes de navigation** (HNSW, et l'antécédent NSW/small-world), **partitionnement
par cellules** (IVF, *inverted file* avec listes inversées et `nprobe`), **hachage** (LSH) ;
la **compression de vecteurs** par quantification — **Product Quantization (PQ)**, ses variantes
(OPQ, SQ scalaire) et la *asymmetric distance computation* ; les index **composites** typiques
(IVF+PQ, HNSW+PQ) ; les métriques d'évaluation (recall@k, QPS) et leurs compromis ; et l'ancrage
dans les bibliothèques/moteurs réels (FAISS, hnswlib, ScaNN, et les vector databases).

Public : ingénieur·e logiciel curieux de la recherche vectorielle (RAG, recommandation,
recherche sémantique), sans prérequis pointu en géométrie algorithmique. Document de référence
unique, best-of, vérifié (≥ 2 sources indépendantes par fait `confirmed`).
