---
name: arrange
description: Use when asked to arrange/classer/ranger les monographies du scriptorium par domaine, (re)définir ou réévaluer la taxonomie de la home GitHub Pages, classer un nouveau thème, rééquilibrer les domaines, ou mettre à jour un portail de domaine (parcours de lecture, arêtes entre thèmes, frontières entre voisins). Maintient tools/taxonomy.json et tools/portals/*.json (seules sources de vérité), lus par tools/build_site.py. Triggered by /arrange.
---

# arrange — agencement des monographies par domaine

Seul responsable de `tools/taxonomy.json` (source de vérité de la taxonomie ; cf.
`docs/superpowers/specs/2026-06-12-taxonomy-domains-design.md`) **et de `tools/portals/*.json`**
(couche éditoriale des portails de domaine ; cf.
`docs/superpowers/specs/2026-07-25-domain-portals-design.md`). `build_site.py` les **lit** ;
`monograph`/`frugalmonograph` n'y touchent jamais.

Classer un thème et l'insérer dans le portail de son domaine sont **le même geste** : les
séparer désynchroniserait les deux fichiers.

Frontière jugement / code : TU **juges** (classer, diagnostiquer, proposer, relier) ; l'écriture
des fichiers + `build_site.py` sont **déterministes**. Ne modifie QUE `tools/taxonomy.json` et
`tools/portals/*.json`.

## Déroulé

1. **Lire l'état** :
   - `tools/taxonomy.json` s'il existe (sinon = premier amorçage : tout est « à classer »).
   - `tools/portals/*.json` : les domaines qui en ont un (l'existence du fichier suffit à le
     déclarer). Pour un thème à insérer, lire aussi sa `these` dans `themes/<slug>/tldr.json`
     — c'est ce que le portail affichera, inutile de la reformuler.
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
   réordonnancement), la raison. **Si le domaine cible a un portail**, proposer dans le même
   plan : la place du thème dans le `parcours` + son `pourquoi`, les `aretes` vers ses voisins,
   et une `delimitations` si un voisin est assez proche pour qu'on les confonde. Présenter à
   l'utilisateur et **attendre sa validation**. Ne rien écrire avant le feu vert.
5. **Écrire** `tools/taxonomy.json` (mêmes clés : `version`, `domains[]` ordonné avec
   `id`/`label`/`blurb`/`themes`). Conserver l'ordre validé. Un thème = un seul domaine.
   Puis, le cas échéant, `tools/portals/<domaine>.json` (clés : `domain`, `intro`, `parcours`,
   `aretes`, `delimitations`). Un thème déplacé sort du portail de son ancien domaine et entre
   dans celui du nouveau.
6. **Régénérer + vérifier** : `python3 tools/build_site.py` (doit sortir 0, sans bucket
   « À classer » résiduel pour les thèmes qu'on vient de classer) ; rapporter le résultat.

## Garde-fous
- `tools/build_site.py` valide les invariants (slug sans dist, slug en double, domaine vide,
  fichier manquant ; côté portail : thème du domaine absent du parcours, slug cité hors
  domaine, doublon, portail orphelin) et **échoue bruyamment** : si le run de l'étape 6 échoue,
  corriger `taxonomy.json` / le portail, ne pas contourner.
- **Aucun fait vérifiable dans un portail** : ni chiffre, ni date, ni attribution, ni mesure de
  performance. Un portail ne porte que des relations et de l'orientation de lecture — c'est ce
  qui l'exempte légitimement du council. Un énoncé du type « X surpasse Y de N points » est un
  claim : sa place est le `knowledge.json` d'une monographie, avec ses ≥ 2 sources.
- Ne rien recopier de dérivable dans un portail (thèse, titre, libellé) : `build_site.py` les
  relit à chaque build, une monographie mise à jour rafraîchit son portail toute seule.
- Ne JAMAIS classer le legacy `automatic-prompt-optimization` dans un domaine.
- Publication : committer/pousser `tools/taxonomy.json` re-déploie le site public — laisser le
  push au feu vert de l'utilisateur (cf. `pages-publication`).
