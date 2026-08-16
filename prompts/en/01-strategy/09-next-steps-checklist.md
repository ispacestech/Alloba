# Next steps — immediate checklist

- [ ] **Set up LLM prompts**: copy `CONTRACT-VIGILANCE-01` (see
  `prompts/en/02-prompt-library/compliance-v1-contract-vigilance.md`) into the
  repository as `prompts/compliance_v1.md`. Test locally against a mock contract
  to ensure it flags errors correctly without generating sensitive data leaks
  (ISO requirement).
- [ ] **Configure the serverless pipeline**: create a free account on
  Vercel/Supabase. Link payment-processor API keys in sandbox mode only until
  actual revenue flows, to avoid unexpected charges from high usage.
- [ ] **Automate the marketing funnel**: set up a simple AI agent that scrapes
  LinkedIn job posts for "Procurement Manager" roles in EU/US, summarizes recent
  activity with your platform's value props, and drafts an email pitch using the
  support-tier prompts, sent via Zapier/Automation.io.
- [ ] **Validate the ISO gap**: use AI legal-tech tooling to generate a
  self-assessment report for ISO/IEC 27001 against the specific architecture
  (cloud + LLM). This document is required by buyers before paid contracts.

## Warning: funding vs self-funding

If at any point revenue covers the cost of one developer salary, hire them
immediately. AI cannot yet replace creative strategy or complex negotiations with
banks/VCs. The roadmap assumes **self-sufficiency** until a 6-figure monthly
runway is reached, then transitions to professional team hiring.
