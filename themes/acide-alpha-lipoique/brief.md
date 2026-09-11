# acide-alpha-lipoique — brief

**Sujet.** L'acide alpha-lipoïque (ALA, acide thioctique) : ce que la preuve établit indication
par indication. Dossier principal = la **neuropathie diabétique périphérique** (lignée ALADIN /
SYDNEY / ORPIL / NATHAN 1, scores TSS et NIS, doses 600 à 1 800 mg/j).

**Fil rouge.** *La voie d'administration décide de l'effet.* Le même produit, perfusé, a un
dossier d'essais ; avalé au long cours, il en a un autre — et c'est la forme vendue en
complément. Variable que le corpus n'a jamais traitée.

**Public.** Lecteur exigeant sans formation médicale ; chaque terme clinique défini à première
occurrence (neuropathie, énantiomère, score symptomatique, critère principal contre secondaire).

**Domaine.** `complements-sante` (méta-domaine `sante-nutrition`) — 5e thème du domaine, après
`vitamine-d`, `omega-3`, `collagene`, `melatonine`.

## Angle : pourquoi PAS la minceur

Le piège est de ranger l'ALA en amincissant. Les méta-analyses y donnent des fractions de kilo,
soit l'ordre de grandeur du CLA, de la L-carnitine et du picolinate de chrome **déjà jugés
molécule par molécule** dans `complements-amincissants` : un 4e verdict en fraction de kilo
n'apprendrait rien. Le poids ne sert qu'à **situer** l'ordre de grandeur contre le seuil
réglementaire des 5 %. L'angle qui vaut le run est l'indication clinique étroite, et la voie.

## Délimitations (vérifiées par LECTURE avant lancement)

- ⚠️ **Le patron « une molécule, deux statuts réglementaires » est DÉJÀ ÉCRIT TROIS FOIS** dans le
  corpus : `omega-3` (section `complement-contre-ordonnance`, complément UE/US contre icosapent
  éthyl sous AMM), `melatonine` (section `liberation-prolongee-et-agonistes`, Circadin), et
  `nootropiques-panorama` (section `piracetam-trois-statuts-une-molecule`, dont la formulation
  « Aucun de ces trois statuts ne dépend d'un désaccord scientifique sur les données »). L'ALA
  **n'énonce pas le principe une quatrième fois** : il l'APPLIQUE à son cas propre — dissociation
  **par pays** (complément libre en France et aux États-Unis, Thioctacid sur prescription en
  Allemagne) et non par formulation ni par dose — et renvoie à ces sections pour la mécanique
  générale.
- `incretines-glp1` tient le diabète de type 2 par le seul critère **HbA1c** (section
  `diabete-hba1c`, programmes SUSTAIN / SURPASS). Aucune complication microvasculaire, aucun score
  symptomatique. Partir de là pour la dimension métabolique ; ne redérouler ni le mécanisme
  incrétine ni ces essais.
- `berberine` tient le HOMA-IR et l'HbA1c chez le diabétique de type 2 (−0,63 à −0,73 point sur
  deux méta-analyses, HOMA-IR −0,71) et porte le patron **mécanisme cellulaire ≠ effet humain**
  (titre exact : « AMPK, complexe I, AXIN1 : un mécanisme cellulaire, pas un effet humain
  démontré »). Réutiliser le patron pour le mécanisme antioxydant de l'ALA ; ne pas reprendre les
  chiffres de la berbérine ni comparer les deux molécule à molécule.
- `complements-amincissants` a posé le seuil réglementaire des 5 % et la graduation kilo par kilo
  sur six substances (thé vert/caféine, CLA/carnitine/chrome, garcinia, glucomannane, cétones de
  framboise, éphédra — l'ALA n'y figure pas). Citer sa section `echelle-de-comparaison` comme
  repère ; **ne pas y auditer l'ALA comme septième substance**.
- `vitamine-d` fournit le patron **verdict par indication** : une section par indication, un
  verdict propre à chacune, et les conditions qui le font basculer. À transposer directement —
  neuropathie par voie intraveineuse, neuropathie par voie orale au long cours, sensibilité à
  l'insuline : trois verdicts distincts, jamais un verdict global sur « l'ALA ».
- ⚠️ **Faux ami à ne pas confondre** : le seul « neuropathie » du corpus est la NAION (neuropathie
  optique ischémique antérieure non artéritique) dans `inhibiteurs-pde5`, effet indésirable
  vasculaire oculaire. Aucun rapport avec la neuropathie diabétique périphérique.

## Gap

« Lipoïque », « thioctique », « lipoic » : **0 occurrence** dans les 93 thèmes publiés
(localisation par grep, conclusion par lecture des voisins). Le seul document où « neuropath »
apparaît est `inhibiteurs-pde5`.

## Doctrine de preuve

`docs/evidence-sante.md`, recopiée **intégralement** dans `args.subject` du run (les agents du
pipeline ne lisent pas ce fichier). Flag `verdicts: true`.

**Règle du promoteur, saillante ici** : la lignée ALADIN / SYDNEY / NATHAN a été financée par le
fabricant allemand du thioctique et plusieurs essais partagent le même investigateur principal —
deux essais du même groupe ne sont pas deux sources indépendantes.

**Piste à corroborer ou à écarter, jamais à affirmer sur une source unique** : le syndrome
insulinique auto-immun (hypoglycémies sévères, allèle HLA-DRB1*04:06, séries japonaises et
coréennes).
