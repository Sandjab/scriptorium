# Brief — Reranking & recherche hybride (BM25 + dense, cross-encoders)

Le pipeline de recherche **multi-étages** : génération de candidats à fort rappel et faible coût
(lexical **BM25** + dense **bi-encoder**, fusionnés) suivie d'un **reranking** à forte précision et
fort coût (**cross-encoder**) sur le top-K. L'angle directeur est la **cascade rappel→précision** :
chaque étage échange du rappel exhaustif bon marché contre une précision chère, et le rappel@K de
l'étage 1 **plafonne** la qualité atteignable par le reranker.

## Cadrage
Document de référence best-of, en français, niveau technique. Le fil rouge est le **découplage
rappel ≠ précision** réparti sur des étages de coûts asymétriques (bi-encoder = encodage séparé
indexable ; cross-encoder = encodage joint query+doc, non indexable). Le document s'insère dans la
famille « recherche & RAG » du scriptorium, à côté de `text-embeddings`,
`approximate-nearest-neighbor` et `retrieval-augmented-generation` — qu'il suppose connus et
auxquels il renvoie plutôt que de les ré-exposer.

## Périmètre à couvrir
- **Lexical (sparse exact-match)** : Okapi **BM25** (saturation TF, normalisation par longueur,
  IDF), forces (termes exacts, tokens rares, robustesse zero-shot) et faiblesse structurelle
  (vocabulary mismatch / décalage lexical).
- **Dense (bi-encoder)** : dual-encoder, **DPR**, recherche sémantique par embeddings + ANN ;
  forces (synonymie, paraphrase) et faiblesses (exact match, hors-domaine).
- **Recherche hybride** : fusion lexical + dense. **Reciprocal Rank Fusion (RRF)**, combinaison
  convexe de scores normalisés, pourquoi l'hybride bat chaque modalité seule.
- **Reranking** : **cross-encoders** (query+doc encodés conjointement), MonoBERT/monoT5 ; le
  contraste architectural clé **bi-encoder vs cross-encoder** (indexable & rapide vs précis & coûteux).
- **Interaction tardive** : **ColBERT / ColBERTv2** (MaxSim) comme voie médiane entre bi- et
  cross-encoder.
- **Sparse neuronal (learned sparse)** : **SPLADE** (expansion + pondération apprises), qui réconcilie
  lexical et dense.
- **Rerankers LLM** : reranking listwise type **RankGPT**, le glissement récent.
- **Instances réelles à corroborer (≥2 sources indépendantes par fait)** : BM25, DPR,
  ColBERT/ColBERTv2, SPLADE, RRF, benchmarks **MS MARCO** et **BEIR** (généralisation zero-shot),
  cross-encoders de la famille sentence-transformers / Cohere Rerank.
- **Trade-offs & limites** : latence du cross-encoder (coût ∝ K candidats), patron en entonnoir
  (funnel/cascade), le rappel@K de l'étage 1 borne la qualité finale, choix de K.

## Frontières (ne pas ré-exposer ; renvoyer aux thèmes voisins)
- Construction et propriétés des embeddings denses → supposées connues (thème `text-embeddings`).
- Index ANN (HNSW, IVF, PQ) servant l'étage dense → supposé connu (thème
  `approximate-nearest-neighbor`) ; ici on l'**utilise**, on ne le ré-expose pas.
- Génération augmentée → reranking est un **composant** de l'étage retrieval du RAG : renvoyer à
  `retrieval-augmented-generation`, ne pas ré-exposer la génération.
