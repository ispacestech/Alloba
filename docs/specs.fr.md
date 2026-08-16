# Alloba — Spécifications

Ligne de base des spécifications fonctionnelles et techniques. Tout changement
de comportement met à jour ce document et `architecture.fr.md`, et est
enregistré en ADR.

## Exigences fonctionnelles

### FR-1 Passerelle proxy
- **FR-1.1** La passerelle expose une origine unique et transmet de façon
  transparente toute route non gérée vers `ALLOBA_BACKEND_URL`.
- **FR-1.2** Les réponses préservent statut, en-têtes et corps ; une erreur 502
  JSON est renvoyée quand le backend est injoignable.
- **FR-1.3** `GET /` renvoie `{service, version, docs}`.

### FR-2 Recherche RAG
- **FR-2.1** `POST /v1/gateway/search` renvoie des résultats classés avec
  `source`, `score`, `snippet`.
- **FR-2.2** `k` est borné à `[1, 20]` ; les requêtes vides sont rejetées (422).
- **FR-2.3** Index manquant ou non sûr → 503 avec instruction de reconstruction.

### FR-3 Chat ancré
- **FR-3.1** `POST /v1/gateway/chat` renvoie `answer`, `model`, `sources`.
- **FR-3.2** La réponse doit être ancrée : le prompt système interdit les
  réponses hors contexte ; en cas d'échec LLM, `answer` est `null` et les
  `sources` sont quand même renvoyées.

### FR-4 Sourcing
- **FR-4.1** `POST /v1/sourcing/run` renvoie intention, résultats, sources et un
  brief. Le brief retombe sur un gabarit déterministe si le LLM est indisponible.
- **FR-4.2** `POST /v1/sourcing/chat` gère les sessions ; `GET
  /v1/sourcing/sessions/{id}` en récupère une (404 si absente).
- **FR-4.3** Les endpoints d'outils `search`, `product`, `compare`, `compliance`
  sont appelables directement et par l'agent.

### FR-5 Moteur de conformité
- **FR-5.1** Les réponses de conformité citent leurs documents sources.
- **FR-5.2** L'index est construit depuis `kb/docs/` par `python ingest.py` (ou
  `scripts/build_index.py`) et stocké en sérialisation sûre uniquement.

## Exigences non fonctionnelles

### NFR-1 Sécurité (politique de l'espace de travail)
- Pas de FAISS par pickle ; pas de `allow_dangerous_deserialization`.
- CORS restreint à la liste d'autorisation ; jamais `*`.
- Pas de secrets commités ; docker-compose utilise `${VAR:-default}`.
- Pas de `debug=True` dans les points d'entrée de production.

### NFR-2 Performance
- Timeout du proxy : 60 s ; timeout du health check : 2 s.
- Le KB est chargé paresseusement une fois puis mis en cache pour la durée du
  processus.

### NFR-3 Fiabilité
- Une panne LLM dégrade vers des gabarits, jamais vers un crash.
- Une panne backend dégrade vers un 502 JSON, jamais vers une connexion pendante.

### NFR-4 Bilinguisme
- Tous les documents destinés aux utilisateurs existent en EN et FR.
- L'assistant répond dans la langue de l'utilisateur.

### NFR-5 Tests
- La suite (29 tests) doit rester verte ; la CI exécute ruff + pytest sur chaque PR.

## Contrat de configuration

Préfixe `ALLOBA_`. Voir `.env.example` pour le tableau complet. Les valeurs
invalides doivent échouer rapidement au démarrage (validation pydantic-settings).

## Surface API (résumé)

| Méthode | Chemin | Rôle |
| --- | --- | --- |
| GET | `/` | infos de service |
| GET | `/v1/gateway/health` | santé + état RAG + backend |
| POST | `/v1/gateway/search` | recherche RAG |
| POST | `/v1/gateway/chat` | chat ancré |
| POST | `/v1/sourcing/run` | exécution complète de sourcing |
| POST | `/v1/sourcing/chat` | sourcing conversationnel |
| GET | `/v1/sourcing/sessions/{id}` | état de session |
| GET | `/v1/sourcing/catalog` | métadonnées catalogue |
| POST | `/v1/sourcing/tools/*` | outils de l'agent |
| /* | tout | proxy vers le backend |
