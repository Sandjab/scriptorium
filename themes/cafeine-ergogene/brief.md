# Brief — cafeine-ergogene

**Sujet.** La caféine comme aide ergogène : ce que les essais mesurent, à quelle dose, pour
quel type d'effort, et chez qui.

9e thème du méta-domaine `sante-nutrition`, 3e du domaine `nutrition-sportive` (après
`creatine` et `proteines-besoins-timing`). Priorité moyenne du backlog
(`docs/candidate-themes.md:773-774`).

## Périmètre

- **Pharmacologie humaine** : absorption et pic plasmatique, demi-vie et sa variabilité
  interindividuelle, métabolisme hépatique par le CYP1A2, formes galéniques (caféine
  anhydre, café, gomme à mâcher, gel) et ce que la forme change réellement au décours.
- **Mécanisme** : antagonisme des récepteurs A1/A2A de l'adénosine — *terrain neuf, décrit
  nulle part dans le corpus*. Y rattacher le sort de l'hypothèse historique de l'épargne
  du glycogène par mobilisation des acides gras libres, largement abandonnée.
- **Endurance** : taille d'effet et plage complète des estimations en méta-analyse, pas une
  borne ; temps jusqu'à épuisement vs contre-la-montre (deux protocoles qui ne mesurent pas
  la même chose et ne donnent pas la même amplitude).
- **Force, puissance, efforts intermittents** : 1RM, hauteur de saut, sports d'équipe —
  effet plus petit et plus hétérogène qu'en endurance ; dire l'hétérogénéité, pas la lisser.
- **Dose-réponse** : la plage 3-6 mg/kg, l'existence ou non d'un gain au-delà, les faibles
  doses (~1-2 mg/kg, ~200 mg), le point où les effets indésirables progressent plus vite
  que la performance.
- **Timing et habituation** : délai de prise, et surtout la question de la tolérance —
  le consommateur habituel conserve-t-il le bénéfice, un sevrage préalable ajoute-t-il
  quelque chose ? Littérature contradictoire, à rendre comme telle.
- **Génotype** : CYP1A2 (rs762551) et ADORA2A — la promesse commerciale du test génétique
  confrontée à des résultats qui ne concordent pas d'un essai à l'autre. Angle central du
  document, à traiter comme un cas d'école de la reproductibilité, pas comme un fait acquis.
- **Position de société savante** : position stand ISSN sur la caféine (Guest et al. 2021),
  classification AIS Groupe A.
- **Statut antidopage** : retrait de la liste des substances interdites en 2004, programme
  de surveillance de l'AMA — et ce que ce statut veut dire, ou ne veut pas dire.
- **Croyances à trancher chiffres en main** : caféine et déshydratation, café vs caféine
  anhydre, part de l'attente/placebo dans l'effet mesuré.
- **Sécurité, doses, interactions** (section obligatoire) : seuils EFSA (400 mg/j chez
  l'adulte sain, 200 mg en dose unique, 3 mg/kg), sommeil et prise en soirée compte tenu de
  la demi-vie, arythmies, anxiété, grossesse, adolescents, interactions médicamenteuses,
  intoxications par poudre de caféine anhydre pesée à domicile.

## Délimitations (vérifiées par LECTURE des 8 documents santé le 2026-08-14)

Le cœur du sujet est **absent à 100 %** du corpus. Un seul recouvrement, déjà borné par le
voisin lui-même :

- **`complements-amincissants`** garde la caféine sous l'angle **thermogenèse et perte de
  poids**, et l'écrit dans sa prose : « La caféine n'est retenue ici que pour sa
  thermogenèse et sa dépense énergétique ; son usage ergogène, en contexte sportif, relève
  d'un autre thème et n'est pas abordé. » Son `brief.md` réservait explicitement
  `cafeine-ergogene`. Ne PAS re-chiffrer ni re-vérifier :
  1. les +3-4 % de métabolisme de repos à 100 mg et l'asymétrie 150 vs 79 kcal/j
     (Dulloo 1989) — fait `confirmed` du corpus, y renvoyer par une arête ;
  2. l'absence de relation dose-réponse **sur le poids** de 1,0 à 15,0 mg/kg (Tabrizi 2019)
     — rejet documenté, ne pas le rejouer. ⚠️ Cette plage en mg/kg recoupe visuellement les
     3-6 mg/kg ergogènes : **deux critères de jugement différents** (masse corporelle vs
     performance), à ne surtout pas fusionner ;
  3. le bras « éphédrine + caféine » de Shekelle 2003 et le dossier des brûleurs
     sur-dosés en stimulants. La sécurité se traite ici sous l'angle du sportif.
- **`creatine`** ne mentionne la caféine qu'une fois, comme élément de la liste AIS Groupe A
  (0 claim sur 33) — renvoyer par une arête, rien à délimiter.
- **`proteines-besoins-timing`**, **`peptides-gris`**, **`berberine`**, **`vitamine-d`**,
  **`collagene`**, **`incretines-glp1`** : absence totale, aucun claim, aucune frontière à
  poser. (`berberine` cite CYP3A4/2D6/2C9 et la P-gp, jamais le CYP1A2.)

## Public

Lecteur exigeant **sans formation médicale** — définir chaque terme clinique à première
occurrence (ergogène, demi-vie d'élimination, CYP1A2, polymorphisme, contre-la-montre vs
temps jusqu'à épuisement, taille d'effet, hétérogénéité).

## Doctrine de preuve santé

`docs/evidence-sante.md`, recopiée **intégralement** dans `args.subject` (les agents du
pipeline ne lisent pas ce fichier). Profil attendu, à l'inverse de `collagene` : littérature
abondante, répliquée, avec plusieurs méta-analyses et une position ISSN — donc peu de rejets
mono-source mécaniques. Le risque n'est pas le rejet, c'est la **fausse concordance** : sur
le génotype CYP1A2 et sur l'habituation, les essais se contredisent ; un claim qui lisse
cette contradiction serait faux même avec deux sources de rang fort.

Run : `/leanmonograph cafeine-ergogene`, 37e run lean, 9e thème santé. `verdicts: true`.
Domaine pressenti `nutrition-sportive` — qui n'a PAS encore de portail malgré ses 2 thèmes ;
`/arrange` devra le créer après ce run.
