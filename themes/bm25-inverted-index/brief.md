# BM25 et index inversé

**Sujet (tel que fourni)** : BM25 et index inversé.

**Cadrage** : monographie sur le cœur de la recherche lexicale (sparse retrieval) — la
structure de données *index inversé* (postings lists, dictionnaire de termes, construction
et compression) et la fonction de score *BM25* (term frequency saturée, IDF, normalisation
par longueur de document via les paramètres k1 et b), héritière du modèle probabiliste
Okapi. Couvrir : du TF-IDF à BM25 et ses variantes (BM25F, BM25+, ATIRE/Lucene), le rôle de
l'index inversé dans l'évaluation efficace des requêtes (term-at-a-time vs document-at-a-time,
WAND/Block-Max WAND), et le positionnement face au dense retrieval / hybrid search.

**Frontière avec les thèmes voisins** : `hybrid-search-reranking` traite la combinaison
lexical+dense+reranking ; `approximate-nearest-neighbor` et `text-embeddings` le versant
dense. Ici le focus reste le pilier *lexical / index inversé / BM25*.
