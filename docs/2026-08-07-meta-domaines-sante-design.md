# Design — Méta-domaines & lancement du méta-domaine Santé/nutrition

Date : 2026-08-07 · Statut : validé par JP (session du 07/08)

## Objectif

Ouvrir scriptorium à des monographies hors IA (nutrition sportive, compléments,
pharmacologie métabolique) en introduisant un **méta-niveau** au-dessus des domaines,
sans casser l'existant (URLs, pipeline, charte), et avec une **doctrine de preuve
durcie** pour les claims santé.

Décisions actées avec JP :
1. **Taxonomie v2 multi-pages** (home hub + une page par méta-domaine).
2. **3 domaines santé d'emblée** (sportif / compléments santé / pharmacologie métabolique).
3. **Hiérarchie de preuve durcie** pour tout claim d'efficacité ou de sécurité santé.

## 1. Méta-niveau — taxonomy.json v2

Schéma cible :

```json
{
  "version": 2,
  "meta_domains": [
    {
      "id": "intelligence-artificielle",
      "label": "Intelligence artificielle",
      "blurb": "…assume le socle algorithmique (sketches, ML classique)…",
      "domains": [ { "id": "...", "label": "...", "blurb": "...", "themes": ["..."] } ]
    },
    {
      "id": "sante-nutrition",
      "label": "Santé, nutrition & performance humaine",
      "blurb": "…",
      "domains": [ … ]
    }
  ]
}
```

- Les 6 domaines actuels passent **tels quels** (ids, labels, blurbs, ordre) sous
  `intelligence-artificielle`.
- **Site** : la home devient un hub à 2 cartes méta-domaines ; chaque méta-domaine
  reçoit sa page reprenant l'actuelle présentation groupée par domaine. Pages méta
  à la racine : `/<meta-id>.html` (ex. `sante-nutrition.html`) — pas de collision
  possible avec les thèmes, qui sont des dossiers.
- **Aucune URL existante ne bouge** : monographies en `<slug>/<slug>.html` à la
  racine, portails sous `/domaines/<id>.html`. Seul le contenu de la home change.
- **Fail-loud étendu** dans `build_site.py` : un thème dans exactement un domaine,
  un domaine dans exactement un méta-domaine, aucun niveau vide, ids uniques à tous
  les étages, version reconnue (v2) sinon échec bruyant.
- **Impacts périphériques** : le skill `/arrange` (mainteneur de `taxonomy.json` et
  de `tools/portals/*.json`) doit apprendre le niveau méta (classer un thème =
  méta-domaine → domaine → position). Les tests de `build_site` s'étendent au
  loader v2.

## 2. Les trois domaines santé

| id | label | périmètre | frontière |
|---|---|---|---|
| `nutrition-sportive` | Nutrition & supplémentation sportive | Performance, récupération, composition corporelle chez le sportif | vs `complements-sante` : finalité = performance, pas santé générale |
| `complements-sante` | Compléments & santé générale | Compléments en vente libre à visée santé/longévité | la berbérine vit ici (statut = complément), arête vers les GLP-1 (« Nature's Ozempic » à démonter) |
| `pharmacologie-metabolique` | Pharmacologie métabolique & perte de poids | La promesse minceur, du médicament efficace au complément inefficace : incrétines, amincissants OTC, peptides gris | vs `complements-sante` : finalité = perte de poids / intervention métabolique, quel que soit le statut du produit |

Déséquilibre de lancement assumé : `pharmacologie-metabolique` démarre à ~3 thèmes
(précédent : `ai-organizations` à 1).

## 3. Doctrine de preuve santé

Le « ≥ 2 sources indépendantes » du repo reste le **plancher**. En plus, pour tout
claim d'**efficacité ou de sécurité** :

- **≥ 1 source de rang fort** : méta-analyse, revue systématique, RCT publié, ou
  position de société savante (ISSN, Cochrane, EFSA, AND). Presse, blogs et sites
  de marques ne suffisent **jamais**, même à deux.
- **Dose et taille d'effet obligatoires** dans le claim (« 3-5 g/j de monohydrate,
  +X % sur 1RM en méta-analyse », pas « la créatine marche »).
- **Section « Sécurité, doses, interactions » systématique** dans le plan de
  sections de chaque monographie santé.
- **Indépendance `docKeys` renforcée** : un RCT + son communiqué de presse = 1
  source ; essais financés par l'industrie signalés comme tels.
- **Bandeau de non-conseil médical** sur toutes les pages du méta-domaine santé,
  injecté par le build (pas par la prose).

**Implémentation v1, volontairement lean** : la doctrine vit dans
`docs/evidence-sante.md` et est injectée dans le brief (« prompt riche ») de chaque
thème santé — **sans modifier les skills monograph**.

**Point ouvert (tranché par le run pilote)** : si les jurés du council n'appliquent
pas la hiérarchie transmise par le brief, câbler un champ doctrine dans le skill
(extension petite mais réelle).

## 4. Candidats au lancement (13)

**Pilote : `creatine`** — le complément le mieux documenté (position stand ISSN,
dizaines de méta-analyses) : calibre la doctrine avec le moins de risque de rejets
en masse.

- **`nutrition-sportive`** (5) : haute — créatine, protéines & timing (whey,
  leucine, « fenêtre anabolique ») ; moyenne — caféine ergogène, bêta-alanine &
  tampons ; basse — hydratation & électrolytes.
- **`complements-sante`** (5) : haute — berbérine, collagène ; moyenne —
  vitamine D, oméga-3 ; basse — magnésium.
- **`pharmacologie-metabolique`** (3) : haute — incrétines GLP-1 (sémaglutide,
  tirzépatide, rétatrutide), compléments amincissants (thé vert, CLA, carnitine,
  garcinia — sujet largement *debunking*, méta-analyses disponibles) ; moyenne —
  peptides « gris » (BPC-157, sécrétagogues GH) ⚠️ littérature mince et animale,
  haut taux de rejets attendu — **à garder pour quand la doctrine sera rodée**.

Les 6 sujets nommés par JP (créatine, berbérine, collagène, amincissants,
tirzépatide/peptides, nutrition sportive) sont tous couverts, les peptides gris
volontairement retardés.

## Ordre de mise en œuvre

1. Taxonomie v2 + `build_site.py` multi-pages + tests + extension `/arrange`
   (aucun nouveau contenu ; le site reste équivalent pour l'IA).
2. `docs/evidence-sante.md` + section santé dans `docs/candidate-themes.md`
   (prompts riches, doctrine incluse).
3. Run pilote `/leanmonograph creatine`, backstop renforcé, bilan doctrine.
4. Suite du backlog santé selon le bilan du pilote.

## Hors périmètre

- Retrofit de l'APO / `legacy/` (gelé, inchangé).
- Modification des skills monograph (v1 = doctrine par brief ; ne rouvrir qu'en
  cas d'échec constaté au pilote).
- Peptides gris avant rodage de la doctrine.

## Contraintes & risques annoncés

- Un run santé coûte comme un run IA : **6-8 M tokens, ~3-4 h** — 13 candidats =
  un programme, pas une session.
- Quota WebSearch 200/session inchangé (PubMed compris).
- Vérification du live : pièges connus (GoatCounter injecté par le CI, « Généré
  le … UTC » de la home) s'appliquent aussi aux nouvelles pages méta.
