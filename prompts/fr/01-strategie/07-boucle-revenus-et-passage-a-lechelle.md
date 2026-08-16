# Phase 2 : Boucle revenus & passage à l'échelle (mois 4-9) — cap sur la trésorerie

Objectif : réinvestir le revenu immédiat dans la complexité d'automatisation et
les coûts de conformité juridique uniquement lorsque c'est nécessaire pour ouvrir
de nouveaux marchés.

| Domaine d'automatisation | Stratégie de gestion des fonds (utiliser ~10 k$ prudemment) | Métrique ROI / étape d'action |
| --- | --- | --- |
| Ops juridiques & conformité (préparation audit ISO) | Ne pas payer de consultants coûteux immédiatement. Utiliser des outils juridiques IA + documentation ISO open source pour rédiger soi-même les documents d'analyse d'écart pour les 5 premiers pays. Investissement : 0 $ jusqu'à ce qu'un audit externe soit exigé par un contrat majeur (<10 k$) ; ensuite, utiliser les revenus. | — |
| Montée en charge technique (coûts GPU) | Ne pas louer de gros GPU. Utiliser la **distillation de modèles** : entraîner de petits modèles locaux sur les données du moteur de connaissances ECP sur du matériel bon marché pour l'inférence dans les régions à faible bande passante. N'envoyer les appels complexes de traduction inter-pays à des API payantes que lorsque c'est absolument nécessaire (<0,10 $/appel). | — |
| Expansion marketing (entrée dans un nouveau pays) | Utiliser la liste de prompts rétro-ingénierés pour rédiger une page d'atterrissage en langue locale (traduite par IA) et la publier automatiquement sur les marketplaces numériques régionales. | Objectif ROI : 3 leads pour 5 $ dépensés. Tuer immédiatement les canaux à <1 % de conversion, avec des données. |

## Application à Alloba

- La passerelle est exclusivement Ollama (ADR-0004) pour une inférence locale et
  économique.
- `ALLOBA_AGENT_TOOL_MODELS` conditionne l'appel d'outils aux modèles déjà
  présents sur l'hôte.
- Chemin de distillation : `scripts/build_index.py` garde un index suffisamment
  petit pour être embarqué sur du matériel modeste.
