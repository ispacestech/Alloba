# Release Record — Promotion de PipelineConfig

> Enregistrement d'audit (stage 4/6 du runbook). Renseigner avant approbation,
> archiver dans le journal d'audit après déploiement. Écrit uniquement par
> reviewers/promoters (RBAC).

---

## 1. Identification

| Champ | Valeur |
|---|---|
| Config `meta.name` | `_` |
| Version promue (`semver`) | `_` |
| Commit SHA (build) | `_` |
| Tag immuable | `config/_/_/_` |
| Domaine | `rag / guardrail / infra` |
| Environment cible | `staging / production` |
| Date de promotion | `_` |
| Author (platform engineer) | `_` |
| Reviewer (approbateur) | `_` |

## 2. Portes automatiques (rapport CI joint)

- [ ] Stage 1 Validate : schema + invariants + lint + secret_scan verts
- [ ] Stage 2 Test : suites unitaires + intégration domaine + régression vertes
- [ ] Stage 3 Stage : artefact rendu, checksums enregistrés, smoke staging vert
- [ ] Checksum de l'artefact promu vérifié (`sha256sum -c MANIFEST.sha256`)

## 3. Décision humaine

- [ ] Approbation accordée (`approvals_required` satisfait)
- [ ] Justification : `_`
- [ ] Risques connus : `_`

## 4. Déploiement & vérification

- [ ] Apply effectué sur `_`
- [ ] Verify : health + sonde e2e verts
- [ ] Drift check : checksum servi == checksum promu (drift = 0)
- [ ] Canary (si activé) : résultat `_`

## 5. Rollback (si applicable)

- Motif : `_`
- Version immuable de retour : `_`
- Checksum de retour vérifié : `_`
- Incident notifié : `_`

## 6. Rétroaction

- Latence du run (par stade) : `_`
- Portes ayant échoué au premier passage : `_`
- Leçons apprises : `_`
