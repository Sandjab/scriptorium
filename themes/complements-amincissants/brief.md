# complements-amincissants — brief

**Sujet** : Compléments amincissants en vente libre : ce que montrent les méta-analyses.

**Domaine visé** : `pharmacologie-metabolique` (méta `sante-nutrition`) — à confirmer par
`/arrange`. Le domaine existe déjà (créé par `incretines-glp1` le 2026-08-08) et son blurb
l'annonce littéralement : « La promesse minceur, du médicament efficace au complément
inefficace. » Ce thème est le second terme de cette phrase.

**Priorité** : haute (backlog `docs/candidate-themes.md`).

## Angle

Le debunking chiffré assumé. Le sujet n'est pas « les compléments amincissants
fonctionnent-ils » — la réponse est connue — mais **de combien exactement**, mesuré
molécule par molécule, et **pourquoi un marché de cette taille survit à ces chiffres**.
La monographie doit rester lisible pour un lecteur qui a ces produits sous les yeux en
pharmacie : chaque molécule reçoit son verdict avec sa dose, sa taille d'effet et la
qualité de sa preuve, pas un jugement global.

## Couverture attendue

- **Molécule par molécule** : thé vert / EGCG, CLA (acide linoléique conjugué),
  L-carnitine, garcinia cambogia (HCA), cétones de framboise, chrome (picolinate),
  glucomannane, caféine. Pour chacune : dose testée, effet mesuré en méta-analyse (au
  mieux 1-2 kg, souvent indiscernable de zéro), qualité et taille des essais.
- **La qualité de la preuve comme résultat** : essais courts, petits, hétérogènes,
  financement industriel fréquent (règle 4 de la doctrine — à signaler claim par claim),
  biais de publication.
- **Le cas éphédra** : efficace ET retiré du marché. Pourquoi — le seul point du sujet où
  l'efficacité est réelle, et où c'est précisément la sécurité qui a tranché.
- **Cadre réglementaire** : complément vs médicament, allégations santé EFSA (registre des
  allégations rejetées) et cadre FDA/DSHEA — pourquoi un produit peut être vendu sans
  avoir démontré quoi que ce soit.
- **Adultération** : produits « naturels » dopés aux principes actifs pharmaceutiques
  (sibutramine, phénolphtaléine, laxatifs) — les listes FDA de *tainted weight loss
  products*, ce que les analyses de laboratoire trouvent réellement dans les gélules.
- **Sécurité, doses, interactions** — section obligatoire par la doctrine : hépatotoxicité
  (thé vert à forte dose, garcinia), effets cardiovasculaires des stimulants, interactions.

## Délimitations (vérifiées par LECTURE de la prose le 2026-08-10)

- **`berberine`** (livré le 2026-08-10, même domaine) traite déjà la berbérine en
  profondeur, y compris **la qualité de fabrication de ce produit précis** (NOW Foods 2023 :
  aucun des 33 produits conforme à son étiquette ; ConsumerLab : teneur moyenne 75 %).
  → Ne PAS re-traiter la berbérine comme une molécule de la liste ; y renvoyer par une
  arête. Le sous-dosage y est traité **produit par produit sur un seul complément** ;
  ici l'angle est l'**adultération pharmacologique délibérée** d'une classe entière, ce
  qui est un autre phénomène — le dire explicitement plutôt que de le laisser deviner.
- **`incretines-glp1`** (livré le 2026-08-08, même domaine) couvre le marché gris, la
  préparation magistrale (503A/503B), la contrefaçon de médicaments GLP-1 et les alertes
  ANSM/EMA. → L'adultération traitée ici porte sur des **compléments alimentaires en vente
  libre**, pas sur des copies de médicaments sur ordonnance. Ne pas re-traiter le
  compounding ; s'adosser à `incretines-glp1` pour l'étalon d'efficacité (ce qui marche
  vraiment, ~15-20 % du poids corporel) contre lequel le « 1-2 kg au mieux » prend son sens.
- **`cafeine-ergogene`** (candidat backlog, domaine `nutrition-sportive`) traitera la
  caféine comme **ergogène** (performance, 3-6 mg/kg, CYP1A2). → Ici, la caféine n'est vue
  que sous l'angle **thermogenèse et perte de poids**. Ne pas empiéter sur la performance.
- **`proteines-besoins-timing`** et **`creatine`** : hors sujet, aucun recouvrement.

## Piège de doctrine à surveiller sur ce thème

L'**argument du silence** (leçon du 30e run) est ici structurellement probable : sur des
molécules inefficaces, la littérature dit souvent « aucun effet indésirable rapporté »
dans des essais qui **ne mesuraient pas** la sécurité, et dont la durée (8-12 semaines) ne
peut de toute façon rien dire d'un usage chronique. Sur toute tournure « sans X rapporté »,
vérifier que le paramètre a été MESURÉ par la source.

Symétriquement, sur un sujet de debunking, le risque miroir est de conclure « ne marche
pas » là où la source dit « effet non significatif sur des essais sous-dimensionnés » —
absence de preuve contre preuve d'absence. Les deux formulations doivent rester distinctes
dans la prose.
