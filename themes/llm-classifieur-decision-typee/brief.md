# Brief — llm-classifieur-decision-typee

**Titre de travail** : Le LLM comme classifieur — décision typée et probabilité calibrée
**Domaine visé** : `llm-agents-generation`
**Origine** : backlog `docs/candidate-themes.md`, ajout du 2026-09-25, priorité haute.
Verdict d'audit : gap réel, ~80 % neuf sur le cœur ; prérequis couverts aux deux tiers mais
éclatés sur cinq monographies voisines.

## Sujet

Le modèle de langage employé non pour écrire mais pour décider : il reçoit un texte et rend une
valeur typée — catégorie, booléen, note — assortie d'une probabilité, consommée par du code
plutôt que lue par un humain.

À couvrir :

1. **Le pattern d'architecture** : espace d'étiquettes fermé, enum contraint, lecture de la
   distribution sur un unique token de sortie, logit bias, extraction d'une probabilité de
   classe, et le régime de coût qui en découle — une réponse d'un seul token est dominée par le
   prefill, pas par le decode.
2. **La calibration de cette probabilité** : ECE et reliability diagram appliqués à une
   probabilité de classe produite par un modèle de langage, effet du RLHF, sensibilité au prompt
   et à l'ordre des options, recalibration quand l'API ne rend pas les logits.
3. **Les quatre routes concurrentes et leurs critères d'arbitrage** : décodage contraint par
   enum, lecture des logprobs, tête de classification sur encodeur discriminatif (piste GLiNER),
   petit modèle distillé sur les annotations du grand.
4. **La consommation décisionnelle** : seuil d'acceptation, coûts asymétriques entre faux
   positifs et faux négatifs, abstention et routage vers un modèle plus lourd.
5. **Étude de cas** : la classe de produits « System One » / decision models apparue en
   septembre 2026 avec Jev (TypeSafe AI). Traiter la CLASSE, pas le produit. Le mode d'échec
   mesuré par l'évaluation tierce pré-enregistrée est le fait central : une description de
   critère erronée fait tomber la justesse sous le plancher aléatoire, ce qui fait du libellé de
   la question un programme à déboguer.
6. **Le piège d'attribution de la décomposition** : découper une question en sous-questions puis
   ajuster une régression sur des exemples annotés relève fortement le score, mais le gain
   appartient à l'ensemble annotations + régression, pas au modèle seul.

## Délimitations (renvois, ne pas re-dériver)

- `structured-extraction-llm` — contrat de schéma et décodage contraint (DFA, masques de logits,
  XGrammar, JSONSchemaBench), et l'inversion d'effet sur la classification à espace fermé
  (DDXPlus / Gemini-1.5-Flash : 41,6 % en libre contre 60,3 % en mode JSON, +18,7 pts, quand le
  même mode coûte −26,7 pts sur GSM8K).
- `calibration-classifieurs` — tout l'appareil ECE / Platt / isotonic / temperature et la
  prédiction conforme, en version ML classique. Cette monographie ne mentionne jamais les
  modèles de langage : l'angle neuf est le raccordement, pas la théorie.
- `hallucination-detection-uncertainty` — P(True), P(IK), entropie sémantique, abstention sous
  garantie, mais en génération libre. S'y appuyer et rester sur l'espace d'étiquettes fermé.
- `llm-evaluation` — le juge et le probability weighting de G-Eval (score = Σ p(sᵢ) × sᵢ). La
  frontière est l'usage : évaluer un modèle contre décider en production.
- `knowledge-distillation` — la fabrication du petit modèle.
- `llm-inference-serving` — l'économie prefill / decode.
- `named-entity-recognition-sequence-labeling` — GLiNER, effleuré en une phrase.

## Discipline de sources (non négociable pour ce run)

Tous les chiffres de performance et de prix de Jev sont soit produits par le vendeur, soit issus
d'une évaluation tierce unique et pseudonyme. Le benchmark maison définit la bonne réponse comme
la moyenne des réponses de deux modèles frontière : il mesure à quel prix le modèle est d'accord
avec eux, pas à quelle fréquence il a raison. Aucun de ces chiffres ne doit viser `confirmed` —
réserve déclarée en prose, ou rejet. Le fond du thème repose sur une littérature établie et
corroborable ; c'est elle qui doit porter les sections.
