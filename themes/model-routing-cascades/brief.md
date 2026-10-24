# Routage multi-modèles et cascades de LLM — brief

**Slug** : `model-routing-cascades` · **Domaine visé** : `llm-agents-generation` (à trancher par /arrange) · **Public** : ingénieur ML/infra.

## Sujet
Servir chaque requête au moindre coût à qualité maintenue : choisir, requête par requête, QUEL modèle répond (un seul répond), soit avant l'appel (routeur), soit après une première réponse (cascade).

## Piliers à couvrir (à comparer au plan avant l'Extract)
1. Le problème et sa forme : frontière coût-qualité, pourquoi un seul modèle frontière pour tout le trafic est un sur-paiement ; routage vs cascade vs ensemble.
2. Les cascades : FrugalGPT (Chen, Zaharia & Zou, 2023), AutoMix (auto-vérification), signal de confiance pour escalader.
3. Les routeurs appris avant l'appel : RouteLLM (données de préférences, classifieurs, matrix factorization, généralisation à des paires de modèles inédites), Hybrid LLM, prédicteurs de difficulté.
4. Les métriques et benchmarks de routage : courbes coût-qualité, APGR, % d'appels au grand modèle, RouterBench et successeurs — et ce qu'ils ne mesurent pas.
5. Le routage dans les produits : routeur intégré aux modèles frontière (à vérifier en source primaire), routeurs commerciaux et passerelles multi-fournisseurs, fallbacks, dégradation contrôlée.
6. Limites et idées reçues ; écosystème.

## Prudence
- Les gains (« −X % de coût à qualité égale ») sont presque toujours auto-déclarés par l'auteur du routeur, sur son propre benchmark : indépendance par TRAVAIL, pas par URL ; un billet de vendeur relève de `document-source` (« X déclare »), jamais d'un fait sur la performance réelle.
- Ne jamais comparer deux pourcentages d'économie sans comparer la paire de modèles, le benchmark et le seuil de qualité.

## Délimitations (vérifiées par LECTURE le 2026-10-24)
- `llm-classifieur-decision-typee` § « Seuil, abstention, routage » traite déjà la règle de rejet de Chow, le report selon l'incertitude, les cascades au niveau du token (Gupta et al., ICLR 2024) et l'early abstention (Zellinger et al.) : citer sans re-dériver.
- `llm-inference-serving` garde le routage côté infra (vers la bonne réplique : prefix-cache-aware, load-aware, autoscaling).
- `small-language-models-edge` garde l'hybride bord/cloud (Apple PCC, Gemini Nano).
- `hallucination-detection-uncertainty` garde les signaux d'incertitude et la prédiction conforme.
- `mixture-of-experts` garde le routage INTERNE (token → expert) ; `multi-agent-orchestration` le pattern Router entre agents ; `decoding-sampling` le speculative decoding (accélération intra-modèle, contrepoint) ; `ensemble-learning` l'agrégation (tous répondent).
