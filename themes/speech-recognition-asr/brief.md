# Brief — speech-recognition-asr

Reconnaissance automatique de la parole (ASR) neuronale : du signal au texte. Couvrir : le front-end
(spectrogrammes log-mel, fenêtrage, SpecAugment) ; le problème d'alignement sans segmentation et ses
trois réponses — CTC (Graves et al. 2006 : forward-backward, symbole blank), l'attention
encodeur-décodeur (Listen, Attend and Spell) et le RNN-Transducer (Graves 2012) pour le streaming ;
les encodeurs (Conformer : convolution + attention) ; le pré-entraînement auto-supervisé audio
(wav2vec 2.0, HuBERT) et ce qu'il achète en faibles ressources ; l'approche faiblement supervisée à
grande échelle (Whisper, 680 000 h) et ses hallucinations sur le silence ; le décodage (beam search,
fusion avec un modèle de langue : shallow fusion et ses variantes) ; l'évaluation (WER, sa
normalisation de texte et ses pièges, LibriSpeech propre vs bruité, robustesse au bruit et aux
accents, écarts de WER entre groupes de locuteurs, multilinguisme).

Positionnement : la parole est la seule grande modalité absente du corpus. Public : ingénieur ML.

## Délimitations (vérifiées par LECTURE de la prose des voisins le 2026-10-01)

- **`document-ai`** pose CTC en OCR : alignement monotone et indépendance conditionnelle des
  sorties (Graves et al. 2006), et le compromis seq2seq autorégressif plus précis mais plus lent.
  Y RENVOYER pour ces deux contraintes ; ici, CTC sur la parole (forward-backward, blank, pics) et
  ce que le streaming change au compromis.
- **`quantization`** cite Whisper Small quantifié en PTQ 2 bits (WER 37,06 % contre 6,77 % en FP16).
  Citer en une phrase, ne pas refaire la compression.
- **`knowledge-distillation`** cite l'expérience de reconnaissance vocale de Hinton et al. (ensemble
  de 10 modèles acoustiques DNN distillé). Citer, ne pas refaire.
- **`state-space-models`** (SaShiMi, génération de waveform) et **`diffusion-models`** (audio comme
  donnée de diffusion) relèvent de la GÉNÉRATION audio ; le candidat `speech-synthesis-tts` tient la
  direction texte → parole. Ici, uniquement parole → texte.
- **`contrastive-self-supervised`** tient le contrastif visuel ; ici, le versant audio de wav2vec 2.0
  (quantification + contrastif) et HuBERT (prédiction masquée de cibles discrètes).
