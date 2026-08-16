# Alloba — Journal des décisions

Résumé chronologique des décisions d'architecture et de gouvernance. Chaque
entrée pointe vers son ADR. La version anglaise est `decision-log.en.md`.

| # | Date | Décision | Statut | ADR |
| --- | --- | --- | --- | --- |
| 1 | 2026-08-15 | Routage de la passerelle : routes explicites d'abord, proxy transparent pour le reste | Acceptée | [0001](adrs/0001-gateway-routing.md) |
| 2 | 2026-08-15 | Sérialisation FAISS sûre : index binaire + docstore JSON, sans pickle, sans `allow_dangerous_deserialization` | Acceptée | [0002](adrs/0002-safe-faiss-serialization.md) |
| 3 | 2026-08-15 | Configuration via pydantic-settings avec préfixe d'env `ALLOBA_` | Acceptée | [0003](adrs/0003-configuration-prefix.md) |
| 4 | 2026-08-15 | Interface LLM locale d'abord (Ollama) ; un fournisseur cloud exige un nouvel ADR | Acceptée | [0004](adrs/0004-local-first-ollama.md) |
| 5 | 2026-08-15 | Catalogue fournisseurs embarqué comme données de paquet (`data/products.json`, 55 produits) | Acceptée | [0005](adrs/0005-bundled-catalog.md) |
| 6 | 2026-08-15 | Chargement paresseux thread-safe de la base de connaissances ; index manquant → 503 avec instruction de reconstruction | Acceptée | [0006](adrs/0006-lazy-kb-loading.md) |

## Processus

Les nouvelles décisions suivent le workflow de `system.fr.md` : demande de
décision → revue → ADR → implémentation → CI → clôture.
