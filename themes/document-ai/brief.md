# Brief — document-ai

**Sujet** : Compréhension de documents (Document AI) : du pixel au contenu structuré.

**Cadrage** : couvrir l'OCR neuronal (détection + reconnaissance, modèles séquence type TrOCR),
les modèles texte + layout + image (lignée LayoutLM v1→v3 et ses pré-entraînements), les approches
sans OCR (Donut, Pix2Struct) et les VLM généralistes appliqués au document, les tâches et
benchmarks (classification, extraction clé-valeur — FUNSD, reconnaissance de tables, DocVQA), le
parsing de PDF pour les pipelines RAG, et l'évaluation (ANLS, TEDS, pièges des benchmarks saturés).

**Positionnement** : le corpus traite l'extraction sur texte propre mais jamais le document image —
OCR, LayoutLM, DocVQA, Donut = 0 occurrence. Gap réel.

**Public** : ingénieur ML/data.

**Délimitations** :
- `structured-extraction-llm` couvre l'extraction depuis le TEXTE — la citer comme aval de l'OCR.
- `relation-extraction` traite le niveau document sur texte propre (DocRED), pas l'image.
- `multimodal-vlm` couvre l'architecture VLM générique (projection, Q-Former, tokens visuels) —
  la citer, ne pas la re-dériver.
- `retrieval-augmented-generation` couvre le pipeline RAG en aval — ici le parsing de PDF qui
  l'alimente.
- Se centrer sur la modalité document/layout : pixel → structure.

**Domaine** : information-retrieval-representation.
