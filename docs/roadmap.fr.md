# Alloba — Feuille de route

Évolution planifiée de la passerelle Alloba, par ordre de priorité. La version
anglaise est `roadmap.en.md`. Chaque élément implémenté est accompagné d'un ADR
dans `docs/collaboration/adrs/` et d'une mise à jour de `docs/specs.*`.

## Court terme (prochainement)

- **Point de métriques.** `GET /v1/metrics` au format Prometheus : percentiles
  de latence RAG, décomptes d'issues de sourcing, taux d'échec LLM. Le health
  continue de couvrir la disponibilité ; les métriques couvrent la performance.
- **Persistance des sessions de sourcing.** Stocker les sessions dans un store
  local borné pour que les exécutions interrompues puissent être reprises et
  auditées après redémarrage de la passerelle.
- **Normalisation région / langue.** L'extracteur d'intention mappe
  actuellement les régions en texte libre vers des codes ; normaliser la regex
  de repli pour qu'une région telle que `africa` n'arrive jamais avec un espace
  de tête.

## Moyen terme

- **Options de vector store.** Ajouter un second backend sûr (Chroma avec
  sérialisation explicite) sélectionnable via `ALLOBA_VECTOR_STORE`, en
  conservant le mode FAISS sûr par défaut. Les deux restent sans pickle.
- **Routage multi-modèles.** Router le chat vers le modèle outillé le plus
  performant disponible (ex. `qwen3.6`) avec repli sur `llama3.2:1b`, sélection
  via `ALLOBA_CHAT_MODEL` et dégradation automatique basée sur la santé.
- **Versionnage de la KB.** Tagger les builds d'index avec le commit git de
  `kb/docs/` et signaler l'obsolescence dans health au lieu d'un silence
  trompeur.
- **Limitation de débit.** Seaux par jeton pour `/v1/gateway/*` et
  `/v1/sourcing/*`, configurés par environnement, désactivés par défaut.

## Long terme

- **Agent marketplace.** Étendre le sourcing pour comparer des fournisseurs
  entre pays via le moteur de connaissances ECP, avec contrôles de conformité
  par juridiction.
- **Marketplace de modèles pour utilisateurs.** Laisser les locataires choisir
  les modèles d'embedding/chat avec provenance audité et badge « modèle sûr »
  aligné sur l'Ethics by design d'ispaces.
- **Déploiements fédérés.** Passerelles multi-locataires avec partitions de KB
  par locataire et infrastructure partagée, en conservant les garanties
  local-first.

## Registre de décisions

Chaque élément de la feuille de route, une fois approuvé, devient un ADR. Les
demandes de décision ouvertes et le RACI d'évaluation vivent dans
`docs/collaboration/`.
