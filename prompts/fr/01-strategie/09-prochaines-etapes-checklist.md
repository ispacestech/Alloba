# Prochaines étapes — checklist immédiate

- [ ] **Mettre en place les prompts LLM** : copier `CONTRACT-VIGILANCE-01` (voir
  `prompts/fr/02-bibliotheque-prompts/compliance-v1-vigilance-contrats.md`) dans
  le dépôt comme `prompts/compliance_v1.md`. Tester localement sur un contrat
  factice pour vérifier qu'il signale correctement les erreurs sans générer de
  fuites de données sensibles (exigence ISO).
- [ ] **Configurer le pipeline serverless** : créer un compte gratuit sur
  Vercel/Supabase. Lier les clés API des processeurs de paiement uniquement en
  mode sandbox jusqu'à ce qu'un chiffre d'affaires réel apparaisse, pour éviter
  des frais inattendus liés à une forte utilisation.
- [ ] **Automatiser l'entonnoir marketing** : installer un agent IA simple qui
  collecte les offres LinkedIn pour les rôles de « Procurement Manager » en
  UE/US, résume leur activité récente avec les propositions de valeur de la
  plateforme, et rédige un e-mail de pitch à partir des prompts de support,
  envoyé via Zapier/Automation.io.
- [ ] **Valider l'écart ISO** : utiliser les outils juridiques IA mentionnés
  pour générer un « rapport d'auto-évaluation » des exigences ISO/IEC 27001
  propres à l'architecture (cloud + LLM). Ce document est exigé par les acheteurs
  avant les contrats payants.

## Avertissement : financement vs autofinancement

Si à un moment le revenu couvre le salaire d'un développeur, embauchez-le
immédiatement. L'IA ne peut pas encore remplacer la stratégie créative ni les
négociations complexes avec les banques/VC. La feuille de route suppose
**l'autosuffisance** jusqu'à un runway mensuel à six chiffres, puis la transition
vers le recrutement d'une équipe professionnelle.
