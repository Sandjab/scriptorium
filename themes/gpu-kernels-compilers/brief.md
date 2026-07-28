# Brief — gpu-kernels-compilers

**Sujet** : Kernels GPU et compilation pour le deep learning : pourquoi le même modèle va
plusieurs fois plus vite bien programmé.

**Cadrage** : couvrir le modèle d'exécution GPU (SM, warps, hiérarchie mémoire, coalescing,
occupancy), l'intensité arithmétique et le modèle Roofline appliqué aux kernels, l'écriture de
kernels en Triton (tiling, mémoire partagée, autotuning) face à CUDA, la fusion d'opérateurs et
ce qu'elle économise, la pile `torch.compile` (TorchDynamo, AOTAutograd, TorchInductor, graph
breaks), les CUDA Graphs contre l'overhead de lancement, et le paysage des compilateurs
(XLA, TVM).

**Positionnement** : gap réel — la couche kernels/compilation n'est traitée nulle part en propre.
Vérifié par greps ciblés sur les 61 thèmes publiés (2026-07-27) : `torch.compile`, TorchDynamo,
TorchInductor, CUDA Graphs, TVM, coalescing, « Roofline » = **0 occurrence** ; XLA n'apparaît
qu'en blurb (GShard/MoE, self-improving-harness, agent-evaluation-observability) ; le langage
**Triton** n'apparaît que comme mention de kernels fusionnés déjà écrits (Liger Kernel dans
`normalization-layers`, Unsloth dans `lora`, un kernel de prefill dans `llm-inference-serving`),
jamais comme modèle de programmation.

⚠️ **Homonymie à ne pas confondre** : *Triton Inference Server* (NVIDIA, serveur d'inférence) est
déjà traité dans `llm-inference-serving` ; ici il s'agit du **langage Triton** (OpenAI) pour
écrire des kernels.

**Public** : ingénieur ML / infra.

**Délimitations** :
- `transformer-attention` couvre FlashAttention comme **algorithme** (attention exacte, tiling
  IO-aware, FA-2/FA-3) — le citer comme exemple canonique de kernel IO-aware, **ne pas re-dériver**.
- `decoding-sampling` et `llm-inference-serving` couvrent l'**intensité arithmétique** et le
  régime memory-bound du décodage — les citer ; ici l'appliquer aux kernels (Roofline, occupancy).
- `distributed-training-parallelism` couvre le MFU et le recouvrement calcul/communication — le citer.
- `normalization-layers` cite Liger Kernel et `lora` les kernels Triton d'Unsloth comme résultats
  — partir de là, expliquer le **comment**.
- `llm-inference-serving` couvre le versant serving (PagedAttention, batching continu, Triton
  Inference Server) — se délimiter : ici la couche kernels/compilation elle-même.
- `quantization` cite les noyaux AQLM — le citer sans re-dériver la quantification.

**Domaine** : deep-learning-foundations.
