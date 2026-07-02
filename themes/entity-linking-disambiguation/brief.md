# Brief — entity-linking-disambiguation

Entity linking (liage d'entités) et désambiguïsation : relier une mention textuelle à l'entrée
canonique d'une base de connaissances (Wikidata/DBpedia). Couvrir le pipeline (détection de
mentions, génération de candidats, désambiguïsation), l'opposition désambiguïsation *locale*
(contexte de la mention) vs *collective/globale* (cohérence par graphe entre les mentions d'un
document), les approches modernes — bi-encodeur + cross-encodeur (BLINK), liage *génératif*
autorégressif (GENRE), zero-shot / entités émergentes et le cas NIL (mention sans entrée) —,
l'évaluation (AIDA-CoNLL, TAC-KBP) et l'usage en *grounding* pour le RAG et la construction de KG.

Public : ingénieur NLP/IR.

Délimitations : la détection + typage d'entités (NER) relève de
named-entity-recognition-sequence-labeling et du NER par LLM de structured-extraction-llm ; la
canonicalisation OpenIE et l'identité RDF (`owl:sameAs`) sont couvertes par
knowledge-graph-construction ; l'entraînement d'embeddings par text-embeddings ; la recherche
vectorielle par approximate-nearest-neighbor. Se centrer sur mention → KB.

Domaine pressenti : information-retrieval-representation.
