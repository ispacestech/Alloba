# Pile d'infrastructure (chaîne d'outillage prévue)

La stack lean et open source considérée pour les couches non-passerelle de la
plateforme. Alloba lui-même ne nécessite que Ollama + un backend (voir
`docs/infrastructure.fr.md`).

| Outil | Rôle | Statut dans Alloba |
| --- | --- | --- |
| Ollama | Runtime LLM local (chat + embeddings) | Utilisé (ADR-0004) |
| Strapi | CMS headless (contenu) | Couche plateforme (optionnel) |
| Appwrite | Backend-as-a-service (auth, BDD, stockage) | Couche plateforme (optionnel) |
| Novu | Notifications | Couche plateforme (optionnel) |
| ToolJet | Outillage interne low-code | Couche plateforme (optionnel) |
| Medusa | Moteur de commerce headless | Couche plateforme (optionnel) |

## Plan

1. Garder Alloba mince : uniquement FastAPI + Ollama + FAISS sûr.
2. Repousser contenu/commerce/notifications vers le backend plateforme (8561)
   et les services optionnels ci-dessus.
3. Enregistrer le port de chaque nouveau service dans le tableau des ports de
   l'espace de travail (`ispaces-design.md`) dès sa mise en service.

## GETI (guidance)

« GETI » renvoie ici à générer, évaluer, tester et itérer les décisions
d'infrastructure — enregistrer chaque changement comme ADR avant de brancher de
nouveaux services dans les fichiers compose.
