# brief — decoding-sampling

**Domaine :** llm-agents-generation

Décodage et sampling pour la génération de texte par LLM autoregressifs : comment, à l'inférence,
on transforme les logits en tokens. Couvrir les stratégies déterministes (greedy, beam search) et
stochastiques (température, top-k, top-p/nucleus, min-p, typical sampling), les pénalités de
répétition et le contrastive search/decoding ; le rôle du KV cache (et son coût mémoire O(L·D)) ;
et le décodage spéculatif (draft model + vérification, Medusa, EAGLE, lookahead) comme principal
levier de latence.

**Positionnement :** l'étape de génération elle-même. **Public :** ingénieur ML.

**Délimitations :** la mécanique du KV cache et l'attention efficace sont déjà dans
`transformer-attention` (rappeler sans re-dériver) ; le décodage contraint est dans
`structured-extraction-llm` ; l'inférence récurrente des SSM dans `state-space-models` (contraste).
