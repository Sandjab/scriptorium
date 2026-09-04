# Passe de style — rendre la prose lisible sans toucher aux faits

Chantier ouvert le 2026-09-03. **13 documents traités sur 90.** File d'attente et procédure
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

## Les huit pièges déjà payés

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

## État

| | avant la passe | à ce jour |
|---|---|---|
| moyenne du corpus | 30,7 mots/phrase | **28,2** |
| documents hors seuil | 89 / 90 | **78 / 90** |
| plus longue phrase du corpus | 175 mots | — |

Les 13 documents traités : omega-3, scaling-laws (deux passes),
coreference-resolution, entity-linking-disambiguation,
named-entity-recognition-sequence-labeling, prompt-optimization,
reasoning-test-time-compute, state-space-models, rlhf-dpo, minimal-perfect-hashing,
agentic-ai, agentic-memory.

Tous sont à zéro section signalée. Tête de file suivante : `llm-evaluation`,
`knowledge-graph-construction`, `bm25-inverted-index`, `normalization-layers`,
`tabular-foundation-models`, `ia-productivite-esn`, `retrieval-augmented-generation`,
`quantization`.

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
