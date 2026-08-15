# Brief — masse-maigre-sous-glp1

> ⚠️ Ce fichier documente le cadrage pour un lecteur humain. **`workflow.js` ne le lit pas** :
> tout ce qui doit atteindre les agents est recopié dans `args.subject` au lancement.

**Domaine visé** : `pharmacologie-metabolique` (4e thème — ferme la gradation par le haut).
**Pipeline** : `/leanmonograph`, `verdicts: true` (thème santé).
**Fiche d'origine** : `docs/candidate-themes.md`, § `pharmacologie-metabolique`.

## Le sujet en une phrase

Préserver la masse maigre sous agonistes des incrétines : ce que change ce qu'on **ajoute** au
traitement — et ce qu'exige la démonstration d'une potentialisation.

## Pourquoi ce thème

`incretines-glp1` établit la contrepartie (environ trois quarts de graisse et un quart de
« tout le reste » sous tirzépatide ; jusqu'à 6,4 kg de masse maigre sous rétatrutide 12 mg), puis
**renvoie explicitement ailleurs** ce qui pourrait la limiter : « apports protéiques, entraînement
en résistance sous déficit énergétique — relève du versant nutritionnel, traité ailleurs dans ce
corpus et non repris ici ». Ce n'est traité nulle part. Un renvoi vers un document inexistant est
le signal de gap le plus fiable dont ce corpus dispose.

C'est aussi la **première monographie d'interaction** du corpus : une potentialisation ne se
démontre que par un plan add-on ou factoriel (le maître seul, l'ajout seul, les deux).

## Fil rouge

La potentialisation existe, elle coûte un anticorps monoclonal de phase 2, et le rayon qui vend
le mot n'a pas un seul bras de randomisation.

## Frontières (ne pas refaire)

| Voisin | Ce qu'il couvre déjà |
|---|---|
| `incretines-glp1` | pharmacologie des maîtres, tailles d'effet, arrêt, marché gris, tolérance |
| `proteines-besoins-timing` | besoin protéique du sujet entraîné en surplus ou à l'équilibre |
| `complements-amincissants` | verdict du rayon minceur en monothérapie, graduation FDA/GLP-1 |
| `peptides-gris` | sécrétagogues GH du marché gris |

## Pistes à corroborer au sweep (PAS des faits acquis)

Recherche web du 2026-08-15, à re-vérifier en source primaire : BELIEVE (bimagrumab +
sémaglutide, n ≈ 507), EMBRACE (apitegromab + tirzépatide, n ≈ 102, *Nature Medicine* 2026),
COURAGE (trevogrumab + sémaglutide, 26 sem.), LEAN-PREP (protocole RCT protéines + résistance),
NICE TA1026 (complément aux apports de référence si apport insuffisant).

## Réflexes de vérification hérités des runs précédents

- **Argument du silence** (30e run) : sur toute tournure « sans X rapporté » / « aucun effet
  observé », vérifier que le paramètre a été MESURÉ par la source.
- **Fausse plage par agrégation de compartiments** (32e run) : deux compartiments de mesure
  fusionnés en une plage. Signal d'alarme : « respectively » dans la source. Ici le risque est
  maximal — AUC vs Cmax, DXA vs impédancemétrie, masse maigre vs muscle appendiculaire.
- **Fausse indépendance par scission de source** (33e run) : comparer effectifs et valeurs
  secondaires avant de croire deux séries « indépendantes ».
- **Rejet qui jette la correction du juré** (37e run) : après le run, lire les notes des jurés
  des claims rejetés en cherchant `holds=false` AVEC une correction.
- **Un protocole de « stack » n'est jamais une source** (fiche de backlog) : objet à décrire.
