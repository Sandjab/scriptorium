# Brief — HyperLogLog

HyperLogLog (HLL) : estimation probabiliste de **cardinalité** (nombre d'éléments distincts) sur
un flux, en mémoire **quasi constante** (kilo-octets pour des milliards d'éléments) au prix d'une
erreur relative bornée. L'angle directeur est le découplage **comptage exact ≠ comptage utile** :
on échange une précision parfaite (coûteuse, O(n) mémoire) contre une estimation à erreur
contrôlée en O(log log n) — d'où « LogLog ».

## Cadrage
Document de référence best-of, en français, niveau technique. Le fil rouge est l'**intuition des
zéros de tête** : hacher chaque élément, observer la statistique du plus long préfixe de zéros, et
en déduire l'ordre de grandeur de la cardinalité ; tout le reste (registres, moyenne harmonique,
corrections de biais) s'y rattache. Le document s'insère dans la famille « structures
probabilistes & hachage » du scriptorium, à côté de `bloom-filters` et `minimal-perfect-hashing`,
qu'il suppose connus à titre de contraste et auxquels il renvoie plutôt que de les ré-exposer.

## Périmètre à couvrir
- Problème : count-distinct exact = O(n) mémoire (set/hashtable) ; HLL = estimation en mémoire
  bornée, mergeable, sur flux et en une passe.
- Intuition : hachage uniforme → observation du nombre de zéros de tête (leading zeros) ;
  le maximum observé ≈ log2(cardinalité). Stochastic averaging via m registres (buckets) indexés
  par les premiers bits du hash.
- Lignée à corroborer (≥2 sources indépendantes par fait) : Flajolet–Martin (1985) →
  LogLog (Durand–Flajolet 2003) → **HyperLogLog (Flajolet, Fusy, Gandouet, Meunier 2007)** →
  HLL++ (Heule, Nunkesser, Hall, Google 2013 : représentation sparse, correction de biais,
  hash 64 bits).
- Estimateur : moyenne **harmonique** des 2^registre, constante de biais α_m ; corrections aux
  régimes extrêmes (small-range / linear counting, large-range).
- Précision & coût : erreur standard ≈ 1.04/√m ; ex. m = 2^14 = 16384 registres → ≈ 0,81 %
  d'erreur pour ≈ 12 Ko (chiffres à vérifier en sources).
- Propriétés algébriques : **union** par max registre-à-registre (mergeable, idempotente,
  ordre-insensible) ; pas d'intersection directe (inclusion-exclusion, perte de précision) ;
  pas de suppression.
- Instances réelles à corroborer : Redis (PFADD/PFCOUNT/PFMERGE, 12 Ko, 0,81 %), Google BigQuery
  (APPROX_COUNT_DISTINCT, HLL++), Presto/Spark, Apache DataSketches.
- Trade-offs et limites : biais aux petites cardinalités, dépendance à la qualité de la fonction
  de hachage (dispersion uniforme), absence de comptage exact, erreur **relative** ~constante.

## Frontières (ne pas ré-exposer ; renvoyer aux thèmes voisins)
- DISTINGUER explicitement HLL d'un **filtre de Bloom** (thème `bloom-filters`) : Bloom répond à
  l'**appartenance** (membership) d'un élément, HLL estime la **cardinalité** d'un ensemble ;
  problèmes différents, garanties différentes.
- Hachage minimal parfait (`minimal-perfect-hashing`) et hachage cohérent (`consistent-hashing`) →
  autres usages du hachage (indexation compacte, placement/routage) ; HLL utilise le hachage pour
  **disperser uniformément**, pas pour indexer ni router — renvoyer sans ré-exposer.
- Théorie analytique de la combinatoire (analyse asymptotique fine de l'estimateur) → mentionnée,
  pas démontrée : on privilégie l'intuition opérationnelle et les chiffres vérifiables.
