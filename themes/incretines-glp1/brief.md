# Brief — incretines-glp1

**Sujet** : Agonistes des incrétines : sémaglutide, tirzépatide, rétatrutide.

Troisième thème du méta-domaine `sante-nutrition`, **premier du domaine
`pharmacologie-metabolique`** (domaine à créer par `/arrange` après le build), après
`creatine` et `proteines-besoins-timing` (domaine `nutrition-sportive`). Priorité haute
du backlog.

⚠️ **Première monographie santé portant sur des MÉDICAMENTS sur ordonnance**, et non sur
des compléments en vente libre. Le cadrage ci-dessous en tire les conséquences.

## Périmètre (cadrage du backlog, `docs/candidate-themes.md`)

- **Physiologie incrétine** : effet incrétine, GLP-1 et GIP, sécrétion post-prandiale,
  demi-vie native et pourquoi une modification structurale est nécessaire ; effets
  centraux (satiété) vs périphériques (insulinosécrétion glucose-dépendante, vidange
  gastrique).
- **Efficacité, tailles d'effet exactes** : programmes STEP (sémaglutide, ~15 % de perte
  de poids) et SURMOUNT (tirzépatide, ~20 % — double agonisme GIP/GLP-1), avec les bras
  **placebo**, les durées, et la **plage complète** des estimations selon les essais et
  les doses (pas une borne, pas un seul chiffre vitrine). Diabète de type 2 (SUSTAIN,
  SURPASS) distingué de l'obésité. Résultats cardiovasculaires (SELECT) traités comme
  un critère distinct de la perte de poids.
- **Pipeline** : rétatrutide (triple agoniste GLP-1/GIP/glucagon) — **dire explicitement
  le stade de développement** (phase 2/3) et ne jamais présenter ses résultats au même
  rang qu'un produit autorisé.
- **Effets indésirables** : gastro-intestinaux (fréquences chiffrées, taux d'arrêt),
  perte de masse maigre (part de la perte totale — chiffres et méthode de mesure),
  débats pancréatite / cancer médullaire de la thyroïde (état réel de la preuve,
  signaux animaux vs humains), gastroparésie, hypoglycémie en association.
- **Regain à l'arrêt** : extension STEP 1 — ampleur et cinétique du regain, ce que cela
  implique sur la durée de traitement.
- **Accès** : coût, pénuries, préparations magistrales (« compounding ») et marché gris
  — **décrire le phénomène et ses risques documentés (erreurs de dosage, produits non
  conformes, alertes d'agences), SANS mode d'emploi d'approvisionnement** : aucune
  source d'achat, aucun protocole de reconstitution ou d'auto-titration.

## Cadrage de sécurité propre au thème

- Les doses citées sont des **doses d'essai ou d'AMM**, présentées comme telles ; la
  monographie ne fournit pas de schéma d'auto-administration.
- La section « Sécurité, doses, interactions » (obligatoire) mentionne explicitement la
  prescription et le suivi médical comme cadre d'usage — sans faire office de conseil
  (le bandeau non-conseil est porté par la clé `notice` du méta-domaine, jamais écrit
  dans la prose).

## Délimitations (renvoyer, ne pas traiter)

- **berberine** (candidat) : le « Ozempic naturel » — le faux équivalent ; arête attendue,
  ne pas traiter ici.
- **complements-amincissants** (candidat) : contraste d'efficacité OTC vs incrétines —
  arête attendue, ne pas traiter ici.
- **proteines-besoins-timing** (publié) : préservation de la masse maigre en déficit —
  renvoyer pour le versant nutritionnel.

## Public

Lecteur exigeant **sans formation médicale** — définir chaque terme clinique à première
occurrence (incrétine, agoniste, glucose-dépendant, vidange gastrique, HbA1c, critère
composite MACE, phase 2/3, insulinorésistance…).

## Doctrine de preuve santé

Recopiée en bloc dans le `subject` du run (les agents ne lisent pas ce fichier).
Source : `docs/evidence-sante.md`. Résumé : hiérarchie des sources (fort = méta-analyse /
revue systématique / RCT publié en revue à comité de lecture / position de société
savante — également ici : notices d'AMM et rapports d'évaluation FDA/EMA ; moyen =
cohorte, essai ouvert, registre ; faible = mécanistique/animal, ne prouve jamais un effet
humain ; nul seul = presse/blogs/marques/influenceurs), tout claim d'efficacité ou de
sécurité exige ≥ 2 sources indépendantes dont ≥ 1 de rang fort, dose ET taille d'effet
obligatoires dans le statement (plage complète, pas une borne), indépendance = travaux
distincts (un essai + son communiqué = 1 source ; deux essais du même sponsor = à
signaler), **financement industriel signalé dans l'audit du claim — ici il est la norme
et non l'exception** (Novo Nordisk sur STEP/SUSTAIN/SELECT, Eli Lilly sur
SURMOUNT/SURPASS et le rétatrutide), section « Sécurité, doses, interactions »
obligatoire, aucun disclaimer médical dans la prose.

## Réflexe de vérification hérité du run précédent

**L'argument du silence** (correction dure du 30e run) : sur toute tournure « sans effet
X rapporté » / « aucun signal observé », vérifier que le paramètre X a été **mesuré** par
la source citée — une absence d'examen n'est pas une absence d'effet. Particulièrement
exposé ici : pancréas, thyroïde, densité osseuse, santé mentale.
