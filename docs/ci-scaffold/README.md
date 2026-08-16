# Pipeline Config Release Workflow

> Runbook end-to-end qu'un platform engineer exécute pour produire une configuration
> de pipeline de **haute qualité**, de façon **répétée**. Livré en docs + templates
> (aucun code exécutable) : les YAML se branchent sur l'outillage CI/CD existant
> (GitHub Actions, GitLab CI, …) et les commandes citées utilisent les outils déjà
> présents dans l'espace de travail (ruff, pytest, docker compose, endpoints ispaces).

---

## 1. Objectif

Produire, valider, tester et promouvoir un artefact — la **PipelineConfig** — à travers
les environnements, avec la même qualité à chaque exécution. Le workflow est un
**scaffold CI générique** : il s'applique à n'importe quel domaine de pipeline
(RAG, garde-fous/modération, infrastructure) en branchant un *adaptateur de domaine*
(stage 2 et stage 5).

### Principes (le « contrat de qualité »)

| Principe | Exigence |
|---|---|
| **Déterministe** | même `config + commit` → même artefact (checksum identique) |
| **Immuable** | une config promue n'est jamais modifiée — une évolution = une nouvelle version |
| **Versionné** | bump de `semver` obligatoire ; jamais d'écrasement |
| **Audité** | chaque promotion a un *release record* signé (RBAC) |
| **Réversible** | rollback documenté vers la version immuable précédente |
| **Gaté** | promotion impossible sans passage des portes machine **et** humaines |
| **Répétable** | paramétré par matrice env/branche ; verrou concurrency ; métriques à chaque run |

Le modèle « **Fondement vs Vue** » de l'espace de travail s'applique ici : la
PipelineConfig est le *Fondement* (immuable) ; les vues rendues par environnement
(staging, production) sont des *Vues* jetables dérivées à la demande.

---

## 2. L'artefact : PipelineConfig

Une PipelineConfig est un fichier YAML unique, immuable, versionné, vivant dans
`config/<domaine>/<nom>/<nom>.<semver>.yaml`. Modèle : `templates/pipeline-config.template.yaml`.
Schéma de validation : `schema/pipeline-config.schema.json`.

```yaml
api_version: pipeline/v1
meta:
  name: rag-main-index          # nom unique de config
  semver: 1.2.0                 # version sémantique
  domain: rag                   # rag | guardrail | infra
  owner_team: platform
spec:
  stages:                       # stades activés/désactivés
    validate: { enabled: true }
    test: { enabled: true }
    promote: { strategy: manual, approvals_required: 1 }
  gates:
    required: [schema, invariants, lint, secret_scan, tests]
  parameters:                   # matrice env → valeurs effectives
    staging: { ... }
    production: { ... }
  rollback:
    keep_previous_versions: 3
```

**Règle d'or** : une config promue est figée. Toute correction crée une nouvelle
version (`semver` patch) ; on ne mute jamais une config déjà promue.

---

## 3. Rôles

| Rôle | Actions |
|---|---|
| **Platform engineer** | autorise (stage 0), relance/annule les runs, lit les rapports, rédige le release record |
| **Reviewer** | approuve la promotion (porte humaine, stage 4) |
| **CI bot** | exécute les portes automatiques (stages 1-3, 5) ; ne décide jamais seul de promouvoir en production |

---

## 4. Le workflow bout en bout

```
[0] Author        ── candidate config + branche + PR
       │  (humain, checklist)
       ▼
[1] Validate      ── schema + invariants sémantiques + lint + secret scan
       │  (CI, automatique)
       ▼
[2] Test          ── tests unitaires + intégration (adaptateur de domaine)
       │  (CI, automatique)
       ▼
[3] Stage         ── rendu des vues + artefacts immuables (checksum) + smoke staging
       │  (CI, automatique)
       ▼
[4] Promote       ── portes auto ✓ + approbation humaine → version figée + release record
       │  (humain + CI)
       ▼
[5] Deploy+Verify ── application prod + canary + drift check + rollback
       │  (CI, automatique)
       ▼
[6] Observe       ── audit, métriques, changelog, leçons → nourrit les templates
       (continu)
```

**Invariant de déroulement** : un stade ne commence que si toutes les portes du
stade précédent sont vertes. Un run échoué laisse les environnements inchangés
(la config n'est jamais « à moitié » appliquée).

---

## 5. Stades, portes et checklists

### Stage 0 — Author (local, platform engineer)

**Objectif** : créer une candidate config à partir du template et d'une matrice
de paramètres, sans ressaisie manuelle du pipeline.

**Étapes**
1. Partir de `main` propre : `git checkout -b pipeline-config/<nom>/<semver>`.
2. Copier `templates/pipeline-config.template.yaml` →
   `config/<domaine>/<nom>/<nom>.<semver>.yaml`.
3. Renseigner `meta` (nom, semver, domaine, owner_team).
4. Configurer `spec.stages` et `spec.gates`.
5. Remplir `spec.parameters` (valeurs par environnement depuis la matrice).
6. Auto-vérification (checklist ci-dessous) puis ouvrir la PR.

**Checklist du platform engineer**
- [ ] Branche nommée `pipeline-config/<nom>/<semver>` ; seule la config a changé
- [ ] `semver` cohérent avec le changelog (majeur/mineur/patch justifié)
- [ ] `domain` ∈ {rag, guardrail, infra} ; `owner_team` renseigné
- [ ] Aucun secret littéral dans le fichier (placeholders `${PIPELINE_*}` uniquement)
- [ ] `rollback.keep_previous_versions ≥ 1` pour tout déploiement en production

---

### Stage 1 — Validate (CI, automatique)

**Objectif** : vérifier par la machine que la config est structurellement et
sémantiquement valide.

| Porte | Commande (existant) | Critère |
|---|---|---|
| **Schema** | `ajv validate -s schema/pipeline-config.schema.json -d config/...yaml` (ou `python -m jsonschema`) | conforme au schéma |
| **Invariants sémantiques** | règles croisées (voir §6) | toutes les invariants passent |
| **Lint** | `yamllint` / analyse YAML | YAML bien formé, indent 2 espaces, pas de whitespace de fin |
| **Secret scan** | `gitleaks detect` / `rg "api_key\\s*[:=]"` | aucun secret littéral |

**Checklist**
- [ ] Rapport de validation généré (machine-readable) et joint à la PR
- [ ] Les 4 portes sont vertes
- [ ] Les seuls diffs sont dans `config/<domaine>/<nom>/` et le release record

---

### Stage 2 — Test (CI, automatique)

**Objectif** : prouver que la config fonctionne réellement dans un environnement
isolé, via l'**adaptateur de domaine**.

| Domaine | Suites (outillage existant) |
|---|---|
| **rag** | `pytest` (invariants config) ; rebuild index sur staging (`POST /v1/rag/rebuild`) ; smoke query (`POST /v1/rag/query`) avec assertion de récupération |
| **guardrail** | `pytest` ; application de politique (`POST /api/v1/admin/guardrail/configure/policies`) ; fixtures propre/bloqué sur `POST /api/v1/guardrails/check` |
| **infra** | `docker compose config -q` ; `docker compose up -d` sur staging ; attente `/health` |

**Checklist**
- [ ] Tests unitaires de la config (schéma + invariants) : verts
- [ ] Intégration domaine (adaptateur) : verts
- [ ] Régression (`ruff check` + `pytest` du projet cible) : verte

---

### Stage 3 — Stage & artefacts (CI, automatique)

**Objectif** : produire des artefacts **déterministes et immuables** à partir de la
config, puis les vérifier sur staging.

**Étapes**
1. Rendu des vues : résoudre les paramètres par environnement (Fondement → Vue).
   Rendu **déterministe** : clés triées, aucun horodatage — même entrée → mêmes octets.
2. Génération des blocs `.env` (placeholders `${PIPELINE_*}` → valeurs du store).
3. Empaquetage + `SHA256` de chaque artefact.
4. Publication dans le store d'artefacts (manifest : semver + commit SHA + checksums).
5. Application staging + smoke test (health + sonde e2e du domaine).

**Checklist**
- [ ] Checksums enregistrés dans le manifest ; re-run → checksums identiques
- [ ] Smoke staging vert
- [ ] Manifest taggé `config/<nom>/<semver>/<sha-court>`

---

### Stage 4 — Promote (automatique + humain)

**Objectif** : figer la version candidate comme version promue.

**Portes automatiques** : stages 1-3 verts, checksum de l'artefact vérifié, staging
vérifié, verrou concurrency détenu.

**Porte humaine** : un reviewer approuve via le *release record*
(`templates/release-record.template.md`). `approvals_required` est configuré dans
`spec.stages.promote` (≥ 1 pour la production).

**Conséquence** : la config est **figée** — un nouvel édit crée une nouvelle version ;
le tag `config/<nom>/<semver>` devient immuable.

**Checklist**
- [ ] Portes automatiques vertes (rapport joint)
- [ ] Release record signé (date, versions, checksums, décisions, reviewer)
- [ ] Tag immuable créé ; aucun diff autorisé par la suite

---

### Stage 5 — Deploy & Verify (CI, automatique)

**Objectif** : appliquer en production et prouver que l'environnement sert **exactement**
la version promue.

**Étapes**
1. Application (canary optionnel si le domaine le permet).
2. Vérifications : health, sonde e2e, **drift check** (checksum servi == checksum de l'artefact).
3. En échec → **rollback automatique** vers la version immuable précédente
   (`rollback.keep_previous_versions`).

**Checklist**
- [ ] Verify green (health + e2e)
- [ ] Drift = 0 (checksum servi == checksum promu)
- [ ] Si rollback : release record mis à jour (motif, version de retour), incident notifié

---

### Stage 6 — Observe & learn (continu)

**Objectif** : boucler la rétroaction pour que le prochain run soit encore plus
rapide et fiable.

**Étapes**
1. Archivage du release record dans le journal d'audit (RBAC : seuls reviewers/promoters écrivent).
2. Métriques : latence par stade, taux d'échec des portes, taux de rollback.
3. Mise à jour du changelog et des leçons apprises (→ mise à jour du runbook et des templates).
4. Nettoyage : suppression des branches `pipeline-config/*` fusionnées, rétention du store.

**Checklist**
- [ ] Release record archivé ; métriques du run enregistrées
- [ ] Changelog mis à jour
- [ ] Nettoyage exécuté (branches + rétention artefacts)

---

## 6. Invariants sémantiques (portes machine)

Règles croisées de validation, indépendantes du domaine, à vérifier au stage 1 :

1. `meta.semver` respecte `major.minor.patch` (`^\d+\.\d+\.\d+$`).
2. `meta.domain` ∈ {rag, guardrail, infra}.
3. `spec.stages.validate.enabled` et `spec.stages.test.enabled` sont `true` pour
   toute config destinée à la production.
4. `spec.stages.promote.approvals_required ≥ 1` si `parameters.production` existe.
5. `spec.gates.required` est non vide et ne contient que des portes connues.
6. `spec.rollback.keep_previous_versions ≥ 1` si un environnement `production` est défini.
7. Les valeurs de `spec.parameters` sont toutes des scalaires/tableaux (pas de structures
   récursives), et les noms d'environnement sont uniques.
8. Aucune valeur ne contient de motif de secret (mot clés `token`, `secret`, `password`,
   `api_key` avec valeur littérale non vide).

Ces invariants sont codés dans l'outil de validation branché au stage 1 ; ce runbook
en est la source de vérité documentaire. Chaque invariant a un cas de test dans la
suite du stage 2 (régression).

---

## 7. Répétabilité (le « repeatedly »)

| Mécanisme | Implémentation |
|---|---|
| **Idempotence** | rendu déterministe + checksum ; rejouer un run validé ne change rien |
| **Versionnement** | `semver` obligatoire ; jamais d'overwrite ; tag immuable par version |
| **Paramétrage** | la matrice env/branche est la SEULE source de variation ; le pipeline lui-même ne change pas entre deux runs |
| **Verrouillage** | 1 run simultané par `nom` de config (mutex CI) → pas de course |
| **Mesure** | latence + résultat enregistrés à chaque run (stage 6) |
| **Rétention** | `keep_previous_versions` borne le nombre de versions conservées |

**Matrice type** : branche `main` → environment `production` ; branche `dev`/PR →
environment `staging`. Le mapping branche→env est centralisé (pas de dérive). La
branche ne pilote que l'environnement **rendu** (stages 1-3) : le déploiement
(stage 5) n'est déclenché que par la **promotion manuelle** (`workflow_dispatch`),
jamais par un push ou une PR — le CI bot ne déploie jamais seul.

---

## 8. Rollback & réversibilité

- Chaque promotion garde les versions immuables précédentes (`keep_previous_versions`).
- Procédure : (1) récupérer la version immuable précédente dans le store, (2) vérifier
  son checksum, (3) appliquer, (4) vérifier drift = 0.
- Le release record documente chaque retour arrière (motif + version cible).
- En production, le rollback est automatique au stage 5 en cas de drift ou de sonde rouge.

---

## 9. Sécurité (conventions AGENTS.md)

- **Aucun secret dans les configs ni les templates** : uniquement des placeholders
  `${PIPELINE_*}` résolus par le store de secrets au moment de l'application.
- Le stage 1 bloque tout secret littéral (porte `secret_scan`).
- Variables d'env préfixées `PIPELINE_*` (convention de préfixe par projet d'AGENTS.md) ;
  `.env.example` versionné, `.env` jamais commité.
- Portes : les valeurs dérivées ne transitent jamais par les logs de la CI.

---

## 10. Adapter le scaffold à un domaine

Pour brancher un nouveau domaine (ou un projet de l'espace de travail) :

1. Copier `templates/pipeline-config.template.yaml` dans le projet cible.
2. Renseigner `meta.domain`.
3. Implémenter l'**adaptateur de domaine** (tests du stage 2 + sonde e2e du stage 5) :
   - *rag* → rebuild + query smoke ;
   - *guardrail* → policy apply + check fixtures ;
   - *infra* → `docker compose config` + `/health`.
4. Pointer le workflow CI (`templates/ci-workflow.github-actions.template.yaml`) sur
   le répertoire `config/` du projet et ses commandes de test.

**Mapping avec l'outillage existant de l'espace de travail**

| Porte / étape | Outillage existant |
|---|---|
| Lint Python | `ruff check` (`ispaces/code/api`) |
| Tests | `pytest` (221 tests verts sur `ispaces/code/api`) |
| Validation infra | `docker compose config -q` |
| Domaine rag | `POST /v1/rag/rebuild`, `POST /v1/rag/query` |
| Domaine garde-fous | `POST /api/v1/admin/guardrail/configure/policies`, `POST /api/v1/guardrails/check`, `POST /v1/llm/generate` |
| Santé | `GET /health` (ispaces API) |

---

## 11. Contenu du scaffold

```
pipeline-ci-scaffold/
├── README.md                                # ce runbook (workflow + checklists)
├── templates/
│   ├── pipeline-config.template.yaml        # modèle d'artefact PipelineConfig
│   ├── ci-workflow.github-actions.template.yaml  # pipeline CI (stages 1-5)
│   ├── release-record.template.md           # enregistrement d'audit de promotion
│   └── .env.example                         # variables CI préfixées PIPELINE_*
└── schema/
    └── pipeline-config.schema.json          # schéma JSON (porte structurelle)
```

---

## 12. Glossaire

- **PipelineConfig** : artefact YAML immuable et versionné décrivant un pipeline.
- **Porte (gate)** : condition bloquante d'avancement (machine ou humaine).
- **Vue rendue** : résolution d'une config par environnement (Fondement → Vue).
- **Adaptateur de domaine** : la part spécifique (tests + sonde e2e) d'un domaine.
- **Drift** : écart entre le checksum servi par l'environnement et le checksum promu.
- **Release record** : enregistrement d'audit d'une promotion (qui, quoi, quand, checksums).
