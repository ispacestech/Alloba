# Alloba — Système de collaboration

Un système de collaboration léger, basé sur les documents, pour le projet
Alloba. Il est volontairement **pas un service** : il vit dans le dépôt pour que
les décisions voyagent avec le code.

## Objectifs

1. Chaque décision conséquente est écrite et retrouvable.
2. Les responsabilités sont explicites (RACI), pour que rien n'attende un
   « quelqu'un ».
3. Les changements passent par un workflow reproductible avec des jalons de
   décision clairs.
4. L'historique des décisions est bilingue au niveau du résumé et précis dans
   les ADRs.

## Artefacts

| Artefact | Emplacement | Rôle |
| --- | --- | --- |
| ADR | `docs/collaboration/adrs/NNNN-*.md` | Enregistrement de décision d'architecture |
| Demande de décision | `docs/collaboration/templates/decision-request-template.md` | Gabarit de proposition |
| RACI | `docs/collaboration/templates/raci-template.md` | Matrice de responsabilités |
| Gabarit ADR | `docs/collaboration/templates/adr-template.md` | Squelette d'ADR |
| Journal des décisions | `docs/collaboration/decision-log.{en,fr}.md` | Index de synthèse (bilingue) |
| Doc du système | ce fichier (system.en.md / system.fr.md) | Définition du processus |

## Workflow

```
1. Décider  → l'auteur rédige une demande de décision avec le gabarit
2. Revue    → les propriétaires concernés revoient ; jalon : approbation du propriétaire
3. Enregistrer → l'ADR est fusionné (scripts/new-adr.py), le journal mis à jour
4. Construire → l'implémentation part de la décision
5. Vérifier  → la CI (lint + tests) doit passer avant fusion
6. Clôturer  → la PR d'implémentation référence le numéro d'ADR
```

## Jalons de décision

| Jalon | Déclencheur | Qui décide | Enregistré comme |
| --- | --- | --- | --- |
| Proposition acceptée | demande de décision complète | propriétaire d'ADR | nouvel ADR |
| Changement d'architecture | touche composants/flux | propriétaire architecture | ADR + doc architecture |
| Posture de sécurité | touche les règles de sécurité | propriétaire sécurité | ADR (obligatoire) |
| Changement de specs | modifie le comportement | propriétaire produit | mise à jour specs + ADR |
| Release | CI verte, image construite | mainteneur | tag git + Docker Hub |

## RACI (niveau macro)

| Activité | R | A | C | I |
| --- | --- | --- | --- | --- |
| Rédaction d'ADR | auteur | propriétaire architecture | leads techniques | équipe |
| Décisions de sécurité | propriétaire sécurité | propriétaire architecture | juriste | équipe |
| Changements de specs | propriétaire produit | propriétaire produit | leads techniques | équipe |
| Contenu du KB | propriétaire contenu | propriétaire sécurité | DPO | équipe |
| Changements de code | développeur | lead technique | relecteurs | équipe |

Légende : R = Réalise, A = Approuve, C = Consulté, I = Informé.

## Règle de langue

- ADRs et gabarits : **anglais** (enregistrements techniques canoniques).
- Journal des décisions et docs de processus : **EN + FR** côte à côte.

## Guide pour une nouvelle décision

```bash
python scripts/new-adr.py "Titre de la décision"
# → crée docs/collaboration/adrs/NNNN-titre-de-la-decision.md
```

## Conventions

- Un ADR par décision. Les ADRs remplacés gardent leur numéro et pointent vers
  le remplaçant.
- Les messages de commit sur les artefacts de décision référencent l'identifiant
  d'ADR (ex. `docs: record ADR-0002`).
- Les décisions ne restent jamais dans les conversations ; elles doivent aboutir
  dans le journal des décisions.
