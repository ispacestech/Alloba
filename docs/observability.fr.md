# Alloba — Observabilité

Comment la passerelle Alloba rapporte santé, journaux, métriques et piste
d'audit. La version anglaise est `observability.en.md`.

## Point de santé

`GET /v1/gateway/health` renvoie :

| Champ | Signification |
| --- | --- |
| `service` | `"alloba"` |
| `version` | version du paquet |
| `rag` | état de chargement de l'index (`loaded` / `missing` / `unsafe`) |
| `backend` | joignabilité du backend ispaces (`ok` / `unreachable`) |
| `endpoints` | liste des routes enregistrées |

Utilisé par le healthcheck Docker (intervalle 10 s, délai 2 s, 3 tentatives).
Un index manquant ne fait pas échouer le healthcheck mais est signalé pour que
les opérateurs puissent le reconstruire.

## Journaux

- Les journaux structurés vont sur stdout (lignes JSON), collectés par la
  plateforme hôte (logs Docker, logger cloud, systemd).
- Les événements de requête journalisent méthode, chemin, statut, durée et id
  de corrélation.
- Les entrées d'audit suivent `AuditLogEntry` (`src/alloba/models.py`) et sont
  émises pour les actions IA à conséquences : exécutions de sourcing,
  vérifications de conformité, déclenchements d'audit LLM.

## Auditiabilité (Ethics by design)

- Chaque tour de chat et de sourcing porte un id traçable.
- Les briefs de sourcing enregistrent les outils utilisés et les sources
  citées.
- Le moteur de connaissances refuse les index basés sur pickle, donc ce qui est
  indexé est exactement ce qui se trouve dans `kb/docs/`.

## Métriques (feuille de route)

Un futur `/v1/metrics` (format Prometheus) est prévu : percentiles de latence
RAG, décomptes d'exécutions de sourcing par issue, taux d'échec LLM. L'issue de
suivi et l'ADR accompagneront l'implémentation.

## Signaux de dépannage

| Signal | Interprétation | Action |
| --- | --- | --- |
| `rag: missing` dans health | index jamais construit | `python ingest.py` |
| `backend: unreachable` | cible de proxy arrêtée | démarrer le backend, vérifier CORS/URL |
| réponses `null` répétées au chat | LLM arrêté ou contexte pauvre | vérifier Ollama, rafraîchir la KB |
| recherche lente | corpus volumineux, sans limite | vérifier le clamp `k` `[1,20]`, taille des chunks |
