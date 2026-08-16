# Bottleneck identification & removal plan

Three major barriers prevent SMEs (especially in emerging markets) from using
global sourcing platforms. The table maps each barrier to a lean, no-capital
solution.

| Industry bottleneck | Why it blocks entry | Platform solution (no-cost/lean) |
| --- | --- | --- |
| "Trust tax" / due-diligence cost. Proving legitimacy costs a lot; large buyers use expensive consultants for vetting. | Filters out high-quality SMEs who cannot afford ~$50k in compliance software. | **LLM audit & governance engine.** Make compliance free: the AI does the work of a $1,000/hour auditor. Use it as a value-add for network effect rather than charging immediately. |
| "Compliance silo" / jurisdiction lock. Companies in Benin/Togo cannot easily access US/EU supply chains because platform data is incompatible with GDPR/Swiss security laws due to server location. | A vendor in Cotonou is treated as a "high-risk data entity", excluded from European e-commerce operations (e.g. Amazon/FairTrade standards). | **Sovereign cloud architecture.** Open-source code hosted on compliant infrastructure (EU data centers) even if the legal entity starts elsewhere. Use the ECP knowledge engine to bridge regulatory gaps dynamically before they are built into contracts. |
| "Working capital gap". Buyers want net-30; vendors need cash for raw materials immediately. Banks in emerging markets say no without collateral. | Platforms like Alibaba require deposits or bank loans most African/Asian SMEs cannot secure. | **Transaction-based trust scoring.** An AI audit layer creates a "trust score" independent of credit score (based on order completion history). Integrate with payment providers that accept this trust signal for immediate payouts, rather than holding funds in escrow. |

## Removal strategy

- **Month 0-3**: launch a free-tier LLM audit engine to vendors in exchange for
  their clean data. This builds the ISO-compliant knowledge graph.
- **Month 4+**: use AI-generated content marketing (from the prompt library) to
  demonstrate compliance standards automatically, cutting acquisition cost per
  customer by ~80%.

## Application to Alloba

- Free compliance checks are exposed via `POST /v1/sourcing/tools/compliance`
  and grounded in `kb/docs/` sources.
- The "sovereign cloud" principle maps to `kb/docs/06_Data_Sovereignty_Africa.md`
  and ADR-0004 (local-first Ollama).
