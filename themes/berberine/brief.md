# berberine — brief

**Sujet** : Berbérine : l'alcaloïde vendu comme « Ozempic naturel ».

**Domaine visé** : `complements-sante` (méta `sante-nutrition`) — à trancher par `/arrange`.
Ce domaine n'existe pas encore dans `tools/taxonomy.json` : `berberine` le crée (3e domaine
du méta santé, après `nutrition-sportive` et `pharmacologie-metabolique`).

**Priorité** : haute (backlog `docs/candidate-themes.md`).

## Angle

Le démontage chiffré d'une équivalence marketing. Le sujet n'est pas « la berbérine
marche-t-elle », mais « qu'est-ce qui est réellement mesuré, à quelle dose, avec quelle
qualité d'essai, et à quelle distance de la molécule à laquelle on la compare ».

## Couverture attendue

- Mécanisme : activation de l'AMPK (rang mécanistique — à formuler comme claim sur le
  mécanisme, pas sur l'effet humain, cf. règle 5 de la doctrine).
- Effets glycémiques : méta-analyses, comparaison à la metformine — ampleur réelle ET
  qualité des essais (petits, hétérogènes, majoritairement chinois, biais de publication
  à documenter explicitement).
- Effets lipidiques.
- Biodisponibilité orale très faible et ses conséquences (le paradoxe pharmacocinétique :
  comment un composé si peu absorbé produit-il un effet mesuré ?).
- Sécurité, doses, interactions — **section obligatoire** : troubles digestifs,
  inhibition CYP3A4/P-gp, contre-indication grossesse/allaitement (kernictère néonatal).
- Démontage de la comparaison aux agonistes GLP-1 : ordres de grandeur de perte de poids
  incomparables.

## Délimitations (vérifiées par lecture le 2026-08-10)

- `incretines-glp1` (livré le 2026-08-08) **exclut explicitement** la berbérine de son
  périmètre et la promet deux fois comme thème du corpus — une fois dans la section sur le
  marché gris (« la berbérine, promue comme "Ozempic naturel" […] deux sujets qui relèvent
  d'autres thèmes du corpus et ne seront pas traités ici »), une fois dans sa clôture
  (« celui sur la berbérine, vendue comme un équivalent naturel de ces molécules »).
  → Ne PAS re-traiter la pharmacologie des incrétines : s'y adosser et la citer pour
  l'ordre de grandeur (jusqu'à ~20 % du poids corporel), qui est l'étalon du démontage.
- `complements-amincissants` (candidat non lancé) couvrira les autres molécules en vente
  libre (EGCG, CLA, garcinia, chrome, glucomannane) — ne pas les traiter ici.
- `proteines-besoins-timing` couvre la masse maigre en déficit calorique.
- Aucune occurrence de « berbérine », « AMPK » ou « metformine » ailleurs dans le corpus
  hors `incretines-glp1` (metformine y apparaît uniquement comme traitement de fond des
  bras SURPASS-2).

## Doctrine

`docs/evidence-sante.md`, recopiée **en bloc** dans `args.subject` (les agents du pipeline
ne lisent pas le fichier).
