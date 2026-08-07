# Doctrine de preuve — méta-domaine santé/nutrition

S'applique à toute monographie du méta-domaine `sante-nutrition`. Le « ≥ 2 sources
indépendantes » du scriptorium reste le PLANCHER ; les règles ci-dessous s'y AJOUTENT.
À injecter en bloc dans le brief de chaque run (« Doctrine : docs/evidence-sante.md »
ne suffit pas — recopier les règles dans le prompt, les agents du pipeline ne lisent
pas ce fichier). Spec d'origine : docs/2026-08-07-meta-domaines-sante-design.md.

## Hiérarchie des sources

- **Rang fort** : méta-analyse, revue systématique, RCT publié en revue à comité de
  lecture, position de société savante (ISSN, Cochrane, EFSA, Academy of Nutrition
  and Dietetics, sociétés médicales).
- **Rang moyen** : étude de cohorte, essai ouvert, examine.com (agrégateur sérieux
  mais secondaire).
- **Rang faible** : étude mécanistique, étude animale ou in vitro. Ne suffit JAMAIS
  à soutenir un claim d'efficacité chez l'humain — seulement à l'expliquer.
- **Rang nul seul** : presse générale, blogs, sites de marques, influenceurs. Deux
  sources de rang nul ne confirment rien, même indépendantes.

## Règles par claim

1. Tout claim d'**efficacité** ou de **sécurité** exige ≥ 2 sources indépendantes
   DONT ≥ 1 de rang fort.
2. **Dose et taille d'effet obligatoires** dans le statement : « 3-5 g/j de créatine
   monohydrate, +N % sur 1RM en méta-analyse », jamais « la créatine marche ».
   La plage COMPLÈTE des mesures, pas une borne (leçon du 27e run).
3. **Indépendance = travaux distincts** (règle docKeys), renforcée : un RCT + son
   communiqué de presse ou sa reprise presse = 1 source ; deux essais du même
   laboratoire = à signaler ; un write-up tiers par d'autres auteurs = 2e source valide.
4. **Financement industriel signalé** dans l'audit du claim quand la source le
   déclare (fréquent : collagène, amincissants).
5. Un claim porté uniquement par des études animales/mécanistiques est un claim sur
   le MÉCANISME, à formuler comme tel — pas sur l'effet humain.

## Règles par document

- Section « Sécurité, doses, interactions » OBLIGATOIRE dans le plan de sections.
- Public : lecteur exigeant sans formation médicale — définir chaque terme clinique
  à première occurrence.
- Bandeau non-conseil médical : porté par la clé `notice` du méta-domaine dans
  `tools/taxonomy.json`, injecté par `build_site.py` (page méta + copies `_site/`
  des monographies). JAMAIS écrit dans la prose ni dans `dist/`.

## Texte de la notice (clé `notice` du méta `sante-nutrition`)

> Document d'information rédigé et vérifié sur sources publiées — ce n'est ni un
> avis médical ni une recommandation individuelle. Consultez un professionnel de
> santé avant toute supplémentation ou traitement.

## Impact sur la vérification du live

Les copies `_site/` des monographies santé diffèrent de leur `dist/` par l'encart
`<aside class="notice-sante-doc">…</aside>` injecté au build, PUIS par le script
GoatCounter injecté par le CI. Pour vérifier « live byte-identique » : neutraliser
LES DEUX par sous-chaîne (avec leurs `\n`), jamais par `grep -vF` (cf. mémoire
handoff-2026-08-05 : sha de fichier vide `e3b0c442…` = signature du piège).
