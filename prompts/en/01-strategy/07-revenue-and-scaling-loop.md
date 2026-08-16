# Phase 2: Revenue & Scaling Loop (months 4-9) — cash focus

Goal: reinvest immediate revenue into automation complexity and legal compliance
costs only where necessary to unlock new markets.

| Automation area | Fund-management strategy (use ~$10k carefully) | ROI metric / action step |
| --- | --- | --- |
| Legal & compliance ops (ISO audit prep) | Do not pay expensive consultants immediately. Use AI legal-tooling + open-source ISO documentation to draft your own gap-analysis documents for the first 5 countries. Investment: $0 until an external audit is required by a major buyer contract (<$10k); once paid, use revenue funds. | — |
| Technical scaling (GPU costs) | Do not rent big GPUs. Use **model distillation**: train small local models on the ECP knowledge-engine data on cheap hardware to run inference in low-bandwidth regions. Only send complex cross-country translation calls to paid APIs when absolutely necessary (<$0.10/call). | — |
| Marketing expansion (new country entry) | Use the reverse-engineered prompts to write a new landing page in the local language (AI translates) and auto-post it on regional digital marketplaces. | ROI goal: 3 leads per $5 spent. Kill channels with <1% conversion immediately, using data. |

## Application to Alloba

- The gateway is Ollama-only (ADR-0004) so inference stays local and cheap.
- `ALLOBA_AGENT_TOOL_MODELS` gates tool-calling to models already on the host.
- Knowledge distillation path: `scripts/build_index.py` keeps the index small
  enough to embed on modest hardware.
