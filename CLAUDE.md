# scriptorium — instructions projet

Fabrique de documents multi-thèmes : chaque thème → une monographie HTML vérifiée
(document de référence unique, best-of). Voir `README.md`.

## Conventions
- **Un dossier par thème** sous `themes/<slug>/`. Slugs kebab-case, sans accents ni espaces.
- **Captures de revue visuelle** : les écrire dans `.playwright-mcp/` (déjà gitignoré), pas
  dans le scratchpad — Playwright n'autorise que des racines à l'intérieur du repo et refuse
  tout chemin sous `/private/tmp/…`.
- **Charte = source unique** : `.claude/skills/monograph/template/` (`charte.css`, `components.py`).
  Ne pas dupliquer de style par thème.
- **Faits = source de vérité unique** : `themes/<slug>/knowledge.json`. Le manifeste d'édition est une *vue* : il référence les faits par id, jamais ne les recopie.
- **Frontière jugement / code** : le modèle recherche, rédige, vérifie ; `build.py` assemble
  de façon déterministe. Pas de logique d'édition cachée dans le code de build.
- **`legacy/` est gelé** : le pipeline hand-built de l'APO n'est ni régénéré ni maintenu ;
  il sert de golden de référence pour la charte.

## Vérité non négociable
- Tout fait `confirmed` dans `knowledge.json` s'appuie sur **≥ 2 sources indépendantes**.
- `build.py` **échoue bruyamment** sur référence manquante ou vérification structurelle cassée.
- **Un audit de couverture se fait en lisant les documents, jamais au grep.** Pour décider
  qu'un sujet est déjà couvert (ou absent) du corpus, lire la prose des monographies
  concernées — un `grep` sur un mot-clé conclut faux dans les deux sens : il rate ce qui est
  dit autrement, et compte comme couvert ce qui n'est qu'évoqué.

## Runs longs
- Un run `/leanmonograph` (ou `/monograph`, `/frugalmonograph`) dure des heures.
  **Annoncer au lancement une fourchette de tokens ET de durée**, puis **donner un point
  d'étape à chaque phase franchie** (Sweep → Extract → Council → Author → Build), sans
  attendre d'être relancé.
- Si une phase dépasse nettement son estimation, **le dire tôt** plutôt qu'au bilan :
  le silence est indiscernable d'un blocage.

## Ne pas faire
- Ne pas redire les règles globales de `~/.claude/CLAUDE.md` (déjà appliquées).
- Ne pas retrofitter l'APO dans le nouveau modèle (hors périmètre v1).
