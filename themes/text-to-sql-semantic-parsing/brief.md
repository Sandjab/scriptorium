# text-to-sql-semantic-parsing — brief

**Domaine visé** : information-retrieval-representation.

## Sujet

Du langage naturel à la requête exécutable : text-to-SQL et parsing sémantique. Couvrir la tâche et
ses benchmarks (Spider et l'évaluation par correspondance exacte vs exécution, BIRD et les bases
réalistes, Spider 2.0 et les flux d'entreprise), le schema linking comme cœur du problème (colonnes
ambiguës, valeurs, jointures implicites), les approches (encodeur-décodeur contraint par la
grammaire, LLM avec schéma dans le contexte, décomposition, exécution comme oracle et
auto-correction), les erreurs typiques (requête plausible et fausse, agrégations, NULL), la
sécurité (injection, droits), l'évaluation (exécution vs sémantique, plusieurs requêtes
correctes), et l'extension aux graphes (text-to-SPARQL/Cypher). Public : ingénieur ML/data.

## Délimitations

- `structured-extraction-llm` garde le schéma JSON en sortie (ici un PROGRAMME exécutable).
- `knowledge-graph-construction` garde les langages de graphe (SPARQL, GQL) eux-mêmes.
- `agentic-ai` garde l'agent qui appelle une base (cas d'usage à citer, pas l'objet).
- `llm-code-generation` garde la génération de code générale (HumanEval, reranking, Self-Debug) ;
  il cite Spider deux fois en passant (oracle 71,6 % vs log-prob 33,7 % ; gain Self-Debug) —
  ici Spider est l'objet, pas un banc parmi d'autres.

## Gap (re-vérifié par lecture le 2026-10-09)

Spider n'apparaît que comme banc cité dans `llm-code-generation` ; schema linking, BIRD,
exact match vs execution accuracy : absents du corpus.
