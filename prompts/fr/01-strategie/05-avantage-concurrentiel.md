# L'avantage concurrentiel : bâtir la confiance sans argent

Pour gagner le marché mondial du sourcing B2B, il ne faut pas être moins cher —
il faut être **digne de confiance**.

## Le protocole « Bootstrap Security »

Comme une équipe SOC dédiée est inabordable au départ :

- **Analyse automatisée** : déployer des scanners open source (ex. Trivy pour
  les conteneurs) dans la CI/CD à chaque commit. Cela empêche le déploiement de
  vulnérabilités et réduit le travail de sécurité manuel à presque zéro.
- **Minimisation des données par conception** : configurer le moteur de
  connaissances ECP pour ne stocker localement que les données de conformité
  essentielles et hacher le reste avant tout envoi vers un traitement IA. Les
  journaux sensibles (chiffrés) vs publics sont stockés différemment
  automatiquement via des scripts, pas du travail administratif manuel.
- **Gouvernance open source** : publier le schéma des journaux d'audit sur
  GitHub sous licence. Un outil ouvert et conforme rend les acheteurs confiants
  qu'aucune donnée n'est cachée dans du code IA en boîte noire. Cela remplace les
  audits de sécurité fournisseurs coûteux pour les premiers clients qui
  valorisent la transparence face aux écosystèmes fermés.

## Application à Alloba

- La CI exécute `ruff` + `pytest` sur chaque PR (voir `.github/workflows/ci.yml`).
- Le stockage FAISS est sérialisé en mode sûr (sans pickle) et les modèles
  d'audit sont publics (`src/alloba/models.py`).
- Les réponses de conformité citent toujours leurs sources — la transparence
  comme fonctionnalité produit.
