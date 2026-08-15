# Brief — nootropiques-stimulants-prescrits

> ⚠️ Ce fichier documente le cadrage pour un lecteur humain. **`workflow.js` ne le lit pas** :
> tout ce qui doit atteindre les agents est recopié dans `args.subject` au lancement.

**Domaine visé** : `performance-cognitive` — **domaine créé par ce thème** (4e domaine santé).
**Pipeline** : `/leanmonograph`, `verdicts: true` (thème santé).
**Fiche d'origine** : `docs/candidate-themes.md`, § `performance-cognitive` (proposé le 2026-08-15).

## Le sujet en une phrase

Modafinil, méthylphénidate, amphétamines pris hors AMM par des sujets sains pour « augmenter »
la cognition : ce que les essais mesurent réellement, domaine cognitif par domaine cognitif.

## Pourquoi ce thème

Couverture nulle vérifiée par lecture (passe du 2026-08-15) : aucune occurrence de `nootrop*`,
`modafinil`, `racétam`, `méthylphénidate` dans les 76 documents alors que le label du méta-domaine
promet « Santé, nutrition & performance **humaine** » — la performance y est exclusivement
physique. Densité de preuve la plus forte du domaine et écart promesse/preuve maximal : la revue
systématique de Battleday & Brem (2015) conclut à un bénéfice **confiné** là où l'usage détourné
promet une augmentation générale.

## Fil rouge

L'effet existe, il est réel, et il est **conditionnel** — à la complexité de la tâche, à la ligne
de base du sujet, à l'état du cerveau qu'on dope. « Augmenter un cerveau sain et reposé » n'est
pas ce que la littérature démontre ; c'est ce que l'usage suppose.

## Frontières (ne pas refaire)

| Voisin | Ce qu'il couvre déjà |
|---|---|
| `creatine`, § « Cerveau et cognition » | **arête à poser** : double comptage des sous-tests dans les méta-analyses pivots, refus d'allégation EFSA, effet qui change de signe selon la métrique (temps de réponse vs précision), **thèse de l'effet de circonstances** (cerveau privé de sommeil vs reposé). Ce thème la *généralise* aux molécules prescrites — il ne la refait pas sur la créatine. |
| `cafeine-ergogene` | purement ergogène ; ne dit rien du versant vigilance/cognition (0 occurrence de « cognition »). Le versant caféine-cognition est un **thème à part** du backlog (n° 6) — ne pas l'absorber ici. |
| `complements-amincissants`, `peptides-gris` | patron du marché gris et du contenu réel des gélules — hors périmètre ici (molécules **prescrites**, pas de rayon). |

## Périmètre

Couvrir : le modafinil chez le narcoleptique (indication autorisée) vs chez le sujet sain non
privé de sommeil ; Battleday & Brem et les méta-analyses antérieures avec le **détail des domaines
cognitifs** où l'effet tient et de ceux où il ne tient pas ; la dépendance du verdict à la
complexité de la tâche et à la ligne de base (effet plus net chez les performeurs bas) ; la
privation de sommeil comme condition qui fabrique l'effet ; méthylphénidate et amphétamines en
usage détourné (populations étudiantes — prévalence déclarée vs mesurée) ; les échelles de mesure
elles-mêmes (« tester une cognition normale ou supra-normale de façon fiable » reste un problème
ouvert) ; sécurité, dépendance, sommeil, effets cardiovasculaires ; statut réglementaire et cadre
du hors-AMM.

**Posture** : document descriptif sur littérature publiée — ce que les essais mesurent, ce que le
régulateur dit, quels risques sont documentés. Ni mode d'emploi, ni guide d'obtention, ni
protocole d'usage. Bandeau non-conseil médical porté par la clé `notice` du méta-domaine.

## Réflexes de vérification hérités des runs précédents

- **Argument du silence** (30e run) : sur toute tournure « sans effet indésirable rapporté »,
  vérifier que le paramètre a été MESURÉ par la source. Risque élevé ici sur le cardiovasculaire
  et le sommeil dans des essais à dose unique.
- **Double comptage des sous-tests** (leçon `creatine`, endémique au domaine) : un essai qui
  fournit sept sous-tests cognitifs aux mêmes participants ne fournit pas sept observations
  indépendantes. Vérifier que « N observations » n'excède pas « N randomisés ».
- **Fausse plage par agrégation de compartiments** (32e run) : ne pas fusionner des domaines
  cognitifs distincts en une plage d'effet unique. Signal d'alarme : « respectively ».
- **Fausse indépendance par scission de source** (33e run) : comparer effectifs et valeurs
  secondaires avant de croire deux séries « indépendantes ».
- **Rejet qui jette la correction du juré** (37e run) : après le run, lire les notes des jurés des
  claims rejetés en cherchant `holds=false` AVEC une correction.
- **Prévalence déclarée vs mesurée** : sur l'usage détourné étudiant, les chiffres d'auto-report
  varient d'un ordre de grandeur selon la formulation de la question — jamais une prévalence sans
  sa méthode de collecte.
