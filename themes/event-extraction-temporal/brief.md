# Brief — event-extraction-temporal

**Sujet** : Extraction d'événements et d'information temporelle : qui a fait quoi, à qui, et quand.

**Cadrage** : couvrir le schéma ACE (triggers, arguments, types d'événements), la détection de
triggers et l'étiquetage d'arguments (par classification, par question-réponse, par génération),
la coréférence d'événements, l'extraction temporelle (TimeML et TIMEX3, normalisation des
expressions temporelles, relations temporelles et TempEval) et la construction de chronologies
(timelines), avec les benchmarks (ACE 2005, MAVEN, TimeBank).

**Positionnement** : gap réel, audience plus étroite que la relation extraction. ACE 2005 n'est
cité que comme benchmark ICL dans `structured-extraction-llm` ; TIMEX seulement comme catégorie
MUC historique dans le thème NER. Triggers/arguments, coréférence d'événements, TimeML =
0 occurrence dans le corpus.

**Public** : ingénieur NLP.

**Délimitations** :
- `structured-extraction-llm` cite l'event extraction comme benchmark des LLM extracteurs — la citer.
- `named-entity-recognition-sequence-labeling` détecte les entités qui servent d'arguments.
- `relation-extraction` traite la RE binaire entité-entité — ne pas la re-dériver.
- `coreference-resolution` traite la coréférence d'entités ; ici celle d'**événements**, distincte.
- `document-ai` couvre la lecture du document image en amont.
- Se centrer sur les structures événementielles et le temps.

**Domaine** : information-retrieval-representation.
