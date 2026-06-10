## Chiffres de référence (médianes par article, mesurées)

| Type de token (par article) | monograph (Opus) | frugal (Opus+Sonnet) |
|---|---:|---:|
| **Entrée fraîche** (plein tarif) | 3,84 M | **0,73 M** |
| Création de cache (~1,25×) | 14,8 M | 11,1 M |
| Lecture de cache (~0,1×) | 48,1 M | 79,9 M |
| **→ Entrée totale** | 75,0 M | 91,4 M |
| **Sortie** | 0,56 M | 0,93 M |
| **Agents / article** | 61–242 (méd. 127) | 103–130 (méd. 118) |
| Temps brut (rate-limit inclus) | 16–474 min | 109–309 min |

- **Signal qualité** : sur 6 thèmes récents, **159 affirmations sur 204 (78 %) corrigées** par le council avant publication.
- **Cumul projet** : 24 runs, **~2 250 agents**, **12,6 M tokens de sortie**.

## Coût estimé — à titre indicatif (tarifs API publics)

Aux prix catalogue de l'API (Opus 4.8 : 5/25 $ le M de tokens entrée/sortie ; Sonnet 4.6 : 3/15 $ ;
**cache écrit ×1,25, lu ×0,1** — vérifié : 100 % du cache est en TTL 5 min), coût **médian mesuré** par article :

| Profil | Coût / article (USD) | Coût / article (EUR ~0,90 €/$) |
|---|---:|---:|
| **Standard** (Opus partout) | ≈ 161 $ | **≈ 145 €** |
| **Frugal** (Opus + Sonnet) | ≈ 100 $ | **≈ 90 €** (−38 %) |

> ⚠️ **Coûts notionnels, pas une facture.** La fabrique tourne sous **forfait Claude Max ×20**
> (abonnement mensuel fixe) : le **coût marginal réel par article est ~nul** au-delà de l'abonnement.
> Ces euros mesurent ce que paierait **un tiers facturé à l'usage**, donc un repère de *valeur* et non une
> dépense engagée. (Conversion ~0,90 €/$, taux indicatif.)
- **Note** : l'entrée totale (~75–90 M) est dominée à ~90 % par de la lecture de cache (facturée ~10 %) ; le temps brut est dominé par les rate-limits serveur, pas le calcul ; le frugal ne réduit pas le *volume* de tokens mais déplace ~65 % de la génération vers un modèle ~5× moins cher.

---
## Présentation ##
L'IA sait écrire vite et bien, mais peut-on lui faire confiance sur les faits ?

Pour y répondre, j'ai tenté par l'ingénierie de transformer n'importe quel sujet en une monographie complète, avec une exigence simple : toute affirmation « confirmée » doit s'appuyer sur au moins 2 sources indépendantes, contrôlées en code.

Pour cela, un workflow multi-agents enchaine les étapes suivantes:
- Recherche multi-angles (fondements, théorie, variantes, applications, idées reçues, écosystème) ;
- Extraction des affirmations candidates ;
- Council adversarial: chaque affirmation est attaquée par 2 à 3 « jurés » sous des angles distincts : réfutation, indépendance des sources, source primaire ;
- Rédaction des faits validés ;
- Widgets interactifs (codés puis relus par un critique) ;
- Assemblage déterministe : le code assemble, et échoue bruyamment si une référence manque ou si une affirmation n'est pas sourcée.

Les chiffres réels (extraits des journaux d'exécution) :
- ~120 agents IA lancés par article (jusqu'à 240 sur les sujets les plus larges) ;
- Côté tokens, par article : ~0,7 M en entrée plein tarif + ~1 M en sortie, auxquels s'ajoutent ~80 M de tokens lus depuis le cache (facturés ~10 % du prix). L'entrée totale atteint donc ~90 M
- 1 à 3 heures de génération, dominé par l'attente des limitations de débit serveur, pas par le calcul ;
- 159 affirmations sur 204 (78 %) corrigées par le council avant publication, sur les 6 derniers thèmes.

Ce dernier chiffre est le plus parlant. 78 % du premier jet était imprécis ou faux.
C'est exactement ce qu'un outil grand public publierait sans filet avec un prompt type « génère moi un playground interactif sur X »: un rendu convaincant, soigné… et factuellement non garanti. Un deep research classique fait mieux (il cite), mais rend de la prose à lire, sans artefact interactif ni build qui refuse les affirmations non sourcées.

Ici, la vérification est adversariale, multi-passes et opposable : chaque article garde sa piste d'audit, affirmation par affirmation.

Il existe aussi une variante dite frugale qui n'économise pas en réduisant la matière, mais simplement en déplaçant ~65 % de la génération vers un modèle moins cher (Sonnet pour la recherche et la vérification, Opus restant réservé au jugement structurant) et divise par ~5 l'entrée facturée plein tarif en bornant le fan-out par des plafonds durs. 

Avantages / limites:
+ Fiabilité factuelle vérifiable et opposable ; livrable unique, interactif, reproductible. 
- Ni instantané ni gratuit, opérationnellement complexe et surdimensionné pour un sujet trivial.

La valeur n'est pas dans le prompt magique, mais dans le harnais autour du modèle : contradiction, vérification croisée, assemblage déterministe. 

👉 Les liens en commentaire

#IA #LLM #ESN #Conseil #IngénierieLogicielle #Agents

