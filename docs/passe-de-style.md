# Passe de style — rendre la prose lisible sans toucher aux faits

Chantier ouvert le 2026-09-03. **41 documents traités sur 90.** File d'attente et procédure
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

## Les douze pièges déjà payés

1. **Témoin incomplet.** Le lint en mode post lit manifest + knowledge + tldr + glossary +
   `widgets/`. Il manquait `tldr.json` une fois, `widgets/` une autre : deux fausses alertes
   de régression dans la même journée. D'où `snapshot`, qui ne se construit plus à la main.
   Les widgets ne sont scannés que pour `rejected_flags` : leur absence ne peut fausser que
   ce champ.
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
   ne la voit plus.
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
12. **Ne jamais RÉIMPLÉMENTER un contrôle : l'importer.** Une copie manuelle de la regex
   `STICKY_RE` a compté 145 insécables au lieu de 19 sur structured-extraction-llm, et
   annonçait une perte inexistante. `importlib` charge `restyle.py` en trois lignes, et
   `sticky_nbsp` / `proper_nouns` répondent juste. Même famille que le piège 11 : l'outil de
   vérification est ce qui ment en premier.

## Ce qui marche, et qu'il faut redemander

- **Travailler par substitutions vérifiées** (`count(old) == 1`, sinon arrêt) plutôt qu'en
  retapant le paragraphe. Les formules, `<sup>`/`<sub>` et `&nbsp;` ne transitent alors
  jamais par une saisie manuelle. Méthode apparue chez un agent, reprise par les suivants.
- **Re-nommer le sujet** quand une incise attributive devient une phrase (« Jamba offre… »,
  pas « Il offre… ») — sauf cas 4 ci-dessus. C'est ce qui fait disparaître les cas à adjuger.
- **Plancher de 16 mots de médiane.** Sous ce seuil la prose devient télégraphique ; trois
  agents ont dû refusionner des coupes trop sèches pour y remonter.
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

## État

| | avant la passe | à ce jour |
|---|---|---|
| moyenne du corpus | 30,7 mots/phrase | **24,1** |
| documents hors seuil | 89 / 90 | **50 / 90** |
| plus longue phrase du corpus | 175 mots | — |

Les 41 documents traités : omega-3, scaling-laws (deux passes),
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
calibration-classifieurs, clustering-dimensionality-reduction.

Tous sont à zéro section signalée. Tête de file suivante :
`knowledge-distillation`, `peptides-gris`, `sarcopenie-exercice-nutrition`,
`transformer-attention`, `relation-extraction`, `ejaculation-precoce`,
`cafeine-cognition-vigilance`, `llm-inference-serving`.

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
