# Brief — rotary-position-embedding

Encodage positionnel dans les transformers, centré sur RoPE (Rotary Position Embedding) et
l'extension de contexte. Couvrir : pourquoi l'attention a besoin d'une information de position
(invariance par permutation) et les familles de réponses — absolu appris, relatif (Shaw et al.
2018, biais relatif de T5) ; le mécanisme RoPE (rotation des requêtes et clés par sous-espaces 2D,
fréquences géométriques, la position RELATIVE qui émerge du produit scalaire) et ses propriétés
annoncées (décroissance à longue portée, extrapolation) confrontées à ce qu'on mesure ; ALiBi
(biais linéaire, extrapolation « train short, test long ») et NoPE (pas d'encodage explicite dans
un décodeur causal) comme contrepoints ; l'échec d'extrapolation de RoPE au-delà de la longueur
d'entraînement et la famille d'extension de contexte — Position Interpolation, NTK-aware, dynamic
NTK, YaRN, LongRoPE — avec ce que chacune fait aux fréquences et ce qu'elle coûte (fine-tuning ou
non, dégradation en contexte court).

Positionnement : RoPE est l'encodage de quasiment tous les LLM ouverts, et le corpus ne fait que
le NOMMER (4 monographies) sans jamais l'expliquer. Public : ingénieur ML.

## Délimitations (vérifiées par LECTURE de la prose des voisins le 2026-09-25)

- **`transformer-attention`** traite en profondeur l'encodage sinusoïdal absolu (formule, linéarité
  en décalage, figure) et mentionne le « RoPE découplé » de MLA/DeepSeek-V2 en aparté. Partir de
  là : ne pas re-dériver le sinusoïdal, y renvoyer ; le RoPE découplé peut être expliqué ici
  puisque le mécanisme y est enfin posé.
- **Évaluation de la longueur effective** : déjà traitée en profondeur — « Lost in the Middle » et
  context rot dans `context-engineering`, RULER et needle-in-a-haystack dans
  `sparse-attention-long-context` et `retrieval-augmented-generation`. Y RENVOYER ; ici, seulement
  ce que ces mesures disent des méthodes d'extension (fenêtre annoncée ≠ fenêtre effective).
- **`context-engineering`** cite l'« atténuation à longue distance de l'encodage positionnel,
  sinusoïdal ou RoPE » comme cause de compression du contexte effectif, sans la développer : c'est
  ici qu'on l'examine.
- **`sparse-attention-long-context`** tient la réduction du CALCUL de l'attention et renvoie
  explicitement PI/YaRN/NTK à ce thème. Frontière : ici la POSITION, là le motif d'attention.
- **`state-space-models`** et **`recursive-language-models`** : voies alternatives au long
  contexte (récurrence, récursion) — citer, pas traiter.
- Mentions périphériques (M-RoPE de Qwen2-VL dans `multimodal-vlm`, RoPE de TimeGPT dans
  `time-series-forecasting`, kernel RoPE fusionné de Liger dans `gpu-kernels-compilers`) : renvois
  possibles, pas des sujets.

## Homonymie à écarter
- « NTK » : dans NTK-aware, le nom vient de la théorie du Neural Tangent Kernel (apprentissage des
  hautes fréquences) ; ce n'est pas un sujet de la monographie, seulement l'origine du nom.
