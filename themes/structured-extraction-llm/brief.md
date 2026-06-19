# brief — structured-extraction-llm

**Sujet**
L'extraction structurée d'information par LLM : transformer du texte non structuré en
sorties machine-exploitables (JSON, enregistrements typés). Couvrir les trois leviers
techniques — **structured output** (JSON mode, décodage contraint par schéma /
grammaires, `response_format`), **function / tool calling** (l'extraction comme appel
d'outil typé), et l'**ancrage aux empans sources** (*span grounding* : relier chaque
valeur extraite à l'empan exact du texte d'origine, façon **LangExtract** de Google) —
ainsi que les compromis fidélité / hallucination / coût et l'évaluation (exactitude des
champs, taux d'ancrage, robustesse de schéma).

**Cadrage**
- Cœur = la *mécanique* de l'extraction structurée : contrainte de décodage (grammaires,
  automates, FSM type Outlines/GBNF), schémas (JSON Schema / Pydantic), tool calling, et
  *span grounding* / ancrage source. LangExtract traité comme cas d'état de l'art de
  l'ancrage, pas comme tutoriel produit.
- **Frontière à surveiller en revue** : `knowledge-graph-construction` extrait déjà
  entités/relations pour bâtir un graphe — NE PAS re-dériver la construction de graphe ;
  rester sur la sortie structurée contrainte et l'ancrage. `retrieval-augmented-generation`
  et `agentic-ai` utilisent le tool/function calling — ne pas re-expliquer l'agentique ;
  traiter le function calling sous l'angle *extraction typée*. `text-embeddings` /
  `hybrid-search-reranking` sont orthogonaux (représentation, pas extraction).
- **Trou pressenti** (à confirmer par le Sweep) : le décodage contraint, l'ancrage aux
  empans et l'extraction-comme-tool-call sont cités en passant ailleurs mais jamais
  expliqués comme discipline propre ; LangExtract, JSON Schema constrained decoding et
  *span grounding* absents du corpus.
