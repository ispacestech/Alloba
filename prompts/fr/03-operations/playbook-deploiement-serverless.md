# Playbook de déploiement serverless (Vercel + Supabase)

Playbook d'application full-stack : guide d'intégration et de sécurité pour les
applications Next.js/React modernes utilisant Supabase. Référence pour la couche
frontend/serverless de la plateforme ; Alloba se déploie lui-même comme
passerelle conteneurisée (voir `docs/infrastructure.fr.md`).

## Plan d'apprentissage

| Phase | Sujet | Durée est. | Objectifs clés |
| --- | --- | --- | --- |
| 1 | Configuration de l'infrastructure Supabase | 45 min | Créer le projet, configurer l'auth (email/Google), le schéma de base et la sécurité au niveau des lignes (RLS). |
| 2 | Intégration client Next.js | 60 min | Installer le SDK Supabase dans le routeur App ou Pages ; configurer `useEffect` pour un chargement sécurisé des données côté client. |
| 3 | Configuration sécurité de l'environnement | 45 min | Maîtriser `.env.local`, les variables d'environnement Vercel, la gestion des clés de rôle de service (backend vs client). |
| 4 | Visualisation de l'architecture | 15 min | Utiliser Mermaid pour schématiser le flux de données : fournisseur d'auth -> route API -> base de données. |

## Règles de sécurité essentielles

- **Côté client (navigateur)** : ne jamais utiliser la clé de rôle de service.
  N'exposer que les clés anon dans `.env.local`.
- **Côté serveur (routes API / edge functions)** : utiliser des chaînes de
  connexion serverless / clés de service injectées au déploiement — jamais de
  secrets codés en dur.
- **Vercel** : `vercel env pull` synchronise les variables de dev locales avec la
  production avant de committer.

Exemple de `.env.local` (ne jamais committer) :

```bash
# .env.local (NE PAS COMMITTER SUR GITHUB)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=...           # clé publique, sûre pour le navigateur
SUPABASE_SERVICE_ROLE_KEY=...               # serveur uniquement, panneau de secrets Vercel
```

## Dépannage

| Symptôme | Cause | Correctif |
| --- | --- | --- |
| `Invalid API key` | Clé de rôle de service utilisée dans le client navigateur. | Passer à la clé anon ; garder le rôle de service côté serveur uniquement. |
| `Connection refused` | Mauvaise URL ou mauvaise configuration CORS. | Paramètres du projet > API : ajouter les origines autorisées ; activer l'accès anon sur les politiques RLS en dev, puis verrouiller en prod. |
| Schéma vide | Migrations non exécutées. | Éditeur SQL : coller le fichier de migration (ex. créer la table users) et rafraîchir. |
| Refus RLS (403/561) | RLS activé mais aucune politique n'autorise l'utilisateur courant. | Authentification > RLS : ajouter des politiques pour `auth.uid()` ; restreindre les lectures privées au propriétaire. |
| `.env` inopérant en dev Vercel | Fichier d'environnement non récupéré. | `vercel env pull` pour synchroniser `.env.example` avec le panneau de secrets. |

## Prochaines étapes

1. Tester le flux de connexion localement avant de déployer les routes API.
2. Déplacer les valeurs sensibles `SERVICE_ROLE_KEY` vers le tableau de bord
   Vercel — ne jamais committer de secrets bruts.
3. Coller le diagramme de flux Mermaid dans le README du dépôt pour la
   documentation d'équipe.
