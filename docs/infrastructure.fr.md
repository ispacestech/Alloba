# Alloba — Infrastructure

Référence d'hébergement et de déploiement de la passerelle Alloba et du moteur
Alloba Training.

## Topologie cible

```
Navigateur / client
      │ HTTPS
      ▼
 Passerelle Alloba  (alloba/gateway, port 8582)
      │            ├─ /v1/gateway + /v1/sourcing  (local)
      │            └─ /* → proxy
      ▼                     ▼
 ispaces Commerce        Ollama (LLM local)
 backend (8561)          embeddings + chat
      │
      ▼
 PostgreSQL / stockage (appartient au backend)

Navigateur / client formation
      │ HTTPS
      ▼
 Alloba Training  (alloba/training, port 8020)
      │
      ├─ /api/v1 (modules, inscriptions, sessions, certifications, reporting)
      ▼
 PostgreSQL (alloba-training-db)  ·  Ollama (branching génératif optionnel)
```

## Allocation des ports (registre de l'espace de travail)

| Port | Service | Propriétaire |
| --- | --- | --- |
| 8080 | Backend Go ispaces | ispaces |
| 8561 | Backend ispaces Commerce / AfroMART | AfroMART |
| **8582** | **Passerelle Alloba** | **Alloba** |
| **8020** | **API Alloba Training** | **Alloba** |

8582 se situe dans la plage 8500-8599 de l'espace de travail réservée aux
services spécifiques ; 8020 se situe dans la plage backend 8000-8099. Les deux
sont enregistrés dans `../ispaces-design.md` (section Allocation des ports).

## Modes de déploiement

### 1. Développement local

```bash
pip install -e ".[dev]"
python ingest.py
python -m alloba            # 127.0.0.1:8582
```

### 2. Docker Compose (hôte unique)

```bash
docker compose up --build
```

- `ALLOBA_BACKEND_URL` par défaut `http://host.docker.internal:8561` pour des
  backends tournant sur l'hôte ; à surcharger pour un backend conteneurisé.
- Le service `training` utilise sa propre base `training-db` (PostgreSQL) et lit
  les variables `ALLOBA_TRAINING_*` ; en dev local, le défaut est SQLite.
- `rag_index/` est monté en lecture seule pour ne jamais reconstruire l'image à
  chaque rafraîchissement du KB.
- Les mots de passe/secrets utilisent uniquement l'interpolation
  `${VAR:-default}` (règle de l'espace de travail).

### 3. Cloud (Docker Hub + GitHub)

- CI : `.github/workflows/ci.yml` exécute lint + tests ; un workflow de release
  peut pousser `alloba/gateway:<tag>` et `alloba/training:<tag>` vers Docker Hub
  (même image, `CMD` différent).
- L'image est minimale (`python:3.12-slim`), secrets injectés au runtime via
  l'environnement, pas de `debug=True`.

## Dépendances runtime

| Dépendance | Défaut | Requise |
| --- | --- | --- |
| Backend ispaces Commerce | `http://localhost:8561` | oui (routes proxifiées) |
| Serveur Ollama | `http://127.0.0.1:11434` | oui (RAG + sourcing) |
| Modèle d'embedding | `nomic-embed-text` | oui (construction d'index + recherche) |
| Modèle de chat | `llama3.2:1b` | optionnel au runtime (des fallbacks existent) |
| Index FAISS pré-construit | `./rag_index` | oui pour la recherche ; construction via `python ingest.py` |

## Santé et observabilité

- `GET /v1/gateway/health` rapporte la version de la passerelle, l'état du RAG,
  la joignabilité du backend et les endpoints disponibles.
- Le healthcheck Compose interroge cet endpoint.
- Les logs structurés vont sur stdout (collectés par la plateforme hôte).

## Posture de sécurité

- Liste CORS via `ALLOBA_ALLOWED_ORIGINS` (jamais `*`).
- Pas d'index FAISS à base de pickle.
- Secrets uniquement par environnement ; `.env` git-ignoré.
- La terminaison TLS est attendue au proxy inverse/ingress devant la passerelle
  (8582 est interne/à confiance limitée).
