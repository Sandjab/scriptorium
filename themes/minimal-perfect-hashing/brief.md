# Tables de hachage minimales parfaites

**Sujet (tel que fourni)** : tables de hashage minimales parfaites.

## Cadrage

Panorama vérifié des **fonctions de hachage parfaites minimales** (Minimal Perfect Hash
Functions, MPHF) : une fonction de hachage qui mappe un ensemble *statique* de n clés vers les
n entiers `[0, n)` **sans collision** (parfaite) et **sans trou** (minimale). Couvrir : la
définition et le contraste perfect vs minimal perfect ; la borne théorique d'espace
(≈ 1,44 bits/clé, lien avec log₂ e) ; les familles de construction historiques et modernes
(CHD, BDZ/hypergraphes, RecSplit, PTHash, fingerprint-based comme BBHash) ; les compromis
espace / temps de construction / temps d'évaluation ; et les usages réels (indexation,
bases de données clé-valeur, bio-informatique k-mers, compilateurs/mots-clés).

Public : ingénieur·e logiciel curieux des structures de données, sans prérequis pointu en
théorie de l'information. Document de référence unique, best-of, vérifié (≥ 2 sources
indépendantes par fait `confirmed`).
