# glp1-hors-poids — brief

**Sujet.** Ce que les agonistes du GLP-1 font hors de la balance : indication autorisée
contre effet de classe. Organe par organe, essai par essai — le foie (MASH/ESSENCE), le rein
(FLOW), l'insuffisance cardiaque à fraction préservée (STEP-HFpEF), l'apnée du sommeil
(SURMOUNT-OSA), le cerveau (EVOKE/EVOKE+, l'essai négatif comme résultat central), les
addictions, le SOPK, l'arthrose (TRIUMPH-4), et ce qui sépare une AMM d'un effet de classe.

**Fil rouge.** Le déplacement du poids vers l'organe, et ce que chaque essai n'a PAS regardé.

**Public.** Lecteur exigeant sans formation médicale ; chaque terme clinique défini à première
occurrence.

**Domaine.** `pharmacologie-metabolique` (méta-domaine `sante-nutrition`) — 5e thème du domaine.

## Délimitations (vérifiées par LECTURE le 2026-09-08)

- `incretines-glp1` tient STEP / SURMOUNT / SELECT, l'HbA1c, le pipeline rétatrutide et le
  compounding. **Partir de** sa section `obesite-step-surmount` et de `select-cardiovasculaire` ;
  ne rien redérouler.
- Sa grille de lecture est déjà écrite dans `signaux-controverses` : « "Aucun signal observé" ne
  vaut que si le paramètre concerné a été mesuré. » L'appliquer, ne pas la réénoncer comme neuve.
- ⚠️ Dans `incretines-glp1`, **toutes** les occurrences de « rénal » désignent la *clairance*
  rénale (pharmacocinétique de l'acylation et de la liaison à l'albumine), jamais un critère
  rénal. Une seule phrase note que trois phases 2 du rétatrutide portent « sur les paramètres
  rénaux » : seul point de contact, à ne pas confondre avec FLOW.
- `masse-maigre-sous-glp1` tient la composition corporelle ; `berberine` et
  `complements-amincissants` tiennent les substituts ; `microdosage-psychedeliques` tient la
  mécanique 5-HT2B.

## Gap vérifié

`MASH`, `ESSENCE`, `HFpEF`, `SURMOUNT-OSA`, `EVOKE`, `SOPK` : **0 occurrence** dans les 92 thèmes
publiés (localisation par grep, contexte des faux positifs — « Nash », « workflow », « flow
matching », clairance rénale — lu un par un).

## Doctrine de preuve

`docs/evidence-sante.md`, recopiée intégralement dans `args.subject` du run (les agents du
pipeline ne lisent pas ce fichier). Flag `verdicts: true`.

**Règle du promoteur, saillante ici** : presque toutes les phases 3 du champ sont financées par
Novo Nordisk ou Eli Lilly. Un communiqué de promoteur compte comme **la même source** que l'essai
qu'il annonce.
