# Alloba — Runbook opérations

Procédures opérationnelles pour construire, tester, exécuter, mettre à jour et
sauvegarder la passerelle Alloba. La version anglaise est `operations.en.md`.

## Boucle de construction et de test

```bash
pip install -e ".[dev]"
ruff check .            # lint
ruff format --check .   # format
pytest                  # suite (doit rester verte)
```

Construction du wheel (préparation cloud) :

```bash
pip wheel . --no-deps -w dist/
```

## Exécution locale

```bash
python ingest.py            # reconstruit l'index FAISS depuis kb/docs/
python -m alloba            # sert sur 127.0.0.1:8582
```

Contrôle de santé : `curl http://127.0.0.1:8582/v1/gateway/health`

## Docker

```bash
docker compose up --build
docker compose ps
docker compose logs -f gateway
```

- `rag_index/` est monté en lecture seule, donc une mise à jour de la KB ne
  force jamais la reconstruction de l'image.
- Arrêt : `docker compose down` (ajouter `-v` uniquement pour supprimer les
  données).

## Rafraîchissement de la base de connaissances

1. Ajouter ou modifier des documents dans `kb/docs/`.
2. Reconstruire l'index :

```bash
python ingest.py
```

3. Vérifier le nombre de chunks et que les nouveaux documents sont
   interrogeables :

```bash
python -c "from alloba.rag import KnowledgeBase; kb=KnowledgeBase(); print(kb.search('votre sujet', k=3))"
```

4. L'index n'utilise que la sérialisation sûre (`index.faiss` +
   `index.safe.json`) ; ne jamais le remplacer par un store FAISS basé sur
   pickle.

## Mises à niveau

- Les versions sont portées dans `pyproject.toml` (source de vérité unique).
- Tout changement de comportement doit mettre à jour `docs/specs.*`,
  `docs/architecture.*` et, le cas échéant, un nouvel ADR (voir
  `docs/collaboration/adrs/`).
- Après un changement : lint, format, pytest, reconstruction du wheel, et
  ré-ingestion si le schéma de la KB ou le découpage a changé.

## Sauvegarde

La passerelle est sans état — rien à sauvegarder à l'exécution. Les actifs
durables sont :

| Actif | Emplacement | Action |
| --- | --- | --- |
| Corpus de connaissances | `kb/docs/` | versionné |
| Index construit | `rag_index/` | reconstructible via `python ingest.py` |
| Catalogue | `src/alloba/data/products.json` | versionné |

Aucune base SQL n'est possédée par la passerelle elle-même ; les données
transactionnelles vivent dans le backend auquel elle fait proxy.

## Dépannage

| Symptôme | Cause probable | Action |
| --- | --- | --- |
| 503 sur search/chat | index manquant ou non sûr | exécuter `python ingest.py` |
| 502 sur route non gérée | backend arrêté | démarrer le backend ispaces Commerce |
| Chat LLM renvoie une réponse `null` | Ollama arrêté | vérifier `127.0.0.1:11434` ; les replis ne renvoient que les sources |
| Fondement incorrect/incomplet | index obsolète | reconstruire l'index, vérifier `kb/docs/` |
