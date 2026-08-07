# Brief — hallucination-detection-uncertainty

**Sujet** : Détection des hallucinations et estimation de l'incertitude des LLM — savoir quand
la réponse ne vaut rien.

## Cadrage (repris du backlog, verdict de gap du 2026-08-06)

Couvrir :
- la **typologie** : confabulation vs erreur de connaissance, incertitude aléatoire vs épistémique ;
- l'**entropie sémantique** : regroupement par équivalence de sens plutôt que par séquence de
  tokens, et les sondes qui l'approchent depuis les états cachés en une seule génération ;
- les méthodes par **échantillonnage et cohérence** : SelfCheckGPT, auto-consistance ;
- les **signaux internes et déclarés** : probabilité de séquence, p(true), confiance verbalisée
  et sa sur-confiance ;
- la **vérification factuelle décomposée** : FActScore et les métriques par atome ;
- la **décision** qui en découle : abstention, escalade, déférence à un humain ;
- l'**évaluation** : TruthfulQA, HaluEval, jeux dédiés, et le piège de mesurer un détecteur sur
  des hallucinations fabriquées.

**Public** : ingénieur ML.

## Délimitations (frontières avec le corpus existant)

- `calibration-classifieurs` couvre la calibration et la prédiction conforme sur classifieurs :
  les citer comme socle, **ne pas re-dériver ECE ni la couverture conforme**.
- `retrieval-augmented-generation` couvre l'ancrage documentaire et ses garanties formelles
  (C-RAG, SGI) : ici le cas **sans corpus de référence**.
- `llm-evaluation` couvre le juge-LLM et ses biais.

**Domaine pressenti** : `llm-agents-generation`.
