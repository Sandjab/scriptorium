# Brief — speech-synthesis-tts

Synthèse vocale neuronale (TTS) et codecs audio neuronaux : du texte à la parole. Couvrir : la lignée
acoustique en deux étages (Tacotron 2 : texte → mel-spectrogramme → vocoder) ; le passage non
autorégressif (FastSpeech, FastSpeech 2) et le contrôle explicite de la durée, de la hauteur et de
l'énergie (prosodie) ; les vocoders neuronaux (WaveNet, puis HiFi-GAN et ses discriminateurs
multi-période/multi-échelle, DiffWave) ; le TTS de bout en bout (VITS) ; les codecs audio neuronaux
(SoundStream, EnCodec, quantification vectorielle résiduelle RVQ, débits et compromis qualité) ; le
TTS comme modèle de langage sur tokens audio (VALL-E, AudioLM) et le zero-shot / clonage de voix à
partir de quelques secondes ; les risques d'usage (usurpation de voix, deepfakes audio) et leurs
contre-mesures (détection, filigrane audio) ; l'évaluation (MOS et ses pièges, WER de resynthèse,
similarité de locuteur).

Positionnement : seule la direction parole → texte existe dans le corpus. Public : ingénieur ML.

## Délimitations (vérifiées par LECTURE de la prose des voisins le 2026-10-10)

- **`speech-recognition-asr`** tient la direction inverse (parole → texte) et nomme la synthèse vocale
  comme telle. Ici uniquement texte → parole ; le WER n'y apparaît que comme métrique d'intelligibilité
  par resynthèse (renvoyer à l'ASR pour ses pièges de normalisation). HuBERT (unités discrètes) : citer,
  ne pas refaire.
- **`diffusion-models`** traite WaveGrad, DiffWave (MOS 4,44 vs WaveNet 4,43 sur LJSpeech) et AudioLDM
  en un paragraphe. Ici DiffWave seulement comme une famille de vocoders parmi d'autres ; renvoyer pour
  le mécanisme de diffusion.
- **`state-space-models`** cite SaShiMi (waveform non conditionnée) ; **`convolutional-networks`** pose
  les convolutions dilatées de WaveNet. Citer, ne pas refaire.
- **`generative-adversarial-networks`** tient l'entraînement adversarial général ; ici, ce que les
  discriminateurs de HiFi-GAN apportent au vocoder.
- **`approximate-nearest-neighbor`** traite la quantification résiduelle pour la recherche vectorielle ;
  ici, la RVQ comme goulot d'un codec appris.
