# Brief — named-entity-recognition-sequence-labeling

## Sujet (tel que fourni)

Reconnaissance d'entités nommées (NER) par étiquetage de séquences et architectures d'empans :
détecter et typer les entités d'un texte. Couvrir les schémas d'étiquetage (BIO, BIOES et leurs
pièges), la lignée discriminative (HMM/MEMM → CRF, fonction de coût et inférence de Viterbi), le
NER neuronal classique (BiLSTM-CRF, features char-CNN + word embeddings), le passage aux encodeurs
(BERT token classification), puis les architectures d'empans (span-based, biaffine, MRC-as-NER) et
les cas durs (entités imbriquées / nested NER, entités discontinues / discontinuous NER), avec
l'évaluation (F1 par entité, CoNLL-2003, OntoNotes, GENIA). Public : ingénieur ML/NLP.

## Cadrage

- **Centre de gravité** : le versant **DISCRIMINATIF** du NER — détection + typage d'empans par
  étiquetage de séquences et modèles d'empans. C'est le socle que le corpus ne couvre pas encore
  (aujourd'hui seul le NER *génératif par LLM* existe via `structured-extraction-llm`).
- **Fil conducteur** : schémas d'étiquetage → chaîne discriminative (HMM/MEMM → CRF, Viterbi) →
  neuronal classique (BiLSTM-CRF, char-CNN) → encodeurs (BERT token classification) → empans
  (span-based, biaffine, MRC-as-NER) → cas durs (nested, discontinu) → évaluation (F1 par entité,
  CoNLL-2003 / OntoNotes / GENIA).

## Délimitations (hors périmètre — renvoyer aux thèmes dédiés)

- NER **génératif par LLM** et décodage contraint → `structured-extraction-llm`
  (ne pas re-traiter GPT-NER / PromptNER / LangExtract).
- **Entity linking** (mention → base de connaissances) → `entity-linking-disambiguation`.
- **Relation extraction** et canonicalisation OpenIE → `knowledge-graph-construction`.
- Entraînement d'**embeddings** → `text-embeddings`.

## Domaine (taxonomie home)

Pressenti : `information-retrieval-representation` (cohérence avec `structured-extraction-llm` /
`knowledge-graph-construction`). Angle architectural `deep-learning-foundations` envisageable —
à trancher par `/arrange`.
