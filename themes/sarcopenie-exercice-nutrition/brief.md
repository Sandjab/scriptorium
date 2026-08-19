# brief — sarcopenie-exercice-nutrition

40e run `/leanmonograph` · 12e thème santé · **crée le domaine `muscle-vieillissement`**
(cf. `docs/candidate-themes.md`, section « `muscle-vieillissement` — domaine À CRÉER »).

Ce fichier est la TRACE du cadrage. Le canal réel du pipeline est `args.subject` :
`workflow.js` ne lit pas ce fichier. Tout ce qui compte ci-dessous y est recopié.

## Sujet

Gagner ou garder du muscle après 60 ans : ce que l'exercice et l'assiette obtiennent
réellement, et sur quel critère. Population de référence : l'homme de plus de 60 ans.

## Fil rouge (à tenir de bout en bout)

La dissociation entre la MASSE et la FONCTION. Le compartiment que les interventions
déplacent le mieux est celui que le SDOC (2020) a EXCLU de la définition de la sarcopénie,
parce qu'il ne prédisait pas les événements incidents, là où force de préhension et vitesse
de marche les prédisent. L'entraînement en résistance fait l'inverse : gain de masse
modeste, gain de force et de performance large. Thèse : « le substitut ne prédit pas le
résultat » — déjà installée par `vitamine-d` (association vs effet) et par
`masse-maigre-sous-glp1` (mesurer une masse n'est pas mesurer une fonction).

## Ossature suggérée (11-12 sections, écosystème inclus)

1. Trois définitions qui ne mesurent pas la même chose (EWGSOP2 2019, GLIS 2024, SDOC 2020)
2. La résistance anabolique : établie, d'ampleur modeste, disputée dans son étiologie
3. L'entraînement en résistance, seul levier de première ligne (masse vs force)
4. Dose-réponse : le renversement récent en faveur du volume bas
5. Charges, vélocité, restriction de flux sanguin — et le vrai verrou, l'adhérence
6. Protéines : le divorce entre consensus d'experts et essais contrôlés
7. Le seuil par repas relevé avec l'âge, et la distribution des prises
8. La créatine chez le sujet âgé : conditionnée à l'entraînement
9. Le reste du rayon : HMB, vitamine D, oméga-3, leucine isolée, collagène
10. Multimodal : ce que le combiné protège vraiment (PROVIDE, SPRINTT)
11. Sécurité, doses, interactions — OBLIGATOIRE par la doctrine
12. Écosystème & pour aller plus loin

## Délimitations strictes (voisins publiés)

- `proteines-besoins-timing` : plateau de 1,6 g/kg/j, fenêtre anabolique, score protéique,
  chez le sujet ENTRAÎNÉ en surplus ou à l'équilibre. Partir de là, ne pas re-dériver.
  L'angle neuf est la population âgée et le critère de jugement.
- `creatine` : mécanisme, charge, dose, répondeurs/non-répondeurs. Ne pas refaire.
  Ce document ne traite que le 60+ et le conditionnement à l'entraînement.
- `vitamine-d` : chutes, fractures, frontière carencé/institutionnalisé, bolus délétères.
  S'y appuyer, ne pas refaire le dossier. L'angle neuf est le MUSCLE (masse et force),
  que ce voisin ne traite pas.
- `collagene` : verdict rendu, et patron de la littérature mono-source.
- `masse-maigre-sous-glp1` : préservation sous déficit pharmacologiquement induit.
  Ici on parle de GAGNER, pas de moins perdre.
- `cafeine-ergogene` : effet aigu sur la performance, aucun contenu sur l'âge.

## Deux pièges spécifiques

1. La question porte sur l'HOMME de plus de 60 ans et la littérature ne coopère pas :
   populations âgées souvent féminines, essais nutritionnels mélangeant les sexes sans
   stratifier. Écrire l'écart comme une limite, ne jamais le lisser.
2. Les pistes de la recherche préliminaire sont À CORROBORER EN SOURCE PRIMAIRE, jamais
   des faits. Si une piste ne se corrobore pas, la RETIRER — ne pas la sauver.
   Deux pistes signalées douteuses d'avance, à ne pas reprendre telles quelles :
   l'allégation « recommandations nutritionnelles américaines à 1,2-1,6 g/kg/j »
   (source secondaire non fiable) et le chiffrage exact d'OPTIMen (non revérifié).

## Paramètres du run

- `verdicts: true` (thème santé : tableau efficacité/sécurité par intervention)
- doctrine `docs/evidence-sante.md` recopiée EN BLOC dans `args.subject`
- plafond de sections laissé au défaut (16) : le cadrage se fait par le prompt, pas par
  la coupe déterministe — qui tranche APRÈS que les transitions sont écrites (leçon du 27e run)
