# Alloba

Alloba est la passerelle et le service de sourcing agentique  organisé en monorepo propre et prêt pour le cloud.
Il héberge aussi **Alloba Training**, le moteur de micro-formation immersive et
de certification .

> Version : 0.3.0 · Licence : MIT · English : see [README.md](README.md)

## Ce qu'il fait

- **Passerelle API** — un point d'entrée unique qui proxye de façon
  transparente toutes les routes plateforme vers le backend ispaces Commerce
  (défaut `http://localhost:8561`).
- **Moteur de connaissances de conformité IA éthique** — RAG ancré sur les
  documents de conformité (`kb/docs/`) utilisant un index FAISS **sûr**
  (binaire + JSON, sans pickle, sans `allow_dangerous_deserialization`).
- **Sourcing agentique** — pipeline orchestré et (optionnellement) boucle
  native d'appel d'outils qui produit des briefs de sourcing ancrés sur le
  catalogue et le contexte de conformité.
- **Alloba Training** — moteur de micro-formation immersive VR/AR et de
  certification (branching de scénarios, scoring par compétence, télémétrie
  d'engagement, export RH).

## Arborescence du dépôt

```
.
├── src/alloba/          # passerelle + moteur de connaissances + agent de sourcing
│   ├── faiss_store.py   # stockage FAISS sûr (sans pickle — exigence de sécurité)
│   ├── rag.py           # KnowledgeBase (chargement paresseux, chat ancré)
│   ├── ingestion.py     # construction d'index (découpage → embedding → sauvegarde sûre)
│   ├── context.py       # élagage de contexte sous budget de jetons
│   ├── models.py        # modèles de gouvernance (DocumentMetadata, RAGResponse, AuditLogEntry)
│   ├── catalog.py       # catalogue fournisseurs embarqué (55 produits)
│   ├── sourcing.py      # SourcingAgent (pipeline + boucle d'outils)
│   ├── proxy.py         # proxy transparent vers le backend
│   ├── routers/         # endpoints /v1/gateway et /v1/sourcing
│   └── training/        # Alloba Training — API de micro-formation/certification immersive
├── kb/docs/             # documents de conformité (ingérés par le RAG)
├── prompts/             # bibliothèque de prompts bilingue (en/fr) (incl. prompts d'agents)
├── docs/                # marque, architecture, collaboration — versions EN + FR
│   └── ci-scaffold/     # workflow de release PipelineConfig (runbook + templates)
├── scripts/             # new-adr.py, build_index.py
├── serverless/          # notes de déploiement serverless du moteur de connaissances
├── tests/               # suite pytest (passerelle + training)
├── brand/               # marques SVG (ispaces + Alloba/AfroMART)
├── ssl/                 # matériel TLS local pour Ollama (ignoré par git)
└── archive/original/    # copie de provenance des sources pré-rebrand
```

## Démarrage rapide

Prérequis : Python 3.11+, [Ollama](https://ollama.com) démarré avec
`llama3.2:1b` et `nomic-embed-text`.

```bash
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -e ".[dev]"
python ingest.py          # construire l'index FAISS depuis kb/docs
python -m alloba          # démarrer la passerelle sur 127.0.0.1:8582
```

Démarrer l'API Alloba Training séparément (SQLite en dev) :

```bash
uvicorn alloba.training.main:app --reload --port 8020   # docs sur /docs
```

Ou avec Docker :

```bash
docker compose up --build
```

Ouvrez <http://127.0.0.1:8582/v1/docs> pour la documentation interactive de l'API.

## Configuration

Tous les réglages se lisent depuis des variables d'environnement préfixées
`ALLOBA_` (voir [`.env.example`](.env.example)). Ne codez jamais de secrets en
dur — copiez `.env.example` vers `.env` et gardez `.env` hors du contrôle de
version.

| Variable | Défaut | Rôle |
| --- | --- | --- |
| `ALLOBA_BACKEND_URL` | `http://localhost:8561` | Backend plateforme à proxier |
| `ALLOBA_PORT` | `8582` | Port de la passerelle |
| `ALLOBA_RAG_INDEX_DIR` | `./rag_index` | Emplacement de l'index FAISS |
| `ALLOBA_RAG_DOCS_DIR` | `./kb/docs` | Documents de connaissances à indexer |
| `ALLOBA_OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Point de terminaison Ollama |
| `ALLOBA_LLM_MODEL` | `llama3.2:1b` | Modèle chat/sourcing |
| `ALLOBA_EMBEDDING_MODEL` | `nomic-embed-text` | Modèle d'embedding |
| `ALLOBA_AGENT_MODE` | `auto` | `pipeline` \| `tools` \| `auto` |
| `ALLOBA_ALLOWED_ORIGINS` | liste séparée par virgules | Liste CORS — jamais `*` |

Alloba Training lit ses propres variables sous le préfixe `ALLOBA_TRAINING_`
(`ALLOBA_TRAINING_DATABASE_URL`, `ALLOBA_TRAINING_ALLOWED_ORIGINS`,
`ALLOBA_TRAINING_API_KEY`, `ALLOBA_TRAINING_OLLAMA_BASE_URL`,
`ALLOBA_TRAINING_OLLAMA_MODEL` — voir [`.env.example`](.env.example)).

## Tests

```bash
python -m pytest -q        # suites passerelle + training
python -m ruff check src tests ingest.py scripts
python -m ruff format --check src tests ingest.py scripts
```

## Notes de sécurité (politique de l'espace de travail)

- Les index FAISS sont sérialisés **sans pickle** (`index.faiss` +
  `index.safe.json`). Les index non sûrs sont refusés et doivent être reconstruits.
- Le CORS est toujours restreint via `ALLOBA_ALLOWED_ORIGINS` — jamais `*`.
- Pas de `debug=True`, pas de secrets commités, les mots de passe docker-compose
  utilisent l'interpolation `${VAR:-default}`.
- Le nommage des variables d'env utilise le préfixe projet `ALLOBA_` ; les
  variables d'infrastructure partagées (`OLLAMA_BASE_URL`, etc.) restent nues
  dans les fichiers compose partagés.

## Publication cloud

- CI GitHub Actions : `.github/workflows/ci.yml` exécute lint + tests sur
  push/PR.
- L'image se construit avec `docker build -t alloba/gateway:0.3.0 .` et se pousse
  vers Docker Hub sous un namespace `alloba/*` (`alloba/gateway` et
  `alloba/training` partagent la même image ; seul le `CMD` diffère).

## Index de documentation

- [docs/README.md](docs/README.md) — index de la documentation EN/FR.
- [docs/architecture.fr.md](docs/architecture.fr.md) — architecture du système.
- [docs/enterprise-architecture.fr.md](docs/enterprise-architecture.fr.md) —
  alignement métier/IT.
- [docs/infrastructure.fr.md](docs/infrastructure.fr.md) — hébergement et déploiement.
- [docs/specs.fr.md](docs/specs.fr.md) — spécifications fonctionnelles et techniques.
- [docs/knowledge-management.fr.md](docs/knowledge-management.fr.md) — cycle de vie du KB RAG.
- [docs/collaboration/system.fr.md](docs/collaboration/system.fr.md) — le système
  de collaboration (workflow, RACI, ADRs).

## Remerciements

Système de marque par **ispaces** (« Ethics by design. ») et **AfroMART**
(« Trade that grows Africa. ») — voir `brand/` et `docs/brand.fr.md`.
