# Design — Tableaux de verdicts du métadomaine santé

**Date** : 2026-08-13 · **Statut** : validé (brainstorming avec JP)

## Problème

Les monographies du métadomaine `sante-nutrition` (6 thèmes : creatine,
proteines-besoins-timing, collagene, incretines-glp1, berberine,
complements-amincissants) argumentent l'efficacité indication par indication dans
la prose, mais aucun endroit ne donne le verdict d'un coup d'œil : pour savoir si
« ça marche », le lecteur doit lire douze sections. Il manque un tableau simple à
lire — par complément/médicament, pour chaque indication discutée : efficacité
graduée, intervalle de confiance quand il existe, statut officiel, note ; plus la
sécurité et les effets indésirables de la substance.

## Décisions (validées une à une)

1. **Forme hybride, source unique** : un fichier structuré par thème, rendu deux
   fois — tableau dans la monographie ET page compilée du métadomaine. Une seule
   donnée, aucune divergence possible entre les deux vues.
2. **Note d'efficacité dérivée des claims confirmés + garde-fou build** : la
   gradation est une synthèse rédactionnelle de claims vérifiés (`confirmed`
   ou `corrected`) de
   `knowledge.json`, relue en passe d'exactitude ; `build.py` échoue si une ligne
   ne s'appuie pas sur du vérifié. Pas de conseil de jurés dédié, pas de
   gradations externes importées.
3. **Ligne = indication ; sécurité par substance** : un tableau par substance
   (les thèmes multi-substances comme complements-amincissants en ont plusieurs),
   bloc sécurité + effets indésirables sous chaque tableau, pas répété par ligne.
4. **Placement : juste après le résumé** dans la monographie.
5. **Séquencement : pilote creatine**, relecture, puis généralisation aux 5
   autres thèmes + page compilée + extension du workflow lean.

## 1. Modèle de données : `themes/<slug>/verdicts.json`

Nouvelle **vue structurée** sur `knowledge.json`, au même statut que le
manifeste : elle référence les faits par id, ne les recopie jamais.

```json
{
  "theme": "creatine",
  "substances": [{
    "id": "creatine-monohydrate",
    "label": "Créatine (monohydrate)",
    "safety":  { "status": "autorise", "label": "Autorisé (EFSA)", "claims": ["claim:8"] },
    "adverse": { "text": "Rétention d'eau ; troubles digestifs à forte dose", "claims": ["claim:9"] },
    "rows": [{
      "indication": "Force / masse musculaire",
      "efficacy": "bonne",
      "ci": "SMD 0,42 [0,18–0,66]",
      "official": "Claim EFSA autorisé",
      "note": "3–5 g/j en continu",
      "claims": ["claim:12", "claim:13"],
      "anchor": "creatine-force-hypertrophie"
    }]
  }]
}
```

- `efficacy` : enum fermée — `nulle`, `faible`, `modeste`, `bonne`, `tres-bonne`,
  `indeterminee`. `indeterminee` = « aucun essai exploitable », distinct de
  « démontré nul ».
- `safety.status` : enum — `autorise`, `interdit`, `restreint`, `pas-avis`.
- `ci` et `official` optionnels (souvent incalculable / sans avis rendu).
- `anchor` optionnel : id de la section de la monographie qui détaille la ligne
  (lien « voir la section »).

## 2. Garde-fous dans `build.py`

Extensions de `validate_refs`, échec bruyant dans tous les cas :

- Ligne, `safety` ou `adverse` **sans aucun claim id** → die.
- Claim id inexistant → die (comportement actuel, étendu à verdicts.json).
- Claim référencé dont `audit` n'est ni `confirmed` ni `corrected` → die
  (nouveau : le tableau ne s'appuie que sur du vérifié). `corrected` compte
  comme vérifié : c'est la sémantique du pipeline lean (`lint.py` garde
  confirmed+corrected, les manifestes référencent des claims corrected) — un
  claim corrected a un énoncé rectifié par les jurés, pas un énoncé douteux.
- `efficacy` ou `safety.status` hors enum → die.
- Élément `{"type": "verdicts"}` au manifeste sans `verdicts.json` → die ;
  `verdicts.json` présent sans élément au manifeste → die (aucun tableau perdu
  en silence).
- `anchor` ne correspondant à aucun id de section du manifeste → die.

## 3. Rendu

### Monographie

- Nouveau renderer `verdicts` dans `components.py` (pur, zéro jugement, comme
  les autres), enregistré dans `RENDERERS`.
- Élément `{"type": "verdicts"}` placé juste après `abstract` dans le manifeste.
- Une table par substance ; sous chaque table, bloc sécurité / effets
  indésirables.
- Pastilles d'efficacité et badges de statut stylés dans `charte.css` (source
  unique de style, pas de style par thème). Contraste AA vérifié **par le code**
  en thèmes clair et sombre (leçon charte-blue-deep).
- Tables dans un conteneur `overflow-x: auto` (jamais de scroll horizontal de
  page).

### Page compilée du métadomaine

- `build_site.py` agrège les `verdicts.json` des thèmes du métadomaine
  `sante-nutrition` en une page « Synthèse — efficacité et sécurité », liée
  depuis la page du métadomaine.
- **Caveat proéminent en tête** : réutilise la `notice` du métadomaine déjà
  présente dans `taxonomy.json` (ni avis médical ni recommandation
  individuelle) ; rappel court sous chaque tableau.
- Un thème sans `verdicts.json` n'y figure pas ; la page liste explicitement
  les monographies couvertes (pas de fausse exhaustivité).
- Chaque tableau lie vers sa monographie (et ses ancres de section).

## 4. Production du contenu et vérification

- Rétrofit : les notes et textes libres sont dérivés des claims vérifiés
  (confirmed/corrected) existants, rédigés **en lisant la monographie** (jamais au grep), sans
  nouvelle recherche web. Relecture d'exactitude après rédaction.
- Futurs runs santé : le workflow **lean** produit `verdicts.json` après le
  Council (au moment où les claims vérifiés sont connus). Les workflows
  monograph et frugal suivront dans une passe ultérieure, comme pour les
  durcissements précédents.

## 5. Tests (intention, pas seulement comportement)

Sous `tools/` pour la page compilée, à côté de `build.py` pour le reste :

- Une ligne de verdict sans claim vérifié (confirmed/corrected) fait échouer
  le build — c'est la
  doctrine « vérité non négociable » encodée en test.
- Une valeur d'`efficacy` hors enum fait échouer le build — ferme la porte aux
  gradations inventées.
- La page compilée sans caveat en tête fait échouer le test — l'exigence de
  non-avis-médical est structurelle, pas décorative.
- Un `verdicts.json` orphelin (sans élément au manifeste) fait échouer le
  build — aucun tableau ne disparaît en silence.

## 6. Séquencement

1. **Pilote creatine** : schéma + renderer + garde-fous + CSS + tests +
   `verdicts.json` + insertion au manifeste → rebuild → relecture par JP.
2. **Généralisation** : verdicts.json des 5 autres thèmes, page compilée dans
   `build_site.py` + tests, extension du workflow lean.
3. **Publication** : procédure habituelle (push main, diff live avec double
   neutralisation santé — GoatCounter + encart notice, balise + son seul `\n`).

## Hors périmètre

- Pas de rétrofit des thèmes non-santé (le modèle verdicts est propre au
  métadomaine `sante-nutrition`).
- Pas de nouvelle recherche ni de nouveaux claims : la donnée existante suffit ;
  si un trou factuel apparaît pendant le rétrofit (ex. aucun claim vérifié sur
  la sécurité d'une substance), la ligne porte `indeterminee`/`pas-avis` plutôt
  que d'inventer, et le trou est signalé à JP.
- Le `legacy/` reste gelé.
