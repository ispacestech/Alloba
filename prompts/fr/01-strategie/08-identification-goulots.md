# Plan d'identification et de suppression des goulots d'étranglement

Trois barrières majeures empêchent les PME (surtout sur les marchés émergents)
d'utiliser les plateformes mondiales de sourcing. Le tableau mappe chaque
barrière à une solution lean, sans capital.

| Goulot sectoriel | Pourquoi il bloque l'entrée | Solution plateforme (sans coût / lean) |
| --- | --- | --- |
| « Taxe de confiance » / coût de due diligence. Prouver sa légitimité coûte cher ; les grands acheteurs utilisent des consultants coûteux pour le contrôle. | Filtre les PME de qualité qui ne peuvent pas payer ~50 k$ de logiciels de conformité. | **Moteur d'audit et de gouvernance LLM.** Rendre la conformité gratuite : l'IA fait le travail d'un auditeur à 1 000 $/heure. L'utiliser comme valeur ajoutée pour l'effet de réseau plutôt que de facturer immédiatement. |
| « Silo de conformité » / verrou juridictionnel. Les entreprises du Bénin/Togo ne peuvent pas facilement accéder aux chaînes d'approvisionnement US/UE car les données de la plateforme ne sont pas compatibles avec le RGPD/les lois suisses de sécurité selon l'emplacement du serveur. | Un vendeur à Cotonou est traité comme une « entité à données à risque élevé », exclu des opérations e-commerce européennes (normes Amazon/FairTrade). | **Architecture de cloud souverain.** Du code open source hébergé sur une infrastructure conforme (data centers UE) même si l'entité juridique démarre ailleurs. Utiliser le moteur de connaissances ECP pour combler dynamiquement les écarts réglementaires avant qu'ils ne soient intégrés aux contrats. |
| « Écart de fonds de roulement ». Les acheteurs veulent du net-30 ; les vendeurs ont besoin de liquidités immédiates pour les matières premières. Les banques des marchés émergents refusent sans garantie. | Les plateformes comme Alibaba exigent des dépôts ou des prêts bancaires que la plupart des PME africaines/asiatiques ne peuvent pas obtenir. | **Score de confiance basé sur les transactions.** Une couche d'audit IA crée un « score de confiance » indépendant du score de crédit (basé sur l'historique d'exécution des commandes). Intégrer des fournisseurs de paiement qui acceptent ce signal de confiance pour des paiements immédiats, plutôt que de bloquer des fonds en escrow. |

## Stratégie de suppression

- **Mois 0-3** : lancer un moteur d'audit LLM en free tier pour les vendeurs en
  échange de leurs données propres. Cela construit le graphe de connaissances
  conforme ISO.
- **Mois 4+** : utiliser le marketing de contenu généré par IA (depuis la
  bibliothèque de prompts) pour démontrer automatiquement les normes de
  conformité, réduisant le coût d'acquisition client d'environ 80 %.

## Application à Alloba

- Des contrôles de conformité gratuits sont exposés via
  `POST /v1/sourcing/tools/compliance` et ancrés dans les sources `kb/docs/`.
- Le principe de « cloud souverain » correspond à
  `kb/docs/06_Data_Sovereignty_Africa.md` et à l'ADR-0004 (Ollama local d'abord).
