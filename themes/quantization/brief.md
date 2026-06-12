# Brief — Quantization techniques

**Sujet (tel que fourni)** : Quantization techniques

**Cadrage** : techniques de **quantification de modèles d'apprentissage automatique**, avec
focus sur les réseaux de neurones profonds et les LLM. On vise une monographie de référence
couvrant la théorie (réduction de précision numérique, mapping réel→entier, échelle et
point-zéro, schémas symétrique/asymétrique, granularité per-tensor/per-channel/per-group),
les deux grandes familles de méthodes (**PTQ** post-training quantization vs **QAT**
quantization-aware training), les formats (INT8, INT4, FP8, NF4, formats bloc), les méthodes
phares (GPTQ, AWQ, SmoothQuant, LLM.int8()/bitsandbytes, GGUF/llama.cpp k-quants, QLoRA),
les compromis mesurables (mémoire, latence, débit, perplexité/exactitude) et les limites
(outliers d'activation, dégradation à très basse précision, support matériel).

**Hors périmètre** : quantification du signal en traitement du signal, quantification en
physique. Le sens retenu est celui de la compression de modèles ML/LLM.
