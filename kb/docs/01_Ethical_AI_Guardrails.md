# Ethical AI Guardrails

The ispaces design philosophy is **"Ethics by design."** Alloba inherits these
guardrails and applies them to every AI-assisted feature.

## Core principles

1. **Human oversight.** Every consequential action (sourcing decision, compliance
   claim, data classification) is reviewable by a human. AI suggests; humans
   decide.
2. **Grounded answers.** AI responses must cite the sources they rely on. The
   knowledge engine returns `sources` alongside every answer; a response with no
   source is flagged, never presented as fact.
3. **No deception.** The assistant identifies itself as AI. It does not claim to
   be human, to hold certifications, or to have performed actions it has not.
4. **Transparency.** Prompts, models, parameters and failure fallbacks are
   documented and visible. Nothing is hidden in a black box.
5. **Auditability.** Every interaction is logged with a traceable id so it can be
   replayed and audited (see `AuditLogEntry` in the models).

## Guardrail checklist for any new AI feature

- [ ] Is the feature's purpose legitimate and clearly scoped?
- [ ] Does it process the minimum data required (minimisation)?
- [ ] Are outputs grounded in retrievable, citable sources?
- [ ] Is there a human review path for consequential outputs?
- [ ] Are biases (language, geography, gender) assessed and mitigated?
- [ ] Is the feature's use of personal data lawful under GDPR?
- [ ] Is an audit trail produced automatically?
- [ ] Is there a kill switch to disable the feature quickly?

## Enforcement in the codebase

- The FAISS knowledge base refuses pickle-based indices
  (`allow_dangerous_deserialization` is never used).
- The sourcing agent always cites suppliers by name and includes compliance
  context in briefs.
- The chat system prompt instructs the model to say when the context does not
  support an answer.
- Model temperature is kept low (0.2) to favour grounded, deterministic output.
