# scriptorium — instructions projet

Fabrique de documents multi-thèmes : chaque thème → triptyque HTML (référence /
publication / pédagogique). Voir `README.md`.

## Conventions
- **Un dossier par thème** sous `themes/<slug>/`. Slugs kebab-case, sans accents ni espaces.
- **Charte = source unique** : `.claude/skills/triptych/template/` (`charte.css`, `components.py`).
  Ne pas dupliquer de style par thème.
- **Faits = source de vérité unique** : `themes/<slug>/knowledge.json`. Les 3 manifestes
  d'édition sont des *vues* : ils référencent les faits par id, jamais ne les recopient.
- **Frontière jugement / code** : le modèle recherche, rédige, vérifie ; `build.py` assemble
  de façon déterministe. Pas de logique d'édition cachée dans le code de build.
- **`legacy/` est gelé** : le pipeline hand-built de l'APO n'est ni régénéré ni maintenu ;
  il sert de golden de référence pour la charte.

## Vérité non négociable
- Tout fait `confirmed` dans `knowledge.json` s'appuie sur **≥ 2 sources indépendantes**.
- `build.py` **échoue bruyamment** sur référence manquante ou vérification structurelle cassée.

## Ne pas faire
- Ne pas redire les règles globales de `~/.claude/CLAUDE.md` (déjà appliquées).
- Ne pas retrofitter l'APO dans le nouveau modèle (hors périmètre v1).
