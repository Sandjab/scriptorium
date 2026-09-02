# Emploi et marché du travail sous IA générative

**Sujet.** Les effets de l'IA générative sur l'emploi : ce que mesurent les indices
d'exposition, et ce que montrent les données réalisées.

**Public.** Dirigeant, économiste, ingénieur — quelqu'un qui doit distinguer une prédiction
d'une mesure.

## Ce que le document doit couvrir

- **La construction des indices d'exposition par tâche** et leurs hypothèses : Eloundou et al.
  (« GPTs are GPTs »), Felten et al. (AI Occupational Exposure), Webb (« The Impact of Artificial
  Intelligence on the Labor Market », appariement brevets/tâches). Ce qu'ils mesurent
  exactement, sur quelles nomenclatures (O*NET), avec quels annotateurs, et où ils divergent
  entre eux — deux indices qui classent la même profession à l'opposé sont un résultat, pas un
  bruit.
- **L'écart entre exposition et usage réel** : l'Anthropic Economic Index et les enquêtes
  d'usage (part des tâches réellement déléguées, automatisation vs augmentation, concentration
  sur quelques occupations). L'exposition est un plafond théorique ; l'usage est une mesure.
- **Les premiers effets réalisés sur l'emploi** : Brynjolfsson, Chandar & Chen (« Canaries in
  the Coal Mine ? », recul relatif de l'emploi des 22-25 ans dans les métiers fortement exposés,
  par tarissement du flux entrant) — et son identification, ses données (paie ADP), ses limites.
- **Contre les effets agrégés nuls** : Humlum & Vestergaard (Danemark, effet agrégé nul sur les
  salaires et les heures). Pourquoi deux études sérieuses ne disent pas la même chose : périmètre,
  pays, période, marge mesurée (flux d'embauche vs stock, salaires vs heures).
- **Substitution vs complémentarité par occupation** : la théorie des tâches (Acemoglu-Autor,
  Autor-Levy-Murnane) comme grille de lecture, l'effet de rétablissement (reinstatement) et les
  nouvelles tâches, et pourquoi « exposé » ne dit ni substitué ni complété.
- **Salaires et polarisation** : ce que les données montrent (et ne montrent pas) sur la
  structure des salaires, la comparaison avec l'épisode d'informatisation/routinisation et sa
  polarisation documentée.
- **Ce qu'on ne sait pas encore mesurer** : recomposition interne des postes, effets d'équilibre
  général, décalage entre adoption et effet.

## Délimitations strictes (vérifiées par lecture du corpus le 2026-09-02)

- ⚠️ **`ia-productivite-esn` tient DÉJÀ, en profondeur et avec une figure, tout le spectre des
  projections macroéconomiques** : Acemoglu (TFP < 0,66 % sur dix ans, 20 % des tâches exposées,
  23 % rentablement automatisables), Goldman Sachs Briggs-Kodnani (+7 %/an de PIB mondial), Penn
  Wharton, OCDE, Baily et al., et le paradoxe d'agrégation gain-de-tâche → point-de-PIB. **NE PAS
  re-dériver ce spectre.** Le citer en une incise comme aval du raisonnement, et rester en amont :
  ce que les indices d'exposition mesurent, et ce que les données d'emploi réalisées montrent.
  `ia-productivite-esn` couvre aussi la productivité et la J-curve : les citer, partir de là.
- ⚠️ **`ia-competences-deskilling-apprentissage` tient déjà les canaries sous l'angle de
  l'apprentissage** : il cite Brynjolfsson/Chandar/Chen (~16 % chez les 22-25 ans), Hosseini
  Maasoum & Lichtinger (effectif junior −9 % après six trimestres chez les adoptantes), la
  tribune Russinovich-Hanselman (« AI boost » senior / « AI drag » junior), et l'enquête WEF sur
  les rôles d'entrée de gamme — mais il déclare explicitement que « la lecture de l'emploi est
  traitée ailleurs » et ne retient que la voie d'apprentissage. **C'est ici cette lecture
  manquante** : le marché du travail, pas l'apprenant. Reprendre ces résultats est légitime et
  attendu, à condition de les traiter comme des faits d'emploi (identification, marge mesurée,
  contrefactuel), pas comme des faits de formation — et de ne pas redire le préceptorat, la
  deliberate practice ni le pipeline de seniors.

## Pièges nommés

- **Les indices d'exposition sont des prédictions, jamais des mesures.** Ne jamais présenter un
  score d'exposition comme un effet observé, ni « X % des emplois exposés » comme « X % des
  emplois menacés » — l'énoncé d'origine porte sur des *tâches*, et souvent sur une réduction de
  temps à qualité constante.
- **Les reprises de presse fabriquent des chiffres.** Les pourcentages qui circulent sur l'emploi
  junior varient d'un relais à l'autre sans source identifiable ; remonter à la publication
  primaire (NBER, SSRN, arXiv, site du labo) et écarter le chiffre qu'on ne retrouve pas.
- **Un working paper non relu par les pairs reste un working paper** : le dire, et ne pas le
  fondre dans une convergence avec des travaux publiés.
- **Ne pas additionner des estimations de périmètres différents** (un pays, une plateforme, une
  cohorte d'âge, un secteur) en une fausse fourchette.

## Domaine

`ai-organizations` (3e thème du domaine, après `ia-productivite-esn` et
`ia-competences-deskilling-apprentissage`).
