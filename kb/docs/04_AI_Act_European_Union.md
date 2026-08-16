# EU AI Act — Applicable Requirements

Summary of the AI Act obligations relevant to Alloba's use of AI in a B2B
marketplace gateway.

## Classification

- Alloba's sourcing assistant and compliance knowledge engine provide
  **information and advice** to buyers. They are not used for automated
  enforcement, credit scoring, or decisions producing legal effects.
- The system is therefore treated as **limited risk** under the AI Act
  (transparency obligations apply; high-risk obligations do not, unless a
  deployment changes the classification).

## Transparency obligations (Article 50)

- Users must be informed that they are interacting with an AI system.
- AI-generated content must be identifiable as such (for example, sourcing
  briefs are labelled as AI-drafted).
- The AI must not be presented as human.

## Good practices adopted anyway

- **Risk assessment** recorded for each AI feature before release.
- **Data governance**: training and retrieval material is documented and kept
  accurate; the knowledge base refuses unsafely serialised (pickle) indices.
- **Technical documentation**: model, base URL, temperature, grounding and
  fallback behaviour are configurable and documented.
- **Logging**: interactions are recorded for traceability and audits.
- **Human oversight**: no fully automated decisions that affect rights.

## Monitoring for change

The classification must be revisited if Alloba is ever used for:

- biometric identification;
- scoring of natural persons' creditworthiness;
- automated determination of supplier eligibility with legal effects;
- any output that leads directly to legal or similarly significant consequences.
