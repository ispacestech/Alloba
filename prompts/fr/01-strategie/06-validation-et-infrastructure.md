# Phase 1 : Validation & infrastructure (mois 0-3) — cap sur les coûts

Objectif : prouver la demande sans écrire de code ni dépenser d'argent.

| Domaine d'automatisation | Stratégie de stack / outillage (gratuit / serverless) | Rôle de l'agent IA | Étape d'action |
| --- | --- | --- | --- |
| MVP plateforme (e-commerce & audit LLM) | Hébergement : Vercel ou Cloudflare Pages. BDD : Supabase Free Tier. Backend IA : API d'inférence HuggingFace (modèles open source via quantification GGUF pour la sûreté locale/hors ligne) + fonctions serverless. Paiements : Stripe Connect / Flutterwave en mode sandbox uniquement jusqu'à ce que le chiffre d'affaires réel déclenche le modèle de frais. | Agent LLM (assistant code) | Utiliser l'IA pour écrire, déboguer et déployer le code elle-même (IDE Cursor/Windsurf). Pas d'embauche dev pour l'instant ; vous êtes l'architecte/gestionnaire de la sortie de l'agent. |
| Ventes & marketing (génération de leads acheteurs/vendeurs) | Compte LinkedIn gratuit ; automatisation e-mail Brevo/SendGrid free tier ; générateur de contenu : script IA qui collecte légalement les news concurrentes et publie des résumés sur un blog d'entreprise. | Agent de croissance (bot d'outreach) | « Trouver 10 responsables achats en Allemagne qui utilisent SAP Ariba » -> générer un e-mail d'approche personnalisé à partir des prompts de support, envoyé via un auto-répondeur gratuit (Zapier). |
| Opérations (support client) | Constructeur de chatbot (Voiceflow/Tidio gratuits) ; base de connaissances : PDF public de réglementations stocké dans le système RAG pour former immédiatement le bot. | Agent helpdesk | « Suivre ma commande » tire depuis l'API logistique ; « Quels sont vos frais ? » lit le moteur de connaissances. Les requêtes complexes montent en escalade vers un e-mail rédigé par IA avec résumé joint. |
| Validation | Onboarding vendeur en libre-service dans le navigateur (portail ECP). | — | Le système vérifie les données, signale les lacunes et alimente le graphe de connaissances. |

Pas de budget publicitaire : boucle virale organique ciblant les forums
d'achat où les acheteurs postent leurs points de douleur.
