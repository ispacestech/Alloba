# Alloba — Architecture du système

Architecture technique de la passerelle Alloba. Complément à
`enterprise-architecture.fr.md` (pourquoi) et `infrastructure.fr.md` (où).

## Composants

```
┌────────────────────────────── Alloba (port 8582) ─────────────────────────────┐
│                                                                                │
│  application fastapi (alloba/main.py)                                          │
│   ├─ middleware CORS (liste d'autorisation depuis ALLOBA_ALLOWED_ORIGINS)      │
│   ├─ /v1/gateway  routers/gateway.py   recherche + chat + santé                │
│   ├─ /v1/sourcing routers/sourcing.py  run + chat + sessions + outils          │
│   └─ /*           proxy.py             proxy transparent vers le backend       │
│                                                                                │
│  moteur de connaissances            agent de sourcing                           │
│  ┌───────────────────────┐           ┌───────────────────────────┐            │
│  │ rag.KnowledgeBase      │           │ sourcing.SourcingAgent     │            │
│  │  chargement FAISS sûr  │◄──────────│  intention → recherche →  │            │
│  │  paresseux             │           │  ancrage → synthèse (LLM) │            │
│  │  similarité + scores   │           └────────────┬──────────────┘            │
│  └───────────┬───────────┘                        │ outils : search_catalog,   │
│              │ faiss_store (index.faiss +         │ get_product, compare,      │
│              │ index.safe.json, sans pickle)      │ compliance_check           │
│              │                                     │                             │
│  OllamaEmbeddings ◄───────────── Ollama ──────────► OllamaClient (chat)         │
└────────────────────────────────────────────────────────────────────────────────┘
```

## Flux de données — recherche RAG

1. `POST /v1/gateway/search` → `kb.search(query, k)`.
2. `KnowledgeBase` charge paresseusement le stockage FAISS sûr depuis
   `ALLOBA_RAG_INDEX_DIR`.
3. La requête est embedded (`OllamaEmbeddings`) puis recherchée via
   `similarity_search_with_scores`.
4. Les distances L2 au carré sont mappées en scores de pertinence 0..1.
5. La réponse renvoie `source`, `score`, `snippet` par résultat.

## Flux de données — chat ancré

1. `POST /v1/gateway/chat` → `kb.chat(query, k)`.
2. Récupérer les top-k chunks → construire un bloc de contexte avec citations.
3. Envoyer un prompt système (« répondre uniquement depuis le contexte, citer les
   sources ») + le contexte à Ollama à basse température (0,2).
4. Si Ollama échoue, `answer` est `None` et seules les `sources` sont renvoyées.
5. Chaque réponse porte ses `sources` pour l'auditabilité.

## Flux de données — sourcing

- **mode pipeline** : extraction d'intention (JSON ou repli par mots-clés) →
  recherche catalogue → ancrage conformité → brief LLM ou gabarit.
- **mode tools** : boucle native d'appel d'outils sur `_TOOL_SCHEMAS` avec
  `search_catalog`, `get_product`, `compare_products`, `compliance_check`.
- **mode auto** : utilise les outils uniquement si le modèle configuré les
  supporte (`ALLOBA_AGENT_TOOL_MODELS`).

## Décisions clés (résumé)

| Décision | Choix | ADR |
| --- | --- | --- |
| Sérialisation | FAISS sûr (binaire + JSON), refuse le pickle | ADR-0002 |
| Interface LLM | Ollama uniquement, local d'abord | ADR-0004 |
| Routage passerelle | routes explicites d'abord, proxy attrape-tout | ADR-0001 |
| Configuration | pydantic-settings, préfixe `ALLOBA_` | ADR-0003 |
| Données catalogue | JSON embarqué dans les données du paquet | ADR-0005 |
| Concurrence | chargement KB paresseux thread-safe | ADR-0006 |

Voir `docs/collaboration/adrs/`.
