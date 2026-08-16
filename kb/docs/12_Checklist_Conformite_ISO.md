# Checklist de conformité ISO 27001 — SMSI

Cette checklist opérationnelle est utilisée pour auditer le système de
management de la sécurité de l'information (SMSI) de la plateforme.

## 1. Politique de sécurité

- [ ] Une politique de sécurité de l'information est écrite, approuvée et diffusée.
- [ ] La politique est révisée au moins une fois par an.
- [ ] Les responsabilités sécurité sont assignées et documentées.

## 2. Organisation de la sécurité

- [ ] Un comité de pilotage sécurité existe.
- [ ] Les rôles et responsabilités (RACI) sont définis pour chaque processus.
- [ ] La sécurité est intégrée à la gestion de projet (CLD / SSDLC).

## 3. Gestion des actifs

- [ ] Un inventaire des actifs informationnels existe et est maintenu.
- [ ] La classification des données (PUBLIC / INTERNAL / RESTRICTED / CONFIDENTIAL) est appliquée.
- [ ] Les supports de stockage sont contrôlés et tracés.

## 4. Contrôle d'accès

- [ ] Le principe du moindre privilège est appliqué.
- [ ] La revue des accès est effectuée tous les trimestres.
- [ ] L'authentification multifacteur (MFA) est activée sur les comptes privilégiés.
- [ ] Les comptes désaffectés sont supprimés sous 30 jours.

## 5. Cryptographie

- [ ] Les données en transit sont chiffrées (TLS 1.2+).
- [ ] Les données au repos sont chiffrées (AES-256 ou équivalent).
- [ ] Les clés sont gérées par un coffre-fort de clés (KMS / Vault) et ne sont jamais committées.

## 6. Sécurité physique et environnementale

- [ ] L'accès physique aux serveurs est contrôlé et journalisé.
- [ ] La redondance électrique et de refroidissement est assurée.
- [ ] Les zones sensibles sont délimitées.

## 7. Sécurité des opérations

- [ ] Les journaux (logs) sont centralisés et conservés 12 mois.
- [ ] Les sauvegardes sont testées (restauration) au moins une fois par trimestre.
- [ ] La gestion des vulnérabilités est planifiée et suivie.
- [ ] Un plan de réponse aux incidents existe et a été exercé.

## 8. Sécurité des communications

- [ ] Le réseau est segmenté (front, back, données, IA).
- [ ] Les accès distants passent par un VPN / tunnel chiffré.
- [ ] Les API sont authentifiées et limitées en débit (rate limiting).

## 9. Relations avec les fournisseurs

- [ ] Les accords de niveau de service (SLA) incluent des clauses de sécurité.
- [ ] Les sous-traitants sont audités ou auto-évalués chaque année.
- [ ] La chaîne d'approvisionnement logicielle (dépendances) est contrôlée.

## 10. Continuité d'activité

- [ ] Une analyse d'impact sur la continuité d'activité (BIA) est réalisée.
- [ ] Un plan de reprise d'activité (PRA) et un plan de continuité (PCA) existent.
- [ ] Les objectifs de point de reprise (RPO) et de temps de reprise (RTO) sont définis.

## 11. Conformité

- [ ] La veille réglementaire (RGPD, AI Act, lois locales) est active.
- [ ] Les audits internes et externes sont planifiés.
- [ ] La politique de sauvegarde est conforme aux obligations légales.

Chaque case non cochée doit être justifiée par une décision acceptée (exception
temporaire, risque accepté) et tracée dans le registre des risques.
