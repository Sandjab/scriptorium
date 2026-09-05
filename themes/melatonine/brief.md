# Mélatonine — brief de run

- **Slug** : `melatonine`
- **Domaine** : `complements-sante` (méta-domaine `sante-nutrition`)
- **Pipeline** : `/leanmonograph`, flag `"verdicts": true` (thème santé)
- **Lancé le** : 2026-09-04 — 52e run
- **Origine** : `docs/candidate-themes.md`, n° 5 de la table d'ordre révisée du 2026-09-01
  (« mot absent du corpus ; ouvre la cible sommeil qu'aucun domaine ne porte »)

## Angle

Une hormone vendue comme somnifère. Le pivot : **chronobiotique, pas hypnotique** — et
pourquoi la distinction commande tout (la dose et l'HEURE de prise décident du sens de
l'effet, ce qu'aucun étiquetage grand public ne dit).

## Périmètre

Ce qu'elle est · l'effet mesuré sur l'insomnie (latence d'endormissement vs temps total de
sommeil) · le décalage horaire (là où la preuve est la meilleure) · dose et heure (plus n'est
pas mieux ; courbe de réponse de phase) · formes à libération prolongée · enfants et TDAH
(usage massif, preuve étroite) · divergence réglementaire États-Unis / Europe / France ·
contenu réel des produits · sécurité, doses, interactions (section obligatoire) · ce que le
marketing « naturel » cache.

## Gap — vérifié PAR LECTURE le 2026-09-04 (corpus à 91 thèmes)

1. « Mélatonine », « chronobiotique », « décalage horaire », « jet lag » : **0 occurrence**.
2. « Circadien » : **1 seule occurrence** dans tout le corpus — `cafeine-cognition-vigilance`,
   claim:23, « les creux circadiens nocturnes », usage adjectival sous privation totale de
   sommeil. Le backlog annonçait 0 : la note était fausse, le verdict tient.
3. Aucun document ne traite d'un produit vendu **pour** dormir.

## Frontières à écrire

- `cafeine-cognition-vigilance` tient la privation de sommeil et la sieste → renvoyer.
  ⚠️ Son unique chiffre de sommeil (−34,67 min de temps total, +8,35 min de latence, méta-analyse
  de 22 essais) est porté par **claim:42, REJETÉ**. Ne pas s'y adosser.
- `nootropiques-stimulants-prescrits` prend le sommeil par l'autre bout (modafinil éveillant,
  travail posté, MSLT comme critère de réveil) → écrire la frontière, ne pas redérouler.
- `complements-amincissants` a posé le patron « contenu réel des gélules » → le citer.

## Doctrine de preuve

`docs/evidence-sante.md`, recopiée **intégralement** dans `args.subject` (les agents du pipeline
ne lisent pas le fichier — canal validé par le pilote `creatine`).

## Réserve sur le brief du backlog

Les chiffres qu'il propose (≈ 7 min de latence, −83 %/+478 % d'écart d'étiquette, Circadin 2 mg,
avis ANSES 2018) viennent de la mémoire du rédacteur, **sans balayage web**. Pistes de recherche,
jamais des faits : à corroborer en source primaire au Sweep, à retirer sinon.
