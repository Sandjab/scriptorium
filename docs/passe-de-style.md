# Passe de style — rendre la prose lisible sans toucher aux faits

Chantier ouvert le 2026-09-03. **80 documents traités sur 90.** File d'attente et procédure
ci-dessous ; l'outillage est `.claude/skills/monograph/scripts/restyle.py`, le contrôle en
continu est le check `prose_style` de `.claude/skills/leanmonograph/scripts/lint.py`.

## Pourquoi

Mesure sur les 90 documents publiés, avant la passe : **30,7 mots par phrase en moyenne**,
un tiers des phrases au-dessus de 35 mots, une sur six au-dessus de 45, la plus longue à
175. Un régime auquel un document se relit mal, sans qu'aucun fait y soit en cause.

La cause est structurelle : une phrase qui tente de porter à la fois le résultat, son
attribution, sa population et sa réserve. Le remède ne coûte aucun fait — **on répartit, on
ne coupe pas**. Une phrase-liste redevient une liste, une incise qui porte un fait autonome
redevient une phrase.

Vérifié sur ce qui est déjà fait : les documents perdent entre 0 et 1 % de leurs mots, et
ce sont des liaisons devenues inutiles.

## La fabrique est fermée

Inutile de repasser derrière les runs futurs : `lint.py` mesure `prose_style` par section
(médiane, moyenne, part de phrases > 45 mots, la plus longue) et liste les sections
au-dessus des seuils (médiane > 22, ou > 8 % de phrases > 45). Il **signale sans bloquer** —
la lisibilité n'est pas une question de vérité, un document exact mais lourd doit sortir.
La clause RYTHME de la charte de voix (`leanmonograph/workflow.js`) est chiffrée, et
l'Audit-prose a sa consigne de découpage.

## Procédure par document

1. `restyle.py snapshot themes/<slug> /tmp/restyle/<slug>/avant` — le témoin vient de
   `git show HEAD:` et emporte knowledge, tldr, glossary ET widgets.
2. `lint.py /tmp/restyle/<slug>/avant > .../lint.AVANT.json` — code de sortie lu **sans
   tube**.
3. `restyle.py dump themes/<slug> <ids de sections>` — section par section.
4. Par lot : patch JSON `{"<élém>.<par>": "<contenu du <p>>"}` → `restyle.py apply` →
   `restyle.py check themes/<slug> /tmp/restyle/<slug>/avant/manifest.json`.
5. `lint.py themes/<slug>` — comparé champ par champ au rapport d'avant, hors `prose_style`
   et hors le champ `context` (qui change mécaniquement).
6. `build.py themes/<slug>`.

Le `check` porte six invariants. **Bloquants** : le multiensemble des nombres, celui des
nombres écrits en toutes lettres, et `id`/`type`/`claims`. **Signalés, à adjuger** : un nom
propre en baisse, un sigle apparu, une insécable collante perdue.

Un septième contrôle vaut d'être ajouté à la main, il est gratuit : **le manifeste privé de son
champ `prose` doit être identique à celui du témoin**. Le `check` ne compare `id`/`type`/`claims`
que par élément, pas les champs voisins.

```
def strip(o):
    if isinstance(o, dict): return {k: strip(v) for k, v in o.items() if k != 'prose'}
    if isinstance(o, list): return [strip(v) for v in o]
    return o
strip(avant) == strip(apres)
```

Le comparer **en JSON**, pas en comptant les lignes de `git diff` : `restyle.py apply` écrit un
saut de ligne final que 23 manifestes du corpus n'ont pas, et le diff montre alors un `}` d'un
octet qui n'est rien. La comparaison JSON ne s'y laisse pas prendre.

## Les dix-neuf pièges déjà payés

1. **Témoin incomplet.** Le lint en mode post lit manifest + knowledge + tldr + glossary +
   `widgets/`. Il manquait `tldr.json` une fois, `widgets/` une autre : deux fausses alertes
   de régression dans la même journée. D'où `snapshot`, qui ne se construit plus à la main.
   Les widgets ne sont scannés que pour `rejected_flags` : leur absence ne peut fausser que
   ce champ.
1bis. **La comparaison des lints n'est pas un rituel : elle a attrapé une VRAIE régression.**
   Sur ejaculation-precoce, déplacer « source unique, non corroborée » en phrase autonome a
   porté la réserve de 315 à 387 caractères de son pivot, et fait basculer `claim:35` de
   `hedged: true` à `false`. Un document de santé y perdait sa réserve sans qu'aucun mot ne
   disparaisse. Réparé avant remise (distance finale 29 c.). C'est le seul contrôle qui l'a vu,
   sur quarante-neuf documents.
2. **`snapshot` reconstruit depuis HEAD.** Linter un « snapshot après » rend un rapport
   identique à l'avant et fait croire que rien n'a bougé. Le lint APRÈS se lance sur le
   thème lui-même.
3. **`unhedged_count` ne doit ni monter NI BAISSER.** Une baisse signifie qu'une réserve a
   été ajoutée — un écart au même titre qu'une perte. La consigne dit « identique », pas
   « meilleur ».
4. **Les noms qui portent un chiffre ne se répètent pas librement.** « CoAct-1 », « Mem0 »,
   « GPT-4 » : les répéter ajoute un nombre au multiensemble et bloque. Le pronom est alors
   correct, à condition que le nom figure dans la phrase voisine.
5. **Un quantifieur ajouté est un écart.** Écrire « ces trois familles » là où l'original ne
   l'écrivait pas duplique un nombre en toutes lettres. Reformuler sans quantifieur.
6. **Les marqueurs d'énumération `(1)`, `(2)` sont des nombres**, donc insupprimables, et
   ouvrir une phrase sur une parenthèse prive le découpeur de sa majuscule. La sortie
   trouvée indépendamment par trois agents : « Étape (1) : … ».
7. **Le découpeur n'ouvre une phrase que sur une majuscule ou un guillemet.** Une phrase
   commençant par « o3 confirme » ou « 92,82 % » se fond dans la précédente et fausse la
   mesure sans gêner personne. Reformuler, et le signaler.
8. **Une réserve reste à moins de 350 caractères de son chiffre**, sinon `HEDGE_RE` du lint
   ne la voit plus. **Limite de la mesure, vue sur nootropiques-stimulants-prescrits** : la
   distance se compte jusqu'au CHIFFRE le plus proche, or une réserve peut qualifier un
   résultat purement qualitatif (« les bas performeurs s'améliorent significativement ») et
   se trouver à 420 caractères du premier chiffre tout en étant collée à ce qu'elle qualifie.
   Elle est alors correcte en prose et invisible au lint, indépendamment de toute passe.
   Mesurer avant de corriger : ici elle était déjà à 414 c. dans le témoin.
9. **La médiane du `check` et celle du lint ne mesurent pas la même chose.** Le lint mesure
   aussi le tldr et le glossaire, que la passe ne touche pas : sa médiane peut rester un
   point sous celle du `check`. Le plancher de 16 s'apprécie sur le `check`, qui ne voit que
   la prose réécrite. Vu sur bm25-inverted-index, à 18 au `check` et 17,0 au lint.
10. **Aucun contrôle ne mesure l'ORDRE des phrases ni la direction d'un verbe.** Deux défauts
   ont passé les six invariants et les six champs de lint : une explication séparée de ce
   qu'elle explique (ia-productivite-esn, l'aveu des auteurs détaché des « signaux
   indirects »), et « le porte à 2,9 % » pour un taux qui BAISSE de 3,7 à 2,9
   (retrieval-augmented-generation). Aucun fait n'était faux, la phrase l'était. Relire la
   prose reste le seul contrôle qui les attrape — et un rapport d'agent peut affirmer le
   contraire de ce qu'il a fait : celui d'ia-productivite-esn annonçait avoir rapproché
   toutes les réserves du pivot, il en avait éloigné une de 257 à 476 caractères.
11. **`grep -c` rend le VIDE, pas zéro, sur un `dist/` qu'il juge binaire.** Le compte de
   `<h3>` de text-embeddings n'a rien affiché — ni 14, ni 0 — et ce vide se lit comme
   « rien à signaler ». Compter avec `grep -ac`. Variante de « la chose, ou un proxy ? ».
12. **Un sigle porteur de chiffre COLLÉ à un nombre ne forme qu'un jeton.** Le tokeniseur lit
   « FP8 2,6 » comme UN nombre : retirer le sigle en écrivant « une erreur numérique 2,6× plus
   faible » déplace le multiensemble et bloque. Symétrique du piège 4 — un tel nom ne se répète
   pas librement, il ne se retire pas librement non plus.
13. **Vérifier un thème SANTÉ par inventaire de vocabulaire, jamais par le lint.** Sur
   peptides-gris, `unhedged_count` valait 0 pour UN seul flag : il ne prouvait rien de cinq
   réserves déplacées. Compter terme à terme, **sans sensibilité à la casse**, les « aucun essai »,
   « source unique », « non corroborée », les populations (chez le rat, sujets âgés) et les
   statuts réglementaires. Une population perdue ne fait bouger aucun compteur.
14. **Une recherche littérale accuse à tort quatre fois sur quatre.** Casse changée par un passage
   en tête de phrase (« aucun essai » → « Aucun essai »), incise devenue relative (« — score SPPB
   de 3 à 7 — » → « dont le score SPPB va de 3 à 7 »), terme cédant la place à sa glose française
   (« hazard ratio » → « ce rapport des risques instantanés »). Chercher la valeur et le contexte,
   pas la chaîne ; et lire le passage avant de conclure à une perte.
15. **Ne jamais RÉIMPLÉMENTER un contrôle : l'importer.** Une copie manuelle de la regex
   `STICKY_RE` a compté 145 insécables au lieu de 19 sur structured-extraction-llm, et
   annonçait une perte inexistante. `importlib` charge `restyle.py` en trois lignes, et
   `sticky_nbsp` / `proper_nouns` répondent juste. Même famille que le piège 11 : l'outil de
   vérification est ce qui ment en premier.
16. **Une réécriture peut AJOUTER une fausse réserve — le miroir exact du piège 1bis.** Sur
   backpropagation, retirer le méta-discours « tient en un mot » a produit « L'efficacité de la
   backpropagation **a une source unique** : la réutilisation ». La chaîne est le premier motif
   de `HEDGE_RE` : une réserve bibliographique fantôme, plantée sur une section qui porte quatre
   claims. Sans effet ce jour-là — les rejets vivaient ailleurs, aucun compteur n'a bougé — mais
   il suffisait qu'un rejet y tombe pour qu'il se déclare hedgé tout seul. **Le diff de
   vocabulaire ne peut pas le voir : c'est un mot AJOUTÉ, pas perdu.** Seule la lecture l'attrape.
   Contrôle gratuit à ajouter : compter les occurrences de `HEDGE_RE` dans la prose avant et
   après, et comparer les DEUX ensembles — pas seulement leur nombre.
17. **Déplier un « respectivement » peut inverser un appariement, sans bouger un seul nombre.**
   Sur hyperloglog : « pour m = 2 048, σ ≈ 2,3 % ; pour m = 16 384, σ ≈ 0,8 %, pour
   **respectivement** environ 1,25 Ko et 10 Ko ». Attribuer 10 Ko aux 2 048 registres écrit un
   fait FAUX en laissant le multiensemble des nombres **rigoureusement identique** — donc
   `check` vert, lint vert, diff de vocabulaire vide. Même exposition pour toute série appariée :
   les constantes α_m par valeur de m, une incertitude absolue par cardinalité, trois doses et
   leurs trois effets. Quand une phrase apparie deux listes, **relire l'appariement terme à
   terme contre le témoin** est le seul contrôle qui existe. Sous-cas du piège 10, mais celui-là
   se repère à une construction nommée : `respectivement`, `l'un… l'autre`, `dans l'ordre`.
   **Complément mécanisable, gratuit** : compter le multiensemble de ces marqueurs avant et
   après. Il ne dit rien de l'ordre des termes, mais il attrape le cas où une réécriture
   *introduit* une construction appariante là où l'original n'en avait pas — un appariement
   neuf est une cible neuve pour la passe suivante. Vérifié sur les quatre documents de la
   treizième vague : 6/6, 1/1, 1/1, 1/1, aucun marqueur ajouté.
   ⚠️ **Le cas limite est le CHIASME**, où l'anaphore inverse l'ordre d'énonciation. Sur
   nootropiques-panorama : « Le sunifiram et le piracétam partagent l'étiquette « nootrope »… :
   **le second** est un médicament sous AMM…, **le premier** n'a jamais rencontré un être humain. »
   Résolu à l'envers, cela ferait du sunifiram — une molécule sans le moindre essai humain — un
   médicament autorisé, avec un multiensemble de nombres inchangé. Ne jamais résoudre une
   anaphore sur l'ordre apparent : **remonter à la phrase qui nomme les termes** et vérifier le
   rattachement un par un. L'agent l'a fait, et il avait raison.
18. **Une réécriture peut introduire une FAUTE DE SAISIE, qu'aucun contrôle du dispositif ne
   voit.** Sur agentic-rl-environments, « avec l'ambition affichée que chacun puisse » est
   devenu « avec cette ambition affichée : **que que** chacun puisse ». Un mot doublé passe le
   `check` (aucun nombre ne bouge), passe le lint, et passe le diff de vocabulaire — « que »
   est trop fréquent pour qu'une occurrence de plus se remarque dans le bruit. Il serait parti
   en ligne. **Contrôle gratuit** : balayer `\b(\w+)\s+\1\b` sur la prose réécrite et
   soustraire les doublons DÉJÀ présents dans le témoin — les labels de schéma en portent
   légitimement (`r_sub r_sub`). Seuls les doublons *introduits* comptent. Vérifié ensuite sur
   les trois autres documents de la quatorzième vague : aucun.
19. **Une MAJUSCULE en tête de phrase peut FABRIQUER un flag de vérité.** Sur
   llm-safety-jailbreaks, découper à « **Contre** Claude-2, ils ne réussissent que… » a fait
   passer `unhedged_count` de 6 à 7 et apparaître un `rejected_flag` neuf : le mot figure dans
   les `examples` du claim rejeté, il fait six caractères, et le lint l'a retenu comme pivot à
   lui seul. Réparé en gardant « contre » en minuscule et en milieu de phrase. C'est le
   symétrique du piège 7 : là, un token minuscule en tête de phrase FAUSSE LA MESURE de
   longueur ; ici, un mot ordinaire capitalisé FABRIQUE une alerte de vérité. Le contrôle
   existe déjà — c'est la comparaison des six champs de lint —, à condition de la lancer après
   CHAQUE lot et pas seulement à la fin. ✅ **Reproduit et pris en direct à la dix-septième
   vague** : sur ia-competences-deskilling-apprentissage, découper sur « **Puisque** » a fait
   monter `unhedged_count` de 8 à 9 avec un `rejected_flag` neuf sur ce mot devenu pivot ;
   restauré au tiret d'origine dans le lot suivant. La consigne par lot fonctionne. Une refusion, elle, ne peut que désamorcer ce piège :
   elle supprime des majuscules initiales, elle n'en crée pas.

20. **Aplatir une parenthèse ou une paire de tirets cadratins change le RANG d'un élément dans
   une énumération.** Deux prises dans le même document, world-models, invisibles à tous les
   invariants. Sortir la glose du tokenizer de sa parenthèse a placé « Sa singularité tient dans
   ce **troisième** bloc » juste derrière une phrase portant sur le premier. Aplatir les tirets
   autour de « MPPI — un autre solveur de commande prédictive — » en faisait un **quatrième**
   solveur d'une liste qui en compte trois. Aucun nombre ne bouge, aucun mot ne disparaît : c'est
   le RANG qui devient faux. Sous-cas nommé du piège 10, et il se cherche : partout où la
   réécriture retire une parenthèse ou des tirets à l'intérieur d'une énumération ou juste avant
   un ordinal, relire le rang. ✅ **Confirmé à la vague suivante, par l'agent qui l'avait dans son
   prompt** : sur gpu-kernels-compilers, aplatir « — par l'intermédiaire de PyTorch/XLA — » en
   virgule faisait de la glose un QUATRIÈME consommateur d'OpenXLA à côté de JAX, TensorFlow et
   PyTorch. Le piège se cherche, et une fois cherché il se trouve.

## Ce qui marche, et qu'il faut redemander

- **Travailler par substitutions vérifiées** (`count(old) == 1`, sinon arrêt) plutôt qu'en
  retapant le paragraphe. Les formules, `<sup>`/`<sub>` et `&nbsp;` ne transitent alors
  jamais par une saisie manuelle. Méthode apparue chez un agent, reprise par les suivants.
- **Re-nommer le sujet** quand une incise attributive devient une phrase (« Jamba offre… »,
  pas « Il offre… ») — sauf cas 4 ci-dessus. C'est ce qui fait disparaître les cas à adjuger.
- **Plancher de 16 mots de médiane, mais consigne de viser 20.** Sous 16 la prose devient
  télégraphique ; trois agents ont dû refusionner des coupes trop sèches pour y remonter.
  Rendre à 18 est conforme et pourtant plus sec que le corpus — vu sur
  hallucination-detection-uncertainty, sorti à 18 avec trois sections à 17. Demander
  explicitement le MILIEU de la bande a suffi : les quatre documents de la douzième vague
  sont sortis entre 19 et 20,2, tous après une passe de refusion assumée.
- **Comparer la SUITE ORDONNÉE des nombres, pas seulement leur multiensemble.** Trouvé par un
  agent au quinzième run, et plus fin que le contrôle du `check` : une permutation laisse le
  multiensemble intact. Sur testosterone-homme-age, la comparaison ordonnée élément par élément
  a isolé exactement deux réordonnancements sur 34 nombres — tous deux voulus, tous deux relus.
  ⚠️ Détacher la ponctuation finale avant de comparer, sinon « 2008. » et « 2008 » divergent
  pour rien.
- **Quand une phrase appariante se découpe, NOMMER les termes plutôt que garder l'anaphore.**
  Sur distributed-training-parallelism, « les premières profitent d'un tensor parallelism élevé,
  les secondes réclament un expert parallelism » est devenu « Les couches d'attention profitent…
  Les couches d'experts réclament… ». Le fait est le même, mais le risque d'inversion disparaît
  pour de bon : plus aucune passe future ne peut se tromper de référent. C'est la seule
  réparation du piège 17 qui soit définitive plutôt que ponctuelle.
- **`pct_over_45` n'a pas à valoir 0 : le seuil est 8 %.** Quatorze documents de rang sont
  sortis à 0 %, ce qui a fini par passer pour la norme. Les deux thèmes santé de la seizième
  vague rendent 3,5 % et 2,4 %, et c'est correct : les phrases restantes, de 46 à 56 mots, sont
  des descriptions de protocole d'essai — population, dose, durée, comparateur, financement —
  qu'on ne fragmente pas sans perdre la cohérence. Un agent qui avait d'abord surcoupé à médiane
  15 / max 32 est remonté de lui-même. Exiger 0 % reproduirait le défaut sanctionné à la
  quinzième vague.
- **Un appariement qui porte un RAPPORT s'adjuge par l'arithmétique, pas par l'ordre
  apparent.** Le cas le plus exposé de la dix-septième vague est en guardrails-conception, où
  l'ordre des termes s'inverse entre deux phrases voisines : « Le gain de pratique du premier
  vaut 2,6 fois celui du second ». Les nombres tranchent seuls — 0,361 / 0,137 = 2,6 et
  0,004 / 0,054 ≈ 1/13 rattachent le « premier » au bras contraint sans qu'on ait à parier sur
  l'ordre d'énonciation. Quand le texte donne le ratio, il donne aussi la clé de son propre
  appariement : la vérifier coûte une division.
- **Compter les marqueurs d'appariement OCCURRENCE PAR OCCURRENCE, jamais en net.** Un
  multiensemble comparé par clé masque une disparition compensée par un ajout ailleurs :
  « le premier » à 4 avant et 4 après peut cacher un marqueur résolu ici et un marqueur
  fabriqué là. Sur collagene, seule la liste des 25 occurrences de `premier`/`second` avec leur
  contexte, avant et après, a prouvé que les trois disparitions étaient bien les trois anaphores
  résolues et qu'aucune n'était réintroduite. ✅ **Il a payé dès la vague suivante** : sur
  agent-evaluation-observability, l'agent s'est vu introduire « À l'autre bout » et l'a retiré
  avant remise, alors que ses marqueurs passaient de onze à sept — un compte net aurait tenu le
  total et n'aurait rien montré.
- **Un document peut GAGNER des mots, et c'est bon signe.** La règle « entre 0 et 1 % de mots
  perdus » vaut pour la répartition seule. Nommer les termes d'une anaphore appariante en coûte :
  collagene gagne 7 mots, ia-competences-deskilling-apprentissage en gagne 41. C'est le prix de
  la seule réparation définitive du piège 17 — ne pas le lire comme une anomalie, et ne surtout
  pas le corriger en re-pronominalisant.

- **Un ordinal immédiatement suivi de son contenu n'est PAS un appariement à risque.** La règle
  « n'introduis aucun marqueur » vise l'anaphore qu'il faut résoudre à distance, pas l'ordinal
  d'une énumération qui porte son terme dans la même phrase (« La première exemption est l'œuvre
  artistique… La seconde est le texte relu »). Rien n'y est à résoudre, donc rien ne peut s'y
  inverser. Le compte mécanique des marqueurs signale une introduction **pour la faire LIRE**,
  il ne la condamne pas. En revanche le marqueur devient inutile — donc à retirer — quand les
  reprises lointaines viennent d'être nommées : sur llm-watermarking-detection, la découpe avait
  posé « Le premier réunit 91 copies… Le second réunit 88 copies… » alors que les deux reprises
  étaient déjà devenues « Sur les copies TOEFL » et « Sur les copies américaines ». Remplacé par
  « Le corpus TOEFL… Le corpus américain… ».
- **Ne jamais écrire un manifeste à la main sans reproduire sa sérialisation.** Une correction
  d'une phrase, écrite par `json.dump(..., indent=2)`, a reformaté les 586 lignes de
  llm-watermarking-detection. Le dépôt sérialise en **`indent=1` avec saut de ligne final** — le
  vérifier par `json.dumps(obj, ensure_ascii=False, indent=1) + "\n" == contenu de HEAD` avant
  d'écrire, ou passer par `restyle.py apply`. Le symptôme se lit en une commande :
  `git diff --numstat` annonce le fichier entier là où la correction ne touche qu'une ligne.

- **Laisser une section au-dessus du seuil plutôt que sacrifier un fait**, en disant
  pourquoi. Mais « c'est technique » n'est pas une raison : quatre documents à formules
  (state-space-models, rlhf-dpo, minimal-perfect-hashing, scaling-laws en seconde passe)
  sont descendus dans la cible sans rien perdre.

## Fan-out

Un agent par document, chacun dans `/tmp/restyle/<slug>/` — des noms de fichiers génériques
partagés se sont écrasés entre agents dès la première vague. Le manifeste témoin, lui,
n'était pas en danger : il portait un nom de thème. Vérifier chaque retour soi-même contre
un témoin reconstruit, jamais sur le rapport de l'agent.

## Le prompt d'agent, littéral

À recopier tel quel, en remplaçant `<slug>` et les trois mesures de départ (données par la
commande de reconstruction de la file, en fin de document). Un agent par document.

---

Réécris la prose de `themes/<slug>` (cwd /Users/jean-paulgavini/Documents/Dev/scriptorium)
pour la rendre LISIBLE, **à faits strictement constants**. Tu ne vérifies rien, ne cherches
rien sur le web, n'ajoutes rien : la matière est déjà auditée. Document à <X> mots/phrase,
<Y> % de phrases > 45 mots, <Z> sections hors seuil.

### Procédure (dossier à toi seul : /tmp/restyle/<slug>/)

1. `python3 .claude/skills/monograph/scripts/restyle.py snapshot themes/<slug> /tmp/restyle/<slug>/avant`
2. `python3 .claude/skills/leanmonograph/scripts/lint.py /tmp/restyle/<slug>/avant > /tmp/restyle/<slug>/lint.AVANT.json` — code de sortie lu SANS tube (`$?` après un pipe ment).
3. `restyle.py dump themes/<slug> <ids de sections>` — section par section, le dump complet est volumineux.
4. Par lot : patch `{"<élém>.<par>": "<contenu du <p>, sans les balises <p>>"}` → `restyle.py apply themes/<slug> <patch.json>` → `restyle.py check themes/<slug> /tmp/restyle/<slug>/avant/manifest.json`.
   - Écart **nombres / nombres en toutes lettres / claims** : BLOQUANT. Corrige ta réécriture, jamais le contrôle.
   - Ligne **À ADJUGER** (nom propre en baisse, sigle apparu, insécable collante perdue) : tranche et rapporte. Une répétition devenue inutile passe ; une attribution remplacée par un pronom se répare ; une insécable de ponctuation double disparaît légitimement avec son « : », une insécable entre un nombre et son unité non.
5. Lint APRÈS **sur le thème lui-même** (`themes/<slug>`, jamais sur une copie : `snapshot` reconstruit depuis HEAD et rendrait un rapport identique à l'avant, qui ferait croire que rien n'a bougé). Compare champ par champ au lint AVANT : `rejected_flags`, `unhedged_count`, `foreign_statements`, `novel_numbers`, `low_rank_sources`, `low_rank_blocking`. **Identiques exigés**, hors `prose_style` et hors le champ `context` de chaque entrée, qui change mécaniquement avec la phrase. ⚠️ `unhedged_count` ne doit ni monter NI BAISSER : une baisse signifierait que tu as ajouté une réserve.
6. `python3 .claude/skills/monograph/scripts/build.py themes/<slug>` (exit 0).

### Méthode

Travaille par **substitutions vérifiées** sur le texte d'origine (`count(old) == 1`, sinon
arrêt) plutôt qu'en retapant les paragraphes : les formules, les `<sup>`/`<sub>` et les
`&nbsp;` ne transitent alors jamais par une saisie manuelle. C'est plus sûr que la recopie
caractère par caractère.

### Style

- **Cible 18-22 mots/phrase en médiane**, < 8 % au-dessus de 45. **Plancher : ne descends pas sous 16** — une prose hachée n'est pas lisible. Si tu passes dessous, refusionne les phrases d'annonce trop courtes avec ce qu'elles introduisent. Apprécie la médiane sur le `check`, pas sur le lint : le lint mesure aussi le tldr et le glossaire, que tu ne touches pas, et sa médiane reste un point plus basse.
- Le levier est la RÉPARTITION, jamais la coupe : une phrase porte UN fait ; population, intervalle et réserve suivent en phrases propres. Au plus UNE rupture (—, ;, :) par phrase.
- Trois éléments ou plus : phrases séparées, jamais une phrase à points-virgules. Alterne les longueurs.
- **Quand une incise attributive devient une phrase, RE-NOMME le sujet** au lieu de le pronominaliser (« Jamba offre… », pas « Il offre… »). **Exception** : les noms qui portent un chiffre — CoAct-1, Mem0, GPT-4 — ajoutent un nombre au multiensemble et font échouer le contrôle ; garde le pronom si le nom figure dans la phrase voisine.
- Marqueurs d'énumération `(1)`, `(2)` : ce sont des NOMBRES, insupprimables, et ouvrir une phrase sur une parenthèse prive le découpeur de sa majuscule. Écris « Étape (1) : … ».
- N'ajoute aucun quantifieur absent de l'original (« ces trois familles ») : c'est un nombre en toutes lettres de plus, donc un écart bloquant.
- Le découpeur n'ouvre une phrase que sur une majuscule ou un guillemet : une phrase commençant par un token minuscule ou un chiffre (« o3 confirme… », « 92,82 % … ») se fond dans la précédente et fausse la mesure. Reformule, et signale-le.
- Une réserve reste à **moins de 350 caractères** de son chiffre.
- Bannis le méta-discours (« il faut ici nommer », « tient en une phrase ») et l'auto-référence au corpus (« ce document ») hors section écosystème — mais garde intact le renvoi vers un thème voisin, qui est un fait.
- **Interdits** : retirer/modifier chiffre, date, attribution, nom de système, réserve ; convertir un nombre en lettres ou l'inverse ; ajouter un fait même déductible, ni aucune déduction que la source ne porte pas ; toucher autre chose que `manifest.json` et son `dist/`.
- Si une section résiste, laisse-la au-dessus du seuil et dis PRÉCISÉMENT pourquoi. Le seuil est un signal, pas un quota — mais « c'est technique » n'est pas une raison : quatre documents à formules sont descendus dans la cible sans rien perdre.

### Ne fais pas

Ne commite pas, ne pousse pas, pas de `build_site.py`, aucun autre thème.

### Rends (français, court)

Mesures avant/après du `check`, comparaison des deux lints champ par champ, paragraphes
réécrits, cas À ADJUGER et tes décisions, sections laissées hors seuil avec la raison,
hésitations.

---

## Dette de vérité — un chantier distinct

**67 documents sur 90 sortent en exit 2** sur le lint actuel. Ce ne sont pas 67 documents
faux : un flag non hedgé ou une source de rang faible appellent une **adjudication**, qui a
eu lieu pendant chaque run mais dont aucune trace n'est persistée. Le lint n'est donc pas
rejouable comme contrôle de non-régression.

Le sous-ensemble qui mérite un examen réel : les thèmes fabriqués **avant le 46e run**, où
le contrôle de rang des sources n'existait pas et n'a jamais tourné — `count-min-sketch`
(5 claims), `convolutional-networks` (4), `bm25-inverted-index` (3), `peptides-gris` (3),
`scaling-laws` (claim:18, confirmé sur un WordPress et un Medium).

La passe de style n'y touche pas, et ne doit pas y toucher.

**Contradictions internes relevées par la passe, non corrigées** — elles changent un fait,
pas une phrase, et relèvent de ce chantier :

- `approximate-nearest-neighbor` — la plus nette. `pq-quantification-produit` borne l'erreur
  d'ADC par MSE(q) et celle de SDC par 2·MSE(q) ; `garanties-theoriques` énonce l'INVERSE.
  Une troisième phrase (« FAISS utilise ADC par défaut : ne pas quantifier la requête réduit
  de moitié le plancher d'erreur ») tranche en faveur de la première : la seconde est fausse.
- `quantization` — `limites-et-idees-recues` annonce « trois stratégies distinctes » puis en
  énumère quatre (GPTQ, AWQ, SpQR, AQLM).
- `lora` — l'overhead DoRA est dit « réduit à +17 % de temps et +41 % de mémoire » avec
  DoraCaching, alors que la mémoire MONTE de +4 % à +41 %.
- `cafeine-cognition-vigilance` — le même résultat de Philip est rapporté en « trois sujets sur
  quatre » dans `travail-poste-et-conduite` et en « les trois quarts des ESSAIS » dans
  `la-sieste-cafeinee`. Deux unités d'analyse incompatibles pour une seule étude. Deux autres
  soupçons du même agent ont été écartés à l'examen : le 3,7× est introduit par « rapporté en
  taux », donc une autre grandeur, et le F(1,95) voisin d'un 1,95 de taille d'effet est une
  notation de degrés de liberté — une collision numérique, pas une reprise.

## État

| | avant la passe | à ce jour |
|---|---|---|
| moyenne du corpus | 30,7 mots/phrase | **20,1** |
| documents hors seuil | 89 / 90 | **10 / 90** |
| plus longue phrase du corpus | 175 mots | — |

Les 72 documents traités : omega-3, scaling-laws (deux passes),
coreference-resolution, entity-linking-disambiguation,
named-entity-recognition-sequence-labeling, prompt-optimization,
reasoning-test-time-compute, state-space-models, rlhf-dpo, minimal-perfect-hashing,
agentic-ai, agentic-memory, llm-evaluation, knowledge-graph-construction,
bm25-inverted-index, normalization-layers, tabular-foundation-models,
ia-productivite-esn, retrieval-augmented-generation, quantization,
agent-harness-engineering, lora, self-improving-harness, text-embeddings,
recursive-language-models, diffusion-models, approximate-nearest-neighbor,
hybrid-search-reranking, ia-emploi-marche-du-travail, count-min-sketch,
generative-adversarial-networks, mechanistic-interpretability,
time-series-forecasting, bloom-filters, ensemble-learning,
structured-extraction-llm, mixture-of-experts, decoding-sampling,
calibration-classifieurs, clustering-dimensionality-reduction,
knowledge-distillation, peptides-gris, sarcopenie-exercice-nutrition,
transformer-attention, relation-extraction, ejaculation-precoce,
cafeine-cognition-vigilance, llm-inference-serving, vitamine-d,
microdosage-psychedeliques, hallucination-detection-uncertainty,
backpropagation, hyperloglog, consistent-hashing, learning-to-rank,
nootropiques-stimulants-prescrits, multi-agent-orchestration,
multimodal-vlm, creatine, distributed-training-parallelism,
incretines-glp1, agentic-rl-environments, diffusion-language-models,
streaming-quantiles-sampling, testosterone-homme-age, inhibiteurs-pde5,
event-extraction-temporal, llm-safety-jailbreaks, context-engineering,
nootropiques-vegetaux, nootropiques-panorama, contrastive-self-supervised,
cafeine-ergogene, world-models, collagene,
ia-competences-deskilling-apprentissage, agent-evaluation-observability,
llm-watermarking-detection, gpu-kernels-compilers, complements-amincissants.

Tous sont à zéro section signalée. **Il reste dix documents**, et la file tient désormais en
deux vagues et demie : `document-ai`, `sparse-attention-long-context`,
`reinforcement-learning-fundamentals`, `berberine`, `pretraining-data-curation`,
`masse-maigre-sous-glp1`, `proteines-besoins-timing`, `graph-neural-networks`,
`convolutional-networks`, `variational-autoencoders`.

Pour reconstruire la file à jour :

```
python3 - <<'PY'
import glob, pathlib, importlib.util
spec = importlib.util.spec_from_file_location("lint", ".claude/skills/leanmonograph/scripts/lint.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows = []
for t in sorted(glob.glob('themes/*')):
    p = pathlib.Path(t)
    if not (p / 'manifest.json').exists(): continue
    st = m.prose_style(p, False)
    if st['sentences'] and st['sections_over']:
        rows.append((st['mean_words'], st['median_words'], st['pct_over_45'], len(st['sections_over']), p.name))
for r in sorted(rows, reverse=True): print(r)
PY
```
