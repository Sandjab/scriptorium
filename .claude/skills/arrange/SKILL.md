---
name: arrange
description: Use when asked to arrange/classer/ranger les monographies du scriptorium par domaine, (re)définir ou réévaluer la taxonomie de la home GitHub Pages, classer un nouveau thème, ou rééquilibrer les domaines. Maintient tools/taxonomy.json (seule source de vérité), lu par tools/build_site.py. Triggered by /arrange.
---

# arrange — agencement des monographies par domaine

Seul responsable de `tools/taxonomy.json` (source de vérité de la taxonomie ; cf.
`docs/superpowers/specs/2026-06-12-taxonomy-domains-design.md`). `build_site.py` la **lit** ;
`monograph`/`frugalmonograph` n'y touchent jamais.

Frontière jugement / code : TU **juges** (classer, diagnostiquer, proposer) ; l'écriture du
fichier + `build_site.py` sont **déterministes**. Ne modifie QUE `tools/taxonomy.json`.

## Déroulé

1. **Lire l'état** :
   - `tools/taxonomy.json` s'il existe (sinon = premier amorçage : tout est « à classer »).
   - Thèmes publiés = dossiers ayant un `themes/<slug>/dist/*.html`. Exclure le legacy
     `automatic-prompt-optimization` (hors taxonomie, rendu en dernier).
   - Pour chaque thème, lire le contexte : `<title>` du dist + `themes/<slug>/knowledge.json`
     (champ `theme`, et au besoin la nature des `claims`) pour juger son sujet.
2. **Repérer les nouveaux** : thèmes publiés absents de toute liste `themes` (ils sortiront du
   bucket « À classer » de la home une fois rangés).
3. **Diagnostiquer** (signaux, pas règles dures) :
   - domaine sur-peuplé (cohérence interne faible → candidat à scission) ;
   - domaine sous-peuplé (1-2 thèmes → fusionner ou nourrir ?) ;
   - thème dont le sujet colle mieux à un autre domaine (candidat déplacement) ;
   - orphelins (aucun domaine naturel).
4. **PROPOSER** un plan explicite : pour chaque nouveau thème, le domaine cible + 1 phrase de
   justification ; pour chaque ajustement (déplacement / fusion / scission / renommage /
   réordonnancement), la raison. Présenter à l'utilisateur et **attendre sa validation**.
   Ne rien écrire avant le feu vert.
5. **Écrire** `tools/taxonomy.json` (mêmes clés : `version`, `domains[]` ordonné avec
   `id`/`label`/`blurb`/`themes`). Conserver l'ordre validé. Un thème = un seul domaine.
6. **Régénérer + vérifier** : `python3 tools/build_site.py` (doit sortir 0, sans bucket
   « À classer » résiduel pour les thèmes qu'on vient de classer) ; rapporter le résultat.

## Garde-fous
- `tools/build_site.py` valide les invariants (slug sans dist, slug en double, domaine vide,
  fichier manquant) et **échoue bruyamment** : si le run de l'étape 6 échoue, corriger
  `taxonomy.json`, ne pas contourner.
- Ne JAMAIS classer le legacy `automatic-prompt-optimization` dans un domaine.
- Publication : committer/pousser `tools/taxonomy.json` re-déploie le site public — laisser le
  push au feu vert de l'utilisateur (cf. `pages-publication`).
