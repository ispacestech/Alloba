# Alloba — Gestion des connaissances

Cycle de vie et gouvernance de la base de connaissances de conformité (`kb/`) et
de l'index FAISS.

## Rôle

La base de connaissances est la source de vérité unique sur laquelle l'IA
s'ancre. Elle est gouvernée, versionnée et reconstruisible à tout moment depuis
`kb/docs/`.

## Politique de contenu

- Seuls des documents approuvés et citables vivent dans `kb/docs/`. Le matériel
  de brouillon n'est pas indexé.
- Chaque document porte des métadonnées de gouvernance (voir `models.py`
  `DocumentMetadata`) : `type`, `status`, `sensitivity_level`.
- Les sources référencées par les tests et les réponses de conformité doivent
  exister dans `kb/docs/` (ex. `00_Conformite_Plateforme.md`,
  `12_Checklist_Conformite_ISO.md`).

## Cycle de vie de l'index

```
éditer kb/docs/* → python ingest.py (ou scripts/build_index.py)
     → découpage (800/150) → embedding (nomic-embed-text) → sauvegarde sûre
     → rag_index/{index.faiss, index.safe.json}
     → la passerelle charge paresseusement et met en cache pour la durée du processus
```

- **Idempotent** : la reconstruction remplace l'index de façon atomique.
- **Sûr uniquement** : les index à base de pickle sont refusés au chargement ; si
  `index.pkl` apparaît, reconstruire avec `python ingest.py`.
- **Rafraîchissement** : modifier `kb/docs/` impose de relancer l'ingestion ; la
  passerelle en cours d'exécution prend le nouvel index au redémarrage.

## Paramètres de découpage

| Paramètre | Valeur | Justification |
| --- | --- | --- |
| chunk_size | 800 | bon équilibre pour de la prose de conformité |
| chunk_overlap | 150 | préserve le contexte aux frontières de chunks |
| k de recherche | 4 (chat), 3 (ancrage) | assez court pour les modèles à faible contexte |

## Élagage du contexte

`context.optimize_context(snippets, token_limit)` ne garde que les extraits les
plus pertinents dans un budget, pour ne pas submerger les modèles à faible
contexte (ex. `llama3.2:1b`).

## Routage des requêtes

- `/v1/gateway/search` — récupération brute, sans LLM.
- `/v1/gateway/chat` — synthèse ancrée avec citations.
- `/v1/sourcing/tools/compliance` — contrôle de conformité utilisé par l'agent
  de sourcing.

## Conservation et audit

- Chaque réponse ancrée renvoie `sources` (piste d'audit).
- `AuditLogEntry` modélise chaque interaction (`read`, `edit`, `generate`).
- Les documents suivent les statuts de gouvernance
  `draft → approved → deprecated` ; `audited` marque un document ayant passé une
  revue formelle.

## Références

- Stockage FAISS sûr : `src/alloba/faiss_store.py`
- Ingestion : `src/alloba/ingestion.py`
- Modèles de gouvernance : `src/alloba/models.py`
