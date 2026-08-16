# Alloba — Architecture d'entreprise

Ce document relie les capacités métier aux capacités informatiques. C'est la
couche « pourquoi » au-dessus de `architecture.fr.md` et `infrastructure.fr.md`.

## Contexte métier

L'entreprise exploite un marché B2B panafricain (ispaces Commerce / AfroMART).
Acheteurs et fournisseurs transactionnent en transfrontalier ; la confiance et
la conformité sont les deux actifs critiques du métier.

## Carte des capacités

| Capacité métier | Capacité IT | Composant propriétaire |
| --- | --- | --- |
| Découvrir des produits | Recherche + filtre catalogue | Alloba `catalog.py` / recherche backend |
| Sourcer intelligemment | Briefs de sourcing agentique | Alloba `sourcing.py` |
| Acheter en confiance | Vérification des fournisseurs | Backend + `kb/docs/05` |
| Rester conforme | Moteur de connaissances de conformité | RAG Alloba (`rag.py`) |
| Intégrer des partenaires | API ouverte + proxy transparent | Alloba `main.py` / `proxy.py` |
| Gouverner la plateforme | Enregistrements de décision, RACI, ADRs | `docs/collaboration/` |
| Opérer de façon éthique | Garde-fous IA + piste d'audit | `kb/docs/01`, `models.py` |

## Principes directeurs

1. **Point d'entrée unique** — la passerelle est le contrat unique pour les
   clients ; le backend plateforme est interchangeable derrière elle.
2. **IA ancrée** — pas de sortie IA sans sources citables.
3. **Conformité d'abord** — les décisions de sécurité et de protection des
   données précèdent les fonctionnalités, et sont enregistrées.
4. **Intégration progressive** — Alloba est autonome .
5. **Opérations bilingues** — les documents métier sont maintenus en EN et FR.

## Parties prenantes et préoccupations

| Partie prenante | Préoccupation | Où c'est traité |
| --- | --- | --- |
| Acheteurs | Sourcing fiable et rapide | Agent de sourcing, catalogue |
| Fournisseurs | Cotation et vérification équitables | `kb/docs/05_Supplier_Verification.md` |
| Régulateurs | RGPD, ISO 27001, ISO 9001, AI Act | `kb/docs/00`, `12`, `04` |
| Ingénieurs | Code clair et testé | `pyproject.toml`, CI, tests |
| Ops | Déploiement cloud reproductible | `infrastructure.fr.md`, compose |

## Flux de décision

Toutes les décisions qui façonnent ces capacités sont enregistrées via le
système de collaboration : proposition → revue → ADR → implémentation. Voir
`docs/collaboration/system.fr.md`.
