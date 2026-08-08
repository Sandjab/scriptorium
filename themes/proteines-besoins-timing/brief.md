# Brief — proteines-besoins-timing

**Sujet** : Protéines et hypertrophie : besoins quotidiens, qualité, timing.

Deuxième thème du méta-domaine `sante-nutrition` (domaine `nutrition-sportive`), après le
pilote `creatine`. Priorité haute du backlog.

## Périmètre (cadrage du backlog, `docs/candidate-themes.md`)

- **Besoins quotidiens** : méta-analyses dose-réponse, plateau ~1,6 g/kg/j chez le
  pratiquant en résistance, plage haute jusqu'à ~2,2 g/kg/j — donner les intervalles de
  confiance et la plage COMPLÈTE des estimations, pas une borne.
- **Qualité** : whey vs caséine vs sources végétales ; seuil de leucine et réponse
  anabolique ; scores DIAAS/PDCAAS et ce qu'ils mesurent réellement.
- **Fenêtre anabolique** péri-entraînement : démystification chiffrée — l'apport TOTAL
  quotidien domine le timing.
- **Distribution des prises** : nombre de prises, dose par prise, effet plafond.
- **Protéines et perte de poids** : préservation de la masse maigre en déficit, satiété.
- **Sécurité, doses, interactions** (section obligatoire) : fonction rénale chez le sujet
  sain vs insuffisant rénal, os/calcium, apports très élevés, populations particulières.

## Délimitations (renvoyer, ne pas traiter)

- **créatine** : thème publié distinct — renvoyer.
- **collagène** (protéine incomplète, DIAAS ~0) : thème candidat distinct — renvoyer.

## Public

Lecteur exigeant **sans formation médicale** — définir chaque terme clinique à première
occurrence (synthèse protéique musculaire, bilan azoté, DIAAS, leucine, m-TOR…).

## Doctrine de preuve santé

Recopiée en bloc dans le `subject` du run (les agents ne lisent pas ce fichier).
Source : `docs/evidence-sante.md`. Résumé : hiérarchie des sources (fort = méta-analyse /
revue systématique / RCT / position de société savante — ISSN, Cochrane, EFSA, Academy of
Nutrition and Dietetics ; moyen = cohorte, essai ouvert, examine.com ; faible =
mécanistique/animal, ne prouve jamais un effet humain ; nul seul = presse/blogs/marques),
tout claim d'efficacité ou de sécurité exige ≥ 2 sources indépendantes dont ≥ 1 de rang
fort, dose ET taille d'effet obligatoires dans le statement (plage complète, pas une
borne), indépendance = travaux distincts, financement industriel signalé dans l'audit du
claim (fréquent sur les protéines en poudre), section « Sécurité, doses, interactions »
obligatoire, aucun disclaimer médical dans la prose (porté par la clé `notice` du
méta-domaine côté site).
