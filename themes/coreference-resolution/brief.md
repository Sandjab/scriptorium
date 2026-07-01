# Brief — coreference-resolution

**Sujet (passé à /frugalmonograph) :**

Résolution de coréférence (coreference resolution) : regrouper les mentions d'un texte qui désignent
la même entité (« Marie… elle… la directrice »). Couvrir la formulation par paires puis par rang de
mention (mention-pair, mention-ranking), le modèle end-to-end neuronal à scoring d'empans (Lee et al.
2017) et l'inférence d'ordre supérieur (higher-order), le clustering de mentions, la coréférence par
LLM, et l'évaluation (MUC, B³, CEAF, score CoNLL-2012 sur OntoNotes ; cas Winograd). Public :
ingénieur NLP. Délimitations : distinct de l'entity linking (coréférence = clustering intra-document
de mentions ; EL = mention → base de connaissances) et du NER (détection + typage) ;
structured-extraction-llm ne fait que nommer la coréférence. Se centrer sur le clustering
intra-document des mentions coréférentes.

**Cadrage :**
- Domaine taxonomique pressenti : `information-retrieval-representation` (cohérence avec NER,
  structured-extraction-llm, knowledge-graph-construction). Angle architectural
  `deep-learning-foundations` envisageable — à trancher via `/arrange`.
- Candidat backlog priorité moyenne : gap réel mais plus étroit que NER / entity-linking.
- Poursuit l'intérêt NER de l'utilisateur, après `named-entity-recognition-sequence-labeling`.
