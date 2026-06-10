# scriptorium

Fabrique de documents multi-thèmes. Chaque thème est transformé en une **monographie**
partageant une charte graphique commune.

Un document unique : abstract, sections vérifiées, widgets démonstratifs, exercices, biblio, pointeurs, glossaire.

## Structure

```
themes/<slug>/            un dossier par thème (slug kebab-case, sans accents)
  knowledge.json          base de faits vérifiée (source de vérité)
  glossary.json · tldr.json
  widgets/                widgets interactifs du thème
  manifest.json           manifeste-vue du document
  dist/                   le HTML généré
.claude/skills/monograph/  le skill local qui produit une monographie
```

## Produire une monographie

Dans Claude Code, invoque le skill local avec un sujet (d'une phrase à une page) :

```
/monograph <sujet>
```

Le skill effectue une recherche approfondie, vérifie chaque fait contre **≥ 2 sources
indépendantes** (passe adversariale/council), construit la base de faits, puis assemble
le document de façon déterministe. Le modèle juge ; le code assemble.

**Variante à coût réduit :**

```
/frugalmonograph <sujet>
```

Même produit et **mêmes garanties non négociables** (≥ 2 sources indépendantes ; `build.py`
échoue bruyamment) ; seul le profil de coût change : modèles moins chers (Sonnet) sur la
recherche/vérification, council ramené à **2 jurés** dans tous les cas, et des plafonds
(`MAX_SECTIONS=9`, `MAX_CLAIMS_PER_SECTION=4`). Le jugement structurant (Plan, Author, Widgets,
Compose) reste sur Opus. Pour comparer les deux variantes sur un même sujet, utilise un slug
distinct (ex. `bloom-filters-frugal`).

> [!WARNING]
> `/monograph` consomme **ÉNORMÉMENT de tokens** — de l'ordre de **plusieurs millions de
> tokens de sortie par monographie** (runs observés : ~5 M chacun). Le coût est dominé par le
> fan-out massif des phases **Verify** (council adversarial : 2–3 jurés × tous les claims de
> toutes les sections) et **Widgets** (codage + relecture de HTML interactif). À lancer en
> connaissance de cause — mais un run interrompu (rate-limit) se **reprend sans re-payer le
> travail déjà fait** (voir « Reprise après interruption »).

### Reprise après interruption

Le fan-out massif se fait régulièrement **rate-limiter côté serveur**. Plutôt que de relancer un
run frais (qui re-paie tout), le workflow écrit des **checkpoints incrémentaux** dans
`themes/<slug>/.monograph/` au fil de l'eau : la recherche après *Plan*, **une fois par section
auditée** pendant *Verify*, et les widgets après leur phase. Relancer avec **`args.resume = true`**
(mêmes `subject`/`slug`/`themeDir`) reprend là où ça s'est arrêté : *Sweep*/*Plan* sont sautés,
**seules les sections sans checkpoint sont re-vérifiées**, les widgets déjà faits sont sautés. Ces
checkpoints survivent à un `/clear` ou à un changement de session (ce que le cache de reprise du
moteur, lui, ne garantit pas). Un run **frais** (sans `resume`) ignore et réécrit les checkpoints.
Détail dans le `SKILL.md` du skill ; le câblage est couvert par `scripts/test_resume.mjs`.

### Le pipeline multi-agents

En coulisse, `/monograph` lance un **workflow multi-agents** en 8 phases. La frontière est
nette : **le modèle juge** (cherche, rédige, vérifie, sélectionne) et **le code assemble** de
façon déterministe. Le fan-out est massif sur **Verify** (le council) et **Widgets**.

1. **Sweep** — 6 agents en parallèle, un par angle (fondations, théorie, variantes,
   applications, idées reçues, écosystème) ; chacun cherche sur le web et remonte des sources
   et des faits sourcés (URL exactes, jamais inventées).
2. **Plan** — 1 agent conçoit l'outline (4–9 sections) à partir des findings agrégés.
3. **Extract** — 1 agent par section (en pipeline) : rédige la prose et propose 2–4 claims
   vérifiables, dont au moins un « contestable » (idée reçue à départager).
4. **Verify** — *council adversarial* : chaque claim passe devant 2 jurés (s'il est « établi »)
   ou 3 (s'il est « contestable »), sous trois lentilles — réfutation, indépendance des sources,
   source primaire. Puis, **en code** : la décision d'audit (`confirmed` = tenu par ≥ 2 jurés
   **et** ≥ 2 sources indépendantes ; sinon `corrected`, sinon `rejected`), l'assemblage de
   `knowledge.json` et l'élagage des sections sans matière vérifiée.
5. **Author** — 1 agent écrit `glossary.json` et `tldr.json` à partir des faits vérifiés.
6. **Widgets** — 2ᵉ fan-out : un *planner* choisit les mécanismes non triviaux qui gagnent à
   être *montrés*, des *codeurs* écrivent chacun un widget HTML interactif autonome, un *critic*
   les relit (une re-passe de correction possible).

   Au-delà des **sondes** (un widget par mécanisme), une monographie peut porter un ou plusieurs
   **super-widgets synoptiques** : la visualisation d'un **processus de bout en bout** (ex. backprop :
   passe avant → rétropropagation → itérations jusqu'à convergence) sur un réseau jouet. On peut aussi
   les ajouter après coup à un article existant (`args.superwidgetOnly`).

   Quand une illustration **fixe** vaut mieux qu'une interaction (une courbe, un organigramme, un
   schéma), le pipeline insère une **figure statique** au fil du texte, légendée et numérotée
   « Figure N » — choisie par le même planificateur visuel, sans surcharger.

7. **Compose** — 1 agent écrit `manifest.json`, le *layout* best-of (abstract → sections +
   widgets → exercices → biblio → pointeurs → glossaire).
8. **Build** — `build.py` assemble le HTML final de façon déterministe et **échoue bruyamment**
   (référence manquante, balise déséquilibrée, jeton non substitué…).

```mermaid
flowchart TD
    S(["Sujet"]) --> SW["Sweep<br/>6 agents · 1 par angle"]
    SW --> PL["Plan<br/>outline 4–9 sections"]
    PL --> EX["Extract · 1/section<br/>prose + claims"]
    EX --> VE["Verify · council<br/>2–3 jurés / claim"]
    VE --> KN{{"code : audit<br/>knowledge.json<br/>≥2 sources indép."}}
    KN --> AU["Author<br/>glossary + tldr"]
    AU --> WG["Widgets<br/>plan → code ×N → critic"]
    WG --> CO["Compose<br/>manifest.json"]
    CO --> BD{{"code : build.py<br/>HTML · échoue bruyamment"}}
    BD --> OUT(["dist · 1 HTML"])
```

## Thèmes

Chaque document est sous `themes/<slug>/dist/`. Hors APO (construit à la main), tous sont
générés par `/monograph` ou sa variante économe `/frugalmonograph` (les plus récents).

- **automatic-prompt-optimization** — panorama des approches d'APO + contrat d'architecture.
  Édition **construite à la main** (avant le skill), 3 documents ; le pipeline d'origine est
  conservé, gelé, sous `themes/automatic-prompt-optimization/legacy/`.
- **bloom-filters** — premier thème **généré par `/monograph`** : filtres de Bloom (principe,
  garanties, variantes, limites).
- **consistent-hashing** — hachage cohérent : anneau, nœuds virtuels, rééquilibrage.
- **knowledge-graph-construction** — construction de graphes de connaissances.
- **transformer-attention** — mécanisme d'attention des transformeurs.
- **text-embeddings** — plongements lexicaux : tokenisation, similarité cosinus.
- **prompt-optimization** — optimisation de prompts.
- **ensemble-learning** — méthodes d'ensemble : bagging, boosting (25 faits confirmés, 15 corrigés).
- **backpropagation** — rétropropagation du gradient (34 confirmés, 13 corrigés, 1 rejeté).
- **time-series-forecasting** — prévision de séries temporelles : panorama des familles de
  méthodes (statistiques, ML, modèles de fondation) (5 confirmés, 30 corrigés, 1 rejeté).
- **minimal-perfect-hashing** — fonctions de hachage parfaites minimales (MPHF) : construction,
  espace, état de l'art (12 confirmés, 18 corrigés, 1 rejeté).
- **approximate-nearest-neighbor** — recherche approchée de plus proches voisins : HNSW, IVF,
  PQ, LSH (12 confirmés, 22 corrigés).
- **diffusion-models** — modèles de diffusion génératifs : DDPM, score matching, SDE/PF-ODE,
  flow matching (7 confirmés, 25 corrigés).
- **ia-productivite-esn** — IA et gains de productivité dans les ESN : annonces vs réalités
  (3 confirmés, 32 corrigés).
- **agentic-ai** — IA agentique : état de l'art, applications, projections (3 confirmés,
  32 corrigés, 1 rejeté).

## Statut

- Phase 0 — restructure & migration : ✅
- Phase 1 — générateur déterministe (`.claude/skills/monograph/` : charte + `build.py`, 16 tests) : ✅
- Phase 2 — workflow multi-agents + `SKILL.md` des skills `monograph` et `frugalmonograph` : ✅
  Pipeline à **8 phases** (Sweep → Plan → Extract → Verify → Author → **Widgets** → Compose →
  Build), document unique « best-of » + widgets pilotés par concept. Éprouvé sur **14 thèmes**
  hors APO (voir ci-dessus) et publié via GitHub Pages.
