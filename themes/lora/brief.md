# brief — lora

**Sujet**
LoRA (Low-Rank Adaptation) pour le fine-tuning efficace en paramètres des LLM :
adaptation de bas rang ΔW = B·A sur des poids figés, hyperparamètres rang r et alpha,
variantes de référence (QLoRA, DoRA, AdaLoRA), fusion des poids à l'inférence, et
compromis face au fine-tuning complet.

**Cadrage**
- LoRA au cœur (méthode de référence) ; la famille PEFT (QLoRA, DoRA, AdaLoRA,
  adapters) est traitée comme variantes / état de l'art, pas comme panorama dilué.
- Frontière à surveiller en revue : QLoRA s'appuie sur la quantification 4-bit (NF4)
  déjà couverte par le thème `quantization` — ne pas re-dériver la quantization, la
  citer comme socle.
- Demande latente confirmée : LoRA est cité mais jamais expliqué dans le corpus
  (`self-improving-harness`).
